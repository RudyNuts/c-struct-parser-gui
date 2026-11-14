# C Struct Parser (GUI)

A graphical user interface module for a C struct declaration parser.

## About the Project
This project is a laboratory work for the "Methods of Translation and Compilation" course in NSU. 
It represents a text editor with a graphical user interface, prepared for the future integration of a syntax analyzer (parser) for C struct declarations.

**Current status:** The GUI module is fully implemented (version 0.1). The parser core will be added later.

## Features
- File management (New, Open, Save, Save As, Exit)
- Standard text editing operations (Undo, Redo, Cut, Copy, Paste, Delete, Select All)
- Split view: code editor and output area
- Dark theme for the read-only output area
- Status bar with information
- Stub menus for future sections (Task Statement, Grammar, etc.)
- Keyboard shortcuts for all major actions

## How to Run

### Option 1: Using Python (requires Python 3.10+)
1. Install the dependencies:
```bash
pip install -r requirements.txt
```
2. Run application:
```bash
python main.py
```

### Option 2: Using the compiled binaries:
Download the appropriate file from the **[Releases page](https://github.com/RudyNuts/c-struct-parser-gui/releases/tag/v0.1)**:
- Windows (64-bit): Download CStructParserGUI_Windows_x64.exe and run it.
- Linux (64-bit): Download CStructParserGUI_Linux_x64, make it executable, and run it:
```bash
chmod +x CStructParserGUI_Linux_x64
./CStructParserGUI_Linux_x64
```
## Project Structure
- `main`.py — application entry point
- `mainwindow.py` — main window class and GUI logic
- `requirements.txt` — project dependencies
- `.gitignore` — Git ignore rules
