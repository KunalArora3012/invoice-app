from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=15)
    emp_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)

    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name