from pathlib import Path
from typing import Optional
import math
from dataclasses import dataclass

@dataclass
class Mepa:
    file: Optional[str] = None
    file_size: Optional[int] = None
    buffer: Optional[str] = None
    lines: Optional[int] = None
    runable: Optional[bool] = None

    # TODO Change the logic of Mepa.file and Mepa.buffer

    # TODO CREATE EXCEPTIONS: Archive not founded; Cannot load archive.
    # TODO Print for visualization: Archive loaded Successful
    # TODO Updating File (maybe, needs to implement SAVE() function)
    def LOAD(self, file: Optional[str] = None, instruction: Optional[str] = None) -> None:
        path_root = Path(__file__).parents[1] / 'files'

        ###READ###
        # This parameter appears not to be to implement
        if instruction == "READ":
            if file is not None:
                path = path_root / file
                self.file = path
            # if not file.endswith('mepa'): TODO CREATE AN EXCEPTION
                print("Arquivo existente!")
                with open(path, 'r') as archive:
                    self.buffer = archive.read() # Store each command in the buffer of class
                    archive.seek(0,0) # Reset the pointer
                    self.lines = len(archive.readlines()) # Returning the total of lines
                    self.file_size = archive.tell() # Getting the size of archive
                print("Arquivo carregado com sucesso!")
            else:
                print("Erro: O arquivo não existe.")

    def LIST(self):

        if self.file:

            number_loop = math.ceil(self.lines / 20)
            i = 0

            with open(str(self.file), 'r') as file:
                lines = file.readlines()

            for i in range(number_loop):
                start = i * 20
                end = start + 20

                for j in range(start, min(end, len(lines))):
                    print(lines[j].strip())

                print(input("\nAperte Enter para continuar..."))

        else: # TODO Create an Exception
            print('Leia um arquivo existente!')

    def RUN(self):
        if self.file:
            print("Ativo!") # Mock print
            self.runable = True
        else: # TODO Create an Exception
            print("Leia um arquivo existente!")

    # TODO Improve the Logic
    def INS(self, line: int = None, instruction: str = None):
        if self.file:
            with open(str(self.file), 'r+') as file:
                lines = file.readlines()

                if line is None or instruction is None:
                    input_data = input("Insere a linha e a instrução desejada (Ex: 1, CRCT 5): ")
                    line, instruction = input_data.split(',')
                    line = int(line)
                    instruction = instruction.strip()
                
                if int(line) < 0:
                    print("A linha não pode ser negativa!")
                elif line <= len(lines):
                    lines[line - 1] = instruction.upper() + "\n"
                    print("Linha atualizada!")
                else:
                    lines.append("\n" + instruction.upper() + "\n")
                    print("Linha adicionada!")

                self.buffer = ''.join(lines)

        else:  # TODO Create an Exception
            print("Leia um arquivo existente!")


    def DEL(start:int, end:int = None):...
    def SAVE(): ...
############################ DEBUG SECTION ###############################
    def DEBUG(): ...
    def NEXT(): ...
    def STOP(): ...
    def STACK(): ...
    def EXIT(): ...
            

###TESTE###
a = Mepa()
a.LOAD('ex1.mepa', instruction="READ")
# a.LIST()
# a.RUN()
a.INS()
# print(a.buffer,'\n')
# with open(a.file) as archive:
#     print(archive.read())
# print(a)
