from PyQt5 import (QtWidgets, QtCore, QtGui)
from pdf_handler import PdfHandler
from bookmark import Bookmark
import os
import logging
from copy import deepcopy, copy

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        _window_title = "Ghost Quartz (EXPERIMENTAL)"
        _size_x, _size_y = 800, 600
        _icon_x, _icon_y = 16, 16

        self.pdf_handler = PdfHandler(self)
        self.bookmark = Bookmark()
        self.n = 0

        self.setWindowTitle(_window_title)
        self.resize(_size_x, _size_y)
        self.center_window()
        self.setStatusBar(QtWidgets.QStatusBar(self))

        menu = self.menuBar()

        # Define layout of obj(menuBar)
        # File menu
        self.define_file_menu(menu)
        # Edit menu
        self.define_edit_menu(menu)
        # View menu
        self.define_view_menu(menu)
        # Bookmark menu
        self.define_bookmark_menu(menu)
        # Help menu
        self.define_help_menu(menu)

        # Define layout of obj(QToolBar)
        toolbar = self.define_toolbar(_icon_x, _icon_y)
        self.define_toolbar_buttons(toolbar)

        # Layout widgets
        layout_label = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel()
        self.label.setBackgroundRole(QtGui.QPalette.Base)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.label.setScaledContents(True)

        layout_label.addWidget(self.label)
        layout_label.setContentsMargins(0, 0, 0, 0)
        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(layout_label)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setBackgroundRole(QtGui.QPalette.Dark)
        scroll_area.setWidget(self.widget)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setSizeAdjustPolicy(QtWidgets.QScrollArea.AdjustToContents)
        self.setCentralWidget(scroll_area)

        # Required since PyQt5 sets windows hidden by default.
        self.show()

    def define_toolbar_buttons(self, toolbar):

        # Sidebar button
        button_sidebar = QtWidgets.QAction(QtGui.QIcon("./res/icons/application-sidebar.png"), "Toggle side bar", self)
        button_sidebar.setStatusTip("Toggle side bar")
        # button_sidebar.triggered.connect()
        toolbar.addAction(button_sidebar)

        # Open file button
        button_open_file = QtWidgets.QAction(QtGui.QIcon("./res/icons/blue-folder-open-document.png"), "Open file",
                                             self)
        button_open_file.setStatusTip("Open file")
        button_open_file.triggered.connect(self.open_file_dialog)
        toolbar.addAction(button_open_file)

        # Refresh button
        button_refresh = QtWidgets.QAction(QtGui.QIcon("./res/icons/arrow-circle-045-left.png"), "Refresh", self)
        button_refresh.setStatusTip("Refresh")
        toolbar.addAction(button_refresh)

        # Rewind page button
        button_rewind = QtWidgets.QAction(QtGui.QIcon("./res/icons/control-double-180.png"), "Rewind page", self)
        button_rewind.setStatusTip("Rewind page")
        button_rewind_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+PgUp"), self)
        button_rewind_shortcut.activated.connect(self.pdf_handler.rewind_page)
        button_rewind.triggered.connect(self.pdf_handler.rewind_page)
        toolbar.addAction(button_rewind)

        # Seek page button
        button_seek = QtWidgets.QAction(QtGui.QIcon("./res/icons/control-double.png"), "Seek page", self)
        button_seek.setStatusTip("Seek page")
        button_seek_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+PgDown"), self)
        button_seek_shortcut.activated.connect(self.pdf_handler.seek_page)
        button_seek.triggered.connect(self.pdf_handler.seek_page)
        toolbar.addAction(button_seek)

        # Stretch page by width button
        button_stretch_to_width = QtWidgets.QAction(QtGui.QIcon("./res/icons/arrow-resize.png"),
                                                    "Stretch page by width", self)
        button_stretch_to_width.setStatusTip("Stretch page by width")
        button_stretch_to_width.triggered.connect(self.pdf_handler.stretch_by_width)
        toolbar.addAction(button_stretch_to_width)

        # Stretch page by screen button
        button_stretch_to_screen = QtWidgets.QAction(QtGui.QIcon("./res/icons/document-resize.png"),
                                                     "Stretch page by screen", self)
        button_stretch_to_screen.setStatusTip("Stretch page by screen")
        toolbar.addAction(button_stretch_to_screen)
        toolbar.addSeparator()

        # Compress pdf button
        button_compress_pdf = QtWidgets.QAction(QtGui.QIcon("./res/icons/document-zipper.png"), "Compress pdf", self)
        button_compress_pdf.setStatusTip("Compress pdf")
        toolbar.addAction(button_compress_pdf)

        # Extract pdf button
        button_extract_pdf = QtWidgets.QAction(QtGui.QIcon("./res/icons/document-import.png"), "Extract pdf", self)
        button_extract_pdf.setStatusTip("Extract pdf")
        toolbar.addAction(button_extract_pdf)

        # Wildcard compress pdf singly button
        button_wildcard_compress_pdf = QtWidgets.QAction(QtGui.QIcon("./res/icons/blue-folder-zipper.png"),
                                                         "Wildcard compress pdf", self)
        button_wildcard_compress_pdf.setStatusTip("Wildcard compress pdf")
        toolbar.addAction(button_wildcard_compress_pdf)

        # Wildcard extract pdf singly button
        button_wildcard_extract_pdf = QtWidgets.QAction(QtGui.QIcon("./res/icons/blue-folder-import.png"),
                                                        "Wildcard extract pdf", self)
        button_wildcard_extract_pdf.setStatusTip("Wildcard extract pdf")
        toolbar.addAction(button_wildcard_extract_pdf)

        # Change archive container of pdf button
        button_change_archive = QtWidgets.QAction(QtGui.QIcon("./res/icons/wand-magic.png"), "Change archive", self)
        button_change_archive.setStatusTip("Change archive")
        toolbar.addAction(button_change_archive)

    def define_toolbar(self, _icon_x, _icon_y):
        toolbar = QtWidgets.QToolBar("My Toolbar")
        toolbar.setIconSize(QtCore.QSize(_icon_x, _icon_y))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        return toolbar

    def define_help_menu(self, menu):
        help_menu = menu.addMenu("&Help")
        help_reference = QtWidgets.QAction("Reference", self)
        help_about = QtWidgets.QAction("About", self)
        help_menu.addAction(help_reference)
        help_menu.addAction(help_about)

    def define_view_menu(self, menu):
        view_menu = menu.addMenu("&View")
        view_full_screen = QtWidgets.QAction("Full screen", self)
        view_menu.addAction(view_full_screen)

    def define_edit_menu(self, menu):
        edit_menu = menu.addMenu("&Edit")
        edit_seek = QtWidgets.QAction("Seek page", self)
        edit_rewind = QtWidgets.QAction("Rewind page", self)
        edit_first = QtWidgets.QAction("First page", self)
        edit_last = QtWidgets.QAction("Last page", self)
        edit_settings = QtWidgets.QAction("Settings", self)
        edit_menu.addAction(edit_seek)
        edit_menu.addAction(edit_rewind)
        edit_menu.addAction(edit_first)
        edit_menu.addAction(edit_last)
        edit_menu.addAction(edit_settings)

    def define_file_menu(self, menu):
        file_menu = menu.addMenu("&File")
        file_open = QtWidgets.QAction("Open", self)
        file_open.triggered.connect(self.open_file_dialog)
        file_refresh = QtWidgets.QAction("Refresh", self)
        file_exit = QtWidgets.QAction("Exit", self)
        file_menu.addAction(file_open)
        file_menu.addAction(file_refresh)
        file_menu.addAction(file_exit)

    def center_window(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget.availableGeometry(QtWidgets.QDesktopWidget()).center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def open_file_dialog(self):
        logging.debug(f"Opening file...")
        dialog = QtWidgets.QFileDialog()
        dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        # dialog.setNameFilter("*.pdf")
        # dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)

        if dialog.exec_():
            # filename = dialog.getOpenFileName(self, "Open PDF", "/home/emeraspe", "PDF Files (*.pdf)")
            file_path = dialog.selectedFiles()
            self.pdf_handler.set_file_path(file_path[0])
            self.pdf_handler.open_file()

            return

    def define_bookmark_menu(self, menu):
        bookmark_menu = menu.addMenu("&Bookmark")
        bookmark_add_bookmark = QtWidgets.QAction("Add bookmark", self)
        bookmark_add_bookmark.triggered.connect(
            lambda: self.bookmark.add_bookmark(self.pdf_handler.pdf_name, hash=self.pdf_handler.hash,
                                               page_number=self.pdf_handler.pdf_page_num,
                                               file_path=self.pdf_handler.file_path))
        bookmark_menu.addAction(bookmark_add_bookmark)

        bookmark_menu.addSeparator()
        bookmark_show_bookmarks = bookmark_menu.addMenu("Show bookmarks")

        bookmarks = self.bookmark.bookmarks.get("bookmarks")

        # O(n^2), find another efficient way.
        i = 0
        for bookmark in bookmarks:
            for key, value in bookmark.items():
                if key == "name":
                    txt = value
                    txt += ", " + str(os.path.basename(bookmarks[i]["file_path"]))
                    txt += ", " + str(bookmarks[i]["page_number"])
                    action = QtWidgets.QAction(txt, self)
                    action.triggered.connect(lambda connected, n=i: self.open_file_bookmark(bookmarks[n]["file_path"],
                                                                                            bookmarks[n]["page_number"]))
                    bookmark_show_bookmarks.addAction(action)
            print(i)
            print(bookmarks[i]["file_path"])
            i += 1

    def open_file_bookmark(self, file_path, page_number):
        self.pdf_handler.pdf_page_num = page_number
        self.pdf_handler.file_path = file_path
        self.pdf_handler.open_file()
