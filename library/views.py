from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
#from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import F


from accounts.models import studentProfile
from .forms import *
from .models import *


def index(response):
    return render(response, "library/index.html")


def admindashboard(response):
    if response.method == "GET":
        bookcount = len(Book.objects.all())
        studentcount = len(studentProfile.objects.all())
        print(response.user)

        context = {
            "bookcount": bookcount,
            "studentcount": studentcount
        }
        return render(response, "library/adminDashboard.html", context)


@login_required
def userdashboard(response):
    if response.user.is_superuser == False:
        print(response.user)
        student = studentProfile.objects.get(
            roll_no=response.user.username)
        print(student)
        issues = Issue.objects.filter(user=response.user)
        print(issues)

        context = {
            "student": student,
            "issues": issues
        }
        return render(response, "library/userDashboard.html", context)
    else:
        return HttpResponse("not authorized")


def booksView(response):
    bookList = Book.objects.all()
    context = {
        "bookList": bookList,
    }
    return render(response, "library/booksView.html", context)


def bookDetail(request, id):
    bookdetail = Book.objects.get(id=id)
    if request.user.is_superuser:
        permission = "admin_portal"
        context = {
            "permission": permission,
            "bookdetail": bookdetail
        }
    else:
        permission = "user"
        context = {
            "permission": permission,
            "bookdetail": bookdetail
        }
    print(bookdetail)
    return render(request, "library/bookDetail.html", context)


def sendMessages(response):
    if response.method == "POST":
        form = sendMessageForm(response.POST)
        if form.is_valid():
            m = form.cleaned_data["message"]
            r = form.cleaned_data["user"]
            ty = form.cleaned_data["type"]
            # user = User.objects.get(username=r)
            t = Message(message=m, user=r, type=ty)
            t.save()
            # response.user.message.add(t)
            return redirect("admindashboard")

    else:
        form = sendMessageForm()
        return render(response, "library/sendMessage.html", {"form": form})


@login_required
def viewMessages(request):
    messages = Message.objects.filter(user=request.user)
    print(request.user)
    context = {
        "messages": messages
    }
    return render(request, "library/viewMessage.html", context)


@login_required
def viewCurrBooks(request):
    if request.method == "GET":
        issued = Issue.objects.filter(user=request.user)
        renew_req = Renewrequests.objects.all()

        print("issued", issued)
        print("renew_req", renew_req)

        request_set = set()

        for i in issued:
            for j in renew_req:
                if i.id == j.issue.id:
                    print(i.book.title, i.id, "\n")
                    print(j.issue.renew_count, " ", j.issue.id, "\n")

                    if j.issue.renew_count > 0:
                        request_set.add(i.book.id)

        # for i in renew_req:
        #     if request.user == i.issue.user:
        #         if issued.renew_count > 0:
        #         else:
        #             request_block = True
        print(request_set)

        context = {
            "request_list": list(request_set),
            "issued": issued
        }
        return render(request, "library/viewCurrBooks.html", context)
    if request.method == "POST":
        print(request.user)
        if request.user.is_superuser == False:
            print(len(request.POST), request.POST)
            for key in request.POST:
                if request.POST[key] == "Return":
                    bookId = key
                    # print(bookId, "vi")

                    book = Book.objects.get(id=bookId)
                    # print("applis ", book.title)

                    issued = Issue.objects.filter(
                        Q(book=book) & Q(user=request.user)
                    )[0]

                    # print("iss", issued.book.id)
                    roll_no = issued.user.username
                    book_title = issued.book.title
                    book_id = issued.book.id

                    rb = Returned.objects.create(
                        roll_no=roll_no, book_id=book_id, book_title=book_title)
                    # print("refr", rb)

                    book.available += 1
                    book.save()
                    rb.save()
                    issued.delete()
                    messages.success(
                        request, "Successful deletion and saving in returned books!")
                    return redirect("viewCurrBooks")

                if request.POST[key] == "Renew":
                    bookId = key
                    book = Book.objects.get(id=bookId)
                    issued = Issue.objects.filter(
                        Q(book=book) & Q(user=request.user)
                    )[0]
                    print("iss", issued.due_at)
                    due_date = issued.due_at
                    present_date = timezone.now()

                    if due_date > present_date:
                        print("ncurc", present_date, due_date)

                        rr = Renewrequests.objects.create(
                            issue=issued
                        )

                        rr.save()
                        messages.success(request, "Renew Request accepted!")
                        return redirect("viewCurrBooks")
                    return HttpResponse("cfnvn")

            messages.error(request, "Invalid book request!")
            return redirect("viewCurrBooks")

        else:
            print("Invalid authorization")
            messages.error(request, "Invalid Authorization")
            return redirect("viewCurrBooks")


