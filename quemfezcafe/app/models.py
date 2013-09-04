# coding: utf-8
from django.db import models
from django.contrib.auth.models import User

from datetime import date, datetime


# Create your models here.

# HOrario de verão
# timezone = 2

#Horario Normal
timezone = 3

def por_count(item):
    return item.get('count','')


class RegistraCafe(models.Model):
    
    user = models.ForeignKey(User)
    date_creation = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return '%s - %s ' % (self.user.email, self.date_creation)

    @classmethod
    def getAll(self, limit=0):
        return RegistraCafe.objects.all().order_by("-date_creation")

    @classmethod
    def getJaFez(self):
        now = datetime.now()

        if now.hour-timezone < 12:
            start_date = datetime(now.year,now.month,now.day,0,0,0)
            end_date = datetime(now.year,now.month,now.day,12,0,0)
        else:
            start_date = datetime(now.year,now.month,now.day,12,0,0)
            end_date = datetime(now.year,now.month,now.day,23,59,0)

        result = RegistraCafe.objects.filter(date_creation__range=[start_date, end_date])

        return result.count()

    @classmethod
    def getQuantidadeCafe(self):
        dados = self.getAll()

        L = []
        for item in dados:
            D = {}
            result = RegistraCafe.objects.filter(user=item.user)

            D['user_email'] = item.user.email
            D['count'] = result.count()

            if not D in L:
                L.append(D)

        return sorted(L, key=por_count,reverse=True)
      

    @property
    def dateTimeText(self):
        return self.date_creation.strftime("%d.%m.%Y  - %H:%M")


    @property
    def userName(self):
        return self.user.email

    
