from utils.mepa import Mepa
from utils import functions
from exceptions_files.mepa_exceptions import MepaException
#TODO Fazer a Lógica após de incrementar todos os Métodos do MEPA.mepa.py
#TODO CREATE EXCEPTIONS: Archive not founded; Cannot load archive.
#TODO Print for visualization: Archive loaded Successful

if __name__ == "__main__":
    mepa = Mepa()
    help_list = [
        'LOAD','LIST','RUN','INS <LINE> <INSTRUCTION>','DEL <LINE>', 'DEL <LINE_I> <LINE_J>',
        'SAVE', 'DEBUG', 'NEXT', 'STOP', 'STACK', 'EXIT'
        ]
    while True:
        print(value_input:=input("Insere um Comando:\n (Digite help para saber um pouco mais)")) # Walrus Operator
        match value_input.upper():

            case 'HELP':
                print(*help_list, sep="\n\t")
