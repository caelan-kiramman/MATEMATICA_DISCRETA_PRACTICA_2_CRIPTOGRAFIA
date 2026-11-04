import os
import sys
from auxiliar_functions import get_keys
from excepciones import NonExistingUser

user1, user2 = sys.argv[1].capitalize(), sys.argv[2].capitalize() # Obtaining the names of the users
OPTIONS = ('D', 'C', 'S')
leave = False

try:
    keys_user_1 = get_keys(user1)
    keys_user_2 = get_keys(user2)

    public_values_1, private_values_1 = keys_user_1[0], keys_user_1[1]

    n1, e1, padding1 = public_values_1[0], public_values_1[1], public_values_1[2]
    d1 = private_values_1[0]

    public_values_2, private_values_2 = keys_user_2[0], keys_user_2[1]
    n2, e2, padding2 = public_values_2[0], public_values_2[1], public_values_2[2]
    d2 = private_values_2[0]

    while not leave:
        
        option = input('Elige una Opción:\n\t - (D)escifrar\n\t - (C)ifrar \n\t - (S)alir: \n>>>').upper()
        
        if option == 'D':
            print('\t--- Ha elegido Descifrar ---\n')
            plain_text = input('Introduzca el texto que desea cifrar: \n\t>>>')
            # Función de cifrar para el clave pública del usuario 2 y padding del usuario 2
        
        elif option == 'C':
            print('\t--- Ha elegido Cifrar ---\n')
            ciphered_text = input('Introduzca el texto cifrado: \n\t>>>')
            # Función de descifrar usando la clave privda del usuario 1 y las cifras de padding del usuario 1
        
        elif option == 'S':
            print('--- Saliendo de Criptochat.py ---')
            leave = True
        
        else: print('--- La opción elegida no es válida ---\n')

except NonExistingUser as e: print(f'--- ERROR --- \n\t{e}')