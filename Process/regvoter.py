# Pedir nombre completo
# pedir cedula 

def regVoter():
    while True:
        try:
            name = input("Ingrese su nombre completo: ")
            name = name.lower()
        
            cc = int(input("Ingrese su numero de cedula (sin espacios ni puntos): "))
            cc = str(cc)
            if len(cc) > 10:
                print("La cèdula no puede contener màs de 10 nùmeros")
                continue
            if name == int():
                print("El nombre no puede contener nùmeros")
                continue
            break
        except ValueError:
            print("Error al ingresar los datos. Intente nuevamente... ")
        
    print(f"{name} \n{cc}")
    
        
regVoter()