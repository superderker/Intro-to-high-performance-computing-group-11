import numpy as np
import matplotlib.pyplot as plt
import random
from dask import delayed
import dask
import dask.array as da
from dask.distributed import Client
import timeit

# Constants
GRID_SIZE = 800  # 800x800 forest grid
FIRE_SPREAD_PROB = 0.3  # Probability that fire spreads to a neighboring tree
BURN_TIME = 3  # Time before a tree turns into ash
DAYS = 60  # Maximum simulation time

NUM_SIMULATIONS = 100  # Number of independent wildfire simulations to run in parallel

# State definitions
EMPTY = 0    # No tree
TREE = 1     # Healthy tree 
BURNING = 2  # Burning tree 
ASH = 3      # Burned tree 

def initialize_forest():
    """Creates a forest grid with all trees and ignites one random tree."""
    forest = np.ones((GRID_SIZE, GRID_SIZE), dtype=int)  # All trees
    burn_time = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)  # Tracks how long a tree burns
    
    # Ignite a random tree
    x, y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    forest[x, y] = BURNING
    burn_time[x, y] = 1  # Fire starts burning
    
    return forest, burn_time

def get_neighbors(x, y):
    """Returns the neighboring coordinates of a cell in the grid."""
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Up, Down, Left, Right
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
            neighbors.append((nx, ny))
    return neighbors

@delayed
def simulate_wildfire():
    """Simulates wildfire spread over time."""
    forest, burn_time = initialize_forest()
    
    fire_spread = []  # Track number of burning trees each day
    
    for day in range(DAYS):
        new_forest = forest.copy()
        
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if forest[x, y] == BURNING:
                    burn_time[x, y] += 1  # Increase burn time
                    
                    # If burn time exceeds threshold, turn to ash
                    if burn_time[x, y] >= BURN_TIME:
                        new_forest[x, y] = ASH
                    
                    # Spread fire to neighbors
                    for nx, ny in get_neighbors(x, y):
                        if forest[nx, ny] == TREE and random.random() < FIRE_SPREAD_PROB:
                            new_forest[nx, ny] = BURNING
                            burn_time[nx, ny] = 1
        
        forest = new_forest.copy()
        fire_spread.append(np.sum(forest == BURNING))
        
        if np.sum(forest == BURNING) == 0:  # Stop if no more fire
            break
        
        # Plot grid every 5 days
        # if day % 5 == 0 or day == DAYS - 1:
        #     plt.figure(figsize=(6, 6))
        #     plt.imshow(forest, cmap='viridis', origin='upper')
        #     plt.title(f"Wildfire Spread - Day {day}")
        #     plt.colorbar(label="State: 0=Empty, 1=Tree, 2=Burning, 3=Ash")
        #     plt.show()
    
    return fire_spread



# Run simulation
if __name__ == "__main__":
    times = []
    chunk_size_list = [1, 2, 4, 6, 10, 12, 15, 20, 30, 40, 50, 60]
    client = Client(n_workers=25)

    results = [simulate_wildfire() for _ in range(NUM_SIMULATIONS)]
    results = dask.compute(*results)

    for chunk_size in chunk_size_list:
        print(f"Chunk size: {chunk_size}")
        start = timeit.default_timer()

        # aggregate results
        results_arrays = [da.from_array(result) for result in results]
        padded_results = [da.pad(arr, (0, DAYS - arr.shape[0]), mode='constant', constant_values=0) for arr in results_arrays]

        # Stack all simulations into a single Dask array
        stacked_results = da.stack(padded_results)
        print(stacked_results)
        stacked_results = stacked_results.rechunk(chunks=(chunk_size, DAYS))
        print(stacked_results)

        # Compute the mean of each column (axis=0), which corresponds to the average number of burning trees per day
        avg_fire_spread = stacked_results.mean(axis=0).compute()
        print(avg_fire_spread)

        end = timeit.default_timer()
        print('Time taken in seconds: ', end - start)
        times.append(end - start)

    client.close()
    print(times)
    plt.plot(chunk_size_list, times)
    plt.xlabel("Chunk size")
    plt.ylabel("Time (s)")
    plt.title("Dask Chunk Size vs. Execution Time")
    plt.savefig('wildfire_dask_chunksize.png')