import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPlainTextEdit,
                             QSplitter, QFileDialog, QMessageBox, QLabel, QTabWidget)
from PyQt6.QtGui import QAction, QKeySequence, QFont
from PyQt6.QtCore import Qt

APP_NAME = "C Struct Parser (GUI)"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(900, 700)

        self.current_file = None
        self.is_modified = False

        self.splitter = QSplitter(Qt.Orientation.Vertical, self)
        
        self.tabs = QTabWidget()
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        self.tabs.addTab(self.editor, "New document")
        
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFont(QFont("Consolas", 10))
        self.output.setStyleSheet("""
            QPlainTextEdit { 
                background-color: #1e1e1e; 
                color: #d4d4d4; 
                border: 1px solid #3c3c3c; 
            }
        """)

        self.splitter.addWidget(self.tabs)
        self.splitter.addWidget(self.output)
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 1)
        self.setCentralWidget(self.splitter)

        self.create_actions()
        self.create_menus()
        self.create_toolbar()
        self.create_statusbar()

        self.editor.textChanged.connect(self.update_modified_flag)

    def create_actions(self):
        # File
        self.act_new = QAction("New", self)
        self.act_new.setShortcut(QKeySequence.StandardKey.New)
        self.act_new.triggered.connect(self.new_file)

        self.act_open = QAction("Open", self)
        self.act_open.setShortcut(QKeySequence.StandardKey.Open)
        self.act_open.triggered.connect(self.open_file)

        self.act_save = QAction("Save", self)
        self.act_save.setShortcut(QKeySequence.StandardKey.Save)
        self.act_save.triggered.connect(self.save_file)

        self.act_save_as = QAction("Save As", self)
        self.act_save_as.triggered.connect(self.save_file_as)

        self.act_exit = QAction("Exit", self)
        self.act_exit.triggered.connect(self.close)

        # Edit
        self.act_undo = QAction("Undo", self)
        self.act_undo.setShortcut(QKeySequence.StandardKey.Undo)
        self.act_undo.triggered.connect(self.editor.undo)

        self.act_redo = QAction("Redo", self)
        self.act_redo.setShortcut(QKeySequence.StandardKey.Redo)
        self.act_redo.triggered.connect(self.editor.redo)

        self.act_cut = QAction("Cut", self)
        self.act_cut.setShortcut(QKeySequence.StandardKey.Cut)
        self.act_cut.triggered.connect(self.editor.cut)

        self.act_copy = QAction("Copy", self)
        self.act_copy.setShortcut(QKeySequence.StandardKey.Copy)
        self.act_copy.triggered.connect(self.editor.copy)

        self.act_paste = QAction("Paste", self)
        self.act_paste.setShortcut(QKeySequence.StandardKey.Paste)
        self.act_paste.triggered.connect(self.editor.paste)

        self.act_delete = QAction("Delete", self)
        self.act_delete.triggered.connect(lambda: self.editor.textCursor().removeSelectedText())

        self.act_select_all = QAction("Select All", self)
        self.act_select_all.setShortcut(QKeySequence.StandardKey.SelectAll)
        self.act_select_all.triggered.connect(self.editor.selectAll)

        # Run
        self.act_run = QAction("Run", self)
        self.act_run.triggered.connect(self.run_parser)

        # Help
        self.act_help = QAction("Help", self)
        self.act_help.triggered.connect(self.show_help)

        self.act_about = QAction("About", self)
        self.act_about.triggered.connect(self.show_about)

    def create_menus(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        file_menu.addAction(self.act_new)
        file_menu.addAction(self.act_open)
        file_menu.addAction(self.act_save)
        file_menu.addAction(self.act_save_as)
        file_menu.addSeparator()
        file_menu.addAction(self.act_exit)

        edit_menu = menubar.addMenu("Edit")
        edit_menu.addAction(self.act_undo)
        edit_menu.addAction(self.act_redo)
        edit_menu.addSeparator()
        edit_menu.addAction(self.act_cut)
        edit_menu.addAction(self.act_copy)
        edit_menu.addAction(self.act_paste)
        edit_menu.addAction(self.act_delete)
        edit_menu.addSeparator()
        edit_menu.addAction(self.act_select_all)

        text_menu = menubar.addMenu("Text")
        
        act_task = QAction("Task Statement", self)
        act_task.triggered.connect(lambda: self.show_stub("Task Statement"))
        text_menu.addAction(act_task)

        act_grammar = QAction("Grammar", self)
        act_grammar.triggered.connect(lambda: self.show_stub("Grammar"))
        text_menu.addAction(act_grammar)

        act_class = QAction("Grammar Classification", self)
        act_class.triggered.connect(lambda: self.show_stub("Grammar Classification"))
        text_menu.addAction(act_class)

        act_method = QAction("Analysis Method", self)
        act_method.triggered.connect(lambda: self.show_stub("Analysis Method"))
        text_menu.addAction(act_method)

        act_test = QAction("Test Example", self)
        act_test.triggered.connect(lambda: self.show_stub("Test Example"))
        text_menu.addAction(act_test)

        act_refs = QAction("References", self)
        act_refs.triggered.connect(lambda: self.show_stub("References"))
        text_menu.addAction(act_refs)

        act_src = QAction("Source Code", self)
        act_src.triggered.connect(lambda: self.show_stub("Source Code"))
        text_menu.addAction(act_src)

        run_menu = menubar.addMenu("Run")
        run_menu.addAction(self.act_run)

        help_menu = menubar.addMenu("Help")
        help_menu.addAction(self.act_help)
        help_menu.addAction(self.act_about)

    def create_toolbar(self):
        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)
        
        toolbar.addAction(self.act_new)
        toolbar.addAction(self.act_open)
        toolbar.addAction(self.act_save)
        toolbar.addSeparator()
        toolbar.addAction(self.act_undo)
        toolbar.addAction(self.act_redo)
        toolbar.addSeparator()
        toolbar.addAction(self.act_copy)
        toolbar.addAction(self.act_cut)
        toolbar.addAction(self.act_paste)
        toolbar.addSeparator()
        toolbar.addAction(self.act_run)
        toolbar.addAction(self.act_help)
        toolbar.addAction(self.act_about)

    def create_statusbar(self):
        self.status_label = QLabel("Ready")
        self.statusBar().addWidget(self.status_label)
        self.statusBar().addPermanentWidget(QLabel("UTF-8"))

    def update_modified_flag(self):
        self.is_modified = True
        name = os.path.basename(self.current_file) if self.current_file else "New document"
        self.setWindowTitle(f"{APP_NAME} - {name} *")
        self.status_label.setText("Modified")

    def maybe_save(self):
        if not self.is_modified:
            return True
        ret = QMessageBox.warning(self, APP_NAME, 
                                  "The document has been modified.\nDo you want to save your changes?",
                                  QMessageBox.StandardButton.Save | 
                                  QMessageBox.StandardButton.Discard | 
                                  QMessageBox.StandardButton.Cancel)
        if ret == QMessageBox.StandardButton.Save:
            return self.save_file()
        elif ret == QMessageBox.StandardButton.Cancel:
            return False
        return True

    def new_file(self):
        if not self.maybe_save(): return
        self.editor.clear()
        self.is_modified = False
        self.current_file = None
        self.setWindowTitle(f"{APP_NAME} - New document")
        self.tabs.setTabText(0, "New document")

    def open_file(self):
        if not self.maybe_save(): return
        path, _ = QFileDialog.getOpenFileName(self, "Open", "", "Text files (*.txt);;All files (*)")
        if not path: return
        with open(path, 'r', encoding='utf-8') as f:
            self.editor.setPlainText(f.read())
        self.current_file = path
        self.is_modified = False
        self.setWindowTitle(f"{APP_NAME} - {os.path.basename(path)}")
        self.tabs.setTabText(0, os.path.basename(path))

    def save_file(self):
        if not self.current_file:
            return self.save_file_as()
        with open(self.current_file, 'w', encoding='utf-8') as f:
            f.write(self.editor.toPlainText())
        self.is_modified = False
        self.setWindowTitle(f"{APP_NAME} - {os.path.basename(self.current_file)}")
        self.tabs.setTabText(0, os.path.basename(self.current_file))
        self.status_label.setText("Saved")
        return True

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save As", "", "Text files (*.txt)")
        if not path: return False
        self.current_file = path
        return self.save_file()

    def run_parser(self):
        self.output.clear()
        self.output.appendPlainText("Parser is not connected yet.\n(Will be implemented in the next lab).")

    def show_help(self):
        QMessageBox.information(self, "Help", 
            f"User guide for {APP_NAME}.\n\n"
            "1. Use the 'File' menu to create, open, and save files.\n"
            "2. The 'Edit' menu contains standard text editing commands.\n"
            "3. Click 'Run' to start the parser.\n\n"
            "The full syntax analyzer will be added in the next lab.")

    def show_about(self):
        QMessageBox.about(self, "About", f"{APP_NAME} v0.1")

    def show_stub(self, name):
        QMessageBox.information(self, name, f"The '{name}' section will be implemented later.")

    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()
