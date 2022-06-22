from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from django.utils import timezone


class Book(models.Model):
    # catchoice = [
    #     ('education', 'Education'),
    #     ('entertainment', 'Entertainment'),
    #     ('comics', 'Comics'),
    #     ('biography', 'Biography'),
    #     ('history', 'History'),
    #     ('novel', 'Novel'),
    #     ('fantasy', 'Fantasy'),
    #     ('thriller', 'Thriller'),
    #     ('romance', 'Romance'),
    #     ('scifi', 'Sci-Fi')
    # ]
    title = models.CharField(max_length=40)
    author = models.CharField(max_length=40)
    # category = models.CharField(
    #     max_length=30, choices=catchoice, default='education')
    available = models.IntegerField()
    no_of_copies = models.IntegerField(default=5)
    image = models.ImageField(blank=True, null=True,
                              upload_to='post/')
    publisher = models.CharField(max_length=50)
    year = models.IntegerField()
    cost = models.FloatField()

    def __str__(self):
        return f'{self.title} '


def get_expiry():
    return datetime.today()+timedelta(days=15)

# admin issues books to...


class Issue(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE,  related_name="book", null=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    due_at = models.DateTimeField(default=get_expiry)
    renew_count = models.IntegerField(default=2)

    def __str__(self):
        return f'{self.user} | {self.book} | {self.due_at}'


# admin sends message to...


class Message(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message", null=True)
    message = models.CharField(max_length=300)
    type = models.CharField(max_length=20, choices=[(
        'info', 'info'), ('warning', 'warning'), ('approval', 'approval')])
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user} | {self.message} | {self.time}'


class Borrowrequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    requested_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


# borrow_request by student -> issue by admin-> returned by student->store in returned_books...


class Returned(models.Model):
    roll_no = models.CharField(max_length=9)
    book_id = models.IntegerField()
    book_title = models.CharField(max_length=40)
    returned_date = models.DateTimeField(auto_now_add=True)
    fine = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.roll_no} | {self.book_id}'


class Recommend(models.Model):
    roll_no = models.CharField(max_length=9)
    book_title = models.CharField(max_length=40)
    book_author = models.CharField(max_length=40)
    book_publisher = models.CharField(max_length=40)

    def __str__(self):
        return f'{self.roll_no} | {self.book_title} | {self.book_publisher}'


class Renewrequests(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    requested_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.issue}'
