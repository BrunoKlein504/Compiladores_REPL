from utils.mepa import Mepa
from utils.mepa_exceptions import MepaException
import os
from time import sleep
#TODO Fazer a Lógica após de incrementar todos os Métodos do MEPA.mepa.py
#TODO CREATE EXCEPTIONS: Archive not founded; Cannot load archive.
#TODO Print for visualization: Archive loaded Successful

if __name__ == "__main__":
    mepa = Mepa()
    help_list = [
        'LOAD','LIST','RUN','INS <LINE>,<INSTRUCTION>','DEL <LINE>', 'DEL <LINE_I>,<LINE_J>',
        'SAVE', 'DEBUG', 'NEXT', 'STOP', 'STACK', 'EXIT'
        ]

    while True:
        value_input = input("Insere um Comando:\n(Digite help para saber um pouco mais)\n\t>")
        try:
            # Converter para maiúsculas para garantir que a comparação seja insensível ao caso
            command = value_input.upper().strip()

            if 'HELP' in command:
                # Exibe a lista de ajuda
                print(" ", *help_list, sep="\n\t")

            elif 'LOAD' in command:
                # Carregar arquivos da pasta "files"
                path_files = os.listdir('files')
                print("Escolhe o Arquivo a Ser Carregado:\n\t", *path_files, sep='\n')
                file = input("\n\t>")
                mepa.LOAD(file.strip())

            elif 'LIST' in command:
                # Lista os itens
                mepa.LIST()

            elif "INS" in command:
                command = command.replace("INS","")
                command_splitted = command.split(',')
                line, instruction = command_splitted
                mepa.INS(line=int(line), instruction=instruction.strip()) 

            # TODO Catch values
            elif "DEL" in command:
                command = command.replace("DEL","")

                if command.__contains__(','):
                    command_splitted = command.split(',')
                    start_line, end_line = command_splitted
                    mepa.DEL(start=int(start_line),end=int(end_line))
                
                else:
                    mepa.DEL(start=int(command))
            
            elif "SAVE" in command:
                mepa.SAVE()

            elif "RUN" in command:
                mepa.RUN()

            elif "EXIT" in command:
                mepa.EXIT()
                break
            
            elif "DEBUG" in command:
                mepa.DEBUG()    

            else:
                print("Comando não reconhecido. Digite 'help' para mais informações.")

        except (MepaException, Exception) as e:
            print(e)