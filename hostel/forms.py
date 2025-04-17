from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Allocation, User, Room, RoomRequest

class UserRegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']


class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = ['user', 'room', 'check_in']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_superuser=False)
        self.fields['room'].queryset = Room.objects.filter(is_occupied=False)


class RoomRequestForm(forms.ModelForm):
    class Meta:
        model = RoomRequest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'room_type', 'is_occupied']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_type': forms.Select(attrs={'class': 'form-control'}),
            'is_occupied': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }