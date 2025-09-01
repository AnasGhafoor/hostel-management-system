from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Rooms URLs
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_add, name='room_add'),
    path('rooms/edit/<int:pk>/', views.room_edit, name='room_edit'),
    path('rooms/delete/<int:pk>/', views.room_delete, name='room_delete'),

    # Students URLs
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<int:pk>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),

    # Payments URLs
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.payment_add, name='payment_add'),
    path('payments/edit/<int:pk>/', views.payment_edit, name='payment_edit'),
    path('payments/delete/<int:pk>/', views.payment_delete, name='payment_delete'),
]
