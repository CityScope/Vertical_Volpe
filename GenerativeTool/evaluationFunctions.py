#IMPORT THIRD PARTY LIBRARIES
import numpy as np

#IMPORT OTHER FILES
from parameters import *

def f_gravity(landUses):
    fitness = 0
    for index,landUse in enumerate(landUses):
        height = index//(nodes_per_floor)
        fitness += height*gravity[land_uses_p[landUse]]
    return fitness

def f_greenspace(landUses):
    fitness = 0
    #fitness = -np.sum(x[0:city_length*city_length*city_length]==1)
    return fitness

def g_nbr_residences(nbr_residences_solution):
    constraint = nbr_of_residences - nbr_residences_solution
    return constraint

def g_nbr_offices(nbr_offices_solution):
    constraint = nbr_of_offices - nbr_offices_solution
    return constraint

def g_nbr_amenities(nbr_amenities_solution):
    constraint = nbr_of_amenities - nbr_amenities_solution
    return constraint

def count_landUses(landUses):
    counter_landUses = {n[0]:0 for n in sorted(land_uses_p.items(), key=lambda kv: kv[0])}
    for land in landUses:
        counter_landUses[land] += 1
    return counter_landUses

