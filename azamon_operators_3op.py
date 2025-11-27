class AzamonOperators(object):
    pass

class MourePaquet(AzamonOperators):
    def __init__(self, p_i: int, o_j: int, o_k: int):
        self.p_i = p_i         # paquet i
        self.o_j = o_j         # oferta j
        self.o_k = o_k         # oferta k
    
    def __repr__(self) -> str:
        return f"Mou paquet {self.p_i} de l'oferta {self.o_j} a l'oferta {self.o_k}" 

class IntercanviarPaquet(AzamonOperators):
    def __init__(self, p_i: int, p_j: int):
        self.p_i = p_i          # paquet i
        self.p_j = p_j          # paquet j
    
    def __repr__(self) -> str:
        return f"Intercanvia paquets {self.p_i} i {self.p_j}"

class IntercanviarOfertes(AzamonOperators):
    def __init__(self, o_i: int, o_j: int):
        self.o_i = o_i          # oferta i
        self.o_j = o_j          # oferta j
    
    def __repr__(self) -> str:
        return f"Intercanvia oferta {self.o_i} i {self.o_j}"
