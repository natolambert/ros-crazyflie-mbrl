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
graph =False
dX = True
normal = False

rp = rospkg.RosPack()


#device = torch.device('cpu')
device = torch.device('cuda')
torch.set_default_tensor_type('torch.cuda.FloatTensor')

# make sure norms from pink_clean_long ??

# norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/w-250e-95lr-5e-06b-32d-pink_long_cleanp-True-normparams.pkl")
norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/accel-normparams.pkl")

model_path_accel = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/accel.pth")
model_path_pirol = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/pirol.pth")


fileObj = open(norms_path, 'r')
scalerX, scalerU, scalerdX = pickle.load(fileObj)

#normX = Variable(torch.Tensor(normX))
dXmin   = torch.Tensor(scalerdX.center_)
#dXmin = torch.cat((dXmin[:3], dXmin[4:]), 0)
dXscale = torch.Tensor(scalerdX.scale_)
#dXscale = torch.cat((dXscale[:3], dXscale[4:]), 0)
Xmin   = torch.Tensor(scalerX.center_)
#Xmin = torch.cat((Xmin[:3], Xmin[4:]), 0)
Xscale = torch.Tensor(scalerX.scale_)
#Xscale = torch.cat((Xscale[:3], Xscale[4:]), 0)

Umin   = torch.Tensor(scalerU.center_)
Uscale = torch.Tensor(scalerU.scale_)

print "dXmin : ", dXmin, " dXscale : ", dXscale
print "Xmin : ", Xmin, " Xscale : ", Xscale
print "Umin : ", Umin, " Uscale : ", Uscale

equi     = 42000

model_accel = torch.load(model_path_accel)
model_accel = model_accel.cuda()
model_accel = model_accel.features.train(False)

model_pirol = torch.load(model_path_pirol)
model_pirol = model_pirol.cuda()
model_pirol = model_pirol.features.train(False)

steps = 1024

def run(batch_size, iters, action_len, mean, variance, current_state, state_idx):

  # Create random actions
  actions1 = torch.cuda.FloatTensor(batch_size,1, 1).random_((mean[0] - variance) / steps, (mean[0] + variance) / steps)
  actions2 = torch.cuda.FloatTensor(batch_size,1, 1).random_((mean[1] - variance) / steps, (mean[1] + variance) / steps)
  actions3 = torch.cuda.FloatTensor(batch_size,1, 1).random_((mean[2] - variance) / steps, (mean[2] + variance) / steps)
  actions4 = torch.cuda.FloatTensor(batch_size,1, 1).random_((mean[3] - variance) / steps, (mean[3] + variance) / steps)

  actions1.mul_(steps)
  actions2.mul_(steps)
  actions3.mul_(steps)
  actions4.mul_(steps)
  actions = torch.cat((actions1, actions2, actions3, actions4), 2)
  actions = actions.expand(-1, iters, -1)

  # Get the desired dimensions
  current_state_trimmed = torch.zeros(len(state_idx))
  for i,idx in enumerate(state_idx):
    current_state_trimmed[i] = current_state[idx]

  # Create current state vector
  X = current_state_trimmed.expand(batch_size, -1)

  #print "X shape :", X.shape
  #X = torch.cat((X[:,:3], X[:,4:]), 1)
  #print "X shape :", X.shape
  normX = X.sub(Xmin)
  normX.div_(Xscale)

  normU = actions.sub(Umin)
  normU.div_(Uscale)

  idx = torch.tensor(state_idx)
  results = torch.empty(batch_size, iters, len(state_idx))

  # for each time step
  for i in range(0, iters):

    # create batch for current run
    batch = normU[:,i,:]

    # put states and control together
    input_accel = Variable(torch.Tensor(torch.cat((normX, batch), 1)))
    input_pirol = Variable(torch.Tensor(torch.cat((normX, batch), 1)))

    # create prediction
    states_accel = model_accel(input_accel)
    states_pirol = model_pirol(input_pirol)

    # Ensure you only take states (makes sure not to take variance if PNN)
    #print "accel : ", states_accel.shape, " pirol : ", states_pirol.shape

    states_accel = states_accel[:,:3]
    states_pirol = states_pirol[:,:2]
    #print "accel : ", states_accel.shape, " pirol : ", states_pirol.shape

    states = torch.cat((states_accel, states_pirol), 1)
    #print "States shape : ", states.shape, " states : ", states


    if dX:
      # unnormalize dX
      states.mul_(dXscale)
      states.add_(dXmin)

      # unnormalize X
      normX.mul_(Xscale)
      normX.add_(Xmin)

      # combine dX with previous X to create final prediction
      states.add_(normX)

      # renormalize new X
      states.sub_(Xmin)
      states.div_(Xscale)


    normX  = states
    results[:,i,:] = normX


  results.mul_(Xscale)
  results.add_(Xmin)

  if graph:
    for traj in results.cpu().detach().numpy():
      plt.figure(0)
      plt.plot(traj[:,0], linestyle='--')
      plt.figure(1)
      plt.plot(traj[:,1], linestyle='--')
      plt.figure(2)
      plt.plot(traj[:,2], linestyle='--')
      plt.figure(3)
      plt.plot(traj[:,3], linestyle='--')
      plt.figure(4)
      plt.plot(traj[:,4], linestyle='--')
      #plt.figure(5)
      #plt.plot(traj[:,5], linestyle='--')


  #print "Final Results Example:\n", final_results[0][0]

  #print "final results", final_results

  #return final_results, actions


  # compute arg mm

  # data = X_sim = results
  data_eval = results[:,:,state_idx]
  #print "data_eval : ", data_eval


  #objective_vals = [torch.sum(optimizer(traj), dim=0) for traj in data_eval]


  objective_vals = torch.zeros(batch_size, iters)

  objective_vals.add_((data_eval[:,:,0].mul_(data_eval[:,:,0])).mul_(.1))
  objective_vals.add_((data_eval[:,:,1].mul_(data_eval[:,:,1])).mul_(.1))
  objective_vals.add_((data_eval[:,:,2].mul_(data_eval[:,:,2])).mul_(.05))
  objective_vals.add_((data_eval[:,:,3].mul_(data_eval[:,:,3])).mul_(2))
  objective_vals.add_((data_eval[:,:,4].mul_(data_eval[:,:,4])).mul_(2))
  objective_vals.add_(data_eval[:,:,5].mul_(data_eval[:,:,5]))

  objective_vals = objective_vals.sum(dim=1)

  objective_vals.sqrt_()

  mm_idx = torch.argmin(objective_vals)


  if graph:
    plt.figure(0)
    plt.plot(results.cpu().detach().numpy()[mm_idx,:,0], linewidth=5.0, color='r')
    plt.figure(1)
    plt.plot(results.cpu().detach().numpy()[mm_idx,:,1], linewidth=5.0, color='r')
    plt.figure(2)
    plt.plot(results.cpu().detach().numpy()[mm_idx,:,2], linewidth=5.0, color='r')
    plt.figure(3)
    plt.plot(results.cpu().detach().numpy()[mm_idx,:,3], linewidth=5.0, color='r')
    plt.figure(4)
    plt.plot(results.cpu().detach().numpy()[mm_idx,:,4], linewidth=5.0, color='r')
    #plt.figure(5)
    #plt.plot(results.cpu().detach().numpy()[mm_idx,:,5], linewidth=5.0, color='r')
    plt.show()

  best_action = actions[mm_idx]


  control = best_action[0]

  return control, results[mm_idx][0]
