# gerenciamento de lista de tarefas
def menu():
    print('\nBem-vindo ao gerenciador de tarefas!')
    print('1. adicionar tarefa')
    print('2. listar todas as tarefas')
    print('3. remover tarefa')
    print('4. sair')

def adicionar_tarefa(tarefas):
    tarefa = input('Digite a tarefa que deseja adicionar: ')
    tarefas.append(tarefa)
    print(f'Tarefa "{tarefa}" adicionada com sucesso!')

def listar_tarefas(tarefas): 
    # função para listar as tarefas, verificando se a lista está vazia ou não, e exibindo as tarefas numeradas.
    if not tarefas:
        print("\nSua lista está vazia.")
    else:
        print("\n--- Suas Tarefas ---")
        for i, tarefa in enumerate(tarefas, start=1):
            print(f"{i}. {tarefa}")

def remover_tarefa(tarefas):
    listar_tarefas(tarefas)
    if tarefas: 
        try: 
            indice = int(input('\nDigite o número da tarefa que deseja remover: ')) - 1
            if 0 <= indice < len(tarefas):
                tarefa_removida = tarefas.pop(indice)
                print(f'tarefa "{tarefa_removida}" removida.')
            else:
                print('Número inválido. Por favor, tente novamente.')
        except ValueError:
            print('Entrada inválida. Por favor, digite um número.')

def main():
    tarefas = []
    while True:
        menu()
        escolha = input('\nescolha uma opção: (1-4) ')
        
        if escolha == '1':
            adicionar_tarefa(tarefas)
        
        elif escolha == '2':
            listar_tarefas(tarefas)
        
        elif escolha == '3':
            remover_tarefa(tarefas)

        elif escolha == '4':
            print('Saindo do gerenciador de tarefas. Até logo!')
            break
        else: 
            print('Opção inválida. Por favor, escolha uma opção entre 1 e 4.')

# O gatilho final tem que ficar totalmente à esquerda!
if __name__ == '__main__':
    main()