# 🧠 DICOM-to-BIDS Conversion Pipeline  
The goal of this project is to convert raw MRI data from DICOM format to BIDS (Brain Imaging Data Structure) format using a Python-based workflow for the Center for Precision Psychiatry. The steps are designed for users with little or no coding experience. 

This repository provides a **fully automated workflow** for converting raw MRI **DICOM** datasets into **BIDS (Brain Imaging Data Structure)** format.  
It supports:

- multi-center MRI datasets  
- heterogeneous `.puls` physiology formats  
- automatic anonymized ID mapping via Excel  
- `dcm2bids` + `pydeface`  
- physiology extraction into BIDS-compatible `physio.tsv.gz` files  

The entire workflow is beginner-friendly and requires minimal coding knowledge.

---

## 🚀 Features

✔ Batch conversion of full DICOM datasets  
✔ Automatic participant ID matching  
✔ Integration with `dcm2bids` and `pydeface`  
✔ Douglas + Allen `.puls` formats supported  
✔ Dry-run mode for sanity checks  
✔ BIDS-compliant physiology output  
✔ Jupyter notebook: run step-by-step, safe and transparent  

---

# 1. 📂 Prepare Your Data

## 1.1 Organize Your Raw DICOM Folders

Each participant should have a folder containing all exported DICOMs, typically named using the center’s internal code:
ID0001/
ID0002/
ID0003/


---

## 1.2 Add Physiological `.puls` Files (optional)

If your scanner exports `.puls` files:

- Place each `.puls` file **inside the same folder as the participant’s DICOMs**

Example:
CPP00291A/
├─ DICOM/
├─ CPP00291A.puls


These files will be converted into BIDS physiology files later.

---

# 2. 🧪 Set Up the Python Environment

You can use either **conda** or **venv**.

## 2.1 Create Environment

```bash
conda create -n dicom2bids python=3.12
conda activate dicom2bids
```

## 3.3 Install Required Packages

using pip : 
```
pip install -r requirements.txt
```

This will install all the packages listed in a document called requirements.txt in the code. If you are using a cond environment, you can also write : 
```
conda install --file requirements.txt
```
# 3. ⚙️ Configure the Conversion Notebook

The workflow is executed through a Jupyter Notebook (e.g., Dicom2BIDS.ipynb).

## 3.1 Define Paths Inside the Notebook

At the top of the notebook you will define:
📁 DICOM directory
```
dicom_dir = "/path/to/sourcedata/"
```
📁 Output BIDS directory
```
bids_dir = "/path/to/BIDS_output/"
```
🧬 dcm2bids JSON configuration
```
config = "/path/to/dcm2bids_config.json"
```
📊 Excel mapping file
```
excel_mapping_file = "/path/to/CPP_mapping.xlsx"
```
| RawID (from DICOM folder name) | BIDS_ID (anonymized ID) |
| ------------------------------ | ----------------------- |
| ID000011A                      | SDF45589                |
| ID000012A                      | KVG89943                |

 # 4. ▶️ Run the Conversion Notebook

The notebook is divided into clear execution blocks:

1. Import dependencies
2. Define input/output paths
3. Load subject mapping
4. Helper functions
5. Run DICOM → BIDS conversion (dcm2bids)
6. Run pydeface
7. Physio extraction


8. Dry-run diagnostics
👩‍💻 Executing Cells

To run a cell:

Click inside the cell

Press Shift + Enter

Run the notebook top to bottom, but wait until the large DICOM → BIDS conversion block completes before moving on.

Recommended Workflow

Run all cells up to DICOM → BIDS conversion

Wait until all subjects finish converting

Run the dry-run physiology checker

If .puls files are detected, run the appropriate converter:

Douglas physiology converter

Allen physiology converter

Why two converters?
Because scanners at different centers generate .puls files with different formats.
