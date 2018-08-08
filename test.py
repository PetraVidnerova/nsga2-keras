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
        load_config(config_name)
    
    Config.input_shape = NSGA2_Cfg.input_shape 
    Config.noutputs = NSGA2_Cfg.noutputs

    nsga2 = NSGAII(num_objectives=2, mutation_rate=0.1, crossover_rate=1.0)
    
    P = []
    for i in range(20):
        P.append(KerasSolution())

    popsize = 20
    num_generations = 100
    nsga2.run(P, popsize, num_generations)

    
   
