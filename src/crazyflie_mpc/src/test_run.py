import torch
from torch.autograd import Variable
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pickle
import os
import rospkg
import os
from torch.distributions.normal import Normal
import matplotlib.pyplot as plt
graph = True 
dX = False
normal = False

rp = rospkg.RosPack()

mean = [42000, 42000, 42000, 42000]
variance = 20000

#device = torch.device('cpu')
device = torch.device('cuda')
torch.set_default_tensor_type('torch.cuda.FloatTensor')

#norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "2018-07-25_general_temp-normparams.pkl")
#norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "w-200e-300lr-8e-07b-64d-250hz-cleanp-True-normparams.pkl")
norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "w-100e-100lr-8e-07b-32d-250hz-cleanp-True-normparams.pkl")
#norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "beast-normparams.pkl")

#model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "beast.pth")
#model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "w-200e-300lr-8e-07b-64d-250hz-cleanp-True.pth")
model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "w-100e-100lr-8e-07b-32d-250hz-cleanp-True.pth")

fileObj = open(norms_path, 'r')
scalerX, scalerU, scalerdX = pickle.load(fileObj)

#normX = Variable(torch.Tensor(normX))
dXmin   = torch.Tensor(scalerdX.center_)
dXscale = torch.Tensor(scalerdX.scale_)

Xmin   = torch.Tensor(scalerX.center_)
Xscale = torch.Tensor(scalerX.scale_)

Umin   = torch.Tensor(scalerU.center_)
Uscale = torch.Tensor(scalerU.scale_)

print "dXmin : ", dXmin, " dXscale : ", dXscale  
print "Xmin : ", Xmin, " Xscale : ", Xscale  
print "Umin : ", Umin, " Uscale : ", Uscale  

equi     = 42000

model = torch.load(model_path)
model = model.cuda()
steps = 256


testing = True

def run(batch_size, iters, action_len, mean, variance, current_state, state_idx):

  #model = model.cuda()

  # Get N and T from actions
  #batch_size, iters, action_len = actions.shape
  if not normal:
    actions1 = torch.cuda.FloatTensor(batch_size,1, 1).random_((mean[0] - variance) / steps, (mean[0] + variance) / steps)
    actions2 = torch.cuda.FloatTensor(batch_size,1, 1).random_((mean[1] - variance) / steps, (mean[1] + variance) / steps)
    actions3 = torch.cuda.FloatTensor(batch_size,1, 1).random_((mean[2] - variance) / steps, (mean[2] + variance) / steps)
    actions4 = torch.cuda.FloatTensor(batch_size,1, 1).random_((mean[3] - variance) / steps, (mean[3] + variance) / steps)

    actions1.mul_(steps)
    actions2.mul_(steps)
    actions3.mul_(steps)
    actions4.mul_(steps)

  else:
    actions1 = torch.cuda.FloatTensor(batch_size,1, 1).random_(mean[0] - variance, mean[0] + variance)
    actions2 = torch.cuda.FloatTensor(batch_size,1, 1).random_(mean[1] - variance, mean[1] + variance)
    actions3 = torch.cuda.FloatTensor(batch_size,1, 1).random_(mean[2] - variance, mean[2] + variance)
    actions4 = torch.cuda.FloatTensor(batch_size,1, 1).random_(mean[3] - variance, mean[3] + variance)

  if testing:
    actions1 = torch.cuda.FloatTensor([[[50000]], [[30000]], [[30000]],  [[50000]]])
    actions2 = torch.cuda.FloatTensor([[[30000]], [[50000]], [[30000]],  [[50000]]])
    actions3 = torch.cuda.FloatTensor([[[30000]], [[50000]], [[50000]],  [[30000]]])
    actions4 = torch.cuda.FloatTensor([[[50000]], [[30000]], [[50000]],  [[30000]]])


  actions = torch.cat((actions1, actions2, actions3, actions4), 2)
  actions = actions.expand(-1, iters, -1)




  # Get the desired dimensions
  current_state_trimmed = np.zeros(len(state_idx))
  for i,idx in enumerate(state_idx):
    current_state_trimmed[i] = current_state[idx] 

  # Create current state vector
  X = np.tile(current_state_trimmed, (batch_size, 1))

  # Create scaler objects to scale x and u to standard size
  normU =  scalerU.transform(actions.reshape(batch_size*iters,-1))

  normX =  scalerX.transform(X)
  normU = normU.reshape(batch_size, iters, -1)

  # Convert them to tensors
  normX = Variable(torch.Tensor(normX))
  normU = Variable(torch.Tensor(normU))

  idx = torch.tensor(state_idx)
  results = torch.empty(batch_size, iters, len(state_idx))

  # for each time step
  for i in range(0, iters):

    # create batch for current run
    batch = normU[:,i,:]

    # put states and control together
    input  = Variable(torch.Tensor(torch.cat((normX, batch), 1)))

    # create prediction
    states = model(input)

 
    # Ensure you only take states (makes sure not to take variance if PNN)
    states = states[:,0:len(state_idx):]

    if dX:
      # unnormalize dX
      states.mul_(dXscale)
      states.add_(dXmin)
      #print "statesdX : ", states
      # unnormalize X
      normX.mul_(Xscale)
      normX.add_(Xmin)
      # combine dX with previous X to create final prediction
      states.add_(normX)
      # renormalize new X
      states.sub_(Xmin)
      states.div_(Xscale)

    normX = states  
    results[:,i,:] = normX


  results.mul_(Xscale)
  results.add_(Xmin)

  if graph:
    for i, traj in enumerate(results.cpu().detach().numpy()):
      plt.figure(0)
      plt.plot(traj[:,3], linestyle='--', label="line: " + str(actions[i][0]))
      plt.legend()
      plt.figure(1)
      plt.plot(traj[:,4], linestyle='--', label="line: " + str(actions[i][0]))
      plt.legend()
      #plt.figure(2)
      #plt.plot(traj[:,5], linestyle='--')

  # compute arg mm

  data_eval = results[:,:,state_idx]

  objective_vals = torch.zeros(batch_size, iters)

  #objective_vals.add_((data_eval[:,:,0].mul_(data_eval[:,:,0])).mul_(.1))
  #objective_vals.add_((data_eval[:,:,1].mul_(data_eval[:,:,1])).mul_(.1))
  #objective_vals.add_((data_eval[:,:,2].mul_(data_eval[:,:,2])).mul_(.1))
  objective_vals.add_(data_eval[:,:,3].mul_(data_eval[:,:,3]))
  objective_vals.add_(data_eval[:,:,4].mul_(data_eval[:,:,4]))
  #objective_vals.add_(data_eval[:,:,5].mul_(data_eval[:,:,5]))

  objective_vals = objective_vals.sum(dim=1)

  objective_vals.sqrt_()

  mm_idx = torch.argmin(objective_vals)


  if graph:
    #plt.figure(0)
    #plt.plot(results.cpu().detach().numpy()[mm_idx,:,3], linewidth=5.0, color='r')
    #plt.figure(1)
    #plt.plot(results.cpu().detach().numpy()[mm_idx,:,4], linewidth=5.0, color='r')
    #plt.figure(2)
    #plt.plot(results.cpu().detach().numpy()[mm_idx,:,5], linewidth=5.0, color='r')
    plt.show()

  best_action = actions[mm_idx]


  control = best_action[0]

  return control


