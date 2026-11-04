"""
modular.py

Matemática Discreta - IMAT
ICAI, Universidad Pontificia Comillas

Grupo: GP02A
Integrantes:
    - Luis Adrián García Ruiz
    - Carlos Fracaro Solo de Zaldívar

Descripción:
Librería para la realización de cálculos y resolución de problemas de aritmética modular.
"""

from typing import Tuple, List, Dict
from math import sqrt
from excepciones import IncompatibleEquationError, Nop
import random as r

def es_primo(n:int)->bool:
    """ Reciba un entero n y devuelva verdadero si es un número primo y falso en caso contrario

    Args:
        n (int): Entero
    
    Returns:
        true si el entero es un número primo.
        false en caso contrario.

    Raises: None
    
    Examples:
        es_primo(5)=True
        es_primo(4)=False
    """

    # Test de Primalidad de Miller-Rabin (Versión Determinista)

    if n < 2: return False # Ningún número negativo o 1 es primo
    if n in (2,3,5,7): return True # Comprobaciones rápidas para optimizar
    if n % 2 == 0 or n % 3 == 0 or n % 5 == 0 or n % 7 == 0: return False # Comprobaciones rápidas para optimizar

    # Todo número par n - 1 se puede escribir como 2^r * d, con d impar y r entero
    d = n - 1 
    r = (d & -d).bit_length() - 1
    
    d >>= r
    

    # Se usan estas bases porque admiten un orden muy grande de fiabilidad para determinar si un número es primo o no
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in bases:
        if n <= a: break # Si la base es mayor o igual que n se termina la comprobación
        x = potencia_mod_p(a, d, n) # Uso del pequeño teorema de Fermat (a^d (mod n))
        if x == 1 or x == n - 1: continue
        for _ in range(r - 1):
            x = (x * x) % n # Comprueba para deteminar si el número es compuesto o no
            if x == n - 1: break # Si da n-1, quiere decir que el número no es compuesto para la base tomada
        else: return False # Si no, el número es compuesto
    return True


def lista_primos(a,b)-> List[int]:
    """ Recibe dos enteros a y b y devuelva la lista de números primos en el intervalo [a, b)

    Args:
        a (int): Elemento inicial del intervalo (incluido)
        b (int): Elemento final del intervalo (no incluido)
    
    Returns:
        List[int]: lista ordenada de primos mayores o iguales que a y menores que b.

    Raises: None
    
    Examples:
        lista_primos(1,11)=[2,3,5,7]
    """

    # Si los dos son negativos, devolver la lista vacía
    if a <= 0 and b <= 0: return []
    
    # Asegurando que a < b
    if a > b: a, b = b, a
    if a < 0 and b > 2: a = 2

    prime_list = []
    

    # 2 es el primer primo, si está en el intervalo se añade 
    if a <= 2: 
        if a <= 2 and b > 2: prime_list.append(2)
        start = 3 # Inicio de las comprobaciones   
    else:
        if a % 2 != 0: start = a 
        else: start = a + 1

    # Recorremos los valores de [inicio, b) y si el valor es primo, se añade a la lista 
    for i in range(start, b, 2):
        if es_primo(i): prime_list.append(i)

    # Se devuelve la lista de primos obtenida
    return prime_list


def factorizar(n:int)->Dict[int,int]:
    """ Recibe  un entero n y devuelve un diccionario cuyas claves son los primos que dividen a n y sus valores los
    correspondientes exponentes en la descomposición en producto de factores primos de n.
    Args:
        n (int): Entero que se desea factorizar.
    
    Returns:
        Dict[int,int]: Diccionario en el que las claves son primos positivos p_i que dividen a n y, para cada p_i,
            su valor asociado es el máximo exponente e_i tal que p_i^(e_i) divide a n. Si n=0, devuelve un diccionario vacío.

    Raises: None

    Examples:
        factorizar(12)={2: 2, 3: 1}
        factorizar(0)={}
    """

    factorizacion = {} # Factorización en números primos

    if n in (-1,0,1): return factorizacion # Si n pertenece a {-1,0,1}, se devuelve el diccionario vacío
    n = abs(n) # tomamos el valor positivo para poder factorizar
    
    
    # Se quitan todos los 2 que sean factor de n
    
    if n % 2 == 0:
        exp = 0 # exponente asociado al 2 
    
        while n % 2 == 0: 
            exp += 1
            n //= 2 

        factorizacion[2] = exp

    
    if n % 3 == 0:
        exp = 0 # exponente asociado al 3
        
        while n % 3 == 0: 
            exp += 1
            n //= 3
    
        factorizacion[3] = exp

    i = 5 # Comprobamos los impares solo 
    
    while i * i <= n: # Un número tiene como mucho divisores hasta raíz de n
        
        # Probamos con i (que será 6k - 1)
        if n % i == 0:
            exp = 0
            while n % i == 0:
                exp += 1
                n //= i
            factorizacion[i] = exp
            
        # Probamos con i + 2 (que será 6k + 1)
        if n % (i + 2) == 0:
            exp = 0
            while n % (i + 2) == 0:
                exp += 1
                n //= (i + 2)
            factorizacion[i + 2] = exp
            
        # Avanzamos al siguiente bloque de 6 (el siguiente i será 6(k+1) - 1 = i + 6)
        i += 6

    if n > 1: factorizacion[n] = 1 
    
    return factorizacion

