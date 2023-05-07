class PaginationError(Exception):
    def __init__(self, status_code = None) -> None:
        self.status_code = status_code
        super(PaginationError, self).__init__(f'Pagination failed. Status code: {self.status_code}')
        