import datetime
from models import Machine, ProductionOrder, Component, Record, create_tables
from enums import MachineStatus, ProductionOrderStatus, ProductionOrderStep

def storeRecord(productionOrder):
    Record.insert(
        time=datetime.datetime.now(),
        status=productionOrder.status,
        step=productionOrder.step,
        machine=productionOrder.machine,
        productionOrder=productionOrder
    ).execute()

def allocateMachine(productionOrder, quantity):
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
    ).execute()
    
    print('Ordem de produção criada\n')
    
    storeRecord(productionOrder)

    print('Ordem de produção em processamento')
    print(f'Máquina {machine.id} ocupada')
    print('------------------------')
        
def nextStep(productionOrder):
    productionOrder.update(step=ProductionOrderStep.FINAL.value).execute()
    storeRecord(productionOrder)
    
def finish(productionOrder):
    productionOrder.update(status=ProductionOrderStatus.PRODUCED.value).execute()
    storeRecord(productionOrder)

def listProductionOrders():
    for productionOrder in ProductionOrder.select():
        print(f'Ordem de produção {productionOrder.id} - '\
            f'Quantidade: {productionOrder.quantity} - '\
            f'Componente: {productionOrder.component.name}')
        
def listComponents():
    for component in Component.select():
        print(f'Componente: {component.id} - '\
            f'Quantidade necesária: {component.quantity}')
        
        
def readBarCode():
    try:
        readline = input("Insira a leitura do código de barras: \n");
        productionOrderId = int(readline[0]);
        quantity = int(readline[0:2]);
        
        productionOrder = ProductionOrder.get(ProductionOrder.id == productionOrderId)

        if(productionOrder.status == ProductionOrderStatus.WAITING.value):
            allocateMachine(productionOrder, quantity)
        elif(productionOrder.step == ProductionOrderStep.FIRST):
            nextStep(productionOrder)   
        else:
            finish()     
    except IndexError:
        print('Código de barras inválido') 
    
def menu():
    print('Manufacturing Execution System')
    print('1 - Cadastrar Ordem de Produção')
    print('2 - Cadastrar Componente')
    print('3 - Listar Ordens de Produção')
    print('4 - Listar Componentes')
    print('5 - Ler Ordem de Produção')
    print('0 - Sair')

def run():
    while choice != 0:
        menu()
        choice = int(input('Digite uma opção: '))

if __name__ == '__main__':
    create_tables();
    run();