def mcd(a:int,b:int)->int:
    """ Calcula el máximo común divisor de dos enteros a y b.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        int: devuelve el máximo común divisor de a y b

    Raises: None

    Examples:
        mcd(10,15)=5
    """
    while b != 0: a, b = b, a % b
    return a 

def bezout(n:int, m:int) -> Tuple[int,int,int]:
    """ Calcula el máximo común divisor d de dos enteros a y b junto con dos enteros x e y tales que
            d=ax+by

    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns: (d,x,y)
        d (int): Máximo común divisor.
        x (int): Coeficiente de a.
        y (int): Coeficiente de b.

    Raises: None

    Examples:
        bezout(6,10)=(2,2,-1)
    """
    x0, x1 = 1, 0 # n = x0 * n + x1 * m --> n = 1 * n + 0 * m 
    y0, y1 = 0, 1 # b = y0 * n + y1 * m --> b = 0 * n + 1 * m 
    
    while m != 0:
        q = n // m # Cociente de la división entre n y m 
        n, m = m, n % m # Lógica del algoritmo extendido de Euclides
        
        # Actualizamos los coeficientes de Bézout (Despejar los restos)
        x0, x1 = x1, x0 - q * x1 
        y0, y1 = y1, y0 - q * y1
        
    return n, x0, y0


def mcd_n(nlist:List[int])->int:
    """ Dados una lista de enteros, devuelve el máximo divisor común a todos ellos.
    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns:
        int: devuelve el máximo entero que divide a todos los enteros de la lista.

    Raises: None

    Examples:
        mcd([4,10,14])=2
    """
    #Opcional

    res = nlist[0] # Asumimos que el mcd es el primero de la lista

    for n in nlist[1:]:
        res = mcd(res, n) # Mínimo común múltiplo entre el siguiente de la lista y el resultado acumulado
        if res == 1: break # Si llegamos a uno no tiene sentido seguir mirando


    return res # se devuelve el mínimo común múltiplo calculado

def bezout_n(nlist:List[int])->Tuple[int,List[int]]:
    #Opcional
    """ Dada una lista de enteros [a_1,...,a_n], devuelve el máximo divisor común d a todos ellos y una
    lista de coeficientes [x_1,...,x_n] tal que
        d=a_1*x_1+...a_n*x_n

    Args:
        nList (List[int]): Lista de enteros.        
    
    Returns: (d,X)
        d (int): Máximo entero que divide a todos los enteros de la lista.
        X (List[int]): Lista de coeficientes [x_1,...,x_n].

    Raises: None

    Examples
        bezout_n([4,10,14])=(2,[-2,1,0])
    """

    acumulado, coeficientes = nlist[0], [1] # se guarda el primer número como mcd provisional y el primer coeficiente 1 (a · 1 = a)

    for n in nlist[1:]:
        nuevo_acumulado, u, v = bezout(acumulado, n) # se hace el bezout de los números dos a dos

        nuevos_coeficientes = []
        for c in coeficientes:
            nuevos_coeficientes.append(c * u) # actualiza los coeficientes antiguos con los nuevos resultados

        coeficientes = nuevos_coeficientes
        coeficientes.append(v) # añade el número actual que se ha tomado

        acumulado = nuevo_acumulado

    return acumulado, coeficientes


def coprimos(n:int,m:int)->bool:
    """ Determina si dos enteros son coprimos.
    Args:
        a (int): Primer entero.
        b (int): Segundo entero.
    
    Returns:
        bool: Verdadero si son coprimos y falso si no.

    Raises: None

    Examples:
        coprimos(14,20)=False
        coprimos(14,15)=True
    """

    if mcd(n, m) == 1: return True
    else: return False


