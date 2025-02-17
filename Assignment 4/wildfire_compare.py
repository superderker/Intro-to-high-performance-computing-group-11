import numpy as np
import matplotlib.pyplot as plt
import random
import timeit 
from dask import delayed
import dask
import dask.array as da
from dask.distributed import Client
import multiprocessing

# Constants
GRID_SIZE = 800  # 800x800 forest grid
FIRE_SPREAD_PROB = 0.3  # Probability that fire spreads to a neighboring tree
BURN_TIME = 3  # Time before a tree turns into ash
DAYS = 60  # Maximum simulation time

MAX_NUM_SIMULATIONS = 30
MIN_NUM_SIMULATIONS = 1  
SIMULATION_STEP = 4 

serial_times = []
dask_times = []
multiprocess_times = []

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
            # plt.show()
    
    return fire_spread

@delayed
def simulate_wildfire_dask():
    return simulate_wildfire()

def simulate_wildfire_multiprocess(sim_id):
    return simulate_wildfire()

if __name__ == "__main__":
    # serial
    for NUM_SIMULATIONS in range(MIN_NUM_SIMULATIONS, MAX_NUM_SIMULATIONS, SIMULATION_STEP):
        start = timeit.default_timer()

        # Run simulation
        results = [simulate_wildfire() for _ in range(NUM_SIMULATIONS)]
        
        # Aggregate results
        padded_results = [np.pad(sim, (0, DAYS - len(sim)), mode='constant', constant_values=0) for sim in results]
        results_array = np.array(padded_results) 
        avg_fire_spread = np.mean(results_array, axis=0)

        end = timeit.default_timer()
        serial_times.append(end - start)

        print("Serial Execution: ", NUM_SIMULATIONS, "Time: ", end - start)

    
    # multiprocess
    for NUM_SIMULATIONS in range(MIN_NUM_SIMULATIONS, MAX_NUM_SIMULATIONS, SIMULATION_STEP):
        start = timeit.default_timer()

        # Run simulation
        with multiprocessing.Pool() as pool:
            results = pool.map(simulate_wildfire_multiprocess, range(NUM_SIMULATIONS))

        # Aggregate results
        padded_results = [np.pad(sim, (0, DAYS - len(sim)), mode='constant', constant_values=0) for sim in results]
        results_array = np.array(padded_results) 
        avg_fire_spread = np.mean(results_array, axis=0)

        end = timeit.default_timer()
        multiprocess_times.append(end - start)
        print("Multiprocess Execution: ", NUM_SIMULATIONS, "Time: ", end - start)

    # dask
    for NUM_SIMULATIONS in range(MIN_NUM_SIMULATIONS, MAX_NUM_SIMULATIONS, SIMULATION_STEP):
        start = timeit.default_timer()
        
        client = Client(n_workers=NUM_SIMULATIONS)

        # Run simulation
        results = [simulate_wildfire_dask() for _ in range(NUM_SIMULATIONS)]
        results = dask.compute(*results)

        # aggregate results
        results_arrays = [da.from_array(result) for result in results]
        padded_results = [da.pad(arr, (0, DAYS - arr.shape[0]), mode='constant', constant_values=0) for arr in results_arrays]
        stacked_results = da.stack(padded_results)
        stacked_results = stacked_results.rechunk(chunks=(12, DAYS)) # set chunk size
        # Compute the mean of each column (axis=0), which corresponds to the average number of burning trees per day
        avg_fire_spread = stacked_results.mean(axis=0).compute()

        client.close()

        end = timeit.default_timer()
        dask_times.append(end - start)
        print("Dask Execution: ", NUM_SIMULATIONS, "Time: ", end - start)

    print("serial times", serial_times)
    print("multiprocess times", multiprocess_times)
    print("dask times", dask_times)

    plt.figure(figsize=(8, 5))
    plt.plot(range(MIN_NUM_SIMULATIONS, MAX_NUM_SIMULATIONS, SIMULATION_STEP), serial_times, label="Serial")
    plt.plot(range(MIN_NUM_SIMULATIONS, MAX_NUM_SIMULATIONS, SIMULATION_STEP), multiprocess_times, label="Multiprocess")
    plt.plot(range(MIN_NUM_SIMULATIONS, MAX_NUM_SIMULATIONS, SIMULATION_STEP), dask_times, label="Dask")
    plt.xlabel("Number of Simulations")
    plt.ylabel("Time (s)")
    plt.title("Execution Time Comparison")
    plt.legend()
    plt.savefig('wildfire_comparison.png')    