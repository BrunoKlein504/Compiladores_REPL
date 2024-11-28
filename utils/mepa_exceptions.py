"""
Feito por Bruno Klein Gomes              - RA: 2201010
      Gabriel Souza Morisco              - RA: 2201686
      Luccas Delgado                     - RA: 2200535
      Guilherme de Oliveira Torres       - RA: 2200412
      Ricardo Mantia da Costa Castellani - RA: 2200292
      Kauã Marcelino Duque               - RA: 2201177

"""

class MepaException(Exception):
    def __init__(self, msg:str):
        self.msg = msg
    
    def __str__(self) -> str:
        return f"Erro: {self.msg}"