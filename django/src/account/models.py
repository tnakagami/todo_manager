from django.db import models
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy
from datetime import datetime

class CustomUserManager(UserManager):
    """
    Custom User Manager
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password,  **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password,  **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User
    """
    screen_name = models.CharField(
        ugettext_lazy('screen name'),
        max_length=128,
        blank=True,
        help_text=ugettext_lazy('Option. 128 characters or fewer.'),
    )
    email = models.EmailField(ugettext_lazy('email address'), unique=True)
    is_staff = models.BooleanField(
        ugettext_lazy('staff status'),
        default=False,
        help_text=ugettext_lazy('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        ugettext_lazy('active'),
        default=True,
        help_text=ugettext_lazy(
            'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(ugettext_lazy('date joined'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ugettext_lazy('user')
        verbose_name_plural = ugettext_lazy('users')

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        return self.email

    def get_short_name(self):
        """Return the short name for the user."""
        return self.get_full_name()

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

class UserProfile(models.Model):
    # ?????????????????????
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # ?????????
    score = models.IntegerField(ugettext_lazy('score'), validators=[MinValueValidator(0)], default=0)
    # ?????????
    achievements = models.IntegerField(ugettext_lazy('number of achievements'), validators=[MinValueValidator(0)], default=0)
    # ????????????
    date_of_birth = models.DateTimeField(ugettext_lazy('date of birth'), default=timezone.make_aware(datetime(2000, 1, 1)))

    def __str__(self):
        return self.__unicode__()
    def __unicode__(self):
        return 'profile: {}'.format(self.user.email)

    def set_profile(self, profile):
        self.score = profile.score
        self.achievements = profile.achievements
        self.date_of_birth = profile.date_of_birth

    def update(self, point):
        self.score += point
        self.achievements += 1

@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    """
    ?????????????????????????????????profile???????????????
    """
    if kwargs['created']:
        profile, _ = UserProfile.objects.get_or_create(user=kwargs['instance'])

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()