# 🧠 DICOM-to-BIDS Conversion Pipeline  
*A Python-based workflow for MRI datasets with optional physiological data extraction*
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
conda activate dicom2bids```

## 3.3 Install Required Packages
using pip : 
```
pip install -r requirements.txt
```

using conda : 
```
conda install --file requirements.txt
```

