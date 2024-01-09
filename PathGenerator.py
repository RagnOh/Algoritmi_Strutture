from ReachGoal import ReachGoal
from PF4EA import PF4EA, Percorso

PRINT_PERCORSI = False


def genera(istanza: PF4EA, n_percorsi = 1)->Percorso:
    assert n_percorsi >= 0        
    print(f'Creazione {n_percorsi} percorsi...')
       
    percorsi = []
    non_raggiungibili = 0
    while len(percorsi) < n_percorsi:
        if non_raggiungibili > 70:
            raise Exception('Attenzione, troppi percorsi non raggiungibili!')
        i = istanza.getCellaInit()
        g = istanza.getCellaGoal(init = i)
        if i != g:           

            ist = ReachGoal(istanza, i, g)
            percorso = ist.ricerca(con_rilassato=True)
            del ist

            if isinstance(percorso, Percorso):
                assert len(percorso.sequenza_mosse) > 0
                percorsi.append(percorso)
                print('> Ho creato il percorso!')
                if PRINT_PERCORSI: print(percorso)     
            elif percorso == False:
                print('! Percorso non raggiungibile!')
                non_raggiungibili += 1
            else: 
                print('! Orizzonte temporale troppo breve!')
    print(f'Sono stati creati {n_percorsi} percorsi')
    istanza.setPercorsi(percorsi)
    istanza.aggiungiPercorsiAllaGriglia()