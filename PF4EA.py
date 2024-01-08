
from sys import getsizeof
import time
import numpy as np
from numpy.random import randint
import matplotlib as mplt
import matplotlib.pyplot as plt
import re
from tqdm import tqdm
from random import choice
import joblib
from typing import List

class Cella:
    def __init__(self,x=-1,y=-1, str=None):
        if str != None:
            x,y = str.split("-",2)
            self.x : int=int(x)
            self.y : int=int(y)
        else:
            self.x : int = x
            self.y : int = y   

    def getX(self)->int:
        return self.x

    def getY(self)->int:
        return self.y

    def getAdiacenti(self)-> List["Cella"]:
        #cerco le 8 celle più vicine
        vicini = []
        for i in range(self.x - 1, self.x + 2):
            for j in range(self.y - 1, self.y + 2):
                # evito le celle con indice minore di 0 
                if (i, j) != (self.x, self.y) and i >= 0 and j >= 0:
                    vicini.append(Cella(str=f'{i}-{j}'))
        return vicini

    def __str__(self) -> str:
        return f'{self.x}-{self.y}'
    
    def __eq__(self, other) -> bool: 
        """ restituisce True se le 2 celle sono la stessa"""
        assert isinstance(other, Cella)
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int: #ritorno valore hash unico
        return hash((self.x, self.y))      

       
class Mossa:
    def __init__(self, from_: Cella, to_: Cella):
        """ costruttore """
        assert isinstance(from_, Cella) and isinstance(to_, Cella)
        self.from_ : Cella = from_
        self.to_ : Cella = to_
        if from_.getX() == to_.getX() or from_.getY() == to_.getY(): self.cost_ : float = 1
        else: self.cost_ : float = np.sqrt(2)      
    
    def getFrom(self) -> Cella:
        return self.from_
    def getTo(self) -> Cella:
        return self.to_
    def getCost(self)-> float:
        return self.cost_
    
    def checkCollision(self, mossa: "Mossa"):
        assert isinstance(mossa, Mossa)
        if self.from_ == mossa.getFrom(): return True
        elif self.to_ == mossa.getTo(): return True
        elif self.from_ == mossa.getTo() and self.to_ == mossa.getFrom(): return True
        else: return False    

    def __str__(self) -> str:
        return f' {self.from_}->{self.to_} '
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, other) -> bool: 
        """ restituisce True se le 2 celle sono la stessa"""
        assert isinstance(other, Mossa)
        return self.from_ == other.from_ and self.to_ == other.to_
    
    def __hash__(self) -> int:
        return hash((self.from_, self.to_))       


class ListaAdiacenza:
    def __init__(self):
        self.dict = {}
        self.length : int = 0

    def aggiungiLista(self, c: Cella, adiacenti: List[Cella]):
        assert isinstance(c, Cella) and adiacenti != None
        self.dict[c.__str__()] = adiacenti
        self.length += 1

    def getMosse(self, c: Cella) -> Cella:
        assert isinstance(c, Cella)
        return self.dict.get(c.__str__()) # se non trova la chiave restituisce None

    def getVertici(self)-> List[Cella]:
        return map(lambda x: Cella(str=x), self.dict.keys())

    def __str__(self) -> str:
        result = ""
        for key, value in self.dict.items():
            result += key +  ' : ' + str(value) + '\n'
        return result

    def getSize(self) -> int:
        return getsizeof(self.dict)


