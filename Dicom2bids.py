#!/usr/bin/env python
# coding: utf-8

# ## Import your package
# You will need all of these packages to run the following script in order to convert your scans from DICOM to BIDS.

# In[3]:


import os
import subprocess
import logging
import glob
import random
import string
import csv
import shutil
import pandas as pd
import openpyxl



# Setup logging
logging.basicConfig(
    filename="bids_conversion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

os.chdir("/media/administrator/Scratch/dcm2bids-cpp/code")


# ## Set your DICOM and BIDS path (change as needed)
# 
# In this cell, you will find the path that you need to set up for the scan conversion, such as
# - The path where you store your DICOM files (named : dicom_dir)
# - The folder where you want you BIDS files to be stored (named : bids_dir)
# - The json file that dcm2bids will use to know which file to convert (named : config)
# - A path to an excel file that includes (1) the alphanumerical number for each participant on the left column as well as (2) the coded name of the participant on the right column (named : excel_mapping_file) 

# In[4]:


# Define your paths here 
dicom_dir = ''
bids_dir = ''
config = ''
session = "01"   # ex: "01", "02", etc.
excel_mapping_file = ''



# ## Helper function ##
# This cell has been made to create custom functions that will be used later for the conversion of all our DICOM into BIDS format, such as
# - run_dcm2bids
# - run_pydeface
# - run_bidsphysio

# In[3]:


def run_dcm2bids(orig_id, anon_id, dicom_dir, bids_dir, config, session="1"):
    """
    Convert DICOM to BIDS if not already converted.
    """
    subject_bids_dir = os.path.join(bids_dir, f"sub-{anon_id}", f"ses-{session}")

    # ✅ Skip if participant/session already converted
    if os.path.exists(subject_bids_dir) and any(os.scandir(subject_bids_dir)):
        logging.info(f"✅ Participant {anon_id} (session {session}) already converted. Skipping dcm2bids.")
        return

    cmd = [
        "dcm2bids", 
        "-d", os.path.join(dicom_dir, orig_id),
        "-p", anon_id,
        "-s", session,
        "-c", config,
        "-o", bids_dir,
        "--auto_extract_entities"
        
    ]

    logging.info(f"🚀 Running: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
        logging.info(f"✅ Conversion complete for {anon_id}, session {session}.")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Conversion failed for {anon_id}, session {session}: {e}")


def run_pydeface(bids_dir, anon_id, session="1"):
    anat_dir = os.path.join(bids_dir, f"sub-{anon_id}", f"ses-{session}", "anat")
    if not os.path.exists(anat_dir):
        logging.warning(f"No anat directory for sub-{anon_id}, skipping defacing.")
        return
    for nii_file in glob.glob(os.path.join(anat_dir, "*_T1w.nii.gz")):
        cmd = ["pydeface", nii_file]
        logging.info(f"Defacing {nii_file}")
        subprocess.run(cmd, check=True)

def run_bidsphysio(orig_id, anon_id, dicom_dir, bids_dir, session):
    """
    Check for a .puls file in the participant's DICOM directory.
    Returns True if found, False if missing.
    """
    subject_dicom_path = os.path.join(dicom_dir, orig_id)

    has_puls = False
    for root, dirs, files in os.walk(subject_dicom_path):
        for f in files:
            if f.endswith(".puls"):
                has_puls = True
                logging.info(f".puls file found for subject {orig_id} at {os.path.join(root, f)}")
                break
        if has_puls:
            break

    if not has_puls:
        logging.warning(f"No .puls file found for subject {orig_id}")

    return has_puls



# In[ ]:





#  ## DCM2BIDS conversion + Pydeface
# 
#  This is the main script to do the conversion from DICOM to BIDS. Depending on the type of scans you are doing, it might take a while (approx 10-15 mins per scans)

# In[ ]:


# Read Excel file containing raw IDs and anonymized IDs
df = pd.read_excel(excel_mapping_file)
df = df.iloc[:, :2]  # only keep first 2 columns
df.columns = ['AnonymizedID', 'RawID']

# List DICOM folders detected in the input directory
subjects = [
    name for name in os.listdir(dicom_dir)
    if os.path.isdir(os.path.join(dicom_dir, name))
]

not_found = 0
converted = 0
skipped = 0
missing_puls = 0

for folder_name in subjects:
    match_row = None
    folder_name_str = str(folder_name)

    # Try to match each folder name with the "RawID" column in the Excel file
    for _, row in df.iterrows():
        raw_id = str(row['RawID']).strip()
        if raw_id in folder_name_str:
            match_row = row
            break

    if match_row is None:
        print(f"⚠️  No match found in Excel for {folder_name}, skipping.")
        not_found += 1
        continue

    orig_id = folder_name          # name of the DICOM folder
    anon_id = match_row['AnonymizedID']  # anonymized ID from Excel

    # Display confirmation
    print("\n" + "="*60)
    print(f"🧠 Found match:")
    print(f"   📁 DICOM folder : {orig_id}")
    print(f"   🧾 Assigned BIDS ID : {anon_id}")
    print(f"   🔎 Matched Raw ID : {match_row['RawID']}")
    print("="*60 + "\n")

    try:
        # Main conversion steps
        run_dcm2bids(orig_id, anon_id, dicom_dir, bids_dir, config, session)
        run_pydeface(bids_dir, anon_id, session)
        has_puls = run_bidsphysio(orig_id, anon_id, dicom_dir, bids_dir, session)

    except subprocess.CalledProcessError as e:
        logging.error(f"Error with subject {orig_id}: {e}")
        print(f"❌ Error with subject {orig_id}, check logs.")
        df.loc[df['RawID'] == match_row['RawID'], 'NOTES'] = f"Error: {e}"
        skipped += 1


# # Bidsphysio conversion 
# The rest of the script is made of 2 codeblock to convert the .puls file
# 1. Bidsphysio (dry run): This codecell will go through all of your files in your dicom_dir and tell you which file contain a .puls file and which file doesnt
# 2. Bidsphysio (real run):  Codeblock to retrieve the .puls file from the MRIs of the Douglas

# ## Dry run
# Run this cell just to see which of your file contains a .puls file

# In[ ]:


dry_run = True  # ✅ Set to True for simulation (no real conversion)

# -----------------------------
# 📝 Logging
# -----------------------------
log_file = os.path.join(bids_dir, "bidsphysio_dryrun.log")
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

print(f"📜 Dry run logging to: {log_file}")

# -----------------------------
# 📖 Load Excel mapping
# -----------------------------
df = pd.read_excel(excel_mapping_file)
required_cols = {"RawID", "AnonymizedID"}

if not required_cols.issubset(df.columns):
    raise ValueError("Excel file must contain 'RawID' and 'AnonymizedID' columns")

print(f"📖 Loaded mapping for {len(df)} subjects from Excel")

# -----------------------------
# 🔍 Scan folders and identify .puls matches
# -----------------------------
to_convert = []

for root, _, files in os.walk(dicom_dir):
    for f in files:
        if f.endswith(".puls"):

            raw_id_match = None
            for raw_id in df["RawID"]:
                if str(raw_id) in f:
                    raw_id_match = str(raw_id)
                    break

            if not raw_id_match:
                print(f"⚠️ No matching RawID found in Excel for {f}, skipping.")
                logging.warning(f"No match for puls file: {f}")
                continue

            anon_id_series = df.loc[df["RawID"] == raw_id_match, "AnonymizedID"]
            if anon_id_series.empty:
                print(f"⚠️ No AnonymizedID found for {raw_id_match}, skipping.")
                logging.warning(f"No anonymized ID for RawID {raw_id_match}")
                continue

            anon_id = anon_id_series.values[0]
            puls_path = os.path.join(root, f)
            func_dir = os.path.join(bids_dir, f"sub-{anon_id}",
                                    f"ses-{session}", "func")

            to_convert.append({
                "RawID": raw_id_match,
                "AnonID": anon_id,
                "PulsPath": puls_path,
                "FuncDir": func_dir
            })

# -----------------------------
# 🧪 Summary of what WOULD happen
# -----------------------------
print("\n🧪 DRY RUN SUMMARY")
print("="*60)

for i, item in enumerate(to_convert, 1):
    print(f"{i:02d}. {os.path.basename(item['PulsPath'])}")
    print(f"   → Raw ID     : {item['RawID']}")
    print(f"   → Anon ID    : {item['AnonID']}")
    print(f"   → Target dir : {item['FuncDir']}")
    print("-"*60)

print(f"\n📦 Total .puls files found: {len(to_convert)}")
print(f"🧾 Log file: {log_file}")

if dry_run:
    print("\n✅ Dry run complete — no conversions executed.")
    logging.info(f"Dry run complete — {len(to_convert)} potential conversions listed.")
else:
    print("\n❌ dry_run=False — conversions will be executed.")


# ## Bidsphysio : real run
# Run this cell to convert .puls files

# In[ ]:


# -----------------------------
# 📖 Load Excel mapping
# -----------------------------
df = pd.read_excel(excel_mapping_file)
required_cols = {"RawID", "AnonymizedID"}

if not required_cols.issubset(df.columns):
    raise ValueError("Excel file must contain 'RawID' and 'AnonymizedID' columns")

print(f"📖 Loaded mapping for {len(df)} subjects from Excel")

# -----------------------------
# ⚙️ Function to run physio2bidsphysio
# -----------------------------
def run_physio2bidsphysio(puls_path, sub_id):
    func_dir = os.path.join(bids_dir, f"sub-{sub_id}", f"ses-{session}", "func")
    os.makedirs(func_dir, exist_ok=True)
    os.chdir(func_dir)

    cmd = ["physio2bidsphysio", "-i", puls_path, "-b", f"sub-{sub_id}"]
    logging.info(f"Running: {' '.join(cmd)}")
    print(f"🔄 Converting {os.path.basename(puls_path)} → sub-{sub_id}")

    try:
        subprocess.run(cmd, check=True)
        logging.info(f"✅ Converted {puls_path}")
        print(f"✅ Success for {sub_id}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Error converting {puls_path}: {e}")
        print(f"❌ Error for {sub_id}")
        return False

# -----------------------------
# 🚀 Main loop: Find and convert .puls files
# -----------------------------
converted, errors, skipped = 0, 0, 0

for root, _, files in os.walk(dicom_dir):
    for f in files:
        if f.endswith(".puls"):

            raw_id_match = None
            for raw_id in df["RawID"]:
                if str(raw_id) in f:
                    raw_id_match = str(raw_id)
                    break

            if not raw_id_match:
                print(f"⚠️ No matching RawID found in Excel for file {f}, skipping.")
                skipped += 1
                continue

            anon_id_series = df.loc[df["RawID"] == raw_id_match, "AnonymizedID"]
            if anon_id_series.empty:
                print(f"⚠️ No AnonymizedID found for {raw_id_match}, skipping.")
                skipped += 1
                continue

            anon_id = anon_id_series.values[0]
            puls_path = os.path.join(root, f)

            # Convert!
            success = run_physio2bidsphysio(puls_path, anon_id)
            if success:
                converted += 1
            else:
                errors += 1

# -----------------------------
# 📊 Final Summary
# -----------------------------
print("\n📊 Summary:")
print(f"  ✅ Converted: {converted}")
print(f"  ⚠️ Skipped (no match): {skipped}")
print(f"  ❌ Errors: {errors}")

