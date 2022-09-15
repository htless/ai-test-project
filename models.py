import datetime
from peewee import *

db = SqliteDatabase('ai.sqlite')

def create_tables():
    with db:
        db.create_tables([Machine, ProductionOrder, Component, Record])

class BaseModel(Model):
    class Meta:
        database = db
        
class Machine(BaseModel):
    status = IntegerField(default=0)
    
class Component(BaseModel):
    name = CharField()
    quantity = IntegerField()
    temperature = IntegerField(null=True)
    pressure = IntegerField(null=True)
    speed = IntegerField(null=True)
    
class ProductionOrder(BaseModel):
    quantity = IntegerField(null=True)
    start = DateTimeField(default=datetime.datetime.now)
    end = DateTimeField(null=True)
    status = IntegerField()
    step = IntegerField()
    machine = ForeignKeyField(Machine, null=True)
    component = ForeignKeyField(Component, null=True)
    
class Record(BaseModel):
    time = DateTimeField(default=datetime.datetime.now)
    status = IntegerField()
    step = IntegerField()
    machine = ForeignKeyField(Machine)
    productionOrder = ForeignKeyField(ProductionOrder)