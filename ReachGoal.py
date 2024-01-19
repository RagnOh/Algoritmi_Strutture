from json.encoder import INFINITY
import numpy as np
from PF4EA import PF4EA, Cella, Mossa, Percorso
import heapq


D=np.sqrt(2)

#Reach goal esegue A* in VxN, dove V sono i vertici del grafo (le celle) e N istanti di tempo
#ciascuno stato indica quindi dove si trova il nuovo agente in un certo istante di tempo
class Stato:
    def __init__(self, cella:Cella, istante:int):
        self.cella=cella
        self.istante=istante
        
    def getCella(self) -> Cella:
        return self.cella
    
    def getIstante(self) -> int:
        return self.istante
    
    def __str__(self) -> str:
        return f'({self.cella}, {self.istante})'
    
    
class ReachGoal:
    def __init__(self, init:Cella, goal:Cella, ist:PF4EA):
        self.init=init
        self.goal=goal
        self.max=ist.getMax
        self.ist=ist
        self.adiacenze=ist.getListaAdiacenza()
        self.open=set()
        self.closed=set()
        self.fscore=[] #heapqueue che contiene il valore di f per ogni stato v, f=g+ h(=stima eurisitca del costo per raggiungere il goal da v)
        #self.max_open=0 #dim max della open list
        #self.max_close=0 #dim max della close list
        self.gscore=dict() #(g): associa ad ogni stato il costo minore finora calcolato per raggiungerlo partendo da init all'istante 0
        self.genitore=dict() #(p): associa ad ogni stato il suo stato predecessore nell'albero dei cammini minimi
        self.spazio_occupato_score=0
        self.percorso=Percorso(init, goal)
        self.percorsi=ist.getPercorsi()
       
    #ricerca di un percorso per un nuovo agente che da self.init vada in self.goal in una durata < di self.max
    def ricerca(self)-> Percorso:
         if self.passiMinimi>self.max:
             return True
         else:
             self.open.add(Stato(self.init, 0))
             self.gscore[Stato(self.init, 0)] #costo per raggiungere lo stato iniziale =0
             heapq.heappush(self.fscore, ((Stato(self.init,0)), self.heuristic(self.init, self.goal))) #aggiungo lo stato iniziale in fscore con f=heurisc
             while len(self.open) != 0:
                 (stato, score)=heapq.heappop(self.fscore)
                 self.open.remove(stato)
                 self.closed.add(stato)
                 cella=stato.getCella()
                 istante=stato.getIstante()
                 if cella == self.goal:
                     return self.reconstructPath(stato, self.genitore, Percorso(self.init, self.goal))
                 

                rilassato=percorsoRilassato(self)


                 if stato.getIstante() < self.max:#t+1 o t???
                     for n in cella.getAdiacenti(): #CAMBIA CON for mossa_successiva in self.adiacenze.getMosse(v): 
                         if (Stato(n, istante+1) not in self.closed):
                             traversable=True
                             if self.percorso.checkCollisioneMossa(n, self.percorsi, istante):
                                 traversable=False
                             if traversable:
                                 if self.gscore.get(stato, INFINITY) + (Mossa (cella, n)).getCost() < self.gscore.get(Stato(n, istante+1),INFINITY):
                                     self.genitore[Stato(n, istante+1)]=stato
                                     self.gscore[Stato(n, istante+1)]=self.gscore.get(stato,INFINITY)+(Mossa (cella, n)).getCost()
                                     heapq.heappush(self.fscore, (Stato(n, istante+1), (self.gscore.get(Stato(n, istante+1),INFINITY)+self.heuristic(n, self.goal))))
                                 if Stato(n, istante+1) not in self.open:
                                     self.open.add(Stato(n, istante+1))
                 return False
                                                          
                             
                             
                             

                             
                             
                             
                     
                     
                 
    
    def heuristic(self, v: Cella, goal: Cella) -> int: #euristica che calcola distanza diagonale tra v e goal
         dx = abs(v.getX - goal.getX)
         dy = abs(v.getYy - goal.getY)
         return (dx + dy)+(D-2)*min(dx, dy)
    
        
    def reconstructPath(self,stato:Stato,genitori,percorsoMin:Percorso) -> Percorso:
        while stato.getIstante() > 0:
            padre=genitori[stato]
            percorsoMin.prepend(Mossa(padre.getCella(), stato.getCella()))
            stato=padre
        assert percorsoMin.getLunghezza()>0
        return percorsoMin
    
    def passiMinimi(self, v:Cella, goal: Cella) -> int:
        return max(np.abs(v.getX-goal.getX), np.abs(v.getY-goal.getY))


    def percorsoRilassato(self, stato:Stato):
        rilassato=Percorso(self.init, self.goal)
        open=self.open.copy()
        closed=self.closed.copy()
        genitori=self.genitore.copy()
        gscore=self.gscore.copy()
        fscore=self.fscore.copy()

        open.add(stato) #riaggiungo stato in open che diventa lo stato iniziale da cui inizia la mia ricerca del mio percorso rilassato
        fscore.insert(0,(stato, self.heuristic(stato.getCella(), self.goal)))

        while len(open) != 0:
            (stato, score)=heapq.heappop(self.fscore)
            open.remove(stato)
            closed.add(stato)
            cella=stato.getCella()
            istante=stato.getIstante()
            if cella == self.goal:
                return self.reconstructPath(stato, genitori, rilassato)
            
            if stato.getIstante() < self.max: #t+1 o t???
                     for n in cella.getAdiacenti(): #CAMBIA CON for mossa_successiva in self.adiacenze.getMosse(v): 
                         if (Stato(n, istante+1) not in self.closed):
                             
                                 if self.gscore.get(stato, INFINITY) + (Mossa (cella, n)).getCost() < self.gscore.get(Stato(n, istante+1),INFINITY):
                                     self.genitore[Stato(n, istante+1)]=stato
                                     self.gscore[Stato(n, istante+1)]=self.gscore.get(stato,INFINITY)+(Mossa (cella, n)).getCost()
                                     heapq.heappush(self.fscore, (Stato(n, istante+1), (self.gscore.get(Stato(n, istante+1),INFINITY)+self.heuristic(n, self.goal))))
                                 if Stato(n, istante+1) not in self.open:
                                     self.open.add(Stato(n, istante+1))
            return False








        

    
    
    
    
    
