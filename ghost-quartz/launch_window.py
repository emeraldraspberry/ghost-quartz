#import PySimpleGUIQt as SimpleGUI
import PySimpleGUI as SimpleGUI
import logging


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
    __frame_y_layout = [[SimpleGUI.T("File view goes here.")],
                        ]
    __frame_z_layout = [[SimpleGUI.T("Table of Contents goes here.")],
                        ]
    __left_column = [[SimpleGUI.Frame("", __frame_y_layout, background_color="#555")],
                     [SimpleGUI.Frame("", __frame_z_layout, background_color="#555")],
                     ]
    __right_column = [[SimpleGUI.Image(filename=None, key="__display__", pad=(0, 0))]
                      ]
    __file_browse = SimpleGUI.FileBrowse("A'", target="__file__", enable_events=True)
    __image_size = (0, 0)
    # Using Button instead of ButtonImage as placeholders. Functionality not final.
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
                [SimpleGUI.Column(__left_column),
                 SimpleGUI.Column(layout=__right_column, key="__display_wrapper__",
                                  background_color="#555"),
                 ]
                ]

    def __init__(self, title=__title, resizable=__resizable, size=__size, layout=__layout):
        super().__init__(title=title, resizable=resizable, size=size, layout=layout)

    def open_file_browse(self):
        self.__file_browse.Click()
