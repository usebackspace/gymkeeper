from django.urls import path
from . import views
#------ To incude Media file ---------------
from django.conf import settings
from django.conf.urls.static import static
#-----------------------------------------------

urlpatterns = [
    # Member URLs
    path('add-member/', views.add_member, name='add_member'),
    path('members/list/', views.member_list, name='member_list'),
    path('member/<int:pk>/', views.member_profile, name='member_profile'),
    path('member/', views.member, name='member'),
    path('search/', views.member_search, name='member_search'),
    path('filter/', views.member_filter, name='member_filter'),

    # Trainer URLs
    path('add-trainer/', views.add_trainer, name='add_trainer'),
    path('trainer/<int:pk>/update/', views.update_trainer, name='update_trainer'),

    # Staff URLs
    path('add-staff/', views.add_staff, name='add_staff'),
    path('staff/<int:pk>/update/', views.update_staff, name='update_staff'),

    # Others
    path('index/', views.index, name='index'),
    path('staff-page/', views.staff_trainer_list, name='staff_page'),
    path('doc/', views.document, name='document'),
    path('earnings/', views.earnings_view, name='earnings'),
    path('account/', views.account, name='account'),
    path('help/', views.help_view, name='help'),
    path('signup/', views.gym_signup, name='signup'),
    path('', views.gym_login, name='login'),
    path('logout/', views.gym_logout, name='logout'),


]



#--------- THis is will add file to media folder -----------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)