# Experiment data

## Original

### Memory

Filename: .\volumerender_lx_profile.py

    26     82.8 MiB     82.8 MiB           1   @profile
    27                                         def main():
    28                                             """ Volume Rendering """
    29
    30                                             # Load Datacube
    31     83.6 MiB      0.8 MiB           1       f = h5.File('datacube.hdf5', 'r')
    32    148.0 MiB     64.4 MiB           1       datacube = np.array(f['density'])
    33
    34                                             # Datacube Grid
    35    148.0 MiB      0.0 MiB           1       Nx, Ny, Nz = datacube.shape
    36    148.0 MiB      0.0 MiB           1       x = np.linspace(-Nx / 2, Nx / 2, Nx)
    37    148.0 MiB      0.0 MiB           1       y = np.linspace(-Ny / 2, Ny / 2, Ny)
    38    148.0 MiB      0.0 MiB           1       z = np.linspace(-Nz / 2, Nz / 2, Nz)
    39    148.0 MiB      0.0 MiB           1       points = (x, y, z)
    40
    41                                             # Do Volume Rendering at Different Veiwing Angles
    42    148.0 MiB      0.0 MiB           1       Nangles = 10
    43    629.4 MiB      0.0 MiB          11       for i in range(Nangles):
    44
    45    623.1 MiB      0.0 MiB          10           print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')
    46
    47                                                 # Camera Grid / Query Points -- rotate camera view
    48    623.1 MiB      0.0 MiB          10           angle = np.pi / 2 * i / Nangles
    49    623.1 MiB      0.0 MiB          10           N = 180
    50    623.1 MiB      0.0 MiB          10           c = np.linspace(-N / 2, N / 2, N)
    51    667.5 MiB    534.0 MiB          10           qx, qy, qz = np.meshgrid(c, c, c)
    52    623.1 MiB   -400.5 MiB          10           qxR = qx
    53    623.1 MiB     44.5 MiB          10           qyR = qy * np.cos(angle) - qz * np.sin(angle)
    54    623.1 MiB     44.5 MiB          10           qzR = qy * np.sin(angle) + qz * np.cos(angle)
    55    623.1 MiB    133.5 MiB          10           qi = np.array([qxR.ravel(), qyR.ravel(), qzR.ravel()]).T
    56
    57                                                 # Interpolate onto Camera Grid
    58    667.5 MiB    443.3 MiB          10           camera_grid = interpn(points, datacube, qi, method='linear').reshape((N, N, N))
    59
    60                                                 # Do Volume Rendering
    61    667.5 MiB      2.8 MiB          10           image = np.zeros((camera_grid.shape[1], camera_grid.shape[2], 3))
    62
    63    623.1 MiB   -405.5 MiB        1810           for dataslice in camera_grid:
    64    623.1 MiB    -57.9 MiB        1800               r, g, b, a = transferFunction(np.log(dataslice))
    65    623.1 MiB     -2.2 MiB        1800               image[:, :, 0] = a * r + (1 - a) * image[:, :, 0]
    66    623.1 MiB     -5.1 MiB        1800               image[:, :, 1] = a * g + (1 - a) * image[:, :, 1]
    67    623.1 MiB     -5.1 MiB        1800               image[:, :, 2] = a * b + (1 - a) * image[:, :, 2]
    68
    69    623.1 MiB     -1.0 MiB          10           image = np.clip(image, 0.0, 1.0)
    70
    71                                                 # Plot Volume Rendering
    86
    87                                             # Save figure
    88    636.5 MiB      4.7 MiB           1       plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
    89                                             # plt.show()
    90
    91    636.5 MiB      0.0 MiB           1       return 0

peak performance usage: 667.5 MiB

```
camera_grid = interpn(points, datacube, qi, method='linear').reshape((N, N, N))
```

Other blocks of code that consume a lot of memory：

534.0 MiB

```
qx, qy, qz = np.meshgrid(c, c, c)
```

64.4 MiB

```
datacube = np.array(f['density'])
```

### Time

