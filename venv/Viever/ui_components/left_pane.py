from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QTreeView
from PyQt5.QtCore import Qt

class LeftPane(QWidget):
    def __init__(self, main_window):
        """
        Инициализация левой панели, содержащей элементы управления и дерево файлов.

        Args:
            main_window (QMainWindow): Основное окно приложения.
        """
        super().__init__()
        self.main_window = main_window

        # Создание основного вертикального макета
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Инициализация элементов управления и дерева файлов
        self.initControls()
        self.initTreeView()

    def initControls(self):
        """
        Инициализация элементов управления на левой панели.
        """
        # Создание горизонтального макета для элементов управления
        self.controls_layout = QHBoxLayout()

        # Создание кнопки для выбора папки
        self.btn_open = QPushButton("Выберите папку")
        self.btn_open.clicked.connect(self.main_window.open_folder)
        self.controls_layout.addWidget(self.btn_open)

        # Создание кнопки для отметки файла как просмотренного
        self.pbt_reviewed = QPushButton("Отметить как просмотренно")
        self.pbt_reviewed.clicked.connect(self.main_window.mark_as_reviewed)
        self.controls_layout.addWidget(self.pbt_reviewed)

        # Создание строки поиска
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Поиск...")
        self.search_bar.textChanged.connect(self.main_window.filter_tree_view)
        self.controls_layout.addWidget(self.search_bar)

        # Создание селектора темы
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Светлая тема", "Темная тема"])
        self.theme_selector.currentIndexChanged.connect(self.main_window.change_theme)
        self.controls_layout.addWidget(self.theme_selector)

        # Добавление горизонтального макета элементов управления в основной макет
        self.layout.addLayout(self.controls_layout)

    def initTreeView(self):
        """
        Инициализация дерева файлов на левой панели.
        """
        self.tree_view = QTreeView()
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.main_window.open_menu)
        self.tree_view.doubleClicked.connect(self.main_window.on_tree_view_double_clicked)
        self.tree_view.clicked.connect(self.main_window.on_tree_view_clicked)
        self.tree_view.header().setSortIndicatorShown(True)
        self.tree_view.header().setSectionsClickable(True)
        self.tree_view.header().sectionClicked.connect(self.main_window.sort_tree_view)
        self.layout.addWidget(self.tree_view)
