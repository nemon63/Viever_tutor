from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit

class TextEditors(QWidget):
    def __init__(self, main_window):
        """
        Инициализация редакторов текста.

        Args:
            main_window (QMainWindow): Основное окно приложения.
        """
        super().__init__()
        self.main_window = main_window

        # Создание основного макета
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Инициализация текстового редактора для описания
        self.text_edit_descript = QTextEdit()
        self.text_edit_descript.setPlaceholderText("Описание...")
        self.text_edit_descript.textChanged.connect(self.main_window.save_description)
        self.layout.addWidget(self.text_edit_descript)

        # Создание горизонтального макета для комментариев и кода
        self.horizontal_layout_2 = QHBoxLayout()
        self.text_edit_comment = QTextEdit()
        self.text_edit_comment.setPlaceholderText("Комментарий...")
        self.text_edit_code = QTextEdit()
        self.text_edit_code.setPlaceholderText("Код...")
        self.horizontal_layout_2.addWidget(self.text_edit_comment)
        self.horizontal_layout_2.addWidget(self.text_edit_code)
        self.layout.addLayout(self.horizontal_layout_2)

        # Установка фильтра событий для текстовых редакторов
        self.text_edit_comment.installEventFilter(self.main_window)
        self.text_edit_code.installEventFilter(self.main_window)

        # Создание горизонтального макета для кнопок сохранения и загрузки
        self.horizontal_layout_3 = QHBoxLayout()
        self.pbt_save = QPushButton("Сохранить")
        self.pbt_save.clicked.connect(self.main_window.save_changes)
        self.horizontal_layout_3.addWidget(self.pbt_save)
        self.pbt_load = QPushButton("Загрузить")
        self.pbt_load.clicked.connect(self.main_window.load_changes)
        self.horizontal_layout_3.addWidget(self.pbt_load)
        self.layout.addLayout(self.horizontal_layout_3)

        # Инициализация текстового поля для тегов
        self.text_edit_tags = QLineEdit()
        self.text_edit_tags.setPlaceholderText("Теги (разделяйте пробелами)")
        self.layout.addWidget(self.text_edit_tags)
