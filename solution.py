from nsga2 import Solution

# imports from GAKeras (add GAKeras directory to PYTHONPATH)
from convindividual import ConvIndividual
from fitness import Fitness
from crossover import CrossoverConv
from mutation import MutationConv

from nsga2_config import NSGA2_Cfg 

fit = Fitness(NSGA2_Cfg.train_name)
crossover = CrossoverConv()
mutation = MutationConv() 


class KerasSolution(Solution):
    ''' Solution of Keras model optimisatio problem.
    
    '''
    
    def __init__(self, network=None):
        '''
        Constructor.
        '''
        Solution.__init__(self, 2)

        if network is None:
            self.network = ConvIndividual()
            self.network.randomInit()
        else:
            self.network = network

        self.uptodate = False
            
        #self.evaluate_solution()

    def set_objectives(self, obj):
        self.objectives = obj
        self.uptodate = True
        
    def evaluate_solution(self):
        '''
        Implementation of method evaluate_solution() as call for GAKeras fitness function.
        '''

        if self.uptodate:
       	   print("UP TO DATE") 
           return 

                
        self.objectives[0] = - fit.evaluate(self.network)[0]

        self.objectives[1] =  self.network.nparams / 1000
                
        self.uptodate = True

        return self.objectives 
        
    def crossover(self, other):
        '''
        Crossover.
        '''
        # cxOnePoint returns two children, get the first one
        child =  crossover.cxOnePoint(self.network, other.network)[0] 
        return KerasSolution(child)
        
    def mutate(self):
        '''
        Mutation.
        '''
        child = mutation.mutate(self.network)
        return KerasSolution(child)

    
