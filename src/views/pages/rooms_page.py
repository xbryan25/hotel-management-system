from PyQt6.QtWidgets import QWidget, QSpacerItem, QSizePolicy, QFrame
from PyQt6.QtGui import QIcon, QFontDatabase, QFont, QPixmap
from PyQt6.QtCore import QSize, pyqtSignal, Qt, QTimer, QThread

from views.custom_widgets import ListRoomsFrame, GridRoomsFrame

from ui import RoomsPageUI

import math


class RoomsPage(QWidget, RoomsPageUI):

    window_resized = pyqtSignal()
    next_page_button_pressed = pyqtSignal()
    previous_page_button_pressed = pyqtSignal()
    change_view_mode = pyqtSignal(str)
    clicked_add_room_button = pyqtSignal()
    search_text_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.max_list_rooms_frame = 0
        self.max_grid_rooms_frame = 0

        self.previous_width = self.width()
        self.previous_height = self.height()

        self.size_change_threshold = 10

        self.rooms_view_stacked_widget.setCurrentWidget(self.list_view_widget)

        self.add_timer_to_search_lineedit()

        self.connect_signals_to_slots()

        self.set_external_stylesheet()

        self.load_fonts()

        self.set_icons()

        self.image_cache = {}

    def add_timer_to_search_lineedit(self):
        self.timer = QTimer()

        self.timer.setInterval(300)
        self.timer.setSingleShot(True)

    def start_debounce_timer(self):
        self.timer.start()

    def on_debounced_text_changed(self):
        self.search_text_changed.emit(self.search_lineedit.text())

    def connect_signals_to_slots(self):
        self.grid_view_button.clicked.connect(self.switch_to_grid_view)
        self.list_view_button.clicked.connect(self.switch_to_list_view)

        self.next_page_button.clicked.connect(self.next_page_button_pressed.emit)
        self.previous_page_button.clicked.connect(self.previous_page_button_pressed.emit)

        self.add_room_button.clicked.connect(self.clicked_add_room_button.emit)

        self.search_lineedit.textChanged.connect(self.start_debounce_timer)
        self.timer.timeout.connect(self.on_debounced_text_changed)

    def switch_to_list_view(self):
        self.rooms_view_stacked_widget.setCurrentWidget(self.list_view_widget)
        self.change_view_mode.emit("list_view")

    def switch_to_grid_view(self):
        self.rooms_view_stacked_widget.setCurrentWidget(self.grid_view_widget)
        self.change_view_mode.emit("grid_view")

    # List view ------------------------------------------------------------------------------------------------

    def make_list_view_rooms_frame(self, amount_of_frames):

        new_max_list_rooms_frame = self.get_list_view_current_max_rows()

        # Choose between the lesser value between the two
        new_max_list_rooms_frame = min(amount_of_frames, new_max_list_rooms_frame)

        if new_max_list_rooms_frame < self.max_list_rooms_frame:
            self.clear_list_view_frames(new_max_list_rooms_frame)

        elif new_max_list_rooms_frame > self.max_list_rooms_frame:
            for i in range(new_max_list_rooms_frame):
                item = self.list_view_grid_layout.itemAtPosition(i, 0)

                if item is None:
                    self.list_view_grid_layout.addWidget(ListRoomsFrame({"room_type": "single"}), i, 0, 1, 1)
                elif isinstance(item, QSpacerItem):
                    self.list_view_grid_layout.removeItem(item)
                    self.list_view_grid_layout.addWidget(ListRoomsFrame({"room_type": "single"}), i, 0, 1, 1)

        if new_max_list_rooms_frame != self.max_list_rooms_frame:
            vertical_spacer = QSpacerItem(20, 5, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

            self.list_view_grid_layout.addItem(vertical_spacer, new_max_list_rooms_frame, 0, 1, 1,
                                               Qt.AlignmentFlag.AlignTop)

            self.max_list_rooms_frame = new_max_list_rooms_frame

            print("add row: " + str(self.max_list_rooms_frame + 1))

        print("Elements in list view grid layout: " + str(self.list_view_grid_layout.count()))
        # print("list_view_widget height: " + str(self.list_view_widget.height()))
        # print("list_view_contents_frame height: " + str(self.list_view_contents_frame.height()))

    def clear_list_view_frames(self, new_max_list_rooms_frame):
        for i in reversed(range(new_max_list_rooms_frame, self.list_view_grid_layout.count())):

            # Removes the item from the grid layout, while returning the item
            item = self.list_view_grid_layout.takeAt(i)

            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

            # If item is a QSpacerItem, Python's GC will collect item, since it has no more reference

    def update_list_view_frames_contents(self, data_from_model, open_add_edit_room_dialog_func, delete_room_func):

        for row in range(self.list_view_grid_layout.count()):

            item = self.list_view_grid_layout.itemAtPosition(row, 0)
            if item:
                list_rooms_frame = item.widget()
                if list_rooms_frame:
                    room_number = data_from_model[row][0]

                    list_rooms_frame.room_num_label.setText(room_number.replace("room-", "#"))
                    list_rooms_frame.room_type_value_label.setText(data_from_model[row][1].capitalize())
                    list_rooms_frame.rate_value_label.setText(f"P{data_from_model[row][2]}/day")
                    list_rooms_frame.status_value_label.setText(data_from_model[row][3].capitalize())
                    list_rooms_frame.capacity_value_label.setText(str(data_from_model[row][4]))

                    relative_file_path = "../resources/icons/rooms_page/room_images/" + data_from_model[row][5]

                    if relative_file_path in self.image_cache:
                        pixmap = self.image_cache[relative_file_path]
                        list_rooms_frame.room_image_label.setPixmap(pixmap)
                    else:
                        pixmap = QPixmap(relative_file_path)
                        list_rooms_frame.room_image_label.setPixmap(pixmap)

                        self.image_cache.update({relative_file_path: pixmap})

                    try:
                        list_rooms_frame.edit_button.clicked.disconnect()
                        list_rooms_frame.delete_button.clicked.disconnect()
                    except TypeError:
                        pass

                    list_rooms_frame.edit_button.clicked.connect(lambda _, mode="edit_room", rn=room_number:
                                                                 open_add_edit_room_dialog_func(mode,
                                                                                                room_number=rn))

                    list_rooms_frame.delete_button.clicked.connect(lambda _, rn=room_number: delete_room_func(rn))

                    list_rooms_frame.set_status_value_label_stylesheet()

    # List view end ------------------------------------------------------------------------------------------------
    # Grid view ------------------------------------------------------------------------------------------------

    def make_grid_view_rooms_frame(self, amount_of_frames):

        print("Elements in grid view grid layout b444: " + str(self.grid_view_grid_layout.count()))
        print(f"amount of frames: {amount_of_frames}")

        current_max_rows, current_max_columns = self.get_current_rows_and_columns_in_grid_layout("grid_view")

        new_max_grid_rooms_frame_rows = self.get_grid_view_current_max_rows()
        new_max_grid_rooms_frame_columns = self.get_grid_view_current_max_columns()

        max_slots = new_max_grid_rooms_frame_columns * new_max_grid_rooms_frame_rows

        # Choose between the lesser value between the two
        new_max_grid_rooms_frame = min(amount_of_frames, max_slots)

        self.clear_dummy_grid_frames(current_max_rows, current_max_columns)

        reusable_frames = self.extract_existing_grid_room_frames(current_max_rows, current_max_columns)

        counter = 0
        for row in range(new_max_grid_rooms_frame_rows):
            for column in range(new_max_grid_rooms_frame_columns):
                if counter < amount_of_frames:
                    if reusable_frames:
                        frame = reusable_frames.pop()
                    else:
                        frame = GridRoomsFrame({"room_type": "single"})

                    self.grid_view_grid_layout.addWidget(frame, row, column)
                    frame.show()
                    counter += 1

        for frame in reusable_frames:
            frame.hide()

        self.add_dummy_grid_frames(new_max_grid_rooms_frame_rows, new_max_grid_rooms_frame_columns)

        max_rows, max_columns = self.get_current_rows_and_columns_in_grid_layout("grid_view")

        self.set_column_and_row_stretch(current_max_rows, current_max_columns, max_rows, max_columns)

        self.max_grid_rooms_frame = new_max_grid_rooms_frame

        print("Elements in grid view grid layout: " + str(self.grid_view_grid_layout.count()))

        # self.grid_view_grid_layout.update()
        # self.grid_view_grid_layout.invalidate()
        # self.grid_view_grid_layout.activate()
        # self.grid_view_widget.adjustSize()
        # self.grid_view_widget.updateGeometry()

        # for column in range(new_max_grid_rooms_frame_columns):
        #     self.grid_view_grid_layout.setColumnStretch(column, 1)

    def extract_existing_grid_room_frames(self, rows, columns):
        reusable_frames = []


        for i in reversed(range(self.grid_view_grid_layout.count())):
            item = self.grid_view_grid_layout.itemAt(i)
            widget = item.widget()

            if isinstance(widget, GridRoomsFrame):
                reusable_frames.append(widget)
                self.grid_view_grid_layout.removeWidget(widget)

        return reusable_frames

    def set_column_and_row_stretch(self, current_max_rows, current_max_columns, max_rows, max_columns):

        for c_row in range(current_max_rows):
            self.grid_view_grid_layout.setRowStretch(c_row, 0)

        for c_column in range(current_max_columns):
            self.grid_view_grid_layout.setColumnStretch(c_column, 0)

        for row in range(max_rows):
            self.grid_view_grid_layout.setRowStretch(row, 1)

        for column in range(max_columns):
            self.grid_view_grid_layout.setColumnStretch(column, 1)

    def add_dummy_grid_frames(self, max_row, max_column):
        for row in range(max_row):
            for column in range(max_column):
                item = self.grid_view_grid_layout.itemAtPosition(row, column)

                if not item:
                    dummy_frame = QFrame()
                    dummy_frame.setObjectName(f"dummy_frame_{row}_{column}")
                    dummy_frame.setMinimumSize(320, 250)
                    dummy_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    self.grid_view_grid_layout.addWidget(dummy_frame, row, column)

    def clear_dummy_grid_frames(self, max_row, max_column):
        for row in range(max_row):
            for column in range(max_column):
                item = self.grid_view_grid_layout.itemAtPosition(row, column)

                if item:
                    widget = item.widget()
                    if widget and widget.objectName().startswith("dummy_frame_"):
                        self.grid_view_grid_layout.removeWidget(widget)
                        widget.setParent(None)
                        widget.deleteLater()

    def clear_grid_view_frames(self, new_max_grid_rooms_frame_rows, new_max_grid_rooms_frame_columns, amount_of_frames):
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

                            self.grid_view_grid_layout.setColumnStretch(column, 0)
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

                            self.grid_view_grid_layout.setRowStretch(row, 0)
                        else:
                            self.grid_view_grid_layout.removeItem(item)
                            break

        if amount_of_frames != new_max_grid_rooms_frame_rows * new_max_grid_rooms_frame_columns:
            counter = 0

            for row in range(max_row):
                for column in range(max_column):

                    counter += 1

                    if counter > amount_of_frames:

                        item = self.grid_view_grid_layout.itemAtPosition(row, column)
                        if item:
                            widget = item.widget()
                            if widget:
                                widget.setParent(None)
                                widget.deleteLater()

                                self.grid_view_grid_layout.setRowStretch(row, 0)
                                self.grid_view_grid_layout.setColumnStretch(column, 0)
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

    def update_grid_view_frames_contents(self, data_from_model, open_add_edit_room_dialog_func, delete_room_func):

        print("Elements in grid view grid layout CONTENTT: " + str(self.grid_view_grid_layout.count()))

        max_row, max_column = self.get_current_rows_and_columns_in_grid_layout("grid_view")
        counter = 0

        for row in range(max_row):
            for column in range(max_column):

                item = self.grid_view_grid_layout.itemAtPosition(row, column)
                if item:
                    grid_rooms_frame = item.widget()

                    # If dummy frame
                    if grid_rooms_frame.objectName().startswith("dummy_frame_"):
                        continue
                    else:

                        room_number = data_from_model[counter][0]

                        grid_rooms_frame.room_num_and_title_label.setText(
                            f"{room_number.replace("room-", "#")} - {data_from_model[counter][1].capitalize()}")
                        grid_rooms_frame.rate_value_label.setText(f"P{data_from_model[counter][2]}/day")
                        grid_rooms_frame.status_value_label.setText(data_from_model[counter][3].capitalize())
                        grid_rooms_frame.capacity_label.setText(str(data_from_model[counter][4]))

                        grid_rooms_frame.delete_button.clicked.connect(
                            lambda _, rn=room_number: delete_room_func(rn))

                        relative_file_path = "../resources/icons/rooms_page/room_images/" + \
                                             data_from_model[counter][5]

                        if relative_file_path in self.image_cache:
                            pixmap = self.image_cache[relative_file_path]
                            grid_rooms_frame.room_image_label.setPixmap(pixmap)
                        else:
                            pixmap = QPixmap(relative_file_path)
                            grid_rooms_frame.room_image_label.setPixmap(pixmap)

                            self.image_cache.update({relative_file_path: pixmap})

                    try:
                        grid_rooms_frame.edit_button.clicked.disconnect()
                        grid_rooms_frame.delete_button.clicked.disconnect()
                    except TypeError:
                        pass

                    grid_rooms_frame.edit_button.clicked.connect(lambda _, mode="edit_room", rn=room_number:
                                                                 open_add_edit_room_dialog_func(mode,
                                                                                                room_number=rn))

                    grid_rooms_frame.delete_button.clicked.connect(lambda _, rn=room_number: delete_room_func(rn))

                    grid_rooms_frame.set_status_value_label_stylesheet()

                    counter += 1

    # Grid view end ------------------------------------------------------------------------------------------------

    def get_list_view_current_max_rows(self):
        list_rooms_frame_min_height = 87

        return self.list_view_contents_frame.height() // list_rooms_frame_min_height

    def get_grid_view_current_max_rows(self):
        grid_rooms_frame_min_height = 250

        return self.grid_view_widget.height() // grid_rooms_frame_min_height

    def get_grid_view_current_max_columns(self):
        grid_rooms_frame_min_width = 320

        return self.grid_view_widget.width() // grid_rooms_frame_min_width

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

        self.sort_by_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.sort_type_combobox.setFont(QFont("Inter", 12, QFont.Weight.Normal))
        self.add_room_button.setFont(QFont("Inter", 12, QFont.Weight.Normal))

        self.previous_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))
        self.next_page_button.setFont(QFont("Inter", 11, QFont.Weight.Normal))

    # resizeEvent will be automatically called when switching to rooms page widget, so no need to preload frames
    def resizeEvent(self, event):

        current_width = self.width()
        current_height = self.height()

        width_diff = abs(self.previous_width - current_width)
        height_diff = abs(self.previous_height - current_height)

        if width_diff >= self.size_change_threshold or height_diff >= self.size_change_threshold:

            self.window_resized.emit()

            self.previous_width = current_width
            self.previous_height = current_height

