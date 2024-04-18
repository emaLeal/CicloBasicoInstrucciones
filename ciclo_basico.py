# Clase CBI(Ciclo Basico de Instrucción)
class CBI:
    # Constructor
    def __init__(self) -> None:
        # Inicializando Variables
        self.MEMORIA: list = [] # Memoria principal donde se guardaran las direcciones con su valor
        self.ICR: str = "" # ICR(Instruction's current register - Registro de instruccion actual)
        self.PC: str = "" # PC(Program's control -  Control de programa)
        self.MAR: str = "" # MAR(Memory address register - Registro de dirección de memoria)
        self.MDR: str = "" # MDR(Memory data register - Registro de datos de memoria)
        self.UNIDADCONTROL: str = "" # Unidad de Control
        self.ACUMULADOR: str = ""
        self.ALU: str = "" # ALU(Arithmetic logic unit - Unidad de logica aritmetica)
        # Las opciones se muestran en base a las instrucciones disponibles
        self.opciones: dict = {
            "ADD": self.add,
            "SET": self.set,
            "LDR": self.ldr,
            "STR": self.str,
            "SHW": self.shw,
            "INC": self.inc,
            "DEC": self.dec,
            "PAUSE": self.pause,
            "END": self.end
        }
        self.running: bool = False # Muestra si el programa esta leyendo una linea

    # read_file lee el archivo que se le da
    # @param nombre_archivo se usa para leer un archivo y retornar una lista con las instrucciones
    def read_file(self, nombre_archivo) -> list:
        try:
            with open(nombre_archivo, 'r') as archivo:
                instrucciones: list = archivo.readlines() #cada elemento de la lista sera una linea del archivo
                instrucciones = [instruccion.strip() for instruccion in instrucciones] # se separan las lineas
                return instrucciones
        except FileNotFoundError: # error por si algo sale mal
            print("El archivo '{}' no existe.".format(nombre_archivo))
            return []
    
    # procces_instruccion Lee cada linea y ejecuta la funcion correspondiente
    # @param instructions recibe las instrucciones para correr cada linea
    def process_instruction(self, instructions) -> None: 
        self.running = True # Se establece que el programa lee lineas
        for i in instructions:
            if self.running: # verifica que el programa se este corriendo
                linea = i.split() # separa cada linea por espacios, para poder fragmentar cada parte
                """
                    Se llamara la funcion correspondiente a la instruccion, ej:
                    ADD, se ejecutara la funcion add
                    SET, se ejecutara la funcion set, etc

                    Para mantener un general, se le daran los parametros restantes
                    y se van a llamar usando *args
                """
                self.opciones[linea[0]](linea[1], linea[2], linea[3], linea[4]) 
            
    # procesador funcion para procesar instrucciones
    # @param instruction_type el tipo de instruccion, ej: SET, LOAD, STORE, etc
    # @param memory la posicion de memoria, ej: D2, J3, etc 
    def procesador(self, *args, **kwargs):
        instruction_type, memory = args[0], args[1]
        # Se le asigna al control de programa la posicion de memoria, ej: D2
        self.PC = memory
        # En la direccion de memoria se asigna lo que haya en el control de programa
        self.MAR = self.PC
        print(instruction_type +" "+self.MAR)
        # En el registro del dato de la memoria se concatena la instruccion con MAR
        self.MDR = instruction_type +" "+self.MAR
        # en el Registro de la instruccion actual, se guarda lo que esta en MDR
        self.ICR = self.MDR
        # La unidad de control contendra lo que hay en ICR 
        self.UNIDADCONTROL = self.ICR

        # Se comprobara que el tipo de instruccion sea STORE
        if instruction_type == "STORE":
            # El MDR sera el acumulador, para que haya una instruccion store ya debe haber algo en
            # el acumulador
            self.MDR = self.ACUMULADOR
            # Buscamos en este bucle el elemento de la memoria que contiene MAR y lo cambiaremos por lo que
            # hay en MDR
            for elemento in self.MEMORIA:
                if self.MAR in elemento:
                    elemento[self.MAR] = self.MDR
        
        # Se guardara en MDR lo que haya en el objeto que tenga MAR, ej: {"D2": "5"}, en MDR se guardara "5"
        self.MDR = next((objeto[self.MAR] for objeto in self.MEMORIA if self.MAR in objeto), None)
        self.ICR = self.MDR
        self.UNIDADCONTROL = self.ICR

    # set se crea la posicion en memoria y se le presenta un valor
    # @param memory direccion de memoria
    # @param value valor de la memoria
    def set(self, *args, **kwargs):
        memory, value = args[0], args[1]
        existe: bool = any(args[0] in item for item in self.MEMORIA) # verifica que exista en la memoria dicha direccion
        if not existe: # si no existe
            self.MEMORIA.append({memory: value}) # se crea el diccionario
        else:
            print("El espacio de memoria ya existe")

    # ldr se usa para cargar un valor de memoria en el acumulador
    # @param memory la direccion de memoria
    def ldr(self, *args, **kwargs,):
        memory = args[0]
        self.procesador("LOAD", memory) # se llama la funcion procesador con el tipo de instruccion "LOAD"
        self.ACUMULADOR = self.MDR # se carga en el acumulador lo que haya en MDR

    # add Funcion para sumar los parametros en la linea
    # @param memory1 memoria1
    # @param memory2 memoria2
    # @param memory3 memoria3
    def add(self, *args, **kwargs):
        memory1, memory2, memory3 = args[0], args[1], args[2]
         # verifica que memoria2 y 3 esten vacias para poder tratar con memoria1 unicamente
        if memory2 == "NULL" and memory3 == "NULL":
            # carga en mdr memoria1
            self.procesador("ADD", memory1)
            self.ALU = self.ACUMULADOR # en ALU se guarda acumulador
            self.ACUMULADOR = self.MDR # en acumulador posteriormente se guarda lo que estan en MDR
            self.ACUMULADOR = int(self.ALU) + int(self.ACUMULADOR) # se suman ALU y ACUMULADOR y se guarda en acumulador
        else: # si alguna de las dos memorias esta con info
            # se carga en mdr memoria1
            self.procesador("ADD", memory1)
            # se guarda mdr en el acumulador
            self.ACUMULADOR = self.MDR
            # se guarda en alu el acumulador
            self.ALU = self.ACUMULADOR
            # se carga en mdr memoria2
            self.procesador("ADD", memory2)
            # se guarda en acumulador mdr
            self.ACUMULADOR = self.MDR
            # se suman ambos valores usando acumulador + alu
            self.ACUMULADOR = int(self.ACUMULADOR) + int(self.ALU)
            # finalmente, si memoria3 tiene informacion se almacena lo que hay en el acumulador en memoria3
            if (memory3 != "NULL"):
                self.str(memory3)

    # str funcion para almacenar informacion en memoria
    # @param memory direccion de memoria donde se guarda la instruccion
    def str(self, *args, **kwargs):
        memory = args[0]
        self.procesador("STORE", memory)

    # swh funcion para mostrar el valor deseado
    # @param direction la direccion de memoria o parte del programa que se desea probar
    def shw(self, *args, **kwargs):
        direction = args[0]

        if direction == "ACC":
            print("El acumulador es", self.ACUMULADOR)
        elif direction == "ICR":
            print("El ICR es",self.ICR)
        elif direction == "MAR":
            print("MAR es", self.MAR)
        elif direction == "MDR":
            print("MDR es", self.MDR)
        elif direction == "UC":
            print("La unidad de Control es", self.UNIDADCONTROL)
        else: # se muestra la direccion de memoria buscandola
            for i in self.MEMORIA:
                if direction in i:
                    print("El valor de ", args[0], " es", i.get(args[0]))

    # pause Funcion para pausar el ciclo
    def pause(self, *args, **kwargs):
        print("Pause ejecutado")
        self.running = False # se cambia el valor de running a False, lo que detiene el programa

    # dec Funcion para decrementar un valor de memoria
    # @param memory direccion de memoria
    def dec(self, *args, **kwargs):
        memory = args[0]
        self.procesador("LOAD", memory) # se guarda en mdr el valor de la direccion
        self.ACUMULADOR = int(self.MDR) - 1 # en el acumulador se disminuye en 1
        print("Se ha reducido en 1 el acumulador")

    # inc funcion para incrementar un valor de memoria
    # @param memory direccion de memoria
    def inc(self, *args, **kwargs):
        memory = args[0]
        self.procesador("LOAD", memory)
        self.ACUMULADOR = int(self.MDR) + 1 
        print("Se ha incrementado en 1 el acumulador")

    # end Finaliza el ciclo de instrucciones y reinicia los valores
    def end(self, *args, **kwargs):
        print("End ejecutado")
        self.ACUMULADOR = ""
        self.PC = ""
        self.MEMORIA = []
        self.ALU = ""
        self.MDR = ""
        self.MAR = ""
        self.UNIDADCONTROL = ""
        self.running = False # se detiene el ciclo

if __name__ == "__main__":
    cpu = CBI() #Instanciamos la clase
    # Entramos a un bucle que se repetira hasta que el usuario quiera salir manualmente
    programa = ""
    while True:
        # Menu
        print("CICLO BASICO DE INSTRUCCION")
        print("1. Programa 1")
        print("2. Programa 2")
        print("3. Programa 3")
        print("4. Programa 4")
        print("5. Salir")
        num = int(input("Digite que programa quiere ejecutar: "))
        # Se verifica que la variable num este en las opciones y si no repite el ciclo
        if num >= 1 and num <= 5:
            if num == 5: # si num es 5 se rompe el ciclo
                break
            # En base a lo ingresado se concatena el numero 
            programa = f"programa{num}.txt"

        # se lee el programa y se guarda en la variable instrucciones
        instrucciones = cpu.read_file(programa) 
        if instrucciones: # si las instrucciones existen se procesa todas las lineas
            cpu.process_instruction(instrucciones)

    
    