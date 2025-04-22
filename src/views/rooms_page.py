from PyQt6.QtWidgets import QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QIcon, QFontDatabase, QFont
from PyQt6.QtCore import QSize

from custom_widgets import ListRoomsFrame, GridRoomsFrame

from ui.rooms_page_ui import Ui_Widget as RoomsPageUI


class RoomsPage(QWidget, RoomsPageUI):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.max_list_rooms_frame = 0
        self.max_grid_rooms_frame = 0

        self.rooms_view_stacked_widget.setCurrentWidget(self.list_view_widget)

        self.add_signals()

        self.set_external_stylesheet()

        self.load_fonts()

        self.set_icons()

    def add_signals(self):
        self.grid_view_button.clicked.connect(self.switch_to_grid_view)
        self.list_view_button.clicked.connect(self.switch_to_list_view)

    def switch_to_list_view(self):
        self.rooms_view_stacked_widget.setCurrentWidget(self.list_view_widget)
        self.make_list_view_rooms_frame()

    def switch_to_grid_view(self):
        self.rooms_view_stacked_widget.setCurrentWidget(self.grid_view_widget)
        self.make_grid_view_rooms_frame()

    def make_list_view_rooms_frame(self):

        list_rooms_frame_min_height = 90

        new_max_list_rooms_frame = self.list_view_contents_frame.height() // list_rooms_frame_min_height

        if new_max_list_rooms_frame < self.max_list_rooms_frame:
            self.clear_list_view_frames(new_max_list_rooms_frame)

        elif new_max_list_rooms_frame > self.max_list_rooms_frame:
            for i in range(new_max_list_rooms_frame):
                item = self.list_view_grid_layout.itemAtPosition(i, 1)

                if item is None:
                    self.list_view_grid_layout.addWidget(ListRoomsFrame({"room_type": "single"}), i, 1, 1, 1)
                elif isinstance(item, QSpacerItem):
                    self.list_view_grid_layout.removeItem(item)
                    self.list_view_grid_layout.addWidget(ListRoomsFrame({"room_type": "single"}), i, 1, 1, 1)

        if new_max_list_rooms_frame != self.max_list_rooms_frame:
            self.max_list_rooms_frame = new_max_list_rooms_frame

            vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.list_view_grid_layout.addItem(vertical_spacer, self.max_list_rooms_frame, 1, 1, 1)

        # print("Elements in list view grid layout: " + str(self.list_view_grid_layout.count()))

    def clear_list_view_frames(self, new_max_list_rooms_frame):
        for i in reversed(range(new_max_list_rooms_frame,self.list_view_grid_layout.count())):

            # Removes the item from the grid layout, while returning the item
            item = self.list_view_grid_layout.takeAt(i)

            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

            # If item is a QSpacerItem, Python's GC will collect item, since it has no more reference

    def make_grid_view_rooms_frame(self):
        grid_rooms_frame_min_width = 320
        grid_rooms_frame_min_height = 250

        new_max_grid_rooms_frame_rows = self.grid_view_widget.height() // grid_rooms_frame_min_height
        new_max_grid_rooms_frame_columns = self.grid_view_widget.width() // grid_rooms_frame_min_width

        new_max_grid_rooms_frame = new_max_grid_rooms_frame_columns * new_max_grid_rooms_frame_rows

        if new_max_grid_rooms_frame < self.max_grid_rooms_frame:
            self.clear_grid_view_frames(new_max_grid_rooms_frame_columns, new_max_grid_rooms_frame_rows)

        elif new_max_grid_rooms_frame > self.max_grid_rooms_frame:
            for row in range(new_max_grid_rooms_frame_rows):
                for column in range(new_max_grid_rooms_frame_columns):
                    item = self.grid_view_grid_layout.itemAtPosition(row, column)

                    if item is None:
                        self.grid_view_grid_layout.addWidget(GridRoomsFrame({"room_type": "single"}), row, column, 1, 1)

        if new_max_grid_rooms_frame != self.max_grid_rooms_frame:
            self.max_grid_rooms_frame = new_max_grid_rooms_frame

        # print("Elements in grid view grid layout 20: " + str(self.grid_view_grid_layout.count()))

    def clear_grid_view_frames(self, new_max_grid_rooms_frame_columns, new_max_grid_rooms_frame_rows):

        max_row, max_column = self.get_current_rows_and_columns_in_grid_layout("grid_view")

        if new_max_grid_rooms_frame_columns != max_column:
            # Remove rightmost frames

            # Traverse starting from the rightmost column to the left, until value of new_max_grid_rooms_frame_columns
            for column in reversed(range(new_max_grid_rooms_frame_columns, max_column)):
                # Then traverse from the first row until the last row
                for row in range(max_row):

                    item = self.grid_view_grid_layout.itemAtPosition(row, column)
                    if item:
                        widget = item.widget()
                        if widget:
                            widget.setParent(None)
                            widget.deleteLater()
                        else:
                            self.grid_view_grid_layout.removeItem(item)
                            break

        if new_max_grid_rooms_frame_rows != max_row:
            # Remove bottom frames

            # Traverse starting from the bottommost column to the top, until value of new_max_grid_rooms_frame_rows
            for row in reversed(range(new_max_grid_rooms_frame_rows, max_row)):
                # Then traverse from the first column until the last column
                for column in range(max_column):

                    item = self.grid_view_grid_layout.itemAtPosition(row, column)
                    if item:
                        widget = item.widget()
                        if widget:
                            widget.setParent(None)
                            widget.deleteLater()
                        else:
                            self.grid_view_grid_layout.removeItem(item)
                            break

    def get_current_rows_and_columns_in_grid_layout(self, view_type):

        if view_type == "grid_view":
            current_grid_layout = self.grid_view_grid_layout
        else:
            current_grid_layout = self.list_view_grid_layout

        max_row = 0
        max_column = 0

        for i in range(current_grid_layout.count()):
            row, column, row_span, column_span = current_grid_layout.getItemPosition(i)

            # row + row_span - 1 has -1 because row is zero-indexed
            max_row = max(max_row, row + row_span - 1)
            max_column = max(max_column, column + column_span - 1)

        # Plus one because row is zero-indexed
        return max_row + 1, max_column + 1

    def set_external_stylesheet(self):
        with open("../resources/styles/rooms_page.qss", "r") as file:
            self.setStyleSheet(file.read())

    def set_icons(self):
        self.grid_view_button.setIcon(QIcon("../resources/icons/rooms_page/grid_view_icon.svg"))
        self.grid_view_button.setIconSize(QSize(25, 25))

        self.list_view_button.setIcon(QIcon("../resources/icons/rooms_page/list_view_icon.svg"))
        self.list_view_button.setIconSize(QSize(25, 25))

        self.add_room_button.setIcon(QIcon("../resources/icons/rooms_page/add_icon.svg"))
        self.add_room_button.setIconSize(QSize(20, 20))

    def load_fonts(self):

        self.rooms_label.setFont(QFont("Inter", 20, QFont.Weight.Bold))

        self.unit_room_no_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))
        self.room_type_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))
        self.capacity_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))
        self.rate_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))
        self.status_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))
        self.action_label.setFont(QFont("Inter", 13, QFont.Weight.Normal))

        self.search_lineedit.setFont(QFont("Inter", 16, QFont.Weight.Normal))

        self.room_types_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.room_status_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.add_room_button.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))

    # resizeEvent will be automatically called when switching to rooms page widget, so no need to preload frames
    def resizeEvent(self, event):

        if self.rooms_view_stacked_widget.currentWidget() == self.list_view_widget:
            self.make_list_view_rooms_frame()
        else:
            self.make_grid_view_rooms_frame()

