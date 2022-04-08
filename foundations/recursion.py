def mysum(L): 
    print(L)
    if not L: 
        return 0
    else:
        return L[0] + mysum(L[1:])

print(mysum([1, 2, 3, 4, 5]))