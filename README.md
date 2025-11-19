# 🧠 DICOM-to-BIDS Conversion Pipeline  
The goal of this project is to convert raw MRI data from DICOM format to BIDS (Brain Imaging Data Structure) format using a Python-based workflow. The steps are designed for users with little or no coding experience. 

This repository provides a **fully automated workflow** for converting raw MRI **DICOM** datasets into **BIDS (Brain Imaging Data Structure)** format.  
It supports:

- multi-center MRI datasets  
- heterogeneous `.puls` physiology formats  
- automatic anonymized ID mapping via Excel  
- `dcm2bids` + `pydeface`  
- physiology extraction into BIDS-compatible `physio.tsv.gz` files  

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
ID000001A/
├─ DICOM/
├─ ID000001A.puls


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

Using pip : 
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
For the Excel file, make sure that you use the first two column of the excel file (or adapt in directly in the code with df.iloc) and that your file is made of the (1) alphanumerical code you want to assign to your participant and (2) it’s original ID, as shown in this table:  

| BIDS_ID (anonymized ID) | RawID (from DICOM folder name) |
| ------------------------| ------------------------------ |
| SDF45589                | ID000011A                      |
| KVG89943                | ID000012A                      |

 # 4. ▶️ Run the Conversion Notebook

The notebook is divided into clear execution blocks:

1. Import your package 
2. Set your DICOM and BIDS path (change as needed) 
3. Helper function (custom function in python that will be used later in the script) 
4. DCM2BIDS conversion + Pydeface 
5. Bidsphysio conversion 


You can either run all cells, or use the dicom2bids.py file to run the whole script in one go.
