from django.contrib import admin
from .models import Book,Favourite
from django.contrib.auth.models import User
# Register your models here.
@admin.register(Book) 
class BookAdmin(admin.ModelAdmin):
    list_display=['id','title','description','book_image']
@admin.register(Favourite) 
class BookAdmin(admin.ModelAdmin):
    list_display=['id','book','user']

admin.site.unregister(User)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'id','is_active','is_staff')
    readonly_fields = ('id',)
admin.site.register(User,CustomUserAdmin)
