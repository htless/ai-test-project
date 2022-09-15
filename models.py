from dataclasses import dataclass
import datetime
from peewee import *

db = SqliteDatabase('ai.sqlite')

def create_tables():
    with db:
        db.create_tables([Machine, ProductionOrder, Record])

class BaseModel(Model):
    class Meta:
        database = db
        
class Machine(BaseModel):
    status = IntegerField(default=0)
    temperature = IntegerField(null=True)
    pressure = IntegerField(null=True)
    speed = IntegerField(null=True)
    
class ProductionOrder(BaseModel):
    component = CharField()
    quantity = IntegerField()
    start = DateTimeField(default=datetime.datetime.now)
    end = DateTimeField(null=True)
    status = IntegerField()
    step = IntegerField()
    
class Record(BaseModel):
    time = DateTimeField(default=datetime.datetime.now)
    status = IntegerField()
    machine = ForeignKeyField(Machine)
    productionOrder = ForeignKeyField(ProductionOrder)