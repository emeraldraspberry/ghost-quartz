# import fitz
# import PySimpleGUIQt as sg
# from PIL import Image, ImageQt
from launch_window import LaunchWindow
import logging

# Logging setup
logging.basicConfig(level=logging.DEBUG)


def app():
    doc = None
    # Launch GUI
    win = LaunchWindow().Finalize()
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
            (doc_pages, current_page) = win.open_file(fpath=values["__file__"])
            logging.debug(f"{doc_pages}, {current_page}")
        if event == "D" and current_page is not None:
            (doc_pages, current_page) = win.seek_page(doc_pages, current_page, fpath=values["__file__"])

        logging.debug(f"Event:{event} , Values:{values}")
    win.Close()
    del win


if __name__ == "__main__":
    app()
