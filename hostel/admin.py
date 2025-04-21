from django.contrib import admin
from .models import User, Room, Allocation, RoomRequest

admin.site.register(User)
admin.site.register(Room)
admin.site.register(Allocation)
admin.site.register(RoomRequest)