@login_required
def viewAllBooks(request):
    if request.method == "GET":
        books = Book.objects.all()
        # print(request.user)
        borrow = Borrowrequest.objects.all()

        issue = Issue.objects.all()
        # print(borrow)
        borrow_list = []
        issue_list = []
        # print(borrow[0].book.id, books[0].id)

        for i in borrow:
            if request.user == i.user:
                if i.book.id not in borrow_list:
                    borrow_list.append(i.book.id)

        for i in issue:
            if request.user == i.user:
                if i.book.id not in issue_list:
                    issue_list.append(i.book.id)

        context = {
            "books": books,
            "borrow_list": borrow_list,
            "issue_list": issue_list,
        }
        return render(request, "library/userBookView.html", context)

    if request.method == "POST":
        if request.user.is_superuser == False:
            # print(len(request.POST))
            for key in request.POST:
                if request.POST[key] == "Borrow":
                    bookId = key
                    book = Book.objects.get(id=bookId)
                    print(book.available)
                    # return HttpResponse("itjij")
                    if book.available > 0:
                        br = Borrowrequest.objects.create(
                            user=request.user, book=book)
                        br.save()
                        messages.success(request, "Borrow Request accepted!")
                        return redirect("viewAllBooks")
                    # else:
                    #     messages.error(request, "Book out of stock!")
                    #     return redirect("viewAllBooks")
                # messages.error(request, "Invalid book request!")
                # return redirect("viewAllBooks")
        else:
            print("Invalid authorization")
            messages.error(request, "Invalid Authorization")
            return redirect("viewAllBooks")


def addBook(request):
    if request.method == "GET":
        print("add")
        context = {
            "form": addBookForm()
        }
        return render(request, "library/addBook.html", context)
    if request.method == "POST":
        print("post add")
        form = addBookForm(request.POST)
        if form.is_valid():
            title = request.POST["title"]
            author = request.POST["author"]
            available = request.POST["available"]
            publisher = request.POST["publisher"]
            year = request.POST["year"]
            cost = request.POST["cost"]
            book = Book.objects.create(title=title, author=author, available=available,
                                       publisher=publisher, year=year, cost=cost)
            book.save()
            messages.success(request, "New book added successfully!")
            return redirect("admindashboard")
        else:
            messages.error(request, "Error in adding book")
            return redirect('addBook')


def issueBook(request):
    if request.method == "GET":
        borrow_request = Borrowrequest.objects.all()
        context = {
            "borrow_request": borrow_request
        }
        return render(request, "library/issueBook.html", context)
    if request.method == "POST":
        if request.user.is_superuser:
            # print(len(request.POST))
            for key in request.POST:
                if request.POST[key] == "Issue":
                    bookId, roll_no = [k for k in key.split("|")]

                    book = Book.objects.get(id=bookId)
                    user = User.objects.get(username=roll_no)
                    if book.available > 0:
                        iss = Issue.objects.create(
                            user=user, book=book)
                        iss.save()
                        book.available -= 1
                        book.save()

                        student = studentProfile.objects.get(
                            roll_no=roll_no)
                        student.books_borrowed_count += 1
                        student.save()

                        messages.success(request, "Book issue accepted!")
                        borrow_request = Borrowrequest.objects.filter(
                            Q(book=book) & Q(user=user)
                        )[0]
                        print(borrow_request)
                        borrow_request.delete()
                        return redirect("issueBook")
            messages.error(request, "Invalid book issuing!")
        else:
            print("Invalid authorization")
            messages.error(request, "Invalid Authorization")
            return redirect("issueBook")


@login_required
def viewReturnedBooks(request):
    if request.method == "GET":
        print(request.user)
        # correct method of sending a query list to the returnedViewTemplate
        returned = list(Returned.objects.filter(roll_no=request.user.username))
        context = {
            "returned": returned
        }
        return render(request, "library/viewReturnedBooks.html", context)


