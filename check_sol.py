import sys
import pickle

# this is from GAKeras
from utils import error
from dataset import load_data

def train_and_eval_solution(s, X_train, y_train, X_test, y_test):

    network = s.network.createNetwork()
    E_train, E_test = 0, 0

    network.fit(X_train, y_train,
                batch_size = 128, epochs=10, verbose=0)

    yy_train = network.predict(X_train)
    E_train = error(yy_train, y_train)

    yy_test = network.predict(X_test)
    E_test = error(yy_test, y_test)

    return E_train, E_test
    

if __name__ == '__main__':

    train_name = "digits.train"
    test_name = "digits.train"

    X_train, y_train = load_data("data/"+train_name)
    X_test, y_test = load_data("data/"+test_name)
    
    checkpoint = sys.argv[1]

    # load checkpoint
    with open(checkpoint, "rb") as file:
        cp = pickle.load(file)

    P = cp["population"]

    for s in P:
        E_train, E_test = train_and_eval_solution(s, X_train, y_train, X_test, y_test)
        print(s.objectives[0], s.objectives[1], E_train, E_test)
    
