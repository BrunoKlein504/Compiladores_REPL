class MepaException(Exception):
    def __init__(self, msg:str):
        self.msg = msg
    
    def __str__(self) -> str:
        return f"Erro: {self.msg}"