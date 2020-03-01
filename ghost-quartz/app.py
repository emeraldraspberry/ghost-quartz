# import fitz
import PySimpleGUIQt as sg
# from PIL import Image, ImageQt
from launch_window import LaunchWindow
from pdf_handler import PdfHandler
import logging
import sys
import faulthandler

# Logging setup
logging.basicConfig(level=logging.DEBUG)


def app():
    # Trace debugger
    faulthandler.enable()
    # Launch GUI
    win = LaunchWindow().Finalize()
    pdfhandler = PdfHandler(win)
    is_opened = False
    while True:
        # Event handling
        event, values = win.Read()
        # User exits program
        if event is None or event == "Exit" or event == "Quit":
            break
        # Open file
        if event == "Open":
            win.open_file_browse()
        if event == "__file__" and values["__file__"] is not None:
            print("prepare for opening")
            pdfhandler.set_file_path(values["__file__"])
            pdfhandler.open_file()
            is_opened = True
        if event == "C" and is_opened is not False:
            pdfhandler.rewind_page()
        if event == "D" and is_opened is not False:
            pdfhandler.seek_page()

        logging.debug(f"Event:{event} , Values:{values}")
        # win.Finalize()
    win.Close()
    del win
    return


if __name__ == "__main__":
    app()
