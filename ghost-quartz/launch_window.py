import PySimpleGUIQt as SimpleGUI
import fitz
import tarfile
from PIL import Image, ImageQt
import logging
from copy import deepcopy
# import io, gzip, os


def get_image():
    # Extract .pdf from archive into memory, then display .pdf from memory stream.
    with open("test.tar.gz", "rb") as inpf:
        y = tarfile.open(mode="r:gz", fileobj=inpf)
        file = y.extractfile(member="test.pdf").read()
        doc = fitz.open(filename=None, stream=file, filetype="pdf")
        page = doc[0]
        pix = page.getPixmap()
        mode = "RGBA" if pix.alpha else "RGB"
        img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
        qtimg = ImageQt.ImageQt(img)
        return qtimg


class LaunchWindow(SimpleGUI.Window):
    # Window configuration
    __title = "Ghost Quartz (EXPERIMENTAL)"
    __menu = [["File", ["Open", "Refresh", "Quit"]],
              ["Edit", ["Seek page", "Rewind page", "First Page", "Last Page", "Settings"]],
              ["View", ["Full screen"]],
              ["Help", ["Reference", ["Offline Documentation", "Online Documentation"], "About"]],
              ]
    __resizable = True
    __size = (800, 600)
    __image = get_image()
    __frame_y_layout = [[SimpleGUI.T("File view goes here.")],
                        ]
    __frame_z_layout = [[SimpleGUI.T("Table of Contents goes here.")],
                        ]
    __left_column = [[SimpleGUI.Frame("", __frame_y_layout, background_color="#555")],
                     [SimpleGUI.HorizontalSeparator()],
                     [SimpleGUI.Frame("", __frame_z_layout, background_color="#555")],
                     ]
    __file_browse = SimpleGUI.FileBrowse("A'", target="__file__", enable_events=True)
    # Using Button instead of ButtonImage as placeholders.
    # A - Sidebar toggle, A' - Open file, B - Refresh, C - Rewind, D - Seek, E - Stretch by Width, D - Stretch by Screen
    # G1 - Compress .pdf, G2 - Extract .pdf, G3 - Wildcard compress .pdf singly, G4 - Wildcard extract .pdf singly,
    # G5 - Change archive container of .pdf
    __layout = [[SimpleGUI.Menu(__menu, tearoff=True)],
                [SimpleGUI.Button("A"), __file_browse,
                 SimpleGUI.In(key="__file__", enable_events=True, disabled=True),
                 SimpleGUI.Button("B"), SimpleGUI.Button("C"),
                 SimpleGUI.Button("D"), SimpleGUI.Button("E"), SimpleGUI.VerticalSeparator(),
                 SimpleGUI.Button("G1"), SimpleGUI.Button("G2"), SimpleGUI.Button("G3"),
                 SimpleGUI.Button("G4"), SimpleGUI.Button("G5")],
                [SimpleGUI.Column(__left_column), SimpleGUI.Image(filename=__image, key="__display__")],
                ]

    def __init__(self, title=__title, resizable=__resizable, size=__size, layout=__layout):
        super().__init__(title=title, resizable=resizable, size=size, layout=layout)

    def open_file_browse(self):
        self.__file_browse.Click()

    def open_file(self, fpath):
        try:
            with open(fpath, "rb") as f_inp:
                f_tar = tarfile.open(mode="r:gz", fileobj=f_inp)
                file = f_tar.extractfile(member="test.pdf").read()
                doc = fitz.open(filename=None, stream=file, filetype="pdf")
                page = doc[1]
                pix = page.getPixmap()
                mode = "RGBA" if pix.alpha else "RGB"
                img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                qtimg = ImageQt.ImageQt(img)
                print(qtimg)
                self.FindElement("__display__").Update(filename=qtimg)
                return len(doc), 0
        except Exception as e:
            logging.error("Exception occurred.")
            logging.error(f"{e}")
            return False

    def seek_page(self, doc_pages, current_page, fpath):
        try:
            with open(fpath, "rb") as f_inp:
                current_page += 1
                f_tar = tarfile.open(mode="r:gz", fileobj=f_inp)
                file = f_tar.extractfile(member="test.pdf").read()
                doc = fitz.open(filename=None, stream=file, filetype="pdf")
                page = doc[current_page]
                logging.debug(f"{page}, current_page:{current_page}")
                pix = page.getPixmap()
                mode = "RGBA" if pix.alpha else "RGB"
                img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
                qtimg = ImageQt.ImageQt(img)
                print(qtimg)
                self.FindElement("__display__").Update(filename=qtimg)
                return len(doc), current_page
        except Exception as e:
            logging.error("Exception occurred.")
            logging.error(f"{e}")
            return False
