from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    description = models.TextField()
    cover = models.ImageField(upload_to="cover",null=True,blank=True)
    def __str__(self):
        return f"{self.name} by {self.author}"

class Cart(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)