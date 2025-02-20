import numpy as np
import dask.array as da
import matplotlib.pyplot as plt
import time
from dask.distributed import Client

# Grid parameters
grid_size = 2000
TIME_STEPS = 100

# Initialize fields as Dask arrays with chunking
chunk_size = (500, 500)
# chunk_size = (1000, 1000)
# chunk_size = (2000, 2000)
temperature = da.random.uniform(5, 30, size=(grid_size, grid_size), chunks=chunk_size)
u_velocity = da.random.uniform(-1, 1, size=(grid_size, grid_size), chunks=chunk_size)
v_velocity = da.random.uniform(-1, 1, size=(grid_size, grid_size), chunks=chunk_size)
wind = da.random.uniform(-0.5, 0.5, size=(grid_size, grid_size), chunks=chunk_size)

def compute_laplacian(field):
    """Compute Laplacian using Dask map_overlap with periodic boundaries."""
    return da.map_overlap(
        lambda block: (
            np.roll(block, shift=1, axis=0) +
            np.roll(block, shift=-1, axis=0) +
            np.roll(block, shift=1, axis=1) +
            np.roll(block, shift=-1, axis=1) -
            4 * block
        ),
        field,
        depth=1,
        boundary='reflect'
    )

def update_u_blocks(u, wind, alpha=0.1, beta=0.02):
    """Update ocean fields using parallelized Dask operations."""
    u = da.asarray(u)
    lap_u = compute_laplacian(u)
    u_new = u + alpha * lap_u + beta * wind
    return u_new

def update_v_blocks(v, wind, alpha=0.1, beta=0.02):
    v = da.asarray(v)
    lap_v = compute_laplacian(v)
    v_new = v + alpha * lap_v + beta * wind
    return v_new

def update_temp_blocks(temp):
    temp = da.asarray(temp)
    lap_temp = compute_laplacian(temp)
    temp_new = temp + 0.01 * lap_temp
    return temp_new

def update_ocean(u, v, temp, wind, alpha=0.1, beta=0.02):
    """Update ocean fields using parallelized Dask operations."""
    u_new = da.map_blocks(
        update_u_blocks,
        u, wind,
        dtype=u.dtype
    )
    v_new = da.map_blocks(
        update_v_blocks,
        v, wind,
        dtype=v.dtype
    )
    temp_new = da.map_blocks(
        update_temp_blocks,
        temp,
        dtype=temp.dtype
    )
    return u_new, v_new, temp_new


if __name__ == "__main__":
    # Run simulation and time it
    start = time.time()

    client = Client(n_workers=8)
    print("Dask Dashboard link:", client.dashboard_link)  # Prints the link to the Dask Dashboard

    for t in range(TIME_STEPS):
        u_velocity, v_velocity, temperature = update_ocean(u_velocity, v_velocity, temperature, wind)
        if t % 8 == 0 or t == TIME_STEPS - 1:
            print(f"Time Step {t}: Updated.")

    # Trigger computation and get final results
    u_final, v_final, temp_final = da.compute(u_velocity, v_velocity, temperature)

    client.close()
    print(f"Execution time: {time.time() - start:.2f} seconds")

    # Visualization
    plt.figure(figsize=(6, 5))
    plt.quiver(u_final[::10, ::10], v_final[::10, ::10])
    plt.title("Ocean Current Directions")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.show()

    plt.figure(figsize=(6, 5))
    plt.imshow(temp_final, cmap='coolwarm', origin='lower')
    plt.colorbar(label="Temperature (°C)")
    plt.title("Ocean Temperature Distribution")
    plt.show()
    print("Simulation complete.")