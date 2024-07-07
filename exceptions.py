class UnreadbleStation(BaseException):
    def __init__(self, station: str, message: str='Station in unreadable list') -> None:
        self.message = message + f' - {station}'
        super().__init__(self.message)


class NoDataReceived(BaseException):
    def __init__(self, departure_station: str, operation_station: str, message: str='No data received departure') -> None:
        self.message = message + f'departure - {departure_station}, operation - {operation_station}'
        super().__init__(self.message)
