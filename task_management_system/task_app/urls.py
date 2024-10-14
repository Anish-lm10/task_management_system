from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',log_in,name='log_in'),
    path('signup/',sign_up,name='sign_up'),
    path('logout/',log_out,name='log_out'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='myhtml/auth/change_password.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='myhtml/auth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='myhtml/auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='myhtml/auth/password_reset_complete.html'), name='password_reset_complete'),

    path('dashboard/',home,name='home'),
    path('tasks/create',create,name='create'),
    path('tasks/view',view,name='view'),
    path('tasks/assign',assign,name='assign'),
    path('tasks/assigned',assigned,name='assigned'),
    path('tasks/completed_task',completed_task,name='completed_task'),
    path('tasks/trash',trash,name='trash'),

    path('completed/<int:id>',completed,name='completed'),
    path('acompleted/<int:id>',acompleted,name='acompleted'),
    path('deleted/<int:id>',deleted,name='deleted'),
    path('edit/<int:id>',edit,name='edit'),

    path('recycle/<int:id>',recycle,name='recycle'),
    path('my_delete_all/',my_delete_all,name='my_delete_all'),
    path('assign_delete_all/',assign_delete_all,name='assign_delete_all'),
]