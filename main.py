import datetime
from models import Machine, ProductionOrder
from enums import MachineStatus, ProductionOrderStatus

components = [
  'Aço',
  'Borracha',
  'Batata'
];

readline = input("Insira a leitura do código de barras: \n");

try:
    id = int(readline[0]);
    quantity = int(readline[0:2]);
    temperature = int(readline[2:4])
    pressure = int(readline[4:6])
    speed = int(readline[6:8]) 
    
    print('\n------------------------')
    print(f'Componente: {components[id]}');
    print(f'Quantidade: {quantity}');
    print(f'Temperatura: {temperature}');
    print(f'Pressão: {pressure}');
    print(f'Velocidade {speed}')
    
    machine = Machine.get(Machine.status == MachineStatus.FREE);
    
    machine.temperature = temperature
    machine.pressure = pressure
    machine.speed = speed
    machine.status = MachineStatus.IN_USE
    
    machine.save()
    
    print('\nMáquina configurada e pronta\n')
    
    productionOrder = {
        'component': components[id],
        'quantity': quantity,
        'start': datetime(),
        'status': ProductionOrderStatus.PROCESSING,
        'step': 0,
        'machine': machine
    }

    productionOrder = ProductionOrder.create(productionOrder)
    
    registry = {
        'time': datetime(),
        'status': productionOrder.status,
        'machine': machine,
        'productionOrder': productionOrder
    }

    print('\n Ordem de produção em processamento')
    print(f'Máquina {machine.id} ocupada')
    print('------------------------')
    
except IndexError:
    print('Código de barras inválido')
except: 
    print('Erro iniciar operação');

