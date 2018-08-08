import random, math
import sys

from solution import KerasSolution
from nsga2 import NSGAII

# import from GAKeras (add GAKeras directory to PYTHONPATH)
from config import Config, load_config  

from nsga2_config import NSGA2_Cfg


if __name__ == '__main__':

    config_name = sys.argv[1] 

    if config_name is not None:
        NSGA2_Cfg.load(config_name)

    # copy attributes from NSGA2_Cfg to Config 
    for key in [attr for attr in dir(NSGA2_Cfg) if not attr.startswith('__')]:
        val = getattr(NSGA2_Cfg, key)
        setattr(Config, key, val)

        
    nsga2 = NSGAII(num_objectives=2, mutation_rate=0.1, crossover_rate=1.0)
    
    P = []
    for i in range(2):
        P.append(KerasSolution())
        
    #TODO: evaluate fitness here 
        
    popsize = 2
    num_generations = 100
    nsga2.run(P, popsize, num_generations)

    
   
