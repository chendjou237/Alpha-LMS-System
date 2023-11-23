from django.contrib import admin
from django.urls import path, include
from accounts.views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("library.urls")),
    path('register/', register, name="register"),
    path('', include('django.contrib.auth.urls')),
    path("userlogout/", user_logout, name="user_logout"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'library.views.not_found'
handler500 = 'library.views.server_error'

# urls.py
from django.urls import path
from .views import dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    # Add other URLs as needed
]
