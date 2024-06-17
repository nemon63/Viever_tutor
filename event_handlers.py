import os
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import QMenu, QFileDialog
from PyQt5.QtCore import QDir, Qt
from file_operations import load_image, load_description, load_text_file, load_docx_file, load_pdf_file

def handle_tree_view_clicked(main_window, index):
    """
    Обработчик клика по элементу дерева файлов.
    Сохраняет текущий элемент, обновляет статус и отображает выбранный файл или папку.

    Args:
        main_window (QMainWindow): Основное окно приложения.
        index (QModelIndex): Индекс выбранного элемента.
    """
    main_window.save_current_item()
    path = main_window.model.filePath(index)
    main_window.status_bar.showMessage(f"Выбрано: {path}")
    main_window.current_path = path

    if os.path.isfile(path):
        if path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            main_window.update_video_player()
            main_window.image_label.setVisible(False)
        else:
            handle_file_display(main_window, path)
    else:
        handle_folder_display(main_window, path)

    update_current_item_data(main_window, path)

def handle_tree_view_double_clicked(main_window, index):
    """
    Обработчик двойного клика по элементу дерева файлов.
    Открывает файл или папку.

    Args:
        main_window (QMainWindow): Основное окно приложения.
        index (QModelIndex): Индекс выбранного элемента.
    """
    path = main_window.model.filePath(index)
    if os.path.isdir(path):
        os.startfile(path)
    else:
        main_window.status_bar.showMessage(f"Открытие файла: {path}")
        if path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
            os.startfile(path)

def handle_menu(main_window, position):
    """
    Обработчик контекстного меню для дерева файлов.

    Args:
        main_window (QMainWindow): Основное окно приложения.
        position (QPoint): Позиция курсора для отображения меню.
    """
    indexes = main_window.tree_view.selectedIndexes()
    if indexes:
        index = indexes[0]
        path = main_window.model.filePath(index)
        menu = QMenu()

        add_cover_action = menu.addAction("Добавить обложку")
        add_cover_action.triggered.connect(lambda: add_cover(main_window, path))

        add_description_action = menu.addAction("Добавить описание")
        add_description_action.triggered.connect(lambda: add_description(main_window, path))

        menu.exec_(main_window.tree_view.viewport().mapToGlobal(position))

def add_cover(main_window, path):
    """
    Добавление обложки к выбранной папке.

    Args:
        main_window (QMainWindow): Основное окно приложения.
        path (str): Путь к папке.
    """
    file_path, _ = QFileDialog.getOpenFileName(main_window, "Выберите изображение", "", "Images (*.png *.jpg *.jpeg)")
    if file_path:
        cover_path = os.path.join(path, "cover.jpg")
        QDir().mkpath(path)
        with open(file_path, "rb") as fsrc, open(cover_path, "wb") as fdst:
            fdst.write(fsrc.read())
        main_window.status_bar.showMessage(f"Обложка добавлена: {cover_path}")
        handle_tree_view_clicked(main_window, main_window.model.index(path))

def add_description(main_window, path):
    """
    Добавление описания к выбранной папке.

    Args:
        main_window (QMainWindow): Основное окно приложения.
        path (str): Путь к папке.
    """
    description_path = os.path.join(path, "readme.txt")
    if not os.path.exists(description_path):
        with open(description_path, "w", encoding="utf-8") as f:
            f.write("")
    main_window.status_bar.showMessage(f"Описание добавлено: {description_path}")
    handle_tree_view_clicked(main_window, main_window.model.index(path))
    os.startfile(description_path)

def handle_file_display(main_window, path):
    """
    Отображение содержимого файла в основном окне.

    Args:
        main_window (QMainWindow): Основное окно приложения.
        path (str): Путь к файлу.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in ('.jpg', '.jpeg', '.png', '.bmp', '.gif'):
        pixmap = QPixmap(path)
        main_window.image_label.setPixmap(pixmap.scaled(main_window.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        main_window.show_video_player(False)
    elif ext == '.txt':
        try:
            content = load_text_file(path)
            main_window.text_view.setText(content)
        except Exception as e:
            main_window.status_bar.showMessage(f"Ошибка загрузки файла: {e}")
        main_window.show_video_player(False)
    elif ext == '.docx':
        content = load_docx_file(path)
        main_window.text_view.setText(content)
        main_window.show_video_player(False)
    elif ext == '.pdf':
        content = load_pdf_file(path)
        main_window.text_view.setText(content)
        main_window.show_video_player(False)
    else:
        main_window.text_view.setText("")
        main_window.show_video_player(False)

def handle_folder_display(main_window, path):
    """
    Отображение содержимого папки в основном окне.

    Args:
        main_window (QMainWindow): Основное окно приложения.
        path (str): Путь к папке.
    """
    main_window.video_player.mediaplayer.stop()
    pixmap = load_image(path, main_window.placeholder_image)
    main_window.image_label.setPixmap(pixmap.scaled(main_window.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
    description = load_description(path)
    main_window.text_edit_descript.setText(description)
    main_window.show_video_player(False)

def update_current_item_data(main_window, path):
    """
    Обновление данных текущего элемента (теги, комментарии, код).

    Args:
        main_window (QMainWindow): Основное окно приложения.
        path (str): Путь к текущему элементу.
    """
    try:
        relative_path = os.path.relpath(path, main_window.current_folder)
    except ValueError:
        relative_path = path

    if relative_path not in main_window.data:
        main_window.data[relative_path] = {}
    if "tags" not in main_window.data[relative_path]:
        main_window.data[relative_path]["tags"] = {}
    if isinstance(main_window.data[relative_path]["tags"], list):
        main_window.data[relative_path]["tags"] = {}
    if "comment" not in main_window.data[relative_path]:
        main_window.data[relative_path]["comment"] = ""
    if "code" not in main_window.data[relative_path]:
        main_window.data[relative_path]["code"] = ""

    main_window.text_edit_comment.setText(main_window.data[relative_path]["comment"])
    main_window.text_edit_code.setText(main_window.data[relative_path]["code"])

    current_time = main_window.video_player.mediaplayer.get_time() // 1000
    tags = main_window.data[relative_path]["tags"].get(current_time, [])
    main_window.text_edit_tags.setText(" ".join(tags))

    index = main_window.tree_view.currentIndex()
    if main_window.data[relative_path].get("reviewed"):
        main_window.tree_view.model().setData(index, QColor(Qt.green), Qt.BackgroundRole)
    else:
        main_window.tree_view.model().setData(index, QColor(Qt.white), Qt.BackgroundRole)
