import json
import os

class Candidato:
    def __init__(self, nombre, partido, periodo, gobierno):
        self.nombre = nombre
        self.partido = partido
        self.periodo = periodo
        self.gobierno = gobierno
    
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'partido': self.partido,
            'periodo': self.periodo,
            'gobierno': self.gobierno
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data['nombre'],
            data['partido'],
            data['periodo'],
            data['gobierno']
        )
    
    def __str__(self):
        return f"{self.nombre} | {self.partido} | {self.periodo} | {self.gobierno}"


class SistemaCandidatos:
    def __init__(self, archivo='candidatos.json'):
        self.archivo = archivo
        self.lista = []
        self.cargar_datos()
    
    def cargar_datos(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.lista = [Candidato.from_dict(d) for d in datos]
                print(f"Se cargaron {len(self.lista)} candidatos del archivo\n")
            except json.JSONDecodeError:
                print("Error al leer el archivo JSON. Iniciando con lista vacía.\n")
    
    def guardar_datos(self):
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                datos = [c.to_dict() for c in self.lista]
                json.dump(datos, f, ensure_ascii=False, indent=4)
            print("Datos guardados exitosamente\n")
        except Exception as e:
            print(f"Error al guardar datos: {e}\n")
    
    def registrar_candidato(self):
        print("\n===== R E G I S T R A R C A N D I D A T O =====")
        nombre = input("Nombre del candidato: ").strip()
        partido = input("Partido político: ").strip()
        periodo = input("Período del mandato (años): ").strip()
        gobierno = input("Modelo de gobierno: ").strip()
        
        if nombre and partido and periodo and gobierno:
            candidato = Candidato(nombre, partido, periodo, gobierno)
            self.lista.append(candidato)
            self.guardar_datos()
            print("Candidato registrado exitosamente!\n")
        else:
            print("Todos los campos son obligatorios\n")
    
    def mostrar_candidatos(self):
        print("\n--- LISTA DE CANDIDATOS ---")
        if not self.lista:
            print("No hay candidatos registrados.\n")
            return
        
        print(f"\nTotal de candidatos: {len(self.lista)}\n")
        for i, candidato in enumerate(self.lista, 1):
            print(f"{i}. {candidato}")
        print()
    
    def exportar_json(self):
        nombre_archivo = input("Nombre del archivo (sin extensión): ").strip()
        if nombre_archivo:
            nombre_archivo += '.json'
            try:
                with open(nombre_archivo, 'w', encoding='utf-8') as f:
                    datos = [c.to_dict() for c in self.lista]
                    json.dump(datos, f, ensure_ascii=False, indent=4)
                print(f"Datos exportados a {nombre_archivo}\n")
            except Exception as e:
                print(f"Error al exportar: {e}\n")
    
    def mostrar_menu(self):
        print("=" * 45)
        print("===== L I S T A  D E  C A N D I D A T O S=====")
        print("=" * 45)
        print("1. Registrar Candidato")
        print("2. Consultar listado de candidatos")
        print("3. Salir")
        print("==============================================")
        print("=" * 45)
    
    def ejecutar(self):
        while True:
            self.mostrar_menu()
            try:
                opcion = int(input("Seleccione una opción: "))
                
                if opcion == 1:
                    self.registrar_candidato()
                elif opcion == 2:
                    self.mostrar_candidatos()
                elif opcion == 3:
                    print("\n¡Gracias por usar el sistema!")
                    break
                else:
                    print("Opción inválida. Intente nuevamente.\n")
            except ValueError:
                print("Por favor ingrese un número válido.\n")
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego!")
                break


if __name__ == "__main__":
    sistema = SistemaCandidatos()
    sistema.ejecutar()

    