from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Account(AbstractUser):
    class Meta:
        db_table = "Account"

    def __str__(self):
    	return self.username