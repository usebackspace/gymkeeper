from django.contrib import admin
from .models import Member, Trainer, Staff, Gym, SubscriptionPlan, CustomUser

# -------------------- Member --------------------
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'id','gym_member_id', 'first_name', 'last_name', 'trainer', 'package_name',
        'phone_number', 'email', 'payment_status',
        'join_date', 'subscription_end_date', 'active_member'
    )
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('trainer', 'package_name', 'payment_status', 'active_member')
    ordering = ('-join_date',)


# -------------------- Trainer --------------------
@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'specialty', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('specialty',)
    ordering = ('-hire_date',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        # Only restrict if user is not superuser
        if hasattr(user, "gym") and not user.is_superuser:
            return qs.filter(gym=user.gym)
        return qs



# -------------------- Staff --------------------
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone_number', 'position', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
    list_filter = ('position',)
    ordering = ('-hire_date',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if hasattr(user, "gym") and not user.is_superuser:
            return qs.filter(gym=user.gym)
        return qs




# -------------------- Gym --------------------
@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'phone_number', 'subscription_plan')
    search_fields = ('name', 'owner__email', 'phone_number')
    list_filter = ('subscription_plan',)
    ordering = ('name',)


# -------------------- SubscriptionPlan --------------------
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    ordering = ('price',)


# -------------------- CustomUser --------------------
# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
