from __future__ import annotations
import math
from typing import List, Set, Generator
from azamon_operators_3op import *
from abia_azamon import *
import random

class StateAzamon(object):
    def __init__(self, ofertas:List[Oferta], paquetes:List[Paquete], v_ofertas:List[Set[int]]):
        self.ofertas = ofertas
        self.paquetes = paquetes
        self.v_ofertas = v_ofertas

    def copy(self) -> StateAzamon:
        # Afegim el copy per cada set!
        repr_copy = [set_i.copy() for set_i in self.v_ofertas]
        return StateAzamon(self.ofertas, self.paquetes, repr_copy)

    def __str__(self) -> str:
        return f"v_ofertes={str(self.v_ofertas)}"
    
    def buscar_oferta(self, p_i:int) -> int:
        for o_i in range(len(self.v_ofertas)):
            if p_i in self.v_ofertas[o_i]:
                return o_i
            
    def kilos_oferta(self, o_i):
        kg = 0
        for p_i in self.v_ofertas[o_i]:
            kg += self.paquetes[p_i].peso
        return kg
    
    def dias_prioridad(self, p_i):
        if self.paquetes[p_i].prioridad == 0:
            return 1
        elif self.paquetes[p_i].prioridad == 1:
            return 3
        else:
            return 5
        
    def costes_almacenamiento(self, o_i):
        if self.ofertas[o_i].dias == 4 or self.ofertas[o_i].dias == 3:
            cost = 0.25 * self.kilos_oferta(o_i)
        
        elif self.ofertas[o_i].dias == 5:
            cost = 0.25 * self.kilos_oferta(o_i) * 2
        else:
            cost = 0
        return cost
    
    def costes_transportes(self, o_i):
        return self.kilos_oferta(o_i) * self.ofertas[o_i].precio
    
    def felicidad(self, p_i):
        oferta = self.buscar_oferta(p_i)
        entrega = self.ofertas[oferta].dias
        felicidad = 0
        if self.paquetes[p_i].prioridad == 2:   
            if entrega < 4:
                felicidad = 4 - entrega
        elif self.paquetes[p_i].prioridad == 1:
            if entrega < 2:
                felicidad = 2 - entrega
        return felicidad     
    
    def felicidad_total(self):
        fel=0
        for i in range(len(self.paquetes)):
            fel+= self.felicidad(i)    
        return fel    

    def generate_actions(self) -> Generator[AzamonOperators, None, None]:
        peso_libre_ofertas = []
        for o_i, paquetes in enumerate(self.v_ofertas):
            p_o_i = self.ofertas[o_i].pesomax
            for p_i in paquetes:
                p_o_i -= self.paquetes[p_i].peso
            peso_libre_ofertas.append(p_o_i)

        #Moure el paquet
        for o_j, paquets in enumerate(self.v_ofertas):
            for p_i in paquets:
                for o_k in range(len(self.v_ofertas)):
                    if o_j != o_k and self.ofertas[o_k].dias <= self.dias_prioridad(p_i):
                        pes = (peso_libre_ofertas[o_k] - self.paquetes[p_i].peso) >= 0         
                        if pes:
                            yield MourePaquet(p_i, o_j, o_k)

        #Intercanvia el paquet
        for p_i in range(len(self.paquetes)-1):
            for p_j in range(p_i+1, len(self.paquetes)):
                if p_i != p_j:
                    o_i = self.buscar_oferta(p_i)
                    o_j = self.buscar_oferta(p_j)
                    
                    if o_i != o_j and self.ofertas[o_i].dias <= self.dias_prioridad(p_j) and self.ofertas[o_j].dias <= self.dias_prioridad(p_i):
                        p_p_i = self.paquetes[p_i].peso
                        p_p_j = self.paquetes[p_j].peso
                   
                        if  peso_libre_ofertas[o_j] - p_p_i >= p_p_j and peso_libre_ofertas[o_i] - p_p_j >= p_p_i:
                            yield IntercanviarPaquet(p_i,p_j)

        #Intercanvia ofertes
        for o_i in range (len(self.ofertas)-1):
            for o_j in range (o_i+1, len(self.ofertas)):
                if self.ofertas[o_i].pesomax > self.kilos_oferta(o_j) and self.ofertas[o_j].pesomax > self.kilos_oferta(o_i):
                    dias_i = self.ofertas[o_i].dias
                    dias_j = self.ofertas[o_j].dias
                    arriben_a_temps = True
                    for p_i in self.v_ofertas[o_i]:
                        if self.dias_prioridad(p_i)<self.ofertas[o_j].dias:
                            arriben_a_temps = False
                    for p_j in self.v_ofertas[o_j]:
                        if self.dias_prioridad(p_j)<self.ofertas[o_i].dias:
                            arriben_a_temps = False
                    if arriben_a_temps:
                        yield IntercanviarOfertes(o_i, o_j)


    def apply_action(self, action: AzamonOperators) -> 'Paquete':

        new_state = self.copy()

        if isinstance(action, MourePaquet):
            p_i = action.p_i
            o_j = action.o_j
            o_k = action.o_k

            new_state.v_ofertas[o_k].add(p_i)

            new_state.v_ofertas[o_j].remove(p_i)
  
        
        elif isinstance(action, IntercanviarPaquet):
            p_i = action.p_i
            p_j = action.p_j

            c_i = new_state.buscar_oferta(p_i)
            c_j = new_state.buscar_oferta(p_j)

            new_state.v_ofertas[c_i].add(p_j)
            new_state.v_ofertas[c_i].remove(p_i)

            new_state.v_ofertas[c_j].add(p_i)
            new_state.v_ofertas[c_j].remove(p_j)

        elif isinstance(action, IntercanviarOfertes):
            o_i = action.o_i
            o_j = action.o_j

            p_i = self.v_ofertas[o_i]
            p_j = self.v_ofertas[o_j]

            new_state.v_ofertas[o_i] = p_j
            new_state.v_ofertas[o_j] = p_i

        return new_state

    def heuristic(self) -> float:      
        return self.heuristic_costes()*0.6 + self.heuristic_felicidad()*4.3
    
    def heuristic_felicidad(self) -> float:
        felicidad = 0
        for p_i in range(len(self.paquetes)):
            felicidad -= self.felicidad(p_i)
        return felicidad
    
    def heuristic_costes(self) -> float:
        costes_transportes = 0
        costes_almacenamiento = 0
        for o_i in range(len(self.ofertas)):
            costes_transportes += self.costes_transportes(o_i)
            costes_almacenamiento += self.costes_almacenamiento(o_i)
        return costes_transportes + costes_almacenamiento
    
    def generate_one_action(self) -> Generator[AzamonOperators, None, None]:
        peso_libre_ofertas = []
        for o_i, paquetes in enumerate(self.v_ofertas):
            p_o_i = self.ofertas[o_i].pesomax
            for p_i in paquetes:
                p_o_i -= self.paquetes[p_i].peso
            peso_libre_ofertas.append(p_o_i)

        #Moure el paquet
        moure_combinacions = set()
        for o_j, paquets in enumerate(self.v_ofertas):
            for p_i in paquets:
                for o_k in range(len(self.v_ofertas)):
                    if o_j != o_k and self.ofertas[o_k].dias <= self.dias_prioridad(p_i):
                        pes = (peso_libre_ofertas[o_k] - self.paquetes[p_i].peso) >= 0         
                        if pes:
                            moure_combinacions.add((p_i, o_j, o_k))

        #Intercanvia el paquet
        intercanvia_combinacions = set()
        for p_i in range(len(self.paquetes)):
            for p_j in range(len(self.paquetes)):
                if p_i != p_j:
                    o_i = self.buscar_oferta(p_i)
                    o_j = self.buscar_oferta(p_j)
                    
                    if o_i != o_j and self.ofertas[o_i].dias <= self.dias_prioridad(p_j) and self.ofertas[o_j].dias <= self.dias_prioridad(p_i):
                        p_p_i = self.paquetes[p_i].peso
                        p_p_j = self.paquetes[p_j].peso
                   
                        if  peso_libre_ofertas[o_j] - p_p_i >= p_p_j and peso_libre_ofertas[o_i] - p_p_j >= p_p_i:
                            intercanvia_combinacions.add((p_i,p_j))

        #Intercanvia ofertes
        intercanvia_of_combinacions = set()
        for o_i in range (len(self.ofertas)-1):
            for o_j in range (o_i+1, len(self.ofertas)):
                if self.ofertas[o_i].pesomax > self.kilos_oferta(o_j) and self.ofertas[o_j].pesomax > self.kilos_oferta(o_i):
                    dias_i = self.ofertas[o_i].dias
                    dias_j = self.ofertas[o_j].dias
                    arriben_a_temps = True
                    for p_i in self.v_ofertas[o_i]:
                        if self.dias_prioridad(p_i)<self.ofertas[o_j].dias:
                            arriben_a_temps = False
                    for p_j in self.v_ofertas[o_j]:
                        if self.dias_prioridad(p_j)<self.ofertas[o_i].dias:
                            arriben_a_temps = False
                    if arriben_a_temps:
                        intercanvia_of_combinacions.add((o_i, o_j)) 


        n = len(moure_combinacions)
        m = len(intercanvia_combinacions)
        z = len(intercanvia_of_combinacions)
        random_value = random.random()
        if random_value < (n / (n +m+z)):
            combination = random.choice(list(moure_combinacions))
            yield MourePaquet(combination[0], combination[1], combination[2])
        elif random_value >=(n / (n + m +z)) and random_value <((n + m)/ (n + m +z)):
            combination = random.choice(list(intercanvia_combinacions))
            yield IntercanviarPaquet(combination[0], combination[1])
        else:
            combination = random.choice(list(intercanvia_of_combinacions))
            yield IntercanviarOfertes(combination[0], combination[1])


