#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 21:27:54 (CST) daisuke>

# making a list
list_a = [1, 5, 2, 8, 3, 6, 0, 9, 4, 7]

# printing a list
print ("list_a =", list_a)

# accessing to a value using index
print ("list_a[0] =", list_a[0])
print ("list_a[5] =", list_a[5])
print ("list_a[-2] =", list_a[-2])

# accessing to values using slicing
print ("list_a[2:6] =", list_a[2:6])
print ("list_a[:4] =", list_a[:4])
print ("list_a[3:-4] =", list_a[3:-4])
print ("list_a[:] =", list_a[:])

# copying a value using index
scalar_b = list_a[7]
print ("scalar_b =", scalar_b)

# copying values using slicing
list_c = list_a[1:7]
print ("list_c =", list_c)

# number of elements
n_a = len (list_a)
print ("number of elements of list_a =", n_a)
n_c = len (list_c)
print ("number of elements of list_c =", n_c)

# appending an element to the end of list_c
list_c.append (10)
print ("list_c =", list_c)

# appending list to the end of list
list_c.extend ([50, 20, 30])
print ("list_c =", list_c)

# sorting list
list_d = sorted (list_c)
print ("list_d =", list_d)
