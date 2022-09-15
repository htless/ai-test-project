from enum import Enum

class MachineStatus(Enum):
    FREE = 0 
    IN_USE = 1

class ProductionOrderStatus(Enum):
    WAITING = 0
    PRODUCING = 1
    PRODUCED = 2
    
class ProductionOrderStep(Enum):
    FIRST = 0
    FINAL = 1