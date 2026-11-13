import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QPlainTextEdit, QSplitter, QFileDialog, QMessageBox,
                             QLabel, QTabWidget)
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

        # --- 1. Главная область (Разделитель) ---
        self.splitter = QSplitter(Qt.Orientation.Vertical, self)
        
        # Вкладки для редактора (Доп. требование №2)
        self.tabs = QTabWidget()
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("Consolas", 11))
        self.tabs.addTab(self.editor, "Новый документ")
        
        # Окно вывода (только для чтения - требование задания)
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
        self.splitter.setStretchFactor(0, 3) # Редактор больше
        self.splitter.setStretchFactor(1, 1) # Вывод меньше
        self.setCentralWidget(self.splitter)

        # --- 2. Создаем действия (Actions) ---
        self.create_actions()
        
        # --- 3. Создаем меню и панель инструментов ---
        self.create_menus()
        self.create_toolbar()
        self.create_statusbar()

        # Сигнал изменения текста
        self.editor.textChanged.connect(self.update_modified_flag)

    def create_actions(self):
        # Файл
        self.act_new = QAction("Создать", self)
        self.act_new.setShortcut(QKeySequence.StandardKey.New)
        self.act_new.triggered.connect(self.new_file)

        self.act_open = QAction("Открыть", self)
        self.act_open.setShortcut(QKeySequence.StandardKey.Open)
        self.act_open.triggered.connect(self.open_file)

        self.act_save = QAction("Сохранить", self)
        self.act_save.setShortcut(QKeySequence.StandardKey.Save)
        self.act_save.triggered.connect(self.save_file)

        self.act_save_as = QAction("Сохранить как", self)
        self.act_save_as.triggered.connect(self.save_file_as)

        self.act_exit = QAction("Выход", self)
        self.act_exit.triggered.connect(self.close)

        # Правка
        self.act_undo = QAction("Отменить", self)
        self.act_undo.setShortcut(QKeySequence.StandardKey.Undo)
        self.act_undo.triggered.connect(self.editor.undo)

        self.act_redo = QAction("Повторить", self)
        self.act_redo.setShortcut(QKeySequence.StandardKey.Redo)
        self.act_redo.triggered.connect(self.editor.redo)

        self.act_cut = QAction("Вырезать", self)
        self.act_cut.setShortcut(QKeySequence.StandardKey.Cut)
        self.act_cut.triggered.connect(self.editor.cut)

        self.act_copy = QAction("Копировать", self)
        self.act_copy.setShortcut(QKeySequence.StandardKey.Copy)
        self.act_copy.triggered.connect(self.editor.copy)

        self.act_paste = QAction("Вставить", self)
        self.act_paste.setShortcut(QKeySequence.StandardKey.Paste)
        self.act_paste.triggered.connect(self.editor.paste)

        self.act_delete = QAction("Удалить", self)
        self.act_delete.triggered.connect(lambda: self.editor.textCursor().removeSelectedText())

        self.act_select_all = QAction("Выделить все", self)
        self.act_select_all.setShortcut(QKeySequence.StandardKey.SelectAll)
        self.act_select_all.triggered.connect(self.editor.selectAll)

        # Пуск
        self.act_run = QAction("Пуск", self)
        self.act_run.triggered.connect(self.run_parser)

        # Справка
        self.act_help = QAction("Вызов справки", self)
        self.act_help.triggered.connect(self.show_help)

        self.act_about = QAction("О программе", self)
        self.act_about.triggered.connect(self.show_about)

    def create_menus(self):
        menubar = self.menuBar()

        # 1. Файл
        file_menu = menubar.addMenu("Файл")
        file_menu.addAction(self.act_new)
        file_menu.addAction(self.act_open)
        file_menu.addAction(self.act_save)
        file_menu.addAction(self.act_save_as)
        file_menu.addSeparator()
        file_menu.addAction(self.act_exit)

        # 2. Правка
        edit_menu = menubar.addMenu("Правка")
        edit_menu.addAction(self.act_undo)
        edit_menu.addAction(self.act_redo)
        edit_menu.addSeparator()
        edit_menu.addAction(self.act_cut)
        edit_menu.addAction(self.act_copy)
        edit_menu.addAction(self.act_paste)
        edit_menu.addAction(self.act_delete)
        edit_menu.addSeparator()
        edit_menu.addAction(self.act_select_all)

        # 3. Текст (Заглушки)
        text_menu = menubar.addMenu("Текст")
        stubs = ["Постановка задачи", "Грамматика", "Классификация грамматики",
                 "Метод анализа", "Тестовый пример", "Список литературы", "Исходный код программы"]
        for s in stubs:
            text_menu.addAction(s, lambda checked, name=s: self.show_stub(name))

        # 4. Пуск
        run_menu = menubar.addMenu("Пуск")
        run_menu.addAction(self.act_run)

        # 5. Справка
        help_menu = menubar.addMenu("Справка")
        help_menu.addAction(self.act_help)
        help_menu.addAction(self.act_about)

    def create_toolbar(self):
        toolbar = self.addToolBar("Main")
        toolbar.setMovable(False)
        
        # Добавляем действия в том порядке, как на скриншоте
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
        self.status_label = QLabel("Готово")
        self.statusBar().addWidget(self.status_label)
        self.statusBar().addPermanentWidget(QLabel("UTF-8"))

    # --- Логика ---
    def update_modified_flag(self):
        self.is_modified = True
        name = os.path.basename(self.current_file) if self.current_file else "Новый документ"
        self.setWindowTitle(f"{APP_NAME} — {name} *")
        self.status_label.setText("Изменено")

    def maybe_save(self):
        if not self.is_modified:
            return True
        ret = QMessageBox.warning(self, APP_NAME, 
                                  "Документ был изменён.\nСохранить изменения?",
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
        self.setWindowTitle(f"{APP_NAME} — Новый документ")

    def open_file(self):
        if not self.maybe_save(): return
        path, _ = QFileDialog.getOpenFileName(self, "Открыть", "", "Текстовые файлы (*.txt);;Все файлы (*)")
        if not path: return
        with open(path, 'r', encoding='utf-8') as f:
            self.editor.setPlainText(f.read())
        self.current_file = path
        self.is_modified = False
        self.setWindowTitle(f"{APP_NAME} — {os.path.basename(path)}")

    def save_file(self):
        if not self.current_file:
            return self.save_file_as()
        with open(self.current_file, 'w', encoding='utf-8') as f:
            f.write(self.editor.toPlainText())
        self.is_modified = False
        self.setWindowTitle(f"{APP_NAME} — {os.path.basename(self.current_file)}")
        self.status_label.setText("Сохранено")
        return True

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "Текстовые файлы (*.txt)")
        if not path: return False
        self.current_file = path
        return self.save_file()

    def run_parser(self):
        self.output.clear()
        text = self.editor.toPlainText()
        
        if not text.strip():
            self.output.appendPlainText("Ошибка: текст пуст.")
            return
            
        # Базовая проверка (заглушка для будущего парсера)
        if "struct" in text and "{" in text and "}" in text and ";" in text:
            self.output.appendPlainText("✅ Обнаружены ключевые элементы объявления структуры.")
            self.output.appendPlainText("⚠️ Полноценный синтаксический анализ будет добавлен в следующей работе.")
        else:
            self.output.appendPlainText("❌ Ошибка: не найдены обязательные элементы (struct, {, }, ;).")
            self.output.appendPlainText("Ожидается объявление вида: struct Name { ... };")

    def show_help(self):
        QMessageBox.information(self, "Справка", 
            f"Руководство пользователя для {APP_NAME}.\n\n"
            "1. Используйте меню 'Файл' для создания, открытия и сохранения файлов.\n"
            "2. Меню 'Правка' содержит стандартные команды работы с текстом.\n"
            "3. Нажмите 'Пуск', чтобы запустить базовую проверку кода.\n\n"
            "Полноценный синтаксический анализатор будет добавлен в следующей работе.")

    def show_about(self):
        QMessageBox.about(self, "О программе", 
            f"{APP_NAME} v0.1\n"
            "Лабораторная работа по дисциплине 'Методы трансляции и компиляции'.\n\n"
            "Модуль интерфейса для синтаксического анализатора структур языка C.\n"
            "Ядро парсера будет реализовано в следующей лабораторной работе.")

    def show_stub(self, name):
        QMessageBox.information(self, name, f"Раздел «{name}» будет реализован позже.")

    def closeEvent(self, event):
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()