```
Wrote profile results to volumerender_lx_profile.py.lprof
Timer unit: 1e-06 s

Total time: 20.2865 s
File: volumerender_lx_profile.py
Function: main at line 22

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    22                                           @profile
    23                                           def main():
    24                                               """ Volume Rendering """
    25
    26                                               # Load Datacube
    27         1        441.9    441.9      0.0      f = h5.File('datacube.hdf5', 'r')
    28         1      33459.7  33459.7      0.2      datacube = np.array(f['density'])
    29
    30                                               # Datacube Grid
    31         1          1.9      1.9      0.0      Nx, Ny, Nz = datacube.shape
    32         1         87.8     87.8      0.0      x = np.linspace(-Nx / 2, Nx / 2, Nx)
    33         1         23.3     23.3      0.0      y = np.linspace(-Ny / 2, Ny / 2, Ny)
    34         1         16.5     16.5      0.0      z = np.linspace(-Nz / 2, Nz / 2, Nz)
    35         1          0.4      0.4      0.0      points = (x, y, z)
    36
    37                                               # Do Volume Rendering at Different Veiwing Angles
    38         1          0.2      0.2      0.0      Nangles = 10
    39        11          9.6      0.9      0.0      for i in range(Nangles):
    40
    41        10       2283.7    228.4      0.0          print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')
    42
    43                                                   # Camera Grid / Query Points -- rotate camera view
    44        10         26.2      2.6      0.0          angle = np.pi / 2 * i / Nangles
    45        10          4.2      0.4      0.0          N = 180
    46        10        614.7     61.5      0.0          c = np.linspace(-N / 2, N / 2, N)
    47        10     295608.9  29560.9      1.5          qx, qy, qz = np.meshgrid(c, c, c)
    48        10      14585.8   1458.6      0.1          qxR = qx
    49        10     344515.7  34451.6      1.7          qyR = qy * np.cos(angle) - qz * np.sin(angle)
    50        10     326091.5  32609.2      1.6          qzR = qy * np.sin(angle) + qz * np.cos(angle)
    51        10     265637.8  26563.8      1.3          qi = np.array([qxR.ravel(), qyR.ravel(), qzR.ravel()]).T
    52
    53                                                   # Interpolate onto Camera Grid
    54        10   13814843.6    1e+06     68.1          camera_grid = interpn(points, datacube, qi, method='linear').reshape((N, N, N))
    55
    56                                                   # Do Volume Rendering
    57        10        952.0     95.2      0.0          image = np.zeros((camera_grid.shape[1], camera_grid.shape[2], 3))
    58
    59      1810      16142.1      8.9      0.1          for dataslice in camera_grid:
    60      1800    3378429.2   1876.9     16.7              r, g, b, a = transferFunction(np.log(dataslice))
    61      1800     131744.2     73.2      0.6              image[:, :, 0] = a * r + (1 - a) * image[:, :, 0]
    62      1800     126524.5     70.3      0.6              image[:, :, 1] = a * g + (1 - a) * image[:, :, 1]
    63      1800     124561.6     69.2      0.6              image[:, :, 2] = a * b + (1 - a) * image[:, :, 2]
    64
    65        10       2421.4    242.1      0.0          image = np.clip(image, 0.0, 1.0)
    66
    67                                                   # Plot Volume Rendering
    68        10     430734.8  43073.5      2.1          plt.figure(figsize=(4, 4), dpi=80)
    69
    70        10     233339.6  23334.0      1.2          plt.imshow(image)
    71        10        435.1     43.5      0.0          plt.axis('off')
    72
    73                                                   # Save figure
    74        10     565070.1  56507.0      2.8          plt.savefig('volumerender' + str(i) + '.png', dpi=240, bbox_inches='tight', pad_inches=0)
    75
    76                                               # Plot Simple Projection -- for Comparison
    77         1      35936.8  35936.8      0.2      plt.figure(figsize=(4, 4), dpi=80)
    78
    79         1      25585.1  25585.1      0.1      plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
    80         1         54.5     54.5      0.0      plt.clim(-5, 5)
    81         1         41.9     41.9      0.0      plt.axis('off')
    82
    83                                               # Save figure
    84         1     116241.9 116241.9      0.6      plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
    85                                               # plt.show()
    86
    87         1          0.4      0.4      0.0      return 0

```

Time consuming blocks:

```
54        10   13814843.6    1e+06     68.1          camera_grid = interpn(points, datacube, qi, method='linear').reshape((N, N, N))
```

```
60      1800    3378429.2   1876.9     16.7              r, g, b, a = transferFunction(np.log(dataslice))
```

```
47        10     295608.9  29560.9      1.5          qx, qy, qz = np.meshgrid(c, c, c)
```

```
49        10     344515.7  34451.6      1.7          qyR = qy * np.cos(angle) - qz * np.sin(angle)
50        10     326091.5  32609.2      1.6          qzR = qy * np.sin(angle) + qz * np.cos(angle)
```



## python optimization——transfer function+for loop extract meshgrid+np.log

