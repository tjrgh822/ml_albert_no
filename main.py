import torch
import torch.nn as nn
import math
from torch.optim import Optimizer
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import transforms
import numpy as np
import datetime
import pickle
import os
import matplotlib.pyplot as plt


import utils
import models



#hyper parameter 




#start training

if __name__ == "__main__":
    hyper_param_dict = { 
                'project' : 'VGG13',
                'data root' : './Datasets/cifar10',
                'epochs' : 200,
                'batch' : 256, 
                'lr' : 0.05,
                'optimizer': 'SGD',
                'momentum' : 0.9,   
                'beta1' : 0.9,
                'beta2' : 0.999, 
                'weight_decay' : 5e-4
                }
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    
    # run VGG13
    model = models.VGG13()
    model.to(device)
    print(f'\n\n**************  start new model : {hyper_param_dict['project']} ******************')
    utils.train(hyper_param_dict, model, device)
    del model

    #run GoogleNet without BN
    model = models.GoogLeNet()
    model.to(device)
    hyper_param_dict['project'] = 'GoogLeNet'
    hyper_param_dict['lr'] = 0.1
    hyper_param_dict['epochs'] = 100
    print(f'\n\n**************  start new model : {hyper_param_dict['project']} ******************')
    utils.train(hyper_param_dict, model, device)
    del model
    
    #run GoogleNet with BN
    model = models.GoogLeNet_w_bn()
    model.to(device)
    hyper_param_dict['project'] = 'GoogLeNet_w_bn'
    print(f'\n\n**************  start new model : {hyper_param_dict['project']} ******************')
    utils.train(hyper_param_dict, model, device)
    del model

    # run ResNet18
    model = models.ResNet18()
    model.to(device)
    hyper_param_dict['project'] = 'ResNet18'
    hyper_param_dict['lr'] = 0.03
    print(f'\n\n**************  start new model : {hyper_param_dict['project']} ******************')
    utils.train(hyper_param_dict, model, device)
    del model

    # run ResNet34
    model = models.ResNet34()
    model.to(device)
    hyper_param_dict['project'] = 'ResNet34'
    print(f'\n\n**************  start new model : {hyper_param_dict['project']} ******************')
    utils.train(hyper_param_dict, model, device)
    del model

    # run ResNet50
    model = models.ResNet34()
    model.to(device)
    hyper_param_dict['project'] = 'ResNet50'
    print(f'\n\n**************  start new model : {hyper_param_dict['project']} ******************')
    utils.train(hyper_param_dict, model, device)
    del model






def load_results():
    #find save dir path
    if hyper_param_dict[ 'project'] is not None:
        save_dir = './Result/' + hyper_param_dict[ 'project'] + '/'
    else:
        save_dir = './Result/'
    dir_list = os.listdir(save_dir)

    for dir_name in dir_list:
        if '_' in dir_name:
            load_dir = save_dir + dir_name
            train_acc = np.load(load_dir + '/np_train_acc_list.npy', allow_pickle=True)
            test_acc = np.load(load_dir + '/np_test_acc_list.npy', allow_pickle=True)
            train_loss = np.load(load_dir + '/np_train_loss_list.npy', allow_pickle=True)
            test_loss = np.load(load_dir + '/np_test_loss_list.npy', allow_pickle=True)

            with open( load_dir + '/hyper.pickle', 'rb') as fr:
                hyper_param_load = pickle.load(fr)

            plt.plot(np.arange(0, train_acc.shape[0]), train_acc, label=  'lr = ' + str(hyper_param_load['lr']))
        plt.legend()
        plt.title(hyper_param_dict['project'])
        #plt.show()