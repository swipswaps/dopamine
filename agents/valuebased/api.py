from dopamine.agents.agent import Agent, AgentException
from dopamine.agents.valuebased import FQIAgent
from dopamine.agents.valuebased.vblockestimator import VectorBlockEstimator
from dopamine.fapprox import RBF, Linear

from numpy import mean, array, r_, c_, atleast_2d, random, equal
from operator import itemgetter
import time
from random import shuffle

class APIAgent(FQIAgent):
    
    def __init__(self, faClass=Linear, resetFA=True, ordered=False):
        """ initialize the agent with the estimatorClass. """
        FQIAgent.__init__(self, faClass, resetFA, ordered)
    
    def _setup(self, conditions):
        """ if agent is discrete in states and actions create Q-Table. """
        Agent._setup(self, conditions)
        if not (self.conditions['discreteStates'] == False and self.conditions['discreteActions']):
            raise AgentException('FQIAgent expects continuous states and discrete actions. Use adapter or a different environment.')
            
        self.estimator = VectorBlockEstimator(self.conditions['stateDim'], self.conditions['actionNum'], faClass=self.faClass, ordered=self.ordered)
            
    def learn(self):
        """ go through whole episode and make Q-value updates. """  

        for i in range(self.iterations):
            dataset = []
            
            for episode in self.history:
                ret = 0.
                for state, action, reward, nextstate in episode.reversedSamples():
                    qvalue = self.estimator.getValue(state, action)
                    ret += reward
                    target = (1-self.alpha) * qvalue + self.alpha * ret
                    dataset.append([state, action, target])
                    ret *= self.gamma

            if len(dataset) != 0:
                # ground targets to 0 to avoid drifting values
                mintarget = min(map(itemgetter(2), dataset))
                if self.resetFA:
                    self.estimator.reset()
                for i in range(self.presentations):
                    shuffle(dataset)
                    for state, action, target in dataset:
                        self.estimator.updateValue(state, action, target-mintarget)
                self.estimator.train()

