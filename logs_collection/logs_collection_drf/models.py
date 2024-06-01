from uuid import UUID

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    second_name = models.CharField(max_length=50)

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.second_name}"

    # def __str__(self) -> str:
    #     return f"{self.first_name} {self.second_name}, id = {self.id}"

    def __hash__(self) -> str:
        return repr(self)


class LoggingLevel(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    logging_level_name = models.CharField(max_length=10, unique=True, null=False)

    # def __str__(self) -> str:
    #     return repr(self)


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    logging_level = models.ForeignKey(LoggingLevel, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self) -> str:
        return f"{str(self.id)};{str(self.date)};{str(self.time)};{str(self.user_id)};{str(self.logging_level)};{str(self.message)}"


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)
    message = models.TextField(blank=False, null=False)

    # def __str__(self) -> str:
    #     return hash(repr(self))


class Operation:
    id: UUID
    done: bool

    def __init__(self, id: UUID, done: bool = False, result=None) -> None:
        self.id = id
        self.done = done
        self.result = result

    def __eq__(self, other: "Operation") -> bool:
        return (
                self.id == other.id
                and self.done == other.done
                and self.result == other.result
        )

    def __repr__(self) -> str:
        return str(
            {
                "id": self.id,
                "done": self.done,
                "result": self.result,
            }
        )


class LogsPerUser(models.Model):
    user = models.OneToOneField(User, verbose_name='user', on_delete=models.CASCADE, primary_key=True)
    counter = models.IntegerField(default=0)
