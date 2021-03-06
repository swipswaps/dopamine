from numpy import ones, ndarray, argmax, where, array, random
from random import choice
import types

from dopamine.agents.valuebased.estimator import Estimator

class TableException(Exception):
    pass
    
class TableEstimator(Estimator):
    
    conditions = {'discreteStates':True, 'discreteActions':True}
    
    def __init__(self, stateNum, actionNum):
        """ initialize with the number of states and actions. the table
            values are all set to zero.
        """
        self.stateNum = stateNum
        self.actionNum = actionNum
        
        self.initialize(0.0)
        self.randomize()
 
    def getBestAction(self, state):
        """ expects a scalar or a list or array with one element. """
        state = self._forceScalar(state)
        bestvalue = max(self.values[state, :])
        return array([choice(where(self.values[state, :] == bestvalue)[0])])
        
    def getValue(self, state, action):
        """ returns the value of the given (state,action) pair. """
        state = self._forceScalar(state)
        action = self._forceScalar(action)
        return self.values[state, action]
        
    def updateValue(self, state, action, value):
        """ sets a new value of the given (state, action) pair. """
        state = self._forceScalar(state)
        action = self._forceScalar(action)
        self.values[state, action] = value

    def initialize(self, value=0.0):
        """ Initialize the whole table with the given value. """
        self.values = ones((self.stateNum, self.actionNum)) * value
    
    def randomize(self):
        self.values = 0.1*random.random(size=self.values.shape)

    def _forceScalar(self, value):
        """ accepts scalars, lists and arrays. scalars are just passed through, while
            lists and arrays must have one single element. that element is passed back
            as a scalar. lists/arrays with more than one element raise an Exception.
        """
        if type(value) in [ndarray, types.ListType]:
            if len(value) > 1:
                raise TableException('TableEstimator accepts only scalars or lists/arrays with one element as state or action.')
            if type(value) == ndarray:
                value = value.item()
            else:
                value = value[0]

        return int(value)
        
    def __str__(self):
        return str(self.values)

    