def generate_initial_state(ofertas:List[Oferta], paquetes:List[Paquete]) -> StateAzamon:
    v_ofertes = [set() for _ in range(len(ofertas))]
    peso_ofertas = [i.pesomax for i in ofertas]

    def dias_prioridad(p):
        if p.prioridad == 0:
            return 1
        elif p.prioridad == 1:
            return 3
        else:
            return 5

    #AÑADIR PAQUETES A NUESTRA REPRESENTACIÓN DE LAS OFERTAS
    of = len(peso_ofertas)-1
    i=0
    while i< (len(paquetes)):
        if paquetes[i].peso <= peso_ofertas[of] and dias_prioridad(paquetes[i])>=ofertas[of].dias:
            v_ofertes[of].add(i)
            peso_ofertas[of]-= paquetes[i].peso
            i+=1
            of = len(ofertas)-1

        else:
            of-=1       
  
    return StateAzamon(ofertas, paquetes, v_ofertes)

def generate_initial_state2(ofertas:List[Oferta], paquetes:List[Paquete]) -> StateAzamon:
    v_ofertes = [set() for _ in range(len(ofertas))]
    peso_ofertas = [i.pesomax for i in ofertas]

    #ORDENAR PAQUETES
    paquetes_ordenados = []
    for i in range(3):
        for j in range(len(paquetes)):
            if paquetes[j].prioridad == i:
                paquetes_ordenados.append(paquetes[j])

    peso_paquetes = [i.peso for i in paquetes_ordenados]
    
    #AÑADIR PAQUETES A NUESTRA REPRESENTACIÓN DE LAS OFERTAS
    of = 0
    i=0
    while i< (len(paquetes_ordenados)):
        if paquetes_ordenados[i].peso <= peso_ofertas[of]:
            v_ofertes[of].add(i)
            peso_ofertas[of]-= paquetes_ordenados[i].peso
            i+=1
        else:
            of+=1

    return StateAzamon(ofertas, paquetes_ordenados, v_ofertes)


