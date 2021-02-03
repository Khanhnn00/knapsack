# Approaches to solve knapsack 0/1 problem. </br>

Source code contained in **source.py**.</br>
* brute force
* dynamic programming, includes bottom-up and top-down

<dl>
  <dt>In the experiments folder, there are:</dt>
  <dd>bottomup_data.csv: Experiment on time complexity of bottom-up approach.</dd>
  <dd>topdown_data.csv: Experiment on time complexity of top-down approach.</dd>
  <dd>bruteforce.csv: Experiment on time complexity of bruteforce approach.</dd>
  <dd>btm_optimized_memory_compare.csv: Experiment on memory complexity of bottom-up approach with optimization. 
    On the left side, measuring memory allocated with n and W variables both changed. 
    On the right side, measuring memory allocated with n changed and W unchaged.</dd>
</dl>

**Input folder** contains inputs for test cases, format is as below:</br>
* the number of items
* the knapsack capacity
* sequence of weight-cost pairs

**Output folder** contains outputs of according inputs given in **input folder**, format of each file is:</br>
* the best cost value
* sequence of 0/1: if the i-th element of sequence equal to 1 then we take the i-th item to knapsack overwise we don't take the item to knapsack

**cs112.ipynb**: file is used to predict runtime of each approach in different time complexity functions, using linear regression.

    
