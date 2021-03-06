from dopamine.environments import MirrorEnvironment
from dopamine.agents import APIAgent, FQIAgent
from dopamine.experiments import Experiment
from dopamine.adapters import EpsilonGreedyExplorer, BinaryActionSearchAdapter
from dopamine.fapprox import *
import numpy as np

# create agent, environment, renderer, experiment
agent = APIAgent(faClass=LWPRFA, resetFA=True, vectorblock=False)
agent.gamma = 2.
agent.alpha = 1.0
agent.iterations = 1
agent.presentations = 1

environment = MirrorEnvironment()
experiment = Experiment(environment, agent)

# add bas adapter
bas = BinaryActionSearchAdapter(3., 4., 10)
experiment.addAdapter(bas)

# add e-greedy exploration
# explorer = EpsilonGreedyExplorer(0.5, episodeCount=10000)
# experiment.addAdapter(explorer)

# run experiment
valdata = experiment.evaluateEpisodes(1000)
print "mean rewards:", np.mean([sum(e.rewards) for e in valdata]) #, "exploration:", explorer.epsilon
# print "exploration:", explorer.epsilon

experiment.runEpisodes(10000)
agent.learn()    

valdata = experiment.evaluateEpisodes(1000)
print "mean rewards:", np.mean([sum(e.rewards) for e in valdata]) #, "exploration:", explorer.epsilon
