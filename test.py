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
    for i in range(20):
        P.append(KerasSolution())
        
    
    popsize = 20
    num_generations = 10
    nsga2.run(P, popsize, num_generations)

    for ind in P:
        print(ind.objectives[0], ind.objectives[1])
   
