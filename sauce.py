import linecache
import os
import tracemalloc
import sys
from itertools import combinations
import time
import random
import csv

# sys.setrecursionlimit(10**6)

def htop(snapshot, key_type='lineno', limit=3):
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

def printComponents(memoi, capacity, items,values, weights):
    temp = 0
    components = [0] * items
    w = capacity
    res = memoi[items][w]    #0
    for i in range(items, 0, -1): 
        if res < 0:
            break
        if res != memoi[i-1][w]:
            components[i-1] = 1
            res -= values[i-1]
            w = w - weights[i-1]
            temp += values[i-1]
        else:
            continue
    # print('test: {}'.format(temp))
    return components

def f(number, capacity, weights, values): #brute force
    weight_cost = []
    for kas in range(len(weights)):
        kass = (weights[kas], values[kas])
        weight_cost.append(kass)
    best_cost = None
    best_combination = []
    # generating combinations by all ways: C by 1 from n, C by 2 from n, ...
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


def f(num, capacity, w, c):   #top-down approach
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

# def f(num, capacity, w, c): #btm up
    # # memoi = [[0 for x in range(capacity + 1)] for x in range(num + 1)] #dont fucking need this
  
#     for i in range(num + 1): 
#         for j in range(capacity + 1): 
#             if i == 0 or j == 0: 
#                 memoi[i][j] = 0
#             elif w[i-1] <= j:
#                 memoi[i][j] = max(c[i-1] 
#                           + memoi[i-1][j-w[i-1]],   
#                               memoi[i-1][j]) 
#             else: 
#                 memoi[i][j] = memoi[i-1][j]
#     # print(memoi)
#     # tempp = []
#     # for i in range(num+1):
#     #     tempp.append(memoi[i][capacity])
#     # print(tempp)
#     # print(printComponents(memoi, capacity, num, c, w))
#     return memoi[num][capacity] 

# tracemalloc.start()

global nums, capacity, weights, values  #dont fvcking comment this bobo.
weights = []
values = []
with open('./input3.txt', 'r') as file:
    for line in file:
        nums = line.split()
        items = int(nums[0])
        capacity = int(nums[1])
        for i in range(2, len(nums)):
            if i % 2 == 0:
                weights.append(int(nums[i]))
            else:
                values.append(int(nums[i]))
file.close()
'''
Above is reading input from txt file. Instead u can set the value by uncommenting the following lines.
And ofc comment the above lines.
'''
# capacity = 7
# values= [1,4,5,7]
# weights = [1,3,4,5]
# items = 4
# print(values)
memoi = [[0 for x in range(capacity + 1)] for x in range(items + 1)]
print(f(items, capacity, weights, values))


'''
below is using for generating n and W for testing experiment results.
'''
# with open('bruteforce.csv', mode='a') as csvfile:
#     writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     for i in range(1, 1000, 1):
#         tracemalloc.start()
#         weights = []
#         values = []
#         items = i
#         # weights = random(range(0, 70), i)
#         for j in range(i):
#             tmp = random.randint(0, 70)
#             weights.append(tmp)

#         for j in range(i):
#             tmp = random.randint(50, 300)
#             values.append(tmp)
#         capacity = 400
#         start = time.time()
#         for i in range(100):
#             f(items, capacity, weights, values)
#         print(f(items, capacity, weights, values))
#         end = time.time()
#         print('Total time: {}'.format(end-start))
#         snapshot = tracemalloc.take_snapshot()
#         mem = htop(snapshot)
#         writer.writerow([str(items), str(capacity), str(end-start), str(mem)])
#         if end-start > 600:
#             break
    