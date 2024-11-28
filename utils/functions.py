from pathlib import Path
import re
from .mepa_exceptions import MepaException

"""
Feito por Bruno Klein Gomes              - RA: 2201010
      Gabriel Souza Morisco              - RA: 2201686
      Luccas Delgado                     - RA: 2200535
      Guilherme de Oliveira Torres       - RA: 2200412
      Ricardo Mantia da Costa Castellani - RA: 2200292
      Kauã Marcelino Duque               - RA: 2201177

"""


def reader(path:Path | None) -> str:
    if path is None:
        path = Path(__file__).parents[1] / "files" / "ex1.mepa"
    
    with open(path) as archive:
        return archive.readlines()

def labels_index(archive:str) -> dict[str:int]:
    labels = {}
    for index, line in enumerate(archive):
        if line.startswith(r"L"):
            label = line.split(":")[0]
            labels[label] = index
        
    return labels

def verify_indentifier(code_file:dict[int:str]) -> None:
    pattern = r"[AMEM|ARMZ|CRCT|CRVL|DMEM]*\s([^0-9]*)"
    for key, value in code_file.items():
        match_pattern = re.fullmatch(pattern, value)

        if match_pattern:
            raise MepaException(f"Linha <{key} : {value}> Contém Indetificador '{value.split()[-1]}' Inválido")

def verify_stack_address(code_file:dict[int:str]) -> None:
    for value in code_file.values():
        if value.__contains__("AMEM"):
            allocated_vars_size = int(value.split()[-1])
    
    for key, value in code_file.items():
        if value.__contains__("CRVL"):
            if int(value.split()[-1]) >= allocated_vars_size:
                raise MepaException(f"Valor Inexistente <Linha {key+1} : {value}> No Endereço da Memória")

def jump_to_index(label:str, index: int, labels:dict[str:int]) -> int:
        for key, item in labels.items():
            if label == key:
                index = item
        return index
