# 🩺 SkinLens AI

> An AI-powered desktop application that classifies skin disease from images using deep learning, built with a clean Tkinter interface and MySQL-backed user authentication.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=flat-square&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-D00000?style=flat-square&logo=keras&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow?style=flat-square)

---

## 📖 Overview

**SkinLens AI** takes an uploaded image of a skin lesion and predicts the most likely condition out of seven categories, along with a confidence score and a simple, human-readable recommendation. It's built as a full desktop application — not just a model in a notebook — with account creation, login, an image upload dashboard, and a polished results page.

The model is trained on the **HAM10000** dataset using transfer learning with **MobileNetV2**, and the entire experience runs locally through a Tkinter GUI styled with an Apple-inspired design system.

> ⚠️ **Disclaimer:** This project is built for educational and academic purposes only. It is **not** a diagnostic tool and should never replace professional medical advice.

---

## ✨ Features

- 🔐 **User Authentication** — Sign up and log in, backed by a MySQL `users` table
- 📤 **Image Upload** — Select a skin image directly from your device
- 🧠 **AI-Powered Prediction** — Classifies the image into one of 7 skin condition categories
- 📊 **Confidence Score** — Displays prediction confidence as a percentage
- 💡 **Smart Guidance** — Context-aware suggestions based on confidence level (e.g., recommending a clearer photo if confidence is low)
- 🎨 **Clean, Apple-Inspired UI** — Multi-page navigation (Home → Auth → Sign Up/Login → Dashboard → Result) with a minimal `#FAFAFA` / `#007AFF` design language

---

## 🧬 Skin Conditions Detected

| Code | Condition |
|------|-----------|
| AKIEC | Actinic Keratoses |
| BCC | Basal Cell Carcinoma |
| BKL | Benign Keratosis |
| DF | Dermatofibroma |
| MEL | Melanoma |
| NV | Melanocytic Nevus |
| VASC | Vascular Lesion |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Language** | Python |
| **Deep Learning** | TensorFlow / Keras (MobileNetV2 transfer learning) |
| **GUI** | Tkinter |
| **Database** | MySQL |
| **Image Handling** | Pillow (PIL) |
| **Dataset** | [HAM10000](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000) |

---

## 🏗️ Project Architecture

```
SkinLens-AI/
│
├── organize.py            # Sorts raw HAM10000 images into class-labeled folders
├── clean_dataset.py        # Caps each class folder to a fixed number of images
├── train.py                # Builds, trains & saves the CNN model
├── predict.py               # Standalone script to test predictions on a single image
├── main.py                  # Full Tkinter desktop application (UI + DB + inference)
├── skin_disease_model.h5    # Trained model weights (generated after training)
└── README.md
```

### How the pieces connect

1. **`organize.py`** reads the HAM10000 metadata CSV and copies each image into a folder named after its diagnosis label, creating a clean `dataset/` directory structure.
2. **`clean_dataset.py`** trims each class folder down to a fixed number of images, keeping the dataset balanced and training time manageable.
3. **`train.py`** loads the organized dataset, applies normalization, trains a CNN, and saves it as `skin_disease_model.h5`.
4. **`predict.py`** is a lightweight script to sanity-check the trained model on a single test image from the command line.
5. **`main.py`** ties everything together into a complete desktop app — handling user sign-up/login via MySQL, image upload, live inference using the trained model, and a results page with confidence-based guidance.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MySQL Server running locally
- The [HAM10000 dataset](https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000) (images + metadata CSV)

### Installation

```bash
git clone https://github.com/<your-username>/SkinLens-AI.git
cd SkinLens-AI
pip install tensorflow pillow numpy mysql-connector-python
```

### Database Setup

Create a MySQL database named `ai_skin_analyser` with a `users` table containing:

```sql
CREATE DATABASE ai_skin_analyser;

USE ai_skin_analyser;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    mobile VARCHAR(15),
    email VARCHAR(100),
    password VARCHAR(100)
);
```

> Update the `connect_db()` credentials in `main.py` to match your local MySQL setup.

### Prepare the Dataset

```bash
python organize.py        # Organizes raw images into class folders
python clean_dataset.py   # Trims each class to a fixed image count
```

### Train the Model

```bash
python train.py
```

This generates `skin_disease_model.h5` in the project root.

### Run the App

```bash
python main.py
```

---

## 🖥️ Application Flow

```
Front Page  →  Auth Page  →  Sign Up / Login  →  Dashboard  →  Result Page
```

1. **Front Page** — Welcome screen introducing SkinLens AI
2. **Auth Page** — Choose to sign up or log in
3. **Dashboard** — Upload a skin image and trigger AI analysis
4. **Result Page** — View predicted condition, confidence %, and guidance

---

## 🔮 Future Improvements

- [ ] Replace plain-text password storage with proper hashing (e.g., bcrypt)
- [ ] Upgrade the CNN to a fine-tuned MobileNetV2/EfficientNet backbone for higher accuracy
- [ ] Add prediction history per user account
- [ ] Package as a standalone executable (PyInstaller)
- [ ] Add unit tests for the prediction pipeline

---

## ⚠️ Disclaimer

This application is a student/academic project intended to demonstrate applied machine learning and software development skills. It is **not a certified medical device** and its predictions should **never** be used as a substitute for professional dermatological diagnosis. Always consult a qualified healthcare provider for any skin health concerns.

---

## 👤 Author

**Gunal**
 Learning ML | Building practical, real-world ML applications

If you found this project interesting, consider giving it a ⭐!
