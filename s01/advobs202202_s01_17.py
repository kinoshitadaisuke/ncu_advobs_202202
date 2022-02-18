#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 21:41:39 (CST) daisuke>

# making a dictionary
dic_star_mag = {
    'Sirius': -1.46,
    'Canopus': -0.72,
    'Rigil Kentaurus': -0.27,
    'Arcturus': -0.04,
    'Vega': 0.03,
    'Capella': 0.08,
    'Rigel': 0.12,
    'Procyon': 0.38,
    'Achernar': 0.46,
    'Betelgeuse': 0.50,
}

# printing a dictionary
print (dic_star_mag)

# adding an element
dic_star_mag['Polaris'] = 1.98

# printing a dictionary
print (dic_star_mag)

# accessing an element
print ("visual mag of Betelgeuse =", dic_star_mag['Betelgeuse'])
