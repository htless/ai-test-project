import datetime
from models import Machine, ProductionOrder, Component, Record, create_tables
from enums import MachineStatus, ProductionOrderStatus

def run():
    readline = input("Insira a leitura do código de barras: \n");

    try:
        id = int(readline[0]);
        quantity = int(readline[0:2]);
        temperature = int(readline[2:4])
        pressure = int(readline[4:6])
        speed = int(readline[6:8]) 
        
        component = Component.get(Component.id == id)
        
        print('\n------------------------')
        print(f'Componente: {component.name}');
        print(f'Quantidade: {quantity}');
        print(f'Temperatura: {temperature}');
        print(f'Pressão: {pressure}');
        print(f'Velocidade {speed}')
        
        machine = Machine.get(Machine.status == MachineStatus.FREE.value)
        
        machine.temperature = temperature
        machine.pressure = pressure
        machine.speed = speed
        machine.status = MachineStatus.IN_USE.value
        
        machine.save()
        
        print('\nMáquina configurada e pronta')
        
        productionOrder = ProductionOrder.create(
            start=datetime.datetime.now(),
            status=ProductionOrderStatus.PROCESSING.value,
            step=0,
            component=component,
            machine=machine
        )
        
        print('Ordem de produção criada\n')
        
        Record.insert(
            time=datetime.datetime.now(),
            status=productionOrder.status,
            machine=machine,
            productionOrder=productionOrder
        ).execute()

        print('Ordem de produção em processamento')
        print(f'Máquina {machine.id} ocupada')
        print('------------------------')
        
    except IndexError:
        print('Código de barras inválido')

if __name__ == '__main__':
    create_tables();
    run();