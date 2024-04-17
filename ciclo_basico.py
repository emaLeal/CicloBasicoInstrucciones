class CBI:
    def __init__(self) -> None:
        self.MEMORIA = []
        self.ICR = None
        self.PC = 0
        self.MAR = None
        self.MDR = None
        self.UNIDADCONTROL = None
        self.ACUMULADOR = 0
        self.ALU = 0
        self.opciones = {
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
        self.running = False

    def read_file(self, nombre_archivo) -> list:
        try:
            with open(nombre_archivo, 'r') as archivo:
                instrucciones = archivo.readlines()
                instrucciones = [instruccion.strip() for instruccion in instrucciones]
                return instrucciones
        except FileNotFoundError:
            print("El archivo '{}' no existe.".format(nombre_archivo))
            return []
        
    def process_instruction(self, instructions) -> None:
        self.running = True
        for i in instructions:
            if self.running:
                linea = i.split()
                self.opciones[linea[0]](linea[1], linea[2], linea[3], linea[4])
            
    def procesador(self, *args, **kwargs):
        instruction_type, memory, memory2, memory3 = args[0], args[1], None, None
        if len(args) > 2:
            memory2 = args[2]
        if len(args) > 3:
            memory3 = args[3]
        self.PC = memory
        self.MAR = self.PC
        print(instruction_type +" "+self.MAR)
        self.MDR = instruction_type +" "+self.MAR
        self.ICR = self.MDR
        self.UNIDADCONTROL = self.ICR

        self.MAR = memory
        if instruction_type == "STORE":
            self.MDR = self.ACUMULADOR

            for elemento in self.MEMORIA:
                if self.MAR in elemento:
                    elemento[self.MAR] = self.MDR
        self.MAR = memory
            
        self.MDR = next((objeto[self.MAR] for objeto in self.MEMORIA if self.MAR in objeto), None)

    def set(self, *args, **kwargs):
        memory, value = args[0], args[1]
        existe: bool = any(args[0] in item for item in self.MEMORIA)
        if not existe:
            self.MEMORIA.append({memory: value})
        else:
            print("El espacio de memoria ya existe")

    def ldr(self, *args, **kwargs,):
        self.procesador("LOAD", args[0])
        self.ACUMULADOR = self.MDR

    def add(self, *args, **kwargs):
        memory1, memory2, memory3 = args[0], args[1], args[2]
        if memory2 == "NULL" and memory3 == "NULL":
            self.procesador("ADD", memory1)
            self.ALU = self.ACUMULADOR
            self.ACUMULADOR = self.MDR
            self.ACUMULADOR = int(self.ALU) + int(self.ACUMULADOR)
        else:
            self.procesador("ADD", memory1)
            self.ACUMULADOR = self.MDR
            self.ALU = self.ACUMULADOR
            self.procesador("ADD", memory2)
            self.ACUMULADOR = self.MDR
            self.ACUMULADOR = int(self.ACUMULADOR) + int(self.ALU)

            if (memory3 != "NULL"):
                self.str(memory3)

    def str(self, *args, **kwargs):
        self.procesador("STORE", args[0])
    
    def end(self, *args, **kwargs):
        print("end")

    def shw(self, *args, **kwargs):
        if args[0] == "ACC":
            print("El acumulador es", self.ACUMULADOR)
        elif args[0] == "ICR":
            print("El ICR es",self.ICR)
        elif args[0] == "MAR":
            print("MAR es", self.MAR)
        elif args[0] == "MDR":
            print("MDR es", self.MDR)
        elif args[0] == "UC":
            print("La unidad de Control es", self.UNIDADCONTROL)
        else: 
            for i in self.MEMORIA:
                if args[0] in i:
                    print("El valor de ", args[0], " es", i.get(args[0]))

    def pause(self, *args, **kwargs):
        print("Pause ejecutado")
        self.running = False

    def dec(self, *args, **kwargs):
        self.procesador("LOAD", args[0])
        self.ACUMULADOR = int(self.ACUMULADOR) - 1
        print("Se ha reducido en 1 el acumulador")
        print("El acumulador es", self.ACUMULADOR)

    def inc(self, *args, **kwargs):
        self.procesador("LOAD", args[0])
        self.ACUMULADOR = int(self.ACUMULADOR) + 1 
        print("Se ha incrementado en 1 el acumulador")
        print("el acumulador es", self.ACUMULADOR)

    def end(self, *args, **kwargs):
        print("End ejecutado")
        print( self.ACUMULADOR)
        self.running = False

if __name__ == "__main__":
    cpu = CBI()
    while True:
        print("CICLO BASICO DE INSTRUCCION")
        print("1. Programa 1")
        print("2. Programa 2")
        print("3. Programa 3")
        print("4. Programa 4")
        print("5. Salir")
        num = int(input("Digite que programa quiere ejecutar: "))

        if num >= 1 and num <= 5:
            if num == 5:
                break
            programa = f"programa{num}.txt"
        
        instrucciones = cpu.read_file(programa)
        if instrucciones:
            cpu.process_instruction(instrucciones)

    
    