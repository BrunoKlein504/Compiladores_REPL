from utils.mepa import Mepa
from utils.mepa_exceptions import MepaException
import os

"""
Feito por Bruno Klein Gomes              - RA: 2201010
      Gabriel Souza Morisco              - RA: 2201686
      Luccas Delgado                     - RA: 2200535
      Guilherme de Oliveira Torres       - RA: 2200412
      Ricardo Mantia da Costa Castellani - RA: 2200292
      Kauã Marcelino Duque               - RA: 2201177

"""

if __name__ == "__main__":
    mepa = Mepa()
    help_list = [
        'LOAD | LOAD <FILE>','LIST','RUN','INS <LINE>,<INSTRUCTION>','DEL <LINE>', 'DEL <LINE_I>,<LINE_J>',
        'SAVE',"***DEBUG SECTION***", 'DEBUG', 'NEXT', 'STOP', 'STACK', 'EXIT'
        ]

    while True:
        value_input = input("Insere um Comando:\n\t>")
        try:
            command = value_input.upper().strip()

            if 'HELP' in command:
                # Exibe a lista de ajuda
                print(" ", *help_list, sep="\n\t")

            elif 'LOAD' in command:
                command_splitted = command.split()

                if len(command_splitted) == 2:
                    mepa.LOAD(command_splitted[-1].lower())
                else:
                    path_files = os.listdir('files')
                    print("Escolhe o Arquivo a Ser Carregado:\n\t", *path_files, sep='\n')
                    file = input("\n\t>")
                    mepa.LOAD(file.strip())

            elif 'LIST' in command:
                mepa.LIST()

            elif "INS" in command:
                command = command.replace("INS","")
                command_splitted = command.split(',')
                line, instruction = command_splitted
                mepa.INS(line=int(line), instruction=instruction.strip()) 

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