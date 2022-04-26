#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 16:35:31 (CST) daisuke>

# importing math module
import math

# magnitude of standard star
m_std = 13.55

# flux of standard star
F_std = 730000

# flux of target object
F_obj = 6500

# calculation of magnitude of target object
m_obj = m_std - 2.5 * math.log10 (F_obj / F_std)

# printing result
print ("flux of standard star      = %f ADU/sec" % F_std)
print ("flux of target object      = %f ADU/sec" % F_obj)
print ("magnitude of standard star = %f mag" % m_std)
print ("magnitude of target object = %f mag" % m_obj)
