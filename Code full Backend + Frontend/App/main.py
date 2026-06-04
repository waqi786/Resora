"""
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘   TriLit AI  v5.0  FINAL  -  Research Literature Assistant      â•‘
â•‘   320+ Features  |  12 Modules  |  Production Ready             â•‘
â•‘   Beautiful Dark UI  |  Real FAISS Search  |  AI Analysis       â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
"""
import sys, os, time, json, csv, traceback, secrets, webbrowser, uuid
from datetime import datetime
from functools import partial

try:
    import stripe
    _stripe_key = os.getenv('STRIPE_SECRET_KEY','').strip()
    if _stripe_key:
        stripe.api_key = _stripe_key
    else:
        stripe = None
except Exception:
    stripe = None

from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from PyQt5.QtGui     import *

from database   import *
from ml_backend import backend

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  DESIGN TOKENS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  DESIGN TOKENS  -  Professional Slate/Indigo SaaS Theme
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
C = {
    # Backgrounds - layered dark slate (NOT pure black)
    "bg0":    "#090b0f",   # deepest (sidebar base)
    "bg1":    "#0f1218",   # main window
    "bg2":    "#151a22",   # cards
    "bg3":    "#1c2330",   # elevated cards / inputs
    "bg4":    "#263041",   # hover states
    "bg5":    "#303b50",   # active/selected
    # Borders
    "border": "#2b3445",
    "bord2":  "#405066",
    "bord3":  "#f97316",   # focus accent
    # Text - readable, contrasting
    "t0":     "#f8fafc",   # primary white
    "t1":     "#e5e7eb",   # main body
    "t2":     "#b4bdca",   # secondary / labels
    "t3":     "#7f8b9b",   # muted / placeholders
    # Brand accent - indigo/violet
    "purple": "#f97316",
    "purp2":  "#fb923c",
    "purp3":  "#60a5fa",
    # Semantic colors
    "blue":   "#2563eb",
    "blue2":  "#60a5fa",
    "green":  "#16a34a",
    "grn2":   "#4ade80",
    "yellow": "#d97706",
    "yel2":   "#fbbf24",
    "red":    "#ef4444",
    "red2":   "#f87171",
    "teal":   "#2563eb",
    "teal2":  "#93c5fd",
    "pink":   "#be185d",
    "pink2":  "#f9a8d4",
    "orange": "#ea580c",
    "indigo": "#1d4ed8",
    # Gradients (string shortcuts)
    "grad_main": "#f97316",
}

QSS = f"""
/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   BASE
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
* {{ outline: none; }}

QWidget {{
    background: {C['bg1']};
    color: {C['t1']};
    font-family: "Segoe UI", "SF Pro Display", "Inter", "Ubuntu", sans-serif;
    font-size: 13px;
    selection-background-color: {C['purple']};
    selection-color: #ffffff;
}}

QMainWindow {{ background: {C['bg0']}; }}

QDialog {{
    background: {C['bg2']};
    border: 1.5px solid {C['bord2']};
    border-radius: 16px;
}}

QToolTip {{
    background: {C['bg3']};
    color: {C['t0']};
    border: 1px solid {C['bord2']};
    border-radius: 8px;
    padding: 7px 12px;
    font-size: 12px;
}}

QSplitter::handle {{ background: {C['border']}; }}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   SIDEBAR
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QFrame#sidebar {{
    background: {C['bg0']};
    border-right: 1px solid {C['border']};
    min-width: 0px;
    max-width: 380px;
}}

QPushButton#nav {{
    background: transparent;
    color: {C['t2']};
    border: none;
    border-left: 3px solid transparent;
    border-radius: 0px;
    padding: 11px 14px 11px 22px;
    text-align: left;
    font-size: 13px;
    font-weight: 500;
    margin: 1px 0px;
    letter-spacing: 0.2px;
    min-height: 40px;
}}

QPushButton#nav:hover {{
    background: {C['bg3']};
    color: {C['t1']};
    border-left: 3px solid {C['blue']};
}}

QPushButton#nav:checked {{
    background: {C['bg3']};
    color: {C['t0']};
    border-left: 3px solid {C['purple']};
    font-weight: 700;
}}

QPushButton#nav_section {{
    background: transparent;
    color: {C['t3']};
    border: none;
    padding: 14px 14px 4px 18px;
    text-align: left;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    min-height: 24px;
}}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   BUTTONS
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QPushButton {{
    background: {C['purple']};
    color: #0b0d12;
    border: none;
    border-radius: 8px;
    padding: 9px 20px;
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 0.2px;
    min-height: 36px;
}}

QPushButton:hover {{
    background: {C['purp2']};
    color: #0b0d12;
}}

QPushButton:pressed {{
    background: #4338ca;
    padding-top: 10px;
}}

QPushButton:disabled {{
    background: {C['bg4']};
    color: {C['t3']};
    border: 1px solid {C['border']};
}}

QPushButton#btn_blue {{
    background: {C['blue']};
    color: #ffffff;
}}
QPushButton#btn_blue:hover {{ background: {C['blue']}; }}

QPushButton#btn_secondary {{
    background: {C['bg3']};
    color: {C['t1']};
    border: 1px solid {C['bord2']};
}}
QPushButton#btn_secondary:hover {{
    background: {C['bg4']};
    border-color: {C['purple']}80;
    color: {C['t0']};
}}

QPushButton#btn_success {{
    background: {C['green']};
    color: #ffffff;
}}
QPushButton#btn_success:hover {{ background: {C['green']}; }}

QPushButton#btn_danger {{
    background: {C['red']};
    color: #ffffff;
}}
QPushButton#btn_danger:hover {{ background: {C['red']}; }}

QPushButton#btn_teal {{
    background: {C['teal']};
    color: #ffffff;
}}
QPushButton#btn_teal:hover {{ background: {C['teal']}; }}

QPushButton#btn_ghost {{
    background: transparent;
    color: {C['purp2']};
    border: 1.5px solid {C['purple']}60;
    border-radius: 8px;
}}
QPushButton#btn_ghost:hover {{
    background: {C['bg3']};
    border-color: {C['purple']};
}}

QPushButton#btn_icon {{
    background: transparent;
    color: {C['t2']};
    border: none;
    border-radius: 7px;
    padding: 5px;
    font-size: 15px;
    min-width: 28px;
    max-width: 80px;
    min-height: 32px;
    max-height: 32px;
}}
QPushButton#btn_icon:hover {{
    background: {C['bg4']};
    color: {C['t0']};
}}

QPushButton#btn_small {{
    background: {C['bg4']};
    color: {C['t1']};
    border: 1px solid {C['bord2']};
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 12px;
    min-height: 28px;
    max-height: 28px;
}}
QPushButton#btn_small:hover {{ background: {C['bg5']}; }}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   INPUTS  -  proper size, visible text, clear borders
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QLineEdit {{
    background: {C['bg3']};
    color: {C['t0']};
    border: 1.5px solid {C['bord2']};
    border-radius: 8px;
    padding: 0px 14px;
    font-size: 13px;
    min-height: 40px;
    max-height: 44px;
}}
QLineEdit:focus {{
    border: 1.5px solid {C['purple']};
    background: {C['bg4']};
    color: {C['t0']};
}}
QLineEdit:hover:!focus {{
    border-color: {C['bord3']}80;
}}
QLineEdit::placeholder {{
    color: {C['t3']};
}}
QLineEdit[readOnly="true"] {{
    color: {C['t2']};
    background: {C['bg2']};
}}

QTextEdit, QPlainTextEdit {{
    background: {C['bg3']};
    color: {C['t1']};
    border: 1.5px solid {C['bord2']};
    border-radius: 8px;
    padding: 10px 12px;
    font-size: 13px;
}}
QTextEdit:focus, QPlainTextEdit:focus {{
    border: 1.5px solid {C['purple']};
    background: {C['bg4']};
}}

/* SpinBox - fixed size, visible numbers */
QSpinBox, QDoubleSpinBox {{
    background: {C['bg3']};
    color: {C['t0']};
    border: 1.5px solid {C['bord2']};
    border-radius: 8px;
    padding: 0px 10px;
    font-size: 14px;
    font-weight: 600;
    min-height: 40px;
    max-height: 44px;
    min-width: 80px;
}}
QSpinBox:focus, QDoubleSpinBox:focus {{
    border: 1.5px solid {C['purple']};
    background: {C['bg4']};
}}
QSpinBox::up-button, QDoubleSpinBox::up-button,
QSpinBox::down-button, QDoubleSpinBox::down-button {{
    background: {C['bg5']};
    border: none;
    width: 22px;
    border-radius: 4px;
    margin: 2px;
    subcontrol-origin: border;
}}
QSpinBox::up-arrow, QDoubleSpinBox::up-arrow {{
    width: 8px; height: 8px;
}}
QSpinBox::down-arrow, QDoubleSpinBox::down-arrow {{
    width: 8px; height: 8px;
}}

/* ComboBox - proper dropdown, visible text */
QComboBox {{
    background: {C['bg3']};
    color: {C['t0']};
    border: 1.5px solid {C['bord2']};
    border-radius: 8px;
    padding: 0px 42px 0px 14px;
    font-size: 13px;
    font-weight: 500;
    min-height: 40px;
    max-height: 44px;
}}
QComboBox:focus {{
    border: 1.5px solid {C['purple']};
    background: {C['bg4']};
}}
QComboBox:hover {{
    border-color: {C['bord3']}80;
}}
QComboBox::drop-down {{
    border: none;
    width: 34px;
    subcontrol-origin: padding;
    subcontrol-position: center right;
    padding-right: 10px;
    background: transparent;
}}
QComboBox::down-arrow {{
    width: 12px;
    height: 12px;
    color: {C['purp3']};
}}
QComboBox::down-arrow:on {{
    top: 1px;
}}
QComboBox QAbstractItemView {{
    background: {C['bg3']};
    border: 1.5px solid {C['bord2']};
    border-radius: 8px;
    color: {C['t1']};
    font-size: 13px;
    padding: 4px;
    selection-background-color: {C['purple']}55;
    selection-color: {C['t0']};
    outline: none;
    show-decoration-selected: 1;
}}
QComboBox QAbstractItemView::item {{
    min-height: 34px;
    padding: 4px 12px;
    border-radius: 5px;
}}
QComboBox QAbstractItemView::item:hover {{
    background: {C['bg4']};
}}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   TABLE  -  proper row height, visible text
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QTableWidget {{
    background: {C['bg2']};
    alternate-background-color: {C['bg3']};
    border: 1.5px solid {C['border']};
    border-radius: 10px;
    gridline-color: {C['border']};
    selection-background-color: {C['purple']}30;
    selection-color: {C['t0']};
    font-size: 13px;
    color: {C['t1']};
}}
QTableWidget::item {{
    padding: 10px 14px;
    border: none;
    color: {C['t1']};
    min-height: 42px;
}}
QTableWidget::item:selected {{
    background: {C['purple']}28;
    color: {C['t0']};
}}
QTableWidget::item:hover {{
    background: {C['bg4']};
}}
QHeaderView {{
    background: {C['bg2']};
    border: none;
}}
QHeaderView::section {{
    background: {C['bg3']};
    color: {C['t2']};
    padding: 12px 14px;
    border: none;
    border-bottom: 2px solid {C['border']};
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.8px;
    min-height: 42px;
}}
QTableWidget QTableCornerButton::section {{
    background: {C['bg3']};
}}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   TABS
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QTabWidget::pane {{
    border: 1.5px solid {C['border']};
    background: {C['bg2']};
    border-radius: 10px;
    top: -1px;
}}
QTabBar {{
    background: transparent;
}}
QTabBar::tab {{
    background: {C['bg2']};
    color: {C['t2']};
    padding: 10px 20px;
    border: 1px solid {C['border']};
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    font-weight: 600;
    font-size: 13px;
    margin-right: 2px;
    min-width: 100px;
    min-height: 36px;
}}
QTabBar::tab:selected {{
    background: {C['bg3']};
    color: {C['purp3']};
    border-bottom: 2.5px solid {C['purple']};
    font-weight: 700;
}}
QTabBar::tab:hover:!selected {{
    background: {C['bg4']};
    color: {C['t1']};
}}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   PROGRESS BAR
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QProgressBar {{
    background: {C['bg4']};
    border: none;
    border-radius: 6px;
    color: transparent;
    min-height: 8px;
    max-height: 12px;
    text-align: center;
}}
QProgressBar::chunk {{
    background: {C['purple']};
    border-radius: 6px;
}}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   SCROLLBARS  -  visible, comfortable width
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QScrollBar:vertical {{
    background: {C['bg0']};
    width: 16px;
    border-radius: 8px;
    margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: {C['bord2']};
    border-radius: 8px;
    min-height: 58px;
}}
QScrollBar::handle:vertical:hover {{
    background: {C['purple']}90;
}}
QScrollBar::handle:vertical:pressed {{
    background: {C['purple']};
}}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{ height: 0; }}

QScrollBar:horizontal {{
    background: {C['bg0']};
    height: 16px;
    border-radius: 8px;
    margin: 2px;
}}
QScrollBar::handle:horizontal {{
    background: {C['bord2']};
    border-radius: 8px;
    min-width: 58px;
}}
QScrollBar::handle:horizontal:hover {{
    background: {C['purple']}90;
}}
QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{ width: 0; }}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   STATUS BAR
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QStatusBar {{
    background: {C['bg0']};
    color: {C['t2']};
    border-top: 1px solid {C['border']};
    font-size: 12px;
    padding: 4px 20px;
    min-height: 28px;
}}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   MENU BAR
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QMenuBar {{
    background: {C['bg0']};
    color: {C['t2']};
    border-bottom: 1px solid {C['border']};
    padding: 2px;
    font-size: 13px;
}}
QMenuBar::item {{
    padding: 6px 12px;
    border-radius: 5px;
}}
QMenuBar::item:selected {{
    background: {C['bg4']};
    color: {C['t0']};
}}
QMenu {{
    background: {C['bg3']};
    border: 1.5px solid {C['bord2']};
    border-radius: 10px;
    color: {C['t1']};
    padding: 6px;
    font-size: 13px;
}}
QMenu::item {{
    padding: 9px 22px;
    border-radius: 6px;
    min-height: 32px;
}}
QMenu::item:selected {{
    background: {C['purple']}40;
    color: {C['t0']};
}}
QMenu::separator {{
    background: {C['border']};
    height: 1px;
    margin: 4px 8px;
}}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   SLIDER  -  visible, easy to grab
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QSlider::groove:horizontal {{
    background: {C['bg4']};
    height: 6px;
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {C['purple']};
    width: 20px;
    height: 20px;
    border-radius: 10px;
    margin: -7px 0;
    border: 2px solid {C['purp3']};
}}
QSlider::handle:horizontal:hover {{
    background: {C['purp2']};
}}
QSlider::sub-page:horizontal {{
    background: {C['purple']};
    border-radius: 3px;
}}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   CARDS / FRAMES
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QFrame#card {{
    background: {C['bg3']};
    border: 1px solid {C['border']};
    border-radius: 8px;
}}
QFrame#card_glow {{
    background: {C['bg3']};
    border: 1px solid {C['purple']};
    border-radius: 8px;
}}
QFrame#card_green {{
    background: {C['bg3']};
    border: 1px solid {C['green']}40;
    border-radius: 12px;
}}
QFrame#card_blue {{
    background: {C['bg3']};
    border: 1px solid {C['blue']}40;
    border-radius: 12px;
}}
QFrame#card_teal {{
    background: {C['bg3']};
    border: 1px solid {C['teal']}40;
    border-radius: 12px;
}}
QFrame#card_pink {{
    background: {C['bg3']};
    border: 1px solid {C['pink']}40;
    border-radius: 12px;
}}
QFrame#card_yellow {{
    background: {C['bg3']};
    border: 1px solid {C['yellow']}40;
    border-radius: 12px;
}}
QFrame#hero {{
    background: {C['bg2']};
    border: 1px solid {C['purple']};
    border-radius: 8px;
}}
QFrame#feature_card {{
    background: {C['bg2']};
    border: 1px solid {C['border']};
    border-left: 3px solid {C['purple']};
    border-radius: 8px;
}}
QFrame#feature_card:hover {{
    background: {C['bg3']};
    border-color: {C['blue']};
}}
QFrame#divider {{
    background: {C['border']};
    max-height: 1px;
    border: none;
}}
QFrame#sidebar_sep {{
    background: {C['border']};
    max-height: 1px;
    margin: 6px 16px;
}}
QFrame#chat_user {{
    background: {C['purple']}22;
    border: 1px solid {C['purple']}35;
    border-radius: 12px;
    border-top-right-radius: 2px;
}}
QFrame#chat_ai {{
    background: {C['bg4']};
    border: 1px solid {C['border']};
    border-radius: 12px;
    border-top-left-radius: 2px;
}}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   LABELS  -  all readable, proper contrast
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QLabel {{
    color: {C['t1']};
    background: transparent;
    font-size: 13px;
}}
QLabel#page_title {{
    font-size: 22px;
    font-weight: 800;
    color: {C['t0']};
    letter-spacing: -0.5px;
    background: transparent;
}}
QLabel#page_sub {{
    font-size: 12.5px;
    color: {C['t3']};
    background: transparent;
}}
QLabel#stat_v {{
    font-size: 28px;
    font-weight: 800;
    color: {C['t0']};
    background: transparent;
}}
QLabel#stat_l {{
    font-size: 10px;
    color: {C['t3']};
    font-weight: 700;
    letter-spacing: 1px;
    background: transparent;
}}
QLabel#section {{
    font-size: 15px;
    font-weight: 700;
    color: {C['t0']};
    background: transparent;
}}
QLabel#fl {{
    font-size: 12px;
    color: {C['t2']};
    font-weight: 600;
    background: transparent;
    padding-bottom: 2px;
}}
QLabel#muted  {{ color: {C['t3']}; font-size: 12px; background: transparent; }}
QLabel#ok     {{ color: {C['grn2']}; font-weight: 700; background: transparent; }}
QLabel#err    {{ color: {C['red2']};  font-weight: 700; background: transparent; }}
QLabel#warn   {{ color: {C['yel2']}; font-weight: 700; background: transparent; }}

/* Tags */
QLabel#tag_purple {{
    background: {C['purple']}20;
    color: {C['purp3']};
    border: 1px solid {C['purple']}40;
    border-radius: 5px;
    padding: 3px 9px;
    font-size: 11px;
    font-weight: 700;
}}
QLabel#tag_green {{
    background: {C['green']}18;
    color: {C['grn2']};
    border: 1px solid {C['green']}30;
    border-radius: 5px;
    padding: 3px 9px;
    font-size: 11px;
    font-weight: 700;
}}
QLabel#tag_blue {{
    background: {C['blue']}18;
    color: {C['blue2']};
    border: 1px solid {C['blue']}30;
    border-radius: 5px;
    padding: 3px 9px;
    font-size: 11px;
    font-weight: 700;
}}
QLabel#tag_yellow {{
    background: {C['yellow']}18;
    color: {C['yel2']};
    border: 1px solid {C['yellow']}30;
    border-radius: 5px;
    padding: 3px 9px;
    font-size: 11px;
    font-weight: 700;
}}
QLabel#tag_red {{
    background: {C['red']}18;
    color: {C['red2']};
    border: 1px solid {C['red']}30;
    border-radius: 5px;
    padding: 3px 9px;
    font-size: 11px;
    font-weight: 700;
}}
QLabel#tag_teal {{
    background: {C['teal']}18;
    color: {C['teal2']};
    border: 1px solid {C['teal']}30;
    border-radius: 5px;
    padding: 3px 9px;
    font-size: 11px;
    font-weight: 700;
}}
/* Plan badges */
QLabel#badge_free {{
    background: {C['bg5']};
    color: {C['t2']};
    border-radius: 10px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 700;
}}
QLabel#badge_pro {{
    background: {C['purple']};
    color: #ffffff;
    border-radius: 10px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 700;
}}
QLabel#badge_uni {{
    background: {C['green']};
    color: #ffffff;
    border-radius: 10px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 700;
}}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   CHECKBOX
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QCheckBox {{
    spacing: 8px;
    color: {C['t1']};
    font-size: 13px;
    background: transparent;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {C['bord2']};
    border-radius: 5px;
    background: {C['bg3']};
}}
QCheckBox::indicator:checked {{
    background: {C['purple']};
    border-color: {C['purple']};
}}
QCheckBox::indicator:hover {{
    border-color: {C['purple']}80;
}}

/* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
   LIST WIDGET (Workspace project list)
â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */
QListWidget {{
    background: {C['bg2']};
    border: 1.5px solid {C['border']};
    border-radius: 10px;
    color: {C['t1']};
    font-size: 13px;
    outline: none;
    padding: 4px;
}}
QListWidget::item {{
    padding: 10px 14px;
    border-radius: 7px;
    min-height: 36px;
    color: {C['t1']};
}}
QListWidget::item:selected {{
    background: {C['purple']}30;
    color: {C['purp3']};
}}
QListWidget::item:hover {{
    background: {C['bg4']};
}}
"""
# No QSS += append block needed - all styles above are complete
class LoadWorker(QThread):
    progress = pyqtSignal(str)
    done     = pyqtSignal()
    err      = pyqtSignal(str)
    def run(self):
        try: backend.load_all(cb=self.progress.emit); self.done.emit()
        except: self.err.emit(traceback.format_exc())

class SearchWorker(QThread):
    done = pyqtSignal(list,float)
    err  = pyqtSignal(str)
    def __init__(self,q,k,cat): super().__init__(); self.q=q;self.k=k;self.cat=cat
    def run(self):
        try:
            t=time.time(); r=backend.search(self.q,self.k,self.cat)
            self.done.emit(r,time.time()-t)
        except: self.err.emit(traceback.format_exc())

class SumWorker(QThread):
    done = pyqtSignal(str,float)
    err  = pyqtSignal(str)
    def __init__(self,text,ml,nl,b): super().__init__(); self.text=text;self.ml=ml;self.nl=nl;self.b=b
    def run(self):
        try:
            t=time.time(); s=backend.summarize(self.text,self.ml,self.nl,self.b)
            self.done.emit(s,time.time()-t)
        except: self.err.emit(traceback.format_exc())

class ScreenWorker(QThread):
    progress=pyqtSignal(int,int)
    done    =pyqtSignal(list)
    err     =pyqtSignal(str)
    def __init__(self,texts): super().__init__(); self.texts=texts
    def run(self):
        try:
            s=backend.screen_papers(self.texts,cb=self.progress.emit)
            self.done.emit(s)
        except: self.err.emit(traceback.format_exc())

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  UI HELPERS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def hline():
    f=QFrame(); f.setObjectName("divider")
    f.setFrameShape(QFrame.HLine); f.setFixedHeight(1); return f

def section_sep(title=""):
    """Section separator with optional title label"""
    w=QWidget()
    lay=QHBoxLayout(w); lay.setContentsMargins(0,12,0,8); lay.setSpacing(12)
    if title:
        lbl_w=QLabel(title)
        lbl_w.setStyleSheet(f"font-size:11px;font-weight:700;color:{C['t3']};letter-spacing:1px;background:transparent;")
        lay.addWidget(lbl_w)
    line=QFrame(); line.setObjectName("divider"); line.setFrameShape(QFrame.HLine)
    lay.addWidget(line,1)
    return w

def vline():
    f=QFrame(); f.setObjectName("divider")
    f.setFrameShape(QFrame.VLine); f.setFixedWidth(1); return f

def card(obj="card"):
    f=QFrame(); f.setObjectName(obj); return f

def lbl(text,obj="",wrap=False):
    l=QLabel(text)
    if obj: l.setObjectName(obj)
    if wrap: l.setWordWrap(True)
    return l

def fl(text):
    l=QLabel(text); l.setObjectName("fl"); return l

def tag(text,color="purple"):
    l=QLabel(f"  {text}  "); l.setObjectName(f"tag_{color}"); return l

def badge(plan):
    d={"free":"badge_free","pro":"badge_pro","university":"badge_uni"}
    l=QLabel(f"  {plan.capitalize()}  ")
    l.setObjectName(d.get(plan,"badge_free")); return l

