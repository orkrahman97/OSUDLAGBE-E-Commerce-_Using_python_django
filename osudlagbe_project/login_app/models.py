from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models import fields
from django.db.models.expressions import Value
from django.utils import translation
from django.utils.translation import gettext_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver 
# Create your models here.
# To automatically create onetoone object

class MyUserManager(BaseUserManager):
    # Creating a custom manager to use email as login info
    def __create__user(self,email,password,**extra_fields):
        """ Creates and saves user with a given email
        and password """

        if not email:
            raise ValueError("Email is not valid!")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fileds):
        extra_fileds.setdefault('is_staff', True)
        extra_fileds.setdefault('is_superuser', True)
        extra_fileds.setdefault('is_active', True)

        if extra_fileds.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fileds.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self.__create__user(email, password, **extra_fileds)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False)
    is_staff = models.BooleanField(
        gettext_lazy('staff status'),
        default = False,
        help_text = gettext_lazy('Designates whether the user can log in the site')
    )

    is_active = models.BooleanField(
        gettext_lazy('active'),
        help_text = gettext_lazy('Designates whether the user is an active user or not. Unselect this instead of deleting the account')
    )

    USERNAME_FIELD = 'email'
    objects = MyUserManager()
    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email
    def get_short_name(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=264, blank=True)
    fullname = models.CharField(max_length=264,blank=True)
    address = models.TextField(max_length=300,blank=True)
    city = models.CharField(max_length=50,blank=True)
    zipcode = models.CharField(max_length=10,blank=True)
    country = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
    
    def is_fully_filled(self):
        fields_names = [f.name for f in self._meta.get_fields()]

        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value=='':
                return False
        return True

@receiver(post_save,sender=User)
def create_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save,sender=User)
def save_profile(sender,instance, **kwargs):
    instance.profile.save()

    





