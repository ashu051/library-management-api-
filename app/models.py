from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=30)    
    description = models.CharField(max_length=20)
    book_image=models.ImageField(upload_to='bookimages')
    def __str__(self):
        return str(self.id)

    
class Favourite(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='kitab')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='aadmi')
    def __str__(self):
        return str(self.id)
    
    
