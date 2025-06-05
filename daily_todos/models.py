from uuid import uuid4
from django.db import models

def gen_default_livetodo_key():
    return "livetodo_"+str(uuid4())

def gen_default_datetodos_key():
    return "datetodos_"+str(uuid4())

class TodoSubmitted(models.Model):
    email = models.EmailField()
    submitted_time = models.DateTimeField()
    date_todos = models.JSONField()
    live_todos = models.JSONField()


class DateTodos(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=80,default=gen_default_datetodos_key, unique=True)
    date = models.DateField(auto_now_add=True)
    todos = models.JSONField()
    content = models.TextField()

    def __str__(self):
        return str(self.name)



class TodoLevel(models.IntegerChoices):
    TOP_0 = 0
    TOP_1 = 1
    TOP_2 = 2
    TOP_3 = 3


class LiveTodo(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=80,default=gen_default_livetodo_key, unique=True)
    is_enabled = models.BooleanField(default=True)  # pyright: ignore[reportArgumentType]
    description = models.TextField()
    start_time = models.TimeField()
    level = models.IntegerField(choices=TodoLevel, default=TodoLevel.TOP_3)  # pyright: ignore[reportArgumentType]
    tags = models.TextField()
    datetime = models.DateTimeField()
    relive = models.CharField(max_length=20,help_text="N d/w/m/y; weekday; workday;")
    skip = models.CharField(max_length=20, help_text="on Mon.; on Tue.; on Wed.; on Thu.; on Fri; on Sat.; on Sun.;<br/>on */*/5; <br/> weekend; day off;")
    finish_info = models.TextField(help_text="[]<br/>() (p30) (p31/p32)<br/>{} {N} {p30/ p31/ p32/ p33} {1,2,1,1} {N;+5%,-4,-50%}")

    def __str__(self):
        return str(self.name)

