# Resora: AI-Powered Research Operating System

**Resora** is a comprehensive research assistant designed to solve literature review overload. This repository contains the complete 6th-semester NLP project submission, including the application code, training notebooks, and project documentation.

---

## 📁 Submission Structure

| Folder / File | Description |
| :--- | :--- |
| **[Code full Backend + Frontend/App](./Code%20full%20Backend%20+%20Frontend/App)** | **Main Application Source Code (PyQt5 + Python).** |
| **Code Model Training** | Jupyter notebooks used for model fine-tuning and data preparation. |
| **Code Output like model etc** | Contains project backups and large model artifacts. |
| **Data** | ArXiv metadata dictionary and dataset reference links. |
| **Proposal File** | Initial project proposal (PDF/DOCX). |
| **Report** | Final project report and technical documentation. |
| **Screenshots** | Visual walkthrough of the application's UI. |
| **Video** | Full demonstration video of the system in action. |

---

## 🚀 Quick Start (Running the App)

To run the main application:

1. Navigate to the App directory:
   ```bash
   cd "Code full Backend + Frontend/App"
   ```
2. Install dependencies (Windows users should run the fix script):
   ```powershell
   ./setup_fix.bat
   ```
3. Start the application:
   ```bash
   python main.py
   ```

*For detailed installation steps and feature lists, see the [App/README.md](./Code%20full%20Backend%20+%20Frontend/App/README.md).*

---

## ✨ Key Technical Highlights
- **Semantic Search**: Powered by FAISS and Sentence-Transformers.
- **Neural Summarization**: Uses BART-large-cnn for high-quality abstracts.
- **Paper Analysis**: Automatic methodology and contribution extraction.
- **PRISMA 2020**: Automated flow diagram generation for systematic reviews.

**Developed by:** Waqar Ali (waqi786)