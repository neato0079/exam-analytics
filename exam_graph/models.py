from django.contrib.auth.models import UserManager
from django.db import models

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, user_name, password):
        user = self.model(user_name=user_name)
        user.set_password(password)
        user.save(using=self._db)

        return user

class Member(models.Model):
    username = models.CharField(max_length=100)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    passwd = models.CharField(max_length=50)
    facility = models.CharField(max_length=4)

    def __str__(self):
        return self.username