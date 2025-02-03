from django.contrib.auth.models import UserManager
from django.db import models

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, user_name, password):
        user = self.model(user_name=user_name)
        user.set_password(password)
        user.save(using=self._db)

        return user