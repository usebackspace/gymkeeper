from django.shortcuts import render,redirect,get_object_or_404
from . models import Member,Staff,Trainer
from django.db.models import Sum
from django.utils import timezone
import datetime
from .forms import TrainerForm, MemberForm, StaffForm,TrainerForm, StaffForm
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

# ====================================== Help Page =========================================
@login_required
def help_view(request):
    return render(request,'core/help.html')


# ===========================================================================================

# ====================================== Home Page ==========================================
@login_required
def index(request):
    gym = request.user.gym  # Current user's gym

    # Member stats
    all_members = Member.objects.filter(gym=gym)
    active_members = all_members.filter(active_member=True)

    # Category wise
    complete_package_count = active_members.filter(package_name='COMPLETE_PACKAGE').count()
    gym_package_count = active_members.filter(package_name='GYM').count()
    gym_cardio_package_count = active_members.filter(package_name='GYM_CARDIO').count()
    cardio_package_count = active_members.filter(package_name='CARDIO').count()

    # Earnings
    total_earning = all_members.aggregate(total=Sum('paid_fees'))['total'] or 0
    monthly_earning = all_members.filter(
        join_date__year=timezone.now().year,
        join_date__month=timezone.now().month
    ).aggregate(total=Sum('paid_fees'))['total'] or 0

    half_yearly_earning = all_members.filter(
        join_date__gte=timezone.now() - relativedelta(months=6)
    ).aggregate(total=Sum('paid_fees'))['total'] or 0

    yearly_earning = all_members.filter(
        join_date__gte=timezone.now() - relativedelta(years=1)
    ).aggregate(total=Sum('paid_fees'))['total'] or 0

    context = {
        'all_members_count': all_members.count(),
        'active_members_count': active_members.count(),

        # Category wise
        'complete_package_count': complete_package_count,
        'gym_package_count': gym_package_count,
        'gym_cardio_package_count': gym_cardio_package_count,
        'cardio_package_count': cardio_package_count,

        # Earnings
        'total_earning': f"{total_earning:,}",
        'monthly_earning': f"{monthly_earning:,}",
        'half_yearly_earning': f"{half_yearly_earning:,}",
        'yearly_earning': f"{yearly_earning:,}",
    }

    return render(request, 'core/index.html', context)
# ====================================== Member Page ==========================================
from django.core.paginator import Paginator

@login_required
def member(request):
    gym = request.user.gym
    members = Member.objects.filter(active_member=True, gym=gym).order_by('-join_date', '-id')
    paid_members = members.filter(payment_status='PAID')
    pending_members = members.filter(payment_status='PENDING')
    cancelled_members = Member.objects.filter(active_member=False)

    # Paginate each queryset
    paginator_all = Paginator(members, 6)
    paginator_paid = Paginator(paid_members, 6)
    paginator_pending = Paginator(pending_members, 6)
    paginator_cancelled = Paginator(cancelled_members, 6)

    page_number_all = request.GET.get('page_all', 1)
    page_number_paid = request.GET.get('page_paid', 1)
    page_number_pending = request.GET.get('page_pending', 1)
    page_number_cancelled = request.GET.get('page_cancelled', 1)

    page_obj_all = paginator_all.get_page(page_number_all)
    page_obj_paid = paginator_paid.get_page(page_number_paid)
    page_obj_pending = paginator_pending.get_page(page_number_pending)
    page_obj_cancelled = paginator_cancelled.get_page(page_number_cancelled)

    context = {
        'member': page_obj_all,
        'paid_members': page_obj_paid,
        'pending_members': page_obj_pending,
        'cancelled_members': page_obj_cancelled,
        'page_obj_all': page_obj_all,
        'page_obj_paid': page_obj_paid,
        'page_obj_pending': page_obj_pending,
        'page_obj_cancelled': page_obj_cancelled,
        
    }

    return render(request, 'core/member.html', context)

# ======================== Search Member Page ===================================
@login_required
def member_search(request):
    gym = request.user.gym
    query = request.GET.get('q')
    if query:
        member = Member.objects.filter(gym=gym).filter(
            first_name__icontains=query) | Member.objects.filter(gym=gym).filter(last_name__icontains=query)
    else:
        member = Member.objects.filter(gym=gym)

    context = {
        'member': member,
        'query': query,
    }
    return render(request, 'core/member_search.html', context)


