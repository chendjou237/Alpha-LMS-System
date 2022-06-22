from django.urls import path
from .views import *
from accounts.views import *
urlpatterns = [
    path("", user_login, name="user_login"),

    path("admin_portal/", admindashboard, name="admindashboard"),
    path("admin_portal/books/", booksView, name="booksView"),
    path("admin_portal/messages/", sendMessages, name="sendMessages"),
    path("admin_portal/add_book/", addBook, name="addBook"),
    path("admin_portal/issue_book/", issueBook, name="issueBook"),
    path("admin_portal/renew_book/", renewBook, name="renewBook"),
    path("admin_portal/borrowed_books/", borrowedBooks, name="borrowedBooks"),
    path("admin_portal/view_recommend/", viewRecommend, name="viewRecommend"),
    path("admin_portal/student_list/", viewStudentList, name="viewStudentList"),
    path("admin_portal/books/details/<int:id>", bookDetail, name="bookDetail"),
    path("admin_portal/student_list/edit/<str:id>",
         editStudent, name="editStudent"),
    path("admin_portal/books/edit/<int:id>", editBooks, name="editBooks"),

    path("user/", userdashboard, name="userdashboard"),
    path("user/messages/", viewMessages, name="viewMessages"),
    path("user/books/", viewAllBooks, name="viewAllBooks"),
    path("user/currbooks/", viewCurrBooks, name="viewCurrBooks"),
    path("user/returned/", viewReturnedBooks, name="viewReturnedBooks"),
    path("user/recommend/", recommendBook, name="recommendBook"),
    path("user/books/details/<int:id>", bookDetail, name="bookDetail"),
]
