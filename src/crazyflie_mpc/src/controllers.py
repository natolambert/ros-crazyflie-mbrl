# File containing controllers for both collecting data and for on learned dynamics
import numpy as np
# import cvxopt           # convex opt package
import rundynamics as rd
import rundynamics_stacked as rd_stack
# Import models files for MPC controller
import time

class MPController():
    # MPC control, there will be two types
    # 1. random shooting control, with best reward being taken
    # 2. convext optimization solution on finite time horizon

    def __init__(self, equil, N = 100, T=10, variance = .00001, method = 'Shooter',numStack = 1):
        # initialize some variables
        # dynamics learned will be a model from models.py
        # dynamcis true is the dynamics file for getting some parameters
        # rewardORcost is of class Optimizer
        # N is number of random sequences to try
        # T is time horizon

        # time step to be used inthe future when control update rate != dynamics update rate
        self.numStack = numStack

        # time variance of control variable intialization
        self.i = 0
        self.control = equil

        # opt Parameters
        self.method = 'Shooter'         # default to random shooting MPC
        self.time_horiz = T             # time steps into future to look
        self.N = N                      # number of samples to try when random
        self.var = variance

        self.zeros = np.zeros(12)


    def update(self, current_state, last_action, meanAdjust, vbat = 4000., varadj = 1):
        # function that returns desired control output

        # Simulate a bunch of random actions and then need a way to evaluate reward
        N = self.N
        T = self.time_horiz

        control, objectives, pred_state = rd_stack.run_stack(N,T,4, self.control, last_action, vbat, varadj*self.var, current_state, [0,1,2,3,4,5,6,7,8],self.numStack, meanAdjust)

        return control, objectives, pred_state
