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
graph = False
dX = True
normal = False

rp = rospkg.RosPack()

#mean = [42000, 42000, 42000, 42000]
#variance = 20000

#device = torch.device('cpu')
device = torch.device('cuda')
torch.set_default_tensor_type('torch.cuda.FloatTensor')

#norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "2018-07-25_general_temp-normparams.pkl")
norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/w-200e-100lr-7e-06b-32d-pink_long_hover_cleanp-True-normparams.pkl")
#norms_path_roll = os.path.join(rp.get_path("crazyflie_mpc"), "src", "roll.pkl")
#norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "beast-normparams.pkl")

model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/w-200e-100lr-7e-06b-32d-pink_long_hover_cleanp-True.pth")
#model_path_roll = os.path.join(rp.get_path("crazyflie_mpc"), "src", "roll.pth")


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

model = torch.load(model_path)
model = model.cuda()
steps = 1024

def run(batch_size, iters, action_len, mean, variance, current_state, state_idx):

  #model = model.cuda()
  #print("RECEIVED : ", current_state, " IDX: ", state_idx)
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
    #actions1 = l_actions1[torch.randperm(len(l_actions1))]
    #actions2 = l_actions2[torch.randperm(len(l_actions2))]
    #actions3 = l_actions3[torch.randperm(len(l_actions3))]
    #actions4 = l_actions4[torch.randperm(len(l_actions4))]

    actions1 = torch.cuda.FloatTensor(batch_size,1, 1).random_(mean[0] - variance, mean[0] + variance)
    actions2 = torch.cuda.FloatTensor(batch_size,1, 1).random_(mean[1] - variance, mean[1] + variance)
    actions3 = torch.cuda.FloatTensor(batch_size,1, 1).random_(mean[2] - variance, mean[2] + variance)
    actions4 = torch.cuda.FloatTensor(batch_size,1, 1).random_(mean[3] - variance, mean[3] + variance)
  actions = torch.cat((actions1, actions2, actions3, actions4), 2)
  actions = actions.expand(-1, iters, -1)

  #print "actions : ", actions
  # Get the desired dimensions
  current_state_trimmed = torch.zeros(len(state_idx))
  for i,idx in enumerate(state_idx):
    current_state_trimmed[i] = current_state[idx]
  #print "trimmed : ", current_state_trimmed
  # Create current state vector
  X = current_state_trimmed.expand(batch_size, -1)

  # Create scaler objects to scale x and u to standard size
  #normU =  scalerU.transform(actions.reshape(batch_size*iters,-1))

  #normX =  scalerX.transform(X)
  #normU = normU.reshape(batch_size, iters, -1)
  #X_pitch = X[:,0:1].sub(Xmin)
  #X_pitch.div_(Xscale)
  #X_roll  = X[:,1:2].sub(Xmin_roll)
  #X_roll.div_(Xscale_roll)
  #normX = torch.cat((X_pitch, X_roll), 1)
  normX = X.sub(Xmin)
  normX.div_(Xscale)

  normU = actions.sub(Umin)
  normU.div_(Uscale)


  # Convert them to tensors
  #normX = Variable(torch.Tensor(normX))
  #normU = Variable(torch.Tensor(normU))

  idx = torch.tensor(state_idx)
  results = torch.empty(batch_size, iters, len(state_idx))

  # for each time step
  for i in range(0, iters):

    # create batch for current run
    batch = normU[:,i,:]

    # put states and control together
    #print "normx and batch: ", torch.cat((normX[:,-2:-1], batch), 1)[0]
    #print "normx and batch: ", torch.cat((normX[:,-1:], batch), 1)[0]
    input       = Variable(torch.Tensor(torch.cat((normX, batch), 1)))
    #input_roll  = Variable(torch.Tensor(torch.cat((normX[:,-1:],   batch), 1)))



    # create prediction
    states  = model(input)
    #states_roll = model_roll(input_roll)

    # Ensure you only take states (makes sure not to take variance if PNN)
    states = states[:,0:len(state_idx):]
    #states = states[:,0:1]
    #states_roll = states_roll[:,0:1]

    #states[:,4] = states_roll[:,3]
    #states[:,1] = states_roll[:,1]

    if dX:
      # unnormalize dX
      states.mul_(dXscale)
      states.add_(dXmin)
      #print "statesdX : ", states
      # unnormalize X
      normX.mul_(Xscale)
      normX.add_(Xmin)
      #print "statesX : ", states
      # combine dX with previous X to create final prediction
      states.add_(normX)
      #print "states added : ", states
      # renormalize new X
      states.sub_(Xmin)
      states.div_(Xscale)
      #print "states final norm : ", states

    normX = states
    #normX = torch.cat((states, states_roll), 1)
    #X = normX.clone().detach().cpu().numpy()
    results[:,i,:] = normX

  #results = results.cpu().detach().numpy()

  #final_results = torch.empty(results.shape)
  #for i in range(0,len(results)):
    #final_results[i] = scalerX.inverse_transform(results[i])
  #results[:,:,0] = results[:,:,0].mul(Xscale)
  #results[:,:,0] = results[:,:,0].add(Xmin)

  #results[:,:,1] = results[:,:,1].mul(Xscale_roll)
  #results[:,:,1] = results[:,:,1].add(Xmin_roll)

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

  #THIS IS WHERE THE "OBJECTIVE FUNCTION" FOR THE MPC IS CONSTRUCTED:::::::::::::

  objective_vals.add_((data_eval[:,:,0].mul_(data_eval[:,:,0])).mul_(.1))
  objective_vals.add_((data_eval[:,:,1].mul_(data_eval[:,:,1])).mul_(.1))
  objective_vals.add_((data_eval[:,:,2].mul_(data_eval[:,:,2])).mul_(.05))
  objective_vals.add_((data_eval[:,:,3].mul_(data_eval[:,:,3])).mul_(10))   #Pitch
  objective_vals.add_((data_eval[:,:,4].mul_(data_eval[:,:,4])).mul_(10))   #Roll
  objective_vals.add_((data_eval[:,:,5].mul_(data_eval[:,:,5])).mul_(2)) 

  objective_vals = objective_vals.sum(dim=1)

  objective_vals.sqrt_()

  mm_idx = torch.argmin(objective_vals)                         #Since controlling to 0 setpoint


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

  # Result[mm_idx][0] is the 12 state data for the predicted state
  return control# , results[mm_idx][0]  #Not sure why results is returned here; commented out to see if this is the speed killer
  # return control