def potencia_mod_p(base:int, exp:int, p:int) -> int:
    """ Calcula potencias módulo p.

    Args:
        base (int): Base de la potencia.
        exp (int): Exponente al que se eleva la base.
        p (int): Módulo.
    
    Returns:
        int: Resto de dividir base^exp módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si la base y el exponente
        son ambos 0 al mismo tiempo.

    Examples:
        potencia_mod_p(2,3,7)=1
    """

    p = abs(p)
    resultado = 1
    base = base % p

    if p == 0 or (base == 0 and exp == 0): raise ZeroDivisionError
    elif exp < 0: return potencia_mod_p(inversa_mod_p(base, p), -exp, p)

    for bit in bin(exp)[2:]:
        resultado = (resultado * resultado) % p
        if bit == '1': resultado = (resultado * base) % p
    
    return resultado

def inversa_mod_p(n:int,p:int)->int:
    """ Calcula la inversa de un número n módulo p.

    Args:
        n (int): Número que se desea invertir
        p (int): Módulo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que n*x es congruente con 1 módulo p.

    Raises:
        ZeroDivisionError: Si el módulo es 0 o si n no es invertible módulo p.
    
    Examples:
        inversa_mod_p(2,7)=4
    """

    p = abs(p) # Calculamos el valor absoluto dado que la inversa con mod p y mod -p es igual al ser -p múltiplo de p.

    if p == 0: raise ZeroDivisionError
    if p == 1: return 0 # Devolvemos cero como represante canónico

    n %= p # Normalizamos n a su representante canónico
    old_r, r = p, n
    old_s, s = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q*r
        old_s, s = s, old_s - q*s

    if old_r != 1: raise ZeroDivisionError

    return old_s % p

def euler(n:int)->int:
    """ Calcula la función phi de Euler de un entero positivo n, es decir, cuenta cúantos enteros positivos
    menores que n son coprimos con n.

    Args:
        n (int): Número entero positivo.

    Returns:
        int: Función phi de Euler de n.

    Raises: None

    Examples:
        euler(7)=6
        euler(15)=8
    """

    n_factorizado = factorizar(n)
    phi_n = 1

    for primo, exp in n_factorizado.items():
        phi_n *= (primo - 1) * primo**(exp - 1)

    return phi_n

