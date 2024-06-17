import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QSplitter, QStatusBar, QFileDialog, QFileSystemModel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QComboBox, QTreeView, QTextEdit, QLabel
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt
from file_operations import load_data, save_data, load_image
from event_handlers import handle_tree_view_clicked, handle_tree_view_double_clicked, handle_menu
from video_player import VideoPlayer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Видео уроки")
        self.setGeometry(100, 100, 1049, 805)

        # Инициализация переменных для текущей папки и пути
        self.current_folder = None
        self.current_path = None
        self.data_file = None
        self.data = {}
        self.preview_cache_folder = None

        # Создание и заполнение изображения-заполнителя
        self.placeholder_image = QPixmap(400, 300)
        self.placeholder_image.fill(Qt.lightGray)

        self.initUI()

    def initUI(self):
        # Инициализация центрального виджета и главного макета
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.grid_layout = QGridLayout(self.central_widget)
        self.splitter = QSplitter(Qt.Horizontal)
        self.grid_layout.addWidget(self.splitter)

        self.initLeftPane()
        self.initRightPane()

        # Инициализация строки состояния
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def initLeftPane(self):
        # Инициализация левого окна
        self.left_widget = QWidget()
        self.left_layout = QVBoxLayout()
        self.left_widget.setLayout(self.left_layout)

        self.initLeftPaneControls()
        self.initTreeView()

        self.splitter.addWidget(self.left_widget)

    def initLeftPaneControls(self):
        # Инициализация элементов управления в левом окне
        self.horizontal_layout = QHBoxLayout()

        self.btn_open = QPushButton("Выберите папку")
        self.btn_open.clicked.connect(self.open_folder)
        self.horizontal_layout.addWidget(self.btn_open)

        self.pbt_reviewed = QPushButton("Отметить как просмотренно")
        self.pbt_reviewed.clicked.connect(self.mark_as_reviewed)
        self.horizontal_layout.addWidget(self.pbt_reviewed)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Поиск...")
        self.search_bar.textChanged.connect(self.filter_tree_view)
        self.horizontal_layout.addWidget(self.search_bar)

        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Светлая тема", "Темная тема"])
        self.theme_selector.currentIndexChanged.connect(self.change_theme)
        self.horizontal_layout.addWidget(self.theme_selector)

        self.left_layout.addLayout(self.horizontal_layout)

    def initTreeView(self):
        # Инициализация древовидного вида файлов
        self.tree_view = QTreeView()
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.open_menu)
        self.tree_view.doubleClicked.connect(self.on_tree_view_double_clicked)
        self.tree_view.clicked.connect(self.on_tree_view_clicked)
        self.tree_view.header().setSortIndicatorShown(True)
        self.tree_view.header().setSectionsClickable(True)
        self.tree_view.header().sectionClicked.connect(self.sort_tree_view)
        self.left_layout.addWidget(self.tree_view)

    def initRightPane(self):
        # Инициализация правого окна
        self.right_splitter = QSplitter(Qt.Vertical)
        self.initMediaWidgets()
        self.initTextEditors()
        self.splitter.addWidget(self.right_splitter)

    def initMediaWidgets(self):
        # Инициализация медиа-виджетов (видеоплеер и изображение)
        self.video_player = VideoPlayer(self)
        self.video_player.setMinimumSize(800, 600)
        self.video_player.time_changed.connect(self.update_tags_display)

        self.image_label = QLabel("image")
        self.image_label.setFrameShape(QLabel.Panel)
        self.image_label.setFrameShadow(QLabel.Plain)
        self.image_label.setLineWidth(1)
        self.image_label.setMidLineWidth(1)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(800, 600)
        self.image_label.setScaledContents(False)  # Изменено на False

        self.text_view = QTextEdit()
        self.text_view.setMinimumSize(800, 600)

        self.media_layout = QVBoxLayout()
        self.media_layout.addWidget(self.image_label)
        self.media_layout.addWidget(self.video_player)

        self.media_widget = QWidget()
        self.media_widget.setLayout(self.media_layout)

        self.right_splitter.addWidget(self.media_widget)
        self.right_splitter.addWidget(self.text_view)
        self.right_splitter.setStretchFactor(0, 3)
        self.right_splitter.setStretchFactor(1, 1)
        self.show_video_player(False)

    def initTextEditors(self):
        # Инициализация редакторов текста
        self.text_edit_widget = QWidget()
        self.text_edit_layout = QVBoxLayout(self.text_edit_widget)

        self.text_edit_descript = QTextEdit()
        self.text_edit_descript.textChanged.connect(self.save_description)
        self.text_edit_layout.addWidget(self.text_edit_descript)

        self.horizontal_layout_2 = QHBoxLayout()
        self.text_edit_comment = QTextEdit()
        self.text_edit_code = QTextEdit()
        self.horizontal_layout_2.addWidget(self.text_edit_comment)
        self.horizontal_layout_2.addWidget(self.text_edit_code)
        self.text_edit_layout.addLayout(self.horizontal_layout_2)

        self.text_edit_comment.installEventFilter(self)
        self.text_edit_code.installEventFilter(self)

        self.horizontal_layout_3 = QHBoxLayout()
        self.pbt_save = QPushButton("Сохранить")
        self.pbt_save.clicked.connect(self.save_changes)
        self.horizontal_layout_3.addWidget(self.pbt_save)
        self.pbt_load = QPushButton("Загрузить")
        self.pbt_load.clicked.connect(self.load_changes)
        self.horizontal_layout_3.addWidget(self.pbt_load)
        self.text_edit_layout.addLayout(self.horizontal_layout_3)

        self.text_edit_tags = QLineEdit()
        self.text_edit_tags.setPlaceholderText("Теги (разделяйте пробелами)")
        self.text_edit_layout.addWidget(self.text_edit_tags)

        self.right_splitter.addWidget(self.text_edit_widget)

    def show_video_player(self, show):
        # Показ или скрытие медиа-виджетов в зависимости от типа файла
        if self.current_path is None:
            self.video_player.setVisible(False)
            self.image_label.setVisible(False)
            self.text_view.setVisible(False)
        else:
            is_video = self.current_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov'))
            is_image = self.current_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))
            is_text = self.current_path.lower().endswith(('.txt', '.docx', '.pdf'))
            is_folder = os.path.isdir(self.current_path)

            self.video_player.setVisible(show or is_video)
            self.image_label.setVisible(is_image or is_folder)
            self.text_view.setVisible(is_text)

    def open_folder(self):
        # Открытие диалогового окна для выбора папки и обновление представления
        folder = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder:
            self.model = QFileSystemModel()
            self.model.setRootPath(folder)
            self.tree_view.setModel(self.model)
            self.tree_view.setRootIndex(self.model.index(folder))
            self.status_bar.showMessage(f"Открыта папка: {folder}")
            self.current_folder = folder
            self.data_file = os.path.join(self.current_folder, "data.json")
            self.data = load_data(self.data_file)

            self.create_preview_cache_folder()
            self.update_view()

    def create_preview_cache_folder(self):
        # Создание папки для кэширования превью, если она не существует
        self.preview_cache_folder = os.path.join(self.current_folder, ".preview_cache")
        if not os.path.exists(self.preview_cache_folder):
            os.makedirs(self.preview_cache_folder)

    def on_tree_view_clicked(self, index):
        # Обработчик клика на элементе дерева файлов
        handle_tree_view_clicked(self, index)
        self.current_path = self.model.filePath(index)
        if os.path.isdir(self.current_path):
            self.show_video_player(False)
            self.update_image_label()
        else:
            self.show_video_player(self.current_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')))
            self.update_video_player()

    def on_tree_view_double_clicked(self, index):
        # Обработчик двойного клика на элементе дерева файлов
        handle_tree_view_double_clicked(self, index)

    def open_menu(self, position):
        # Обработчик открытия контекстного меню
        handle_menu(self, position)

    def mark_as_reviewed(self):
        # Обработка отметки файла как просмотренного
        index = self.tree_view.currentIndex()
        if index.isValid():
            path = self.model.filePath(index)
            relative_path = os.path.relpath(path, self.current_folder)
            if relative_path not in self.data:
                self.data[relative_path] = {}
            self.data[relative_path]["reviewed"] = True
            self.tree_view.model().setData(index, QColor(Qt.green), Qt.BackgroundRole)
            save_data(self.data_file, self.data)
            self.update_view()
            self.status_bar.showMessage(f"Файл {relative_path} отмечен как просмотренный")

    def save_changes(self):
        # Сохранение изменений в текущем элементе и запись данных в файл
        self.save_current_item()
        save_data(self.data_file, self.data)
        self.status_bar.showMessage("Изменения сохранены")

    def load_changes(self):
        # Загрузка изменений из файла и обновление представления
        self.data = load_data(self.data_file)
        self.update_view()
        self.status_bar.showMessage("Изменения загружены")

    def update_view(self):
        # Обновление представления дерева файлов
        if self.current_folder:
            index = self.tree_view.rootIndex()
            self.update_view_recursive(index)

    def update_view_recursive(self, parent_index):
        # Рекурсивное обновление представления дерева файлов
        model = self.tree_view.model()
        for row in range(model.rowCount(parent_index)):
            index = model.index(row, 0, parent_index)
            path = model.filePath(index)
            relative_path = os.path.relpath(path, self.current_folder)

            if relative_path in self.data and self.data[relative_path].get("reviewed"):
                model.setData(index, QColor(Qt.green), Qt.BackgroundRole)
            else:
                model.setData(index, QColor(Qt.white), Qt.BackgroundRole)

            if model.isDir(index):
                self.update_view_recursive(index)

    def save_current_item(self):
        # Сохранение текущего элемента (тегов, комментариев и кода)
        if self.current_folder and self.current_path:
            try:
                relative_path = os.path.relpath(self.current_path, self.current_folder)
            except ValueError:
                relative_path = self.current_path
            if relative_path not in self.data:
                self.data[relative_path] = {}
            if "tags" not in self.data[relative_path]:
                self.data[relative_path]["tags"] = {}
            current_time = self.video_player.mediaplayer.get_time() // 1000
            self.data[relative_path]["tags"][current_time] = self.text_edit_tags.text().split()
            self.data[relative_path].update({
                "comment": self.text_edit_comment.toPlainText(),
                "code": self.text_edit_code.toPlainText()
            })

    def save_description(self):
        # Сохранение описания текущей папки
        if self.current_path and os.path.isdir(self.current_path):
            description_path = os.path.join(self.current_path, "readme.txt")
            try:
                with open(description_path, "w", encoding="utf-8") as file:
                    file.write(self.text_edit_descript.toPlainText())
            except IOError as e:
                self.status_bar.showMessage(f"Ошибка сохранения описания: {e}")

    def update_image_label(self):
        # Обновление метки изображения
        if self.current_path and os.path.isdir(self.current_path):
            pixmap = load_image(self.current_path, self.placeholder_image)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)) 

    def eventFilter(self, obj, event):
        # Обработчик события выхода из фокуса для сохранения текущего элемента
        if event.type() == event.FocusOut:
            if obj == self.text_edit_comment or obj == self.text_edit_code:
                self.save_current_item()
        return super().eventFilter(obj, event)

    def resizeEvent(self, event):
        # Обработчик события изменения размера окна
        super().resizeEvent(event)

    def sort_tree_view(self, logical_index):
        # Обработчик сортировки дерева файлов
        header = self.tree_view.header()
        order = header.sortIndicatorOrder()
        self.tree_view.model().sort(logical_index, order)

    def update_video_player(self):
        # Обновление состояния видеоплеера
        if self.current_path and self.current_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            self.video_player.media = self.video_player.instance.media_new(self.current_path)
            self.video_player.mediaplayer.set_media(self.video_player.media)
            self.video_player.media.parse()
            if self.video_player.mediaplayer.play() == -1:
                print("Ошибка при воспроизведении видео")
            self.video_player.playVideo()

            if self.current_path in self.data:
                tags_dict = self.data[self.current_path].get("tags", {})
                if tags_dict:
                    start_time = min(tags_dict.keys()) * 1000
                    self.video_player.mediaplayer.set_time(start_time)
        else:
            self.video_player.mediaplayer.stop()

    def filter_tree_view(self, text):
        # Фильтрация элементов дерева файлов по тексту
        text = text.lower()
        root_index = self.model.index(self.current_folder)
        if not text:
            self.reset_tree_view_visibility(root_index)
        else:
            self.filter_tree_view_recursive(root_index, text)

    def filter_tree_view_recursive(self, index, text):
        # Рекурсивная фильтрация элементов дерева файлов
        model = self.tree_view.model()
        if model.isDir(index):
            dir_name = model.fileName(index).lower()
            has_visible_children = text in dir_name
            for row in range(model.rowCount(index)):
                child_index = model.index(row, 0, index)
                child_visible = self.filter_tree_view_recursive(child_index, text)
                if child_visible:
                    has_visible_children = True

            self.tree_view.setRowHidden(index.row(), index.parent(), not has_visible_children)
            return has_visible_children
        else:
            file_name = model.fileName(index).lower()
            is_visible = text in file_name or self.search_in_tags(model.filePath(index), text)
            self.tree_view.setRowHidden(index.row(), index.parent(), not is_visible)
            return is_visible

    def reset_tree_view_visibility(self, index):
        # Сброс видимости элементов дерева файлов
        model = self.tree_view.model()
        self.tree_view.setRowHidden(index.row(), index.parent(), False)
        if model.isDir(index):
            for row in range(model.rowCount(index)):
                child_index = model.index(row, 0, index)
                self.reset_tree_view_visibility(child_index)

    def change_theme(self, index):
        # Смена темы интерфейса
        if index == 0:
            self.setStyleSheet("")
        elif index == 1:
            self.setStyleSheet("background-color: #2b2b2b; color: white;")

    def search_in_tags(self, path, text):
        # Поиск в тегах
        relative_path = os.path.relpath(path, self.current_folder)
        if relative_path in self.data:
            tags = self.data[relative_path].get("tags", {})
            for time, tag_list in tags.items():
                if text in tag_list:
                    return True
        return False

    def update_tags_display(self):
        # Обновление отображения тегов
        if self.current_folder and self.current_path:
            try:
                relative_path = os.path.relpath(self.current_path, self.current_folder)
            except ValueError:
                relative_path = self.current_path
            current_time = self.video_player.mediaplayer.get_time() // 1000
            tags = self.data[relative_path]["tags"].get(current_time, [])
            self.text_edit_tags.setText(" ".join(tags))
