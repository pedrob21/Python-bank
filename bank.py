def save_data(users):
    with open('registrations.txt', 'w') as file:
        for user_id, (name, age, balance) in users.items():
            file.write(f"{user_id},{name},{age}, {balance}\n")

def carregar_dados():
    users = {}
    try:
        with open('registrations.txt', 'r') as file:
            for line in file:
                user_id, name, age, balance = line.strip().split(',')
                users[int(user_id)] = (name, int(age), float(balance))
    except FileNotFoundError:
        pass
    return users


users = carregar_dados()
user_id = max(users.keys(), default=0) + 1

def register():
    name = input('Insira seu name: ')
    age = int(input('Insira sua age: '))
    balance = float(input('Insira seu balance: '))
    return name, age, balance

def search():
    n = int(input('Insira o ID que deseja search: '))
    if users:
        if n in users:
            name, age, balance = users[n]
            print(f'ID: {n}, name: {name}, age: {age}, balance: {balance:.2f}')
        else:
            print('ID não encontrado.')
    else:
        print('Nenhum dado encontrado.')

def exclude():
    user = int(input('Insira o ID que deseja exclude: '))
    if user in users:
        del users[user]
        save_data(users)
        print(f'Usuário com ID {user} excluído com sucesso.')
    else:
        print('Usuário não encontrado')

def transfer():
    origin = int(input('Insira o id do usuário de origin: '))
    if origin not in users:
        print("ID de origin não encontrado.")
        return
    target = int(input('Insira o id do usuário de target: '))
    if target not in users:
        print("ID de target não encontrado.")
        return
    valor = float(input('Insira a quantia que deseja transfer: '))

    balance_origin = users[origin][2]
    balance_target = users[target][2]

    if valor > balance_origin:
        print('Quantia indisponível!')
    else:
        users[origin] = (users[origin][0], users[origin][1], balance_origin - valor)
        users[target] = (users[target][0], users[target][1], balance_target + valor)
        print(f"Transferência realizada: Do id {origin} para o id {target} com uma quantiade R${valor:.2f}")
    with open('transfers.txt', 'a') as file:
        file.write(f"origin: {origin}, target: {target}, Quantia: {valor:.2f}\n")
    save_data(users)

def extract():
    user = int(input('Insira o id do usuário que deseja conferir o extract: '))
    if user in users:
        try:
                with open('transfers.txt', 'r') as file:
                    print(f"extract de Transferências para o Usuário ID {user}:")
                    print("origin, target, Quantia")
                    
                    found_transactions = False
                    
                    for line in file:
                        origin, target, quantia = line.strip().split(", ")

                        if int(origin.split(": ")[1]) == user or int(target.split(": ")[1]) == user:
                            print(line.strip())
                            found_transactions = True

                    if not found_transactions:
                        print("Nenhuma transação encontrada para este usuário.")
        except FileNotFoundError:
            print("Nenhuma transação encontrada.")
    else:
        print(f"Usuário com id {user} não encontrado.")


def default():
    print('Erro! Por favor, insira uma opção válida.')
    return menu()


switcher = {
    1: register,
    2: search,
    3: exclude,
    4: transfer,
    5: extract
}

def switch(case):
    func = switcher.get(case, default)
    return func()  

def menu():
    option = int(input("(1) register \n(2) search \n(3) Remover \n(4) Transferência\n(5) extract\noption: "))
    return switch(option)

result = menu()  
if isinstance(result, tuple):
    name, age, balance = result
    users[user_id] = (name, age, balance)
    save_data(users) 