```python
import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from scipy.interpolate import interpn
import timeit
# from memory_profiler import profile

"""
Create Your Own Volume Rendering (With Python)
Philip Mocz (2020) Princeton Univeristy, @PMocz

Simulate the Schrodinger-Poisson system with the Spectral method
"""


def transferFunction(x):
    exp1 = np.exp(-(x - 9.0) ** 2 / 1.0)
    exp2 = np.exp(-(x - 3.0) ** 2 / 0.1)
    exp3 = np.exp(-(x + 3.0) ** 2 / 0.5)

    r = 1.0 * exp1 + 0.1 * exp2 + 0.1 * exp3
    g = 1.0 * exp1 + 1.0 * exp2 + 0.1 * exp3
    b = 0.1 * exp1 + 0.1 * exp2 + 1.0 * exp3
    a = 0.6 * exp1 + 0.1 * exp2 + 0.01 * exp3

    return r, g, b, a

# @profile
def main():
    """ Volume Rendering """

    # Load Datacube
    f = h5.File('datacube.hdf5', 'r')
    datacube = np.array(f['density'])

    # Datacube Grid
    Nx, Ny, Nz = datacube.shape
    x = np.linspace(-Nx / 2, Nx / 2, Nx)
    y = np.linspace(-Ny / 2, Ny / 2, Ny)
    z = np.linspace(-Nz / 2, Nz / 2, Nz)
    points = (x, y, z)

    # Do Volume Rendering at Different Veiwing Angles
    Nangles = 10
    angle_unit = np.pi / 2 / Nangles
    N = 180
    c = np.linspace(-N / 2, N / 2, N)
    qx, qy, qz = np.meshgrid(c, c, c)
    cos_angles = np.cos(angle_unit * np.arange(Nangles))
    sin_angles = np.sin(angle_unit * np.arange(Nangles))

    for i in range(Nangles):
        print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')

        # Camera Grid / Query Points -- rotate camera view
        cos_angle = cos_angles[i]
        sin_angle = sin_angles[i]
        # qxR = qx
        qyR = qy * cos_angle - qz * sin_angle
        qzR = qy * sin_angle + qz * cos_angle
        # qi = np.array([qx.ravel(), qyR.ravel(), qzR.ravel()]).T

        # Interpolate onto Camera Grid
        camera_grid_log = np.log(interpn(points, datacube, np.array([qx.ravel(), qyR.ravel(), qzR.ravel()]).T,
                                         method='linear')).reshape((N, N, N))

        # Do Volume Rendering
        r_channel = np.zeros((N, N))
        g_channel = np.zeros((N, N))
        b_channel = np.zeros((N, N))
        for dataslice_log in camera_grid_log:
            r, g, b, a = transferFunction(dataslice_log)
            r_channel = a * r + (1 - a) * r_channel
            g_channel = a * g + (1 - a) * g_channel
            b_channel = a * b + (1 - a) * b_channel

        image = np.stack((r_channel, g_channel, b_channel), axis=-1)
        image = np.clip(image, 0.0, 1.0)

        # Plot Volume Rendering
        plt.figure(figsize=(4, 4), dpi=80)

        plt.imshow(image)
        plt.axis('off')

        # Save figure
        plt.savefig('volumerender' + str(i) + '.png', dpi=240, bbox_inches='tight', pad_inches=0)

    # Plot Simple Projection -- for Comparison
    plt.figure(figsize=(4, 4), dpi=80)

    plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
    plt.clim(-5, 5)
    plt.axis('off')

    # Save figure
    plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
    # plt.show()

    return 0


if __name__ == "__main__":
    main()


```

### Memory

```

Filename: .\volumerender_python.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    28     82.8 MiB     82.8 MiB           1   @profile
    29                                         def main():
    30                                             """ Volume Rendering """
    31
    32                                             # Load Datacube
    33     83.5 MiB      0.8 MiB           1       f = h5.File('datacube.hdf5', 'r')
    34    148.0 MiB     64.4 MiB           1       datacube = np.array(f['density'])
    35
    36                                             # Datacube Grid
    37    148.0 MiB      0.0 MiB           1       Nx, Ny, Nz = datacube.shape
    38    148.0 MiB      0.0 MiB           1       x = np.linspace(-Nx / 2, Nx / 2, Nx)
    39    148.0 MiB      0.0 MiB           1       y = np.linspace(-Ny / 2, Ny / 2, Ny)
    40    148.0 MiB      0.0 MiB           1       z = np.linspace(-Nz / 2, Nz / 2, Nz)
    41    148.0 MiB      0.0 MiB           1       points = (x, y, z)
    42
    43                                             # Do Volume Rendering at Different Veiwing Angles
    44    148.0 MiB      0.0 MiB           1       Nangles = 10
    45    148.0 MiB      0.0 MiB           1       angle_unit = np.pi / 2 / Nangles
    46    148.0 MiB      0.0 MiB           1       N = 180
    47    148.0 MiB      0.0 MiB           1       c = np.linspace(-N / 2, N / 2, N)
    48    281.5 MiB    133.5 MiB           1       qx, qy, qz = np.meshgrid(c, c, c)
    49    281.5 MiB      0.0 MiB           1       cos_angles = np.cos(angle_unit * np.arange(Nangles))
    50    281.5 MiB      0.0 MiB           1       sin_angles = np.sin(angle_unit * np.arange(Nangles))
    51
    52    499.5 MiB      0.0 MiB          11       for i in range(Nangles):
    53    492.5 MiB      0.0 MiB          10           print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')
    54
    55                                                 # Camera Grid / Query Points -- rotate camera view
    56    492.5 MiB      0.0 MiB          10           cos_angle = cos_angles[i]
    57    492.5 MiB      0.0 MiB          10           sin_angle = sin_angles[i]
    58                                                 # qxR = qx
    59    492.5 MiB     44.5 MiB          10           qyR = qy * cos_angle - qz * sin_angle
    60    492.5 MiB     44.5 MiB          10           qzR = qy * sin_angle + qz * cos_angle
    61                                                 # qi = np.array([qx.ravel(), qyR.ravel(), qzR.ravel()]).T
    62
    63                                                 # Interpolate onto Camera Grid
    64    626.0 MiB   -444.2 MiB          30           camera_grid_log = np.log(interpn(points, datacube, np.array([qx.ravel(), qyR.ravel(), qzR.ravel()]).T,
    65    626.0 MiB   -889.5 MiB          20                                            method='linear')).reshape((N, N, N))
    66
    67                                                 # Do Volume Rendering
    68    537.0 MiB   -889.1 MiB          10           r_channel = np.zeros((N, N))
    69    537.0 MiB      0.4 MiB          10           g_channel = np.zeros((N, N))
    70    537.0 MiB      0.2 MiB          10           b_channel = np.zeros((N, N))
    71    492.5 MiB   -922.2 MiB        1810           for dataslice_log in camera_grid_log:
    72    492.5 MiB   -550.7 MiB        1800               r, g, b, a = transferFunction(dataslice_log)
    73    492.5 MiB   -256.7 MiB        1800               r_channel = a * r + (1 - a) * r_channel
    74    492.5 MiB   -332.9 MiB        1800               g_channel = a * g + (1 - a) * g_channel
    75    492.5 MiB   -487.3 MiB        1800               b_channel = a * b + (1 - a) * b_channel
    76
    77    492.5 MiB     -1.4 MiB          10           image = np.stack((r_channel, g_channel, b_channel), axis=-1)
    78    492.5 MiB      0.5 MiB          10           image = np.clip(image, 0.0, 1.0)
    79
    80                                                 # Plot Volume Rendering
    81    494.4 MiB     26.0 MiB          10           plt.figure(figsize=(4, 4), dpi=80)
    82
    83    495.4 MiB     12.3 MiB          10           plt.imshow(image)
    84    495.4 MiB      0.0 MiB          10           plt.axis('off')
    85
    86                                                 # Save figure
    87    499.5 MiB     35.2 MiB          10           plt.savefig('volumerender' + str(i) + '.png', dpi=240, bbox_inches='tight', pad_inches=0)
    88
    89                                             # Plot Simple Projection -- for Comparison
    90    500.8 MiB      1.3 MiB           1       plt.figure(figsize=(4, 4), dpi=80)
    91
    92    501.9 MiB      1.0 MiB           1       plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
    93    501.9 MiB      0.0 MiB           1       plt.clim(-5, 5)
    94    501.9 MiB      0.0 MiB           1       plt.axis('off')
    95
    96                                             # Save figure
    97    506.6 MiB      4.7 MiB           1       plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
    98                                             # plt.show()
    99
   100    506.6 MiB      0.0 MiB           1       return 0

```

