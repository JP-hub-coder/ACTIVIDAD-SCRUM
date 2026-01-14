import json
import os
import hashlib

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
    def __init__(self, archivo='candidatos.json', archivo_votos='votos.json', archivo_votantes='votantes.json'):
        self.archivo = archivo
        self.archivo_votos = archivo_votos
        self.archivo_votantes = archivo_votantes
        self.lista = []
        self.votos = {}
        self.votantes_registrados = set()
        self.cargar_datos()
    
    def cargar_datos(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.lista = [Candidato.from_dict(d) for d in datos]
                print(f"Se cargaron {len(self.lista)} candidatos del archivo")
            except json.JSONDecodeError:
                print("Error al leer el archivo JSON de candidatos. Iniciando con lista vacía.")
    
        if os.path.exists(self.archivo_votos):
            try:
                with open(self.archivo_votos, 'r', encoding='utf-8') as f:
                    self.votos = json.load(f)
            except json.JSONDecodeError:
                print("Error al leer el archivo de votos.")
        
        if os.path.exists(self.archivo_votantes):
            try:
                with open(self.archivo_votantes, 'r', encoding='utf-8') as f:
                    self.votantes_registrados = set(json.load(f))
            except json.JSONDecodeError:
                print("Error al leer el archivo de votantes.")
        print()
    
    def guardar_datos(self):
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                datos = [c.to_dict() for c in self.lista]
                json.dump(datos, f, ensure_ascii=False, indent=4)
            print("Datos guardados exitosamente\n")
        except Exception as e:
            print(f"Error al guardar datos: {e}\n")
    
    def guardar_votos(self):
        try:
            with open(self.archivo_votos, 'w', encoding='utf-8') as f:
                json.dump(self.votos, f, ensure_ascii=False, indent=4)
            
            with open(self.archivo_votantes, 'w', encoding='utf-8') as f:
                json.dump(list(self.votantes_registrados), f, ensure_ascii=False, indent=4)
            
            print("Voto registrado exitosamente de forma anónima!\n")
        except Exception as e:
            print(f"Error al guardar voto: {e}\n")
    
    def hash_cedula(self, cedula):
        """Crea un hash de la cédula para verificar sin almacenar el dato real"""
        return hashlib.sha256(cedula.encode()).hexdigest()
    
    def registrar_candidato(self):
        print("\n===== R E G I S T R A R  C A N D I D A T O =====")
        nombre = input("Nombre del candidato: ").strip()
        partido = input("Partido político: ").strip()
        periodo = input("Período del mandato (años): ").strip()
        gobierno = input("Modelo de gobierno: ").strip()
        
        if nombre and partido and periodo and gobierno:
            candidato = Candidato(nombre, partido, periodo, gobierno)
            self.lista.append(candidato)
            self.votos[nombre] = 0
            self.guardar_datos()
            self.guardar_votos()
            print("Candidato registrado exitosamente!\n")
        else:
            print("Todos los campos son obligatorios\n")
    
    def registrar_voto(self):
        print("\n===== R E G I S T R A R  V O T O =====")
        
        if not self.lista:
            print("No hay candidatos registrados. No se puede votar.\n")
            return
        
        nombre_completo = input("Nombre completo del votante: ").strip()
        if not nombre_completo:
            print("El nombre es obligatorio\n")
            return
        
        try:
            edad = int(input("Edad: ").strip())
            if edad < 18:
                print("Debe ser mayor de 18 años para votar\n")
                return
        except ValueError:
            print("Edad inválida\n")
            return
        
        cedula = input("Cédula de ciudadanía (máximo 10 números): ").strip()
        if not cedula.isdigit() or len(cedula) > 10:
            print("Cédula inválida. Debe contener solo números y máximo 10 dígitos\n")
            return
        

        hash_cedula = self.hash_cedula(cedula)
        if hash_cedula in self.votantes_registrados:
            print("Esta cédula ya ha registrado un voto. No se permite votar dos veces.\n")
            return
        
        print("\n=== C A N D I D A T O S  D I S P O N I B L E S ===")
        for i, candidato in enumerate(self.lista, 1):
            print(f"{i}. {candidato.nombre} - {candidato.partido}")
        
        try:
            opcion = int(input("\nSeleccione el número del candidato por quien vota: "))
            if 1 <= opcion <= len(self.lista):
                candidato_elegido = self.lista[opcion - 1]
                
                if candidato_elegido.nombre not in self.votos:
                    self.votos[candidato_elegido.nombre] = 0
                self.votos[candidato_elegido.nombre] += 1
                
                self.votantes_registrados.add(hash_cedula)
                
                self.guardar_votos()
                print(f"\n¡Gracias por votar! Su voto ha sido registrado de forma anónima.")
                print("Sus datos personales NO han sido almacenados.\n")
            else:
                print("Opción inválida\n")
        except ValueError:
            print("Debe ingresar un número válido\n")
    
    def mostrar_candidatos(self):
        print("\n=== L I S T A  D E  C A N D I D A T O S ===")
        if not self.lista:
            print("No hay candidatos registrados.\n")
            return
        
        print(f"\nTotal de candidatos: {len(self.lista)}\n")
        for i, candidato in enumerate(self.lista, 1):
            print(f"{i}. {candidato}")
        print()
    
    def mostrar_resultados(self):
        print("\n===== R E S U L T A D O S  D E  V O T A C I Ó N =====")
        
        if not self.votos or all(v == 0 for v in self.votos.values()):
            print("No hay votos registrados aún.\n")
            return
        
        total_votos = sum(self.votos.values())
        print(f"\nTotal de votos registrados: {total_votos}\n")
        
        resultados_ordenados = sorted(self.votos.items(), key=lambda x: x[1], reverse=True)
        
        print("=== R E S U L T A D O S  P O R  C A N D I D A T O ===")
        for i, (candidato, votos) in enumerate(resultados_ordenados, 1):
            porcentaje = (votos / total_votos * 100) if total_votos > 0 else 0
            print(f"{i}. {candidato}: {votos} votos ({porcentaje:.2f}%)")
        
        if resultados_ordenados:
            ganador = resultados_ordenados[0]
            print(f"\nCandidato con más votos: {ganador[0]} con {ganador[1]} votos")
    
    def mostrar_menu(self):
        print("=" * 50)
        print("===== S I S T E M A  D E  V O T A C I Ó N =====")
        print("=" * 50)
        print("1. Registrar Candidato")
        print("2. Consultar listado de candidatos")
        print("3. Registrar voto")
        print("4. Ver resultados de votación")
        print("5. Salir")
        print("=" * 50)
    
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
                    self.registrar_voto()
                elif opcion == 4:
                    self.mostrar_resultados()
                elif opcion == 5:
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
