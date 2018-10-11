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
printflag = False
dX = True

rp = rospkg.RosPack()

#device = torch.device('cpu')
device = torch.device('cuda')
torch.set_default_tensor_type('torch.cuda.FloatTensor')

norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/sep12_float/2018-09-12--18-56-18.5--Min error0.0001074432409094537--w=500e=250lr=0.001b=32de=3d=_CONF_p=True--normparams.pkl")

model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/sep12_float/2018-09-12--18-56-18.5--Min error0.0001074432409094537--w=500e=250lr=0.001b=32de=3d=_CONF_p=True.pth")

fileObj = open(norms_path, 'r')
scalerX, scalerU, scalerdX = pickle.load(fileObj)
  #final_results = torch.empty(results.shape)
  #for i in range(0,len(results)):

# FOR ROBUST SCALER
#normX = Variable(torch.Tensor(normX))
# dXmin   = torch.Tensor(scalerdX.center_)
# dXscale = torch.Tensor(scalerdX.scale_)
#
# Xmin   = torch.Tensor(scalerX.center_)
# Xscale = torch.Tensor(scalerX.scale_)

# Umin   = torch.Tensor(scalerU.center_)
# Uscale = torch.Tensor(scalerU.scale_)
#####################

# for minmax scaler
Umin = torch.Tensor(scalerU.data_min_)
# Umax = torch.Tensor(scalerU.max_)
Uscale = torch.Tensor(scalerU.scale_)


###############

# For StandardScaler
# dXmin   = torch.Tensor(scalerdX.mean_)
# dXscale = torch.Tensor(scalerdX.scale_)

# For MinMaxScaler
dXmin   = torch.Tensor(scalerdX.data_min_)
dXscale = torch.Tensor(scalerdX.scale_)

Xmin   = torch.Tensor(scalerX.mean_)
Xscale = torch.Tensor(scalerX.scale_)
#############################





# print "dXmin : ", dXmin, " dXscale : ", dXscale
# print "Xmin : ", Xmin, " Xscale : ", Xscale
# print "Umin : ", Umin, " Uscale : ", Uscale

model = torch.load(model_path)
model.eval()
model = model.cuda()
steps = 256

