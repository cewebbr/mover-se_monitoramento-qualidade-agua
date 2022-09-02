from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.map, name='map'),
    path('ajax/searchPointer/', views.searchPointer, name='search'),
    path('perfil/<int:id>', views.perfil, name='perfil'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.register, name='register'),
    path('about/', views.about, name='about'),
    path('sw.js', (TemplateView.as_view(template_name='sw.js',
         content_type='application/javascript')), name='sw.js')
]
