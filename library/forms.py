from django import forms

from accounts.models import studentProfile
from .models import *


class sendMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ["user", "type", "message", ]
        labels = {"user": "Roll no", "message": "Message", "type": "Category"}
    # roll_no = forms.CharField(max_length=9)
    # message = forms.CharField(max_length=300)


class addBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "available",
                  "no_of_copies", "publisher", "year", "cost", "image"]


class recommendBookForm(forms.ModelForm):
    class Meta:
        model = Recommend
        fields = ["book_title", "book_publisher", "book_author"]
        labels = {"book_title": "Title",
                  "book_publisher": "Publisher", "book_author": "Author"}


# class issueBookForm(forms.ModelForm):
#     class Meta:
#         model = Issue
#         fields = ["book", "issued_at", "due_at"]

class editStudentForm(forms.ModelForm):
    class Meta:
        model = studentProfile
        fields = ["roll_no", "name", "email", "branch",
                  "books_borrowed_count"]
        labels = {"roll_no": "Roll no", "name": "Name", "email": "Email", "branch": "Branch",
                  "books_borrowed_count": "Borrowed Books"}
