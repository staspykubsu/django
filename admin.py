from django.contrib import admin
from django.utils.html import format_html
from .models import Astronaut, Spaceship, Mission


class AstronautAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'nationality', 'birth_date', 'age_display')
    list_filter = ('nationality',)  # Должен быть кортеж, а не строка
    search_fields = ('first_name', 'last_name', 'nationality')
    
    def age_display(self, obj):
        from datetime import date
        today = date.today()
        age = today.year - obj.birth_date.year - (
            (today.month, today.day) < (obj.birth_date.month, obj.birth_date.day)
        )
        return f"{age} лет"
    age_display.short_description = 'Возраст'


class SpaceshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'manufacturer', 'launch_date', 'capacity', 'mass', 'is_available')
    list_filter = ('is_available', 'launch_date')
    search_fields = ('name', 'manufacturer')


class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'spaceship', 'status', 'launch_date', 'destination', 'crew_count_display')
    list_filter = ('status', 'launch_date')
    search_fields = ('name', 'destination', 'spaceship__name')
    
    def crew_count_display(self, obj):
        return obj.astronauts.count()
    crew_count_display.short_description = 'Размер экипажа'


# Регистрация моделей в админке
admin.site.register(Astronaut, AstronautAdmin)
admin.site.register(Spaceship, SpaceshipAdmin)
admin.site.register(Mission, MissionAdmin)