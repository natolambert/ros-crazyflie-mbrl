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
dX = True
normal = False
testing = True
rp = rospkg.RosPack()


#device = torch.device('cpu')
device = torch.device('cuda')
torch.set_default_tensor_type('torch.cuda.FloatTensor')

# make sure norms from pink_clean_long ??

norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "w-250e-95lr-5e-06b-32d-pink_long_cleanp-True-normparams.pkl")

model_path_accel = os.path.join(rp.get_path("crazyflie_mpc"), "src", "accel.pth")
model_path_pirol = os.path.join(rp.get_path("crazyflie_mpc"), "src", "pirol.pth")


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

model_accel = torch.load(model_path_accel)
model_accel = model_accel.cuda()
model_accel = model_accel.features.train(False)

model_pirol = torch.load(model_path_pirol)
model_pirol = model_pirol.cuda()
model_pirol.features.train(False)
  

print "model_accel\n", model_accel
print "model_pirol\n", model_pirol

steps = 512

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

  if testing:
    #actions1 = torch.cuda.FloatTensor([[[50000]], [[30000]], [[30000]],  [[50000]]])
    #actions2 = torch.cuda.FloatTensor([[[30000]], [[50000]], [[30000]],  [[50000]]])
    #actions3 = torch.cuda.FloatTensor([[[30000]], [[50000]], [[50000]],  [[30000]]])
    #actions4 = torch.cuda.FloatTensor([[[50000]], [[30000]], [[50000]],  [[30000]]])
    actions1 = torch.cuda.FloatTensor([[[0000]], [[0000]], [[0000]],  [[0000]]])
    actions2 = torch.cuda.FloatTensor([[[0000]], [[0000]], [[0000]],  [[0000]]])
    actions3 = torch.cuda.FloatTensor([[[0000]], [[0000]], [[0000]],  [[0000]]])
    actions4 = torch.cuda.FloatTensor([[[0000]], [[0000]], [[0000]],  [[0000]]])




  actions = torch.cat((actions1, actions2, actions3, actions4), 2)
  actions = actions.expand(-1, iters, -1)

  # Get the desired dimensions
  current_state_trimmed = torch.zeros(len(state_idx))
  for i,idx in enumerate(state_idx):
    current_state_trimmed[i] = current_state[idx] 

  # Create current state vector
  X = current_state_trimmed.expand(batch_size, -1)

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

    print "states accel\n", states_accel, "\nstates pirol\n", states_pirol
 
    # Ensure you only take states (makes sure not to take variance if PNN)
    #print "accel : ", states_accel.shape, " pirol : ", states_pirol.shape

    states_accel = states_accel[:,:3]
    states_pirol = states_pirol[:,:2]
    #print "accel : ", states_accel.shape, " pirol : ", states_pirol.shape

    states = torch.cat((states_accel, states_pirol), 1)
    print "States shape : ", states.shape, " states : ", states


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


    normX = states
    results[:,i,:] = normX


  results.mul_(Xscale)
  results.add_(Xmin)

  if graph:
    for i,traj in enumerate(results.cpu().detach().numpy()):

      plt.figure(0)
      plt.plot(traj[:,3], linestyle='--', label="line: " + str(actions[i][0]))
      plt.legend()
      plt.figure(1)
      plt.plot(traj[:,4], linestyle='--', label="line: " + str(actions[i][0]))
      plt.legend()
      #plt.figure(0)
      #plt.plot(traj[:,0], linestyle='--')
      #plt.figure(1)
      #plt.plot(traj[:,1], linestyle='--')
      #plt.figure(2)
      #plt.plot(traj[:,2], linestyle='--')
      #plt.figure(3)
      #plt.plot(traj[:,3], linestyle='--')
      #plt.figure(4)
      #plt.plot(traj[:,4], linestyle='--')
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
    #plt.plot(results.cpu().detach().numpy()[mm_idx,:,0], linewidth=5.0, color='r')
    #plt.figure(1)
    #plt.plot(results.cpu().detach().numpy()[mm_idx,:,1], linewidth=5.0, color='r')
    #plt.figure(2)
    #plt.plot(results.cpu().detach().numpy()[mm_idx,:,2], linewidth=5.0, color='r')
    #plt.figure(3)
    #plt.plot(results.cpu().detach().numpy()[mm_idx,:,3], linewidth=5.0, color='r')
    #plt.figure(4)
    #plt.plot(results.cpu().detach().numpy()[mm_idx,:,4], linewidth=5.0, color='r')
    #plt.figure(5)
    #plt.plot(results.cpu().detach().numpy()[mm_idx,:,5], linewidth=5.0, color='r')
    plt.show()

  best_action = actions[mm_idx]


  control = best_action[0]

  return control


