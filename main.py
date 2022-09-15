import datetime
from models import Machine, ProductionOrder, Component, Record, create_tables
from enums import MachineStatus, ProductionOrderStatus, ProductionOrderStep

def run():
    readline = input("Insira a leitura do código de barras: \n");

    try:
        productionOrderId = int(readline[0]);
        quantity = int(readline[0:2]);
        
        productionOrder = ProductionOrder.get(ProductionOrder.id == productionOrderId)
        component = productionOrder.component
        
        print('\n------------------------')
        print(f'Componente: {component.name}');
        print(f'Quantidade: {quantity}');
        print(f'Temperatura: {component.temperature}');
        print(f'Pressão: {component.pressure}');
        print(f'Velocidade {component.speed}')
        
        machine = Machine.get(Machine.status == MachineStatus.FREE.value)
        machine.status = MachineStatus.IN_USE.value
        machine.save()
        
        print('\nMáquina configurada e pronta')
        
        productionOrder = ProductionOrder.update(
            start=datetime.datetime.now(),
            status=ProductionOrderStatus.PROCESSING.value,
            step=ProductionOrderStep.FIRST.value,
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