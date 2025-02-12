import h5py
import numpy as np

filename = "newgrid_results.hdf5"

def list_datasets():
    with h5py.File(filename, "r") as f:
        print("Datasets in the file:")

        def print_structure(name, obj):
            if isinstance(obj, h5py.Dataset):
                print(f"📂 {name} - shape: {obj.shape}, dtype: {obj.dtype}")

        f.visititems(print_structure)


def read_dataset(grid_size):
    with h5py.File(filename, "r") as f:
        dataset_name = f"{grid_size}x{grid_size}/newgrid"
        if dataset_name in f:
            dataset = f[dataset_name]
            data = dataset[:]
            print(f"Loaded {dataset.attrs.get('description', 'No description')}")
            print("Data shape:", data.shape)
            np.set_printoptions(threshold=np.inf)
            print("Data:\n", data)
        else:
            print(f"Dataset {dataset_name} not found!")


if __name__ == "__main__":
    list_datasets()

    # You can adjust this to any desired size for display
    # Modify this to customize the viewing size
    grid_size = 100
    read_dataset(grid_size)
