from django.db import models

class MyUser(models.Model):   
    Device_id=models.CharField(primary_key=True)                                    
    User_name=models.CharField(max_length=30)
    password = models.CharField(max_length=50, blank=True, null=True)
    Mob=models.BigIntegerField(unique=True)
    Email =models.EmailField()
 

    
    def __str__(self):
        return str(self.Device_id)
    


class Alert(models.Model):
    Device_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    alert_message = models.CharField(max_length=100)
    Time_stamp = models.CharField(max_length=100)