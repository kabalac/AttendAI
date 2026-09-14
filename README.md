# 🎓 AttendAI

**AI-powered classroom attendance from a single photograph.**

AttendAI uses computer vision and face recognition to identify registered students from a classroom/group photograph and automatically generate an attendance record.

## ✨ Features

- 📷 Upload a classroom photograph
- 👤 Detect multiple faces
- 🤖 Recognize registered students using AI
- ❓ Identify unknown faces
- 📊 Calculate attendance
- 📝 View attendance with student details
- 📥 Download attendance as CSV
- 📊 Download attendance as Excel

## 🛠️ Technology Stack

- Python
- Streamlit
- OpenCV
- InsightFace
- ONNX Runtime
- Pandas
- OpenPyXL

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/kabalac/AttendAI.git
cd AttendAI
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run AttendAI

```bash
streamlit run app.py
```

The application will open in your browser.

## 📁 Project Structure

```text
AttendAI/
├── app.py
├── recognition.py
├── visualize.py
├── test_recognition.py
├── requirements.txt
├── data/
│   └── students/
└── assets/
    └── classroom_images/
```

## 🎯 Project Workflow

```text
Classroom Image
       ↓
Face Detection
       ↓
Face Recognition
       ↓
Attendance Generation
       ↓
CSV / Excel Export
```

## 🔒 Privacy

The demo uses locally stored face images for recognition.

Real student photographs should only be used with appropriate consent and should be stored securely.

## 📌 Project Status

**Current version:** Student Demo MVP

Future improvements may include:

- Student management
- Attendance history
- Teacher dashboard
- Multiple classes and subjects
- Improved recognition handling
- Database integration
- Cloud deployment

---

Built as an AI/Computer Vision student project demonstration.
