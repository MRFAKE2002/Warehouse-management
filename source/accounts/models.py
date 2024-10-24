# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# from django.contrib.auth.validators import UnicodeUsernameValidator


# class BaseUserManager(BaseUserManager):

#     def create_user(self, username, email, is_active=True, is_admin=False, password=None):
#         """ Creates a user with username and email"""
#         if not email and not username:
#             raise ValueError('وارد تمودن نام کاربری و ایمیل الزامی ست')
        
#         user = self.model(email=self.normalize_email(email.lower()), username=username, is_active=is_active, is_admin=is_admin )

#         if password is not None:
#             password = user.set_password(password)
#         else:
#             password = user.set_unusable_passord()
        
#         user.full_clean()
#         user.save(using=self._db)

#         return user
    

#     def create_superuser(self, email, username, password):

#         user = self.create_user(
#             email=email,
#             username=username,
#             password=password,
#             is_active=True,
#             is_admin=True
#             )

#         user.is_superuser = True
#         user.save(using=self._db)

#         return user
    

# class BaseUser(AbstractBaseUser, PermissionsMixin):
    
#     username_validator = UnicodeUsernameValidator()

#     username = models.CharField(
#         "نام کاربری",
#         max_length=150,
#         unique=True,
#         help_text= "وارد تمودن نام کاربری الزامی ست. نام کاربری شامل حداکثر 150 حرف انگلیسی یا کارکتر های @/./+/-/_ می باشد",
#         validators=[username_validator],
#         error_messages={
#             "unique": "این نام کاربری توسط شخص دیگری به کار گرفته شده است",
#         },
#     )

#     email = models.EmailField(
#         "ایمیل",
#         max_length = 150, 
#         help_text="وارد نمودن ایمیل الزامی می باشد", 
#         unique=True,
#         error_messages={
#             "unique:ایمیل توسط کاربر دیگری به کار گرفته شده است"
#         }, 
#     )

#     first_name = models.CharField("نام ", max_length=150, blank=True)
#     last_name = models.CharField("نام خانوادگی", max_length=150, blank=True)
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     # is_staff = models.BooleanField(default=False)
    
    
#     USERNAME_FIELD = "username"
#     REQUIRED_FIELDS = ["email"]

#     class Meta:
#         verbose_name = "کاربر"
#         verbose_name_plural = "کاربران"
        
#     def __str__(self):
#         return "Username:{} \n Email:{}".format(self.username, self.email)

#     # @property
#     def is_staff(self):
#         return self.is_admin

#     #declaring the manager
#     objects = BaseUserManager()

from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseUser(AbstractUser):
    pass

    def __str__(self):
        return str(self.username)

