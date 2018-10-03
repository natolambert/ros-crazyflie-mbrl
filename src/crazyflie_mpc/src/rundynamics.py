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

#mean = [42000, 42000, 42000, 42000]
#variance = 20000

#device = torch.device('cpu')
device = torch.device('cuda')
torch.set_default_tensor_type('torch.cuda.FloatTensor')

#norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "2018-07-25_general_temp-normparams.pkl")
# norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/w-200e-100lr-7e-06b-32d-pink_long_hover_cleanp-True-normparams.pkl")
norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/sep12_float/2018-09-12--18-56-18.5--Min error0.0001074432409094537--w=500e=250lr=0.001b=32de=3d=_CONF_p=True--normparams.pkl")

#norms_path_roll = os.path.join(rp.get_path("crazyflie_mpc"), "src", "roll.pkl")
#norms_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "beast-normparams.pkl")
model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/sep12_float/2018-09-12--18-56-18.5--Min error0.0001074432409094537--w=500e=250lr=0.001b=32de=3d=_CONF_p=True.pth")
# model_path = os.path.join(rp.get_path("crazyflie_mpc"), "src", "_models/w-200e-100lr-7e-06b-32d-pink_long_hover_cleanp-True.pth")
#model_path_roll = os.path.join(rp.get_path("crazyflie_mpc"), "src", "roll.pth")


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

  # print(actions)
  # print(actions)
  # print(actions.size())
  # actions[:,0,4:] = prev_action
  # print(actions)
  # quit()
  #print "actions : ", actions
  # Get the desired dimensions
  # current_state_trimmed = torch.zeros(len(state_idx))
  current_state_trimmed = torch.tensor(current_state)
  # for i,idx in enumerate(state_idx):
  #   current_state_trimmed[i] = current_state[idx]
  #print "trimmed : ", current_state_trimmed
  # print('Current state is: ', current_state_trimmed)
  # Create current state vector
  # X = current_state_trimmed.expand(batch_size, -1)

  # For stacked state
  X = torch.tensor(current_state).type(torch.cuda.FloatTensor)
  if printflag: print(X)
  X = X.expand(batch_size, -1)

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

  # normU = actions.sub(Umin)
  # normU.div_(Uscale)

  #Usage for minmaxscaler
  normU = actions.sub(Umin)
  normU.mul_(Uscale)
  normU.sub_(1)     # sub one because scaled (-1,1)

  # normU = ((actions.sub(Umin)).div((Umax.sub(Umin)).mul(Umax.sub(Umin)))).add(Umin)
  # print('Normalized Actions', normU)
  # print('Raw Actions', actions)
  # X_std = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
  # X_scaled = X_std * (max - min) + min
  # Convert them to tensors
  #normX = Variable(torch.Tensor(normX))
  #normU = Variable(torch.Tensor(normU))

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

    if i == 0:
        prev_action.sub_(Umin[:4])
        prev_action.mul_(Uscale[:4])
        prev_action.sub_(1)
        batch[:,4:] = prev_action

    # put states and control together
    #print "normx and batch: ", torch.cat((normX[:,-2:-1], batch), 1)[0]
    #print "normx and batch: ", torch.cat((normX[:,-1:], batch), 1)[0]

    input       = torch.Tensor(torch.cat((normX, batch), 1))
    #input_roll  = Variable(torch.Tensor(torch.cat((normX[:,-1:],   batch), 1)))
    # create prediction
    states  = model(input)

    # Ensure you only take states (makes sure not to take variance if PNN)
    states = states[:,0:len(state_idx)]



    # states = states#[:,0:3]  # probablistc euler only
    # print(states.size())
    # print(dXscale.size())
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

      # print(states)
      #print "states added : ", states
      # renormalize new X
      states.sub_(Xmin[:9]) #[3:6])
      states.div_(Xscale[:9]) #[3:6])

      #print "states final norm : ", states

    # print(normX.size())
    # # normX[:,3:6] = states
    # normX[:,9:] = normX[:,:9]
    # normX[:,:9] = states
    #normX = torch.cat((states, states_roll), 1)5
    #X = normX.clone().detach().cpu().numpy()

    # results[:,i,3:6] = normX[:,3:6]
    results[:,i,:] = normX[:,:9]

  # END FOR LOOP OF T
  # =================

  #results = results.cpu().detach().numpy()dim

  #final_results = torch.empty(results.shape)
  #for i in range(0,len(results)):
    #final_results[i] = scalerX.inverse_transform(results[i])
  #results[:,:,0] = results[:,:,0].mul(Xscale)
  #results[:,:,0] = results[:,:,0].add(Xmin)

  #results[:,:,1] = results[:,:,1].mul(Xscale_roll)
  #results[:,:,1] = results[:,:,1].add(Xmin_roll)
  # print('Pre renorm', results)
  # convert back to unscaled values
  results.mul_(Xscale[:9])
  results.add_(Xmin[:9])
  # print("renormed", results)

  if graph:
      # data = results.cpu().detach().numpy()
      # # print(np.shape(data))
      # ax1 = plt.subplot(211)
      # plt.plot(data[:,:,3])
      # ax1.axhline(current_state_trimmed.cpu().numpy()[3], color='k')
      #
      # ax2 = plt.subplot(212)
      # plt.plot(data[:,:,4])
      # ax2.axhline(current_state_trimmed.cpu().numpy()[4], color='k')
      # plt.show()
      curr = current_state_trimmed.cpu().detach().numpy()
      for traj in results.cpu().detach().numpy():
          # current_state_trimmed
          # plt.figure(0)
          # plt.title('Omega X')
          # plt.plot(traj[:,0], linestyle='--')
          # plt.figure(1)
          # plt.title('Omega Y')
          # plt.plot(traj[:,1], linestyle='--')
          # plt.figure(2)
          # plt.title('Omega Z')
          # plt.plot(traj[:,2], linestyle='--')
          plt.figure(3)
          plt.title('Pitch')
          plt.plot(np.append(curr[3], traj[:,3]), linestyle='--')
          plt.figure(4)
          plt.title('Roll')
          plt.plot(np.append(curr[4], traj[:,4]), linestyle='--')
          # plt.figure(5)
          # plt.title('Yaw')
          # plt.plot(np.append(curr[5], traj[:,5]), linestyle='--')
          # plt.figure(6)
          # plt.title('Lin X')
          # plt.plot(traj[:,6], linestyle='--')
          # plt.figure(7)
          # plt.title('Lin Y')
          # plt.plot(traj[:,7], linestyle='--')
          # plt.figure(8)
          # plt.title('Lin Z')
          # plt.plot(traj[:,8], linestyle='--')
      # plt.show()

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
  # print('looking at obj sizes')
  # print((data_eval[:,:,3].mul(data_eval[:,:,3])).mul(20).mean(dim=0))
  # print((data_eval[:,:,4].mul(data_eval[:,:,4])).mul(20).mean(dim=0))
  # print((data_eval[:,:,6].mul_(data_eval[:,:,6])).mul_(50).mean(dim=0))
  # print((data_eval[:,:,7].mul_(data_eval[:,:,7])).mul_(50).mean(dim=0))
  # print(((data_eval[:,:,8].sub_(10)).mul_(data_eval[:,:,8])).mul_(50).mean(dim=0))
  # print((data_eval[:,1,3].sub_(data_eval[:,0,3])).mul_((data_eval[:,1,3])).mul_(2000).mean(dim=0))
  # print((data_eval[:,1,4].sub_(data_eval[:,0,4])).mul_((data_eval[:,1,4])).mul_(2000).mean(dim=0))
  # print((data_eval[:,1,5].sub_(data_eval[:,0,5])).mul_((data_eval[:,1,5])).mul_(2000).mean(dim=0))
  # print('------------------------')
  # # Minimize values of angular accelerations
  # objective_vals.add_((data_eval[:,:,0].mul_(data_eval[:,:,0])).mul_(.001))
  # objective_vals.add_((data_eval[:,:,1].mul_(data_eval[:,:,1])).mul_(.001))
  objective_vals.add_((data_eval[:,:,2].mul_(data_eval[:,:,2])).mul_(.00001))






  # GOOOOOOOOD DATA VALUES
  # T=1, N=7000, Var = 4000
  # sep10_150_ng3
  # pitch/roll: 1; pitch: sub -.5, roll sub: 1.5
  #lx /ly: 10
  # lz: 100 based from 10
  # NO euler rates




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


  # TODO minimize value of slope of the angles. This is for T=1
  # X is the original state, so slope is going to be (data_eval[:,:,i]-X[i])

  # slope = (data_eval[:,:,3:6].squeeze()).sub(X[:,3:6])
  #
  # # print(slope[:,0].mul(slope[:,0]).mul(15).mean(dim=0))
  # # print(slope[:,2].mul(slope[:,2]).mul(15).mean(dim=0))
  # # print(slope[:,1].mul(slope[:,1]).mul(15).mean(dim=0))
  # # print('----------------------')
  #

  # T=1 Slope code
  objective_vals.squeeze_()
  # objective_vals.add_(slope[:,0].mul_(slope[:,0]).mul_(200))
  # objective_vals.add_(slope[:,1].mul_(slope[:,1]).mul_(200))
  # objective_vals.add_(slope[:,2].mul(slope[:,2]).mul(.1))
  # objective_vals.add_(((data_eval[:,:,4].squeeze()).sub(X[:,4])).mul(((data_eval[:,:,4].squeeze()).sub_(X[:,4]))).mul(10))
  # objective_vals.add_(((data_eval[:,:,5].squeeze()).sub(X[:,5])).mul(((data_eval[:,:,5].squeeze()).sub_(X[:,5]))).mul(10))

  # print((data_eval[:,:,0].mul_(data_eval[:,:,0])).mul_(.01).mul_(.01))
  # print((data_eval[:,:,2].mul_(data_eval[:,:,2])).mul_(.005).mul_(.005))
  # print((data_eval[:,:,3].mul_(data_eval[:,:,3])).mul_(100))
  # print((data_eval[:,1:,3].sub_(data_eval[:,:-1,3])).mul_((data_eval[:,1:,3].sub_(data_eval[:,:-1,3]))).mul_(10))
  # print((data_eval[:,1:,5].sub_(data_eval[:,:-1,5])).mul_((data_eval[:,1:,5].sub_(data_eval[:,:-1,5]))).mul_(5))


  if iters >1: objective_vals = objective_vals.sum(dim=1)

  # mm_idx = torch.argmin(objective_vals)   #switch for real objective function
  mm_idx = np.random.randint(0,batch_size)  #switch for random action selection


  # best_actions = torch.empty((5,4))
  # for s in range(5):
  #     mm_idx = torch.argmin(objective_vals)                         #Since controlling to 0 setpoint
  #     objective_vals[mm_idx] = torch.tensor(9999999999)
  #     # print(actions[mm_idx,0,:4])
  #     best_actions[s,:] = actions[mm_idx,0,:4]
      # print(objective_vals.size())
      # print(mm_idx)

  # print(idxs)
  # plt.show()
  # print(best_actions)
  # quit()
  if graph:
    curr = current_state_trimmed.cpu().detach().numpy()
    best = results.cpu().detach().numpy()[mm_idx,:,:]

    # plt.figure(0)
    # plt.plot(results.cpu().detach().numpy()[mm_idx,:,0], linewidth=5.0, color='r')
    # plt.figure(1)
    # plt.plot(results.cpu().detach().numpy()[mm_idx,:,1], linewidth=5.0, color='r')
    # plt.figure(2)
    # plt.plot(np.append(curr, results.cpu().detach().numpy()[mm_idx,:,2]), linewidth=5.0, color='r')
    plt.figure(3)
    plt.plot(np.append(curr[3], best[:,3]), linewidth=5.0, color='r')
    plt.figure(4)
    plt.plot(np.append(curr[4], best[:,4]), linewidth=5.0, color='r')
    # plt.figure(5)
    # plt.plot(np.append(curr[5], best[:, 5]), linewidth=5.0, color='r')
    plt.show()

  # print(best_actions)
  # best_action = torch.mean(best_actions, dim=0)
  best_action = actions[mm_idx]
  # print(best_action)

  # control = torch.mean(best_actions[1:,:], dim=0)

  control = best_action[0]

  # control = actions[torch.tensor(idx)][0]
  # Result[mm_idx][0] is the 12 state data for the predicted state
  return control, objective_vals[mm_idx]# , results[mm_idx][0]  #Not sure why results is returned here; commented out to see if this is the speed killer
  # return control