class Griglia:

    def __init__(self,size, attraversabili: float, agglomerato: int):
        
        assert len(size) == 2 
        self.size = size
        self.attraversabili = attraversabili
        self.agglomerato = agglomerato

        self.griglia = np.ones(self.size, dtype=np.uint8)
        self.lista_adiacenza = ListaAdiacenza()

    def initGriglia(self):       
        self.creaGriglia()
        self.popolaListeAdiacenza()
        self.spazio_memoria_griglia = getsizeof(self.griglia)
        print(f'Spazio occupato griglia: {self.spazio_memoria_griglia} bytes')
        self.spazio_memoria_lista_adiacenza = self.lista_adiacenza.getSize()
        print(f'Spazio occupato lista adiacenza: {self.spazio_memoria_lista_adiacenza} bytes')
        

    def creaGriglia(self):  
        max_ostacoli = int(np.floor(self.dimensioni[0]*self.dimensioni[1]*(1-self.attraversabili)))
        ostacoli_presenti = 0
        start = time.time()
        while ostacoli_presenti < max_ostacoli: 
            
            x,y = randint(0,self.dimensioni[0]), randint(0,self.dimensioni[1])#genero 2 coordinate casuali
            if x < 0 or y < 0: continue
            
            if self.griglia[x,y] != 0:#controllo che non ci sia gia ostacolo in x,y generato
                self.griglia[x,y] = 0
                ostacoli_presenti += 1
            
            # creo gli ostacoli agglomerati vicini
            max_ostacoli_vicini= randint(0,self.agglomerato)
            num_ostacoli_vicini=0
            while num_ostacoli_vicini < max_ostacoli_vicini and ostacoli_presenti < max_ostacoli:
                z,t = choice(self.getVicini(x,y))
                if (z >= 0 and z < self.dimensioni[0]) and (t >= 0 and t < self.dimensioni[1]):
                    if self.griglia[z,t] != 0:
                        self.griglia[z,t] = 0
                        current_obstacle += 1
                        num_ostacoli_vicini +=1

        end = time.time()
        self.tempo_creazione_griglia = end - start
        print(f'Tempo creazione griglia: {self.tempo_creazione_griglia} s')
    
    def mostraGriglia(self, path='img/griglia con percorsi.png'):
        print('Salvo la griglia...\n')
        IMG_SCLALE = 4
        DPI = 200
        n_percorsi = self.griglia.max() - 1
        if n_percorsi > 0:
            colors = []
            colors.append('#000000')
            colors.append('#FFFFFF')
            for i in range(n_percorsi):
                colors.append('#%06X' % randint(0, 0xFFFFFF))
            cmap = mplt.colors.ListedColormap(colors)
            norm = mplt.colors.BoundaryNorm([x for x in range(n_percorsi+2)], cmap.N)

        rows, cols = self.griglia.shape
        fig, ax = plt.subplots(figsize=(int(cols/IMG_SCLALE), int(rows/IMG_SCLALE)))
        

        if n_percorsi > 0: plt.imshow(self.griglia,cmap=cmap, norm=norm)
        else : plt.imshow(self.griglia, cmap="gray",vmin=0, vmax=1)   

        if n_percorsi > 0:
            # scrive gli id dei percorsi nelle celle
            for i in range(0, self.griglia.shape[0]):
                for j in range(0, self.griglia.shape[1]):
                    c = self.griglia[i,j]
                    if c != 1 and c != 0: ax.text(j, i, str(c-1), va='center', ha='center')

        plt.savefig(path, dpi=DPI, bbox_inches='tight')
        print("Griglia salvata in img/")

    def popolaListeAdiacenza(self): # O(N*M)
        print('Creo la lista di adiacenza...')
        start = time.time()
        for i in tqdm(range(self.dimensioni[0])):
            for j in tqdm(range(self.dimensioni[1]),leave=False):
                if self.griglia[i,j] == 1:
                    cella = Cella(x=i,y=j)
                    l = []
                    for c in cella.getCelleAdiacenti():                       
                        # se la cella  è legale e non è un ostacolo, la aggiungo dalla lista
                        if self.isCellaLegale(c) and self.griglia[c.getX(), c.getY()] == 1:
                            l.append(Mossa(cella, c))
                    l.append(Mossa(cella,cella))
                    self.lista_adiacenza.aggiungiLista(cella, l)
        end = time.time()
        self.tempo_popolamento_lista_adiacenza = end - start
        print(f'Tempo popolamento lista adiacenza: {self.tempo_popolamento_lista_adiacenza} s')
        print(f"Num elementi lista di adiacenza: {self.lista_adiacenza.length}")


        
    # restituisce le 8 celle più vicine
    def getVicini(self,x,y):        
        vicini = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                # Esclude il pixel stesso
                if (i, j) != (x, y):
                    vicini.append([i, j])
        return vicini


    def isCellaLegale(self, c: Cella) -> bool:
        assert isinstance(c, Cella)
        return (c.getX() >= 0 and c.getX() < self.dimensioni[0]) and (c.getY() >= 0 and c.getY() < self.dimensioni[1])


    

    def getRandomCella(self):
        x,y = randint(self.dimensioni[0]), randint(self.dimensioni[1])
        while self.griglia[x,y] == 0:
            x,y = randint(self.dimensioni[0]), randint(self.dimensioni[1])
        
        return Cella(x=x,y=y)
    
    def getMosse(self, cella: Cella):
        return self.lista_adiacenza.getMosse(cella)
    

    def getListaAdiacenza(self) -> ListaAdiacenza:
        return self.lista_adiacenza
    
    def aggiungiPercorso(self, percorso, id_percorso):
        assert isinstance(percorso, Percorso)
        init = percorso.getInit()
        self.griglia[init.getX(), init.getY()] = id_percorso
        for mossa in percorso.getSequenzaMosse():
            cella = mossa.getTo()
            self.griglia[cella.getX(), cella.getY()] = id_percorso
