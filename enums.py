from enum import Enum

class MachineStatus(Enum):
    FREE = 0 
    IN_USE = 1

class ProductionOrderStatus(Enum):
    WAITING = 1
    PRODUCING = 2
    PRODUCED = 3
    
class ProductionOrderStep(Enum):
    FIRST = 0
    FINAL = 1