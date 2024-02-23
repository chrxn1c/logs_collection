class User:
    user_count: int = 0

    def __init__(self, first_name: str, second_name: str) -> None:
        self.first_name: str = first_name
        self.second_name: str = second_name
        user_count += 1
        self.id: int = user_count

    def __str__(self) -> str:
        return f"{self.first_name} {self.second_name}, id = {self.id}"

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.second_name}"
