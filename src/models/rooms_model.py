

class RoomsModel:
    def __init__(self, room_list: list[dict], initial_rows_per_page):
        self._rooms = room_list
        self._rows_per_page = initial_rows_per_page
        self._current_page = 1

    def total_pages(self):
        return (len(self._rooms) + self._rows_per_page - 1) // self._rows_per_page

    def set_next_page(self):
        if self._current_page + 1 <= self.total_pages():
            self._current_page += 1

    def set_previous_page(self):
        if self._current_page > 1:
            self._current_page -= 1
            print(self._current_page)

    def get_per_page(self):
        return len(self.get_rooms_from_current_page())

    def set_max_rows_per_page(self, new_rows_per_page):
        self._rows_per_page = new_rows_per_page

    def get_max_rows_per_page(self):
        return self._rows_per_page

    def get_rooms_from_current_page(self):
        # Has -1 because zero-based
        start = (self._current_page - 1) * self._rows_per_page
        end = start + self._rows_per_page
        return self._rooms[start:end]

    def reset(self):
        self._current_page = 0

    def current_page_index(self):
        return self._current_page
