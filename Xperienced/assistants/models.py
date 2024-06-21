from django.db import models
from account.models import User

class Type(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="type", null=True, blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="category", null=True, blank=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Offer(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offer",null=True,blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(Type, on_delete=models.CASCADE,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=10, choices= [('Full Time', 'full time'), ('Part Time', 'part time')], default='Chouse')
    file = models.FileField(upload_to='offers/', null=True, blank=True)
    def __str__(self):
        return self.title

# class Offer(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     type = models.ForeignKey(Type, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     salary = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed')], default='open')
#     file = models.FileField(upload_to='offers/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title
    