from dopamine.agents.direct.direct import DirectAgent
from dopamine.agents.direct.linear import LinearController
from numpy import *
from numpy.linalg import pinv
from copy import copy

class ReinforceAgent(DirectAgent):
 
    alpha = 10e-1
    sigmadecay = 0.99
                              
    def learn(self):
        # create the derivative of the log likelihoods for each timestep in each episode
        # loglh has the shape of lists (episodes) of lists (timesteps) of arrays of dimensions (s, a)
        
        loglh = []
        for episode in self.history:
            inner_loglh = []
            for s, a, r, ns in episode:
                rl_error = array((a - self.controller.activate(s))).reshape(1, self.conditions['actionDim'])
                inner_loglh.append(self.controller.getDerivative(s, rl_error))
            loglh.append(inner_loglh)
        
        baseline = mean([sum(loglh[ie], axis=0)**2 * mean(e.rewards) for ie, e in enumerate(self.history)], axis=0) / mean([sum(loglh[ie], axis=0)**2 for ie, e in enumerate(self.history)], axis=0)
        gradient = mean([sum(loglh[ie], axis=0) * ((mean(e.rewards) - baseline)) for ie, e in enumerate(self.history)], axis=0)
        
        # update parameters of controller
        # print self.controller.parameters
        self.controller.parameters = self.controller.parameters + self.alpha * gradient.flatten()
        # print self.controller.parameters
        
        # decay exploration variance
        for explorer in self.experiment.explorers:
            explorer.sigma *= self.sigmadecay
        
        