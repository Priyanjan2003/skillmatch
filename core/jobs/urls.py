from django.urls import path
from .views import dashboard_view
from . import views
from .views import home_view

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('explore/', views.explore_view, name='explore'),
    path('home/', home_view, name='home'),
]
