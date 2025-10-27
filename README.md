# 🐍 Python Project Setup and Run Guide

This guide explains step-by-step how to install **Python**, set up the environment, install dependencies from `requirements.txt`, and run the project (`main.py`).

---

## ℹ️ About the Project

This project is a Python application that can be run using `main.py`.  
It requires some external libraries which are listed in `requirements.txt`.

---

## 1. Install Python

Before starting, you must have **Python 3.8 or higher** installed.

### 🔽 Download Python
Go to the official website and download the latest version:

👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

### 🪟 Windows Installation Steps
1. Download the **Windows installer (64-bit)**.
2. Run the installer.
3. **Check the box “Add Python to PATH”** before clicking “Install Now”.
4. After installation, verify Python is available:
   ```bash
   python --version

## 2. Set Up a Virtual Environment

# Create a virtual environment named 'venv'
python -m venv <folder_name>

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

## 3. Install Dependencies

pip install -r requirements.txt
or
python -m pip install -r requirements.txt

## 4. Run the Project

python main.py

## 5. Deactivate Virtual Environment

deactivate