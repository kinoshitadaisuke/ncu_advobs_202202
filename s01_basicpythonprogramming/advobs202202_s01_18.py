#!/usr/pkg/bin/python3.9

# Time-stamp: <2022/02/17 21:46:56 (CST) daisuke>

# making a dictionaries of dictionary
dic_stars = {
    'Sirius': {
        'mag': -1.46,
        'dist': 2.670,
        'sptype': 'A0V',
    },
    'Canopus': {
        'mag': -0.72,
        'dist': 95,
        'sptype': 'A9II',
    },
    'Rigil Kentaurus': {
        'mag': -0.27,
        'dist': 1.339,
        'sptype': 'G2V',
    },
    'Arcturus': {
        'mag': -0.04,
        'dist': 11.26,
        'sptype': 'K1.5III',
    },
    'Vega': {
        'mag': -0.04,
        'dist': 7.68,
        'sptype': 'A0V',
    },
}

# printing dictionary of dictionaries
print (dic_stars)

# accessing to an element
print ("dic_stars['Vega']['dist'] =", dic_stars['Vega']['dist'], "pc")
print ("dic_stars['Canopus']['sptype'] =", dic_stars['Canopus']['sptype'])
