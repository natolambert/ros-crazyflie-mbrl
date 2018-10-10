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

device = torch.device('cuda')
torch.set_default_tensor_type('torch.cuda.FloatTensor')

#NORMS FILE
norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/vid_models/2018-09-15--16-03-14.5--Min error0.017405348309015824--w=500e=60lr=0.0003b=32de=3d=_CONF_p=True--normparams.pkl")
#MODEL FILE
model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/vid_models/2018-09-15--16-03-14.5--Min error0.017405348309015824--w=500e=60lr=0.0003b=32de=3d=_CONF_p=True.pth")


fileObj = open(norms_path, 'r')
scalerX, scalerU, scalerdX = pickle.load(fileObj)

# for minmax scaler
Umin = torch.Tensor(scalerU.data_min_)
# Umax = torch.Tensor(scalerU.max_)
Uscale = torch.Tensor(scalerU.scale_)


###############
# For MinMaxScaler
dXmin   = torch.Tensor(scalerdX.data_min_)
dXscale = torch.Tensor(scalerdX.scale_)

Xmin   = torch.Tensor(scalerX.mean_)
Xscale = torch.Tensor(scalerX.scale_)
#############################

model = torch.load(model_path)
model.eval()
model = model.cuda()
steps = 256

def run_stack(batch_size, iters, action_len, mean, prev_action, variance, current_state, state_idx, numStack, meanAdjust):
  if printflag: print('\n')
  #model = model.cuda()
  #print("RECEIVED : ", current_state, " IDX: ", state_idx)
  prev_action = torch.tensor(prev_action).type(torch.cuda.FloatTensor)

  mean = meanAdjust * mean
  # variance = variance*(1+4*(1.25-meanAdjust))
  # print(variance)
  # print(mean)
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

  # actions = torch.cat((actions,actions),2)
  # actions = actions.repeat(-1,-1,numStack*4)

  actions = actions.expand(-1, iters, -1)
  actions = actions.repeat(1, 1, numStack)


  # Replace the correct actions with the prev_action
  if numStack >1:
      for i in range(min(iters,numStack-1)):

          actions[:,i,4*(i+1):] = prev_action[:-4*(i+1)]

  # For stacked state
  X = torch.tensor(current_state).type(torch.cuda.FloatTensor)
  if printflag: print(X)
  X = X.expand(batch_size, -1)

  normX = X.sub(Xmin)
  normX.div_(Xscale)

  #Usage for minmaxscaler
  normU = actions.sub(Umin)
  normU.mul_(Uscale)
  normU.sub_(1)     # sub one because scaled (-1,1)

  idx = torch.tensor(state_idx)
  results = torch.empty(batch_size, iters, len(state_idx))

  # for each time step
  for i in range(0, iters):
    if printflag:
        print('------------')
        print(i)

    # if (i>1):
    # create batch for current run
    batch = normU[:,i,:]
    #
    # if i == 0:
    #     prev_action.sub_(Umin[:4])
    #     prev_action.mul_(Uscale[:4])
    #     prev_action.sub_(1)
    #     batch[:,4:] = prev_action

    input   = torch.Tensor(torch.cat((normX, batch), 1))
    states  = model(input)              # For stacked model input, input should be of form (1, numStack*(9+4))
    states = states[:,0:len(state_idx)] # Ensure you only take states (makes sure not to take variance if PNN)

    # unnormalize dX
    states.add_(1)   #because scaled to -1
    states.div_(dXscale)
    states.add_(dXmin)

    # unnormalize X
    normX.mul_(Xscale)
    normX.add_(Xmin)

    # combine dX with previous X to create final prediction
    states.add_(normX[:,:9]) #[:,3:6])
    normX[:,9:] = normX[:,:9*(numStack-1)]
    normX[:,:9] = states


    # renormalize normX
    normX = normX.sub(Xmin)
    normX.div_(Xscale)

    # renormalize new X
    states.sub_(Xmin[:9]) #[3:6])
    states.div_(Xscale[:9]) #[3:6])

    results[:,i,:] = normX[:,:9]

  # END FOR LOOP OF T
  # =================

  # convert back to unscaled values
  results.mul_(Xscale[:9])
  results.add_(Xmin[:9])

  data_eval = results[:,:,state_idx]
  objective_vals = torch.zeros(batch_size, iters)


  # # Minimize values of angular accelerations
  # objective_vals.add_((data_eval[:,:,0].mul_(data_eval[:,:,0])).mul_(.0001))
  # objective_vals.add_((data_eval[:,:,1].mul_(data_eval[:,:,1])).mul_(.0001))
  # objective_vals.add_((data_eval[:,:,2].mul_(data_eval[:,:,2])).mul_(.00001))

  # # Minimize values of euler angles, trimmed, squared
  objective_vals.add_(((data_eval[:,:,3].sub_(2)).mul_(data_eval[:,:,3])).mul_(10))   #Pitch DD trim 5
  objective_vals.add_(((data_eval[:,:,4].sub_(2)).mul_(data_eval[:,:,4])).mul_(2))   #Roll DD trime -3
  # objective_vals.add_((data_eval[:,:,5].mul_(data_eval[:,:,5])).mul_(2))

  # euler angle rate regularization (add penalty to faster rate changes)
  # objective_vals[:,1:].add_((data_eval[:,1:,3].sub_(data_eval[:,:-1,3])).mul_((data_eval[:,1:,3].sub_(data_eval[:,:-1,3]))).mul_(2))
  # objective_vals[:,1:].add_((data_eval[:,1:,4].sub_(data_eval[:,:-1,4])).mul_((data_eval[:,1:,4].sub_(data_eval[:,:-1,4]))).mul_(2))
  # objective_vals[:,1:].add_((data_eval[:,1:,5].sub_(data_eval[:,:-1,5])).mul_((data_eval[:,1:,5].sub_(data_eval[:,:-1,5]))).mul_(.2))
  objective_vals[:,1].add_((data_eval[:,1,3].sub_(data_eval[:,0,3])).mul_((data_eval[:,1,3])).mul_(10780))   #Pitch rate
  objective_vals[:,1].add_((data_eval[:,1,4].sub_(data_eval[:,0,4])).mul_((data_eval[:,1,4])).mul_(8300))   #Roll rate
  objective_vals[:,1].add_((data_eval[:,1,5].sub_(data_eval[:,0,5])).mul_((data_eval[:,1,5])).mul_(300))    #Yaw rate

  # Minimize values of linear accelerations
  # objective_vals.add_((data_eval[:,:,6].mul_(data_eval[:,:,6])).mul_(2))
  # objective_vals.add_((data_eval[:,:,7].mul_(data_eval[:,:,7])).mul_(2))
  # objective_vals.add_(((data_eval[:,:,8].sub_(11)).mul_(data_eval[:,:,8])).mul_(20))


  # slope = (data_eval[:,:,3:6].squeeze()).sub(X[:,3:6])
  # # # T=1 Slope code
  # objective_vals.squeeze_()
  # objective_vals.add_(slope[:,0].mul_(slope[:,0]).mul_(800))
  # objective_vals.add_(slope[:,1].mul_(slope[:,1]).mul_(500))
  # objective_vals.add_(slope[:,2].mul_(slope[:,2]).mul(500))
  # objective_vals.add_(((data_eval[:,:,4].squeeze()).sub(X[:,4])).mul(((data_eval[:,:,4].squeeze()).sub_(X[:,4]))).mul(10))
  # objective_vals.add_(((data_eval[:,:,5].squeeze()).sub(X[:,5])).mul(((data_eval[:,:,5].squeeze()).sub_(X[:,5]))).mul(10))


  if iters >1: objective_vals = objective_vals.sum(dim=1)

  # mm_idx = torch.argmin(objective_vals)   #switch for real objective function
  mm_idx = np.random.randint(0,batch_size)  #switch for random action selection


  if graph:
      current_state_trimmed = torch.tensor(current_state) #for plotting
      curr = current_state_trimmed.cpu().detach().numpy()
      best = results.cpu().detach().numpy()[mm_idx,:,:]


      # SAVE ARRAYS FOR WATERFALL PLOT
      np.save('actions', actions.cpu().detach().numpy())
      np.save('curr', curr)
      np.save('predicted', results.cpu().detach().numpy())
      np.save('best_id', mm_idx.cpu().detach().numpy())

      for traj in results.cpu().detach().numpy():
        plt.figure(3)
        plt.title('Pitch')
        plt.plot(np.append(curr[3], traj[:,3]), linestyle='--')
        plt.figure(4)
        plt.title('Roll')
        plt.plot(np.append(curr[4], traj[:,4]), linestyle='--')

      plt.figure(3)
      plt.plot(np.append(curr[3], best[:,3]), linewidth=5.0, color='r')
      plt.figure(4)
      plt.plot(np.append(curr[4], best[:,4]), linewidth=5.0, color='r')
      plt.show()

  best_action = actions[mm_idx]
  control = best_action[0]

  # for dropped packets
  next_state = results[mm_idx,0,:]




  return control, objective_vals[mm_idx], next_state
