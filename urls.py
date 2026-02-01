from django.contrib import admin
from django.urls import path
from space_app import views as space_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', space_views.HomeView.as_view(), name='home'),
    
    # Миссии
    path('missions/create/', space_views.MissionCreateView.as_view(), name='mission_create'),
    path('missions/<int:pk>/', space_views.MissionDetailView.as_view(), name='mission_detail'),
    path('missions/<int:pk>/edit/', space_views.MissionUpdateView.as_view(), name='mission_update'),
    
    # Астронавты
    path('astronauts/create/', space_views.AstronautCreateView.as_view(), name='astronaut_create'),
    path('astronauts/<int:pk>/', space_views.AstronautDetailView.as_view(), name='astronaut_detail'),
    path('astronauts/<int:pk>/edit/', space_views.AstronautUpdateView.as_view(), name='astronaut_update'),
    
    # Космические корабли
    path('spaceships/create/', space_views.SpaceshipCreateView.as_view(), name='spaceship_create'),
    path('spaceships/<int:pk>/', space_views.SpaceshipDetailView.as_view(), name='spaceship_detail'),
    path('spaceships/<int:pk>/edit/', space_views.SpaceshipUpdateView.as_view(), name='spaceship_update'),
]