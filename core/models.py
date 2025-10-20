from django.db import models
from django.core.validators import RegexValidator,MaxValueValidator
from datetime import timedelta
from dateutil.relativedelta import relativedelta  # better for month arithmetic

# Create your models here.

# Reuse these
name_validator = RegexValidator(
    regex=r'^[A-Za-z][A-Za-z\s]*$',
    message='Name must start with a letter and contain only letters and spaces.'
)

phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
)


class Trainer(models.Model):
    gym = models.ForeignKey('Gym', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, validators=[name_validator])
    last_name = models.CharField(max_length=50, validators=[name_validator])
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, validators=[phone_validator])
    hire_date = models.DateField(auto_now_add=True)
    specialty = models.CharField(max_length=100)
    salary = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MaxValueValidator(100000, message="Salary cannot exceed ₹100,000.")]
    )
    photo = models.ImageField(upload_to='trainer_photos/', blank=True, null=True)  # <-- new field
    aadhar_document = models.FileField(upload_to='documents/aadhar/', blank=True, null=True)
    pan_document = models.FileField(upload_to='documents/pan/', blank=True, null=True)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Member(models.Model):
    COMPLETE_PACKAGE = 'COMPLETE_PACKAGE'
    GYM_CARDIO = 'GYM_CARDIO'
    GYM = 'GYM'
    CARDIO = 'CARDIO'

    PACKAGE_CHOICES = [
        (COMPLETE_PACKAGE, 'Complete Package'),
        (GYM, 'Gym'),
        (GYM_CARDIO, 'Gym + Cardio'),
        (CARDIO, 'Cardio'),
    ]

    STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
    ]

    DURATION_CHOICES = [
        (1, '1 Months'),
        (3, '3 Months'),
        (6, '6 Months'),
        (9, '9 Months'),
        (12, '1 Year'),
    ]

    phone_validator = RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits.")

    gym = models.ForeignKey('Gym', on_delete=models.CASCADE, null=True, blank=True)
    gym_member_id = models.PositiveIntegerField(null=True, blank=True)
    first_name = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=r'^[A-Za-z][A-Za-z\s]*$', message='First name must start with a letter and contain only letters and spaces.')
        ]
    )
    last_name = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(regex=r'^[A-Za-z][A-Za-z\s]*$', message='Last name must start with a letter and contain only letters and spaces.')
        ]
    )
    phone_number = models.CharField(max_length=15, validators=[phone_validator])
    email = models.EmailField(unique=True)
    join_date = models.DateField(auto_now_add=True)
    package_name = models.CharField(max_length=100, choices=PACKAGE_CHOICES)
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)
    duration_months = models.IntegerField(choices=DURATION_CHOICES)
    admission_fees = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MaxValueValidator(10000, message="Admission fees cannot exceed ₹10,000.")]
    )
    total_fees = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MaxValueValidator(100000, message="Total fees cannot exceed ₹100,000.")]
    )
    paid_fees = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    aadhar_document = models.FileField(upload_to='documents/aadhar/', blank=True, null=True)
    pan_document = models.FileField(upload_to='documents/pan/', blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, default='photos/default_user.png')
    active_member = models.BooleanField(default=True)
    subscription_end_date = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ('gym', 'gym_member_id')

    @property
    def calculated_end_date(self):
        if self.join_date and self.duration_months:
            return self.join_date + relativedelta(months=self.duration_months)
        return None

    def save(self, *args, **kwargs):
        if not self.gym_member_id:
            if self.gym:
                last_member = Member.objects.filter(gym=self.gym).order_by('-gym_member_id').first()
                self.gym_member_id = last_member.gym_member_id + 1 if last_member and last_member.gym_member_id else 1
            else:
                self.gym_member_id = 1  # Fallback if gym is not set
        if self.email:
            self.email = self.email.lower()

        # Automatically calculate subscription_end_date before saving
        if self.join_date and self.duration_months:
            self.subscription_end_date = self.join_date + relativedelta(months=self.duration_months)
        else:
            self.subscription_end_date = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def balance_fees(self):
        return self.total_fees - self.paid_fees


# ===== Signal Added to if join_date isn’t available on first save =====

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Member)
def update_subscription_end_date(sender, instance, created, **kwargs):
    if created and instance.join_date and instance.duration_months:
        instance.subscription_end_date = instance.join_date + relativedelta(months=instance.duration_months)
        instance.save(update_fields=['subscription_end_date'])

# ================ Signal Ends ========================

class Staff(models.Model):
    gym = models.ForeignKey('Gym', on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, validators=[name_validator])
    last_name = models.CharField(max_length=50, validators=[name_validator])
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, validators=[phone_validator])
    hire_date = models.DateField(auto_now_add=True)
    position = models.CharField(max_length=100)
    salary = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MaxValueValidator(100000, message="Salary cannot exceed ₹100,000.")]
    )
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)  # <-- new field
    aadhar_document = models.FileField(upload_to='documents/aadhar/', blank=True, null=True)
    pan_document = models.FileField(upload_to='documents/pan/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.position}"


# ======================= Authentication =======================

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class SubscriptionPlan(models.Model):
    PLAN_CHOICES = [
        ('FREE', 'Free'),
        ('STANDARD', 'Standard'),
        ('PREMIUM', 'Premium'),
    ]
    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.get_name_display()} – ₹{self.price:.2f}"



class Gym(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    owner = models.OneToOneField('CustomUser', on_delete=models.CASCADE,related_name='gym')
    phone_number = models.CharField(max_length=15, validators=[phone_validator])
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
