import tarfile
import fitz
from PIL import Image, ImageTk
import logging
import filetype

from zipfile import ZipFile


class PdfHandler:
    def __init__(self, launch_window, file_path=None):
        self.launch_window = launch_window
        self.file_path = file_path
        self.pdf_len = None
        self.pdf_page_num = 0
        self.pdf_width = 0
        self.pdf_height = 0
        self.scale_factor = 1

    def set_file_path(self, file_path):
        if self.file_path == file_path:
            return
        self.file_path = file_path
        self.pdf_page_num = 0

    def update_image(self, document):
        logging.debug(f"type:{type(document)}")
        page = document[self.pdf_page_num]
        logging.debug(f"page:{page}")
        org_mat = fitz.Matrix(1, 1)
        mat = fitz.Matrix(self.scale_factor, self.scale_factor)
        org_pix = page.getPixmap(matrix=org_mat)
        pix = page.getPixmap(matrix=mat)
        self.pdf_width = org_pix.width
        self.pdf_height = org_pix.height
        logging.debug(f".pdf original size:({self.pdf_width},{self.pdf_height})")
        pix_mode = "RGBA" if pix.alpha else "RGB"
        img = Image.frombytes(pix_mode, [pix.width, pix.height], pix.samples)
        # PySimpleGuiQt implementation
        # Not used due to segmentation fault problems with Qt.
        # qtimg = ImageQt.ImageQt(img)
        # self.launch_window.FindElement("__display__").Update(filename=qtimg)
        # logging.debug(f"Updated __display with {qtimg}")

        # PySimpleGui TK implementation
        tkimg = ImageTk.PhotoImage(img)
        self.launch_window.FindElement("__display__").Update(data=tkimg)
        logging.debug(f"Updated __display with {tkimg}")
        self.pdf_len = len(document)
        document.close()

    def open_archive(self, mode):
        with open(self.file_path, "rb") as f_inp:
            tar = tarfile.open(mode=mode, fileobj=f_inp)
            file = tar.getnames()
            file_count = len(file)
            logging.debug(f"Tar members:{file}, Tar amount:{file_count}")
            if file_count == 1:
                logging.debug(f"Extracting {file[0]}")
                pdf = tar.extractfile(member=file[0]).read()
                pdf_doc = fitz.open(filename=None, stream=pdf, filetype="pdf")
                self.update_image(pdf_doc)

    def open_pdf(self):
        pdf_doc = fitz.open(filename=self.file_path)
        self.update_image(pdf_doc)

    def open_gz(self):
        self.open_archive(mode="r:gz")

    def open_bz2(self):
        self.open_archive(mode="r:bz2")

    def open_xz(self):
        self.open_archive(mode="r:xz")

    def open_zip(self):
        with ZipFile(self.file_path, "r") as zip_file:
            list = zip_file.namelist()
            file_count = len(list)
            logging.debug(f"Zip members:{list}, Zip amount:{file_count}")
            if file_count == 1:
                logging.debug(f"Extracting {list[0]}")
                pdf = zip_file.read(name=list[0])
                pdf_doc = fitz.open(filename=None, stream=pdf, filetype="pdf")
                self.update_image(pdf_doc)

    def open_7z(self):
        return

    def open_file(self):
        try:
            kind = filetype.guess(self.file_path)
            if kind.EXTENSION == "pdf":
                logging.debug("Opening pdf format...")
                self.open_pdf()
                return
            elif kind.EXTENSION == "gz":
                logging.debug("Opening gz format...")
                self.open_gz()
                return
            elif kind.EXTENSION == "bz2":
                logging.debug("Opening bz2 format...")
                self.open_bz2()
                return
            elif kind.EXTENSION == "xz":
                logging.debug("Opening xz format...")
                self.open_xz()
                return
            elif kind.EXTENSION == "7z":
                logging.debug("Opening 7z format...")
                self.open_7z()
                return
            elif kind.EXTENSION == "zip":
                logging.debug("Opening zip format...")
                self.open_zip()
                return
        except Exception as e:
            logging.error("Exception occurred.")
            logging.error(f"{e}")
            return False

    def rewind_page(self):
        if self.pdf_page_num == 0:
            return
        self.pdf_page_num -= 1
        self.open_file()

    def seek_page(self):
        if self.pdf_page_num >= self.pdf_len - 1:
            return
        self.pdf_page_num += 1
        self.open_file()

    def stretch_by_width(self):
        win_size = self.launch_window.size
        wrap_size = int(0.75 * win_size[0])
        self.scale_factor = wrap_size / self.pdf_width
        self.open_file()
