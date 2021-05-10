import numpy as np
import math

def restrict(factor,variable):
    newFactor = {}

    for eachFactor in factor.keys():
        if variable in eachFactor: #if the variable is found then we basically replace it from that line of the table(dict)
            newFactorKey = eachFactor.replace(variable,"")
            newFactor[newFactorKey] = factor[eachFactor]

    #printing part
    print("")
