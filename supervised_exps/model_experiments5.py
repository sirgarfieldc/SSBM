# -*- coding: utf-8 -*-
"""SSBM_dev_prob.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HvOMW5VuPMKgVCJPNc9TZ8iG8xDFdXrp
"""

"""
from google.colab import drive
drive.mount('/gdrive')
!ls /gdrive
!cp /gdrive/My\ Drive/SSBM/dev_data_csv.zip dev_data_csv.zip
!unzip -q dev_data_csv.zip

!pip install py-slippi

import os
from getpass import getpass
import urllib

user = input('User name: ')
password = getpass('Password: ')
password = urllib.parse.quote(password) # your password is converted into url format

cmd_string = 'git clone https://{0}:{1}@git.uwaterloo.ca/w2999wen/f2020-cs486-g84.git SSBM'.format(user, password)

os.system(cmd_string)
cmd_string, password = "", "" # removing the password from the variable
del cmd_string
del password

!ls
!mv ./dev_data_csv  ./SSBM/dev_data_csv

# Commented out IPython magic to ensure Python compatibility.
# %cd ./SSBM
!git pull
!git checkout origin/wwen-action-head-train
!git log

# Commented out IPython magic to ensure Python compatibility.
# %cd ./SSBM
"""
from slp_parser import SLPParser
from torch.utils.data import DataLoader
from dataset import SSBMDataset
import dataset
# import importlib; importlib.reload(dataset)
from lstm_model import SSBM_LSTM
from mvp_model import SSBM_MVP
from mvp_model_prob import SSBM_MVP_Prob
from lstm_model_prob import SSBM_LSTM_Prob
from train import train
import torch
import traceback

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

## Sample usage for the SSBM_MVP model and training loop:
# model = SSBM_MVP_Prob(100, 50)
# model = SSBM_LSTM_Prob(action_embedding_dim = 100, button_embedding_dim = 50, hidden_size = 256, num_layers = 3, bidirectional=True, dropout_p=0.2)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Training on device: {device}', flush=True)

trn_ds = SSBMDataset(src_dir="./dev_data_csv/train", char_id=2, opponent_id=1, window_size=60, device='cpu')
val_ds = SSBMDataset(src_dir="./dev_data_csv/valid", char_id=2, opponent_id=1, window_size=60, device='cpu')

trn_dl = DataLoader(trn_ds, batch_size=256, shuffle=True, num_workers=0)
val_dl = DataLoader(val_ds, batch_size=256, shuffle=True, num_workers=0)

import train_prob
# importlib.reload(train_prob)
from action_head import ActionHead
out_hidden_sizes=[
    [256, 128], # buttons
    [512, 256, 128], # stick coarse - NOTE - actually has 129 outputs
    [128, 128], # stick fine
    [128, 128], # stick magn
    [256, 128], # cstick coarse - NOTE - actually has 129 outputs
    [16, 16], # cstick fine
    [128, 128], # cstick magn
    [256, 128], # trigger
]

experiments = [
    [1, False, 0.005],
    [1, False, 0.001],
    [1, False, 0.0005],
    [1, False, 0.0001],
]
for exp in experiments:
    model = SSBM_LSTM_Prob(
        action_embedding_dim = 100, button_embedding_dim = 50, hidden_size = 256,
        num_layers = exp[0], bidirectional=exp[1], dropout_p=0.2,
        out_hidden_sizes=out_hidden_sizes, bn=True
    )
    train_prob.train(model, trn_dl, val_dl, 3, ActionHead.MAX, 2000, True, device, initial_lr=exp[2])

"""# Notes
mvp_fit
"""
"""
!mkdir weights

torch.save(model.state_dict(), "./weights/lstm_action_head_delay_15_2020_11_18.pth")

!git checkout wwen-action-head-train
!git add weights/
!git config --global user.email "w2999wen@uwaterloo.ca"
!git config --global user.name "William Wen"
!git commit -m "add large lstm action head weights"
!git push origin wwen-action-head-train

!git push origin wwen-action-head-train
"""