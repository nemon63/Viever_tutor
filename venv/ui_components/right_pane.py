from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PyQt5.QtCore import Qt
from ui_components.text_editors import TextEditors
from ui_components.media_widgets import MediaWidgets

class RightPane(QWidget):
    def __init__(self, main_window):
        """
        Инициализация правой панели, содержащей медиа-виджеты и текстовые редакторы.

        Args:
            main_window (QMainWindow): Основное окно приложения.
        """
        super().__init__()
        self.main_window = main_window

        # Создание основного вертикального макета
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Создание разделителя для разделения медиа-виджетов и текстовых редакторов
        self.splitter = QSplitter(Qt.Vertical)
        self.layout.addWidget(self.splitter)

        # Инициализация медиа-виджетов и добавление их в верхнюю часть разделителя
        self.media_widgets = MediaWidgets(self.main_window)
        self.splitter.addWidget(self.media_widgets)

        # Инициализация текстовых редакторов и добавление их в нижнюю часть разделителя
        self.text_editors = TextEditors(self.main_window)
        self.splitter.addWidget(self.text_editors)