### Time

```python
Wrote profile results to volumerender_python.py.lprof
Timer unit: 1e-06 s

Total time: 18.5187 s
File: volumerender_python.py
Function: main at line 28

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    28                                           @profile
    29                                           def main():
    30                                               """ Volume Rendering """
    31
    32                                               # Load Datacube
    33         1        474.5    474.5      0.0      f = h5.File('datacube.hdf5', 'r')
    34         1      34298.8  34298.8      0.2      datacube = np.array(f['density'])
    35
    36                                               # Datacube Grid
    37         1          2.1      2.1      0.0      Nx, Ny, Nz = datacube.shape
    38         1         86.4     86.4      0.0      x = np.linspace(-Nx / 2, Nx / 2, Nx)
    39         1         24.6     24.6      0.0      y = np.linspace(-Ny / 2, Ny / 2, Ny)
    40         1         24.7     24.7      0.0      z = np.linspace(-Nz / 2, Nz / 2, Nz)
    41         1          0.4      0.4      0.0      points = (x, y, z)
    42
    43                                               # Do Volume Rendering at Different Veiwing Angles
    44         1          0.3      0.3      0.0      Nangles = 10
    45         1          1.0      1.0      0.0      angle_unit = np.pi / 2 / Nangles
    46         1          0.3      0.3      0.0      N = 180
    47         1         17.9     17.9      0.0      c = np.linspace(-N / 2, N / 2, N)
    48         1      24677.3  24677.3      0.1      qx, qy, qz = np.meshgrid(c, c, c)
    49         1         31.1     31.1      0.0      cos_angles = np.cos(angle_unit * np.arange(Nangles))
    50         1          4.9      4.9      0.0      sin_angles = np.sin(angle_unit * np.arange(Nangles))
    51
    52        11         17.0      1.5      0.0      for i in range(Nangles):
    53        10       2230.4    223.0      0.0          print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')
    54
    55                                                   # Camera Grid / Query Points -- rotate camera view
    56        10         23.3      2.3      0.0          cos_angle = cos_angles[i]
    57        10          6.1      0.6      0.0          sin_angle = sin_angles[i]
    58                                                   # qxR = qx
    59        10     347384.6  34738.5      1.9          qyR = qy * cos_angle - qz * sin_angle
    60        10     349714.3  34971.4      1.9          qzR = qy * sin_angle + qz * cos_angle
    61                                                   # qi = np.array([qx.ravel(), qyR.ravel(), qzR.ravel()]).T
    62
    63                                                   # Interpolate onto Camera Grid
    64        30   14631429.7 487714.3     79.0          camera_grid_log = np.log(interpn(points, datacube, np.array([qx.ravel(), qyR.ravel(), qzR.ravel()]).T,
    65        20         20.1      1.0      0.0                                           method='linear')).reshape((N, N, N))
    66
    67                                                   # Do Volume Rendering
    68        10        342.4     34.2      0.0          r_channel = np.zeros((N, N))
    69        10        226.4     22.6      0.0          g_channel = np.zeros((N, N))
    70        10        204.3     20.4      0.0          b_channel = np.zeros((N, N))
    71      1810      18661.2     10.3      0.1          for dataslice_log in camera_grid_log:
    72      1800    1316306.3    731.3      7.1              r, g, b, a = transferFunction(dataslice_log)
    73      1800     125242.5     69.6      0.7              r_channel = a * r + (1 - a) * r_channel
    74      1800      92121.2     51.2      0.5              g_channel = a * g + (1 - a) * g_channel
    75      1800      84600.0     47.0      0.5              b_channel = a * b + (1 - a) * b_channel
    76
    77        10       1528.8    152.9      0.0          image = np.stack((r_channel, g_channel, b_channel), axis=-1)
    78        10       1734.1    173.4      0.0          image = np.clip(image, 0.0, 1.0)
    79
    80                                                   # Plot Volume Rendering
    81        10     449177.6  44917.8      2.4          plt.figure(figsize=(4, 4), dpi=80)
    82
    83        10     253099.1  25309.9      1.4          plt.imshow(image)
    84        10        447.3     44.7      0.0          plt.axis('off')
    85
    86                                                   # Save figure
    87        10     602470.0  60247.0      3.3          plt.savefig('volumerender' + str(i) + '.png', dpi=240, bbox_inches='tight', pad_inches=0)
    88
    89                                               # Plot Simple Projection -- for Comparison
    90         1      36958.6  36958.6      0.2      plt.figure(figsize=(4, 4), dpi=80)
    91
    92         1      25416.5  25416.5      0.1      plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
    93         1         56.7     56.7      0.0      plt.clim(-5, 5)
    94         1         45.5     45.5      0.0      plt.axis('off')
    95
    96                                               # Save figure
    97         1     119596.7 119596.7      0.6      plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
    98                                               # plt.show()
    99
   100         1          0.4      0.4      0.0      return 0

```

