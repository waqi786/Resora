# Resora v5.0 — AI-Powered Research Operating System

**Resora** is a high-performance, AI-driven desktop ecosystem designed to modernize the academic research workflow. Built for scholars, PhD candidates, and research teams, it automates the most time-consuming parts of literature review, from discovery and screening to synthesis and citation management.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/UI-PyQt5-orange.svg)](https://pypi.org/project/PyQt5/)
[![FAISS](https://img.shields.io/badge/Search-FAISS-green.svg)](https://github.com/facebookresearch/faiss)
[![Transformers](https://img.shields.io/badge/AI-Transformers-red.svg)](https://huggingface.co/docs/transformers/index)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Core Research Capabilities

Resora is not just a search tool; it is a full-cycle Research Operating System that integrates:

*   **Semantic Discovery**: Search over 50,000+ ArXiv papers using FAISS (Facebook AI Similarity Search) and Sentence-Transformers. It understands context, not just keywords.
*   **Neural Summarization**: Automated abstract condensation using `BART-large-cnn` models, providing plain-English insights from dense academic text.
*   **LitRev-AI Screening**: A systematic literature review assistant that uses a PubMedBERT-based classifier to help you make Inclusion/Exclusion decisions faster.
*   **Paper Analysis Engine**: Deep analysis of methodology, contributions, limitations, and future work directly from the abstract.
*   **PRISMA 2020 Flow**: Automated generation of publication-ready PRISMA flow diagrams (PDF/PNG) based on your screening sessions.
*   **Research Workspace**: A centralized project manager for bookmarks, reading lists, task tracking, and citation exports.

---

## 🛠️ Technical Stack

| Component | Technology |
| :--- | :--- |
| **Programming Language** | Python 3.11+ |
| **Frontend Interface** | PyQt5 (Modern Slate/Indigo SaaS Theme) |
| **Vector Database** | FAISS (High-speed similarity search) |
| **NLP Models** | Transformers (BART, Sentence-Transformers, PubMedBERT) |
| **Storage** | SQLite with WAL journaling (Robust local database) |
| **Data Processing** | NumPy, Pandas, Scikit-learn |
| **Visualizations** | Matplotlib (PRISMA & Trend Analytics) |

---

## 📂 Repository Submission Structure

| Folder / File | Description |
| :--- | :--- |
| **App Source Code** | The primary Python/PyQt5 application code. |
| **Model Training** | Jupyter notebooks for dataset processing and classifier training. |
| **Model Artifacts** | Backups of fine-tuned models and system artifacts. |
| **Data Resources** | ArXiv metadata guides and external dataset reference links. |
| **Documentation** | Detailed Word/PDF technical reports and project proposal files. |
| **Visuals** | High-resolution UI screenshots of all modules. |
| **Video Demo** | 1080p demonstration video showing the full system workflow. |

---

## 🚀 Getting Started

### Prerequisites
*   Windows 10/11, macOS, or Linux.
*   Python 3.11 or higher installed.
*   At least 4GB of RAM (8GB recommended for Transformers).

### Installation

1.  **Clone and Navigate**:
   ```bash
   cd "Code full Backend + Frontend/App"
   ```

2.  **Run Setup (Windows)**:
    This script ensures PyTorch is installed correctly for CPU to avoid DLL errors.
   ```powershell
   ./setup_fix.bat
   ```

3.  **Manual Install (Linux/macOS)**:
   ```bash
   pip install -r requirements.txt
   ```

### Launching Resora

   ```bash
   python main.py
   ```

---

## 🧩 Module Breakdown

### 1. Smart Search (Semantic Retrieval)
Uses a FAISS vector index of 50,000+ ArXiv papers. It allows researchers to find papers based on "ideas" rather than just keywords. If the model fails to load, the system falls back to an optimized TF-IDF search.

### 2. Paper Analysis Engine
Detects the research type (Survey, Empirical, Theoretical), methodology, contributions, and potential limitations. It also generates research hypotheses and provides a "Novelty/Reproducibility" score.

### 3. Literature Screening (PRISMA Support)
Allows users to import CSV lists of papers and perform systematic screening. The system provides AI-suggested scores for inclusion/exclusion, tracks all decisions in an audit log, and generates PRISMA 2020 diagrams.

### 4. AI Research Assistant
An integrated Chat interface specialized in research methodology, statistical explanation, and study design advice.

### 5. Research Workspace
A robust project management system. Each project has its own paper collection, task manager with deadlines, and reading progress tracking.

---

## 🔐 Access & Demo Credentials

*   **Admin Email**: `admin@trilit.ai`
*   **Admin Password**: `admin123`
*   **Promo Codes**: `RESORA2026`, `PHD2024`, `UNIVERSITY2024` (For upgrading plans).

---

## ⚠️ Large File Management (Git LFS)

This project uses **Git LFS** (Large File Storage) for high-performance indices and model files:
*   `arxiv_faiss.index` (Vector Index)
*   `arxiv_embeddings.npy` (Numpy Embeddings)
*   `trilit_ai_vscode.zip` (Project Backup)

If cloning without LFS, please ensure these files are manually placed in the `App/data/` folder.

---

## 📈 Implementation Details
*   **Architecture**: Decoupled Model-View-Controller (MVC) pattern.
*   **Database**: SQLite with WAL (Write-Ahead Logging) for safe multi-threaded access.
*   **ML Fallbacks**: Heuristic sentence scoring is used if Transformer models are unavailable, ensuring zero-downtime.
*   **UI**: Custom stylesheet (QSS) implementation for a modern, responsive Dark Mode.

---

## 📄 License

Distributed under the **MIT License**. This project is submitted as a final NLP project for the 6th Semester.

**Developed by:** Waqar Ali (waqi786)