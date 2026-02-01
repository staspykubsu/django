from django import forms
from django.core.exceptions import ValidationError
from .models import Astronaut, Spaceship, Mission
from datetime import date, datetime
import re

class AstronautForm(forms.ModelForm):
    class Meta:
        model = Astronaut
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Выберите дату рождения'
                }
            ),
            'biography': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите национальность'}),
        }
        labels = {
            'first_name': 'Имя астронавта',
            'last_name': 'Фамилия астронавта',
            'birth_date': 'Дата рождения',
            'nationality': 'Национальность',
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()
        if len(first_name) < 2:
            raise ValidationError('Имя должно содержать минимум 2 символа')
        if not first_name.isalpha():
            raise ValidationError('Имя может содержать только буквы')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()
        if len(last_name) < 2:
            raise ValidationError('Фамилия должна содержать минимум 2 символа')
        if not last_name.isalpha():
            raise ValidationError('Фамилия может содержать только буквы')
        return last_name

    def clean_nationality(self):
        nationality = self.cleaned_data.get('nationality', '').strip()
        if len(nationality) < 2:
            raise ValidationError('Национальность должна содержать минимум 2 символа')
        if not nationality.isalpha():
            raise ValidationError('Национальность может содержать только буквы')
        return nationality

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date > date.today():
            raise ValidationError('Дата рождения не может быть в будущем')
            
        age = date.today().year - birth_date.year
        if age < 18:
            raise ValidationError('Астронавт должен быть старше 18 лет')
        
        return birth_date


class SpaceshipForm(forms.ModelForm):
    class Meta:
        model = Spaceship
        fields = '__all__'
        widgets = {
            'launch_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Выберите дату запуска'
                }
            ),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название корабля'}),
            'manufacturer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите производителя'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Введите вместимость'}),
            'mass': forms.NumberInput(attrs={'class': 'form-control', 'min': '0.1', 'step': '0.1', 'placeholder': 'Введите массу в тоннах'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Название корабля',
            'manufacturer': 'Производитель',
            'launch_date': 'Дата запуска',
            'capacity': 'Вместимость (человек)',
            'mass': 'Масса (тонны)',
            'is_available': 'Доступен для миссий',
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise ValidationError('Название корабля должно содержать минимум 2 символа')
        return name

    def clean_manufacturer(self):
        manufacturer = self.cleaned_data.get('manufacturer', '').strip()
        if len(manufacturer) < 2:
            raise ValidationError('Название производителя должно содержать минимум 2 символа')
        if not re.match(r'^[A-Za-zА-Яа-яЁё0-9\-\s\(\)\.]+$', manufacturer):
            raise ValidationError('Название производителя может содержать только буквы, цифры, тире, пробелы, скобки и точки')
        return manufacturer

    def clean_launch_date(self):
        launch_date = self.cleaned_data.get('launch_date')
        if launch_date > date.today():
            raise ValidationError('Дата запуска не может быть в будущем')
        return launch_date

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if capacity < 0:
            raise ValidationError('Вместимость не может быть отрицательной')
        return capacity

    def clean_mass(self):
        mass = self.cleaned_data.get('mass')
        if mass <= 0:
            raise ValidationError('Масса должна быть положительной')
        return mass


class MissionForm(forms.ModelForm):
    # Кастомное поле для выбора астронавтов
    astronauts = forms.ModelMultipleChoiceField(
        queryset=Astronaut.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '6'}),
        required=False,
        label='Экипаж'
    )
    
    class Meta:
        model = Mission
        fields = '__all__'
        widgets = {
            'launch_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'Выберите дату и время запуска'
                }
            ),
            'landing_date': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'placeholder': 'Выберите дату и время посадки'
                }
            ),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название миссии'}),
            'spaceship': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите место назначения'}),
        }
        labels = {
            'name': 'Название миссии',
            'spaceship': 'Космический корабль',
            'launch_date': 'Дата и время запуска',
            'landing_date': 'Дата и время посадки',
            'status': 'Статус миссии',
            'destination': 'Место назначения',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем начальные значения для выбора астронавтов
        if self.instance and self.instance.pk:
            self.fields['astronauts'].initial = self.instance.astronauts.all()
        # Фильтруем доступные корабли
        self.fields['spaceship'].queryset = Spaceship.objects.filter(is_available=True)

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise ValidationError('Название миссии должно содержать минимум 2 символа')
        if not name.replace(' ', '').isalpha():
            raise ValidationError('Название миссии может содержать только буквы и пробелы')
        return name

    def clean_destination(self):
        destination = self.cleaned_data.get('destination', '').strip()
        if len(destination) < 2:
            raise ValidationError('Место назначения должно содержать минимум 2 символа')
        if not destination.replace(' ', '').isalpha():
            raise ValidationError('Место назначения может содержать только буквы и пробелы')
        return destination

    def clean(self):
        cleaned_data = super().clean()
        launch_date = cleaned_data.get('launch_date')
        landing_date = cleaned_data.get('landing_date')
        spaceship = cleaned_data.get('spaceship')
        status = cleaned_data.get('status')
        astronauts = cleaned_data.get('astronauts', [])

        # Проверка дат
        if landing_date and launch_date:
            if landing_date <= launch_date:
                self.add_error('landing_date', 'Дата посадки должна быть позже даты запуска')

        # Проверка доступности корабля
        if spaceship and status not in ['Запланирована', 'Отменена']:
            if not spaceship.is_available:
                self.add_error('spaceship', 'Корабль должен быть доступен для выполнения миссии')
            
            # Проверка, что корабль не используется в других активных миссиях
            active_missions = Mission.objects.filter(
                spaceship=spaceship,
                status__in=['Запланирована', 'В процессе']
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if active_missions.exists():
                self.add_error('spaceship', 'Этот корабль уже используется в другой активной миссии')

        # Проверка вместимости корабля
        if spaceship and astronauts:
            if len(astronauts) > spaceship.capacity:
                self.add_error('astronauts', f'Корабль вмещает только {spaceship.capacity} человек. Выбрано: {len(astronauts)}')

        # Проверка, что астронавт не участвует в двух миссиях одновременно
        if astronauts and launch_date and landing_date:
            for astronaut in astronauts:
                conflicting_missions = Mission.objects.filter(
                    astronauts=astronaut,
                    status__in=['Запланирована', 'В процессе'],
                    launch_date__lt=landing_date,
                    landing_date__gt=launch_date
                ).exclude(pk=self.instance.pk if self.instance else None)
                
                if conflicting_missions.exists():
                    self.add_error('astronauts', f'Астронавт {astronaut} уже участвует в другой миссии в это время')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        
        # Сохраняем связи с астронавтами
        if 'astronauts' in self.cleaned_data:
            instance.astronauts.set(self.cleaned_data['astronauts'])
        
        return instance