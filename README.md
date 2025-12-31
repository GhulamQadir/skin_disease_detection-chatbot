# Skin Disease Detection Chatbot

A Python-based prototype **Skin Disease Detection Chatbot** using **OpenCV feature matching** for detecting common skin conditions and **Streamlit** for a simple web UI. This project is implemented following **OOP principles**, with modular components for easy maintainability and extensibility.

---

## Project Overview

- Detects skin diseases from user-uploaded images using **feature matching** (OpenCV ORB descriptors).  
- Displays educational **description and treatment** information for detected conditions.  
- Includes a **disclaimer**: for educational purposes only, not professional medical advice.  
- UI built using **Streamlit** for easy interaction.
  
---

## 📂 Folder Structure

```text
chatbot/
├── app/
│   └── app.py                  # Streamlit App class and UI logic
├── descriptor_manager/
│   └── des_manager.py          # Feature extraction & matching
├── image_loader/
│   └── loader.py               # Image preprocessing and loading
├── image_processor/
│   └── processor.py            # Orchestrates matching & classification
├── disease_info/
│   └── disease_info.py         # Disease info dictionary
├── data/
│   └── disease.json            # JSON data for diseases
├── main.py                     # Entry point
├── Scripts/
│   ├── data_preprocessor.py    # Dataset standardization script
│   └── test.py                 # Test script for Preprocessor
├── requirements.txt            # Dependencies
└── .gitignore                  # Git ignore file
```

## Features

- **OOP Design**: Modular structure for easy maintenance and scalability  
- **Image Preprocessing**: Converts to grayscale, resizes, and standardizes images  
- **Feature Matching**: Uses ORB descriptors with Brute-Force matcher  
- **Interactive UI**: Streamlit interface for uploading images and displaying results  
- **Disclaimer**: Ensures user awareness that the app is educational  

---

## Dataset Preprocessing

A utility script in `Scripts/data_preprocessor.py` helps to prepare the dataset:

- Users provide a **root folder** with subfolders named after each disease.  
- The script copies a **limited number of images** from each folder into the central `dataset/` folder.  
- It **standardizes file names** for consistency (`1.jpg, 2.jpg, …`).  

Example usage:

```python
from dataset_preprocessor import DatasetPreprocessor

root_path = "dataset"
folders = ["Melanoma", "Chickenpox", "Herpes", "Eczema", "Acne", "Lupus"]

preprocessor = DatasetPreprocessor(root_path, folders)
preprocessor.prepare_dataset(max_files=50)
```

### How To Run
- git clone [https://github.com/GhulamQadir/skin_disease_detection-chatbot.git]
- pip install -r requirements.txt
- cd chatbot
- python main.py
