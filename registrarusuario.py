import rsa
import os

valid_name = False # Flag that states whether the user name is available
correct_min_value = False # Flag that states whether the min value of the prime has been set correctly 
correct_max_value = False # Flag that states whether the max value of the prime has been set correctly 
correct_padding = False # Flag that states whether the paddinf value has been set correctly 

# Ascii desing with decorative purpose
WELCOME = r''' 
·········································································································
:                                                                                                       :
:   _______ __                               __    __                                                   :
:  |   _   |__.-----.-----.--.--.-----.-----|__.--|  .-----.   .---.-.                                  :
:  |.  1   |  |  -__|     |  |  |  -__|     |  |  _  |  _  |   |  _  |                                  :
:  |.  _   |__|_____|__|__|\___/|_____|__|__|__|_____|_____|   |___._|                                  :
:  |:  1    \                                                                                           :
:  |::.. .  /                                                                                           :
:  `-------'         __       __                                           __                      __   :
:  .----.-----.-----|__.-----|  |_.----.---.-.--.--.-----.--.--.---.-.----|__.-----.  .-----.--.--|  |  :
:  |   _|  -__|  _  |  |__ --|   _|   _|  _  |  |  |__ --|  |  |  _  |   _|  |  _  |__|  _  |  |  |__|  :
:  |__| |_____|___  |__|_____|____|__| |___._|_____|_____|_____|___._|__| |__|_____|__|   __|___  |__|  :
:             |_____|                                                                 |__|  |_____|     :
:                                                                                                       :
·········································································································
'''

# Obtaining the path of the script
actual_path = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '.'

# Creating the path for the users directory
users_directory = os.path.join(actual_path, "Usuarios")

# Creates the directory only if it does not exist
os.makedirs(users_directory, exist_ok=True)

print(WELCOME)

while not valid_name:

    name = input('Indique un nombre: ').strip().capitalize() # Its asummed that name can be of any type (no restrictions)

    public_route = os.path.join(users_directory, f"pub_{name}.txt")
    private_route = os.path.join(users_directory, f"priv_{name}.txt")

    if os.path.exists(public_route) or os.path.exists(private_route):
        print(f"\n--- Error: El usuario '{name}' ya existe en el sistema ---")
        print('\t--- Inténtelo con otro nombre de usuario ---\n')

    else: valid_name = True

print() # With clarity purpose in the terminal

while not correct_min_value:
    min_value = input('Indique el valor mínimo del primo: ')
    if min_value.isdecimal() and int(min_value) > 0: 
        min_value = int(min_value) # transforming the number into int
        correct_min_value = True
    else: print('--- Valor incorrecto ---\n\t --- Recuerda que debe ser un valor entero positivo---\n')

while not correct_max_value:
    max_value = input('Indique el valor máximo del primo: ')
    if max_value.isdecimal() and int(max_value) > 0: 
        max_value = int(max_value) # transforming the number into int
        correct_max_value = True
    else: print('--- Valor incorrecto ---\n\t --- Recuerda que debe ser un valor entero positivo---\n')

while not correct_padding:
    padding = input('Indique un número de cifras para el padding: ')
    if padding.isdecimal() and int(padding) > 0: correct_padding = True
    else: print('--- Valor incorrecto ---\n\t --- Recuerda que debe ser un valor entero positivo---\n')

tuple_rsa = rsa.generar_claves(min_value, max_value)
n, e , d = tuple_rsa[0], tuple_rsa[1], tuple_rsa[2]


# Public key
with open(public_route, 'w', encoding='utf-8') as f:
    f.write(f"{n}\n")
    f.write(f"{e}\n")
    f.write(f"{padding}\n")
    
# Private key
with open(private_route, 'w', encoding='utf-8') as f:
    f.write(f"{d}\n")
    
print('--- Usuario registrado con éxito ---')
print(f"\t Los ficheros de claves de '{name}' se han guardado correctamente en la carpeta 'Usuarios'.")