# ================= Member Filter By Gym Package ================
@login_required
def member_filter(request):
    gym = request.user.gym
    package_filter = request.GET.get('package_filter', 'option-1')
    time_filter = request.GET.get('time_filter', 'all')

    member = Member.objects.filter(gym=gym)

    if package_filter and package_filter != 'option-1':
        if package_filter == 'option-2':
            member = member.filter(package_name='COMPLETE_PACKAGE')
        elif package_filter == 'option-3':
            member = member.filter(package_name='GYM_CARDIO')
        elif package_filter == 'option-4':
            member = member.filter(package_name='CARDIO')

    now = timezone.now()
    if time_filter == 'this_month':
        member = member.filter(join_date__year=now.year, join_date__month=now.month)
    elif time_filter == 'last_3_months':
        member = member.filter(join_date__gte=now - datetime.timedelta(days=90))
    elif time_filter == 'last_6_months':
        member = member.filter(join_date__gte=now - datetime.timedelta(days=182))

    context = {
        'member': member,
        'package_filter': package_filter,
        'time_filter': time_filter,
    }
    return render(request, 'core/member_search.html', context)


# =============== For CRUD Operation Of Member ================
@login_required
def add_member(request):
    gym = request.user.gym
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, gym=gym)  # pass gym here
        if form.is_valid():
            member = form.save(commit=False)
            member.gym = gym
            member.save()
            return redirect('member')
    else:
        form = MemberForm(gym=gym)  # pass gym here
    return render(request, 'core/add_member.html', {'form': form})


def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_success')
    else:
        form = StaffForm()

    return render(request, 'members/add_staff.html', {'form': form})


#=========================== Document and Profile of the User =================== 
@login_required
def document(request):
    gym = request.user.gym
    members = Member.objects.filter(gym=gym).exclude(photo='')  # Only members with a photo
    return render(request, 'core/docs.html', {'members': members})

@login_required
def member_profile(request, pk):
    gym = request.user.gym
    member = get_object_or_404(Member, pk=pk, gym=gym)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member, gym=gym)  # pass gym here
        if form.is_valid():
            form.save()
            return redirect('member_profile', pk=member.pk)
    else:
        form = MemberForm(instance=member, gym=gym)  # pass gym here

    context = {'member': member, 'form': form}
    return render(request, 'core/member_profile.html', context)

# =============== Adding Staff And Trainer ==================

@login_required
def staff_trainer_list(request):
    gym = request.user.gym
    trainers = Trainer.objects.filter(gym=gym)
    staff = Staff.objects.filter(gym=gym)
    return render(request, 'core/staff.html', {'trainers': trainers, 'staff': staff})

@login_required
def add_trainer(request):
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            trainer = form.save(commit=False)
            trainer.gym = request.user.gym  # ensure correct gym
            trainer.save()
            return redirect('staff_page')
    else:
        form = TrainerForm()
    return render(request, 'core/add_trainer.html', {'form': form})


@login_required
def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.gym = request.user.gym  # ensure correct gym assignment
            staff.save()
            return redirect('staff_page')
    else:
        form = StaffForm()
    return render(request, 'core/add_staff.html', {'form': form})


# ================= Update Trainer And Staff Detail ================
@login_required
def update_trainer(request, pk):
    gym = request.user.gym
    trainer = get_object_or_404(Trainer, pk=pk, gym=gym)
    if request.method == 'POST':
        form = TrainerForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            trainer = form.save(commit=False)
            trainer.gym = gym  # re-enforce gym
            trainer.save()
            return redirect('staff_page')
    else:
        form = TrainerForm(instance=trainer)
    return render(request, 'core/update_trainer.html', {'form': form, 'trainer': trainer})

@login_required
def update_staff(request, pk):
    gym = request.user.gym
    staff = get_object_or_404(Staff, pk=pk, gym=gym)
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.gym = gym  # ensure it cannot be moved to another gym
            staff.save()
            return redirect('staff_page')
    else:
        form = StaffForm(instance=staff)
    return render(request, 'core/update_staff.html', {'form': form, 'staff': staff})