## Numba

```python
import numpy as np
import matplotlib.pyplot as plt
import h5py as h5
from scipy.interpolate import interpn
import timeit
# from memory_profiler import profile
from numba import jit, njit, vectorize, float64, guvectorize

"""
Create Your Own Volume Rendering (With Python)
Philip Mocz (2020) Princeton Univeristy, @PMocz

Simulate the Schrodinger-Poisson system with the Spectral method
"""

# @guvectorize(['(float64[:,:], float64[:,:], float64[:,:], float64[:,:], float64[:,:])'], '(n,n)->(n,n), (n,n), (n,n), (n,n)',
#               target='parallel', fastmath=True)
# def transferFunction(x, r, g, b, a):
#     exp1 = np.exp(-(x - 9.0) ** 2 / 1.0)
#     exp2 = np.exp(-(x - 3.0) ** 2 / 0.1)
#     exp3 = np.exp(-(x + 3.0) ** 2 / 0.5)
#
#     r[:, :] = 1.0 * exp1 + 0.1 * exp2 + 0.1 * exp3
#     g[:, :] = 1.0 * exp1 + 1.0 * exp2 + 0.1 * exp3
#     b[:, :] = 0.1 * exp1 + 0.1 * exp2 + 1.0 * exp3
#     a[:, :] = 0.6 * exp1 + 0.1 * exp2 + 0.01 * exp3
# using @njit here is not efficient
# # @njit(fastmath=True)
def transferFunction(x):
    exp1 = np.exp(-(x - 9.0) ** 2 / 1.0)
    exp2 = np.exp(-(x - 3.0) ** 2 / 0.1)
    exp3 = np.exp(-(x + 3.0) ** 2 / 0.5)

    r = 1.0 * exp1 + 0.1 * exp2 + 0.1 * exp3
    g = 1.0 * exp1 + 1.0 * exp2 + 0.1 * exp3
    b = 0.1 * exp1 + 0.1 * exp2 + 1.0 * exp3
    a = 0.6 * exp1 + 0.1 * exp2 + 0.01 * exp3

    return r, g, b, a


@vectorize(['float64(float64, float64, float64, float64)'], fastmath=True, target='parallel')
def rotate_qy(qy, qz, cos_angle, sin_angle):
    qyR = qy * cos_angle - qz * sin_angle
    return qyR

@vectorize(['float64(float64, float64, float64, float64)'], fastmath=True, target='parallel')
def rotate_qz(qy, qz, cos_angle, sin_angle):
    qzR = qy * sin_angle + qz * cos_angle
    return qzR


@profile
def main():
    """ Volume Rendering """

    # Load Datacube
    f = h5.File('datacube.hdf5', 'r')
    datacube = np.array(f['density'])

    # Datacube Grid
    Nx, Ny, Nz = datacube.shape
    x = np.linspace(-Nx / 2, Nx / 2, Nx)
    y = np.linspace(-Ny / 2, Ny / 2, Ny)
    z = np.linspace(-Nz / 2, Nz / 2, Nz)
    points = (x, y, z)

    # Do Volume Rendering at Different Veiwing Angles
    Nangles = 10
    angle_unit = np.pi / 2 / Nangles
    N = 180
    c = np.linspace(-N / 2, N / 2, N)
    qx, qy, qz = np.meshgrid(c, c, c)
    cos_angles = np.cos(angle_unit * np.arange(Nangles))
    sin_angles = np.sin(angle_unit * np.arange(Nangles))

    for i in range(Nangles):
        print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')

        # Camera Grid / Query Points -- rotate camera view
        cos_angle = cos_angles[i]
        sin_angle = sin_angles[i]
        # qxR = qx
        # qyR = qy * cos_angle - qz * sin_angle
        # qzR = qy * sin_angle + qz * cos_angle
        qyR = rotate_qy(qy, qz, cos_angle, sin_angle)
        qzR = rotate_qz(qy, qz, cos_angle, sin_angle)
        # qyR, qzR = rotate(qy, qz, cos_angle, sin_angle)

        # Interpolate onto Camera Grid
        camera_grid_log = np.log(interpn(points, datacube, np.array([qx.ravel(), qyR.ravel(), qzR.ravel()]).T, method='linear')).reshape((N, N, N))

        # Do Volume Rendering
        r_channel = np.zeros((N, N))
        g_channel = np.zeros((N, N))
        b_channel = np.zeros((N, N))
        for dataslice_log in camera_grid_log:
            r, g, b, a = transferFunction(dataslice_log)
            r_channel = a * r + (1 - a) * r_channel
            g_channel = a * g + (1 - a) * g_channel
            b_channel = a * b + (1 - a) * b_channel

        image = np.stack((r_channel, g_channel, b_channel), axis=-1)
        image = np.clip(image, 0.0, 1.0)

        # Plot Volume Rendering
        plt.figure(figsize=(4, 4), dpi=80)

        plt.imshow(image)
        plt.axis('off')

        # Save figure
        plt.savefig('volumerender' + str(i) + '.png', dpi=240, bbox_inches='tight', pad_inches=0)

    # Plot Simple Projection -- for Comparison
    plt.figure(figsize=(4, 4), dpi=80)

    plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
    plt.clim(-5, 5)
    plt.axis('off')

    # Save figure
    plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
    # plt.show()

    return 0


if __name__ == "__main__":
    main()

```

