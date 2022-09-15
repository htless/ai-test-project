from enum import Enum

class MachineStatus(Enum):
    FREE = 0 
    IN_USE = 1

class ProductionOrderStatus(Enum):
    WAITING = 1
    PROCESSING = 2
    PRODUCING = 3
    PRODUCED = 4
    
class ProductionOrderStep(Enum):
    FIRST = 0
    FINAL = 1