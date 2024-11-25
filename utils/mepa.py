from pathlib import Path
from typing import Optional
import math
from dataclasses import dataclass
from functions import reader, labels_index
from time import sleep

@dataclass
class Mepa:
    file: Optional[str] = None
    buffer: Optional[str] = None
    
    file_lines: dict[int:str] = None
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
                    self.file_lines = dict(enumerate([x.replace("\n","") for x in lines]))

                    with open(buffer_path, 'w+') as buffer:
                        buffer.writelines(lines)
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
    # TODO COPIAR A LÓGICA DO DEBUG
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
    # def DEBUG(self):
    #     global buffer
    #     global stack
    #     global index
    #     global p
    #     stack = []

    #     with open(self.file, 'r') as buffer: # TODO MUDAR AS VARS
    #         index = buffer.readlines()
    #         print(f"Iniciando a Depuração:\n\t{index}")
    #         while buffer.readable():
    #             match input("Insere um Comando: "):
    #                 case 'next':
    #                     self.NEXT()
    #                     if index == "PARA":
    #                         print("Finalizando o Debug")
    #                         return
    #                 case 'stack':
    #                     self.STACK()
    #                 case _:
    #                     print("Finalizando Debug")
    #                     return
                    
    def DEBUG(self):
            # global buffer
            global stack, index, p

            stack = []
            index = 0

            print(f"Iniciando a Depuração:\n\t{self.file_lines[index]}")

            while True:
                # match input("Insere um Comando: "):
                match "next":
                    case 'next':
                        self.NEXT()
                        sleep(0.5)
                        if self.file_lines[index] == "PARA":
                            print("Finalizando o Debug")
                            return
                    case 'stack':
                        self.STACK()
                    case _:
                        print("Finalizando Debug")
                        return
            

    # TODO Averiguar sobre o CRVL; CONJ; DISJ; INVR
    # def NEXT(self):
    #     global stack
    #     global index
    #     global p
    #     # labels = labels_index(reader(self.buffer))
    #     # print(labels)
    #     index = buffer.readline()
    #     if index.__contains__('amem'.upper()):
    #         for i in range(int(index.split()[-1])):
    #             stack.append(0)
    #         # print(stack)
    #     elif index.__contains__('crct'.upper()):
    #         val = int(index.split()[-1])
    #         stack.append(val)
    #     elif index.__contains__('crvl'.upper()):
    #         val_index = int(index.split()[-1])
    #         stack.append(stack.index(val_index))
    #     elif index.__contains__('armz'.upper()):
    #         mem_index = int(index.split()[-1])
    #         stack[mem_index] = stack[-1]
    #         stack.pop()
    #     elif index == "SOMA":
    #         stack[-2] = stack[-2] + stack[-1]
    #         stack.pop()
    #     elif index == "MULT":
    #         stack[-2] = stack[-2] * stack[-1]
    #         stack.pop()
    #     elif index == "CMEG":
    #         if stack[-2] <= stack[-1]:
    #             p = True
    #         else:
    #             p = False
    #         stack


    #     print("\t",index)

    def NEXT(self):
        global stack, index, p

        labels = labels_index(reader(self.file))
        # print(labels)
        # print(self.file_lines)
        index += 1
        if self.file_lines[index].__contains__('amem'.upper()):
            for i in range(int(self.file_lines[index].split()[-1])):
                stack.append(0)
            # print(stack)
        if self.file_lines[index].__contains__('dmem'.upper()):
            dmem_range = int(self.file_lines[index].split()[-1])
            for i in range(dmem_range):
                stack.pop()

        elif self.file_lines[index].__contains__('crct'.upper()):
            val = int(self.file_lines[index].split()[-1])
            stack.append(val)

        elif self.file_lines[index].__contains__('crvl'.upper()):
            val_index = int(self.file_lines[index].split()[-1])
            stack.append(stack[val_index])

        elif self.file_lines[index].__contains__('armz'.upper()):
            mem_index = int(self.file_lines[index].split()[-1])
            stack[mem_index] = stack[-1]
            stack.pop()

        elif self.file_lines[index] == "SOMA":
            stack[-2] = stack[-2] + stack[-1]
            stack.pop()

        elif self.file_lines[index] == "MULT":
            stack[-2] = stack[-2] * stack[-1]
            stack.pop()

        elif self.file_lines[index] == "DIVI":
            stack[-2] = stack[-2] / stack[-1]
            stack.pop()

        elif self.file_lines[index] == "SUBT":
            stack[-2] = stack[-2] - stack[-1]
            stack.pop()
        
        elif self.file_lines[index] == "INVR":
            stack[-1] = -stack[-1]
        
        elif self.file_lines[index] ==  "CONJ":
            if stack[-2] and stack[-1]:
                stack[-2] =  1 # True
            else:
                stack[-2] = 0 # False
            stack.pop()

        elif self.file_lines[index] ==  "DISJ":
            if stack[-2] or stack[-1]:
                stack[-2] =  1 # True
            else:
                stack[-2] = 0 # False
            stack.pop()

        # Less Than (<)
        elif self.file_lines[index] == "CMME":
            if stack[-2] < stack[-1]:
                stack.pop()
                stack.pop()
                p = True
            else:
                stack.pop()
                stack.pop()
                p = False

        # Greater Than (>)
        elif self.file_lines[index] == "CMMA":
            if stack[-2] > stack[-1]:
                stack.pop()
                stack.pop()
                p = True
            else:
                stack.pop()
                stack.pop()
                p = False

        # Equal (=)
        elif self.file_lines[index] == "CMIG":
            if stack[-2] == stack[-1]:
                stack.pop()
                stack.pop()
                p = True
            else:
                stack.pop()
                stack.pop()
                p = False

        # Different (<>)
        elif self.file_lines[index] == "CMDG":
            if stack[-2] != stack[-1]:
                stack.pop()
                stack.pop()
                p = True
            else:
                stack.pop()
                stack.pop()
                p = False
        
        # Less Than or Equal (<=)
        elif self.file_lines[index] == "CMEG":
            if stack[-2] <= stack[-1]:
                stack.pop()
                stack.pop()
                p = True
            else:
                stack.pop()
                stack.pop()
                p = False

        # Greater Than or Equal (>=)
        elif self.file_lines[index] == "CMAG":
            if stack[-2] >= stack[-1]:
                stack.pop()
                stack.pop()
                p = True
            else:
                stack.pop()
                stack.pop()
                p = False

        elif self.file_lines[index].startswith("DVSF"):
            label = self.file_lines[index].split()[1]
            if not p:
                index = self.jump_to_index(label, index, labels)
        
        elif self.file_lines[index].startswith("DSVS"):
            label = self.file_lines[index].split()[1]
            index = self.jump_to_index(label, index, labels)
        
        elif self.file_lines[index].startswith("IMPR"):
            print(f"\t{stack[-1]}")
            stack.pop()


        print("\t",self.file_lines[index], '\n\t',stack)

    #TODO CRIAR EXCEPTION
    def jump_to_index(self, label:str, index: int, labels:dict[str:int]) -> int:
        for key, item in labels.items():
            if label == key:
                index = item
        return index

    def STOP(self):
        print("Depuração Encerrada!")

    def STACK(self):
        global stack
        for i,j in enumerate(stack):
            print(f'{i}: {j}')

    # TODO FAZER AO LADO DE LOAD
    def EXIT(self): ...
            

###TESTE###
a = Mepa()
a.LOAD('ex1.mepa', instruction="READ")
# print(a.file_lines)
# print(a)
# a.LIST()
# a.RUN()
# a.INS()
# a.DEL(7)
# a.INS()
# a.SAVE()
a.DEBUG()