### Memory

```python

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    56    133.0 MiB    133.0 MiB           1   @profile
    57                                         def main():
    58                                             """ Volume Rendering """
    59
    60                                             # Load Datacube
    61    133.6 MiB      0.6 MiB           1       f = h5.File('datacube.hdf5', 'r')
    62    198.0 MiB     64.4 MiB           1       datacube = np.array(f['density'])
    63
    64                                             # Datacube Grid
    65    198.0 MiB      0.0 MiB           1       Nx, Ny, Nz = datacube.shape
    66    198.0 MiB      0.0 MiB           1       x = np.linspace(-Nx / 2, Nx / 2, Nx)
    67    198.0 MiB      0.0 MiB           1       y = np.linspace(-Ny / 2, Ny / 2, Ny)
    68    198.0 MiB      0.0 MiB           1       z = np.linspace(-Nz / 2, Nz / 2, Nz)
    69    198.0 MiB      0.0 MiB           1       points = (x, y, z)
    70
    71                                             # Do Volume Rendering at Different Veiwing Angles
    72    198.0 MiB      0.0 MiB           1       Nangles = 10
    73    198.0 MiB      0.0 MiB           1       angle_unit = np.pi / 2 / Nangles
    74    198.0 MiB      0.0 MiB           1       N = 180
    75    198.0 MiB      0.0 MiB           1       c = np.linspace(-N / 2, N / 2, N)
    76    331.6 MiB    133.5 MiB           1       qx, qy, qz = np.meshgrid(c, c, c)
    77    331.6 MiB      0.0 MiB           1       cos_angles = np.cos(angle_unit * np.arange(Nangles))
    78    331.6 MiB      0.0 MiB           1       sin_angles = np.sin(angle_unit * np.arange(Nangles))
    79
    80    544.5 MiB      0.0 MiB          11       for i in range(Nangles):
    81    538.0 MiB      0.0 MiB          10           print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')
    82
    83                                                 # Camera Grid / Query Points -- rotate camera view
    84    538.0 MiB      0.0 MiB          10           cos_angle = cos_angles[i]
    85    538.0 MiB      0.0 MiB          10           sin_angle = sin_angles[i]
    86                                                 # qxR = qx
    87                                                 # qyR = qy * cos_angle - qz * sin_angle
    88                                                 # qzR = qy * sin_angle + qz * cos_angle
    89    538.0 MiB     44.9 MiB          10           qyR = rotate_qy(qy, qz, cos_angle, sin_angle)
    90    538.0 MiB     44.5 MiB          10           qzR = rotate_qz(qy, qz, cos_angle, sin_angle)
    91                                                 # qyR, qzR = rotate(qy, qz, cos_angle, sin_angle)
    92
    93                                                 # Interpolate onto Camera Grid
    94    671.5 MiB   -444.7 MiB          30           camera_grid_log = np.log(interpn(points, datacube, np.array([qx.ravel(), qyR.ravel(), qzR.ravel()]).T,
    95    671.5 MiB   -889.8 MiB          20                                            method='linear')).reshape((N, N, N))
    96
    97                                                 # Do Volume Rendering
    98    582.5 MiB   -889.7 MiB          10           r_channel = np.zeros((N, N))
    99    582.5 MiB      0.2 MiB          10           g_channel = np.zeros((N, N))
   100    582.5 MiB      0.0 MiB          10           b_channel = np.zeros((N, N))
   101    538.0 MiB   -677.7 MiB        1810           for dataslice_log in camera_grid_log:
   102    538.0 MiB   -180.4 MiB        1800               r, g, b, a = transferFunction(dataslice_log)
   103    538.0 MiB   -250.9 MiB        1800               r_channel = a * r + (1 - a) * r_channel
   104    538.0 MiB   -282.4 MiB        1800               g_channel = a * g + (1 - a) * g_channel
   105    538.0 MiB   -351.8 MiB        1800               b_channel = a * b + (1 - a) * b_channel
   106
   107    538.0 MiB     -1.4 MiB          10           image = np.stack((r_channel, g_channel, b_channel), axis=-1)
   108    538.0 MiB      0.7 MiB          10           image = np.clip(image, 0.0, 1.0)
   109
   110                                                 # Plot Volume Rendering
   111    539.1 MiB     22.6 MiB          10           plt.figure(figsize=(4, 4), dpi=80)
   112
   113    540.3 MiB     11.0 MiB          10           plt.imshow(image)
   114    540.3 MiB      0.0 MiB          10           plt.axis('off')
   115
   116                                                 # Save figure
   117    544.5 MiB     40.6 MiB          10           plt.savefig('volumerender' + str(i) + '.png', dpi=240, bbox_inches='tight', pad_inches=0)
   118
   119                                             # Plot Simple Projection -- for Comparison
   120    545.4 MiB      0.9 MiB           1       plt.figure(figsize=(4, 4), dpi=80)
   121
   122    546.3 MiB      0.9 MiB           1       plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
   123    546.3 MiB      0.0 MiB           1       plt.clim(-5, 5)
   124    546.3 MiB      0.0 MiB           1       plt.axis('off')
   125
   126                                             # Save figure
   127    551.3 MiB      4.9 MiB           1       plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
   128                                             # plt.show()
   129
   130    551.3 MiB      0.0 MiB           1       return 0

```

