from google.appengine.ext import db

from datetime import date, datetime

timezone = 3

def por_count(item):
    return item.get('count','')

class RegistraCafe(db.Model):
    
  user = db.UserProperty()
  date_creation = db.DateTimeProperty()
    
  @classmethod
  def getAll(self):
    filter = db.GqlQuery("SELECT * FROM RegistraCafe ORDER BY date_creation DESC")

    return filter #RegistraCafe.all() #.fetch(100)

  @classmethod
  def getJaFez(self):
      now = datetime.now()
      
      if now.hour-timezone < 12:
          start_date = datetime(now.year,now.month,now.day,0,0,0)
          end_date = datetime(now.year,now.month,now.day,12,0,0)
      else:
          start_date = datetime(now.year,now.month,now.day,12,0,0)
          end_date = datetime(now.year,now.month,now.day,23,59,0)
    
      
      result = RegistraCafe.all().filter("date_creation >=", start_date).filter("date_creation <=", end_date)
      return result.count()

  @classmethod
  def getQuantidadeCafe(self):
      dados = self.getAll()
      
      L = []
      for item in dados:
          D = {}
          result =  RegistraCafe.all().filter('user =',item.user)
          D['user'] = item.user
          D['count'] = result.count()
          
          if not D in L:
            L.append(D)
      
      return sorted(L, key=por_count)
      

  @property
  def dateTimeText(self):
    return self.date_creation.strftime("%d.%m.%Y  - %H:%M")


  @property
  def userName(self):
    return self.user.email()

    