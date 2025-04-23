

class RoomsModel:
    def __init__(self, room_list: list[dict], initial_rows_per_page, initial_columns_per_page):
        self._rooms = room_list

        self._rows_per_page = initial_rows_per_page
        self._columns_per_page = initial_columns_per_page

        self._current_page = 1

    def total_pages(self, view_mode):

        if view_mode == "list_view":
            return (len(self._rooms) + self._rows_per_page - 1) // self._rows_per_page
        else:
            return ((len(self._rooms) - 1) // (self._rows_per_page * self._columns_per_page)) + 1

    def set_next_page(self, view_mode):
        if self._current_page + 1 <= self.total_pages(view_mode):
            self._current_page += 1
            return True

    def set_previous_page(self):
        if self._current_page > 1:
            self._current_page -= 1
            return True

    def get_per_page(self, view_mode):
        return len(self.get_rooms_from_current_page(view_mode))

    def set_max_rows_per_page(self, new_rows_per_page):
        self._rows_per_page = new_rows_per_page

    def get_max_rows_per_page(self):
        return self._rows_per_page

    def set_max_columns_per_page(self, new_columns_per_page):
        self._columns_per_page = new_columns_per_page

    def get_max_columns_per_page(self):
        return self._columns_per_page

    def get_len_of_data(self):
        return len(self._rooms)

    def get_rooms_from_current_page(self, view_mode):

        start = 0
        end = 0

        if view_mode == "list_view":
            # Has -1 because zero-based
            start = (self._current_page - 1) * self._rows_per_page
            end = start + self._rows_per_page

        elif view_mode == "grid_view":
            frames_per_page = self._rows_per_page * self._columns_per_page

            start = (self._current_page - 1) * frames_per_page
            end = start + frames_per_page

        return self._rooms[start:end]

    def check_if_underflow_contents(self, view_mode):
        if self.get_per_page(view_mode) == 0:
            self.set_previous_page()

    def reset(self):
        self._current_page = 1

    def current_page_index(self):
        return self._current_page