@login_required
def recommendBook(request):
    if request.method == "GET":
        form = recommendBookForm()
        if request.user.is_superuser:
            permission = "admin_portal"
        else:
            permission = "user"
        context = {
            "permission": permission,
            "form": form
        }
        return render(request, "library/recommendBook.html", context)
    if request.method == "POST":
        form = recommendBookForm(request.POST)

        book_title = request.POST["book_title"]
        book_publisher = request.POST["book_publisher"]
        book_author = request.POST["book_author"]
        roll_no = request.user.username
        if form.is_valid():
            rc = Recommend.objects.create(
                roll_no=roll_no, book_title=book_title, book_publisher=book_publisher, book_author=book_author)
            rc.save()
            messages.success(
                request, "Book recommendation request posted!")
            return redirect("userdashboard")
        else:
            messages.error(request, "Error in recommending book")
            return redirect('recommendBook')


def viewRecommend(request):
    if request.user.is_superuser:
        recommendations = Recommend.objects.all()
        context = {
            "recommendations": recommendations
        }
        return render(request, "library/viewUserRecommend.html", context)


@login_required
def renewBook(request):
    if request.user.is_superuser:
        if request.method == "GET":
            # correct method of sending a query list to the returnedViewTemplate
            renew_req = Renewrequests.objects.all()
            print(renew_req)
            context = {
                "renew_req": renew_req
            }
            return render(request, "library/renewBooks.html", context)
        if request.method == "POST":
            # print(len(request.POST))
            for key in request.POST:
                if request.POST[key] == "Renew":
                    bookId, roll_no = [k for k in key.split("|")]

                    book = Book.objects.get(id=bookId)
                    user = User.objects.get(username=roll_no)

                    issue = Issue.objects.filter(
                        Q(book=book) & Q(user=user)
                    )[0]
                    issue.due_at = issue.due_at+timedelta(days=10)
                    issue.save()

                    renew_req_item = Renewrequests.objects.get(issue=issue)
                    if renew_req_item.issue.renew_count > 0:
                        issue.renew_count -= 1
                        issue.save()
                        renew_req_item.delete()
                        return redirect("renewBook")

                    else:
                        print("Renewal Count exceeded")
                        messages.error(request, "Renewal count exceeded!")
                        return redirect("renewBook")


def borrowedBooks(request):
    if request.user.is_superuser:
        if request.method == "GET":
            issued_books = Issue.objects.all()
            print(issued_books)
            context = {
                "issued_books": issued_books
            }
            return render(request, "library/borrowedBooks.html", context)


@login_required
def viewStudentList(request):
    if request.user.is_superuser:
        if request.method == "GET":
            students = studentProfile.objects.all()
            context = {
                "students": students
            }
            return render(request, "library/studentList.html", context)
        if request.method == "POST":
            print(request.POST)
            for key in request.POST:
                print(key)
                if request.POST[key] == "Delete":
                    roll_no = key
                    student = studentProfile.objects.get(roll_no=roll_no)
                    print(student)
                    student.delete()
                    messages.success(
                        request, "Student Profile deleted successfully!")
                    return redirect('viewStudentList')

    else:
        print("Not authorized!")
        return redirect('viewStudentList')


@login_required
def editStudent(request, id):
    if request.user.is_superuser:
        student = studentProfile.objects.get(roll_no=id)
        if request.method == "GET":
            form = editStudentForm(instance=student)
            context = {
                "student": student,
                "form": form
            }
            return render(request, "library/editDetails.html", context)
        if request.method == "POST":
            form = editStudentForm(request.POST, instance=student)
            if form.is_valid():
                form.save()
                return redirect("viewStudentList")


@login_required
def editBooks(request, id):
    if request.user.is_superuser:
        book = Book.objects.get(id=id)
        if request.method == "GET":
            form = addBookForm(instance=book)
            context = {
                "form": form
            }
            return render(request, "library/editBooks.html", context)
        if request.method == "POST":
            form = addBookForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
                return redirect("booksView")


# ERROR HANDLING


def not_found(request, exception=None):
    response = render(request, 'library/404.html', {})
    response.status_code = 404
    return response


def server_error(request, exception=None):
    response = render(request, 'library/500.html', {})
    response.status_code = 500
    return response


    # views.py
from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html')



# FINE
# GENRE
# ALERTS
# RENEWAL                    *
# AVAILABLE BOOKS            *
# ADMIN ISSUE BOOKLIST
# GROUP MESSAGE POSTING
# MAX BOOK BORROW COUNT
# UI/UX DESIGN + STYLING
# STATISTICS-ADMIN/USER
# MONTHLY, YEARLY
# PROFILE-ADMIN/USER         *
# EDIT BOOK DETAIL
# AUTHENICATION
"""
    BOOK CAN BE RENEWED MAX FOR 1 WEEK MORE
"""
