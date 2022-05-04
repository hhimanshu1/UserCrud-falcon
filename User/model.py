from peewee import *

db=PostgresqlDatabase('mydb',user='hhimanshu',password='hhimanshu',host='localhost')



class BaseModel(Model):
    class Meta:
        database=db

class User(BaseModel):
    id=AutoField()
    username=CharField()
    role=CharField(default='user')
    firstName=CharField()
    lastName=CharField()
    age=IntegerField()
    password=CharField()

    class Meta:
        db_table='userhhimanshu'


class PeeweeConnectionMiddleware(object):
    def process_request(self,req,resp):
        db.connect()

    def process_response(self,req,resp,resource,req_succeeded):
        if not db.is_closed:
            db.close()