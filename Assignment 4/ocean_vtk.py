import time
import numpy as np
import matplotlib.pyplot as plt
import pyvtk

# Grid size
grid_size = 200
TIME_STEPS = 100

# Initialize temperature field (random values between 5C and 30C)
temperature = np.random.uniform(5, 30, size=(grid_size, grid_size))

# Initialize velocity fields (u: x-direction, v: y-direction)
u_velocity = np.random.uniform(-1, 1, size=(grid_size, grid_size))
v_velocity = np.random.uniform(-1, 1, size=(grid_size, grid_size))

# Initialize wind influence (adds turbulence)
wind = np.random.uniform(-0.5, 0.5, size=(grid_size, grid_size))

def laplacian(field):
    """Computes the discrete Laplacian of a 2D field using finite differences."""
    lap = (
        np.roll(field, shift=1, axis=0) +
        np.roll(field, shift=-1, axis=0) +
        np.roll(field, shift=1, axis=1) +
        np.roll(field, shift=-1, axis=1) -
        4 * field
    )
    return lap

def update_ocean(u, v, temperature, wind, alpha=0.1, beta=0.02):
    """Updates ocean velocity and temperature fields using a simplified flow model."""
    u_new = u + alpha * laplacian(u) + beta * wind
    v_new = v + alpha * laplacian(v) + beta * wind
    temperature_new = temperature + 0.01 * laplacian(temperature)  # Small diffusion
    return u_new, v_new, temperature_new

def save_to_vtk(filename, u_velocity, v_velocity, temperature, wind):
    """
    Save the evolving simulation data as a VTK file.
    This function writes the velocity, temperature, and wind fields to a VTK file.
    """
    # Flatten the arrays to be stored in VTK format
    u_flat = u_velocity.T.flatten()
    v_flat = v_velocity.T.flatten()
    temp_flat = temperature.flatten()
    wind_flat = wind.flatten()

    # Grid size (assuming a 2D grid)
    nx, ny = u_velocity.shape

    # Create VTK structure
    vtk_data = pyvtk.VtkData(
        pyvtk.StructuredPoints([nx, ny, 1]),  # 2D structured grid
        pyvtk.PointData(
            pyvtk.Vectors(np.column_stack((u_flat, v_flat, np.zeros_like(v_flat))), name="velocity"),  # Velocity as vectors
            pyvtk.Scalars(temp_flat, name="temperature"),  # Temperature as scalar field
            pyvtk.Scalars(wind_flat, name="wind")  # Wind as scalar field
        )
    )
    vtk_data.tofile(filename)  # Write the VTK file
    print(f"Saved VTK file: {filename}")

outputCount = 1
# Run the simulation
start = time.time()
for t in range(TIME_STEPS):
    u_velocity, v_velocity, temperature = update_ocean(u_velocity, v_velocity, temperature, wind)
    if t % 10 == 0 or t == TIME_STEPS - 1:
        # save to vtk file
        vtk_filename = f'frame_{outputCount:03d}.vtk'
        save_to_vtk(vtk_filename, u_velocity, v_velocity, temperature, wind)
        outputCount += 1

        print(f"Time Step {t}: Ocean currents updated.")
print(f"Execution time: {time.time() - start:.2f} seconds")

# Plot the velocity field
# plt.figure(figsize=(6, 5))
# plt.quiver(u_velocity[::10, ::10], v_velocity[::10, ::10])
# plt.title("Ocean Current Directions")
# plt.xlabel("X Position")
# plt.ylabel("Y Position")
# plt.show()
#
# # Plot temperature distribution
# plt.figure(figsize=(6, 5))
# plt.imshow(temperature, cmap='coolwarm', origin='lower')
# plt.colorbar(label="Temperature (°C)")
# plt.title("Ocean Temperature Distribution")
# plt.show()

print("Simulation complete.")
