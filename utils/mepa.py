from pathlib import Path
from typing import Optional
import math
from dataclasses import dataclass

@dataclass
class Mepa:
    file: Optional[str] = None
    file_size: Optional[int] = None

    buffer: Optional[str] = None
    buffer_size: Optional[int] = None

    file_lines: Optional[int] = None
    buffer_lines: Optional[int] = None
    
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
                buffer_path = path_root / 'buffer.mepa'
                self.buffer = buffer_path
            # if not file.endswith('mepa'): TODO CREATE AN EXCEPTION
                print("Arquivo existente!")
                with open(path, 'r+') as archive:
                    lines = archive.readlines()
                    self.lines = len(lines) # Returning the total of lines
                    self.file_size = archive.tell() # Getting the size of archive

                    with open(buffer_path, 'w+') as buffer:
                        buffer.writelines(lines)
                        self.buffer_lines = self.lines
                        self.buffer_size = self.file_size
                    
                print("Arquivo carregado com sucesso!")
            else:
                print("Erro: O arquivo não existe.")

    def LIST(self):

        if self.buffer:

            number_loop = math.ceil(self.buffer_lines / 20)
            i = 0

            with open(str(self.buffer), 'r') as file:
                lines = file.readlines()

            for i in range(number_loop):
                start = i * 20
                end = start + 20

                for j in range(start, min(end, len(lines))):
                    print(lines[j].strip())

                print(input("\nAperte Enter para continuar..."))

        else: # TODO Create an Exception
            print('Leia um arquivo existente!')


    #TODO MUDAR A LÒGICA AQUI, VERIFICA SE ESTUDO ESTÁ OK {Gramaticas e etc}
    def RUN(self):
        if self.buffer:
            print("Ativo!") # Mock print
            self.runable = True
        else: # TODO Create an Exception
            print("Leia um arquivo existente!")

    # TODO Improve the Logic
    def INS(self, line: int = None, instruction: str = None):
        if self.file:
            with open(str(self.buffer), 'r+') as file:
                lines = file.readlines()
                file.seek(0) # Reset the pointer (dodging for copies)

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
                    lines.append('\n' + instruction.upper())
                    print("Linha adicionada!")

                # self.buffer = ''.join(lines)
                file.writelines(lines)

        else:  # TODO Create an Exception
            print("Leia um arquivo existente!")


    def DEL(self, start:int, end:int = None):
        if end:
            if self.file:
                with open(str(self.buffer), 'r+') as buffer:
                    lines = buffer.readlines()
                    buffer.seek(0)
                    if start > 0 and start <= len(lines) and end > start  and end <= len(lines):
                        del lines[start-1:end]
                        lines[-1] = lines[-1].replace('\n', '')
                        buffer.writelines(lines)
                        buffer.truncate()
                        print(f'Linhas <{start}, {end}> Removidas Com Sucesso!')
                    else:
                        print("Linha Inexistente")
                        return
            else:
                # TODO EXCEPTION
                ...

        else:
            if self.file:
                with open(str(self.buffer), 'r+') as buffer:
                    lines = buffer.readlines()
                    buffer.seek(0)
                    if start > 0 and start <= len(lines):
                        del lines[start - 1]
                        buffer.writelines(lines)
                        print(f'Linha <{start}> Removida Com Sucesso!')
                    else:
                        print("Linha Inexistente")
                        return
            else:
                ... # TODO FAZER UM EXCEPTION

    def SAVE(self):
        if self.file:
            with open(str(self.buffer), 'r') as buffer:
                lines = buffer.readlines()
                with open(str(self.file), 'w') as file:
                    file.writelines(lines)
                    print('Arquivo Salvo!')
        else:
            #TODO Exception
            ...
############################ DEBUG SECTION ###############################
    def DEBUG(self):
        global buffer
        global stack
        global index
        global p
        stack = []

        with open(str(self.buffer), 'r') as buffer:
            index = buffer.readline()
            print(f"Iniciando a Depuração:\n\t{index}")
            while buffer.readable():
                match input("Insere um Comando: "):
                    case 'next':
                        self.NEXT()
                        if index == "PARA":
                            print("Finalizando o Debug")
                            return
                    case 'stack':
                        self.STACK()
                    case _:
                        print("Finalizando Debug")
                        return
                

    # TODO Averiguar sobre o CRVL; CONJ; DISJ; INVR
    def NEXT(self):
        global stack
        global index
        global p
        p_condition = False
        index = buffer.readline()
        if index.__contains__('amem'.upper()):
            for i in range(int(index.split()[-1])):
                stack.append(0)
            # print(stack)
        elif index.__contains__('crct'.upper()):
            val = int(index.split()[-1])
            stack.append(val)
        elif index.__contains__('crvl'.upper()):
            val_index = int(index.split()[-1])
            stack.append(stack.index(val_index))
        elif index.__contains__('armz'.upper()):
            mem_index = int(index.split()[-1])
            stack[mem_index] = stack[-1]
            stack.pop()
        elif index == "SOMA":
            stack[-2] = stack[-2] + stack[-1]
            stack.pop()
        elif index == "MULT":
            stack[-2] = stack[-2] * stack[-1]
            stack.pop()
        elif index == "CMEG":
            if stack[-2] <= stack[-1]:...


        print("\t",index)
    
        

    def STOP(self): ...
    def STACK(self):
        global stack
        for i,j in enumerate(stack):
            print(f'{i}: {j}')
    def EXIT(self): ...
            

###TESTE###
a = Mepa()
a.LOAD('ex1.mepa', instruction="READ")
# print(a)
# a.LIST()
# a.RUN()
# a.INS()
# a.DEL(7)
# a.INS()
# a.SAVE()
a.DEBUG()