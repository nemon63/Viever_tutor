from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from video_player import VideoPlayer

class MediaWidgets(QWidget):
    def __init__(self, main_window):
        """
        Инициализация медиа-виджетов.

        Args:
            main_window (QMainWindow): Основное окно приложения.
        """
        super().__init__()
        self.main_window = main_window

        # Создание основного макета
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Инициализация видеоплеера
        self.video_player = VideoPlayer(self.main_window)
        self.video_player.setMinimumSize(800, 600)
        self.layout.addWidget(self.video_player)

        # Инициализация метки для отображения изображений
        self.image_label = QLabel("image")
        self.image_label.setFrameShape(QLabel.Panel)
        self.image_label.setFrameShadow(QLabel.Plain)
        self.image_label.setLineWidth(1)
        self.image_label.setMidLineWidth(1)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(800, 600)
        self.image_label.setScaledContents(False)  # Измените на False, чтобы сохранить пропорции изображения
        self.layout.addWidget(self.image_label)
