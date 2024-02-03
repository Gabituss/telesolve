from tortoise.models import Model
from tortoise import fields


class User(Model):
    user_id = fields.IntField(unique=True)
    username = fields.CharField(max_length=255, null=True)
    full_name = fields.CharField(max_length=255)

    class Meta:
        table = "users"

    def __str__(self):
        return f"{self.user_id} {self.full_name}"


class Solver(Model):
    user_id = fields.IntField(unique=True)

    class Meta:
        table = "solvers"

    def __str__(self):
        return f"{self.user_id}"


class Test(Model):
    test_id = fields.IntField(unique=True)
    test_name = fields.CharField(max_length=255)
    test_cost = fields.IntField()
    visible = fields.BooleanField()

    class Meta:
        table = "tests"

    def __str__(self):
        return f"{self.test_id} {self.test_name} {self.test_cost}"


class Task(Model):
    task_id = fields.IntField(unique=True)
    user_id = fields.IntField()
    test_id = fields.IntField()

    full_name = fields.CharField(max_length=255)
    deadline = fields.CharField(max_length=255)
    login = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)

    mark = fields.IntField()
    approved = fields.IntField()
    hidden = fields.BooleanField()

    class Meta:
        table = "tasks"

    def task_info(self):
        return f"{self.task_id} {self.user_id}"

    def __str__(self):
        return f"{self.task_id} {self.test_id} {self.user_id}"
