



def generateGrid(width,height,num_obstacle):

        import random


        GRID_WIDTH = width
        GRID_HEIGHT = height
        NUM_BLACK_CELLS = num_obstacle

# Crea una griglia vuota con celle bianche
        grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Posizioni casuali per le celle nere
        black_cell_positions = set()
        while len(black_cell_positions) < NUM_BLACK_CELLS:
              x = random.randint(0, GRID_WIDTH - 1)
              y = random.randint(0, GRID_HEIGHT - 1)
              black_cell_positions.add((x, y))

# Imposta le celle nere nella griglia
        for x, y in black_cell_positions:
            grid[y][x] = 1

        green_agent_x = random.randint(0, GRID_WIDTH - 1)
        green_agent_y = random.randint(0, GRID_HEIGHT - 1)

# Imposta l'agente verde nella griglia
        grid[green_agent_y][green_agent_x] = 'A'  

        goal_x = random.randint(0, GRID_WIDTH - 1)
        goal_y = random.randint(0, GRID_HEIGHT - 1)

# Imposta il "goal" rosso nella griglia
        grid[goal_y][goal_x] = 'G'   
 
# Stampa la griglia
        for row in grid:
            for cell in row:
                if cell == 0:
                   print("⬜", end=" ")  # Cella bianca
                elif cell == 1:
                   print("⬛", end=" ")  # Cella nera
                elif cell == 'A':
                   print("🟩", end=" ")  # Agente verde
                elif cell == 'G':
                   print("🟥", end=" ")  # "Goal" rosso
            print()  # Vai a una nuova riga per la prossima fila

        black_cell_positions   
        

def generateVisualGrid(w,h,n):
     
     import matplotlib.pyplot as plt
     import numpy as np
     import random

# Imposta le dimensioni della grigli a e il numero di celle nere
     GRID_WIDTH = w
     GRID_HEIGHT = h
     NUM_BLACK_CELLS = n

# Inizializza la griglia binaria
     grid_binary = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)

# Scegli posizioni casuali per le celle nere
     black_cell_positions = set()
     while len(black_cell_positions) < NUM_BLACK_CELLS:
           x = random.randint(0, GRID_WIDTH - 1)
           y = random.randint(0, GRID_HEIGHT - 1)
           black_cell_positions.add((x, y))
           grid_binary[y][x] = 1

     grid_with_borders = np.zeros((GRID_HEIGHT * 2 - 1, GRID_WIDTH * 2 - 1), dtype=int)
     grid_with_borders[1::2, 1::2] = grid_binary      

# Crea una rappresentazione grafica della griglia
     plt.imshow(grid_with_borders, cmap='gray', origin='upper', extent=[0, GRID_WIDTH, 0, GRID_HEIGHT])
     plt.colorbar()
     plt.show()