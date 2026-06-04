# Resora v5.0 — AI-Powered Research Operating System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/UI-PyQt5-orange.svg)](https://pypi.org/project/PyQt5/)
[![FAISS](https://img.shields.io/badge/Search-FAISS-green.svg)](https://github.com/facebookresearch/faiss)
[![Transformers](https://img.shields.io/badge/AI-Transformers-red.svg)](https://huggingface.co/docs/transformers/index)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Resora** is a high-performance desktop research assistant designed for scholars, PhD students, and research teams. It streamlines the literature review process using semantic search, AI-driven analysis, and automated screening.
---

## 🚀 Project Vision
## Overview

Resora is a comprehensive desktop research assistant built in Python with a modern PyQt5 interface, a local SQLite workspace, and fast semantic retrieval over an ArXiv paper corpus. The app is designed for students, PhD scholars, researchers, and research teams who need a single workspace for discovery, analysis, screening, summarization, planning, and citation support.

The application combines:

- Semantic search over 50,000+ ArXiv papers using FAISS + SentenceTransformers
- Fallback TF-IDF search when semantic models cannot load
- Abstract summarization using `facebook/bart-large-cnn` or extractive fallback
- Paper analysis for methodology, contributions, limitations, and impact scoring
- Research gap detection and related-work suggestions
- PRISMA-like screening workflow with session management and export
- Workspace bookmarks, reading list, project tracking, and history
- User authentication, promo codes, credits, billing, and admin dashboard

---

## What this repository contains

- `main.py` — Primary desktop application and user interface built with PyQt5
- `ml_backend.py` — Machine learning backend for semantic search, summaries, screening, and paper analysis
- `database.py` — SQLite persistence layer for users, sessions, bookmarks, summaries, screenings, plans, notifications, tasks, projects, and audit logs
- `requirements.txt` — Python dependency list (Run `pip install -r requirements.txt`)
- `setup_fix.bat` — Windows helper for fixing PyTorch-related installation issues
- `data/` — required model and dataset files
- `assets/` — optional assets and visual resources
- `output/` — runtime output directory created automatically

---

## Key features

### Core research workflows

- Semantic paper discovery with keyword and category filtering
- Similarity-based search and paper recommendation
- Manual and automatic paper bookmarking
- Reading list tracking with status labels: unread, in progress, done
- Export search results to CSV, BibTeX, RIS, and EndNote
- Open selected paper directly on arXiv

### 🧠 AI-Powered Analysis & Summarization
### AI-powered analysis

- Abstract summarization with BART-large-cnn
- Extractive summary fallback when transformer models are unavailable
- Paper analysis engine to detect:
  - research method and methodology
  - main contributions
  - limitations and risks
  - research type and impact score
  - keywords and hypothesis suggestions

### 🛠️ Research Workflow Tools

- Project workspace with paper collections and task tracking
- Search history, summaries history, screening sessions, and bookmarks
- Research gap finder for unexplored directions
- Related-work draft generation and hypothesis building
- Inclusion/exclusion screening workflow
- Threshold tuning and session audit
- CSV import support for screening candidate papers
- PRISMA-style counts and flow preparation

### 💳 Enterprise & Admin Features

- Free, Pro, and University pricing model built into the app
- **Stripe Integration**: Ready for live payments (requires API key).
- Promo code upgrade support for fast plan changes
- Billing page with plan descriptions and payment flow
- Admin dashboard for user, revenue, ticket, and audit log management

---


---

## Requirements

This app is built for Python 3.11+ and works on Windows, macOS, and Linux. It uses CPU-only PyTorch on Windows by default.

### Python dependencies

- torch
- torchvision
- torchaudio
- transformers
- sentence-transformers
- faiss-cpu
- scikit-learn
- pandas
- numpy
- matplotlib
- PyQt5
- Pillow
- requests
- python-dateutil

`requirements.txt` is included in the repository.

---

## Setup and installation

### Windows setup

1. Open PowerShell or Command Prompt in the project folder.
2. Run the Windows fix script if needed:

```powershell
setup_fix.bat
```

3. Install packages manually if preferred:

```powershell
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install transformers sentence-transformers faiss-cpu pandas numpy matplotlib PyQt5 scikit-learn Pillow requests python-dateutil
```

### macOS / Linux setup

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

### Data files

> [!CAUTION]
> Due to GitHub file size limits (100MB), the large pre-computed indices are excluded from the initial push. To fully run the application, ensure the following files are in your `data/` directory:

```text
data/
├── arxiv_faiss.index      # FAISS Vector Index
├── arxiv_metadata.csv     # Paper Metadata (CSV)
├── arxiv_embeddings.npy   # Pre-computed Embeddings (NumPy)
```

Optional files:

- `data/litrev_model/` — screening model files for literature screening

The application will also create `data/trilit.db` automatically when it runs.

### Start the app

Run the desktop application with:

```bash
python main.py
```

---

## Login and demo access

### Default admin account

- Email: `admin@trilit.ai`
- Password: `admin123`

### Guest access

- Open the app and click **Continue as Guest** to access the workspace without registering.

### Promo codes

Built-in promo codes provide immediate plan upgrades:

- `RESORA2026`
- `RESEARCH50`
- `PHD2024`
- `SCHOLAR2024`
- `UNIVERSITY2024`

Promo codes currently map to plans such as `pro`, `university`, and enhanced free modes.

---

## Application modules

### Dashboard

- Overview of recent searches, summaries, bookmarks, and screening sessions
- Quick access buttons for Search, Summarize, Analyze, Screen, and PRISMA
- Research problem solver cards that map common research issues to app features
- Credit usage, plan summary, and workspace statistics

### Search

- Smart paper discovery powered by FAISS semantic search and TF-IDF fallback
- Search over 50,000 ArXiv papers
- Category filters for ArXiv sections like `cs.AI`, `cs.CL`, `stat.ML`, `physics`, and more
- Export results as CSV, BibTeX, RIS, or EndNote
- Bookmark, save for later, analyze, summarize, or open selected papers directly

### Analyze

- Paper analysis engine for titles and abstracts
- Detects methodology, contributions, limitations, and research type
- Assigns an impact score and novelty/reproducibility signals
- Generates keywords and hypothesis suggestions

### Summarize

- Abstract summarizer using BART-large-cnn
- Extractive fallback summary when transformer model cannot load
- Save summary history automatically
- Copy generated summaries instantly

### Research Tools

- Research Gap Finder to reveal unexplored directions in the literature
- Research analytics and category breakdowns
- Related work and hypothesis support
- Citation formatting utilities in multiple export formats

### Workspace

- Research workspace for project planning and paper organization
- Project paper lists and notes
- Task tracking and deadlines
- Reading status management
- Workspace-level summaries and bookmarks

### Bookmarks

- Save selected papers with title, abstract, score, and note
- Organize papers into collections
- Export bookmarks to CSV

### Reading List

- Track reading progress with status labels
- Manage papers in a personal reading queue
- Keep research notes and progress visible

### Billing

- Built-in subscription plans and credit limits
- Promo code redemption and plan upgrades
- Payment history and invoice support
- Team / university licensing hints for larger deployments

### Admin (University plan only)

- Admin dashboard for users, revenue, support tickets, and audit logs
- Promo code management and billing controls
- Team plans and enterprise support workflows

---

## Architecture and data flow

### Backend

- `ml_backend.py`
  - Loads FAISS index from `data/arxiv_faiss.index`
  - Loads metadata from `data/arxiv_metadata.csv`
  - Loads embeddings from `data/arxiv_embeddings.npy`
  - Uses `sentence-transformers` (`all-MiniLM-L6-v2`) for semantic queries
  - Falls back to TF-IDF search when semantic models are unavailable
  - Provides summarization and paper analysis APIs

- `database.py`
  - Uses SQLite with WAL journaling and foreign key support
  - Stores users, sessions, bookmarks, summaries, screenings, payments, notifications, tasks, projects, and audit logs
  - Seeds the admin user automatically on first run

### Frontend

- `main.py`
  - Builds the entire PyQt5 desktop interface
  - Implements navigation, page widgets, user forms, search, analysis, summaries, and exports
  - Handles plan-based feature access and user credit management
  - Creates a modern dark SaaS-style UI with cards, buttons, tabs, and responsive panels

---

## Recommended workflow

1. Install dependencies and place required data files in `data/`.
2. Run `python main.py` and sign in or continue as a guest.
3. Start with the Search page to discover papers.
4. Preview abstracts and bookmark valuable papers.
5. Analyze selected papers with the Analyze page.
6. Summarize abstracts using the Summarize page.
7. Use Research Tools for gap detection and related-work insights.
8. Organize papers in the Workspace and track reading progress.

---

## Troubleshooting

### Common errors

- `ModuleNotFoundError: No module named 'PyQt5'`
  - `pip install PyQt5`

- `ModuleNotFoundError: No module named 'faiss'`
  - `pip install faiss-cpu`

- `ImportError` or `WinError 1114` from PyTorch
  - Reinstall CPU-only PyTorch:

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

- App cannot find data files
  - Confirm `data/arxiv_faiss.index`, `data/arxiv_metadata.csv`, and `data/arxiv_embeddings.npy` exist

### Performance notes

- The first model load may take several seconds to download or initialize
- Semantic search performs best with the locally cached `all-MiniLM-L6-v2` model
- If the summarizer fails to load, the app uses a fallback extractive summarization method

---

## File structure

```text
App/
├── main.py
├── ml_backend.py
├── database.py
├── requirements.txt
├── setup_fix.bat
├── README.md
├── assets/
├── data/
│   ├── arxiv_embeddings.npy
│   ├── arxiv_faiss.index
│   ├── arxiv_metadata.csv
│   └── litrev_model/
└── output/
```

---

## Notes for developers

- `main.py` is the entrypoint and contains the full UI layout
- `ml_backend.py` exposes `load_all`, `search`, `find_similar`, `summarize`, and `analyze_paper`
- `database.py` exposes authentication, user plans, bookmarks, summaries, screenings, and notification functions
- The app saves state in `data/trilit.db` automatically

---

## License & attribution

This repository is a custom research assistant app built from Python, PyQt5, FAISS, Hugging Face transformers, and SQLite. Use it as a foundation for research productivity tools or a personal literature review assistant.
