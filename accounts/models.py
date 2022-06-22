from django.db import models
from django.contrib.auth.models import User
from library.models import Returned
# Create your models here.


# class student(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=40)
#     email = models.EmailField()

#     def __str__(self):
#         return f'{self.user} | {self.name} | {self.email}'


class studentProfile(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=9)
    name = models.CharField(max_length=40)
    email = models.EmailField()
    branch = models.CharField(default="NONE", max_length=50)
    books_borrowed_count = models.IntegerField()
    date_of_joining = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.roll_no} | {self.name} | {self.email}'
