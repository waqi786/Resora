@echo off
title TriLit AI - Windows Setup
color 0A
echo.
echo  ================================================
echo   TriLit AI v5  -  Windows Setup Script
echo   Fixes: WinError 1114 PyTorch DLL Error
echo  ================================================
echo.
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo  ERROR: Python not found! Get it from python.org
    pause & exit /b 1
)
python --version & echo  OK!
echo.
echo [2/5] Upgrading pip...
python -m pip install --upgrade pip --quiet & echo  OK!
echo.
echo [3/5] Removing broken PyTorch...
pip uninstall torch torchvision torchaudio -y --quiet 2>nul & echo  OK!
echo.
echo [4/5] Installing CPU PyTorch (2-5 min)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --quiet
echo  OK!
echo.
echo [5/5] Installing all packages...
pip install transformers>=4.30.0 sentence-transformers>=2.2.0 faiss-cpu>=1.7.0 pandas>=1.5.0 numpy>=1.24.0 matplotlib>=3.7.0 PyQt5>=5.15.0 scikit-learn>=1.2.0 Pillow>=9.0.0 requests>=2.28.0 --quiet
echo  Done!
echo.
echo  ================================================
echo   RUN THE APP:  python main.py
echo   VS CODE:      Press F5
echo  ================================================
pause
