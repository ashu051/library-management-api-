
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken import views as tview
from app import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# router.register('book_api1', views.book_api,basename="bookapi"),


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.registration_view),
    path('logout/', views.logout,name="logout"),
     path('book_api/',views.book_api,name="bookapi"),
path('fav_api/',views.fav_api,name="favapi"),
path('fav_api/<int:pk>',views.fav_api,name="favapiint"),
    path('book_api/<int:pk>',views.book_api,name="bookapiint"),
    path('login/', tview.obtain_auth_token,name="login"),
    # path('',include(router.urls)),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