def run(batch_size, iters, action_len, mean, prev_action, variance, current_state, state_idx, numStack = 1):
  if printflag: print('\n')
  #model = model.cuda()
  #print("RECEIVED : ", current_state, " IDX: ", state_idx)

  prev_action = torch.tensor(prev_action).type(torch.cuda.FloatTensor)

  actions1 = torch.cuda.FloatTensor(batch_size,1, 1).random_(int((mean[0] - variance)) / steps, int((mean[0] + variance)) / steps)
  actions2 = torch.cuda.FloatTensor(batch_size,1, 1).random_(int((mean[1] - variance)) / steps, int((mean[1] + variance)) / steps)
  actions3 = torch.cuda.FloatTensor(batch_size,1, 1).random_(int((mean[2] - variance)) / steps, int((mean[2] + variance)) / steps)
  actions4 = torch.cuda.FloatTensor(batch_size,1, 1).random_(int((mean[3] - variance)) / steps, int((mean[3] + variance)) / steps)

  actions1.mul_(steps)
  actions2.mul_(steps)
  actions3.mul_(steps)
  actions4.mul_(steps)


  #CHANGE TO NUMSTACK
  actions = torch.cat((actions1, actions2, actions3, actions4), 2)
  actions = torch.cat((actions,actions),2)
  actions = actions.expand(-1, iters, -1)

  current_state_trimmed = torch.tensor(current_state)

  # For stacked state
  X = torch.tensor(current_state).type(torch.cuda.FloatTensor)
  if printflag: print(X)
  X = X.expand(batch_size, -1)

  # Create scaler objects to scale x and u to standard size
  #normU =  scalerU.transform(actions.reshape(batch_size*iters,-1))


  normX = X.sub(Xmin)
  normX.div_(Xscale)

  # normU = actions.sub(Umin)
  # normU.div_(Uscale)

  #Usage for minmaxscaler
  normU = actions.sub(Umin)
  normU.mul_(Uscale)
  normU.sub_(1)     # sub one because scaled (-1,1)

  # X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
  # X_scaled = X_std * (max - min) + min

  idx = torch.tensor(state_idx)
  results = torch.empty(batch_size, iters, len(state_idx))

  # for each time step
  for i in range(0, iters):

    batch = normU[:,i,:]

    if i == 0:
        prev_action.sub_(Umin[:4])
        prev_action.mul_(Uscale[:4])
        prev_action.sub_(1)
        batch[:,4:] = prev_action

    # put states and control together
    input       = torch.Tensor(torch.cat((normX, batch), 1))
    #input_roll  = Variable(torch.Tensor(torch.cat((normX[:,-1:],   batch), 1)))
    # create prediction
    states  = model(input)

    # Ensure you only take states (makes sure not to take variance if PNN)
    states = states[:,0:len(state_idx)]


    if dX:
      # unnormalize dX
      states.add_(1)   #because scaled to -1
      states.div_(dXscale)
      states.add_(dXmin)
      #print "statesdX : ", states

      # unnormalize X
      normX.mul_(Xscale)
      normX.add_(Xmin)
      #print "statesX : ", states


      # combine dX with previous X to create final prediction
      states.add_(normX[:,:9]) #[:,3:6])

      normX[:,9:] = normX[:,:9]
      normX[:,:9] = states

      # renormalize normX
      normX = normX.sub(Xmin)
      normX.div_(Xscale)

      # renormalize new X
      states.sub_(Xmin[:9])
      states.div_(Xscale[:9])

    results[:,i,:] = normX[:,:9]

  # END FOR LOOP OF T
  # =================

  # convert back to unscaled values
  results.mul_(Xscale[:9])
  results.add_(Xmin[:9])



  # compute arg mm
  data_eval = results[:,:,state_idx]


  objective_vals = torch.zeros(batch_size, iters)

  #THIS IS WHERE THE "OBJECTIVE FUNCTION" FOR THE MPC IS CONSTRUCTED:::::::::::::
  # # Minimize values of angular accelerations
  # objective_vals.add_((data_eval[:,:,0].mul_(data_eval[:,:,0])).mul_(.001))
  # objective_vals.add_((data_eval[:,:,1].mul_(data_eval[:,:,1])).mul_(.001))
  objective_vals.add_((data_eval[:,:,2].mul_(data_eval[:,:,2])).mul_(.00001))



  # # minimize values of euler angles
  # if abs(current_state_trimmed[3]) > 5: objective_vals.add_(((data_eval[:,:,3].sub_(0)).mul_(data_eval[:,:,3])).mul_(.1))   #Pitch
  # if abs(current_state_trimmed[4]) > 5: objective_vals.add_(((data_eval[:,:,4].sub_(0)).mul_(data_eval[:,:,4])).mul_(.1))   #Roll
  objective_vals.add_(((data_eval[:,:,3].sub_(0)).mul_(data_eval[:,:,3])).mul_(10))   #Pitch
  objective_vals.add_(((data_eval[:,:,4].sub_(0)).mul_(data_eval[:,:,4])).mul_(10))   #Roll
  # objective_vals.add_((data_eval[:,:,5].mul_(data_eval[:,:,5])).mul_(2))

  # euler angle rate regularization (add penalty to faster rate changes)
  # objective_vals[:,1:].add_((data_eval[:,1:,3].sub_(data_eval[:,:-1,3])).mul_((data_eval[:,1:,3].sub_(data_eval[:,:-1,3]))).mul_(2))
  # objective_vals[:,1:].add_((data_eval[:,1:,4].sub_(data_eval[:,:-1,4])).mul_((data_eval[:,1:,4].sub_(data_eval[:,:-1,4]))).mul_(2))
  # objective_vals[:,1:].add_((data_eval[:,1:,5].sub_(data_eval[:,:-1,5])).mul_((data_eval[:,1:,5].sub_(data_eval[:,:-1,5]))).mul_(.2))
  objective_vals[:,1].add_((data_eval[:,1,3].sub_(data_eval[:,0,3])).mul_((data_eval[:,1,3])).mul_(10))
  objective_vals[:,1].add_((data_eval[:,1,4].sub_(data_eval[:,0,4])).mul_((data_eval[:,1,4])).mul_(10))
  # objective_vals[:,1].add_((data_eval[:,1,5].sub_(data_eval[:,0,5])).mul_((data_eval[:,1,5])).mul_(1))

  # Minimize values of linear accelerations
  # objective_vals.add_((data_eval[:,:,6].mul_(data_eval[:,:,6])).mul_(.002))
  # objective_vals.add_((data_eval[:,:,7].mul_(data_eval[:,:,7])).mul_(.002))
  objective_vals.add_(((data_eval[:,:,8].sub_(11)).mul_(data_eval[:,:,8])).mul_(.02))


  # T=1 Slope code
  objective_vals.squeeze_()

  if iters >1: objective_vals = objective_vals.sum(dim=1)

  mm_idx = torch.argmin(objective_vals)   #switch for real objective function
  # mm_idx = np.random.randint(0,batch_size)  #switch for random action selection

  best_action = actions[mm_idx]


  control = best_action[0]

  return control, objective_vals[mm_idx]# , results[mm_idx][0]  #Not sure why results is returned here; commented out to see if this is the speed killer
