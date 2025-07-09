from .models import *
from django.contrib import admin

@admin.register(MyUser)
class MyUser(admin.ModelAdmin):
    list_display = ('Device_id','User_name','Mob','Email','password')
    
    
@admin.register(Alert)
class Alert(admin.ModelAdmin):
    list_display = ('Device_id','alert_message', 'Time_stamp')
    