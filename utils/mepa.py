from pathlib import Path
from typing import Optional
import math
from dataclasses import dataclass
from functions import reader, labels_index, verify_indentifier, verify_stack_address
from time import sleep
from exceptions_files.mepa_exceptions import MepaException

@dataclass
class Mepa:
    file: Optional[str] = None
    buffer: Optional[str] = None
    
    file_lines: dict[int:str] = None

    def LOAD(self, file: Optional[str] = None) -> None:
        path_root = Path(__file__).parents[1] / 'files'

                #Verificar se há modificações antes de abrir outro arquivo
        if self.buffer:
            with open(self.buffer, "r+") as buffer:
                buffer_lines = buffer.readlines()
                with open(self.file, "r+") as archive:
                    archive_lines = archive.readlines()
                    if archive_lines != buffer_lines:
                        print(input_value:=input("Há Modificações Não Salvas. Deseja Salvar? (sim/não)\n\t")) # Walrus Operator
            if input_value.lower()[0] == 's':
                self.SAVE()

        # if not file.endswith('mepa'): TODO CREATE AN EXCEPTION
        if file is not None:
            path = path_root / file
            self.file = path
            buffer_path = path_root / 'buffer.mepa'
            self.buffer = buffer_path
            print("Arquivo existente!")

            with open(path, 'r+') as archive:
                lines = archive.readlines()
                self.file_lines = dict(enumerate([x.replace("\n","") for x in lines]))

                with open(buffer_path, 'w+') as buffer:
                    buffer.writelines(lines)
            print("Arquivo carregado com sucesso!")
        else:
            raise MepaException("O arquivo não existe.")
        


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

        else:
            raise MepaException("Leia um Arquivo Antes!")
     
    def RUN(self):
        if self.file:
            global index, p, stack
            index = 0
            stack = []
            p = False

            if not self.file_lines[index] == "INPP":
                raise MepaException("Código Fonte Deve Iniciar Com a Instrução <INPP>")

            labels = labels_index(reader(self.file))

            #SECTION OF VALIDATORS
            verify_indentifier(self.file_lines)
            verify_stack_address(self.file_lines)


            # print(labels)
            # print(self.file_lines)
            while self.file_lines[index] != "PARA":
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

            # self.runable = True
        else:
            raise MepaException("Leia um arquivo existente!")

    
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

        else:
            raise MepaException("Leia um arquivo existente!")


    def DEL(self, start:int, end:int = None):
        if end is not None:
            if self.file:
                with open(str(self.buffer), 'r+') as buffer:
                    lines = buffer.readlines()
                    buffer.seek(0,0)
                    buffer.truncate()
                    if start > 0 and start <= len(lines) and end > start  and end <= len(lines):
                        # del lines[start-1:end]
                        deleted_lines = lines[start-1:end]
                        del lines[start-1:end]
                        print(f"Linhas <{start}> à <{end}> Deletadas!")
                        print(" ",*deleted_lines, sep='\t')


                        lines[-1] = lines[-1].replace('\n', '')
                        buffer.writelines(lines)
                        # buffer.truncate()
                        # print(f'Linhas <{start}, {end}> Removidas Com Sucesso!')
                    else:
                        print("Linha Inexistente!")
                        return
            else:
                raise MepaException("Leia um arquivo existente!")

        else:
            if self.file:
                with open(self.buffer, 'r+') as buffer:
                    lines = buffer.readlines()
                    buffer.seek(0,0)
                    buffer.truncate()
                    if start > 0 and start <= len(lines):
                        deleted_line = lines.pop(start-1)
                        buffer.writelines(lines)
                        print(f'Linha {start} <{deleted_line.replace("\n","")}> Removida Com Sucesso!')
                    else:
                        print("Linha Inexistente")
            else:
                raise MepaException("Leia um arquivo existente!")


    def SAVE(self):
        if self.file:
            with open(str(self.buffer), 'r') as buffer:
                lines = buffer.readlines()
                self.file_lines = dict(enumerate([x.replace("\n","") for x in lines]))
                with open(str(self.file), 'w') as file:
                    file.writelines(lines)
                    print('Arquivo Salvo!')

            # Deleting the buffer
            Path(self.buffer).unlink()
        else:
            raise MepaException("Não Há arquivos para salvar!")

############################ DEBUG SECTION ###############################

    def DEBUG(self):
            # global buffer
            global stack, index, p

            stack = []
            index = 0
            p = False

            print(f"Iniciando a Depuração:\n\t{self.file_lines[index]}")

            while True:
                match input("Insere um Comando: ").upper():
                # match "NEXT":
                    case 'NEXT':
                        self.NEXT()
                        # self.STACK()
                        # sleep(0.5)
                        if self.file_lines[index] == "PARA":
                            print("Finalizando o Debug")
                            return
                    case 'STACK':
                        self.STACK()
                    case "STOP":
                        self.STOP()
                        return 
                    case _:
                        print("Insere um Comando Válido!\n\tLista De Comandos: NEXT, STACK, STOP")

    def NEXT(self):
        global stack, index, p

        labels = labels_index(reader(self.file))

        #SECTION OF VALIDATORS
        verify_indentifier(self.file_lines)
        verify_stack_address(self.file_lines)

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


        print("\t",self.file_lines[index])

    def jump_to_index(self, label:str, index: int, labels:dict[str:int]) -> int:
        for key, item in labels.items():
            if label == key:
                index = item
        return index

    def STOP(self):
        print("Depuração Encerrada!")

    def STACK(self):
        global stack
        if stack:
            for i,j in enumerate(stack):
                print(f'{i}: {j}')
        else:
            print("Memória Vazia!")

    def EXIT(self):
        if self.buffer:
            with open(self.buffer, "r+") as buffer:
                buffer_lines = buffer.readlines()
                with open(self.file, "r+") as archive:
                    archive_lines = archive.readlines()
                    if archive_lines != buffer_lines:
                        print(input_value:=input("Há Modificações Não Salvas. Deseja Salvar? (sim/não)\n\t")) # Walrus Operator
            if input_value.lower()[0] == 's':
                self.SAVE()
        print("Finalizando o Programa.")
            

# ###TESTE###
# try:
#     a = Mepa()
#     a.LOAD('ex1.mepa')
#     # print(a.file_lines)
#     # print(a)
#     # a.LIST()
#     a.RUN()
#     # a.INS()
#     # a.INS()
#     a.DEL(3,8)
#     # a.LOAD('ex2.mepa')
#     # a.INS()
#     # a.SAVE()
#     # a.RUN()
#     # a.DEBUG()
#     a.EXIT()
# except MepaException as e:
#     print(e)