import glob
import numpy as np
from torch.utils.data import DataLoader
from constants import DATA_PATH
from dataset.colorization_dataset import ColorizationDataset

def make_dataloaders(batch_size=16, n_workers=4, pin_memory=True, **kwargs): # A handy function to make our dataloaders
    dataset = ColorizationDataset(**kwargs)
    dataloader = DataLoader(dataset, batch_size=batch_size, num_workers=n_workers,
                            pin_memory=pin_memory)
    return dataloader

def create_dataset():
    paths_subset = np.array(glob.glob(DATA_PATH + "/*.jpg"))
    rand_idxs = np.random.permutation(len(paths_subset))
    train_idxs = rand_idxs[:8000]  # choosing the first 8000 as training set
    val_idxs = rand_idxs[8000:]  # choosing last 2000 as validation set
    train_paths = paths_subset[train_idxs]
    val_paths = paths_subset[val_idxs]
    train_dl = make_dataloaders(paths=train_paths, split='train')
    val_dl = make_dataloaders(paths=val_paths, split='val')

    data = next(iter(train_dl))
    Ls, abs_ = data['L'], data['ab']
    print(Ls.shape, abs_.shape)
    print(len(train_dl), len(val_dl))
    return train_dl, val_dl

if __name__ == '__main__':
    create_dataset()