from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(Issue)
admin.site.register(Message)
admin.site.register(Borrowrequest)
admin.site.register(Returned)
admin.site.register(Renewrequests)
