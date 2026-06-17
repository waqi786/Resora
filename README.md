# 🛡️ Resora v5.0 — The AI-Powered Research Operating System

**Resora** is a cutting-edge, high-performance desktop ecosystem engineered to revolutionize the academic research lifecycle. Designed specifically for scholars, PhD candidates, and institutional research teams, it automates the most grueling aspects of literature reviews—from high-speed semantic discovery and systematic screening to neural synthesis and PRISMA-compliant reporting.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/UI-PyQt5-orange.svg)](https://pypi.org/project/PyQt5/)
[![FAISS](https://img.shields.io/badge/Search-FAISS-green.svg)](https://github.com/facebookresearch/faiss)
[![Transformers](https://img.shields.io/badge/AI-Transformers-red.svg)](https://huggingface.co/docs/transformers/index)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![LFS](https://img.shields.io/badge/Data-Git%20LFS-blueviolet.svg)](https://git-lfs.github.com/)

---

## 🌟 Executive Summary: Core Research Capabilities::

Resora transcends traditional reference management by providing a unified, AI-native workspace. It integrates advanced Natural Language Processing (NLP) with high-speed vector retrieval to solve the "Information Overload" problem in modern academia.

### 🔑 Key Modules:
*   **🧠 Semantic Discovery Engine**: Leveraging **FAISS** (Facebook AI Similarity Search) and `all-MiniLM-L6-v2` transformers to search 50,000+ papers based on conceptual meaning rather than rigid keywords.
*   **📝 Neural Synthesis (Summarization)**: Utilizing `BART-large-cnn` architecture to condense dense academic abstracts into coherent, plain-English executive summaries.
*   **⚖️ LitRev-AI Systematic Screening**: An advanced screening assistant using **PubMedBERT**-based classification to suggest Inclusion/Exclusion decisions, complete with a full decision audit trail.
*   **📊 PRISMA 2020 Automation**: Generate publication-standard PRISMA flow diagrams (PDF/PNG) dynamically based on your screening sessions.
*   **🔍 Deep Paper Analysis**: An automated extraction engine that identifies Research Methodologies, Contributions, Limitations, and Future Work from abstract text.
*   **📅 Unified Research Workspace**: A centralized hub for project-based organization, task management with deadlines, and multi-format citation exports (BibTeX, RIS, EndNote).

---

## 📂 Detailed Submission Structure

This repository contains the full 6th-semester NLP project submission. Below is the comprehensive directory map:

| Component | Path | Description |
| :--- | :--- | :--- |
| **🚀 Core Software** | `Code full Backend + Frontend/App` | The production-ready Python/PyQt5 application. |
| **📓 Model Training** | `Code Model Training & Other Things` | Jupyter notebooks for BERT fine-tuning and data preprocessing. |
| **📦 Artifacts** | `Code Output like model etc` | Fine-tuned model weights and system backup zips. |
| **💾 Data Assets** | `Data` | Metadata guides, data dictionaries, and reference dataset links. |
| **📄 Documentation** | `Proposal File` & `Report` | Formal project proposal, SRS, and 50+ page technical report. |
| **📸 Visual Media** | `Screenshots` | High-definition UI/UX walkthrough images. |
| **🎬 Demonstration** | `Video` | A 1080p full-length system demonstration video. |

---

## 🛠️ Full Technical Architecture

| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.11+ (Optimized for Windows/Linux/macOS) |
| **GUI Framework** | PyQt5 with custom QSS (Slate/Indigo SaaS aesthetics) |
| **Vector Retrieval** | FAISS (Facebook AI Similarity Search) with Inner Product indexing |
| **NLP Core** | Hugging Face Transformers, Sentence-Transformers, NLTK |
| **Summarizer** | `facebook/bart-large-cnn` (Conditional Generation) |
| **Database** | SQLite3 with **WAL Journaling** and Foreign Key constraints |
| **Financials** | Stripe API Integration (Subscription & Credit logic) |
| **Visuals** | Matplotlib (PRISMA flow generation) |

---

## 🚀 Quick Start & Installation:

### 💻 Windows Setup (Recommended)
Windows users should use the provided `setup_fix.bat` to ensure **CPU-only PyTorch** is installed correctly, preventing common DLL errors.

1.  **Navigate to App Folder**:
    ```powershell
    cd "Code full Backend + Frontend/App"
    ```
2.  **Execute Fix Script**:
    ```powershell
    ./setup_fix.bat
    ```
3.  **Run Application**:
    ```powershell
    python main.py
    ```

### 🐧 macOS / Linux Setup
```bash
cd "Code full Backend + Frontend/App"
pip install -r requirements.txt
python main.py
```

---

## 🧠 Module Deep-Dive

### 1. The Research Workspace
A robust project-management layer. Each project allows users to:
*   Track paper reading status (Unread, Reading, Done).
*   Assign task priorities (High, Medium, Low) with deadlines.
*   Consolidate AI summaries and analysis results per project.

### 2. Systematic Screening & PRISMA
Designed for SLR (Systematic Literature Reviews):
*   **Heuristic + ML Scoring**: Calculates a probability score for paper inclusion.
*   **Session Persistence**: Save screening sessions to resume later.
*   **Export**: Generate a full audit log in CSV and a PRISMA 2020 diagram.

### 3. AI Research Assistant (Chat)
An expert system specialized in academic queries:
*   Explains complex statistical concepts (P-values, ANOVA, etc.).
*   Suggests appropriate research methodologies based on study aims.
*   Provides templates for writing hypotheses and research gaps.

### 4. Admin & Billing System
A production-ready SaaS module:
*   **Stripe Checkout**: Integrated payment flow for Pro/University plans.
*   **Promo Codes**: Logic for `RESORA2026`, `PHD2024`, etc.
*   **Admin Dashboard**: Manage user tiers, revenue tracking, and support tickets.

---

## 🔐 Access & Credentials

| User Type | Email | Password |
| :--- | :--- | :--- |
| **System Admin** | `admin@trilit.ai` | `admin123` |
| **Guest User** | N/A | Click "Continue as Guest" |

---

## ⚠️ Data Integrity & Large Files (Git LFS)

This repository uses **Git LFS** to manage high-dimensional vector data and model artifacts. Ensure you have Git LFS installed to pull the following critical files:
*   `arxiv_faiss.index`: 250MB+ vector index.
*   `arxiv_embeddings.npy`: Pre-computed research embeddings.
*   `trilit_ai_vscode.zip`: Full workspace backup.

---

## 🗺️ Roadmap & Future Enhancements
*   [ ] **Multi-Agent RAG**: Integration of local PDF parsing for full-paper Q&A.
*   [ ] **Cloud Sync**: Optional PostgreSQL backend for team-wide collaboration.
*   [ ] **Zotero Integration**: Direct sync with Zotero/Mendeley libraries.

---

## 📄 Project Attribution

Developed by **Waqar Ali** (waqi786) as a Project (6th Semester NLP).
**Institution**: University Research Submission.
**License**: MIT License.

*Special thanks to Cornell University for the ArXiv dataset.*
