import numpy as np
import torch
from torch.autograd import Variable
import pickle

#model = torch.load('clean_flie_hover_long.pth')
model = torch.load('beast.pth')

fileObj = open('beast-normparams.pkl')
scalerX, scalerU, scalerDx = pickle.load(fileObj)

pwmslist = [ [[60000, 60000, 20000, 20000]],[[20000, 20000, 60000, 60000]], [[60000,20000,20000,60000]], [[20000, 60000, 60000, 20000]] ]


states = [[0,0,0,0,0]]


for pwms in pwmslist:

  print "Running: ", pwms
  pwms = model.scalarU.transform(pwms)
  states = model.scalarX.transform(states)

  input = Variable(torch.Tensor(np.concatenate((states, pwms), 1)))

  #output = model(input)
  #input = torch.cat((output[:,:5],torch.Tensor(pwms)), 1)

  output = input
  for i in range(0,500):
    old_output = output[:,:5]
    output = model(input)
    output = output.detach().numpy()
    output = output[:,:5]
    output = model.scalardX.inverse_transform(output)
    output = torch.Tensor(output)
    output = output + old_output # take off from here

    input = torch.cat((output[:,:5],torch.Tensor(pwms)), 1)
    


  output = output.detach().numpy()
  output = output[:,:5]

  output = model.scalardX.inverse_transform(output)

  print "OUTPUT: ", output


