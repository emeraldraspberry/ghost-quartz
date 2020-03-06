import json
import logging

from copy import copy, deepcopy


class Bookmark:

    def __init__(self):
        self.id = 0

        try:
            with open("./res/data.json") as file:
                self.bookmarks = json.load(file)
                self.id = len(self.bookmarks.get("bookmarks"))
                return
        except Exception as e:
            logging.error(f"Exception occurred with loading bookmarks.")
            logging.error(f"{e}")

        # Create a dictionary list of dictionaries
        self.bookmarks = {"bookmarks": []}

    def add_bookmark(self, book_name, page_number, hash, file_path, name="happy_little_bookmark"):
        bookmark = {}
        bookmark.update({"id": self.id})
        bookmark.update({"name": name})
        bookmark.update({"file_path": file_path})
        bookmark.update({"hash": hash})
        bookmark.update({"book_name": book_name})
        bookmark.update({"page_number": page_number})

        # Append bookmark to list.
        self.bookmarks.get("bookmarks").append(copy(bookmark))
        self.id += 1
        for key, value in self.bookmarks.items():
            logging.debug(f"{key}, {value}")

        with open("./res/data.json", "w") as file:
            json.dump(self.bookmarks, file, indent=1)

