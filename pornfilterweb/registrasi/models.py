from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Registrasi(models.Model):
    mode = models.TextField()
    ip = models.TextField()

    def __unicode__(self):
        return self.ip+' - '+self.mode