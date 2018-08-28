import sys
import matplotlib.pyplot as plt

filename = sys.argv[1]
assert filename is not None


with open(filename, 'r') as f:
    f1 = []
    f2 = [] 
    best = [] 
    mean = []
    for line in f:
        if line.startswith("Iteracao"):
            best.append(min(f1))
            mean.append(sum(f1)/len(f1))
            f1 = []
            f2 = []
        else:
            a1, a2 = line.split(' ')
            f1.append(float(a1))
            f2.append(float(a2))


fig, ax = plt.subplots(2)

ax[0].set_title("Best fitness")
ax[1].set_title("Mean fitness")

ax[0].plot(range(len(best)), best)
ax[1].plot(range(len(best)), mean)
plt.show()


    


    
