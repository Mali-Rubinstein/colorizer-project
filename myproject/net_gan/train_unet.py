from torchvision.models import resnet18
import torch
import tqdm
from torch import nn, optim
from utility_functions import AverageMeter
from dataset.dataset import create_dataset
from constants import NET_GAN_PATH
from torchvision.models import resnet18, ResNet18_Weights
from fastai.vision.all import create_body, DynamicUnet  # אם אתה משתמש ב-fastai

weights = ResNet18_Weights.DEFAULT

model_instance = resnet18(weights=weights)

def build_res_unet(n_input=1, n_output=2, size=256):
    body = create_body(resnet18(weights=weights), n_in=n_input, cut=-2)
    net_G = DynamicUnet(body, n_output, (size, size))
    return net_G

def pretrain_generator(net_G, train_dl, opt, criterion, epochs):
    for e in range(epochs):
        loss_meter = AverageMeter()
        for data in tqdm.tqdm(train_dl):
            L, ab = data['L'], data['ab']
            preds = net_G(L)
            loss = criterion(preds, ab)
            opt.zero_grad()
            loss.backward()
            opt.step()

            loss_meter.update(loss.item(), L.size(0))

        print(f"Epoch {e + 1}/{epochs}")
        print(f"L1 Loss: {loss_meter.avg:.5f}")

def create_net_gan():
    train_dl, _ = create_dataset()
    net_G = build_res_unet(n_input=1, n_output=2, size=256)
    opt = optim.Adam(net_G.parameters(), lr=1e-4)
    criterion = nn.L1Loss()
    pretrain_generator(net_G, train_dl, opt, criterion, 20)
    torch.save(net_G.state_dict(), NET_GAN_PATH)


if __name__ == '__main__':
    create_net_gan()