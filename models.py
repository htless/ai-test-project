from peewee import *

db = SqliteDatabase('ai.db')

class BaseModel(Model):
    class Meta:
        database = db
        
class Machine(BaseModel):
    name = CharField(unique=True)
    status = IntegerField()
    temperature = IntegerField()
    pressure = IntegerField()
    speed = IntegerField()
    
class ProductionOrder(BaseModel):
    component = CharField()
    quantity = IntegerField()
    start = DateTimeField()
    status = IntegerField()
    step = IntegerField()
    
class Registry(BaseModel):
    time = DateTimeField()
    status = IntegerField()
    machine = ForeignKeyField(Machine)
    productionOrder = ForeignKeyField(ProductionOrder)