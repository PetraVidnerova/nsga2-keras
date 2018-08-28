'''
@summary: Implementation of the NSGA-II algorithm in Python.
@version: 1.0
@since: 2011-01-07
@author: Marcelo Pita, http://marcelopita.wordpress.com
@contact: marcelo.souza.pita <at> gmail.com
@copyright: Copyright 2011 Marcelo Pita
@license:

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

modified-by Petra Vidnerova, August 2018
'''

import sys, random
import pickle
import datetime 
from multiprocessing import Pool

from nsga2_config import NSGA2_Cfg


class Solution:
    '''
    Abstract solution. To be implemented.
    '''
    
    def __init__(self, num_objectives):
        '''
        Constructor. Parameters: number of objectives. 
        '''
        self.num_objectives = num_objectives
        self.objectives = []
        for _ in range(num_objectives):
            self.objectives.append(None)
        #self.attributes = []
        self.rank = sys.maxsize
        self.distance = 0.0
        
    def evaluate_solution(self):
        '''
        Evaluate solution, update objectives values.
        '''
        raise NotImplementedError("Solution class have to be implemented.")
    
    def crossover(self, other):
        '''
        Crossover operator.
        '''
        raise NotImplementedError("Solution class have to be implemented.")
    
    def mutate(self):
        '''
        Mutation operator.
        '''
        raise NotImplementedError("Solution class have to be implemented.")
    
    def __rshift__(self, other):
        '''
        True if this solution dominates the other (">>" operator).
        '''
        dominates = False
        
        for i in range(len(self.objectives)):
            if self.objectives[i] > other.objectives[i]:
                return False
                
            elif self.objectives[i] < other.objectives[i]:
                dominates = True
        
        return dominates
        
    def __lshift__(self, other):
        '''
        True if this solution is dominated by the other ("<<" operator).
        '''
        return other >> self


def crowded_comparison(s1, s2):
    '''
    Compare the two solutions based on crowded comparison.
    '''
    if s1.rank < s2.rank:
        return 1
        
    elif s1.rank > s2.rank:
        return -1
        
    elif s1.distance > s2.distance:
        return 1
        
    elif s1.distance < s2.distance:
        return -1
        
    else:
        return 0


class NSGAII:
    '''
    Implementation of NSGA-II algorithm.
    '''
    current_evaluated_objective = 0

    def __init__(self, num_objectives, mutation_rate=0.1, crossover_rate=1.0):
        '''
        Constructor. Parameters: number of objectives, mutation rate (default value 10%) and crossover rate (default value 100%). 
        '''
        self.num_objectives = num_objectives
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.pool = Pool(NSGA2_Cfg.processors)
        
        random.seed(64);
        
    def run(self, P, population_size, num_generations):
        '''
        Run NSGA-II. 
        '''

        # get start time 
        start_time = datetime.datetime.now()

        objs = self.pool.map(eval_sol, P)
        for s, o in zip(P, objs):
            s.set_objectives(o)

        
        #for s in P:
        #    s.evaluate_solution()
        
        Q = []
        
        for i in range(num_generations):
            # print objectives 
            for s in P:
                print(s.objectives[0], s.objectives[1])
           
<<<<<<< HEAD
            print("Iteracao ", i)
            sys.stdout.flush()
=======
            print("Iteracao ", i, flush=True)
>>>>>>> 140e4278e2558a0606284bb40f0de98b2797f77f
             
            R = []
            R.extend(P)
            R.extend(Q)
            
            fronts = self.fast_nondominated_sort(R)
            
            del P[:]
            
            for front in fronts.values():
                if len(front) == 0:
                    break
                
                self.crowding_distance_assignment(front);
                P.extend(front)
                
                if len(P) >= population_size:
                    break
            
            self.sort_crowding(P)
            
            if len(P) > population_size:
                del P[population_size:]

            # save P
            cp = dict(population=P, generation=i, rngstate=random.getstate())
            cp_name = "checkpoint_nsga2_{}.pkl".format(NSGA2_Cfg.id)
            with open(cp_name, "wb") as file:
                pickle.dump(cp, file)                 

            total_time = datetime.datetime.now() - start_time
            if total_time > datetime.timedelta(hours=8*24):
                print("Time limit exceeded.")
                return 

                
                
            Q = self.make_new_pop(P)
            
            
    def sort_ranking(self, P):
        for i in range(len(P) - 1, -1, -1):
            for j in range(1, i + 1):
                s1 = P[j - 1]
                s2 = P[j]
                
                if s1.rank > s2.rank:
                    P[j - 1] = s2
                    P[j] = s1
                    
    def sort_objective(self, P, obj_idx):
        for i in range(len(P) - 1, -1, -1):
            for j in range(1, i + 1):
                s1 = P[j - 1]
                s2 = P[j]
                
                if s1.objectives[obj_idx] > s2.objectives[obj_idx]:
                    P[j - 1] = s2
                    P[j] = s1
                    
    def sort_crowding(self, P):
        for i in range(len(P) - 1, -1, -1):
            for j in range(1, i + 1):
                s1 = P[j - 1]
                s2 = P[j]
                
                if crowded_comparison(s1, s2) < 0:
                    P[j - 1] = s2
                    P[j] = s1
                
    def make_new_pop(self, P):
        '''
        Make new population Q, offspring of P. 
        '''
        Q = []
        
        while len(Q) != len(P):
            selected_solutions = [None, None]
            
            while selected_solutions[0] == selected_solutions[1]:
                for i in range(2):
                    s1 = random.choice(P)
                    s2 = s1
                    while s1 == s2:
                        s2 = random.choice(P)
                    
                    if crowded_comparison(s1, s2) > 0:
                        selected_solutions[i] = s1
                        
                    else:
                        selected_solutions[i] = s2
            
            if random.random() < self.crossover_rate:
                child_solution = selected_solutions[0].crossover(selected_solutions[1])
                                
                if random.random() < self.mutation_rate:
                    child_solution = child_solution.mutate()
                    
                #child_solution.evaluate_solution()
                
                Q.append(child_solution)

        objs = self.pool.map(eval_sol, Q)
        for s, o in zip(Q, objs):
            s.set_objectives(o)

        #for s in Q:
        #    s.evaluate_solution()
                
        return Q
        
    def fast_nondominated_sort(self, P):
        '''
        Discover Pareto fronts in P, based on non-domination criterion. 
        '''
        fronts = {}
        
        S = {}
        n = {}
        for s in P:
            S[s] = []
            n[s] = 0
            
        fronts[1] = []
        
        for p in P:
            for q in P:
                if p == q:
                    continue
                
                if p >> q:
                    S[p].append(q)
                
                elif p << q:
                    n[p] += 1
            
            if n[p] == 0:
                fronts[1].append(p)
        
        i = 1
        
        while len(fronts[i]) != 0:
            next_front = []
            
            for r in fronts[i]:
                for s in S[r]:
                    n[s] -= 1
                    if n[s] == 0:
                        next_front.append(s)
            
            i += 1
            fronts[i] = next_front
                    
        return fronts
        
    def crowding_distance_assignment(self, front):
        '''
        Assign a crowding distance for each solution in the front. 
        '''
        for p in front:
            p.distance = 0
        
        for obj_index in range(self.num_objectives):
            self.sort_objective(front, obj_index)
            
            front[0].distance = float('inf')
            front[len(front) - 1].distance = float('inf')
            
            for i in range(1, len(front) - 1):
                front[i].distance += (front[i + 1].distance - front[i - 1].distance)


# auxiliary function
def eval_sol(x):
    return x.evaluate_solution()
