from django.db import models
from accounts.models import UserAccount


class Note(models.Model):
    user = models.ForeignKey(UserAccount,on_delete=models.CASCADE,null=True)
    note_title = models.TextField(null=True,blank=True)
    note_conntent = models.TextField(null=True,blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.note_title