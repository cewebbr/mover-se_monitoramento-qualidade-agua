from django.urls import path
from . import views

app_name = 'spring-water'

urlpatterns = [
    path('create/', views.create_watersource, name='create_watersource'),
    path('view/<int:id>', views.view_watersource, name='view_watersource'),
    path('remove/', views.remove_watersource, name='remove_watersource'),
]
