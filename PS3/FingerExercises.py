def findAnEven(L):
    for i in L:
        if i % 2 == 0:
            return i
    raise ValueError('L does not contain an even number')
print(findAnEven([1, 3, 5, 7]))