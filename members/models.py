from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class AccountDB(models.Model):
    username = models.CharField(max_length=40)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # email = models.EmailField()

class Template(models.Model):
    owner = models.ForeignKey(AccountDB, on_delete=models.CASCADE, default=None)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    id_template = models.IntegerField(default=0)
    id_global = models.IntegerField(default=0)
    male_name = models.CharField(max_length=4, default="default")
    female_name = models.CharField(max_length=40, default="default")
    date = models.DateField(default=datetime.now())
    # time = models.TimeField()

# # class publicTemplate(models.Model):
# #     public_id = models.IntegerChoices()
# # Create your models here.
