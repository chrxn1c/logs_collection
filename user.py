class User:
    def __init__(self, first_name: str, second_name: str, id: int) -> None:
        self.first_name: str = first_name
        self.second_name: str = second_name
        self.id: int = id

    def __str__(self) -> str:
        return f"{self.first_name} {self.second_name}, id = {self.id}"
