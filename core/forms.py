# members/forms.py

from django import forms
from .models import Trainer, Member, Staff

from django.core.exceptions import ValidationError

MAX_UPLOAD_SIZE = 2 * 1024 * 1024  # 2MB
ALLOWED_FILE_TYPES = ['application/pdf', 'image/jpeg', 'image/png']
ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png']



class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = '__all__'
        exclude = ['subscription_end_date','gym','gym_member_id']      # exclude end_date explicitly

    def __init__(self, *args, **kwargs):
         # Pop the gym or request from kwargs
        gym = kwargs.pop('gym', None) 
        super(MemberForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control add-member'
            field.widget.attrs['placeholder'] = field.label

        # Filter trainer field queryset by gym if gym provided
        if gym is not None:
            self.fields['trainer'].queryset = Trainer.objects.filter(gym=gym)

        # Mark file fields as optional
        self.fields['aadhar_document'].required = False
        self.fields['pan_document'].required = False
        self.fields['photo'].required = False
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Member.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A member with this email already exists.")
        return email
    
    def clean_aadhar_document(self):
        doc = self.cleaned_data.get('aadhar_document')
        if not doc:
            return self.instance.aadhar_document  # keep existing file if no new upload

        content_type = getattr(doc, 'content_type', None)
        if content_type is not None and content_type not in ALLOWED_FILE_TYPES:
            raise ValidationError("Only PDF, JPEG, and PNG files are allowed.")
        if hasattr(doc, 'size') and doc.size > MAX_UPLOAD_SIZE:
            raise ValidationError("Aadhar document must be less than 2MB.")
        return doc

    def clean_pan_document(self):
        doc = self.cleaned_data.get('pan_document')
        if not doc:
            return self.instance.pan_document  # keep existing file if no new upload

        content_type = getattr(doc, 'content_type', None)
        if content_type is not None and content_type not in ALLOWED_FILE_TYPES:
            raise ValidationError("Only PDF, JPEG, and PNG files are allowed.")
        if hasattr(doc, 'size') and doc.size > MAX_UPLOAD_SIZE:
            raise ValidationError("PAN document must be less than 2MB.")
        return doc

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            return self.instance.photo  # keep existing photo if no new upload

        content_type = getattr(photo, 'content_type', None)
        if content_type is not None and content_type not in ALLOWED_IMAGE_TYPES:
            raise ValidationError("Only JPG or PNG images are allowed.")
        if hasattr(photo, 'size') and photo.size > MAX_UPLOAD_SIZE:
            raise ValidationError("Photo must be less than 2MB.")
        return photo

            
class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ['gym']

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control add-member'
                field.widget.attrs['placeholder'] = field.label

        self.fields['aadhar_document'].required = False
        self.fields['pan_document'].required = False
        self.fields['photo'].required = False

    def clean_aadhar_document(self):
        doc = self.cleaned_data.get('aadhar_document')
        if not doc:
            return self.instance.aadhar_document
        content_type = getattr(doc, 'content_type', None)
        if content_type not in ALLOWED_FILE_TYPES:
            raise ValidationError("Only PDF, JPEG, and PNG files are allowed.")
        if doc.size > MAX_UPLOAD_SIZE:
            raise ValidationError("Aadhar document must be less than 2MB.")
        return doc

    def clean_pan_document(self):
        doc = self.cleaned_data.get('pan_document')
        if not doc:
            return self.instance.pan_document
        content_type = getattr(doc, 'content_type', None)
        if content_type not in ALLOWED_FILE_TYPES:
            raise ValidationError("Only PDF, JPEG, and PNG files are allowed.")
        if doc.size > MAX_UPLOAD_SIZE:
            raise ValidationError("PAN document must be less than 2MB.")
        return doc

class TrainerForm(forms.ModelForm):
    class Meta:
        model = Trainer
        fields = '__all__'
        exclude = ['gym']

    def __init__(self, *args, **kwargs):
        super(TrainerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control add-member'
                field.widget.attrs['placeholder'] = field.label

        self.fields['aadhar_document'].required = False
        self.fields['pan_document'].required = False
        self.fields['photo'].required = False

    def clean_aadhar_document(self):
        doc = self.cleaned_data.get('aadhar_document')
        if not doc:
            return self.instance.aadhar_document
        content_type = getattr(doc, 'content_type', None)
        if content_type not in ALLOWED_FILE_TYPES:
            raise ValidationError("Only PDF, JPEG, and PNG files are allowed.")
        if doc.size > MAX_UPLOAD_SIZE:
            raise ValidationError("Aadhar document must be less than 2MB.")
        return doc

    def clean_pan_document(self):
        doc = self.cleaned_data.get('pan_document')
        if not doc:
            return self.instance.pan_document
        content_type = getattr(doc, 'content_type', None)
        if content_type not in ALLOWED_FILE_TYPES:
            raise ValidationError("Only PDF, JPEG, and PNG files are allowed.")
        if doc.size > MAX_UPLOAD_SIZE:
            raise ValidationError("PAN document must be less than 2MB.")
        return doc

# ===================== Gym Sign Up Form =======================
# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Gym, SubscriptionPlan

class GymSignupForm(UserCreationForm):
    gym_name = forms.CharField(max_length=100, label="Gym Name")
    gym_address = forms.CharField(widget=forms.Textarea, label="Gym Address")
    owner_full_name = forms.CharField(max_length=100, label="Owner Full Name")
    phone_number = forms.CharField(max_length=15, label="Owner Phone Number")
    subscription_plan = forms.ModelChoiceField(queryset=SubscriptionPlan.objects.all(), label="Subscription Plan")

    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('owner_full_name')
        if full_name:
            names = full_name.strip().split(" ", 1)
            user.first_name = names[0]
            user.last_name = names[1] if len(names) > 1 else ''
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

            # Fix subscription plan dropdown loading
        self.fields['subscription_plan'].queryset = SubscriptionPlan.objects.all()