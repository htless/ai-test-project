import datetime
from models import *
from enums import *

def storeRecord(productionOrder):
    Record.insert(
        time=datetime.datetime.now(),
        status=productionOrder.status,
        step=productionOrder.step,
        machine=productionOrder.machine,
        productionOrder=productionOrder).execute()

def allocateMachine(productionOrder):
    component = productionOrder.component
    
    print('\n------------------------')
    print(f'Ordem de produção {productionOrder.id} - Quantidade: {productionOrder.quantity}')
    
    print(f'Componente: {component.name}')
    print(f'Temperatura: {component.temperature}')
    print(f'Pressão: {component.pressure}')
    print(f'Velocidade {component.speed}')
    print(f'Quantidade: {component.quantity}')
    
    try:
        machine = Machine.get(Machine.status == MachineStatus.FREE.value, Machine.id != 3)
        machine.status = MachineStatus.IN_USE.value
        machine.save()
        
        print('\nMáquina configurada e pronta')
    
        productionOrder.start = datetime.datetime.now()
        productionOrder.status = ProductionOrderStatus.PRODUCING.value
        productionOrder.step = ProductionOrderStep.FIRST.value
        productionOrder.machine = machine
        
        productionOrder.save()
        
        print('Ordem de produção atualizada\n')
        
        storeRecord(productionOrder)

        print('Ordem de produção em processamento. Status: Produzindo')
        print(f'Máquina {machine.id} ocupada')
        print('------------------------')
    except DoesNotExist:
        print('\nNenhuma máquina liberada no momento')

def setMachineStatus(machine, status):
    machine.status = status.value
    machine.save()
    
def lastMachineBeingUsed():
    machine = Machine.get(Machine.id == 3)
    print(machine, machine.status)
    if(machine.status == MachineStatus.IN_USE.value):
        return True
    return False
        
def nextStep(productionOrder):
    if(lastMachineBeingUsed()):
        print('\nA máquina de finalização está sendo utilizada')
        return
    
    setMachineStatus(productionOrder.machine, MachineStatus.FREE)
    
    productionOrder.step = ProductionOrderStep.FINAL.value
    productionOrder.machine = 3
    productionOrder.save()
    
    setMachineStatus(productionOrder.machine, MachineStatus.IN_USE)

    storeRecord(productionOrder)
    
    print(f'\nOrdem de produção {productionOrder.id} foi para etapa final de produção. Status: Produzindo')
    
def finish(productionOrder):
    productionOrder.status = ProductionOrderStatus.PRODUCED.value
    productionOrder.end = datetime.datetime.now()
    productionOrder.save()
    
    print(f'\nOrdem de produção {productionOrder.id} finalizada. Status: Produzida')
    
    setMachineStatus(productionOrder.machine, MachineStatus.FREE)
    
    storeRecord(productionOrder)

def listProductionOrders():
    print(f"\nListagem de ordens de produção:")
    for productionOrder in ProductionOrder.select():
        print(f'Ordem de produção {productionOrder.id} - '\
            f'Quantidade: {productionOrder.quantity} - '\
            f'Componente: {productionOrder.component.name} - '\
            f'Status: {ProductionOrderStatus(productionOrder.status).name}')
        
def listComponents():
    print(f"\nListagem de componentes:")
    for component in Component.select():
        print(f'Componente: {component.id} - '\
            f'Quantidade necesária: {component.quantity}')
   
def createProductionOrder():
    code = input('\nInsira o código para cadastro: ')
    status = ProductionOrderStatus.WAITING.value
    step = ProductionOrderStep.FIRST.value
    quantity = input('Insira a quantidade: ')
    componentId = input('Insira o código do componente: ')
    component = Component.get(Component.id == componentId)
    
    productionOrder = ProductionOrder.create(id=code, 
        quantity=quantity, 
        status=status, 
        step=step,
        component=component)
    
    print(f"\nOrdem de produção criada com o id: {productionOrder.id}. Status: EM FILA")
        
def createComponent():
    name = input('Insira o nome do componente: ')
    quantity = input('Insira a quantidade: ')
    temperature = input('Insira a temperatura: ')
    pressure = input('Insira a pressão: ')
    speed = input('Insira a velocidade: ')
    
    component = Component.create(name=name, 
        quantity=quantity,
        temperature=temperature,
        pressure=pressure,
        speed=speed)
    
    print(f"\nComponente criado com o id: {component.id}")
    
def readBarCode():
    try:
        productionOrderId = input("Insira a leitura do código de barras: ")
        productionOrder = ProductionOrder.get(ProductionOrder.id == productionOrderId)

        if(productionOrder.status == ProductionOrderStatus.WAITING.value):
            allocateMachine(productionOrder)
        elif(productionOrder.step == ProductionOrderStep.FIRST.value):
            nextStep(productionOrder)   
        else:
            finish(productionOrder)     
    except IndexError:
        print('Código de barras inválido') 
        
def productionRate():
    ano = int(input('Insira o ano da consulta: '))
    mes = int(input('Insira o número do mês da consulta: '))
    dia = int(input('Insira o dia da consulta: '))

def leadtime():
    ano = int(input('Insira o ano da consulta: '))
    mes = int(input('Insira o número do mês da consulta: '))
    dia = int(input('Insira o dia da consulta: '))
    
def menu():
    print('\n Manufacturing Execution System\n')
    print('1 - Cadastrar Ordem de Produção')
    print('2 - Cadastrar Componente')
    print('3 - Listar Ordens de Produção')
    print('4 - Listar Componentes')
    print('5 - Ler Ordem de Produção')
    print('6 - Relatório taxa de produção')
    print('7 - Relatório leadtime')
    print('0 - Sair')

def execute(choice):
    if(choice == 1):
        createProductionOrder()
    elif(choice == 2):
        createComponent()
    elif(choice == 3):
        listProductionOrders()
    elif(choice == 4):
        listComponents()
    elif(choice == 5):
        readBarCode()
    elif(choice == 6):
        productionRate()
    elif(choice == 7):
        leadtime()
    elif(choice == 0):
        print('\nEncerrando sistema')
    else:
        print('Opção não encontrada')

def run():
    choice = 1
    while choice != 0:
        menu()
        choice = int(input('\nDigite uma opção: '))
        execute(choice)

if __name__ == '__main__':
    create_tables()
    create_machines()
    run()