def legendre(n:int,p:int)->int:
    """ Dado un entero n y un número primo p, calcula el símbolo de Legendre de n módulo p.

    Args:
        n (int): Número entero.
        p (int): Número primo.
    
    Returns:
        int: Símbolo de Legendre de Euler de n módulo p:
            0 si es múltiplo de p
            1 si es un cuadrado perfecto (distinto de 0), módulo p
            -1 en caso contrario.

    Raises:
        ZeroDivisionError: Si el módulo p es 0.

    Examples:
        legendre(2,5)=-1
        legendre(2,7)=1
        legendre(10,5)=0
    """
    if p == 0: raise ZeroDivisionError
    if p == 2: return 0 if n % 2 == 0 else 1
    
    n %= p
    if n == 0: return 0
    r = potencia_mod_p(n, (p-1)//2, p)
    return 1 if r == 1 else -1


def resolver_sistema_congruencias(alist:List[int],blist:List[int],plist:List[int])->Tuple[int,int]:
    """ Dadas tres listas de números enteros [a_1,...,a_n], [b_1,...,b_n] y [p_1,...,p_n], resuelve el sistema de congruencias
    
    a_i * x = b_i (mod p_i)   i=1,...,n
    
    devolviendo un entero r y un módulo m tales que las soluciones del sistema corresponden a todos los enteros
    x congruentes con r módulo m.

    Args:
        alist (List[int]): Lista de coeficientes de la variable x, [a_1,...,a_n].
        blist (List[int]): Lista de términos independientes [b_1,...,b_n].
        plist (List[int]): Lista de módulos [p_1,...,p_n]
    
    Returns: (r,m)
        r (int): Entero entre 0 y m-1.
        m (int): Entero positivo, módulo de la solución.

    Raises:
        IncompatibleEquationError: Si no es posible resolver el sistema.

    Examples:
        resolver_sistema_congruencias([2],[3],[5]])=(4,5)
        resolver_sistema_congruencias([2],[4],[6])=(2,3)
        resolver_sistema_congruencias([1,4],[1,7],[3,11])=(10,33)
    """

    alen = len(alist)
    blen = len(blist)
    plen = len(plist)

    if alen != blen or alen != plen or blen != plen: raise IncompatibleEquationError
    elif not alist or not blist or not plist: raise IncompatibleEquationError
    elif 0 in plist: raise IncompatibleEquationError

    abs_plist = [abs(p) for p in plist]

    # ── FASE 1: normalizar cada ecuación a x ≡ r (mod m) ──
    rlist = []
    mlist = []

    for a, b, p in zip(alist, blist, abs_plist):
        a %= p
        d = mcd(a, p)

        if b % d != 0: raise IncompatibleEquationError

        z, y, m = a//d, b//d, p//d
        r = (inversa_mod_p(z, m) * y) % m
        rlist.append(r)
        mlist.append(m)

    # ── FASE 2: TCR por fusión sucesiva ──
    r_total, M = rlist[0], mlist[0]

    for r_k, m_k in zip(rlist[1:], mlist[1:]):
        g = mcd(M, m_k)
        dif = r_k - r_total

        if dif % g != 0: raise IncompatibleEquationError

        m_red = m_k // g
        k = (inversa_mod_p(M // g, m_red) * (dif // g)) % m_red
        r_total += k * M
        M *= m_red
        r_total %= M

    return (r_total, M)



def raiz_mod_p(n:int,p:int)->int:
    """ Encuentra, si existe, una raíz cuadrada para un entero n módulo un número primo p.

    Args:
        n (int): Entero del que se desea hallar la raíz.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns:
        int: Entero x entre 0 y p-1 tal que x^2 = n (mod p).

    Raises:
        IncompatibleEquationError: Si no es posible hallar dicha raíz.

    Examples:
        raiz_mod_p(2,7)=3
    """
    #Opcional
    
    n %= p
    if n == 0: return 0
    if legendre(n, p) == -1: raise IncompatibleEquationError
    if p == 2: return n                        # 0²=0, 1²=1
    if p % 4 == 3: x = potencia_mod_p(n, (p+1)//4, p)
    else: x = cipolla(n, p)
    return min(x, p - x)


def ecuacion_cuadratica(a:int,b:int,c:int,p:int)->Tuple[int,int]:
    """ Halla, si es posible, las dos posibles soluciones de la ecuación cuadrática ax^2+bx+c=0 (mod p).
    Devuelve una tupla con las dos raíces (distintas o una misma raíz repetida en caso de ser doble).

    Args:
        a (int): Coeficiente de x^2.
        b (int): Coeficiente de x.
        c (int): Término independiente.
        p (int): Módulo. Se asume que es un número primo.
    
    Returns: (x1,x2)
        x1 (int): Primera solución. Entero entre 0 y p-1.
        x2 (int): Segunda solución. Entero entre 0 y p-1.

    Raises:
        IncompatibleEquationError: Si no es posible resolver la ecuación.

    Examples:
        ecuacion_cuadratica(4,1,3,11)
        ecuacion_cuadratica(4,1,5,11)=(3, 5)
        ecuacion_cuadratica(1,2,1,11)=(10,10)
    """
    #Opcional
    
    if p == 2:
        soluciones = [x for x in (0, 1) if (a*x*x + b*x + c) % 2 == 0]
        if not soluciones: raise IncompatibleEquationError
        if len(soluciones) == 1: return (soluciones[0], soluciones[0])
        return (0, 1)
    
    if a % p == 0: raise IncompatibleEquationError

    d = (b * b - 4 * a * c) % p

    if legendre(d, p) == -1: raise IncompatibleEquationError

    r = raiz_mod_p(d, p)
    inv = inversa_mod_p(2 * a, p)
    x1, x2 = ((-b + r) * inv) % p, ((-b - r) * inv) % p

    return tuple(sorted((x1, x2)))
    

##########################################################################################
# AUXILIARY FUNCTIONS
##########################################################################################

def cipolla(n:int, p:int):
    a = 1
    
    while True:

        if a >= p: raise IncompatibleEquationError

        w2 = (a*a - n) % p

        if legendre(w2, p) == -1: break
        
        a += 1

    (u, v) = potencia_ext((a, 1), (p + 1)//2, w2, p)

    if v == 0: return u
    else: raise AssertionError

def potencia_ext(par:tuple, exp:int, w2:int, p:int):
    resultado = (1, 0)
    base = par

    while exp > 0:

        if exp % 2 != 0: resultado = mult_ext(resultado, base, w2, p)
        base =  mult_ext(base, base, w2, p)
        exp //= 2

    return resultado

def mult_ext(par1:tuple, par2:tuple, w2:int, p:int):
    u1, v1 = par1
    u2, v2 = par2
    u = (u1 * u2 + v1 * v2 * w2) % p
    v = (u1 * v2 + u2 * v1) % p

    return (u, v)

def coprimo_valor_a(a: int) -> List[int]:
    """
    Genera un número aleatorio coprimo con a

    Args:
        a (int): Extremo superior del intervalo.

    Returns:
        List[int]: Lista ordenada de enteros coprimos con 'a'.
    """
    
    while True:
        e = r.randint(2, a - 1) # generación de candidato para ser coprimo
        
        if coprimos(e, a):
            return e # En el momento que sea coprimo se devuelve