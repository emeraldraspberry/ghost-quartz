import tarfile
import fitz
from PIL import Image, ImageQt
import logging
import filetype
import hashlib

from zipfile import ZipFile


class PdfHandler:
    def __init__(self, window, file_path=None):
        self.window = window
        self.file_path = file_path
        self.pdf_len = None
        self.pdf_page_num = 0
        self.pdf_name = None
        self.hash = None
        self.pdf_width = 0
        self.pdf_height = 0
        self.scale_factor = 1

    def set_file_path(self, file_path):
        if self.file_path == file_path:
            return
        self.file_path = file_path
        self.pdf_page_num = 0

    # TODO
    # Refactor this big long method.
    def update_image(self, document):
        print(self.pdf_page_num)
        try:
            self.pdf_name = document.metadata["title"]
        except Exception as e:
            logging.error(f"Exception occurred with {self.file_path}.")
            logging.error(f"{e}")
            return False
        logging.debug(f"type:{type(document)}")
        page = document[self.pdf_page_num]
        logging.debug(f"page:{page}")
        org_mat = fitz.Matrix(1, 1)
        # mat = fitz.Matrix(self.scale_factor, self.scale_factor)
        org_pix = page.getPixmap(matrix=org_mat)
        # pix = page.getPixmap(matrix=mat)
        self.pdf_width = org_pix.width
        self.pdf_height = org_pix.height

        size = self.window.widget.size().width()
        wrap_size = int(size)
        self.scale_factor = wrap_size / self.pdf_width
        mat = fitz.Matrix(self.scale_factor, self.scale_factor)
        pix = page.getPixmap(matrix=mat)
        logging.debug(f".pdf original size:({self.pdf_width},{self.pdf_height})")
        pix_mode = "RGBA" if pix.alpha else "RGB"
        img = Image.frombytes(pix_mode, [pix.width, pix.height], pix.samples)
        # qtimg = ImageQt.ImageQt(img)
        self.window.label.setPixmap(ImageQt.toqpixmap(img))
        self.window.label.update()
        logging.debug(f"Updated label with {img}")

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
                self.generate_hash(pdf)
                pdf_doc = fitz.open(filename=None, stream=pdf, filetype="pdf")
                self.update_image(pdf_doc)

    def open_pdf(self):
        with open(self.file_path, "rb") as file:
            data = file.read()
            self.hash = hashlib.md5(data).hexdigest()
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
            zip_list = zip_file.namelist()
            file_count = len(zip_list)
            logging.debug(f"Zip members:{zip_list}, Zip amount:{file_count}")
            if file_count == 1:
                logging.debug(f"Extracting {zip_list[0]}")
                self.generate_hash(zip_list[0])
                pdf = zip_file.read(name=zip_list[0])
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
            logging.error(f"Exception occurred with {self.file_path}.")
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
        size = self.window.widget.size().width()
        wrap_size = int(size)
        self.scale_factor = wrap_size / self.pdf_width
        self.open_file()

    def generate_hash(self, pdf):
        md5 = hashlib.md5(pdf).hexdigest()
        self.hash = md5
