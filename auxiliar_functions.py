import os
from excepciones import NonExistingUser

def get_keys(name: str) -> tuple[tuple[int]]:
    '''
    returns the route for the files of the public and private key for the name provided

    Args:
        name (str): name of the user
    
    Returns:
        tuple[tuple[int]]: tuple containing the routs to the public and private key values

    '''

    actual_path = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '.' # path of the script

    users_directory = os.path.join(actual_path, "Usuarios") # path of the directory 'Usuarios'

    public_route = os.path.join(users_directory, f"pub_{name}.txt") # route to the public keys
    private_route = os.path.join(users_directory, f"priv_{name}.txt") # route to the private keys

    if not os.path.exists(public_route) or not os.path.exists(private_route): raise NonExistingUser(f'--- El usuario {name} no existe ---\n\t --- Fin del programa ---')

    with open(public_route, 'r', encoding='utf-8') as f:
        
        public_elements = []
        for line in f: 
            line = line.strip()
            public_elements.append(int(line))

    with open(private_route, 'r', encoding='utf-8') as f:
            
            private_elements = []
            for line in f: 
                line = line.strip()
                private_elements.append(int(line))

    public_elements, private_elements = tuple(public_elements), tuple(private_elements)

    return public_elements, private_elements