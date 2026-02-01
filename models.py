from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
import re

class Astronaut(models.Model):
    """Модель астронавта"""
    first_name = models.CharField('Имя', max_length=100)
    last_name = models.CharField('Фамилия', max_length=100)
    birth_date = models.DateField('Дата рождения')
    nationality = models.CharField('Национальность', max_length=100)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Астронавт'
        verbose_name_plural = 'Астронавты'
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Spaceship(models.Model):
    """Модель космического корабля"""
    name = models.CharField('Название', max_length=200, unique=True)
    manufacturer = models.CharField('Производитель', max_length=200)
    launch_date = models.DateField('Дата запуска')
    capacity = models.IntegerField('Вместимость (человек)', default=0)
    mass = models.FloatField('Масса (тонны)')
    is_available = models.BooleanField('Доступен', default=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Космический корабль'
        verbose_name_plural = 'Космические корабли'
    
    def __str__(self):
        return self.name


class Mission(models.Model):
    """Модель космической миссии"""
    STATUS_CHOICES = [
        ('Запланирована', 'Запланирована'),
        ('В процессе', 'В процессе'),
        ('Завершена', 'Завершена'),
        ('Провалена', 'Провалена'),
        ('Отменена', 'Отменена'),
    ]
    
    name = models.CharField('Название миссии', max_length=200, unique=True)
    spaceship = models.ForeignKey(
        Spaceship, 
        on_delete=models.PROTECT, 
        verbose_name='Космический корабль',
        related_name='missions'
    )
    astronauts = models.ManyToManyField(
        Astronaut, 
        verbose_name='Экипаж',
        related_name='missions',
        blank=True
    )
    launch_date = models.DateTimeField('Дата и время запуска')
    landing_date = models.DateTimeField('Дата и время посадки', null=True, blank=True)
    status = models.CharField(
        'Статус', 
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='Запланирована'
    )
    destination = models.CharField('Место назначения', max_length=200)
    
    class Meta:
        ordering = ['-launch_date']
        verbose_name = 'Миссия'
        verbose_name_plural = 'Миссии'
    
    def __str__(self):
        return self.name