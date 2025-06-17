import torch
from tqdm import tqdm
from model.model import MainModel

from dataset.dataset import create_dataset
from utility_functions import create_loss_meters, update_losses
from constants import MODEL_PATH
def train_model(model, train_dl, epochs, display_every=200):
    for e in range(epochs):
        loss_meter_dict = create_loss_meters()  # function returing a dictionary of objects to
        i = 0  # log the losses of the complete network
        for data in tqdm(train_dl):
            model.setup_input(data)
            model.optimize()
            update_losses(model, loss_meter_dict, count=data['L'].size(0))  # function updating the log objects
            i += 1
            if i % display_every == 0:
                print(f"\nEpoch {e + 1}/{epochs}")
                print(f"Iteration {i}/{len(train_dl)}")


def create_model():
    train_dl, _ = create_dataset()
    model = MainModel()
    train_model(model, train_dl, 200)
    torch.save(model.state_dict(), MODEL_PATH)

if __name__ == '__main__':
    create_model()
