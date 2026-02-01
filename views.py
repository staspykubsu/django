from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Astronaut, Spaceship, Mission
from .forms import AstronautForm, SpaceshipForm, MissionForm


class HomeView(ListView):
    """Главная страница со списком миссий"""
    model = Mission
    template_name = 'space_app/home.html'
    context_object_name = 'missions'
    paginate_by = 10


class MissionDetailView(DetailView):
    """Детальная страница миссии"""
    model = Mission
    template_name = 'space_app/mission_detail.html'
    context_object_name = 'mission'


class AstronautDetailView(DetailView):
    """Детальная страница астронавта"""
    model = Astronaut
    template_name = 'space_app/astronaut_detail.html'
    context_object_name = 'astronaut'


class SpaceshipDetailView(DetailView):
    """Детальная страница космического корабля"""
    model = Spaceship
    template_name = 'space_app/spaceship_detail.html'
    context_object_name = 'spaceship'


class MissionCreateView(CreateView):
    """Создание новой миссии"""
    model = Mission
    form_class = MissionForm
    template_name = 'space_app/mission_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Миссия успешно создана!')
        return super().form_valid(form)


class MissionUpdateView(UpdateView):
    """Редактирование миссии"""
    model = Mission
    form_class = MissionForm
    template_name = 'space_app/mission_form.html'
    
    def get_success_url(self):
        return reverse_lazy('mission_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Миссия успешно обновлена!')
        return super().form_valid(form)


class AstronautCreateView(CreateView):
    """Создание нового астронавта"""
    model = Astronaut
    form_class = AstronautForm
    template_name = 'space_app/astronaut_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Астронавт успешно создан!')
        return super().form_valid(form)

class AstronautUpdateView(UpdateView):
    """Редактирование миссии"""
    model = Astronaut
    form_class = AstronautForm
    template_name = 'space_app/astronaut_form.html'
    
    def get_success_url(self):
        return reverse_lazy('astronaut_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Астронавт успешно обновлен!')
        return super().form_valid(form)

class SpaceshipCreateView(CreateView):
    """Создание нового космического корабля"""
    model = Spaceship
    form_class = SpaceshipForm
    template_name = 'space_app/spaceship_form.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Космический корабль успешно создан!')
        return super().form_valid(form)

class SpaceshipUpdateView(UpdateView):
    """Редактирование миссии"""
    model = Spaceship
    form_class = SpaceshipForm
    template_name = 'space_app/spaceship_form.html'
    
    def get_success_url(self):
        return reverse_lazy('spaceship_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Корабль успешно обновлен!')
        return super().form_valid(form)