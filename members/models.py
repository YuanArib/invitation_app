from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

class AccountDB(models.Model):
    username = models.CharField(max_length=40)
    # username_name = models.CharField(max_length=40)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # email = models.EmailField()
    def __str__(self):
        return self.username

class Template(models.Model):
    owner = models.ForeignKey(AccountDB, on_delete=models.CASCADE, default=None)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    id_template = models.IntegerField(default=0)
    id_global = models.IntegerField(default=0)
    male_name = models.CharField(max_length=40, default="default")
    female_name = models.CharField(max_length=40, default="default")
    # date_end = models.DateField(default=datetime.now())
    date = models.DateField(default=datetime.now())

    # def __str__(self):
    #     return "%s, %s & %s" % (self.id_global, self.male_name, self.female_name)
    # time = models.TimeField()

class Template_Event(models.Model):
    template_id = models.IntegerField(default=0)
    event_id = models.IntegerField(default=0)
    name = models.CharField(max_length=40, default="default")
    description = models.CharField(max_length=200, default="default")
    date_start = models.DateField(default=datetime.now())
    date_end = models.DateField(default=datetime.now())
    address = models.CharField(max_length=200, default="default")

# # class publicTemplate(models.Model):
# #     public_id = models.IntegerChoices()
# # Create your models here.