### Time

```python
Total time: 17.8501 s
File: .\volumerender_numba.py
Function: main at line 53

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    53                                           @profile
    54                                           def main():
    55                                               """ Volume Rendering """
    56
    57                                               # Load Datacube
    58         1        479.0    479.0      0.0      f = h5.File('datacube.hdf5', 'r')
    59         1      31761.2  31761.2      0.2      datacube = np.array(f['density'])
    60
    61                                               # Datacube Grid
    62         1          1.5      1.5      0.0      Nx, Ny, Nz = datacube.shape
    63         1         86.5     86.5      0.0      x = np.linspace(-Nx / 2, Nx / 2, Nx)
    64         1         21.0     21.0      0.0      y = np.linspace(-Ny / 2, Ny / 2, Ny)
    65         1         16.8     16.8      0.0      z = np.linspace(-Nz / 2, Nz / 2, Nz)
    66         1          0.5      0.5      0.0      points = (x, y, z)
    67
    68                                               # Do Volume Rendering at Different Veiwing Angles
    69         1          0.2      0.2      0.0      Nangles = 10
    70         1          1.1      1.1      0.0      angle_unit = np.pi / 2 / Nangles
    71         1          0.3      0.3      0.0      N = 180
    72         1         16.7     16.7      0.0      c = np.linspace(-N / 2, N / 2, N)
    73         1      24872.0  24872.0      0.1      qx, qy, qz = np.meshgrid(c, c, c)
    74         1         23.4     23.4      0.0      cos_angles = np.cos(angle_unit * np.arange(Nangles))
    75         1          3.9      3.9      0.0      sin_angles = np.sin(angle_unit * np.arange(Nangles))
    76
    77        11          8.8      0.8      0.0      for i in range(Nangles):
    78        10       1697.0    169.7      0.0          print('Rendering Scene ' + str(i + 1) + ' of ' + str(Nangles) + '.\n')
    79
    80                                                   # Camera Grid / Query Points -- rotate camera view
    81        10         21.4      2.1      0.0          cos_angle = cos_angles[i]
    82        10          5.1      0.5      0.0          sin_angle = sin_angles[i]
    83                                                   # qxR = qx
    84                                                   # qyR = qy * cos_angle - qz * sin_angle
    85                                                   # qzR = qy * sin_angle + qz * cos_angle
    86        10     104454.3  10445.4      0.6          qyR = rotate_qy(qy, qz, cos_angle, sin_angle)
    87        10      75544.7   7554.5      0.4          qzR = rotate_qz(qy, qz, cos_angle, sin_angle)
    88                                                   # qyR, qzR = rotate(qy, qz, cos_angle, sin_angle)
    89
    90                                                   # Interpolate onto Camera Grid
    91        30   14744452.5 491481.8     82.6          camera_grid_log = np.log(interpn(points, datacube, np.array([qx.ravel(), qyR.ravel(), qzR.ravel()]).T,
    92        20         22.1      1.1      0.0                                           method='linear')).reshape((N, N, N))
    93
    94                                                   # Do Volume Rendering
    95        10        350.1     35.0      0.0          r_channel = np.zeros((N, N))
    96        10        197.8     19.8      0.0          g_channel = np.zeros((N, N))
    97        10        194.7     19.5      0.0          b_channel = np.zeros((N, N))
    98      1810      16829.7      9.3      0.1          for dataslice_log in camera_grid_log:
    99      1800    1165503.2    647.5      6.5              r, g, b, a = transferFunction(dataslice_log)
   100      1800      92257.7     51.3      0.5              r_channel = a * r + (1 - a) * r_channel
   101      1800      75748.2     42.1      0.4              g_channel = a * g + (1 - a) * g_channel
   102      1800      75187.1     41.8      0.4              b_channel = a * b + (1 - a) * b_channel
   103
   104        10       1347.1    134.7      0.0          image = np.stack((r_channel, g_channel, b_channel), axis=-1)
   105        10       1688.3    168.8      0.0          image = np.clip(image, 0.0, 1.0)
   106
   107                                                   # Plot Volume Rendering
   108        10     465704.4  46570.4      2.6          plt.figure(figsize=(4, 4), dpi=80)
   109
   110        10     225602.9  22560.3      1.3          plt.imshow(image)
   111        10        447.3     44.7      0.0          plt.axis('off')
   112
   113                                                   # Save figure
   114        10     564186.6  56418.7      3.2          plt.savefig('volumerender' + str(i) + '.png', dpi=240, bbox_inches='tight', pad_inches=0)
   115
   116                                               # Plot Simple Projection -- for Comparison
   117         1      38520.6  38520.6      0.2      plt.figure(figsize=(4, 4), dpi=80)
   118
   119         1      24967.4  24967.4      0.1      plt.imshow(np.log(np.mean(datacube, 0)), cmap='viridis')
   120         1         55.6     55.6      0.0      plt.clim(-5, 5)
   121         1         46.1     46.1      0.0      plt.axis('off')
   122
   123                                               # Save figure
   124         1     117791.4 117791.4      0.7      plt.savefig('projection.png', dpi=240, bbox_inches='tight', pad_inches=0)
   125                                               # plt.show()
   126
   127         1          0.6      0.6      0.0      return 0

```