# ========================= Earning View ============================================
@login_required
def earnings_view(request):
    now = timezone.now()
    gym = request.user.gym  # <-- Restrict to logged-in user's gym
    all_members = Member.objects.filter(active_member=True, gym=gym)

    total_earning_num = all_members.aggregate(total_earning=Sum('paid_fees'))['total_earning'] or 0
    seven_days_ago = now - datetime.timedelta(days=7)
    weekly_earning_num = all_members.filter(join_date__gte=seven_days_ago).aggregate(weekly_earning=Sum('paid_fees'))['weekly_earning'] or 0
    monthly_earning_num = all_members.filter(join_date__year=now.year, join_date__month=now.month).aggregate(monthly_earning=Sum('paid_fees'))['monthly_earning'] or 0
    three_months_ago = now - relativedelta(months=3)
    three_months_earning_num = all_members.filter(join_date__gte=three_months_ago).aggregate(three_months_earning=Sum('paid_fees'))['three_months_earning'] or 0
    six_months_ago = now - relativedelta(months=6)
    six_months_earning_num = all_members.filter(join_date__gte=six_months_ago).aggregate(six_months_earning=Sum('paid_fees'))['six_months_earning'] or 0
    one_year_ago = now - relativedelta(years=1)
    yearly_earning_num = all_members.filter(join_date__gte=one_year_ago).aggregate(yearly_earning=Sum('paid_fees'))['yearly_earning'] or 0

    # Package-wise earnings (only for current gym)
    complete_package_earning = all_members.filter(package_name='COMPLETE_PACKAGE').aggregate(total_earning=Sum('paid_fees'))['total_earning'] or 0
    gym_package_earning = all_members.filter(package_name='GYM').aggregate(total_earning=Sum('paid_fees'))['total_earning'] or 0
    gym_cardio_package_earning = all_members.filter(package_name='GYM_CARDIO').aggregate(total_earning=Sum('paid_fees'))['total_earning'] or 0
    cardio_package_earning = all_members.filter(package_name='CARDIO').aggregate(total_earning=Sum('paid_fees'))['total_earning'] or 0

    context = {
        'total_earning': f"{total_earning_num:,}",
        'weekly_earning': f"{weekly_earning_num:,}",
        'monthly_earning': f"{monthly_earning_num:,}",
        'three_months_earning': f"{three_months_earning_num:,}",
        'six_months_earning': f"{six_months_earning_num:,}",
        'yearly_earning': f"{yearly_earning_num:,}",

        # Chart values
        'total_earning_chart': total_earning_num,
        'weekly_earning_chart': weekly_earning_num,
        'monthly_earning_chart': monthly_earning_num,
        'three_months_earning_chart': three_months_earning_num,
        'six_months_earning_chart': six_months_earning_num,
        'yearly_earning_chart': yearly_earning_num,

        # Package-wise earnings
        'complete_package_earning_chart': complete_package_earning,
        'gym_package_earning_chart': gym_package_earning,
        'gym_cardio_package_earning_chart': gym_cardio_package_earning,
        'cardio_package_earning_chart': cardio_package_earning,
    }

    return render(request, 'core/earnings.html', context)

# ==================== Category Wise Member List ==========================
@login_required
def member_list(request):
    gym = request.user.gym
    members = Member.objects.filter(gym=gym).order_by('-join_date')

    package_filter = request.GET.get('package')
    active_filter = request.GET.get('active')

    if package_filter:
        members = members.filter(package_name=package_filter)
    if active_filter == 'true':
        members = members.filter(active_member=True)

    paginator = Paginator(members, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'package_filter': package_filter,
        'active_filter': active_filter,
    }
    return render(request, 'core/member_list.html', context)


# =========================== Account ===================================
@login_required
def account(request):
    return render(request, 'core/account.html')

# =========================== Sign Up ===================================

from django.shortcuts import render, redirect
from .forms import GymSignupForm
from .models import Gym

def gym_signup(request):
    if request.method == 'POST':
        form = GymSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            Gym.objects.create(
                name=form.cleaned_data['gym_name'],
                address=form.cleaned_data['gym_address'],
                owner=user,
                phone_number=form.cleaned_data['phone_number'],
                subscription_plan=form.cleaned_data['subscription_plan']
            )
            return redirect('login')  # or dashboard
    else:
        form = GymSignupForm()
    return render(request, 'core/signup.html', {'form': form})

def gym_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/index/')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'core/login.html')

@login_required
def gym_logout(request):
    logout(request)
    messages.error(request, "You have been logged out.")  # Red alert
    return redirect('login')