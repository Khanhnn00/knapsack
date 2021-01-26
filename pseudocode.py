'''
pseudo code for topdown approach

def topDown(weights, values, num_items, capacity):
    if num_items equals to 0 or capacity equals to 0:
        return 0
    end if
    
    if memoi[num_items][capacity] is not 0:
        return memoi[num_items][capacity]
    end if

    if weights[num_items-1] > capacity:
        set memoi[num_items][capacity] to topDown(weights, values, num_items-1, capacity)
        return memoi[num_items][capacity]
    end if

    set memoi[num_items][capacity] to max(values[num_items-1] + topDown(weights, values, num_items-1, capacity - weights[num_items-1]), 
                                            topDown(weights, values, num_items-1, capacity))
    return memoi[num_items][capacity]

in main function:
    generate weights list containing weight of each item 
    generate values list containing value of each item
    num_items = len(weights) = len(values)
    a capacity variable represents the maximum weight of the bag
    a memoi table with size of num_items * capacity, make it global
    print the output of function topDown(weights, values, num_items, capacity)
'''

'''
pseudo code for bottom-up approach

def bottomUp(memoi, weights, values, num_items, capacity):
    for i <- 0 to num_items do:
        for j <- 0 to capacity do:
            if i or j equals to 0 do:
                memoi[i][j] = 0
            else:
                if weights[i-1] > j:
                    set memoi[i][j] to memoi[i-1][j]
                else:
                    set memoi[i][j] to max(values[i-1] + memoi[i-1][j-weights[i-1]], memoi[i-1][j])
                end if
            end if
    return memoi

in main function:
    generate weights list containing weight of each item 
    generate values list containing value of each item
    num_items = len(weights) = len(values)
    a capacity variable represents the maximum weight of the bag
    a memoi table with size of num_items * capacity
    print the output of function bottomUp(memoi, weights, values, num_items, capacity)

'''