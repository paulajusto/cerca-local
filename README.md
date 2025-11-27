# AZAMON – Cerca Local amb Hill Climbing i Simulated Annealing

Aquest repositori conté la implementació de la pràctica *Pràctica de Búsqueda Local – AZAMON* del Grau en Intel·ligència Artificial (UPC). S’hi resol un problema d’optimització logística utilitzant tècniques de cerca local, comparant el rendiment dels algorismes Hill Climbing i Simulated Annealing.

---

## Descripció del problema

L’objectiu és distribuir eficientment un conjunt de paquets entre diverses ofertes de transport, minimitzant els costos d’enviament i emmagatzematge, i maximitzant la felicitat dels clients en funció de la prioritat i els dies d’entrega.
L’espai de cerca és ampli, ja que cada paquet pot ser assignat a múltiples ofertes segons les seves restriccions.

---

## Representació de l’estat

La solució s’ha representat com una llista d’ofertes, on cada oferta conté els paquets assignats:

```
[
  {paquets_oferta_1},
  {paquets_oferta_2},
  ...
]
```

Aquesta estructura permet aplicar operadors de moviment de forma eficient i mantenir les restriccions de pes i temps.

---

## Operadors implementats

Per generar solucions veïnes, s’han implementat els operadors següents:

* Moure un paquet d’una oferta a una altra.
* Intercanviar dos paquets de diferents ofertes.
* Intercanviar completament els continguts de dues ofertes.

---

## Heurístiques

S’utilitzen tres heurístiques diferents:

1. Heurística basada en els costos (transport + emmagatzematge).
2. Heurística basada en la felicitat dels clients.
3. Heurística combinada (ponderació 60% costos, 40% felicitat).

La tercera s’ha utilitzat principalment per avaluar els algorismes.

---

## Algorismes aplicats

### Hill Climbing

Algorisme de millora local directa. Cerquen sempre un estat veí millor. És molt ràpid, però pot quedar atrapat en mínims locals.

### Simulated Annealing

Permet acceptar solucions pitjors de manera controlada, cosa que ajuda a evitar mínims locals. Requereix més iteracions i temps d’execució, però pot explorar millor l’espai de cerca.
Paràmetres seleccionats: `k = 1`, `lam = 0.0005`, `LIMIT = 5000`.

---

## Experimentació

S’han dut a terme diferents experiments per analitzar:

* L’efecte de les combinacions d’operadors.
* El tipus de solució inicial (aleatòria o ordenada).
* L’ajust dels paràmetres del Simulated Annealing.
* La influència de la proporció del pes transportable.
* L’impacte del nombre de paquets.
* L’evolució de l’heurística al llarg de les iteracions.
* La comparació directa entre Hill Climbing i Simulated Annealing.

Les conclusions mostren que Hill Climbing és més ràpid i suficient per a aquest problema, mentre que Simulated Annealing aporta més capacitat d’exploració però amb un cost d’execució superior.

---

## Contingut del repositori

* Codi Python amb les classes del problema AZAMON.
* Implementació dels operadors.
* Algorismes Hill Climbing i Simulated Annealing configurats.
* Scripts d’experimentació.
* Informe complet de la pràctica.

---

## Autores

Nadia Fernandez, Jana Roman, Júlia Pedrol i Paula Justo
Universitat Politècnica de Catalunya – Facultat d’Informàtica de Barcelona

