from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Allocation, Room
from .forms import AllocationForm
from django.db.models import Q
from .models import RoomRequest
from .forms import RoomRequestForm
from .forms import UserRegisterForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RoomForm
from django.contrib.auth.decorators import login_required, user_passes_test


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)
            return redirect('dashboard')
        else:
            return render(request, 'hostel/login.html', {'error': 'Invalid credentials'})
    return render(request, 'hostel/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    if request.user.is_superuser:
        role = request.GET.get('role')
        room_type = request.GET.get('room_type')
        occupancy = request.GET.get('occupancy')

        allocations = Allocation.objects.select_related('user', 'room')

        if role:
            allocations = allocations.filter(user__role=role)
        if room_type:
            allocations = allocations.filter(room__room_type=room_type)
        if occupancy == 'occupied':
            allocations = allocations.filter(room__is_occupied=True)
        elif occupancy == 'available':
            allocations = allocations.filter(room__is_occupied=False)

        context = {
            'allocations': allocations,
            'selected_role': role,
            'selected_room_type': room_type,
            'selected_occupancy': occupancy
        }
        return render(request, 'hostel/admin_dashboard.html', context)
    else:
        try:
            allocation = Allocation.objects.get(user=request.user)
        except Allocation.DoesNotExist:
            allocation = None
        return render(request, 'hostel/user_dashboard.html', {'allocation': allocation})

@login_required
def allocate_room(request):
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            allocation = form.save()

            # Automatically update room status to occupied
            room = allocation.room
            room.is_occupied = True
            room.save()

            # Update corresponding room request to 'approved'
            RoomRequest.objects.filter(user=allocation.user, status='pending').update(status='approved')

            return redirect('allocation_list')  # or wherever you're redirecting
    else:
        form = AllocationForm()

    return render(request, 'hostel/allocate_room.html', {'form': form})

@login_required
def request_room(request):
    if request.user.is_superuser:
        return redirect('dashboard')

    existing_request = RoomRequest.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if existing_request:
            return render(request, 'hostel/request_room.html', {
                'form': None,
                'existing_request': existing_request,
                'error': 'You have already submitted a request.'
            })
        form = RoomRequestForm(request.POST)
        if form.is_valid():
            room_request = form.save(commit=False)
            room_request.user = request.user
            room_request.save()
            return redirect('dashboard')
    else:
        form = RoomRequestForm()

    return render(request, 'hostel/request_room.html', {
        'form': form,
        'existing_request': existing_request
    })

@login_required
def view_requests(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    requests = RoomRequest.objects.select_related('user')
    return render(request, 'hostel/view_requests.html', {'requests': requests})

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserRegisterForm()
    return render(request, 'hostel/register.html', {'form': form})

def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hostel/room_list.html', {'rooms': rooms})

@login_required
@user_passes_test(is_admin)
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm()
    return render(request, 'hostel/room_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('room_list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'hostel/room_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    return render(request, 'hostel/room_confirm_delete.html', {'room': room})