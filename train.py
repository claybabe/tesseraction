#!/usr/bin/env python3

#tesseraction net
#copyright - clayton thomas baber 2019


import torch
import torch.nn as nn
import time
import datetime
import random
import numpy as np
from torch.utils.data import Dataset, DataLoader

#use cuda if available, otherwise use cpu
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# Defining input size, output size respectively
n_in, n_out = 177, 148

class TrainingData(Dataset):
    def __init__(self):
        xy = np.loadtxt("data/trainingdata.csv", delimiter=",", dtype=np.int32)
        self.len = xy.shape[0]
        self.x_data = torch.tensor(xy[:,:n_in], device=device, dtype=torch.float)
        self.y_data = torch.tensor(xy[:,-n_out:], device=device, dtype=torch.float)
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]
    def __len__(self):
        return self.len
#----------------------------------------------------------------------------------

#this will generate and return a dictionary containing a model, dataloader, loss function, and optimizer
#also contains a results list where we can store validation results
def genModel(hidden_size, batchSize, learningRate, step_size, gamma, xav, shuffle):

    #function to init weights to 0.5
    def init_weights(m):
        if type(m) == nn.Linear:
            torch.nn.init.xavier_uniform_(m.weight)
            #m.bias.data.fill_(0.01)

    #layers of the net
    layers = [
                nn.Linear(n_in, hidden_size),nn.Tanh(),
                nn.Linear(hidden_size, n_out),nn.Tanh()
             ]
    model = nn.Sequential(*layers).to(device)
    if xav:
        model.apply(init_weights)
    loss_function = torch.nn.MSELoss()
    optimizer = torch.optim.Adamax(model.parameters(), lr=learningRate)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size, gamma)
    training_data = DataLoader(dataset=dataset, batch_size=batchSize, shuffle=shuffle)

    return {"name" : str(hidden_size) +"-"+ str(batchSize) +"-"+ str(learningRate)+"-"+str(step_size)+"-"+str(gamma),
            "model" : model,
            "training_data" : training_data,
            "loss_function" : loss_function,
            "optimizer" : optimizer,
            "scheduler" : scheduler,
            "results" : []}
#endef genModel-----------------------------------------------------------------------

#this will validate a given model against the testing data and return a score [0,1]
def validate(model):
    yes = 0
    for i in testingData:
        x, y = i[:n_in], i[-n_out:]
        y_pred = model(torch.from_numpy(x).to(device)).detach().cpu().numpy()
        a = np.round(y_pred)
        if(np.array_equal(y,a)):
            yes += 1
    return (yes/len(testingData))    
#endef validate--------------------------------------------------------------------

def train(subjects, epochSize, validateInterval):
    start = time.time()
    epoch = 0
    while(epoch < epochSize):
        epoch += 1
        for idx, subject in enumerate(subjects):
            subject["scheduler"].step()
            for i, data in enumerate(subject["training_data"], 0):
                x, y = data
                
                # Forward pass: Compute predicted y by passing x to the model
                y_pred = subject["model"](x)
                # Compute and print loss
                loss = subject["loss_function"](y_pred, y)

                # Zero gradients, perform a backward pass, and update the weights.
                subject["optimizer"].zero_grad()
                
                # perform a backward pass (backpropagation)
                loss.backward()
                
                # Update the parameters
                subject["optimizer"].step()
                print("epoch", epoch, "training model ", idx, ": ", loss.item(),"     ", end="\r")

            #validate subject every interval
            if epoch % validateInterval == 0:
                print("epoch", epoch, "validating model ", idx, "                       ", end="\r")
                subject["results"].append(validate(subject["model"]))
            
    end = time.time()
    print("done training in ", end - start, "seconds               ")
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------

#training data
print("loading training data...", end="\r")
dataset = TrainingData()
print("loading training data... done.")

#testing data
print("loading testing data...", end="\r")
testingData = np.loadtxt('data/testingdata.csv', delimiter=',', dtype=np.float32)
print("loading testing data... done.")

#genModel(hidden_size, batchSize, learningRate, decay, step, xav_init, shuffle)
print("generating models...", end="\r")
models = [
    genModel(325, 16, 0.04, 3, 0.1, False, False),
    genModel(325, 16, 0.04, 3, 0.2, False, False),
    genModel(325, 16, 0.04, 3, 0.3, False, False),
    genModel(325, 16, 0.04, 3, 0.4, False, False),
    genModel(325, 16, 0.04, 3, 0.5, False, False),
    genModel(325, 16, 0.04, 3, 0.6, False, False),
    genModel(325, 16, 0.04, 3, 0.7, False, False),
    genModel(325, 16, 0.04, 3, 0.8, False, False),
    genModel(325, 16, 0.04, 3, 0.9, False, False),
]
print("generating models... done.")

#do the training! --- train(subjects, epochSize, validateInterval)
train(models, 12, 1)

import os
import re
now = re.sub("[\:]","-", str(datetime.datetime.now()))
model_path = "models/"+now+"/"

os.makedirs(model_path)


for i,subject in enumerate(models):
    torch.save(subject["model"], model_path+str(i)+"  "+subject["name"]+" ("+str(subject["results"][-1]) + ").pt")
    print(subject["results"])
