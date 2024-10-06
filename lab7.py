from collections import defaultdict

#Función para cargar la CFG
def cargar_gramatica(archivo):
    gramatica = defaultdict(list)
    with open(archivo, 'r', encoding='utf-8') as CFG:
        for linea in CFG:
            #Imprime la línea que está siendo analizada
            print(f"Leyendo línea: {linea}")
            #Eliminar espacios
            linea = linea.strip()
            #Separar símbolos no terminales de producciones
            izquierda, derecha = linea.split('->')
            #Separar las múltiples producciones
            producciones = derecha.split('|')

            for prod in producciones:
                gramatica[izquierda.strip()].append(prod.strip())
    return gramatica


# Función para eliminar producciones-𝜀
def eliminar_producciones_epsilon(gramatica):
    anulables = set()
    
    # Encontrar símbolos anulables
    for no_terminal, producciones in gramatica.items():
        for prod in producciones:
            if prod == '𝜀':
                anulables.add(no_terminal)
    
    # Reemplazar producciones anulables
    nueva_gramatica = defaultdict(list)
    for no_terminal, producciones in gramatica.items():
        for prod in producciones:
            if prod != '𝜀':
                nueva_gramatica[no_terminal].append(prod)
            if any(simbolo in anulables for simbolo in prod):
                nuevas_producciones = set()
                for i in range(len(prod)):
                    if prod[i] in anulables:
                        nueva = prod[:i] + prod[i+1:]
                        if nueva:
                            nuevas_producciones.add(nueva)
                nueva_gramatica[no_terminal].extend(nuevas_producciones)
    
    return nueva_gramatica

# Función para eliminar producciones unarias
def eliminar_producciones_unarias(gramatica):
    unarias = defaultdict(list)
    
    for no_terminal, producciones in gramatica.items():
        for prod in producciones:
            if len(prod) == 1 and prod.isupper():
                unarias[no_terminal].append(prod)
    
    # Eliminar unarias y expandirlas
    for no_terminal, producciones in unarias.items():
        for prod in producciones:
            gramatica[no_terminal].remove(prod)
            if prod in gramatica:
                gramatica[no_terminal].extend(gramatica[prod])
    
    return gramatica

# Función para eliminar símbolos inútiles
def eliminar_simbolos_inutiles(gramatica):
    # Remover símbolos que no producen
    producidos = set()
    for no_terminal, producciones in gramatica.items():
        for prod in producciones:
            if all(simbolo.islower() for simbolo in prod):  # Solo contiene terminales
                producidos.add(no_terminal)
    
    cambios = True
    while cambios:
        cambios = False
        for no_terminal, producciones in gramatica.items():
            for prod in producciones:
                if all(simbolo in producidos or simbolo.islower() for simbolo in prod):
                    if no_terminal not in producidos:
                        producidos.add(no_terminal)
                        cambios = True
    
    # Remover producciones que no producen
    nueva_gramatica = defaultdict(list)
    for no_terminal, producciones in gramatica.items():
        if no_terminal in producidos:
            for prod in producciones:
                if all(simbolo in producidos or simbolo.islower() for simbolo in prod):
                    nueva_gramatica[no_terminal].append(prod)
    
    # Remover símbolos no alcanzables
    alcanzables = {'S'}
    cambios = True
    while cambios:
        cambios = False
        for no_terminal in alcanzables.copy():
            if no_terminal in nueva_gramatica:
                for prod in nueva_gramatica[no_terminal]:
                    for simbolo in prod:
                        if simbolo.isupper() and simbolo not in alcanzables:
                            alcanzables.add(simbolo)
                            cambios = True
    
    nueva_gramatica = {no_terminal: prods for no_terminal, prods in nueva_gramatica.items() if no_terminal in alcanzables}
    return nueva_gramatica

# Función para convertir a CNF
def convertir_a_cnf(gramatica):
    nueva_gramatica = defaultdict(list)
    nuevas_producciones = []
    contador = 0
    
    for no_terminal, producciones in gramatica.items():
        for prod in producciones:
            if len(prod) == 2 and all(simbolo.isupper() for simbolo in prod):
                nueva_gramatica[no_terminal].append(prod)
            elif len(prod) == 1:
                nueva_gramatica[no_terminal].append(prod)
            else:
                nuevo_simbolo = f'X{contador}'
                contador += 1
                nueva_gramatica[no_terminal].append(prod[0] + nuevo_simbolo)
                nuevas_producciones.append((nuevo_simbolo, prod[1:]))
    
    for nuevo_simbolo, prod in nuevas_producciones:
        while len(prod) > 2:
            nuevo_simbolo2 = f'X{contador}'
            contador += 1
            nueva_gramatica[nuevo_simbolo].append(prod[0] + nuevo_simbolo2)
            nuevo_simbolo = nuevo_simbolo2
            prod = prod[1:]
        nueva_gramatica[nuevo_simbolo].append(prod)
    
    return nueva_gramatica

# Función principal para cargar y simplificar la gramática
def simplificar_gramatica(archivo):
    gramatica = cargar_gramatica(archivo)
    
    print("Gramática original:")
    print(gramatica)
    
    gramatica = eliminar_producciones_epsilon(gramatica)
    print("\nDespués de eliminar producciones-𝜀:")
    print(gramatica)
    
    gramatica = eliminar_producciones_unarias(gramatica)
    print("\nDespués de eliminar producciones unarias:")
    print(gramatica)
    
    gramatica = eliminar_simbolos_inutiles(gramatica)
    print("\nDespués de eliminar símbolos inútiles:")
    print(gramatica)
    
    gramatica = convertir_a_cnf(gramatica)
    print("\nGramática en CNF:")
    print(gramatica)


archivo_gramatica = r"C:\Users\javie\Desktop\Tareas\Teoria compu\lab7TeoriaCompu\gramaticas.txt"

simplificar_gramatica(archivo_gramatica)