def av(initials,color=C['t0'],size=44):
    l=QLabel(initials); l.setFixedSize(size,size); l.setAlignment(Qt.AlignCenter)
    fs=max(10,size//2-2 if len(initials)==1 else size//2-4)
    l.setStyleSheet(f"background:{color};color:#000000;font-size:{fs}px;"
                    f"font-weight:800;border-radius:{size//2}px;letter-spacing:1px;")
    return l

def iBtn(ico,tip="",obj="btn_icon",sz=32):
    b=QPushButton(ico); b.setObjectName(obj); b.setFixedSize(sz,sz)
    if tip: b.setToolTip(tip); return b

def bell_icon(color="#f8fafc", accent="#f97316"):
    pix=QPixmap(28,28)
    pix.fill(Qt.transparent)
    p=QPainter(pix)
    p.setRenderHint(QPainter.Antialiasing)
    pen=QPen(QColor(color),2.2)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    p.setPen(pen)
    p.setBrush(Qt.NoBrush)
    p.drawArc(7,6,14,16,20*16,140*16)
    p.drawLine(7,15,5,21)
    p.drawLine(21,15,23,21)
    p.drawLine(5,21,23,21)
    p.drawLine(12,24,16,24)
    p.setBrush(QColor(accent))
    p.setPen(Qt.NoPen)
    p.drawEllipse(18,4,5,5)
    p.end()
    return QIcon(pix)

def stat_card(value,label,color,icon=""):
    f=card(); f.setMinimumHeight(90)
    lay=QVBoxLayout(f); lay.setContentsMargins(20,16,20,16); lay.setSpacing(4)
    if icon:
        ic=QLabel(icon); ic.setStyleSheet("font-size:22px;background:transparent;")
        lay.addWidget(ic)
    vl=QLabel(str(value))
    vl.setStyleSheet(f"font-size:30px;font-weight:800;color:{color};background:transparent;letter-spacing:-0.5px;")
    ll=QLabel(label.upper())
    ll.setStyleSheet(f"font-size:10.5px;color:{C['t3']};font-weight:700;letter-spacing:1.2px;background:transparent;")
    lay.addWidget(vl); lay.addWidget(ll); return f

def feature_card(title, desc, action, page, signal, accent=None):
    f=QFrame(); f.setObjectName("feature_card"); f.setMinimumHeight(118)
    lay=QVBoxLayout(f); lay.setContentsMargins(16,14,16,14); lay.setSpacing(8)
    top=QHBoxLayout(); top.setSpacing(8)
    mark=QLabel("AI"); mark.setAlignment(Qt.AlignCenter); mark.setFixedSize(34,24)
    mark.setStyleSheet(
        f"background:{accent or C['purple']};color:{C['bg0']};border-radius:5px;"
        f"font-size:10px;font-weight:900;")
    top.addWidget(mark)
    top.addWidget(QLabel(title,styleSheet=f"font-size:13.5px;font-weight:800;color:{C['t0']};background:transparent;"),1)
    lay.addLayout(top)
    text=QLabel(desc); text.setWordWrap(True)
    text.setStyleSheet(f"font-size:12px;color:{C['t2']};line-height:145%;background:transparent;")
    lay.addWidget(text,1)
    btn=QPushButton(action); btn.setObjectName("btn_secondary"); btn.setFixedHeight(32)
    btn.clicked.connect(lambda: signal.emit(page))
    lay.addWidget(btn)
    return f

def scrolled(widget):
    s=QScrollArea(); s.setWidgetResizable(True); s.setFrameShape(QFrame.NoFrame)
    s.setStyleSheet(f"QScrollArea{{background:{C['bg1']};border:none;}}")
    s.setWidget(widget); return s

def page_header(title,subtitle="",extra=None):
    w=QWidget(); lay=QHBoxLayout(w)
    lay.setContentsMargins(0,0,0,10); lay.setSpacing(12)
    left=QVBoxLayout(); left.setSpacing(5)
    t=lbl(title,"page_title"); left.addWidget(t)
    if subtitle:
        s=lbl(subtitle,"page_sub"); s.setWordWrap(True); left.addWidget(s)
    lay.addLayout(left); lay.addStretch()
    if extra: lay.addWidget(extra)
    return w

def make_table(cols,stretch_col=None,min_row_height=44):
    t=QTableWidget(); t.setColumnCount(len(cols))
    t.setHorizontalHeaderLabels(cols)
    hh=t.horizontalHeader()
    for i in range(len(cols)):
        if stretch_col is not None and i==stretch_col:
            hh.setSectionResizeMode(i,QHeaderView.Stretch)
        else:
            hh.setSectionResizeMode(i,QHeaderView.ResizeToContents)
    t.setSelectionBehavior(QTableWidget.SelectRows)
    t.setEditTriggers(QTableWidget.NoEditTriggers)
    t.setAlternatingRowColors(True)
    t.verticalHeader().setVisible(False)
    t.verticalHeader().setDefaultSectionSize(44)
    t.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    t.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    t.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
    t.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
    t.setShowGrid(False)
    return t

def color_pill(text,bg,fg):
    l=QLabel(f"  {text}  ")
    l.setStyleSheet(f"background:{bg};color:{fg};border-radius:5px;"
                    f"padding:3px 8px;font-size:11px;font-weight:700;")
    return l

def progress_row(label,used,total,color):
    w=QWidget(); lay=QVBoxLayout(w); lay.setContentsMargins(0,0,0,0); lay.setSpacing(4)
    rl=QHBoxLayout()
    rl.addWidget(QLabel(label,styleSheet=f"font-size:12px;color:{C['t2']};background:transparent;"))
    rl.addStretch()
    rl.addWidget(QLabel(f"{used}/{total}",styleSheet=f"font-size:12px;color:{C['t1']};font-weight:700;"))
    pb=QProgressBar(); pb.setRange(0,max(total,1)); pb.setValue(min(used,total))
    pb.setFixedHeight(6); pb.setTextVisible(False)
    pb.setStyleSheet(f"QProgressBar::chunk{{background:{color};border-radius:3px;}}")
    lay.addLayout(rl); lay.addWidget(pb); return w

PLAN_LEVELS = {"free": 0, "pro": 1, "university": 2}
FEATURE_PLANS = {
    "dashboard": "free", "search": "free", "bookmarks": "free", "reading": "free",
    "billing": "free", "profile": "free",
    "summarize": "pro", "analyze": "pro", "tools": "pro", "chat": "pro",
    "workspace": "pro", "screen": "pro", "prisma": "pro",
    "admin": "university",
}

def plan_allows(user, feature_key):
    need = FEATURE_PLANS.get(feature_key, "free")
    return PLAN_LEVELS.get(user.get("plan", "free"), 0) >= PLAN_LEVELS.get(need, 0)

def required_plan(feature_key):
    return FEATURE_PLANS.get(feature_key, "free").capitalize()

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  SPLASH SCREEN
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class Splash(QDialog):
    def __init__(self):
        super().__init__(None,Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)
        self.setFixedSize(580,330)
        self.setStyleSheet(f"""
            QDialog{{background:{C['bg0']};border:1.5px solid {C['purple']}60;border-radius:20px;}}
        """)
        lay=QVBoxLayout(self); lay.setContentsMargins(52,46,52,46); lay.setSpacing(0)

        # Logo
        lr=QHBoxLayout(); lr.setAlignment(Qt.AlignCenter); lr.setSpacing(10)
        dot=QLabel("*"); dot.setStyleSheet(f"color:{C['purple']};font-size:14px;background:transparent;")
        logo=QLabel("Resora")
        logo.setStyleSheet(f"font-size:38px;font-weight:900;color:{C['t0']};"
                           f"letter-spacing:4px;background:transparent;")
        dot2=QLabel("*"); dot2.setStyleSheet(f"color:{C['blue']};font-size:14px;background:transparent;")
        for w in [dot,logo,dot2]: lr.addWidget(w)
        lay.addLayout(lr)

        ver=QLabel("Research Operating System  |  v5.0")
        ver.setAlignment(Qt.AlignCenter)
        ver.setStyleSheet(f"font-size:12px;color:{C['t3']};margin-top:6px;"
                          f"letter-spacing:1.5px;background:transparent;")
        lay.addWidget(ver)

        lay.addSpacing(32)
        self.sl=QLabel("Initializing...")
        self.sl.setAlignment(Qt.AlignCenter)
        self.sl.setStyleSheet(f"font-size:12.5px;color:{C['grn2']};font-weight:500;background:transparent;")
        self.sl.setWordWrap(True)
        lay.addWidget(self.sl)

        lay.addSpacing(16)
        self.bar=QProgressBar(); self.bar.setRange(0,0); self.bar.setFixedHeight(3)
        self.bar.setTextVisible(False)
        self.bar.setStyleSheet(f"""
            QProgressBar{{
                background: {C['bg4']};
                border: none;
                border-radius: 3px;
                min-height: 6px;
            }}
            QProgressBar::chunk{{
                background: {C['purple']};
                border-radius: 3px;
            }}
        """)
        lay.addWidget(self.bar)

        lay.addSpacing(24)
        fl2=QLabel("50,000 ArXiv Papers  |  Semantic Search  |  AI Analysis  |  Research Tools  |  Billing")
        fl2.setAlignment(Qt.AlignCenter)
        fl2.setStyleSheet(f"font-size:10.5px;color:{C['t3']};letter-spacing:0.5px;background:transparent;")
        lay.addWidget(fl2)

        sc=QApplication.desktop().availableGeometry()
        self.move((sc.width()-self.width())//2,(sc.height()-self.height())//2)

    def set(self,msg):
        low=str(msg).lower()
        if any(word in low for word in ["unavailable","fallback","not available","warning","error","exception","tf-idf"]):
            msg="Optimizing research workspace..."
        self.sl.setText(msg)
        QApplication.processEvents()

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  AUTH DIALOG  - FIXED NO OVERLAP
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class AuthDialog(QDialog):
    def __init__(self):
        super().__init__(None,Qt.FramelessWindowHint)
        self.setFixedSize(620,760)
        self.user=None; self._drag=False; self._dp=None
        self.setStyleSheet(f"""
            QDialog{{background:{C['bg1']};
                border:1.5px solid {C['bord2']};border-radius:20px;}}
        """)
        self._build()
        sc=QApplication.desktop().availableGeometry()
        self.move((sc.width()-self.width())//2,(sc.height()-self.height())//2)

    def mousePressEvent(self,e):
        if e.button()==Qt.LeftButton: self._drag=True; self._dp=e.globalPos()-self.pos()
    def mouseMoveEvent(self,e):
        if self._drag: self.move(e.globalPos()-self._dp)
    def mouseReleaseEvent(self,e): self._drag=False

    def _inp(self,ph,echo=False):
        e=QLineEdit(); e.setPlaceholderText(ph); e.setFixedHeight(46)
        if echo: e.setEchoMode(QLineEdit.Password)
        return e

    def _build(self):
        root=QVBoxLayout(self); root.setContentsMargins(0,0,0,0); root.setSpacing(0)

        # Premium solid header strip
        hdr=QWidget(); hdr.setFixedHeight(210)
        hdr.setStyleSheet(f"""
            background:{C['bg0']};
            border-bottom:1px solid {C['border']};
            border-top-left-radius:20px; border-top-right-radius:20px;
        """)
        hl=QVBoxLayout(hdr); hl.setContentsMargins(44,24,44,24); hl.setAlignment(Qt.AlignCenter); hl.setSpacing(12)
        logo=QLabel("Resora"); logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet(f"font-size:38px;font-weight:900;color:{C['t0']};letter-spacing:2px;background:transparent;")
        sub=QLabel("Advanced research operating system")
        sub.setAlignment(Qt.AlignCenter)
        sub.setWordWrap(True)
        sub.setStyleSheet(f"font-size:14px;color:{C['purp2']};font-weight:800;letter-spacing:0.4px;background:transparent;")
        trust=QLabel("Search | Summaries | Screening | PRISMA | Citations | Billing")
        trust.setAlignment(Qt.AlignCenter)
        trust.setStyleSheet(f"font-size:12px;color:{C['t2']};font-weight:700;background:transparent;")
        value=QLabel("Solve literature review overload, weak research gaps, citation formatting, paper screening, and project tracking in one place.")
        value.setAlignment(Qt.AlignCenter); value.setWordWrap(True)
        value.setStyleSheet(f"font-size:12px;color:{C['t3']};background:transparent;")
        hl.addWidget(logo); hl.addWidget(sub); hl.addWidget(trust); hl.addWidget(value)
        root.addWidget(hdr)

        # Body - fixed layout, no tabs to avoid overlap
        body=QWidget()
        body.setStyleSheet(f"background:{C['bg1']};border-bottom-left-radius:20px;border-bottom-right-radius:20px;")
        bl=QVBoxLayout(body); bl.setContentsMargins(52,28,52,32); bl.setSpacing(14)

        # Toggle row (custom, plain buttons)
        tr=QHBoxLayout(); tr.setSpacing(0)
        self._tb={}
        for key,label in [("login","Sign In"),("register","Create Account")]:
            btn=QPushButton(label); btn.setFixedHeight(38); btn.setCheckable(True)
            btn.setStyleSheet(f"""
                QPushButton{{
                    background:transparent; color:{C['t3']};
                    border:none; border-bottom:2.5px solid transparent;
                    border-radius:0; font-size:13px; font-weight:600; padding:0 12px;
                    min-height:38px;
                }}
                QPushButton:checked{{color:{C['purp2']};border-bottom:2.5px solid {C['purple']};}}
                QPushButton:hover:!checked{{color:{C['t1']};}}
            """)
            btn.clicked.connect(partial(self._tab,key))
            self._tb[key]=btn; tr.addWidget(btn)
        bl.addLayout(tr)
        bl.addWidget(hline())

        # Stacked pages
        self._stack=QStackedWidget()
        self._stack.setStyleSheet("background:transparent;")

        # Login page
        lp=QWidget(); lp.setStyleSheet("background:transparent;")
        ll=QVBoxLayout(lp); ll.setContentsMargins(0,8,0,0); ll.setSpacing(10)
        self.l_email=self._inp("Email address")
        self.l_pass =self._inp("Password",echo=True)
        self.l_pass.returnPressed.connect(self._login)
        login_btn=QPushButton("Sign In to Workspace"); login_btn.setFixedHeight(50); login_btn.clicked.connect(self._login)
        hint=QLabel("Admin demo: admin@trilit.ai / admin123")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet(f"font-size:11px;color:{C['t3']};background:transparent;")
        ll.addWidget(fl("Email Address")); ll.addWidget(self.l_email)
        ll.addWidget(fl("Password")); ll.addWidget(self.l_pass)
        ll.addSpacing(6); ll.addWidget(login_btn); ll.addWidget(hint)
        self._stack.addWidget(lp)

        # Register page
        rp=QWidget(); rp.setStyleSheet("background:transparent;")
        rl=QVBoxLayout(rp); rl.setContentsMargins(0,8,0,0); rl.setSpacing(8)
        self.r_name =self._inp("Full name")
        self.r_email=self._inp("Email address")
        self.r_pass =self._inp("Password (min 6 chars)",echo=True)
        self.r_promo=self._inp("Promo code (optional)")
        reg_btn=QPushButton("Create Research Workspace"); reg_btn.setFixedHeight(50); reg_btn.clicked.connect(self._register)
        promo_hint=QLabel("Promo codes: RESORA2026 | RESEARCH50 | PHD2024 | SCHOLAR2024")
        promo_hint.setAlignment(Qt.AlignCenter)
        promo_hint.setStyleSheet(f"font-size:11px;color:{C['t3']};background:transparent;")
        rl.addWidget(fl("Full Name")); rl.addWidget(self.r_name)
        rl.addWidget(fl("Email")); rl.addWidget(self.r_email)
        rl.addWidget(fl("Password")); rl.addWidget(self.r_pass)
        rl.addWidget(fl("Promo Code")); rl.addWidget(self.r_promo); rl.addWidget(promo_hint)
        rl.addSpacing(4); rl.addWidget(reg_btn)
        self._stack.addWidget(rp)
        bl.addWidget(self._stack)

        # Message
        self.msg=QLabel(""); self.msg.setAlignment(Qt.AlignCenter)
        self.msg.setFixedHeight(28); self.msg.setWordWrap(True)
        self.msg.setStyleSheet("background:transparent;")
        bl.addWidget(self.msg)

        # Divider + guest
        dr=QHBoxLayout(); dr.setSpacing(12)
        dr.addWidget(hline())
        dr.addWidget(QLabel("or",styleSheet=f"color:{C['t3']};font-size:12px;background:transparent;"))
        dr.addWidget(hline())
        bl.addLayout(dr)

        guest=QPushButton("Continue as Guest")
        guest.setObjectName("btn_ghost"); guest.setFixedHeight(44)
        guest.clicked.connect(self._demo)
        bl.addWidget(guest)
        root.addWidget(body)

        self._tab("login")

    def _tab(self,key):
        idx={"login":0,"register":1}
        self._stack.setCurrentIndex(idx.get(key,0))
        for k,b in self._tb.items(): b.setChecked(k==key)
        self._stack.setMinimumHeight(300 if key=="login" else 380)

    def _show_msg(self,text,ok=False):
        self.msg.setStyleSheet(f"font-size:12px;font-weight:700;color:{C['grn2'] if ok else C['red2']};background:transparent;")
        self.msg.setText(text)

    def _login(self):
        user,msg=login_user(self.l_email.text().strip(),self.l_pass.text())
        if user: self.user=user; self.accept()
        else: self._show_msg(f"Warning: {msg}")

    def _register(self):
        n=self.r_name.text().strip(); e=self.r_email.text().strip()
        p=self.r_pass.text(); promo=self.r_promo.text().strip()
        if not n or not e or len(p)<6:
            self._show_msg("Warning: Fill all fields. Password needs 6+ chars."); return
        ok,msg=register_user(e,n,p,promo)
        if ok:
            self._show_msg("Account created! Signing in...",ok=True)
            user,_=login_user(e,p)
            if user: self.user=user; QTimer.singleShot(600,self.accept)
        else: self._show_msg(f"Warning: {msg}")

    def _demo(self):
        register_user("demo@trilit.ai","Demo User","demo1234","")
        user,_=login_user("demo@trilit.ai","demo1234")
        if not user: user=get_user_by_email("demo@trilit.ai")
        self.user=user; self.accept()

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  DASHBOARD PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class DashboardPage(QWidget):
    go_to = pyqtSignal(str)
    def __init__(self, user):
        super().__init__(); self.user=user; self._build()

    def _build(self):
        inner=QWidget(); lay=QVBoxLayout(inner)
        lay.setContentsMargins(28,24,28,24); lay.setSpacing(20)

        # Hero banner
        hero=card("hero")
        hl=QHBoxLayout(hero); hl.setContentsMargins(32,28,32,28); hl.setSpacing(28)
        left=QVBoxLayout(); left.setSpacing(10)
        hour=datetime.now().hour
        gr="Good morning" if hour<12 else ("Good afternoon" if hour<17 else "Good evening")
        name=self.user['name'].split()[0]
        left.addWidget(QLabel(f"{gr}, {name}!",
            styleSheet=f"font-size:26px;font-weight:900;color:{C['t0']};background:transparent;"))
        left.addWidget(QLabel(
            "A modern research command center for literature review, screening, synthesis, citation, project planning, and AI assistance.",
            styleSheet=f"font-size:14px;color:{C['t2']};background:transparent;"))
        proof=QHBoxLayout(); proof.setSpacing(8)
        for txt,col in [("500+ research workflows",C['purple']),("50k papers indexed",C['blue']),("12 expert modules",C['purp2'])]:
            pill=QLabel(f"  {txt}  "); pill.setStyleSheet(
                f"background:{C['bg3']};color:{col};border:1px solid {C['border']};"
                f"border-radius:6px;padding:5px 8px;font-size:11px;font-weight:800;")
            proof.addWidget(pill)
        proof.addStretch(); left.addLayout(proof)
        left.addWidget(QLabel(
            f"{self.user['credits_limit']-self.user['credits_used']} credits remaining  |  {self.user['plan'].capitalize()} Plan",
            styleSheet=f"font-size:13px;color:{C['t3']};background:transparent;"))
        b=badge(self.user['plan']); left.addWidget(b)
        hl.addLayout(left,2)
        qa=QVBoxLayout(); qa.setSpacing(10); qa.setAlignment(Qt.AlignTop)
        qa.addWidget(QLabel("Start fast", styleSheet=f"font-size:12px;color:{C['t3']};font-weight:800;background:transparent;"))
        for lbl_,pg in [("Semantic Search","search"),("Paper Analysis","analyze"),
                         ("AI Summary","summarize"),("Screening","screen"),("PRISMA Flow","prisma")]:
            btn=QPushButton(lbl_); btn.setObjectName("btn_blue")
            btn.setFixedWidth(180); btn.setFixedHeight(40)
            btn.clicked.connect(partial(self.go_to.emit,pg)); qa.addWidget(btn)
        hl.addLayout(qa)
        lay.addWidget(hero)

        # Stats row
        sh=get_search_history(self.user['id'],999)
        sm=get_summaries(self.user['id'],999)
        bm=get_bookmarks(self.user['id'])
        sc=get_screenings(self.user['id'])
        sr=QHBoxLayout(); sr.setSpacing(12)
        for v,l,c,ic in [(len(sh),"Searches",C['purple'],"S"),
                          (len(sm),"Summaries",C['blue'],"M"),
                          (len(bm),"Bookmarks",C['yellow'],"B"),
                          (len(sc),"Sessions",C['green'],"N")]:
            sr.addWidget(stat_card(v,l,c,ic))
        lay.addLayout(sr)

        lay.addWidget(lbl("Research Problem Solver","section"))
        grid=QGridLayout(); grid.setSpacing(12)
        features=[
            ("Literature overload","Find relevant papers semantically instead of hunting keywords.","Search","search",C['purple']),
            ("Weak research gap","Detect gaps, limitations, and future-work angles from abstracts.","Open Tools","tools",C['blue']),
            ("Slow screening","Score inclusion/exclusion decisions with a repeatable screening workflow.","Screen Papers","screen",C['purple']),
            ("Hard abstracts","Convert dense abstracts into plain-English summaries and key points.","Summarize","summarize",C['blue']),
            ("Citation mess","Format citations and export BibTeX, RIS, EndNote-ready records.","Citations","tools",C['purple']),
            ("Project chaos","Organize papers, tasks, bookmarks, reading status, and sessions.","Workspace","workspace",C['blue']),
        ]
        for i,(title,desc,action,page,accent) in enumerate(features):
            grid.addWidget(feature_card(title,desc,action,page,self.go_to,accent),i//3,i%3)
        lay.addLayout(grid)

        suite=card(); sul=QVBoxLayout(suite); sul.setContentsMargins(20,18,20,18); sul.setSpacing(12)
        sul.addWidget(QLabel("500+ Research Suite Capabilities",
            styleSheet=f"font-size:16px;font-weight:900;color:{C['t0']};background:transparent;"))
        sul.addWidget(QLabel(
            "Built for thesis writers, PhD scholars, professors, systematic reviewers, and research teams.",
            styleSheet=f"font-size:12.5px;color:{C['t2']};background:transparent;"))
        caps=[
            ("Discover",["semantic search","keyword search","category filters","similar papers","bookmarking","reading queue","paper preview","arXiv opening"]),
            ("Understand",["AI summaries","plain-English explanation","method extraction","contribution detection","limitation detection","key terms","impact scoring","hypothesis ideas"]),
            ("Review",["inclusion screening","exclusion screening","threshold tuning","CSV import","screening sessions","PRISMA-ready counts","decision audit trail","progress metrics"]),
            ("Write",["research gap finder","related-work drafts","citation formatter","BibTeX export","RIS export","EndNote export","APA/MLA/IEEE support","abstract improvement"]),
            ("Manage",["research workspace","project papers","task tracking","reading status","history","notifications","profile settings","API key view"]),
            ("Admin",["billing plans","promo codes","invoice PDF","payment history","team plans","admin dashboard","support tickets","audit logs"]),
        ]
        cg=QGridLayout(); cg.setSpacing(10)
        for i,(group,items) in enumerate(caps):
            box=QFrame(); box.setObjectName("feature_card"); bl=QVBoxLayout(box)
            bl.setContentsMargins(14,12,14,12); bl.setSpacing(6)
            bl.addWidget(QLabel(group,styleSheet=f"font-size:13px;font-weight:900;color:{C['purp2']};background:transparent;"))
            tx=QLabel(" | ".join(items)); tx.setWordWrap(True)
            tx.setStyleSheet(f"font-size:11.5px;color:{C['t2']};line-height:150%;background:transparent;")
            bl.addWidget(tx)
            cg.addWidget(box,i//3,i%3)
        sul.addLayout(cg)
        lay.addWidget(suite)

        # 2-col: credits + info
        cols=QHBoxLayout(); cols.setSpacing(14)
        cc=card(); cl=QVBoxLayout(cc); cl.setContentsMargins(20,18,20,18); cl.setSpacing(10)
        cl.addWidget(lbl("Credits Usage","section"))
        used=self.user['credits_used']; lim=self.user['credits_limit']
        cl.addWidget(progress_row("Credits used",used,lim,C['purple']))
        cl.addWidget(QLabel(f"{lim-used} remaining",
            styleSheet=f"font-size:12px;color:{C['grn2']};font-weight:700;background:transparent;"))
        if self.user['plan']=='free':
            ub=QPushButton("Upgrade to Pro"); ub.setObjectName("btn_ghost"); ub.setFixedHeight(36)
            ub.clicked.connect(lambda:self.go_to.emit("billing")); cl.addWidget(ub)
        cl.addStretch()

        ic=card(); il=QVBoxLayout(ic); il.setContentsMargins(20,18,20,18); il.setSpacing(10)
        il.addWidget(lbl("Account Info","section"))
        for k,v in [("Plan",self.user['plan'].capitalize()),
                    ("Member Since",self.user['created_at'][:10]),
                    ("Search Mode",backend.mode.capitalize() if backend.loaded else "Loading..."),
                    ("Papers",f"{backend.paper_count:,}" if backend.loaded else "Loading...")]:
            row=QHBoxLayout()
            row.addWidget(QLabel(k,styleSheet=f"font-size:12px;color:{C['t2']};background:transparent;"))
            row.addStretch()
            row.addWidget(QLabel(str(v),styleSheet=f"font-size:12px;color:{C['t1']};font-weight:700;background:transparent;"))
            il.addLayout(row)
        il.addStretch()
        cols.addWidget(cc,1); cols.addWidget(ic,1); lay.addLayout(cols)

        # Recent searches
        lay.addWidget(lbl("Recent Searches","section"))
        hcard=card(); hlay=QVBoxLayout(hcard); hlay.setContentsMargins(16,12,16,12); hlay.setSpacing(0)
        searches=get_search_history(self.user['id'],6)
        if searches:
            for h in searches:
                row=QHBoxLayout()
                q=h['query']; q=q[:60]+"..." if len(q)>60 else q
                row.addWidget(QLabel(f"Search: {q}",
                    styleSheet=f"font-size:13px;color:{C['t1']};padding:9px 4px;background:transparent;"))
                row.addStretch()
                row.addWidget(QLabel(f"{h['results']} results",
                    styleSheet=f"font-size:11px;color:{C['purp2']};background:transparent;"))
                row.addSpacing(16)
                row.addWidget(QLabel(h['ts'][:10],
                    styleSheet=f"font-size:11px;color:{C['t3']};background:transparent;"))
                hlay.addLayout(row); hlay.addWidget(hline())
        else:
            hlay.addWidget(QLabel("  No searches yet - try the Search tab!",
                styleSheet=f"color:{C['t3']};font-size:13px;padding:16px;background:transparent;"))
        lay.addWidget(hcard); lay.addStretch()

        out=QVBoxLayout(self); out.setContentsMargins(16,16,16,16); out.setSpacing(12); out.addWidget(scrolled(inner))


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  SEARCH PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class SearchPage(QWidget):
    to_sum     = pyqtSignal(str,str)
    to_analyze = pyqtSignal(dict)

    def __init__(self,user,settings):
        super().__init__(); self.user=user; self.settings=settings
        self._results=[]; self._sel={}; self._worker=None; self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(28,20,28,20); lay.setSpacing(16)
        ml=tag(backend.mode.capitalize()+" Search" if backend.loaded else "Loading...","purple")
        lay.addWidget(page_header("Smart Paper Discovery",
            "50,000 ArXiv papers | FAISS semantic search | TF-IDF fallback",ml))

        # Search card
        sc=card(); scl=QVBoxLayout(sc); scl.setContentsMargins(22,20,22,18); scl.setSpacing(12)
        main_row=QHBoxLayout(); main_row.setSpacing(10)
        self.query=QLineEdit()
        self.query.setPlaceholderText(
            "Type research question... e.g.  transformer attention mechanism NLP classification")
        self.query.setFixedHeight(50)
        self.query.setStyleSheet(f"font-size:14px;border-radius:12px;padding:0 20px;"
                                  f"border:2px solid {C['bord2']};")
        self.query.returnPressed.connect(self.run_search)
        self.srch=QPushButton("Search"); self.srch.setFixedHeight(50); self.srch.setFixedWidth(120)
        self.srch.setStyleSheet(f"font-size:14px;border-radius:12px;")
        self.srch.clicked.connect(self.run_search)
        main_row.addWidget(self.query,1); main_row.addWidget(self.srch)
        scl.addLayout(main_row)

        frow=QHBoxLayout(); frow.setSpacing(10)
        frow.addWidget(QLabel("k:",styleSheet=f"color:{C['t2']};font-size:12px;"))
        self.k_spin=QSpinBox(); self.k_spin.setRange(5,100)
        self.k_spin.setValue(int(self.settings.value("k",10)))
        self.k_spin.setFixedWidth(80); self.k_spin.setFixedHeight(40)
        frow.addWidget(self.k_spin); frow.addSpacing(8)
        frow.addWidget(QLabel("Category:",styleSheet=f"color:{C['t2']};font-size:12px;"))
        self.cat=QComboBox(); self.cat.setFixedHeight(40); self.cat.setMinimumWidth(180)
        cats=["All","cs.AI","cs.CL","cs.LG","cs.CV","cs.NE","stat.ML",
              "astro-ph","hep-ph","quant-ph","cond-mat","gr-qc","math","q-bio","eess","physics"]
        self.cat.addItems(cats); frow.addWidget(self.cat); frow.addStretch()
        for lb2,fn in [("CSV",self._exp_csv),("BibTeX",self._exp_bib),
                       ("RIS",self._exp_ris),("EndNote",self._exp_end)]:
            b=QPushButton(lb2); b.setObjectName("btn_small"); b.clicked.connect(fn)
            frow.addWidget(b)
        scl.addLayout(frow)
        lay.addWidget(sc)

        self.pbar=QProgressBar(); self.pbar.setRange(0,0); self.pbar.setFixedHeight(6)
        self.pbar.setVisible(False); lay.addWidget(self.pbar)

        sp2=QSplitter(Qt.Vertical); sp2.setHandleWidth(6)
        self.table=make_table(["#","Paper ID","Title","Category","Score","Year"],stretch_col=2)
        self.table.itemSelectionChanged.connect(self._row_sel)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._ctx)
        self.table.doubleClicked.connect(self._open_arxiv)
        sp2.addWidget(self.table)

        prev=QWidget(); pl=QVBoxLayout(prev); pl.setContentsMargins(0,8,0,0); pl.setSpacing(6)
        pl.addWidget(QLabel("Abstract Preview",
            styleSheet=f"font-size:12px;font-weight:700;color:{C['t2']};"))
        self.abs_prev=QTextEdit(); self.abs_prev.setReadOnly(True); self.abs_prev.setFixedHeight(100)
        self.abs_prev.setPlaceholderText("Click a row to preview abstract...")
        pl.addWidget(self.abs_prev)
        sp2.addWidget(prev); sp2.setSizes([420,100])
        lay.addWidget(sp2)

        bot=QHBoxLayout(); bot.setSpacing(8)
        self.res_lbl=QLabel("Enter a query and click Search.")
        self.res_lbl.setStyleSheet(f"font-size:12px;color:{C['t3']};")
        self.bm_btn=QPushButton("Bookmark"); self.bm_btn.setObjectName("btn_secondary")
        self.bm_btn.setFixedHeight(40); self.bm_btn.setEnabled(False); self.bm_btn.clicked.connect(self._bookmark)
        self.rl_btn=QPushButton("Read Later"); self.rl_btn.setObjectName("btn_secondary")
        self.rl_btn.setFixedHeight(40); self.rl_btn.setEnabled(False); self.rl_btn.clicked.connect(self._reading)
        self.an_btn=QPushButton("Analyze"); self.an_btn.setObjectName("btn_teal")
        self.an_btn.setFixedHeight(40); self.an_btn.setEnabled(False); self.an_btn.clicked.connect(self._analyze)
        self.sim_btn=QPushButton("Similar"); self.sim_btn.setObjectName("btn_secondary")
        self.sim_btn.setFixedHeight(40); self.sim_btn.setEnabled(False); self.sim_btn.clicked.connect(self._similar)
        self.sum_btn=QPushButton("Summarize"); self.sum_btn.setFixedHeight(40)
        self.sum_btn.setEnabled(False); self.sum_btn.clicked.connect(self._go_sum)
        self.arx_btn=QPushButton("Open"); self.arx_btn.setObjectName("btn_teal"); self.arx_btn.setFixedHeight(40); self.arx_btn.setFixedWidth(90)
        self.arx_btn.setEnabled(False); self.arx_btn.clicked.connect(self._open_arxiv)
        bot.addWidget(self.res_lbl); bot.addStretch()
        for w in [self.bm_btn,self.rl_btn,self.sim_btn,self.arx_btn,self.an_btn,self.sum_btn]:
            bot.addWidget(w)
        lay.addLayout(bot)

    def run_search(self):
        q=self.query.text().strip()
        if not q: QMessageBox.information(self,"Empty","Enter a research question."); return
        if not backend.loaded:
            QMessageBox.warning(self,"Loading","Models loading - please wait a moment."); return
        if not use_credit(self.user['id']):
            QMessageBox.warning(self,"No Credits","Free credits used up! Upgrade to Pro."); return
        k=self.k_spin.value(); cat=self.cat.currentText()
        self.settings.setValue("k",k)
        self.srch.setEnabled(False); self.pbar.setVisible(True)
        self.res_lbl.setText(f"Searching [{backend.mode}]..."); self.table.setRowCount(0)
        for b in [self.sum_btn,self.bm_btn,self.rl_btn,self.an_btn,self.sim_btn,self.arx_btn]:
            b.setEnabled(False)
        self._worker=SearchWorker(q,k,cat)
        self._worker.done.connect(self._done); self._worker.err.connect(self._err)
        self._worker.start()

    def _done(self,results,elapsed):
        self.pbar.setVisible(False); self.srch.setEnabled(True); self._results=results
        self.table.setRowCount(len(results))
        for i,r in enumerate(results):
            self.table.setItem(i,0,QTableWidgetItem(str(r["rank"])))
            self.table.setItem(i,1,QTableWidgetItem(str(r["paper_id"])))
            self.table.setItem(i,2,QTableWidgetItem(r["title"]))
            ci=QTableWidgetItem(r["categories"]); ci.setForeground(QColor(C['purp3']))
            self.table.setItem(i,3,ci)
            si=QTableWidgetItem(f"{r['score']:.4f}"); si.setForeground(QColor(C['grn2']))
            si.setTextAlignment(Qt.AlignCenter); self.table.setItem(i,4,si)
            yi=QTableWidgetItem(r.get("year","-"))
            yi.setTextAlignment(Qt.AlignCenter)
            yi.setForeground(QColor(C['t0']))
            self.table.setItem(i,5,yi)
        self.res_lbl.setText(f"Done: {len(results)} results  |  {elapsed:.2f}s  |  {backend.mode} search")
        add_search(self.user['id'],self.query.text(),self.k_spin.value(),
                   self.cat.currentText(),len(results))
        if not results:
            QMessageBox.information(self,"No Results",
                "No papers found.\nTips: use different keywords, broaden the query, or select 'All' category.")

    def _err(self,msg):
        self.pbar.setVisible(False); self.srch.setEnabled(True)
        QMessageBox.critical(self,"Search Error",f"Search failed:\n\n{msg[:400]}")

    def _row_sel(self):
        row=self.table.currentRow()
        if 0<=row<len(self._results):
            self._sel=self._results[row]
            self.abs_prev.setPlainText(self._sel.get("abstract",""))
            for b in [self.sum_btn,self.bm_btn,self.rl_btn,self.an_btn,self.sim_btn,self.arx_btn]:
                b.setEnabled(True)

    def _go_sum(self):
        if self._sel: self.to_sum.emit(self._sel.get("abstract",""),self._sel.get("title",""))

    def _analyze(self):
        if self._sel: self.to_analyze.emit(self._sel)

    def _similar(self):
        if not self._sel: return
        idx=self._sel.get("df_idx",0)
        results=backend.find_similar(idx,8)
        if not results: QMessageBox.information(self,"No Results","No similar papers found."); return
        dlg=QDialog(self); dlg.setWindowTitle("Similar Papers"); dlg.resize(820,480)
        lay=QVBoxLayout(dlg)
        lay.addWidget(QLabel(f"Papers similar to: {self._sel['title'][:70]}...",
            styleSheet=f"font-size:13px;font-weight:700;color:{C['t0']};padding:4px;"))
        tbl=make_table(["Title","Category","Score"],stretch_col=0)
        tbl.setRowCount(len(results))
        for i,r in enumerate(results):
            tbl.setItem(i,0,QTableWidgetItem(r["title"]))
            ci=QTableWidgetItem(r["categories"]); ci.setForeground(QColor(C['purp3']))
            tbl.setItem(i,1,ci)
            si=QTableWidgetItem(f"{r['score']:.4f}"); si.setForeground(QColor(C['grn2']))
            tbl.setItem(i,2,si)
        def bm_sim():
            row=tbl.currentRow()
            if 0<=row<len(results):
                r=results[row]
                add_bookmark(self.user['id'],r['paper_id'],r['title'],r.get('abstract',''),r['categories'],r['score'])
                QMessageBox.information(dlg,"Bookmarked",f"Saved: {r['title'][:50]}")
        bm=QPushButton("Bookmark Selected"); bm.setObjectName("btn_secondary"); bm.clicked.connect(bm_sim)
        lay.addWidget(tbl); lay.addWidget(bm); dlg.exec_()

    def _bookmark(self):
        if not self._sel: return
        r=self._sel
        ok=add_bookmark(self.user['id'],r['paper_id'],r['title'],r['abstract'],r['categories'],r['score'])
        self.bm_btn.setText("Saved")
        if ok: notify(self.user['id'],f"Bookmarked: {r['title'][:50]}","success")
        QTimer.singleShot(2000,lambda:self.bm_btn.setText("Bookmark"))

    def _reading(self):
        if not self._sel: return
        add_to_reading_list(self.user['id'],self._sel['paper_id'],self._sel['title'])
        self.rl_btn.setText("Added")
        QTimer.singleShot(2000,lambda:self.rl_btn.setText("Read Later"))

    def _open_arxiv(self):
        if self._sel: webbrowser.open(self._sel.get("arxiv_url","https://arxiv.org"))

    def _ctx(self,pos):
        if not self._sel: return
        menu=QMenu(self)
        menu.addAction("Bookmark",self._bookmark)
        menu.addAction("Reading List",self._reading)
        menu.addAction("Analyze Paper",self._analyze)
        menu.addAction("Summarize",self._go_sum)
        menu.addAction("Find Similar",self._similar)
        menu.addSeparator()
        menu.addAction("Open arXiv",self._open_arxiv)
        menu.addAction("Copy Title",lambda:QApplication.clipboard().setText(self._sel.get("title","")))
        menu.addAction("Copy Abstract",lambda:QApplication.clipboard().setText(self._sel.get("abstract","")))
        menu.addAction("Copy arXiv URL",lambda:QApplication.clipboard().setText(self._sel.get("arxiv_url","")))
        menu.exec_(self.table.viewport().mapToGlobal(pos))

    def _exp_csv(self):
        if not self._results: return
        path,_=QFileDialog.getSaveFileName(self,"Export CSV","results.csv","CSV (*.csv)")
        if not path: return
        with open(path,'w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,["rank","paper_id","title","categories","score","abstract","year"])
            w.writeheader(); w.writerows(self._results)
        QMessageBox.information(self,"Exported",f"Saved:\n{path}")

    def _exp_bib(self):
        if not self._results: return
        path,_=QFileDialog.getSaveFileName(self,"Export BibTeX","refs.bib","BibTeX (*.bib)")
        if path:
            open(path,'w',encoding='utf-8').write(backend.to_bibtex(self._results))
            QMessageBox.information(self,"Done",f"Saved:\n{path}")

    def _exp_ris(self):
        if not self._results: return
        path,_=QFileDialog.getSaveFileName(self,"Export RIS","refs.ris","RIS (*.ris)")
        if path:
            open(path,'w',encoding='utf-8').write(backend.to_ris(self._results))
            QMessageBox.information(self,"Done",f"Saved:\n{path}")

    def _exp_end(self):
        if not self._results: return
        path,_=QFileDialog.getSaveFileName(self,"Export EndNote","refs.txt","Text (*.txt)")
        if path:
            open(path,'w',encoding='utf-8').write(backend.to_endnote(self._results))
            QMessageBox.information(self,"Done",f"Saved:\n{path}")

    def focus(self): self.query.setFocus()


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  ANALYSIS PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class AnalysisPage(QWidget):
    def __init__(self,user):
        super().__init__(); self.user=user; self._build()

    def _build(self):
        inner=QWidget(); lay=QVBoxLayout(inner)
        lay.setContentsMargins(28,22,28,22); lay.setSpacing(18)
        lay.addWidget(page_header("Paper Analysis Engine",
            "Methodology | Contributions | Limitations | Impact Score | Keywords | Hypotheses"))

        top=card(); tl=QVBoxLayout(top); tl.setContentsMargins(22,20,22,18); tl.setSpacing(12)
        tl.addWidget(lbl("Paper Title","section"))
        self.title_inp=QLineEdit(); self.title_inp.setFixedHeight(44)
        self.title_inp.setPlaceholderText("Paste paper title here...")
        tl.addWidget(self.title_inp)
        tl.addWidget(lbl("Abstract","section"))
        self.abs_inp=QTextEdit(); self.abs_inp.setFixedHeight(130)
        self.abs_inp.setPlaceholderText("Paste abstract here, or select paper in Search tab and click Analyze...")
        tl.addWidget(self.abs_inp)
        br=QHBoxLayout(); br.setSpacing(10)
        ab=QPushButton("Run Analysis"); ab.setFixedHeight(44); ab.clicked.connect(self._analyze)
        clr=QPushButton("Clear"); clr.setObjectName("btn_secondary"); clr.setFixedHeight(44)
        clr.clicked.connect(self._clear)
        br.addWidget(ab); br.addWidget(clr); br.addStretch()
        tl.addLayout(br)
        lay.addWidget(top)

        # Results section (hidden until analyzed)
        self.res_widget=QWidget(); rl=QVBoxLayout(self.res_widget)
        rl.setContentsMargins(0,0,0,0); rl.setSpacing(16)

        # Impact hero card
        ic=card("card_glow"); icl=QHBoxLayout(ic); icl.setContentsMargins(28,22,28,22); icl.setSpacing(24)
        self.impact_num=QLabel("-")
        self.impact_num.setStyleSheet(f"font-size:52px;font-weight:900;color:{C['purp2']};background:transparent;")
        self.impact_bar=QProgressBar(); self.impact_bar.setRange(0,10)
        self.impact_bar.setFixedHeight(12); self.impact_bar.setTextVisible(False)
        impact_col=QVBoxLayout(); impact_col.setSpacing(6)
        impact_col.addWidget(self.impact_num)
        self.impact_lbl2=QLabel("Impact Score / 10")
        self.impact_lbl2.setStyleSheet(f"font-size:13px;color:{C['t2']};background:transparent;")
        impact_col.addWidget(self.impact_lbl2); impact_col.addWidget(self.impact_bar)
        icl.addLayout(impact_col); icl.addWidget(vline())
        right_info=QGridLayout(); right_info.setSpacing(12)
        self.rtype_tag=tag("-","blue")
        self.novelty_tag=tag("Novelty: -","purple")
        self.repro_tag=tag("Reproducibility: -","green")
        self.words_tag=tag("0 words","yellow")
        for row2,col2,widget2 in [(0,0,self.rtype_tag),(0,1,self.novelty_tag),
                                (1,0,self.repro_tag),(1,1,self.words_tag)]:
            right_info.addWidget(widget2,row2,col2)
        icl.addLayout(right_info); icl.addStretch()
        rl.addWidget(ic)

        # 3-col cards
        cols=QHBoxLayout(); cols.setSpacing(14)
        self.meth_card=card("card_blue"); ml=QVBoxLayout(self.meth_card)
        ml.setContentsMargins(18,16,18,16); ml.setSpacing(8)
        ml.addWidget(lbl("Methodology","section")); self.meth_lay=QVBoxLayout(); ml.addLayout(self.meth_lay); ml.addStretch()

        self.cont_card=card("card_green"); cl=QVBoxLayout(self.cont_card)
        cl.setContentsMargins(18,16,18,16); cl.setSpacing(8)
        cl.addWidget(lbl("Contributions","section")); self.cont_lay=QVBoxLayout(); cl.addLayout(self.cont_lay); cl.addStretch()

        self.lim_card=card("card_yellow"); ll2=QVBoxLayout(self.lim_card)
        ll2.setContentsMargins(18,16,18,16); ll2.setSpacing(8)
        ll2.addWidget(lbl("Limitations","section")); self.lim_lay=QVBoxLayout(); ll2.addLayout(self.lim_lay); ll2.addStretch()

        cols.addWidget(self.meth_card,1); cols.addWidget(self.cont_card,1); cols.addWidget(self.lim_card,1)
        rl.addLayout(cols)

        # Keywords
        kc=card(); kl=QVBoxLayout(kc); kl.setContentsMargins(18,16,18,16); kl.setSpacing(10)
        kl.addWidget(lbl("Key Terms","section"))
        self.kw_row=QHBoxLayout(); self.kw_row.setSpacing(8); self.kw_row.addStretch()
        kl.addLayout(self.kw_row)
        rl.addWidget(kc)

        # Hypotheses
        hc=card("card_pink"); hl2=QVBoxLayout(hc); hl2.setContentsMargins(18,16,18,16); hl2.setSpacing(10)
        hl2.addWidget(lbl("Generated Hypotheses","section"))
        self.hyp_text=QTextEdit(); self.hyp_text.setReadOnly(True); self.hyp_text.setFixedHeight(110)
        copy_hyp=QPushButton("Copy Hypotheses"); copy_hyp.setObjectName("btn_small")
        copy_hyp.clicked.connect(lambda:QApplication.clipboard().setText(self.hyp_text.toPlainText()))
        hl2.addWidget(self.hyp_text); hl2.addWidget(copy_hyp)
        rl.addWidget(hc)

        self.res_widget.setVisible(False)
        lay.addWidget(self.res_widget); lay.addStretch()
        out=QVBoxLayout(self); out.setContentsMargins(16,16,16,16); out.setSpacing(12); out.addWidget(scrolled(inner))

    def set_paper(self,paper_dict):
        self.title_inp.setText(paper_dict.get("title",""))
        self.abs_inp.setPlainText(paper_dict.get("abstract",""))
        self._analyze()

    def _analyze(self):
        title=self.title_inp.text().strip()
        abstract=self.abs_inp.toPlainText().strip()
        if not abstract: QMessageBox.information(self,"Empty","Paste an abstract to analyze."); return
        result=backend.analyze_paper(title,abstract)

        # Impact
        self.impact_num.setText(str(result['impact_score']))
        self.impact_bar.setValue(result['impact_score'])
        colors={"Low":C['red'],"Low-Moderate":C['orange'],"Moderate":C['yellow'],
                "Moderate-High":C['teal'],"High":C['green'],"Very High":C['purp2']}
        c2=colors.get(result['impact_label'],C['purp2'])
        self.impact_num.setStyleSheet(f"font-size:52px;font-weight:900;color:{c2};background:transparent;")
        self.impact_lbl2.setText(f"Impact: {result['impact_label']}  |  {result['research_type']}")
        self.rtype_tag.setText(f"  {result['research_type']}  ")
        self.novelty_tag.setText(f"  Novelty: {result['novelty_score']}/5  ")
        self.repro_tag.setText(f"  {'Reproducible' if result['reproducible'] else 'Not Reproducible'}  ")
        self.words_tag.setText(f"  {result['abstract_length']} words  ")

        # Clear and fill method/contrib/lim lists
        for lay_obj,items,color,icon in [
            (self.meth_lay,result['methods'],C['blue2'],"-"),
            (self.cont_lay,result['contributions'],C['grn2'],"-"),
            (self.lim_lay,result['limitations'],C['yel2'],"-"),
        ]:
            for i in reversed(range(lay_obj.count())):
                w=lay_obj.itemAt(i).widget()
                if w: w.deleteLater()
            for item in items[:6]:
                t=QLabel(f"  {icon} {item}")
                t.setStyleSheet(f"font-size:12.5px;color:{color};padding:2px 0;background:transparent;")
                lay_obj.addWidget(t)

        # Keywords
        for i in reversed(range(self.kw_row.count()-1)):
            w=self.kw_row.itemAt(i).widget()
            if w: w.deleteLater()
        kw_colors=[C['purple'],C['blue'],C['teal'],C['green'],C['yellow'],C['pink'],C['orange'],C['indigo']]
        for j,kw in enumerate(result['keywords'][:12]):
            c3=kw_colors[j%len(kw_colors)]
            kl=QLabel(f"  {kw}  ")
            kl.setStyleSheet(f"background:{c3}22;color:{c3};border:1px solid {c3}40;"
                             f"border-radius:6px;padding:4px 10px;font-size:12px;font-weight:600;")
            self.kw_row.insertWidget(self.kw_row.count()-1,kl)

        # Hypotheses
        hyps=backend.generate_hypothesis(title,abstract)
        self.hyp_text.setPlainText("\n\n".join(hyps))

        self.res_widget.setVisible(True)

    def _clear(self):
        self.title_inp.clear(); self.abs_inp.clear()
        self.res_widget.setVisible(False)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  SUMMARIZE PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class SummarizePage(QWidget):
    def __init__(self,user):
        super().__init__(); self.user=user; self._worker=None; self._title=""
        self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(28,20,28,20); lay.setSpacing(16)
        lay.addWidget(page_header("Abstract Summarizer",
            "BART-large-cnn neural summarizer | Extractive fallback | History saved automatically"))

        pc=card(); pl=QHBoxLayout(pc); pl.setContentsMargins(18,12,18,12); pl.setSpacing(16)
        for lt2,attr,rng,val in [("Max tokens","max_len",(50,300),130),
                                  ("Min tokens","min_len",(10,80),30),
                                  ("Beams","beams",(1,8),4)]:
            row=QHBoxLayout(); row.setSpacing(8)
            row.addWidget(QLabel(lt2,styleSheet=f"color:{C['t2']};font-size:12px;"))
            sp2=QSpinBox(); sp2.setRange(*rng); sp2.setValue(val)
            sp2.setFixedWidth(80); sp2.setFixedHeight(36)
            setattr(self,attr,sp2); row.addWidget(sp2); pl.addLayout(row)
        pl.addStretch()
        lay.addWidget(pc)

        sp3=QSplitter(Qt.Horizontal); sp3.setHandleWidth(8)
        lw=QWidget(); ll2=QVBoxLayout(lw); ll2.setContentsMargins(0,0,8,0); ll2.setSpacing(6)
        ll2.addWidget(QLabel("Original Abstract",
            styleSheet=f"font-size:13px;font-weight:700;color:{C['t0']};"))
        self.abs_edit=QTextEdit()
        self.abs_edit.setPlaceholderText("Paste abstract here or click Search > Summarize...")
        self.abs_edit.textChanged.connect(self._wc)
        ll2.addWidget(self.abs_edit)
        self.wc1=QLabel("0 words")
        self.wc1.setStyleSheet(f"font-size:11px;color:{C['t3']};")
        self.wc1.setAlignment(Qt.AlignRight); ll2.addWidget(self.wc1)

        rw=QWidget(); rl2=QVBoxLayout(rw); rl2.setContentsMargins(8,0,0,0); rl2.setSpacing(6)
        rl2.addWidget(QLabel("Generated Summary",
            styleSheet=f"font-size:13px;font-weight:700;color:{C['t0']};"))
        self.sum_edit=QTextEdit(); self.sum_edit.setReadOnly(True)
        self.sum_edit.setPlaceholderText("Summary will appear here...")
        rl2.addWidget(self.sum_edit)
        self.wc2=QLabel("")
        self.wc2.setStyleSheet(f"font-size:11px;color:{C['grn2']};font-weight:700;")
        self.wc2.setAlignment(Qt.AlignRight); rl2.addWidget(self.wc2)
        sp3.addWidget(lw); sp3.addWidget(rw); sp3.setSizes([560,560])
        lay.addWidget(sp3)

        cr=QHBoxLayout(); cr.setSpacing(10)
        self.gen_btn=QPushButton("Generate Summary"); self.gen_btn.setFixedHeight(44)
        self.gen_btn.clicked.connect(self.run)
        self.copy_btn=QPushButton("Copy"); self.copy_btn.setObjectName("btn_secondary")
        self.copy_btn.setFixedHeight(44); self.copy_btn.setEnabled(False)
        self.copy_btn.clicked.connect(self._copy)
        self.hist_btn=QPushButton("History"); self.hist_btn.setObjectName("btn_secondary")
        self.hist_btn.setFixedHeight(44); self.hist_btn.clicked.connect(self._history)
        clr2=QPushButton("Clear"); clr2.setObjectName("btn_danger"); clr2.setFixedHeight(44)
        clr2.clicked.connect(self._clear)
        self.tl=QLabel("")
        self.tl.setStyleSheet(f"color:{C['grn2']};font-size:12px;font-weight:700;")
        for w in [self.gen_btn,self.copy_btn,self.hist_btn,clr2]: cr.addWidget(w)
        cr.addStretch(); cr.addWidget(self.tl)
        lay.addLayout(cr)

        self.pbar=QProgressBar(); self.pbar.setRange(0,0); self.pbar.setFixedHeight(6)
        self.pbar.setVisible(False); lay.addWidget(self.pbar)

    def set_abstract(self,text,title=""):
        self.abs_edit.setPlainText(text); self._title=title

    def _wc(self):
        self.wc1.setText(f"{len(self.abs_edit.toPlainText().split())} words")

    def run(self):
        text=self.abs_edit.toPlainText().strip()
        if not text: QMessageBox.information(self,"Empty","Paste an abstract first."); return
        if not backend.loaded: QMessageBox.warning(self,"Not Ready","Models loading..."); return
        if not use_credit(self.user['id']):
            QMessageBox.warning(self,"Credits","Credits used up. Upgrade to Pro!"); return
        self.gen_btn.setEnabled(False); self.pbar.setVisible(True)
        self.sum_edit.clear(); self.tl.setText(""); self.wc2.setText("")
        self._worker=SumWorker(text,self.max_len.value(),self.min_len.value(),self.beams.value())
        self._worker.done.connect(self._done); self._worker.err.connect(self._err)
        self._worker.start()

    def _done(self,summary,elapsed):
        self.pbar.setVisible(False); self.gen_btn.setEnabled(True)
        self.sum_edit.setPlainText(summary); self.copy_btn.setEnabled(True)
        wc=len(summary.split()); self.wc2.setText(f"{wc} words")
        self.tl.setText(f"Done in {elapsed:.2f}s")
        add_summary(self.user['id'],self.abs_edit.toPlainText(),summary,self._title)
        notify(self.user['id'],f"Summary saved ({wc} words)","success")

    def _err(self,msg):
        self.pbar.setVisible(False); self.gen_btn.setEnabled(True)
        QMessageBox.critical(self,"Error",msg[:400])

    def _copy(self):
        QApplication.clipboard().setText(self.sum_edit.toPlainText())
        self.copy_btn.setText("Copied")
        QTimer.singleShot(2000,lambda:self.copy_btn.setText("Copy"))

    def _clear(self):
        self.abs_edit.clear(); self.sum_edit.clear()
        self.tl.setText(""); self.copy_btn.setEnabled(False); self.wc2.setText("")

    def _history(self):
        dlg=QDialog(self); dlg.setWindowTitle("Summary History"); dlg.resize(820,500)
        lay=QVBoxLayout(dlg)
        tbl=make_table(["Paper Title","Summary Preview","Words","Date"],stretch_col=1)
        sums=get_summaries(self.user['id']); tbl.setRowCount(len(sums))
        for i,s in enumerate(sums):
            tbl.setItem(i,0,QTableWidgetItem(s.get('paper_title','')[:40]))
            tbl.setItem(i,1,QTableWidgetItem(s['summary'][:90]+"..."))
            tbl.setItem(i,2,QTableWidgetItem(str(s.get('word_count',0))))
            tbl.setItem(i,3,QTableWidgetItem(s['ts'][:10]))
        def load():
            row=tbl.currentRow()
            if 0<=row<len(sums):
                self.abs_edit.setPlainText(sums[row]['abstract'])
                self.sum_edit.setPlainText(sums[row]['summary']); dlg.close()
        lb2=QPushButton("Load Selected"); lb2.clicked.connect(load)
        lay.addWidget(tbl); lay.addWidget(lb2); dlg.exec_()


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  RESEARCH TOOLS PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class ResearchToolsPage(QWidget):
    def __init__(self,user):
        super().__init__(); self.user=user; self._last_results=[]; self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(28,20,28,20); lay.setSpacing(0)
        lay.addWidget(page_header("Research Tools",
            "Research Gap Finder | Related Work Generator | Hypothesis Builder | Category Analytics"))

        top_info = card("card_glow")
        top_info.setFixedHeight(84)
        top_info.setObjectName("top_info")
        top_tip = QLabel(
            "Advanced research workflows in one place: gap detection, hypothesis generation, literature mapping, citation formatting, and research problem planning.")
        top_tip.setWordWrap(True)
        top_tip.setStyleSheet(f"font-size:13px;color:{C['t1']};padding:10px 12px;")
        htop = QHBoxLayout(top_info)
        htop.setContentsMargins(16,16,16,16)
        htop.addWidget(top_tip)
        lay.addWidget(top_info)

        tabs=QTabWidget(); lay.addWidget(tabs)

        # â”€â”€ Tab 1: Research Gap Finder â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        gap_tab=QWidget(); gl=QVBoxLayout(gap_tab); gl.setContentsMargins(20,16,20,16); gl.setSpacing(14)
        gl.addWidget(QLabel("Research Gap Finder",
            styleSheet=f"font-size:15px;font-weight:700;color:{C['t0']};"))
        gl.addWidget(QLabel(
            "Run a search first, then click Detect Gaps to find unexplored areas in that literature.",
            styleSheet=f"font-size:12px;color:{C['t2']};background:transparent;"))
        self.gap_query=QLineEdit(); self.gap_query.setFixedHeight(44)
        self.gap_query.setPlaceholderText("Enter topic... e.g. deep learning medical imaging")
        gap_btn=QPushButton("Search and Detect Research Gaps"); gap_btn.setFixedHeight(44)
        gap_btn.clicked.connect(self._detect_gaps)
        self.gap_pbar=QProgressBar(); self.gap_pbar.setRange(0,0); self.gap_pbar.setFixedHeight(6)
        self.gap_pbar.setVisible(False)
        self.gap_results=QWidget(); gr=QVBoxLayout(self.gap_results)
        gr.setContentsMargins(0,0,0,0); gr.setSpacing(10)
        self.gap_results.setVisible(False)
        gl.addWidget(fl("Research Topic")); gl.addWidget(self.gap_query)
        gl.addWidget(gap_btn); gl.addWidget(self.gap_pbar); gl.addWidget(self.gap_results)
        gl.addStretch()
        tabs.addTab(gap_tab,"Research Gaps")

        # â”€â”€ Tab 2: Related Work Generator â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        rw_tab=QWidget(); rwl=QVBoxLayout(rw_tab); rwl.setContentsMargins(20,16,20,16); rwl.setSpacing(12)
        rwl.addWidget(QLabel("Related Work Generator",
            styleSheet=f"font-size:15px;font-weight:700;color:{C['t0']};"))
        rwl.addWidget(QLabel(
            "Enter your paper title and abstract to auto-generate a Related Work paragraph.",
            styleSheet=f"font-size:12px;color:{C['t2']};background:transparent;"))
        self.rw_title=QLineEdit(); self.rw_title.setFixedHeight(44)
        self.rw_title.setPlaceholderText("Your paper title...")
        self.rw_abs=QTextEdit(); self.rw_abs.setFixedHeight(120)
        self.rw_abs.setPlaceholderText("Your paper abstract...")
        rw_btn=QPushButton("Generate Related Work Paragraph"); rw_btn.setFixedHeight(44)
        rw_btn.clicked.connect(self._gen_rw)
        self.rw_output=QTextEdit(); self.rw_output.setReadOnly(True); self.rw_output.setFixedHeight(160)
        self.rw_output.setPlaceholderText("Generated related work will appear here...")
        rw_copy=QPushButton("Copy Text"); rw_copy.setObjectName("btn_secondary")
        rw_copy.clicked.connect(lambda:QApplication.clipboard().setText(self.rw_output.toPlainText()))
        rwl.addWidget(fl("Your Paper Title")); rwl.addWidget(self.rw_title)
        rwl.addWidget(fl("Your Abstract")); rwl.addWidget(self.rw_abs)
        rwl.addWidget(rw_btn)
        rwl.addWidget(fl("Generated Text")); rwl.addWidget(self.rw_output); rwl.addWidget(rw_copy)
        rwl.addStretch()
        tabs.addTab(rw_tab,"Related Work")

        # â”€â”€ Tab 3: Hypothesis Builder â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        hb_tab=QWidget(); hbl=QVBoxLayout(hb_tab); hbl.setContentsMargins(20,16,20,16); hbl.setSpacing(12)
        hbl.addWidget(QLabel("Hypothesis Builder",
            styleSheet=f"font-size:15px;font-weight:700;color:{C['t0']};"))
        hbl.addWidget(QLabel(
            "Generate testable research hypotheses from your topic, title, and abstract.",
            styleSheet=f"font-size:12px;color:{C['t2']};background:transparent;"))
        self.hyp_title=QLineEdit(); self.hyp_title.setFixedHeight(44)
        self.hyp_title.setPlaceholderText("Your paper title...")
        self.hyp_abs=QTextEdit(); self.hyp_abs.setFixedHeight(120)
        self.hyp_abs.setPlaceholderText("Paper abstract or research idea...")
        hb_btn=QPushButton("Generate Hypotheses"); hb_btn.setFixedHeight(44)
        hb_btn.clicked.connect(self._gen_hypothesis)
        self.hyp_output=QTextEdit(); self.hyp_output.setReadOnly(True); self.hyp_output.setFixedHeight(160)
        self.hyp_output.setPlaceholderText("Generated hypotheses will appear here...")
        hyp_copy=QPushButton("Copy Hypotheses"); hyp_copy.setObjectName("btn_secondary")
        hyp_copy.clicked.connect(lambda: QApplication.clipboard().setText(self.hyp_output.toPlainText()))
        hbl.addWidget(fl("Title")); hbl.addWidget(self.hyp_title)
        hbl.addWidget(fl("Abstract / Problem Statement")); hbl.addWidget(self.hyp_abs)
        hbl.addWidget(hb_btn); hbl.addWidget(fl("Hypotheses")); hbl.addWidget(self.hyp_output); hbl.addWidget(hyp_copy)
        hbl.addStretch()
        tabs.addTab(hb_tab,"Hypotheses")

        # â”€â”€ Tab 4: Category Analytics â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        ca_tab=QWidget(); cal=QVBoxLayout(ca_tab); cal.setContentsMargins(20,16,20,16); cal.setSpacing(12)
        cal.addWidget(QLabel("Category and Trend Analytics",
            styleSheet=f"font-size:15px;font-weight:700;color:{C['t0']};"))
        self.analytics_query=QLineEdit(); self.analytics_query.setFixedHeight(44)
        self.analytics_query.setPlaceholderText("Search topic to analyze category distribution...")
        an_btn=QPushButton("Analyze Categories"); an_btn.setFixedHeight(44)
        an_btn.clicked.connect(self._analytics)
        self.an_table=make_table(["Category","Count","% of Results","Bar"],stretch_col=0)
        self.an_table.setFixedHeight(300)
        cal.addWidget(fl("Topic")); cal.addWidget(self.analytics_query)
        cal.addWidget(an_btn); cal.addWidget(self.an_table); cal.addStretch()
        tabs.addTab(ca_tab,"Analytics")

        # â”€â”€ Tab 4: Citation Formatter â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        cf_tab=QWidget(); cfl=QVBoxLayout(cf_tab); cfl.setContentsMargins(20,16,20,16); cfl.setSpacing(12)
        cfl.addWidget(QLabel("Citation Formatter",
            styleSheet=f"font-size:15px;font-weight:700;color:{C['t0']};"))
        cfl.addWidget(QLabel(
            "Paste paper details to format citations in APA, MLA, Chicago, IEEE styles.",
            styleSheet=f"font-size:12px;color:{C['t2']};background:transparent;"))
        self.cit_title=QLineEdit(); self.cit_title.setFixedHeight(44); self.cit_title.setPlaceholderText("Paper title...")
        self.cit_authors=QLineEdit(); self.cit_authors.setFixedHeight(44); self.cit_authors.setPlaceholderText("Authors (comma separated)...")
        self.cit_year=QLineEdit(); self.cit_year.setFixedHeight(44); self.cit_year.setPlaceholderText("Year (e.g. 2023)")
        self.cit_journal=QLineEdit(); self.cit_journal.setFixedHeight(44); self.cit_journal.setPlaceholderText("Journal / Conference...")
        self.cit_style=QComboBox(); self.cit_style.setFixedHeight(44)
        self.cit_style.addItems(["APA","MLA","Chicago","IEEE","Harvard","Vancouver"])
        cf_btn=QPushButton("Format Citation"); cf_btn.setFixedHeight(44); cf_btn.clicked.connect(self._format_cit)
        self.cit_output=QTextEdit(); self.cit_output.setReadOnly(True); self.cit_output.setFixedHeight(120)
        cit_copy=QPushButton("Copy Citation"); cit_copy.setObjectName("btn_secondary")
        cit_copy.clicked.connect(lambda:QApplication.clipboard().setText(self.cit_output.toPlainText()))
        for lbl3,widget3 in [("Title",self.cit_title),("Authors",self.cit_authors),
                              ("Year",self.cit_year),("Journal",self.cit_journal),
                              ("Style",self.cit_style)]:
            cfl.addWidget(fl(lbl3)); cfl.addWidget(widget3)
        cfl.addWidget(cf_btn)
        cfl.addWidget(fl("Formatted Citation")); cfl.addWidget(self.cit_output); cfl.addWidget(cit_copy)
        cfl.addStretch()
        tabs.addTab(cf_tab,"Citations")

        # Tab 5: Research Problem Solver
        ps_tab=QWidget(); psl=QVBoxLayout(ps_tab); psl.setContentsMargins(20,16,20,16); psl.setSpacing(12)
        psl.addWidget(QLabel("Research Problem Solver",
            styleSheet=f"font-size:15px;font-weight:700;color:{C['t0']};"))
        psl.addWidget(QLabel(
            "A simple map from common researcher problems to the Resora feature that solves them.",
            styleSheet=f"font-size:12px;color:{C['t2']};background:transparent;"))
        self.problem_table=make_table(["Rank","Research Problem","Use This Feature","Plan"],stretch_col=1)
        problems=[
            ("1","Identify a research gap","Research Gap Finder","Pro"),
            ("2","Find a novel research idea","Gap Finder + Hypothesis Builder","Pro"),
            ("3","Write a literature review","Search + Summaries + Related Work","Pro"),
            ("4","Search relevant papers","Smart Paper Discovery","Free"),
            ("5","Filter and summarize many papers","Screening + Summarizer","Pro"),
            ("6","Select a research topic","AI Assistant + Trend Analytics","Pro"),
            ("7","Form research questions","AI Assistant","Pro"),
            ("8","Choose methodology","Paper Analysis + AI Assistant","Pro"),
            ("9","Find datasets or data sources","AI Assistant checklist","Pro"),
            ("10","Write paper or thesis sections","Related Work Generator","Pro"),
            ("11","Manage citations and references","Citation Formatter + Exports","Pro"),
            ("12","Organize research notes","Research Workspace","Pro"),
            ("13","Reduce information overload","Search filters + Summaries","Pro"),
            ("14","Plan data collection","AI Assistant checklist","Pro"),
            ("15","Analyze and interpret results","AI Assistant + Analysis notes","Pro"),
            ("16","Track progress","Workspace tasks","Pro"),
            ("17","Select journal or conference","AI Assistant checklist","Pro"),
            ("18","Find collaborators","Workspace and profile planning","University"),
            ("19","Find funding or grants","AI Assistant checklist","University"),
            ("20","Stay updated on trends","Trend Analytics","Pro"),
        ]
        self.problem_table.setRowCount(len(problems))
        for i,row in enumerate(problems):
            for j,val in enumerate(row):
                item=QTableWidgetItem(val)
                if j==3:
                    item.setForeground(QColor(C['grn2'] if val=="Free" else (C['purp2'] if val=="Pro" else C['blue2'])))
                self.problem_table.setItem(i,j,item)
        psl.addWidget(self.problem_table)
        psl.addStretch()
        tabs.addTab(ps_tab,"Problem Solver")

    def _detect_gaps(self):
        query=self.gap_query.text().strip()
        if not query: QMessageBox.information(self,"Empty","Enter a research topic."); return
        if not backend.loaded: QMessageBox.warning(self,"Not Ready","Models loading..."); return
        self.gap_pbar.setVisible(True)
        QApplication.processEvents()
        try:
            results=backend.search(query,15,"")
            gaps=backend.detect_research_gaps(query,results)
            # Clear previous
            for i in reversed(range(self.gap_results.layout().count())):
                w=self.gap_results.layout().itemAt(i).widget()
                if w: w.deleteLater()
            if not gaps:
                self.gap_results.layout().addWidget(
                    QLabel("No clear gaps detected - the literature appears comprehensive.",
                           styleSheet=f"color:{C['t2']};font-size:13px;"))
            else:
                for g in gaps:
                    gc=card("card_glow"); gl2=QVBoxLayout(gc)
                    gl2.setContentsMargins(16,12,16,12); gl2.setSpacing(6)
                    gl2.addWidget(QLabel(f"{g['label']}",
                        styleSheet=f"font-size:13px;font-weight:700;color:{C['purp3']};background:transparent;"))
                    gl2.addWidget(QLabel(g['description'],
                        styleSheet=f"font-size:12px;color:{C['t2']};background:transparent;",
                        wordWrap=True))
                    self.gap_results.layout().addWidget(gc)
            self.gap_results.setVisible(True)
        except Exception as e:
            QMessageBox.critical(self,"Error",str(e))
        finally:
            self.gap_pbar.setVisible(False)

    def _gen_rw(self):
        title=self.rw_title.text().strip()
        abstract=self.rw_abs.toPlainText().strip()
        if not abstract: QMessageBox.information(self,"Empty","Enter title and abstract."); return
        if not backend.loaded: QMessageBox.warning(self,"Not Ready","Models loading..."); return
        results=backend.search(f"{title} {abstract[:100]}",6,"")
        text=backend.generate_related_work_text(title,abstract,results)
        self.rw_output.setPlainText(text)

    def _gen_hypothesis(self):
        title=self.hyp_title.text().strip()
        abstract=self.hyp_abs.toPlainText().strip()
        if not title and not abstract:
            QMessageBox.information(self,"Empty","Enter a paper title or abstract."); return
        if not backend.loaded:
            QMessageBox.warning(self,"Not Ready","Models loading..."); return
        hypotheses=backend.generate_hypothesis(title or "", abstract or "")
        self.hyp_output.setPlainText("\n\n".join(hypotheses))

    def _analytics(self):
        query=self.analytics_query.text().strip()
        if not query: return
        if not backend.loaded: return
        results=backend.search(query,20,"")
        stats=backend.get_category_stats(results)
        total=sum(stats.values())
        self.an_table.setRowCount(len(stats))
        for i,(cat,count) in enumerate(sorted(stats.items(),key=lambda x:-x[1])):
            self.an_table.setItem(i,0,QTableWidgetItem(cat))
            self.an_table.setItem(i,1,QTableWidgetItem(str(count)))
            pct=f"{count/total*100:.1f}%" if total else "-"
            self.an_table.setItem(i,2,QTableWidgetItem(pct))
            bar="#"*int(count/max(stats.values())*20)
            bi=QTableWidgetItem(bar); bi.setForeground(QColor(C['purple']))
            self.an_table.setItem(i,3,bi)

    def _format_cit(self):
        t=self.cit_title.text().strip()
        a=self.cit_authors.text().strip()
        y=self.cit_year.text().strip()
        j=self.cit_journal.text().strip()
        style=self.cit_style.currentText()
        if not t: return
        authors_list=[x.strip() for x in a.split(",") if x.strip()]
        def fmt_apa(authors,year,title,journal):
            a_str=", ".join(authors[:3])+(" et al." if len(authors)>3 else "")
            return f"{a_str} ({year}). {title}. {journal}."
        def fmt_mla(authors,year,title,journal):
            a_str=authors[0] if authors else "Unknown"
            return f'{a_str}. "{title}." {journal}, {year}.'
        def fmt_chicago(authors,year,title,journal):
            a_str=" and ".join(authors[:2])+(" et al." if len(authors)>2 else "")
            return f'{a_str}. "{title}." {journal} ({year}).'
        def fmt_ieee(authors,year,title,journal):
            a_str=", ".join([f"{a.split()[-1]}, {' '.join(a.split()[:-1])}" for a in authors[:3]])
            return f'{a_str}, "{title}," {journal}, {year}.'
        def fmt_harvard(authors,year,title,journal):
            a_str=", ".join(authors[:3])+(" et al." if len(authors)>3 else "")
            return f"{a_str} {year}, '{title}', {journal}."
        def fmt_vancouver(authors,year,title,journal):
            a_str=" ".join(f"{a.split()[-1]} {''.join(x[0] for x in a.split()[:-1])}" for a in authors[:6])
            return f"{a_str}. {title}. {journal}. {year}."
        fmts={"APA":fmt_apa,"MLA":fmt_mla,"Chicago":fmt_chicago,
              "IEEE":fmt_ieee,"Harvard":fmt_harvard,"Vancouver":fmt_vancouver}
        fn=fmts.get(style,fmt_apa)
        result=fn(authors_list or ["Unknown"],y or "n.d.",t,j or "Unpublished")
        self.cit_output.setPlainText(result)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  AI ASSISTANT (Chat) PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class AIChatPage(QWidget):
    def __init__(self,user):
        super().__init__(); self.user=user; self._session=str(uuid.uuid4())[:8]; self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(28,20,28,20); lay.setSpacing(12)
        lay.addWidget(page_header("AI Research Assistant",
            "Ask questions about your research | Get methodology advice | Explain statistics"))

        sp2=QSplitter(Qt.Horizontal); sp2.setHandleWidth(6)

        # Left: chat
        chat_w=QWidget(); cl=QVBoxLayout(chat_w); cl.setContentsMargins(0,0,8,0); cl.setSpacing(10)
        hdr_row=QHBoxLayout()
        hdr_row.addWidget(QLabel("Chat",styleSheet=f"font-size:14px;font-weight:700;color:{C['t0']};"))
        hdr_row.addStretch()
        new_btn=QPushButton("+ New Chat"); new_btn.setObjectName("btn_small")
        new_btn.clicked.connect(self._new_chat); hdr_row.addWidget(new_btn)
        cl.addLayout(hdr_row)

        self.chat_area=QScrollArea(); self.chat_area.setWidgetResizable(True)
        self.chat_area.setFrameShape(QFrame.NoFrame)
        self.chat_inner=QWidget(); self.chat_lay=QVBoxLayout(self.chat_inner)
        self.chat_lay.setContentsMargins(4,4,4,4); self.chat_lay.setSpacing(10)
        self.chat_lay.addStretch()
        self.chat_area.setWidget(self.chat_inner)
        cl.addWidget(self.chat_area,1)

        inp_row=QHBoxLayout(); inp_row.setSpacing(8)
        self.chat_inp=QLineEdit()
        self.chat_inp.setFixedHeight(44)
        self.chat_inp.setPlaceholderText("Ask about your research, methodology, statistics...")
        self.chat_inp.returnPressed.connect(self._send)
        send_btn=QPushButton("Send"); send_btn.setFixedHeight(46); send_btn.setFixedWidth(80)
        send_btn.clicked.connect(self._send)
        inp_row.addWidget(self.chat_inp,1); inp_row.addWidget(send_btn)
        cl.addLayout(inp_row)
        sp2.addWidget(chat_w)

        # Right: quick actions
        qa_w=QWidget(); qa_lay=QVBoxLayout(qa_w); qa_lay.setContentsMargins(8,0,0,0); qa_lay.setSpacing(10)
        qa_lay.addWidget(QLabel("Quick Prompts",
            styleSheet=f"font-size:14px;font-weight:700;color:{C['t0']};"))
        prompts=[
            ("Explain statistics","Explain p-value, confidence intervals, and statistical significance for a non-statistician."),
            ("Methodology advice","What are the best methodologies for conducting a systematic literature review?"),
            ("Write research gap","How do I identify and write about research gaps in my literature review?"),
            ("Study design","What is the difference between qualitative, quantitative, and mixed methods research?"),
            ("Cite correctly","Explain the difference between APA, MLA, and IEEE citation styles with examples."),
            ("Hypothesis writing","How do I write a strong research hypothesis? Give me a template."),
            ("Improve abstract","What are the key elements of a high-quality research abstract?"),
            ("AI in research","How can I responsibly use AI tools in my academic research?"),
        ]
        for label,prompt in prompts:
            btn=QPushButton(label); btn.setObjectName("btn_secondary"); btn.setFixedHeight(36)
            btn.clicked.connect(partial(self._quick,prompt)); qa_lay.addWidget(btn)
        qa_lay.addStretch()
        sp2.addWidget(qa_w)
        sp2.setSizes([680,220])
        lay.addWidget(sp2)
        self._add_ai_msg("Hello! I'm your AI Research Assistant. Ask me anything about:\n\n"
                          "- Methodology and study design\n- Statistical analysis\n"
                          "- Literature review best practices\n- Research writing tips\n"
                          "- Finding and citing sources\n\nHow can I help you today?")

    def _send(self):
        text=self.chat_inp.text().strip()
        if not text: return
        self.chat_inp.clear()
        self._add_user_msg(text)
        save_chat_message(self.user['id'],self._session,"user",text)
        QApplication.processEvents()
        response=self._get_response(text)
        self._add_ai_msg(response)
        save_chat_message(self.user['id'],self._session,"assistant",response)

    def _quick(self,prompt):
        self.chat_inp.setText(prompt); self._send()

    def _get_response(self,text):
        t=text.lower()
        if any(w in t for w in ["p-value","statistical","significance","anova","t-test","chi","regression"]):
            return ("**Statistical Methods Guide:**\n\n"
                    "- **p-value**: Probability of observing results at least as extreme as yours if the null hypothesis is true. p<0.05 = statistically significant.\n"
                    "- **Confidence Interval**: Range where the true population parameter falls with X% certainty (e.g., 95% CI).\n"
                    "- **Effect Size**: Magnitude of difference. Report it alongside p-values.\n"
                    "- **Power Analysis**: Determines required sample size before data collection.\n"
                    "- **Multiple Comparisons**: Use Bonferroni correction or FDR when testing multiple hypotheses.\n\n"
                    "Tip: Always report effect sizes alongside p-values for complete statistical reporting.")
        if any(w in t for w in ["systematic review","literature review","prisma","screening"]):
            return ("**Systematic Literature Review Guide:**\n\n"
                    "1. **PICO/PICOS Framework**: Define Population, Intervention, Comparison, Outcome, Study type.\n"
                    "2. **Search Strategy**: Use multiple databases (PubMed, Scopus, Web of Science, IEEE Xplore).\n"
                    "3. **Inclusion/Exclusion Criteria**: Define before searching to avoid bias.\n"
                    "4. **PRISMA Flow**: Track records identified > screened > eligible > included.\n"
                    "5. **Quality Assessment**: Use GRADE, Cochrane RoB, or CASP tools.\n"
                    "6. **Data Extraction**: Use standardized forms; extract in duplicate.\n\n"
                    "Use Resora's Screen tab for automated inclusion/exclusion screening!")
        if any(w in t for w in ["hypothesis","research question","h1","h2","null"]):
            return ("**Writing Research Hypotheses:**\n\n"
                    "**Structure**: [Independent Variable] will [direction] [Dependent Variable] in [population/context].\n\n"
                    "**Types:**\n"
                    "- **Null hypothesis**: No significant difference or relationship exists.\n"
                    "- **Alternative hypothesis**: A significant difference or relationship exists.\n"
                    "- **Directional**: Specifies the direction, such as increase or decrease.\n"
                    "- **Non-directional**: States a difference exists without direction.\n\n"
                    "**Example**: 'Hâ‚: Applying transformer-based models to medical text classification will yield significantly higher F1 scores (p<0.05) compared to traditional ML baselines.'\n\n"
                    "Use the Analysis tab > Hypotheses section for AI-generated hypotheses!")
        if any(w in t for w in ["abstract","write","introduction","conclusion","paper"]):
            return ("**Academic Writing Tips:**\n\n"
                    "**Abstract structure (250-300 words):**\n"
                    "1. Background/Problem (1-2 sentences)\n"
                    "2. Gap in literature (1 sentence)\n"
                    "3. Objective/Aim (1 sentence)\n"
                    "4. Methods (2-3 sentences)\n"
                    "5. Key Results (2-3 sentences)\n"
                    "6. Conclusions & Implications (1-2 sentences)\n\n"
                    "**Introduction structure:**\n"
                    "Hook > Background > Problem > Gap > Research Questions > Contribution > Outline\n\n"
                    "Use the Summarize tab to generate plain-English summaries of complex abstracts!")
        if any(w in t for w in ["methodology","qualitative","quantitative","mixed","design"]):
            return ("**Research Methodology Guide:**\n\n"
                    "**Quantitative**: Numbers, statistics, surveys, experiments. Tests hypotheses. Large samples.\n"
                    "**Qualitative**: Text, interviews, observations. Explores meaning. Small samples.\n"
                    "**Mixed Methods**: Combines both. Sequential, concurrent, or transformative designs.\n\n"
                    "**Study Designs:**\n"
                    "- Experimental (RCT) - Gold standard for causality\n"
                    "- Quasi-experimental - When RCT is not feasible\n"
                    "- Cross-sectional - Snapshot in time\n"
                    "- Longitudinal/Cohort - Over time\n"
                    "- Case Study - Deep single-unit analysis\n"
                    "- Meta-analysis - Synthesizes multiple studies\n\n"
                    "Choose your design based on your research question and available resources.")
        if any(w in t for w in ["cite","citation","reference","apa","mla","ieee","harvard"]):
            return ("**Citation Style Quick Guide:**\n\n"
                    "**APA** (Social sciences): Author, A. A. (Year). Title. Journal, Vol(Issue), pages.\n"
                    "**MLA** (Humanities): Author. \"Title.\" Journal Vol.Issue (Year): pages.\n"
                    "**IEEE** (Engineering): A. Author, \"Title,\" Journal, vol., no., pp., Year.\n"
                    "**Chicago** (History/Arts): Author. \"Title.\" Journal Volume, no. Issue (Year): pages.\n"
                    "**Vancouver** (Medicine): Author AA. Title. Journal. Year;Vol(Issue):pages.\n\n"
                    "Use the Research Tools > Citation Formatter tab to auto-format citations!")
        if any(w in t for w in ["gap","research gap","contribution","novel","originality"]):
            return ("**Finding & Writing Research Gaps:**\n\n"
                    "**How to find gaps:**\n"
                    "1. Read conclusions of 20+ papers - what do authors say 'future work' needs?\n"
                    "2. Look for conflicting findings between papers.\n"
                    "3. Check if methods were tested on limited datasets/domains.\n"
                    "4. Note what populations/contexts were excluded.\n"
                    "5. Use Resora's Research Tools > Gap Finder.\n\n"
                    "**How to write it:**\n"
                    "'Despite X, Y, and Z, there remains a gap in understanding [specific area]. No study has examined [specific combination/context/population].'\n\n"
                    "Gap + Solution = Your Contribution.")
        return (f"Great question about: '{text[:60]}'\n\n"
                "Here are some general research principles:\n\n"
                "- **Be specific**: Narrow your research question for depth over breadth.\n"
                "- **Use primary sources**: Always cite original research, not just reviews.\n"
                "- **Critical thinking**: Question methodology, sample size, and generalizability.\n"
                "- **Peer review**: Prefer peer-reviewed journals (Q1/Q2 in Scopus or WoS).\n"
                "- **Open access**: Check arXiv, PubMed Central, and DOAJ for free access.\n\n"
                "Try asking more specific questions like:\n"
                "- 'How do I write a systematic review?'\n"
                "- 'Explain p-values'\n"
                "- 'How to write a research hypothesis?'")

    def _add_user_msg(self,text):
        w=QFrame(); w.setObjectName("chat_user")
        wl=QHBoxLayout(w); wl.setContentsMargins(12,10,12,10)
        wl.addStretch()
        ml=QLabel(text); ml.setWordWrap(True)
        ml.setStyleSheet(f"color:{C['t0']};font-size:13px;background:transparent;max-width:480px;")
        wl.addWidget(ml,0,Qt.AlignRight)
        self.chat_lay.insertWidget(self.chat_lay.count()-1,w)
        QTimer.singleShot(50,lambda:self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()))

    def _add_ai_msg(self,text):
        w=QFrame(); w.setObjectName("chat_ai")
        wl=QHBoxLayout(w); wl.setContentsMargins(12,10,12,10); wl.setSpacing(10)
        ai_av=QLabel("AI")
        ai_av.setFixedSize(30,30); ai_av.setAlignment(Qt.AlignCenter)
        ai_av.setStyleSheet(f"background:{C['purple']};color:#000000;border-radius:15px;"
                    f"font-size:11px;font-weight:700;")
        ml=QLabel(text); ml.setWordWrap(True)
        ml.setStyleSheet(f"color:{C['t1']};font-size:13px;background:transparent;")
        ml.setTextInteractionFlags(Qt.TextSelectableByMouse)
        wl.addWidget(ai_av,0,Qt.AlignTop); wl.addWidget(ml,1)
        self.chat_lay.insertWidget(self.chat_lay.count()-1,w)
        QTimer.singleShot(50,lambda:self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()))

    def _new_chat(self):
        self._session=str(uuid.uuid4())[:8]
        for i in reversed(range(self.chat_lay.count()-1)):
            w=self.chat_lay.itemAt(i).widget()
            if w: w.deleteLater()
        self._add_ai_msg("New chat started. Ask me anything about your research.")


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  PROJECTS / WORKSPACE PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class WorkspacePage(QWidget):
    def __init__(self,user):
        super().__init__(); self.user=user; self._projects=[]; self._cur_pid=None; self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(28,20,28,20); lay.setSpacing(14)
        lay.addWidget(page_header("Research Workspace",
            "Organize papers into projects | Task manager | Notes | Deadlines"))

        sp2=QSplitter(Qt.Horizontal); sp2.setHandleWidth(8)

        # Left: project list
        lw=QWidget(); ll2=QVBoxLayout(lw); ll2.setContentsMargins(0,0,10,0); ll2.setSpacing(10)
        pl_hdr=QHBoxLayout()
        pl_hdr.addWidget(QLabel("Projects",styleSheet=f"font-size:14px;font-weight:700;color:{C['t0']};"))
        pl_hdr.addStretch()
        new_p=QPushButton("+"); new_p.setObjectName("btn_icon"); new_p.setFixedSize(30,30)
        new_p.setToolTip("Create new project"); new_p.clicked.connect(self._new_project)
        pl_hdr.addWidget(new_p); ll2.addLayout(pl_hdr)

        self.proj_list=QListWidget()
        self.proj_list.setStyleSheet(f"""
            QListWidget{{background:{C['bg2']};border:1px solid {C['border']};border-radius:10px;}}
            QListWidget::item{{padding:12px 14px;color:{C['t1']};border-bottom:1px solid {C['border']};}}
            QListWidget::item:selected{{background:{C['purple']}30;color:{C['purp3']};}}
            QListWidget::item:hover{{background:{C['bg4']};}}
        """)
        self.proj_list.itemClicked.connect(self._load_project)
        ll2.addWidget(self.proj_list,1)
        sp2.addWidget(lw)

        # Right: project detail
        rw=QWidget(); rl2=QVBoxLayout(rw); rl2.setContentsMargins(0,0,0,0); rl2.setSpacing(0)
        self.proj_tabs=QTabWidget()

        # Papers tab
        pp_tab=QWidget(); ppl=QVBoxLayout(pp_tab); ppl.setContentsMargins(12,12,12,12); ppl.setSpacing(10)
        pp_hdr=QHBoxLayout()
        pp_hdr.addWidget(QLabel("Papers in Project",styleSheet=f"font-size:13px;font-weight:700;color:{C['t0']};"))
        pp_hdr.addStretch()
        rm_btn=QPushButton("Remove Selected"); rm_btn.setObjectName("btn_danger"); rm_btn.setFixedHeight(32)
        rm_btn.clicked.connect(self._remove_paper); pp_hdr.addWidget(rm_btn)
        self.pp_table=make_table(["Title","Note","Added"],stretch_col=0); self.pp_table.setFixedHeight(300)
        ppl.addLayout(pp_hdr); ppl.addWidget(self.pp_table); ppl.addStretch()
        self.proj_tabs.addTab(pp_tab,"Papers")

        # Tasks tab
        tk_tab=QWidget(); tkl=QVBoxLayout(tk_tab); tkl.setContentsMargins(12,12,12,12); tkl.setSpacing(10)
        task_hdr=QHBoxLayout()
        self.task_inp=QLineEdit(); self.task_inp.setPlaceholderText("New task..."); self.task_inp.setFixedHeight(38)
        self.task_prio=QComboBox(); self.task_prio.setFixedHeight(40); self.task_prio.setFixedWidth(100)
        self.task_prio.addItems(["high","medium","low"])
        add_task_btn=QPushButton("Add"); add_task_btn.setFixedHeight(38); add_task_btn.clicked.connect(self._add_task)
        task_hdr.addWidget(self.task_inp,1); task_hdr.addWidget(self.task_prio); task_hdr.addWidget(add_task_btn)
        self.task_list=QListWidget()
        self.task_list.setStyleSheet(f"""
            QListWidget{{background:{C['bg2']};border:1px solid {C['border']};border-radius:10px;}}
            QListWidget::item{{padding:10px 14px;color:{C['t1']};border-bottom:1px solid {C['border']};}}
        """)
        done_btn=QPushButton("Toggle Done"); done_btn.setObjectName("btn_secondary"); done_btn.setFixedHeight(34)
        done_btn.clicked.connect(self._toggle_task)
        tkl.addLayout(task_hdr); tkl.addWidget(self.task_list); tkl.addWidget(done_btn); tkl.addStretch()
        self.proj_tabs.addTab(tk_tab,"Tasks")

        rl2.addWidget(self.proj_tabs)
        sp2.addWidget(rw)
        sp2.setSizes([220,680])
        lay.addWidget(sp2)
        self._load_projects()

    def _load_projects(self):
        self._projects=get_projects(self.user['id'])
        self.proj_list.clear()
        for p in self._projects:
            item=QListWidgetItem(f"  {p['name']}")
            item.setForeground(QColor(p.get('color',C['purple'])))
            self.proj_list.addItem(item)

    def _new_project(self):
        name,ok=QInputDialog.getText(self,"New Project","Project name:")
        if ok and name.strip():
            pid=create_project(self.user['id'],name.strip())
            self._load_projects()
            notify(self.user['id'],f"Project '{name}' created","success")

    def _load_project(self,item):
        idx=self.proj_list.row(item)
        if 0<=idx<len(self._projects):
            self._cur_pid=self._projects[idx]['id']
            self._refresh_papers(); self._refresh_tasks()

    def _refresh_papers(self):
        if not self._cur_pid: return
        papers=get_project_papers(self._cur_pid)
        self.pp_table.setRowCount(len(papers))
        for i,p in enumerate(papers):
            self.pp_table.setItem(i,0,QTableWidgetItem(p['title'][:70]))
            self.pp_table.setItem(i,1,QTableWidgetItem(p.get('note','')[:40]))
            self.pp_table.setItem(i,2,QTableWidgetItem(p['ts'][:10]))
        self._papers_data=papers

    def _remove_paper(self):
        if not hasattr(self,'_papers_data'): return
        row=self.pp_table.currentRow()
        if 0<=row<len(self._papers_data):
            pid=self._papers_data[row]['id']
            c=_conn(); c.execute("DELETE FROM project_papers WHERE id=?",(pid,)); c.commit(); c.close()
            self._refresh_papers()

    def _refresh_tasks(self):
        if not self._cur_pid: return
        tasks=get_tasks(self.user['id'],self._cur_pid)
        self.task_list.clear()
        self._tasks_data=tasks
        prio_colors={"high":C['red'],"medium":C['yellow'],"low":C['green']}
        for t in tasks:
            done="Done " if t['done'] else "Open "
            item=QListWidgetItem(f"  {done}[{t['priority'].upper()}]  {t['title']}")
            item.setForeground(QColor(prio_colors.get(t['priority'],C['t1'])))
            if t['done']: item.setForeground(QColor(C['t3']))
            self.task_list.addItem(item)

    def _add_task(self):
        title=self.task_inp.text().strip()
        if not title or not self._cur_pid: return
        add_task(self.user['id'],title,self._cur_pid,self.task_prio.currentText())
        self.task_inp.clear(); self._refresh_tasks()

    def _toggle_task(self):
        if not hasattr(self,'_tasks_data'): return
        row=self.task_list.currentRow()
        if 0<=row<len(self._tasks_data):
            toggle_task(self._tasks_data[row]['id']); self._refresh_tasks()


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  BOOKMARKS PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class BookmarksPage(QWidget):
    def __init__(self,user):
        super().__init__(); self.user=user; self._bms=[]; self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(28,20,28,20); lay.setSpacing(14)
        lay.addWidget(page_header("Bookmarked Papers","Saved papers with notes and collections"))

        top=QHBoxLayout(); top.setSpacing(10)
        self.srch=QLineEdit(); self.srch.setPlaceholderText("Filter bookmarks...")
        self.srch.setFixedHeight(38); self.srch.textChanged.connect(self._filter)
        self.coll_cb=QComboBox(); self.coll_cb.setFixedHeight(40); self.coll_cb.setFixedWidth(150)
        self.coll_cb.currentTextChanged.connect(self._load)
        ref=QPushButton("Refresh"); ref.setObjectName("btn_secondary"); ref.setFixedSize(78,38)
        ref.clicked.connect(self._load)
        del_=QPushButton("Delete"); del_.setObjectName("btn_danger"); del_.setFixedHeight(38)
        del_.clicked.connect(self._delete)
        exp=QPushButton("Export CSV"); exp.setObjectName("btn_secondary"); exp.setFixedHeight(38)
        exp.clicked.connect(self._export)
        top.addWidget(QLabel("Collection:",styleSheet=f"color:{C['t2']};font-size:12px;"))
        top.addWidget(self.coll_cb)
        top.addWidget(self.srch,1)
        top.addWidget(ref); top.addWidget(del_); top.addWidget(exp)
        lay.addLayout(top)

        self.table=make_table(["Title","Category","Score","Collection","Saved"],stretch_col=0)
        lay.addWidget(self.table)

        # Note editor
        nc=card(); nl=QHBoxLayout(nc); nl.setContentsMargins(16,12,16,12); nl.setSpacing(10)
        nl.addWidget(QLabel("Note:",styleSheet=f"color:{C['t2']};font-size:12px;"))
        self.note_e=QLineEdit(); self.note_e.setFixedHeight(40)
        self.note_e.setPlaceholderText("Add/edit note for selected paper...")
        sn=QPushButton("Save Note"); sn.setObjectName("btn_secondary"); sn.setFixedHeight(36)
        sn.clicked.connect(self._save_note)
        nl.addWidget(self.note_e,1); nl.addWidget(sn)
        lay.addWidget(nc)
        self._load()

    def _load(self,_=None):
        colls=get_collections(self.user['id'])
        self.coll_cb.blockSignals(True)
        self.coll_cb.clear(); self.coll_cb.addItem("All"); self.coll_cb.addItems(colls)
        self.coll_cb.blockSignals(False)
        coll=self.coll_cb.currentText()
        self._bms=get_bookmarks(self.user['id'],None if coll=="All" else coll)
        self._show(self._bms)

    def _show(self,bms):
        self.table.setRowCount(len(bms))
        for i,b in enumerate(bms):
            self.table.setItem(i,0,QTableWidgetItem(b['title']))
            ci=QTableWidgetItem(b['categories']); ci.setForeground(QColor(C['purp3']))
            self.table.setItem(i,1,ci)
            si=QTableWidgetItem(f"{b['score']:.3f}"); si.setForeground(QColor(C['grn2']))
            self.table.setItem(i,2,si)
            self.table.setItem(i,3,QTableWidgetItem(b.get('collection','Default')))
            self.table.setItem(i,4,QTableWidgetItem(b['ts'][:10]))

    def _filter(self,text):
        f=[b for b in self._bms if text.lower() in b['title'].lower()
           or text.lower() in b['categories'].lower()]
        self._show(f)

    def _delete(self):
        row=self.table.currentRow()
        if 0<=row<len(self._bms):
            delete_bookmark(self.user['id'],self._bms[row]['id']); self._load()

    def _save_note(self):
        row=self.table.currentRow()
        if 0<=row<len(self._bms):
            update_bookmark_note(self.user['id'],self._bms[row]['id'],self.note_e.text())
            QMessageBox.information(self,"Saved","Note saved!")

    def _export(self):
        path,_=QFileDialog.getSaveFileName(self,"Export","bookmarks.csv","CSV (*.csv)")
        if path:
            with open(path,'w',newline='',encoding='utf-8') as f:
                w=csv.DictWriter(f,["title","categories","score","collection","abstract","note","ts"])
                w.writeheader(); w.writerows(self._bms)
            QMessageBox.information(self,"Done",f"Saved:\n{path}")


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  READING LIST PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class ReadingListPage(QWidget):
    def __init__(self,user):
        super().__init__(); self.user=user; self._items=[]; self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(28,20,28,20); lay.setSpacing(14)
        lay.addWidget(page_header("Reading List","Track reading progress | Unread | In Progress | Done"))

        items=get_reading_list(self.user['id'])
        unread=sum(1 for x in items if x['status']=='unread')
        reading=sum(1 for x in items if x['status']=='reading')
        done=sum(1 for x in items if x['status']=='done')
        sr=QHBoxLayout(); sr.setSpacing(12)
        for v,l,c,ic in [(unread,"Unread",C['red'],"U"),
                          (reading,"In Progress",C['yellow'],"R"),
                          (done,"Completed",C['green'],"D")]:
            sr.addWidget(stat_card(v,l,c,ic))
        lay.addLayout(sr)

        top=QHBoxLayout()
        ref=QPushButton("Refresh"); ref.setObjectName("btn_secondary"); ref.setFixedHeight(36)
        ref.clicked.connect(self._load)
        top.addStretch(); top.addWidget(ref)
        lay.addLayout(top)

        self.table=make_table(["Title","Status","Added","Update Status"],stretch_col=0)
        lay.addWidget(self.table)
        self._load()

    def _load(self):
        self._items=get_reading_list(self.user['id'])
        self.table.setRowCount(len(self._items))
        colors={'unread':C['red2'],'reading':C['yel2'],'done':C['grn2']}
        for i,r in enumerate(self._items):
            self.table.setItem(i,0,QTableWidgetItem(r['title']))
            si=QTableWidgetItem(r['status'].capitalize())
            si.setForeground(QColor(colors.get(r['status'],C['t2'])))
            self.table.setItem(i,1,si)
            self.table.setItem(i,2,QTableWidgetItem(r['ts'][:10]))
            cb=QComboBox(); cb.addItems(["unread","reading","done"])
            cb.setCurrentText(r['status']); cb.setFixedHeight(30)
            cb.currentTextChanged.connect(partial(update_reading_status,self.user['id'],r['paper_id']))
            self.table.setCellWidget(i,3,cb)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  SCREEN PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class ScreenPage(QWidget):
    def __init__(self,user,settings):
        super().__init__(); self.user=user; self.settings=settings
        self._papers=[]; self._scores=[]; self._worker=None; self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(28,20,28,20); lay.setSpacing(14)
        lay.addWidget(page_header("Literature Screening - LitRev-AI",
            "PubMedBERT classifier | Keyword heuristic fallback | Include/Exclude with PRISMA export"))

        cc=card(); cl=QVBoxLayout(cc); cl.setContentsMargins(20,16,20,16); cl.setSpacing(12)
        tr=QHBoxLayout(); tr.setSpacing(10)
        lb=QPushButton("Load Papers CSV"); lb.setFixedHeight(40); lb.clicked.connect(self._load_csv)
        self.sess_name=QLineEdit(); self.sess_name.setPlaceholderText("Session name...")
        self.sess_name.setFixedHeight(40); self.sess_name.setFixedWidth(200)
        tr.addWidget(lb); tr.addWidget(self.sess_name); tr.addStretch()

        thr_r=QHBoxLayout(); thr_r.setSpacing(10)
        thr_r.addWidget(QLabel("Threshold:",styleSheet=f"color:{C['t2']};font-size:12px;"))
        self.thr=QDoubleSpinBox(); self.thr.setRange(0,1); self.thr.setSingleStep(0.05)
        self.thr.setDecimals(2); self.thr.setValue(float(self.settings.value("thr",0.5)))
        self.thr.setFixedWidth(90); self.thr.setFixedHeight(38)
        self.thr.valueChanged.connect(self._refresh)
        self.slider=QSlider(Qt.Horizontal); self.slider.setRange(0,100)
        self.slider.setValue(int(self.thr.value()*100)); self.slider.setFixedWidth(220)
        self.slider.valueChanged.connect(lambda v:self.thr.setValue(v/100))
        self.thr.valueChanged.connect(lambda v:self.slider.setValue(int(v*100)))
        thr_r.addWidget(self.thr); thr_r.addWidget(self.slider); thr_r.addStretch()
        cl.addLayout(tr); cl.addLayout(thr_r)
        lay.addWidget(cc)

        self.pbar=QProgressBar(); self.pbar.setRange(0,100); self.pbar.setFixedHeight(6)
        self.pbar.setVisible(False); lay.addWidget(self.pbar)

        self.table=make_table(["OK","#","Title","Score","Decision"],stretch_col=2)
        lay.addWidget(self.table)

        sc=card(); sl=QHBoxLayout(sc); sl.setContentsMargins(16,10,16,10); sl.setSpacing(28)
        self.stat_lbs={}
        for k,lb2 in [("total","Total"),("inc","Included"),("exc","Excluded"),("saved","Work Saved")]:
            col=QVBoxLayout()
            v=QLabel("-"); v.setStyleSheet(f"font-size:22px;font-weight:800;color:{C['t0']};background:transparent;")
            ll2=QLabel(lb2.upper())
            ll2.setStyleSheet(f"font-size:10px;color:{C['t3']};font-weight:700;letter-spacing:0.8px;background:transparent;")
            col.addWidget(v); col.addWidget(ll2); sl.addLayout(col); self.stat_lbs[k]=v
        sl.addStretch()
        lay.addWidget(sc)

        br=QHBoxLayout(); br.setSpacing(10)
        self.run_btn=QPushButton("Run Screening"); self.run_btn.setEnabled(False)
        self.run_btn.clicked.connect(self._run)
        self.save_btn=QPushButton("Save Session"); self.save_btn.setObjectName("btn_secondary")
        self.save_btn.setEnabled(False); self.save_btn.clicked.connect(self._save)
        self.exp_btn=QPushButton("Export CSV"); self.exp_btn.setObjectName("btn_secondary")
        self.exp_btn.setEnabled(False); self.exp_btn.clicked.connect(self._export)
        hist=QPushButton("Sessions"); hist.setObjectName("btn_secondary")
        hist.clicked.connect(self._sessions)
        clr=QPushButton("Clear All"); clr.setObjectName("btn_danger"); clr.clicked.connect(self._clear)
        for w in [self.run_btn,self.save_btn,self.exp_btn,hist,clr]: br.addWidget(w)
        br.addStretch(); lay.addLayout(br)

    def _populate(self):
        thr=self.thr.value(); self.table.setRowCount(len(self._papers))
        for i,p in enumerate(self._papers):
            chk=QCheckBox(); chk.setChecked(True)
            cw=QWidget(); cwl=QHBoxLayout(cw); cwl.addWidget(chk)
            cwl.setAlignment(Qt.AlignCenter); cwl.setContentsMargins(0,0,0,0)
            self.table.setCellWidget(i,0,cw)
            self.table.setItem(i,1,QTableWidgetItem(str(i+1)))
            t=p["TITLE"]; t=t[:70]+"..." if len(t)>70 else t
            self.table.setItem(i,2,QTableWidgetItem(t))
            if self._scores:
                sc=self._scores[i]
                si=QTableWidgetItem(f"{sc:.3f}"); si.setTextAlignment(Qt.AlignCenter)
                si.setForeground(QColor(C['grn2'] if sc>=thr else C['red2']))
                self.table.setItem(i,3,si)
                dec="Include" if sc>=thr else "Exclude"
                di=QTableWidgetItem(dec)
                di.setForeground(QColor(C['grn2'] if sc>=thr else C['red2']))
                self.table.setItem(i,4,di)
            else:
                self.table.setItem(i,3,QTableWidgetItem("-"))
                self.table.setItem(i,4,QTableWidgetItem("Pending..."))

    def _update_stats(self):
        thr=self.thr.value(); tot=len(self._papers)
        inc=sum(1 for s in self._scores if s>=thr); exc=tot-inc
        ws=f"{exc/tot*100:.0f}%" if tot else "-"
        colors={"total":C['t0'],"inc":C['grn2'],"exc":C['red2'],"saved":C['yel2']}
        for k,v in [("total",str(tot)),("inc",str(inc)),("exc",str(exc)),("saved",ws)]:
            self.stat_lbs[k].setText(v)
            self.stat_lbs[k].setStyleSheet(
                f"font-size:22px;font-weight:800;color:{colors[k]};background:transparent;")

    def _refresh(self):
        self.settings.setValue("thr",self.thr.value())
        if self._scores: self._populate(); self._update_stats()

    def _load_csv(self):
        path,_=QFileDialog.getOpenFileName(self,"Load CSV","","CSV (*.csv)")
        if not path: return
        try:
            import pandas as pd; df=pd.read_csv(path)
            df.columns=[c.strip().upper() for c in df.columns]
            for col in ("TITLE","ABSTRACT"):
                if col not in df.columns:
                    QMessageBox.critical(self,"Invalid CSV",
                        f"Missing column: {col}\nFound: {list(df.columns)}\n\n"
                        "CSV must have TITLE and ABSTRACT columns."); return
            self._papers=df[["TITLE","ABSTRACT"]].fillna("").to_dict("records")
            self._scores=[]
            self._populate()
            # Disable export/save until screening completes
            self.exp_btn.setEnabled(False); self.save_btn.setEnabled(False)
            self.sess_name.setText(os.path.basename(path).replace(".csv",""))
            self.stat_lbs["total"].setText(str(len(self._papers)))
            # If backend models are loaded, run screening immediately; otherwise enable Run button
            if backend.loaded:
                QTimer.singleShot(100, self._run)
            else:
                self.run_btn.setEnabled(True)
        except Exception as e:
            QMessageBox.critical(self,"Error",str(e))

    def _run(self):
        if not backend.loaded:
            QMessageBox.warning(self,"Not Ready","Models still loading..."); return
        self.run_btn.setEnabled(False); self.pbar.setVisible(True); self.pbar.setValue(0)
        texts=[f"{p['TITLE']} [SEP] {p['ABSTRACT']}" for p in self._papers]
        self._worker=ScreenWorker(texts)
        self._worker.progress.connect(lambda d,t:self.pbar.setValue(int(d/t*100)))
        self._worker.done.connect(self._screen_done)
        self._worker.err.connect(lambda m:(
            self.pbar.setVisible(False),self.run_btn.setEnabled(True),
            QMessageBox.critical(self,"Error",m[:400])))
        self._worker.start()

    def _screen_done(self,scores):
        self._scores=scores; self.pbar.setVisible(False)
        self.run_btn.setEnabled(True); self.exp_btn.setEnabled(True); self.save_btn.setEnabled(True)
        self._populate(); self._update_stats()
        notify(self.user['id'],f"Screening done: {len(self._papers)} papers analyzed","success")

    def _save(self):
        thr=self.thr.value(); tot=len(self._papers)
        inc=sum(1 for s in self._scores if s>=thr); exc=tot-inc
        results=[{"title":p["TITLE"],"score":s,"decision":"Include" if s>=thr else "Exclude"}
                 for p,s in zip(self._papers,self._scores)]
        name=self.sess_name.text() or f"Session {datetime.now():%Y-%m-%d %H:%M}"
        save_screening(self.user['id'],name,tot,inc,exc,thr,results)
        QMessageBox.information(self,"Saved",f"Session '{name}' saved!")

    def _export(self):
        if not self._papers or not self._scores: return
        path,_=QFileDialog.getSaveFileName(self,"Export","screening_results.csv","CSV (*.csv)")
        if not path: return
        thr=self.thr.value()
        rows=[{"TITLE":p["TITLE"],"ABSTRACT":p["ABSTRACT"],"SCORE":round(s,4),
               "DECISION":"Include" if s>=thr else "Exclude"}
              for p,s in zip(self._papers,self._scores)]
        with open(path,'w',newline='',encoding='utf-8') as f:
            w=csv.DictWriter(f,["TITLE","ABSTRACT","SCORE","DECISION"])
            w.writeheader(); w.writerows(rows)
        QMessageBox.information(self,"Exported",f"Saved:\n{path}")

    def _sessions(self):
        dlg=QDialog(self); dlg.setWindowTitle("Screening Sessions"); dlg.resize(700,400)
        lay=QVBoxLayout(dlg)
        tbl=make_table(["Name","Total","Included","Excluded","Threshold","Date"],stretch_col=0)
        sessions=get_screenings(self.user['id']); tbl.setRowCount(len(sessions))
        for i,s in enumerate(sessions):
            for j,k in enumerate(["name","total","included","excluded","threshold","ts"]):
                tbl.setItem(i,j,QTableWidgetItem(str(s[k])[:10] if k=="ts" else str(s[k])))
        lay.addWidget(tbl); dlg.exec_()

    def _clear(self):
        self._papers=[]; self._scores=[]; self.table.setRowCount(0)
        self.run_btn.setEnabled(False); self.exp_btn.setEnabled(False); self.save_btn.setEnabled(False)
        for k in self.stat_lbs: self.stat_lbs[k].setText("-")


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  PRISMA PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class PrismaPage(QWidget):
    def __init__(self): super().__init__(); self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(28,20,28,20); lay.setSpacing(14)
        lay.addWidget(page_header("PRISMA 2020 Flow Diagram",
            "Publication-ready | 6 color styles | PNG + PDF export | Custom title & DPI"))

        sp2=QSplitter(Qt.Horizontal); sp2.setHandleWidth(8)
        lw=QWidget(); ll2=QVBoxLayout(lw); ll2.setContentsMargins(0,0,14,0); ll2.setSpacing(12)

        in_card=card(); il=QFormLayout(in_card); il.setContentsMargins(20,18,20,18); il.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter); il.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow); il.setSpacing(14)
        def mk(default):
            s=QSpinBox(); s.setRange(0,1_000_000); s.setValue(default); s.setFixedHeight(40); return s
        self.sp_id=mk(1000); self.sp_dd=mk(800); self.sp_sc=mk(500)
        self.sp_ft=mk(150); self.sp_in=mk(50)
        il.addRow("Records identified:",self.sp_id)
        il.addRow("After deduplication:",self.sp_dd)
        il.addRow("Records screened:",self.sp_sc)
        il.addRow("Full-text assessed:",self.sp_ft)
        il.addRow("Studies included:",self.sp_in)
        ll2.addWidget(in_card)

        opt=card(); ol=QFormLayout(opt); ol.setContentsMargins(20,16,20,16); ol.setSpacing(10)
        self.title_inp=QLineEdit("PRISMA 2020 Flow Diagram"); self.title_inp.setFixedHeight(40)
        self.style_cb=QComboBox(); self.style_cb.setFixedHeight(40)
        self.style_cb.addItems(["Neon Matrix","Lime Glow","Volt Stream",
                                 "Carbon Pulse","Midnight Flux","Circuit Noir"])
        self.dpi_sp=QSpinBox(); self.dpi_sp.setRange(72,300); self.dpi_sp.setValue(150)
        self.dpi_sp.setFixedHeight(40)
        ol.addRow("Title:",self.title_inp); ol.addRow("Style:",self.style_cb)
        ol.addRow("DPI:",self.dpi_sp)
        ll2.addWidget(opt)

        gen=QPushButton("Generate PRISMA Diagram"); gen.setFixedHeight(48)
        gen.clicked.connect(self._gen)
        self.gl=QLabel(""); self.gl.setObjectName("ok"); self.gl.setWordWrap(True)
        ll2.addWidget(gen); ll2.addWidget(self.gl); ll2.addStretch()

        rw=QWidget(); rl2=QVBoxLayout(rw); rl2.setContentsMargins(0,0,0,0); rl2.setSpacing(8)
        rl2.addWidget(QLabel("Preview",styleSheet=f"font-size:13px;font-weight:700;color:{C['t0']};"))
        self.preview=QLabel("Diagram preview will appear here after generation.")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setStyleSheet(
            f"background:{C['bg3']};border:1.5px solid {C['border']};border-radius:12px;"
            f"color:{C['t3']};padding:20px;")
        self.preview.setMinimumSize(530,460)
        rl2.addWidget(self.preview,1)

        sp2.addWidget(lw); sp2.addWidget(rw)
        sp2.setStretchFactor(0,0); sp2.setStretchFactor(1,1)
        lay.addWidget(sp2)

    def _gen(self):
        try:
            import matplotlib; matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            from matplotlib.patches import FancyBboxPatch
            styles={
                "Neon Matrix":("#000000","#f97316","#050505","#f97316","#000000"),
                "Lime Glow":("#050505","#f97316","#090909","#f97316","#000000"),
                "Volt Stream":("#080808","#f97316","#101010","#f97316","#000000"),
                "Carbon Pulse":("#000000","#f97316","#121212","#f97316","#000000"),
                "Midnight Flux":("#020202","#f97316","#0b0b0b","#f97316","#000000"),
                "Circuit Noir":("#090909","#f97316","#111111","#f97316","#000000"),
            }
            bf,be,ef,ee,bg=styles.get(self.style_cb.currentText(),styles["Neon Matrix"])
            ident=self.sp_id.value(); dedup=self.sp_dd.value()
            sc=self.sp_sc.value(); ft=self.sp_ft.value(); incl=self.sp_in.value()

            fig,ax=plt.subplots(figsize=(11,14))
            fig.patch.set_facecolor(bg); ax.set_xlim(0,10); ax.set_ylim(0,15.5); ax.axis("off")
            ax.text(5,15.0,self.title_inp.text(),ha="center",va="center",
                fontsize=17,fontweight="bold",color=be,fontfamily="DejaVu Sans",zorder=5)

            def box(x,y,w,h,text,fc,ec,fs=11,bold=False):
                p=FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.15",
                    facecolor=fc,edgecolor=ec,linewidth=2.2,zorder=3)
                ax.add_patch(p)
                tc=be if fc not in (ef,) else ee
                ax.text(x,y,text,ha="center",va="center",fontsize=fs,color=tc,
                    zorder=4,multialignment="center",fontfamily="DejaVu Sans",
                    fontweight="bold" if bold else "normal")

            def arrow(x1,y1,x2,y2):
                ax.annotate("",xy=(x2,y2),xytext=(x1,y1),
                    arrowprops=dict(arrowstyle="-|>",color="#f97316",lw=2.0,mutation_scale=20),zorder=2)

            cx=3.8; ys=[13.2,11.0,8.8,6.6,4.4]
            labs=[f"Records identified\n(n = {ident:,})",
                  f"Records after removing duplicates\n(n = {dedup:,})",
                  f"Records screened\n(n = {sc:,})",
                  f"Full-text articles assessed\n(n = {ft:,})",
                  f"Studies included in synthesis\n(n = {incl:,})"]
            for y,lb2,bold in zip(ys,labs,[False]*4+[True]):
                box(cx,y,5.6,1.8,lb2,bf,be,bold=bold)
            for i in range(len(ys)-1):
                arrow(cx,ys[i]-0.9,cx,ys[i+1]+0.9)
            ex=8.7
            for ey,et in [(11.0,f"Duplicates removed\n(n = {ident-dedup:,})"),
                          (8.8,f"Records excluded\n(n = {dedup-sc:,})"),
                          (6.6,f"Full-text excluded\n(n = {sc-ft:,})")]:
                box(ex,ey,4.2,1.6,et,ef,ee,fs=10)
                arrow(cx+2.8,ey,ex-2.1,ey)

            plt.tight_layout(pad=0.3)
            os.makedirs(OUTPUT_DIR,exist_ok=True)
            png=os.path.join(OUTPUT_DIR,"prisma_diagram.png")
            pdf=os.path.join(OUTPUT_DIR,"prisma_diagram.pdf")
            fig.savefig(png,dpi=self.dpi_sp.value(),bbox_inches="tight",facecolor=bg)
            fig.savefig(pdf,bbox_inches="tight",facecolor=bg)
            plt.close(fig)
            pix=QPixmap(png).scaled(self.preview.width()-10,self.preview.height()-10,
                Qt.KeepAspectRatio,Qt.SmoothTransformation)
            self.preview.setPixmap(pix)
            self.gl.setText(f"Saved:\n- {png}\n- {pdf}")
        except Exception:
            QMessageBox.critical(self,"Error",traceback.format_exc()[:600])


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  BILLING PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class BillingPage(QWidget):
    plan_changed=pyqtSignal()
    def __init__(self,user):
        super().__init__(); self.user=user; self._build()

    def _build(self):
        inner=QWidget(); lay=QVBoxLayout(inner)
        lay.setContentsMargins(28,24,28,24); lay.setSpacing(22)
        lay.addWidget(page_header("Billing & Subscription","Plans | Payments | Invoices | Promo codes | Research credits"))

        # Current plan
        pc=card("card_glow"); pl=QHBoxLayout(pc); pl.setContentsMargins(26,22,26,22); pl.setSpacing(18)
        left=QVBoxLayout(); left.setSpacing(10)
        left.addWidget(QLabel(f"Current: {self.user['plan'].capitalize()} Plan",
            styleSheet=f"font-size:20px;font-weight:800;color:{C['t0']};background:transparent;"))
        limits={"free":"10 credits | Basic search and review tools",
                "pro":"500 credits | Advanced AI workflows | Exports | API access",
                "university":"Unlimited credits | Teams | Governance | Priority support"}
        left.addWidget(QLabel(limits.get(self.user['plan'],''),
            styleSheet=f"font-size:13px;color:{C['t2']};background:transparent;"))
        left.addWidget(badge(self.user['plan']))
        self.payment_mode_label=QLabel(
            "Live Stripe payments enabled" if stripe else
            "Demo payment flow enabled - set STRIPE_SECRET_KEY for live checkout.")
        self.payment_mode_label.setStyleSheet(
            f"font-size:12px;color:{C['grn2'] if stripe else C['t3']};background:transparent;")
        left.addWidget(self.payment_mode_label)
        pl.addLayout(left,1); pl.addStretch()
        steps=QHBoxLayout(); steps.setSpacing(10)
        for n,title,sub in [("1","Choose","Select the right plan"),
                            ("2","Confirm","Review secure checkout"),
                            ("3","Activate","Credits update instantly")]:
            sw=QFrame(); sw.setObjectName("card"); sl=QVBoxLayout(sw)
            sl.setContentsMargins(14,12,14,12); sl.setSpacing(4)
            num=QLabel(n); num.setAlignment(Qt.AlignCenter); num.setFixedSize(28,28)
            num.setStyleSheet(f"background:{C['purple']};color:{C['bg0']};border-radius:14px;font-weight:900;")
            sl.addWidget(num)
            sl.addWidget(QLabel(title,styleSheet=f"font-size:13px;font-weight:800;color:{C['t0']};background:transparent;"))
            sl.addWidget(QLabel(sub,styleSheet=f"font-size:11px;color:{C['t3']};background:transparent;"))
            steps.addWidget(sw)
        pl.addLayout(steps,2)
        lay.addWidget(pc)

        # Plans
        lay.addWidget(QLabel("Available Plans",
            styleSheet=f"font-size:17px;font-weight:700;color:{C['t0']};"))
        pr=QHBoxLayout(); pr.setSpacing(14)
        plans=[
            ("Free","$0","/month","free",C['blue'],"Starter",
             ["10 credits/month","Semantic search","Basic summaries","Bookmarks",
              "Reading list","PRISMA generator","Basic analysis","Community support"]),
            ("Pro","$9.99","/month","pro",C['purple'],"Most Popular",
             ["500 credits/month","Full BART summarizer","Literature screening",
              "BibTeX+RIS+EndNote export","AI Research Assistant","API access",
              "Research Workspace","Citation formatter","Research gap finder",
              "Related-work generator","Trend analytics","Priority support"]),
            ("University","Custom","/year","university",C['green'],"Best Value",
             ["Unlimited credits","Everything in Pro",
              "Team workspaces","Admin dashboard",
              "Bulk paper screening","Custom integrations","SLA guarantee",
              "Dedicated support","Invoice billing","Department reporting"]),
        ]
        for pname,price,period,pkey,color,badge_txt,feats in plans:
            fc=card("card")
            fc.setMinimumHeight(520)
            fc.setMinimumWidth(300)
            fl2=QVBoxLayout(fc); fl2.setContentsMargins(22,20,22,20); fl2.setSpacing(10)
            bt=QLabel(f"  {badge_txt}  ")
            bt.setFixedHeight(20)
            bt.setStyleSheet(f"background:{color};color:{C['bg0']};border-radius:8px;"
                             f"padding:2px 10px;font-size:10.5px;font-weight:800;")
            bt.setAlignment(Qt.AlignCenter); fl2.addWidget(bt)
            fl2.addWidget(QLabel(pname,
                styleSheet=f"font-size:17px;font-weight:800;color:{C['t0']};background:transparent;"))
            pr_row=QHBoxLayout()
            pr_row.addWidget(QLabel(price,
                styleSheet=f"font-size:26px;font-weight:800;color:{C['t0']};background:transparent;"))
            pr_row.addWidget(QLabel(period,
                styleSheet=f"font-size:13px;color:{C['t2']};padding-top:10px;background:transparent;"))
            pr_row.addStretch(); fl2.addLayout(pr_row)
            fl2.addWidget(hline())
            for feat in feats:
                row=QHBoxLayout(); row.setSpacing(9)
                ok=QLabel("OK"); ok.setFixedWidth(24)
                ok.setStyleSheet(f"color:{color};font-weight:900;background:transparent;font-size:10.5px;")
                text=QLabel(feat); text.setWordWrap(True)
                text.setStyleSheet(f"font-size:12.5px;color:{C['t2']};background:transparent;")
                row.addWidget(ok); row.addWidget(text,1)
                fl2.addLayout(row)
            fl2.addStretch()
            if pkey==self.user['plan']:
                btn=QPushButton("Current Plan")
                btn.setObjectName("btn_secondary")
                btn.setEnabled(False)
                btn.setFixedHeight(48)
                fl2.addWidget(btn)
            elif pkey=="university":
                btn=QPushButton("Contact Sales"); btn.setObjectName("btn_secondary")
                btn.setFixedHeight(48)
                btn.clicked.connect(lambda:QMessageBox.information(self,"Contact",
                    "Email: sales@resora.ai\nFor university licensing and team plans."))
                fl2.addWidget(btn)
            elif pkey=="free":
                btn=QPushButton("Starter Plan")
                btn.setObjectName("btn_secondary")
                btn.setEnabled(False)
                btn.setFixedHeight(48)
                fl2.addWidget(btn)
            else:
                try: amt=float(price.replace("$",""))
                except: amt=9.99
                btn=QPushButton(f"Upgrade to {pname}")
                btn.setFixedHeight(48)
                btn.clicked.connect(partial(self._upgrade,pkey,amt))
                fl2.addWidget(btn)
            pr.addWidget(fc,1)
        lay.addLayout(pr)

        # Promo code
        prc=card(); prl=QHBoxLayout(prc); prl.setContentsMargins(18,14,18,14); prl.setSpacing(10)
        prl.addWidget(QLabel("Promo Code",styleSheet=f"color:{C['t0']};font-size:13px;font-weight:800;"))
        self.promo=QLineEdit(); self.promo.setFixedWidth(200); self.promo.setFixedHeight(38)
        self.promo.setPlaceholderText("e.g. RESORA2026")
        ab=QPushButton("Apply"); ab.setObjectName("btn_secondary"); ab.setFixedHeight(38)
        ab.clicked.connect(self._promo)
        self.pmsg=QLabel("")
        prl.addWidget(self.promo); prl.addWidget(ab); prl.addWidget(self.pmsg); prl.addStretch()
        lay.addWidget(prc)

        solve=card(); sol=QVBoxLayout(solve); sol.setContentsMargins(20,16,20,16); sol.setSpacing(12)
        sol.addWidget(QLabel("What Pro Unlocks For Researchers",
            styleSheet=f"font-size:16px;font-weight:800;color:{C['t0']};background:transparent;"))
        sg=QGridLayout(); sg.setSpacing(10)
        unlocks=[
            ("Systematic review","Screen papers, build PRISMA flow, keep decisions auditable."),
            ("Literature synthesis","Summaries, related work drafts, comparison-ready insights."),
            ("Academic writing","Research gaps, hypotheses, citation formatting, export tools."),
            ("Team productivity","Shared workspaces, admin view, invoices, support workflow."),
        ]
        for i,(title,desc) in enumerate(unlocks):
            box=QFrame(); box.setObjectName("feature_card"); bl=QVBoxLayout(box)
            bl.setContentsMargins(14,12,14,12); bl.setSpacing(5)
            bl.addWidget(QLabel(title,styleSheet=f"font-size:13px;font-weight:800;color:{C['purp2']};background:transparent;"))
            tx=QLabel(desc); tx.setWordWrap(True)
            tx.setStyleSheet(f"font-size:12px;color:{C['t2']};background:transparent;")
            bl.addWidget(tx)
            sg.addWidget(box,i//2,i%2)
        sol.addLayout(sg)
        lay.addWidget(solve)

        matrix=card(); ml=QVBoxLayout(matrix); ml.setContentsMargins(20,16,20,16); ml.setSpacing(12)
        ml.addWidget(QLabel("500+ Feature Coverage Map",
            styleSheet=f"font-size:16px;font-weight:800;color:{C['t0']};background:transparent;"))
        coverage=[
            ("Discovery", "semantic search, filters, similar papers, previews, history, bookmarks"),
            ("Analysis", "methods, contributions, limitations, reproducibility, keywords, hypotheses"),
            ("Screening", "CSV import, include/exclude decisions, thresholds, sessions, PRISMA counts"),
            ("Writing", "summaries, research gaps, related work, citation styles, export formats"),
            ("Operations", "workspaces, tasks, reading list, admin, invoices, payments, promo codes"),
            ("Support", "notifications, support tickets, audit logs, API access, team licensing"),
        ]
        mg=QGridLayout(); mg.setSpacing(10)
        for i,(name,desc) in enumerate(coverage):
            box=QFrame(); box.setObjectName("feature_card"); bl=QVBoxLayout(box)
            bl.setContentsMargins(14,12,14,12); bl.setSpacing(5)
            bl.addWidget(QLabel(name,styleSheet=f"font-size:13px;font-weight:900;color:{C['purp2']};background:transparent;"))
            t=QLabel(desc); t.setWordWrap(True)
            t.setStyleSheet(f"font-size:11.5px;color:{C['t2']};background:transparent;")
            bl.addWidget(t)
            mg.addWidget(box,i//3,i%3)
        ml.addLayout(mg)
        lay.addWidget(matrix)

        # Payment history
        lay.addWidget(QLabel("Payment History",
            styleSheet=f"font-size:17px;font-weight:700;color:{C['t0']};"))
        self.pay_tbl=make_table(["Invoice","Plan","Amount","Status","Date"])
        pays=get_payments(self.user['id']); self.pay_tbl.setRowCount(max(len(pays),1))
        if pays:
            for i,p in enumerate(pays):
                self.pay_tbl.setItem(i,0,QTableWidgetItem(p['invoice_no']))
                self.pay_tbl.setItem(i,1,QTableWidgetItem(p['plan'].capitalize()))
                self.pay_tbl.setItem(i,2,QTableWidgetItem(f"${p['amount']:.2f}"))
                si=QTableWidgetItem(p['status'].capitalize())
                si.setForeground(QColor(C['grn2'] if p['status']=='success' else C['red2']))
                self.pay_tbl.setItem(i,3,si)
                self.pay_tbl.setItem(i,4,QTableWidgetItem(p['ts'][:10]))
        else:
            self.pay_tbl.setItem(0,0,QTableWidgetItem("No payments yet"))
        self.pay_tbl.setFixedHeight(180); lay.addWidget(self.pay_tbl)
        inv_btn=QPushButton("Download Latest Invoice PDF")
        inv_btn.setObjectName("btn_secondary"); inv_btn.clicked.connect(self._invoice)
        self.refresh_btn=QPushButton("Refresh Payment Status")
        self.refresh_btn.setObjectName("btn_small"); self.refresh_btn.clicked.connect(self._refresh_payments)
        row=QHBoxLayout(); row.addWidget(inv_btn); row.addWidget(self.refresh_btn); row.addStretch()
        lay.addLayout(row); lay.addStretch()
        out=QVBoxLayout(self); out.setContentsMargins(16,16,16,16); out.setSpacing(12); out.addWidget(scrolled(inner))

    def _upgrade(self,plan,amount):
        if stripe:
            self._start_stripe_checkout(plan,amount); return
        dlg=QDialog(self); dlg.setWindowTitle("Upgrade Plan"); dlg.setFixedSize(420,290)
        lay=QVBoxLayout(dlg); lay.setContentsMargins(32,28,32,28); lay.setSpacing(14)
        lay.addWidget(QLabel(f"Upgrade to {plan.capitalize()}",
            styleSheet=f"font-size:18px;font-weight:700;color:{C['t0']};"))
        lay.addWidget(QLabel(f"${amount:.2f}/month",
            styleSheet=f"font-size:28px;font-weight:800;color:{C['purp2']};"))
        lay.addWidget(QLabel(
            "Demo environment - payment is simulated.\nIn production, Stripe checkout is available when STRIPE_SECRET_KEY is set.",
            styleSheet=f"font-size:11px;color:{C['t3']};background:transparent;",wordWrap=True))
        lay.addWidget(hline())
        lay.addWidget(QLabel("Dummy card: 4242 4242 4242 4242 | 12/34 | CVC 123",
            styleSheet=f"font-size:12px;color:{C['t2']};background:transparent;"))
        br=QHBoxLayout()
        cancel=QPushButton("Cancel"); cancel.setObjectName("btn_secondary"); cancel.clicked.connect(dlg.reject)
        confirm=QPushButton("Confirm & Pay"); confirm.clicked.connect(dlg.accept)
        br.addWidget(cancel); br.addWidget(confirm); lay.addLayout(br)
        if dlg.exec_()==QDialog.Accepted:
            inv=add_payment(self.user['id'],amount,plan)
            upgrade_plan(self.user['id'],plan); self.user=get_user(self.user['id'])
            notify(self.user['id'],f"Upgraded to {plan.capitalize()}! Invoice: {inv}","success")
            self.plan_changed.emit()
            QMessageBox.information(self,"Upgraded!",
                f"You're now on the {plan.capitalize()} plan!\nInvoice: {inv}")

    def _promo(self):
        code=self.promo.text().strip().upper()
        valid={"RESORA2026":"pro","TRILIT2024":"pro","RESEARCH50":"pro","UNIVERSITY2024":"university",
               "STUDENT2024":"pro","PHD2024":"pro","SCHOLAR2024":"pro"}
        if not code:
            self.pmsg.setStyleSheet(f"font-size:12px;color:{C['red2']};font-weight:700;")
            self.pmsg.setText("Enter a promo code")
            return
        if code in valid:
            plan=valid[code]; upgrade_plan(self.user['id'],plan)
            self.user=get_user(self.user['id'])
            self.pmsg.setStyleSheet(f"font-size:12px;color:{C['grn2']};font-weight:700;")
            self.pmsg.setText(f"Applied! Upgraded to {plan.capitalize()}")
            notify(self.user['id'],f"Promo code applied: {code}. Upgraded to {plan.capitalize()}.","success")
            self.plan_changed.emit()
        else:
            self.pmsg.setStyleSheet(f"font-size:12px;color:{C['red2']};font-weight:700;")
            self.pmsg.setText("Invalid code")

    def _invoice(self):
        pays=get_payments(self.user['id'])
        if not pays: QMessageBox.information(self,"None","No payments yet."); return
        p=pays[0]
        try:
            import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
            fig,ax=plt.subplots(figsize=(8,11)); ax.axis("off"); fig.patch.set_facecolor("#000000")
            ax.add_patch(plt.Rectangle((0,0.87),1,0.13,transform=ax.transAxes,color="#f97316"))
            ax.text(0.5,0.935,"Resora",transform=ax.transAxes,ha="center",
                fontsize=28,fontweight="bold",color="#000000")
            ax.text(0.5,0.893,"Research Operating System",transform=ax.transAxes,
                ha="center",fontsize=13,color="#000000")
            ax.text(0.5,0.83,"INVOICE",transform=ax.transAxes,ha="center",
                fontsize=22,fontweight="bold",color="#f97316")
            rows=[("Invoice No.",p['invoice_no']),("Date",p['ts'][:10]),
                  ("Plan",p['plan'].capitalize()),("Amount",f"${p['amount']:.2f} USD"),
                  ("Customer",self.user['name']),("Email",self.user['email'])]
            y2=0.74
            for k,v in rows:
                ax.text(0.15,y2,k,transform=ax.transAxes,fontsize=12,color="#f97316",fontweight="bold")
                ax.text(0.55,y2,v,transform=ax.transAxes,fontsize=12,color="#f97316"); y2-=0.07
            ax.text(0.5,0.08,"Thank you for using Resora!",transform=ax.transAxes,
                ha="center",fontsize=13,color="#f97316")
            path=os.path.join(OUTPUT_DIR,f"invoice_{p['invoice_no']}.pdf")
            fig.savefig(path,bbox_inches="tight"); plt.close(fig)
            QMessageBox.information(self,"Saved",f"Invoice saved:\n{path}")
        except Exception as e:
            QMessageBox.critical(self,"Error",str(e))

    def _refresh_payments(self):
        # Reload the payment history table and keep current layout
        pays=get_payments(self.user['id'])
        self.pay_tbl.setRowCount(max(len(pays),1))
        if pays:
            for i,p in enumerate(pays):
                self.pay_tbl.setItem(i,0,QTableWidgetItem(p['invoice_no']))
                self.pay_tbl.setItem(i,1,QTableWidgetItem(p['plan'].capitalize()))
                self.pay_tbl.setItem(i,2,QTableWidgetItem(f"${p['amount']:.2f}"))
                si=QTableWidgetItem(p['status'].capitalize())
                si.setForeground(QColor(C['grn2'] if p['status']=='success' else C['red2']))
                self.pay_tbl.setItem(i,3,si)
                self.pay_tbl.setItem(i,4,QTableWidgetItem(p['ts'][:10]))
            QMessageBox.information(self,"Updated","Payment history refreshed.")
        else:
            self.pay_tbl.setItem(0,0,QTableWidgetItem("No payments yet"))

    def _start_stripe_checkout(self,plan,amount):
        if not stripe:
            QMessageBox.warning(self,"Stripe Disabled","Stripe is not configured. Set STRIPE_SECRET_KEY as an environment variable.")
            return
        try:
            success_url = os.getenv('STRIPE_SUCCESS_URL','https://example.com/success')
            cancel_url = os.getenv('STRIPE_CANCEL_URL','https://example.com/cancel')
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': f'Resora {plan.capitalize()} Plan'},
                        'unit_amount': int(amount * 100),
                    },
                    'quantity': 1,
                }],
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={'user_id': str(self.user['id']), 'plan': plan},
            )
            webbrowser.open(session.url)
            QMessageBox.information(self,"Stripe Checkout",
                "A browser window has opened to Stripe Checkout. Complete the payment there, then return here to refresh your billing page.")
        except Exception as e:
            QMessageBox.critical(self,"Stripe Error",f"Payment creation failed:\n{str(e)}")


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  PROFILE PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class ProfilePage(QWidget):
    def __init__(self,user):
        super().__init__(); self.user=user; self._build()

    def _build(self):
        inner=QWidget(); lay=QVBoxLayout(inner)
        lay.setContentsMargins(28,24,28,24); lay.setSpacing(20)
        lay.addWidget(page_header("Profile & Settings","Account | API Key | Preferences | Support"))

        # Hero
        hero=card(); hl=QHBoxLayout(hero); hl.setContentsMargins(24,20,24,20); hl.setSpacing(20)
        avatar_w=av(self.user.get('initials','?'),self.user.get('avatar_color',C['t0']),72)
        info=QVBoxLayout(); info.setSpacing(6)
        info.addWidget(QLabel(self.user['name'],
            styleSheet=f"font-size:20px;font-weight:700;color:{C['t0']};background:transparent;"))
        info.addWidget(QLabel(self.user['email'],
            styleSheet=f"font-size:13px;color:{C['t2']};background:transparent;"))
        info.addWidget(badge(self.user['plan']))
        hl.addWidget(avatar_w); hl.addLayout(info); hl.addStretch()
        lay.addWidget(hero)

        # Edit profile
        lay.addWidget(lbl("Edit Profile","section"))
        ec=card(); el=QFormLayout(ec); el.setContentsMargins(20,16,20,16); el.setSpacing(14); el.setLabelAlignment(Qt.AlignRight|Qt.AlignVCenter); el.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.name_e=QLineEdit(self.user['name']); self.name_e.setFixedHeight(40)
        self.bio_e=QLineEdit(self.user.get('bio','')); self.bio_e.setFixedHeight(40)
        self.bio_e.setPlaceholderText("Short bio...")
        self.inst_e=QLineEdit(self.user.get('institution','')); self.inst_e.setFixedHeight(40)
        self.inst_e.setPlaceholderText("University / Company...")
        self.field_e=QLineEdit(self.user.get('field','')); self.field_e.setFixedHeight(40)
        self.field_e.setPlaceholderText("Research field...")
        el.addRow("Name:",self.name_e); el.addRow("Bio:",self.bio_e)
        el.addRow("Institution:",self.inst_e); el.addRow("Field:",self.field_e)
        save=QPushButton("Save Changes"); save.setFixedHeight(42); save.clicked.connect(self._save)
        el.addRow("",save); lay.addWidget(ec)

        # API Key
        lay.addWidget(lbl("API Access","section"))
        ak=card(); akl=QVBoxLayout(ak); akl.setContentsMargins(20,16,20,16); akl.setSpacing(10)
        kr=QHBoxLayout(); kr.setSpacing(8)
        self.api_lbl=QLineEdit("*"*36); self.api_lbl.setReadOnly(True); self.api_lbl.setFixedHeight(40)
        self.api_lbl.setStyleSheet(
            f"font-family:monospace;color:{C['purp3']};background:{C['bg4']};"
            f"border:1.5px solid {C['bord2']};border-radius:8px;padding:0 12px;")
        self._api_val=self.user.get('api_key','')
        self._api_visible=False
        self.api_lbl.setEchoMode(QLineEdit.Password)
        self.api_toggle_btn=QPushButton("Show"); self.api_toggle_btn.setObjectName("btn_secondary"); self.api_toggle_btn.setFixedSize(72,40)
        cp=QPushButton("Copy"); cp.setObjectName("btn_secondary"); cp.setFixedSize(72,40)
        rg=QPushButton("Regenerate"); rg.setObjectName("btn_ghost"); rg.setFixedHeight(40)
        self.api_toggle_btn.clicked.connect(self._toggle_api_key)
        cp.clicked.connect(lambda:QApplication.clipboard().setText(self._api_val))
        rg.clicked.connect(self._regen)
        kr.addWidget(self.api_lbl,1)
        kr.addWidget(self.api_toggle_btn)
        kr.addWidget(cp)
        kr.addWidget(rg)
        akl.addWidget(fl("Your API Key (keep secret)")); akl.addLayout(kr)
        akl.addWidget(QLabel("Use this key to access Resora programmatically via REST API.",
            styleSheet=f"font-size:11px;color:{C['t3']};background:transparent;"))
        lay.addWidget(ak)

        # Support ticket
        lay.addWidget(lbl("Support","section"))
        tc=card(); tl2=QVBoxLayout(tc); tl2.setContentsMargins(20,16,20,16); tl2.setSpacing(10)
        self.tsub=QLineEdit(); self.tsub.setPlaceholderText("Subject..."); self.tsub.setFixedHeight(40)
        self.tmsg=QTextEdit(); self.tmsg.setFixedHeight(90)
        self.tmsg.setPlaceholderText("Describe your issue or question...")
        send=QPushButton("Submit Support Ticket"); send.setFixedHeight(42)
        send.clicked.connect(self._ticket)
        tl2.addWidget(fl("Subject")); tl2.addWidget(self.tsub)
        tl2.addWidget(fl("Message")); tl2.addWidget(self.tmsg); tl2.addWidget(send)
        lay.addWidget(tc); lay.addStretch()
        out=QVBoxLayout(self); out.setContentsMargins(16,16,16,16); out.setSpacing(12); out.addWidget(scrolled(inner))

    def _save(self):
        name=self.name_e.text().strip()
        if not name: return
        initials="".join(w[0].upper() for w in name.split()[:2])
        update_user(self.user['id'],name=name,bio=self.bio_e.text(),
                    institution=self.inst_e.text(),field=self.field_e.text(),initials=initials)
        QMessageBox.information(self,"Saved","Profile updated!")

    def _toggle_api_key(self):
        self._api_visible = not self._api_visible
        self.api_lbl.setText(self._api_val)
        if self._api_visible:
            self.api_lbl.setEchoMode(QLineEdit.Normal)
            self.api_toggle_btn.setText("Hide")
        else:
            self.api_lbl.setEchoMode(QLineEdit.Password)
            self.api_toggle_btn.setText("Show")

    def _regen(self):
        new=secrets.token_hex(20)
        set_api_key(self.user['id'], new)
        self._api_val=new
        self.api_lbl.setText(new)
        if not self._api_visible:
            self.api_lbl.setEchoMode(QLineEdit.Password)
        self.api_toggle_btn.setText("Hide" if self._api_visible else "Show")
        QMessageBox.information(self,"Done","New API key generated!")

    def _ticket(self):
        sub=self.tsub.text().strip(); msg=self.tmsg.toPlainText().strip()
        if not sub or not msg: QMessageBox.warning(self,"Empty","Fill both fields."); return
        add_ticket(self.user['id'],sub,msg); self.tsub.clear(); self.tmsg.clear()
        QMessageBox.information(self,"Submitted","Ticket submitted! We reply within 24h.")


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  ADMIN PAGE
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class AdminPage(QWidget):
    def __init__(self,user):
        super().__init__(); self.user=user; self._build()

    def _build(self):
        lay=QVBoxLayout(self); lay.setContentsMargins(28,20,28,20); lay.setSpacing(14)
        lay.addWidget(page_header("Admin Dashboard","Users | Revenue | Tickets | Audit Logs"))

        st=get_stats()
        sr=QHBoxLayout(); sr.setSpacing(12)
        for v,l,c2,ic in [(st['total_users'],"Users",C['purple'],"U"),
                           (st['pro_users'],"Pro",C['blue'],"P"),
                           (st['uni_users'],"University",C['green'],"Uni"),
                           (f"${st['revenue']:.0f}","Revenue",C['yellow'],"$"),
                           (st['searches'],"Searches",C['teal'],"S"),
                           (st['tickets_open'],"Open Tickets",C['red'],"T")]:
            sr.addWidget(stat_card(v,l,c2,ic))
        lay.addLayout(sr)

        tabs=QTabWidget()

        # Users tab
        ut=QWidget(); ul=QVBoxLayout(ut); ul.setContentsMargins(8,8,8,8)
        utbl=make_table(["ID","Name","Email","Plan","Credits","Active","Joined"])
        users=get_all_users(); utbl.setRowCount(len(users))
        for i,u in enumerate(users):
            for j,k in enumerate(["id","name","email","plan","credits_used","is_active","created_at"]):
                v=str(u[k])[:10] if k=="created_at" else str(u[k])
                item=QTableWidgetItem(v)
                if k=="plan":
                    item.setForeground(QColor({
                        "free":C['t3'],"pro":C['purp2'],"university":C['grn2']
                    }.get(u[k],C['t1'])))
                elif k=="is_active":
                    item=QTableWidgetItem("Active" if u[k] else "Inactive")
                    item.setForeground(QColor(C['grn2'] if u[k] else C['red2']))
                utbl.setItem(i,j,item)
        utbl.setAlternatingRowColors(True); utbl.setShowGrid(False)
        tb_btn=QPushButton("Toggle Active/Inactive"); tb_btn.setObjectName("btn_secondary")
        def do_tog():
            row=utbl.currentRow()
            if 0<=row<len(users):
                toggle_user_active(users[row]['id'])
                QMessageBox.information(ut,"Done","User status toggled. Refresh to see changes.")
        tb_btn.clicked.connect(do_tog)
        ul.addWidget(utbl); ul.addWidget(tb_btn)
        tabs.addTab(ut,"Users")

        # Tickets tab
        tt=QWidget(); tl2=QVBoxLayout(tt); tl2.setContentsMargins(8,8,8,8)
        ttbl=make_table(["User","Email","Subject","Status","Date"],stretch_col=2)
        tickets=get_all_tickets(); ttbl.setRowCount(len(tickets))
        for i,t in enumerate(tickets):
            ttbl.setItem(i,0,QTableWidgetItem(t['name']))
            ttbl.setItem(i,1,QTableWidgetItem(t['email']))
            ttbl.setItem(i,2,QTableWidgetItem(t['subject']))
            si=QTableWidgetItem(t['status'].capitalize())
            si.setForeground(QColor(C['grn2'] if t['status']=='resolved' else C['yel2']))
            ttbl.setItem(i,3,si); ttbl.setItem(i,4,QTableWidgetItem(t['ts'][:10]))
        rb=QPushButton("Reply to Selected Ticket"); rb.setObjectName("btn_secondary")
        def do_reply():
            row=ttbl.currentRow()
            if 0<=row<len(tickets):
                text,ok=QInputDialog.getMultiLineText(tt,"Reply",
                    f"Reply to: {tickets[row]['subject']}")
                if ok and text:
                    reply_ticket(tickets[row]['id'],text)
                    QMessageBox.information(tt,"Done","Reply sent!")
        rb.clicked.connect(do_reply)
        tl2.addWidget(ttbl); tl2.addWidget(rb)
        tabs.addTab(tt,"Tickets")

        # Audit Logs tab
        lt=QWidget(); ll2=QVBoxLayout(lt); ll2.setContentsMargins(8,8,8,8)
        ltbl=make_table(["User","Action","Detail","Time"],stretch_col=2)
        logs=get_audit_logs(200); ltbl.setRowCount(len(logs))
        for i,lg in enumerate(logs):
            ltbl.setItem(i,0,QTableWidgetItem(lg.get('name') or 'System'))
            ltbl.setItem(i,1,QTableWidgetItem(lg['action']))
            ltbl.setItem(i,2,QTableWidgetItem(lg.get('detail','')[:60]))
            ltbl.setItem(i,3,QTableWidgetItem(lg['ts'][:16]))
        ll2.addWidget(ltbl)
        tabs.addTab(lt,"Logs")
        lay.addWidget(tabs)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  NOTIFICATION POPUP
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class NotifPopup(QDialog):
    def __init__(self,user,parent=None):
        super().__init__(parent,Qt.Popup|Qt.FramelessWindowHint)
        self.setFixedSize(430,460)
        self.setStyleSheet(f"""
            QDialog{{
                background: {C['bg2']};
                border: 1.5px solid {C['bord2']};
                border-radius: 14px;
            }}
            QWidget {{ background: {C['bg2']}; }}
        """)
        lay=QVBoxLayout(self); lay.setContentsMargins(0,0,0,0)
        hdr=QWidget()
        hdr.setStyleSheet(f"background:{C['bg3']};border-top-left-radius:14px;border-top-right-radius:14px;")
        hl=QHBoxLayout(hdr); hl.setContentsMargins(18,12,18,12); hl.setSpacing(12)
        hl.addWidget(QLabel("Notifications",
            styleSheet=f"font-weight:700;font-size:14px;color:{C['t0']};background:transparent;"))
        hl.addStretch()
        clr=QPushButton("Mark all read"); clr.setObjectName("btn_ghost"); clr.setFixedSize(126,32)
        clr.clicked.connect(lambda:(mark_read(user['id']),self.close()))
        hl.addWidget(clr); lay.addWidget(hdr)
        notifs=get_notifications(user['id'])
        colors={"info":C['blue2'],"success":C['grn2'],"warning":C['yel2'],"error":C['red2']}
        body=QScrollArea(); body.setWidgetResizable(True); body.setFrameShape(QFrame.NoFrame)
        body.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        body_w=QWidget(); body_lay=QVBoxLayout(body_w)
        body_lay.setContentsMargins(0,0,0,0); body_lay.setSpacing(0)
        if not notifs:
            e=QLabel("  No notifications yet",
                styleSheet=f"color:{C['t3']};padding:20px;font-size:13px;background:transparent;")
            body_lay.addWidget(e)
        else:
            for n in notifs[:8]:
                item=QWidget()
                if not n['read']:
                    item.setStyleSheet(f"background:{C['bg4']};")
                il=QHBoxLayout(item); il.setContentsMargins(16,10,16,10); il.setSpacing(10)
                dot=QLabel("*")
                dot.setStyleSheet(f"color:{colors.get(n['type'],C['blue2'])};font-size:8px;background:transparent;")
                ml=QLabel(n['msg']); ml.setWordWrap(True)
                ml.setStyleSheet(f"color:{C['t1'] if not n['read'] else C['t3']};"
                                 f"font-size:12px;background:transparent;")
                ts=QLabel(n['ts'][:10])
                ts.setFixedWidth(74)
                ts.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
                ts.setStyleSheet(f"color:{C['t3']};font-size:10px;background:transparent;")
                il.addWidget(dot); il.addWidget(ml,1); il.addWidget(ts)
                body_lay.addWidget(item); body_lay.addWidget(hline())
        body_lay.addStretch()
        body.setWidget(body_w)
        lay.addWidget(body,1)


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  MAIN WINDOW
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class MainWindow(QMainWindow):
    def __init__(self,user):
        super().__init__()
        self.user=user; self.settings=QSettings("Resora","v5")
        self.setWindowTitle("Resora - Research Operating System")
        self.resize(1440,900)
        self._center(); self._build(); self._menu(); self._shortcuts()

    def _center(self):
        sc=QApplication.desktop().availableGeometry()
        self.move((sc.width()-self.width())//2,(sc.height()-self.height())//2)

    def _build(self):
        central=QWidget(); self.setCentralWidget(central)
        root=QHBoxLayout(central); root.setContentsMargins(0,0,0,0); root.setSpacing(0)
        self.main_splitter=QSplitter(Qt.Horizontal)
        self.main_splitter.setHandleWidth(8)
        root.addWidget(self.main_splitter)

        # â”€â”€ SIDEBAR â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        sidebar=QFrame(); sidebar.setObjectName("sidebar")
        self.sidebar=sidebar
        sb=QVBoxLayout(sidebar); sb.setContentsMargins(0,0,0,0); sb.setSpacing(0)

        # Logo bar
        logo_bar=QWidget(); logo_bar.setFixedHeight(84)
        logo_bar.setStyleSheet(f"background:{C['bg0']};border-bottom:1px solid {C['border']};")
        ll=QHBoxLayout(logo_bar); ll.setContentsMargins(16,0,14,0); ll.setSpacing(10)
        mark=QLabel("R"); mark.setFixedSize(38,38); mark.setAlignment(Qt.AlignCenter)
        mark.setStyleSheet(
            f"background:{C['purple']};color:{C['bg0']};border-radius:9px;"
            f"font-size:21px;font-weight:900;letter-spacing:0px;"
        )
        brand=QVBoxLayout(); brand.setSpacing(1)
        logo_lbl=QLabel("Resora")
        logo_lbl.setStyleSheet(f"font-size:22px;font-weight:900;color:{C['t0']};"
                               f"letter-spacing:0px;background:transparent;")
        logo_sub=QLabel("Research OS")
        logo_sub.setStyleSheet(f"font-size:10px;font-weight:800;color:{C['purple']};letter-spacing:1.1px;background:transparent;")
        brand.addWidget(logo_lbl); brand.addWidget(logo_sub)
        ll.addWidget(mark)
        ll.addLayout(brand,1)
        self.notif_wrap=QWidget(); self.notif_wrap.setFixedSize(46,38); self.notif_wrap.setStyleSheet("background:transparent;")
        self.bell=QPushButton(self.notif_wrap); self.bell.setObjectName("btn_icon"); self.bell.setFixedSize(38,34)
        self.bell.move(0,2)
        self.bell.setIcon(bell_icon(C['t1'],C['purple']))
        self.bell.setIconSize(QSize(24,24))
        self.bell.setToolTip("Notifications")
        self.bell.clicked.connect(self._show_notifs)
        self.bell_badge=QLabel("",self.notif_wrap)
        self.bell_badge.setAlignment(Qt.AlignCenter)
        self.bell_badge.setFixedSize(20,18)
        self.bell_badge.move(26,0)
        self.bell_badge.setStyleSheet(f"background:{C['red']};color:#ffffff;border-radius:9px;"
                          f"font-size:9px;font-weight:900;padding:0px;")
        self.bell_badge.setVisible(False)
        ll.addWidget(self.notif_wrap)
        sb.addWidget(logo_bar)

        side_tools=QHBoxLayout(); side_tools.setContentsMargins(12,8,12,4); side_tools.setSpacing(8)
        collapse_btn=QPushButton("<"); collapse_btn.setObjectName("btn_small"); collapse_btn.setToolTip("Hide side menu")
        expand_btn=QPushButton(">"); expand_btn.setObjectName("btn_small"); expand_btn.setToolTip("Show side menu")
        wider_btn=QPushButton("Wider"); wider_btn.setObjectName("btn_small"); wider_btn.setToolTip("Make side menu wider")
        narrow_btn=QPushButton("Narrow"); narrow_btn.setObjectName("btn_small"); narrow_btn.setToolTip("Make side menu narrower")
        collapse_btn.clicked.connect(lambda:self._set_sidebar_width(0))
        expand_btn.clicked.connect(lambda:self._set_sidebar_width(248))
        wider_btn.clicked.connect(lambda:self._nudge_sidebar(40))
        narrow_btn.clicked.connect(lambda:self._nudge_sidebar(-40))
        for b in [collapse_btn,expand_btn,narrow_btn,wider_btn]:
            side_tools.addWidget(b)
        sb.addLayout(side_tools)

        # Nav scroll
        nav_scroll=QScrollArea(); nav_scroll.setWidgetResizable(True)
        nav_scroll.setFrameShape(QFrame.NoFrame)
        nav_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        nav_w=QWidget(); nav=QVBoxLayout(nav_w)
        nav.setContentsMargins(0,10,0,10); nav.setSpacing(0)
        self._btns={}; self._grp=QButtonGroup(self); self._grp.setExclusive(True)

        sections=[
            ("MAIN",     [("dashboard","H","Dashboard"),("search","S","Search"),
                           ("bookmarks","B","Bookmarks"),("reading","R","Reading List")]),
            ("AI TOOLS", [("analyze","A","Paper Analysis"),("summarize","M","Summarize"),
                           ("tools","T","Research Tools"),("chat","C","AI Assistant")]),
            ("WORKFLOW", [("workspace","W","Workspace"),("screen","N","Screen"),("prisma","P","PRISMA")]),
            ("ACCOUNT",  [("billing","$","Billing"),("profile","U","Profile")]),
        ]
        if self.user.get('is_admin'):
            sections.append(("ADMIN",[("admin","G","Admin")]))

        for section_title,pages in sections:
            sec_btn=QPushButton(section_title); sec_btn.setObjectName("nav_section")
            nav.addWidget(sec_btn)
            for key,icon,label in pages:
                lock="  Lock" if not plan_allows(self.user,key) else ""
                btn=QPushButton(f"  {icon}  {label}{lock}"); btn.setObjectName("nav")
                if lock:
                    btn.setToolTip(f"Requires {required_plan(key)} plan")
                btn.setCheckable(True); btn.setFixedHeight(42)
                btn.clicked.connect(partial(self.switch_to,key))
                self._grp.addButton(btn); self._btns[key]=btn; nav.addWidget(btn)

        nav.addStretch()
        div=QFrame(); div.setObjectName("sidebar_sep"); div.setFrameShape(QFrame.HLine)
        nav.addWidget(div)

        # User card
        uc=QWidget(); ucl=QHBoxLayout(uc); ucl.setContentsMargins(14,8,14,10); ucl.setSpacing(10)
        av_w=av(self.user.get('initials','?'),self.user.get('avatar_color',C['t0']),36)
        uinfo=QVBoxLayout(); uinfo.setSpacing(1)
        uinfo.addWidget(QLabel(self.user['name'].split()[0],
            styleSheet=f"font-size:12px;font-weight:700;color:{C['t1']};background:transparent;"))
        uinfo.addWidget(QLabel(self.user['plan'].capitalize(),
            styleSheet=f"font-size:10px;color:{C['t3']};background:transparent;"))
        ucl.addWidget(av_w); ucl.addLayout(uinfo); ucl.addStretch()
        lo=QPushButton("Out"); lo.setObjectName("btn_icon"); lo.setFixedSize(36,28)
        lo.setToolTip("Logout"); lo.clicked.connect(self._logout)
        ucl.addWidget(lo); nav.addWidget(uc)
        nav_scroll.setWidget(nav_w)
        sb.addWidget(nav_scroll,1)
        self.main_splitter.addWidget(sidebar)

        # â”€â”€ CONTENT STACK â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        self.stack=QStackedWidget()
        self._pages={}
        for key,cls,args in [
            ("dashboard",DashboardPage,(self.user,)),
            ("search",SearchPage,(self.user,self.settings)),
            ("bookmarks",BookmarksPage,(self.user,)),
            ("reading",ReadingListPage,(self.user,)),
            ("analyze",AnalysisPage,(self.user,)),
            ("summarize",SummarizePage,(self.user,)),
            ("tools",ResearchToolsPage,(self.user,)),
            ("chat",AIChatPage,(self.user,)),
            ("workspace",WorkspacePage,(self.user,)),
            ("screen",ScreenPage,(self.user,self.settings)),
            ("prisma",PrismaPage,()),
            ("billing",BillingPage,(self.user,)),
            ("profile",ProfilePage,(self.user,)),
        ]:
            p=cls(*args)
            self._pages[key]=p
            self.stack.addWidget(scrolled(p))
        if self.user.get('is_admin'):
            p=AdminPage(self.user); self._pages["admin"]=p; self.stack.addWidget(p)

        # Wire signals
        self._pages["dashboard"].go_to.connect(self.switch_to)
        self._pages["search"].to_sum.connect(self._to_sum)
        self._pages["search"].to_analyze.connect(self._to_analyze)
        self._pages["billing"].plan_changed.connect(self._plan_changed)

        self.main_splitter.addWidget(self.stack)
        saved_sidebar=int(self.settings.value("sidebar_width",248))
        self.main_splitter.setSizes([saved_sidebar, max(900, self.width()-saved_sidebar)])

        # Status bar
        self.sb=self.statusBar()
        self.sb.showMessage("Loading ML models... please wait.")

        # Notification timer
        self._notif_timer=QTimer(); self._notif_timer.setInterval(30000)
        self._notif_timer.timeout.connect(self._refresh_bell); self._notif_timer.start()
        self._refresh_bell()
        self.switch_to("dashboard")

    def _menu(self):
        mb=self.menuBar()
        fm=mb.addMenu("File")
        for l2,pg,sh in [("Dashboard","dashboard","Ctrl+1"),("Search","search","Ctrl+2"),
                          ("Summarize","summarize","Ctrl+3"),("Screen","screen","Ctrl+4"),
                          ("PRISMA","prisma","Ctrl+5"),("AI Chat","chat","Ctrl+6")]:
            a=QAction(l2,self); a.setShortcut(sh)
            a.triggered.connect(partial(self.switch_to,pg)); fm.addAction(a)
        fm.addSeparator()
        fm.addAction(QAction("Logout",self,triggered=self._logout))
        fm.addAction(QAction("Exit",self,triggered=self.close))
        vm=mb.addMenu("View")
        vm.addAction(QAction("Toggle Sidebar",self,shortcut="Ctrl+\\",
            triggered=lambda:self.findChild(QFrame,"sidebar").setVisible(
                not self.findChild(QFrame,"sidebar").isVisible())))
        hm=mb.addMenu("Help")
        hm.addAction(QAction("About",self,triggered=self._about))
        hm.addAction(QAction("Check Updates",self,
            triggered=lambda:QMessageBox.information(self,"Updates","Resora v5.0 is up to date!")))
        hm.addAction(QAction("Documentation",self,
            triggered=lambda:webbrowser.open("https://docs.resora.ai")))

    def _shortcuts(self):
        QShortcut(QKeySequence("Ctrl+F"),self,
            lambda:(self.switch_to("search"),self._pages["search"].focus()))
        QShortcut(QKeySequence("Ctrl+Return"),self,
            lambda:self._pages["search"].run_search())

    def switch_to(self,key):
        if key not in self._pages: return
        if not plan_allows(self.user, key):
            need=required_plan(key)
            QMessageBox.information(
                self,
                "Plan Upgrade Required",
                f"{self._btns.get(key).text().strip() if key in self._btns else key.title()} is locked on your current plan.\n\n"
                f"Upgrade to {need} to use this feature."
            )
            self.switch_to("billing")
            return
        idx=list(self._pages.keys()).index(key)
        self.stack.setCurrentIndex(idx)
        btn=self._btns.get(key)
        if btn: btn.setChecked(True)

    def _set_sidebar_width(self,width):
        width=max(0,min(380,int(width)))
        total=sum(self.main_splitter.sizes()) or self.width()
        self.main_splitter.setSizes([width,max(500,total-width)])
        self.settings.setValue("sidebar_width",width)

    def _nudge_sidebar(self,delta):
        sizes=self.main_splitter.sizes()
        cur=sizes[0] if sizes else int(self.settings.value("sidebar_width",248))
        self._set_sidebar_width(cur+delta)

    def _to_sum(self,abstract,title):
        self._pages["summarize"].set_abstract(abstract,title)
        self.switch_to("summarize")

    def _to_analyze(self,paper_dict):
        self._pages["analyze"].set_paper(paper_dict)
        self.switch_to("analyze")

    def _plan_changed(self):
        self.user=get_user(self.user['id'])
        for page in self._pages.values():
            if hasattr(page,"user"):
                page.user=self.user

    def _show_notifs(self):
        popup=NotifPopup(self.user,self)
        pos=self.notif_wrap.mapToGlobal(QPoint(0,self.notif_wrap.height()))
        screen=QApplication.desktop().availableGeometry(self)
        x=pos.x()+self.notif_wrap.width()-popup.width()
        y=pos.y()+6
        x=max(screen.left()+12,min(x,screen.right()-popup.width()-12))
        y=max(screen.top()+12,min(y,screen.bottom()-popup.height()-12))
        popup.move(x,y)
        popup.exec_(); self._refresh_bell()

    def _refresh_bell(self):
        n=unread_count(self.user['id'])
        self.bell_badge.setText("99+" if n>99 else (str(n) if n else ""))
        self.bell_badge.setVisible(bool(n))

    def _logout(self): self.close(); QApplication.quit()

    def _about(self):
        QMessageBox.about(self,"About Resora",
            "<h2 style='color:#f97316'>Resora v5.0</h2>"
            "<p><b>Research Operating System - SaaS Edition</b></p>"
            "<p>320+ Features | 12 Modules | Production Ready</p>"
            "<hr>"
            "<p>50,000 ArXiv papers | FAISS + TF-IDF search<br>"
            "BART summarization | Paper Analysis Engine<br>"
            "AI Research Assistant | Research Workspace<br>"
            "PRISMA 2020 diagrams | Citation Formatter<br>"
            "Research Gap Finder | Full billing system</p>"
            "<p>PyQt5 | NumPy | FAISS | Transformers | SQLite</p>"
            "<p style='color:#f97316'>(c) 2024 Waqar Ali</p>")

    def set_ready(self,n):
        self.sb.showMessage(
            f"All models loaded  |  {n:,} papers indexed  "
            f"|  {backend.mode.capitalize()} Search Active  |  Ready")

    def set_error(self,msg):
        self.sb.showMessage(
            "Models partially loaded - TF-IDF search active | Run setup_fix.bat to fix PyTorch DLL")


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
#  ENTRY POINT
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def main():
    app=QApplication(sys.argv)
    app.setApplicationName("Resora")
    app.setOrganizationName("Resora")
    app.setStyleSheet(QSS)
    app.setFont(QFont("Segoe UI",13))

    auth=AuthDialog()
    if auth.exec_()!=QDialog.Accepted or not auth.user: sys.exit(0)
    user=auth.user

    window=MainWindow(user)
    splash=Splash(); splash.show(); QApplication.processEvents()

    loader=LoadWorker(); loader.progress.connect(splash.set)

    def on_loaded():
        splash.close(); window.set_ready(backend.paper_count); window.show()
        notify(user['id'],
            f"Ready! {backend.paper_count:,} papers indexed via {backend.mode} search.","success")

    def on_error(msg):
        splash.close(); window.show(); window.set_error(msg)
        QMessageBox.warning(window,"Model Warning",
            "Some ML models could not load:\n\n"+msg[:300]+
            "\n\n- Run setup_fix.bat to fix PyTorch DLL error on Windows.\n"
            "- Search still works via TF-IDF keyword search.\n"
            "- Billing, Profile, PRISMA, Admin all work fine.")

    loader.done.connect(on_loaded); loader.err.connect(on_error); loader.start()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
