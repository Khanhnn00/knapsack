import linecache
import os
import tracemalloc
import sys
from itertools import combinations
import time
import random
import csv

def htop(snapshot, key_type='lineno', limit=3):
    '''
    This function is used for measuring the memory usage of any certain function
    It prints the top 3 lines that consume most memory and return the total memory that function allocated
    '''
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        # replace "/path/to/module/file.py" with "module/file.py"
        filename = os.sep.join(frame.filename.split(os.sep)[-2:])
        print("#%s: %s:%s: %.1f KiB"
              % (index, filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))
    return total/1024

def bruteForce(number, capacity, weights, values): 
    '''
    bruteForce approach to solve knapsack 0/1 problem
    source: https://github.com/madcat1991/knapsack
    Input (from left to right): 
        number of items
        the capacity of the bag
        array contains weight of each item
        array contains value of each item
    Output:
        the maximum value that can be taken
    '''  
    weight_cost = []
    for kas in range(len(weights)):
        kass = (weights[kas], values[kas])
        weight_cost.append(kass)
    best_cost = None
    best_combination = []
    for way in range(number):
        for comb in combinations(weight_cost, way + 1):
            weight = sum([wc[0] for wc in comb])
            cost = sum([wc[1] for wc in comb])
            if (best_cost is None or best_cost < cost) and weight <= capacity:
                best_cost = cost
                best_combination = [0] * number
                for wc in comb:
                    best_combination[weight_cost.index(wc)] = 1
    return best_cost

def topDown(num, capacity, w, c): 
    '''
    top-down approach to solve knapsack 0/1 problem
    Input (from left to right): 
        number of items
        the capacity of the bag
        array contains weight of each item
        array contains value of each item
    Output:
        the maximum value that can be taken
    '''  
    #base case
    if num == 0 or capacity == 0:
        return 0
    
    if memoi[num][capacity] != 0:
        return memoi[num][capacity]

    if w[num-1] > capacity:
        memoi[num][capacity] = f(num-1, capacity, w,c)
        return memoi[num][capacity]
    else:
        memoi[num][capacity] = max(c[num-1] + f(num-1, capacity-w[num-1], w,c), f(num-1, capacity, w,c))
        return memoi[num][capacity]

def btmUp(num, capacity, w, c):
    '''
    bottom-up approach to solve knapsack 0/1 problem
    Input (from left to right): 
        number of items
        the capacity of the bag
        array contains weight of each item
        array contains value of each item
    Output:
        the maximum value that can be taken
    '''
    memoi = [[0 for x in range(capacity + 1)] for x in range(num + 1)] 
  
    for i in range(num + 1): 
        for j in range(capacity + 1): 
            if i == 0 or j == 0: 
                memoi[i][j] = 0
            elif w[i-1] <= j: 
                memoi[i][j] = max(c[i-1] 
                          + memoi[i-1][j-w[i-1]],   
                              memoi[i-1][j]) 
            else: 
                memoi[i][j] = memoi[i-1][j] 
  
    return memoi[num][capacity]

def f(num, capacity, w, v):  #optimized
    '''
    bottom-up approach which is optimized to solve knapsack 0/1 problem
    Input (from left to right): 
        number of items
        the capacity of the bag
        array contains weight of each item
        array contains value of each item
    Output:
        the maximum value that can be taken
    '''
    memoi = [[0 for x in range(capacity + 1)]  
              for x in range(2)]
    for i in range(num): 
        j = 0   
        while j < capacity:
            j += 1
            if w[i] <= j:
                memoi[~(i&1)][j] = max(v[i] + memoi[(i&1)][j - w[i]], memoi[(i&1)][j]) 
            else: 
                memoi[~(i&1)][j] = memoi[(i&1)][j] 
    return memoi

'''
Below is the code we use to conduct experiment on proving time and memory
complexity of each approach
'''
with open('btm_opt_2.csv', mode='w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(100, 1000, 10):
        weights = []
        values = []
        items = i
        # weights = random(range(0, 70), i)
        for j in range(i):
            tmp = random.randint(0, 70)
            weights.append(tmp)

        for j in range(i):
            tmp = random.randint(50, 300)
            values.append(tmp)
        capacity = 1000
        start = time.time()
        tracemalloc.start()
        temp = []
        for k in range(30):
            res = f(items, capacity, weights, values)
            temp.append(res)
        a = f(items, capacity, weights, values)
        end = time.time()
        print('Total time: {}'.format(end-start))
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        mem = htop(snapshot)
        writer.writerow([str(items), str(capacity), str(end-start), str(mem)])
        del(temp)
        if i>500 or int(end-start) > 300:
            break