## Multiprocessing

run 10 times

async: Time:  60.3124525

sync (blocking): Time:  60.4812567

### Memory

```python
Filename: .\volumerender_mp.py

Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    77     83.2 MiB     83.2 MiB           1   @profile
    78                                         def main():
    79                                             """ Volume Rendering """
    80
    81                                             # Load Datacube
    82     84.0 MiB      0.8 MiB           1       f = h5.File('datacube.hdf5', 'r')
    83    148.4 MiB     64.4 MiB           1       datacube = np.array(f['density'])
    84
    85                                             # Datacube Grid
    86    148.4 MiB      0.0 MiB           1       Nx, Ny, Nz = datacube.shape
    87    148.4 MiB      0.0 MiB           1       x = np.linspace(-Nx / 2, Nx / 2, Nx)
    88    148.4 MiB      0.0 MiB           1       y = np.linspace(-Ny / 2, Ny / 2, Ny)
    89    148.4 MiB      0.0 MiB           1       z = np.linspace(-Nz / 2, Nz / 2, Nz)
    90    148.4 MiB      0.0 MiB           1       points = (x, y, z)
    91
    92                                             # Do Volume Rendering at Different Veiwing Angles
    93    148.4 MiB      0.0 MiB           1       Nangles = 10
    94    148.4 MiB      0.0 MiB           1       num_process = 10
    95    149.1 MiB      0.7 MiB           1       with multiprocessing.Pool(processes=num_process) as pool:
    96    149.1 MiB      0.0 MiB          13           pool.starmap_async(render, [(i, points, datacube, Nangles) for i in range(Nangles)])
    97    149.1 MiB      0.0 MiB           1           pool.apply_async(simple_projection, args=(datacube,))
    98    149.1 MiB      0.0 MiB           1           pool.close()
    99    149.1 MiB     -0.0 MiB           1           pool.join()
   100    149.1 MiB      0.0 MiB           1       return 0


Wrote profile results to volumerender_mp.py.lprof
Timer unit: 1e-06 s
```

### Time

The actual data seems to deviate significantly. It appears that `line_profiler` doesn't wait for the process to complete before being joined.

