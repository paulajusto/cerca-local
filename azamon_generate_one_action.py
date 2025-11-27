import random

def generate_one_action(self) -> Generator[BinPackingOperator, None, None]:
    # Primer calculem l'espai lliure de cada contenidor
    free_spaces = []
    for c_i, parcels in enumerate(self.v_c):
        h_c_i = self.params.h_max
        for p_i in parcels:
            h_c_i = h_c_i - self.params.v_h[p_i]
        free_spaces.append(h_c_i)

    # Recorregut contenidor per contenidor per saber quins paquets podem moure
    move_parcel_combinations = set()
    for c_j, parcels in enumerate(self.v_c):
        for p_i in parcels:
            for c_k in range(len(self.v_c)):
                # Condició: contenidor diferent i té espai lliure suficient
                if c_j != c_k and free_spaces[c_k] >= self.params.v_h[p_i]:
                    move_parcel_combinations.add((p_i, c_j, c_k))

    # Intercanviar paquets
    swap_parcels_combinations = set()
    for p_i in range(self.params.p_max):
        for p_j in range(self.params.p_max):
            if p_i != p_j:
                c_i = self.find_container(p_i)
                c_j = self.find_container(p_j)

                if c_i != c_j:
                    h_p_i = self.params.v_h[p_i]
                    h_p_j = self.params.v_h[p_j]

                    # Condició: hi ha espai lliure suficient per fer l'intercanvi
                    # (Espai lliure del contenidor + espai que deixa el paquet >= espai del nou paquet)
                    if free_spaces[c_i] + h_p_i >= h_p_j and free_spaces[c_j] + h_p_j >= h_p_i:
                        swap_parcels_combinations.add((p_i, p_j))

    n = len(move_parcel_combinations)
    m = len(swap_parcels_combinations)
    random_value = random.random()
    if random_value < (n / (n + m)):
        combination = random.choice(list(move_parcel_combinations))
        yield MoveParcel(combination[0], combination[1], combination[2])
    else:
        combination = random.choice(list(swap_parcels_combinations))
        yield SwapParcels(combination[0], combination[1])
