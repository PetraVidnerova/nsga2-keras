import sys
import pickle

from multiprocessing import Pool


from dataset import load_data
from config import Config
from utils import error

from nsga2_config import NSGA2_Cfg


def evaluate(ind, X_train, y_train, X_test, y_test):
    network = ind.network.createNetwork()
    
    E_train, E_test = 0, 0
    network.fit(X_train, y_train,
                batch_size=Config.batch_size, epochs=12, verbose=0)

    yy_train = network.predict(X_train)
    E_train = error(yy_train, y_train)
    
    yy_test = network.predict(X_test)
    E_test = error(yy_test, y_test)

    return E_train, E_test 
    


if __name__ == "__main__":

    # load configuration 
    config_name = sys.argv[1]
    if config_name is None:
        raise Exception("no config name") 
    NSGA2_Cfg.load(config_name)

    #load the population
    checkpoint_file = sys.argv[2] 
    if checkpoint_file is None:
        raise Exception("no checkpoint file")
    with open(checkpoint_file, "rb") as f:  
        cp = pickle.load(f)

    pop = cp["population"]

    for i, ind in  enumerate(pop):
        print(i, ":", ind.objectives)


    index = input()
    if index is None:
        raise Exception("no index") 

    ind = pop[int(index)]
    # print individual
    print(ind.objectives)
    print(ind.network)

    
    # load data 
    X_train, y_train = load_data(NSGA2_Cfg.train_name)
    X_test, y_test = load_data(NSGA2_Cfg.test_name)



    def myeval(x):
        return evaluate(ind, X_train, y_train, X_test, y_test)

    N = 10
    p = Pool(N)
    errors = list(p.map(myeval, range(N)))
        
    print(errors)
        
    E_train = sum([x[0] for x in errors]) / N
    E_test = sum([x[1] for x in errors]) / N

    print("E_train: {}".format(E_train))
    print("E_test: {}".format(E_test))

