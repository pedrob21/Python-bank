def save_data(users):
    with open('registrations.txt', 'w') as file:
        for user_id, (name, age, balance) in users.items():
            file.write(f"{user_id},{name},{age}, {balance}\n")

def load_data():
    users = {}
    try:
        with open('registrations.txt', 'r') as file:
            for line in file:
                user_id, name, age, balance = line.strip().split(',')
                users[int(user_id)] = (name, int(age), float(balance))
    except FileNotFoundError:
        pass
    return users


users = load_data()
user_id = max(users.keys(), default=0) + 1

def register():
    name = input('Name: ')
    age = int(input('Age: '))
    balance = float(input('Initial balance: '))
    return name, age, balance

def search():
    user = int(input('Enter the ID you want to seacrh: '))
    if users:
        if user in users:
            name, age, balance = users[user]
            print(f'ID: {user}, name: {name}, age: {age}, balance: {balance:.2f}')
        else:
            print('ID not found.')
    else:
        print('No data found.')

def exclude():
    user = int(input('Insira o ID que deseja exclude: '))
    if user in users:
        del users[user]
        save_data(users)
        print(f'User with the ID {user} excluded succesfully.')
    else:
        print('User not found')

def transfer():
    source = int(input('Enter the ID of the source user: '))
    if source not in users:
        print("Source ID not found.")
        return
    target = int(input('Enter the ID of the target user: '))
    if target not in users:
        print("Target ID not found.")
        return
    valor = float(input('Enter the amount you want to transfer: '))

    balance_source = users[source][2]
    balance_target = users[target][2]

    if valor > balance_source:
        print('Insufficient funds!')
    else:
        users[source] = (users[source][0], users[source][1], balance_source - valor)
        users[target] = (users[target][0], users[target][1], balance_target + valor)
        print(f"Transfer completed: From ID {source} to ID {target} with amount US${valor:.2f}")
    with open('transfers.txt', 'a') as file:
        file.write(f"Source: {source}, target: {target}, amount: {valor:.2f}\n")
    save_data(users)

def extract():
    user = int(input('Enter the ID of an user to see its extract: '))
    if user in users:
        try:
                with open('transfers.txt', 'r') as file:
                    print(f"ID {user} transfer extract:")
                    print("Source, target, amount")
                    
                    found_transactions = False
                    
                    for line in file:
                        source, target, quantia = line.strip().split(", ")

                        if int(source.split(": ")[1]) == user or int(target.split(": ")[1]) == user:
                            print(line.strip())
                            found_transactions = True

                    if not found_transactions:
                        print("No transactions found.")
        except FileNotFoundError:
            print("No transactions found.")
    else:
        print(f"User with id {user} not found.")


def default():
    print('Error! Please choose a valid option.\n')
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
    option = int(input("(1) Register \n(2) Search \n(3) Exclude \n(4) Transfer\n(5) Extract\nOption: "))
    return switch(option)

def again():
    while True:
        opc = int(input('Would you like to execute the program again?\n(1) Yes\t(2) No\nOption: '))
        if opc == 1:
            return True  # Continues the program
        elif opc == 2:
            print('Thank you for using our app!\nClosing app...')
            return False  # Exits the loop and program
        else:
            print('Error! Please choose a valid option.')

def main():
    while True:
        result = menu()
        
        if isinstance(result, tuple):
            name, age, balance = result
            users[user_id] = (name, age, balance)
            save_data(users)
        
        if not again():
            break

main()