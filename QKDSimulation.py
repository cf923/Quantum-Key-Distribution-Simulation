# -*- coding: utf-8 -*-
"""
Quantum Key Distribution Simulation, WIP

@author: Alexandra Höhl
"""

import numpy as np
import random as rd


# define bases
RL = "Rectilinear" # vertical or horizontal polarisation
DG = "Diagonal" # equivalent to tilting the polarising filter by 45°

bases = [RL,DG]

# define particle states
v = "vertical" # corresponds to 1 in RL basis
h = "horizontal" # corresponds to 0 in RL basis
b = "backslash" # corresponds to 1 in DG basis
f = "forwardslash" # corresponds to 0 in DG basis

RLstates = [v,h]
DGstates = [b,f]

# sender action, randomly generate a message containing nbits (number of bits) bits for the given bases and states
def sendsignal(RLstates, DGstates, bases, nbits):
    senderbases = rd.choices(bases, k = nbits)
    senderstates = []
    for basis in senderbases: 
        if basis == RL: 
            senderstates.append(rd.choice(RLstates))
        elif basis == DG:
            senderstates.append(rd.choice(DGstates))
        else: 
            raise Exception("The input basis is not a valid basis.")
            
    return senderbases, senderstates

testbases,teststates = sendsignal(RLstates, DGstates, bases, 10)

def eavesdrop(eavesdropactive,RLstates,DGstates,bases,senderbases,senderstates,nbits):
    if eavesdropactive: 
        eavesdropperbases = rd.choice(bases, k = nbits)
        eavesdropperstates = []
        if len(eavesdropperbases) != len(senderbases):
            raise Exception("You cannot eavesdrop on a message that is longer or shorter than the one sent.")
        else: 
            for i in range(0,len(eavesdropperbases)):
                if eavesdropperbases[i] == senderbases[i]:
                    eavesdropperstates.append(senderstates[i])
                elif eavesdropperbases[i] != eavesdropperbases[i]:
                    if eavesdropperbases[i] == RL: 
                        eavesdropperstates.append(rd.choice(RLstates))
                    elif eavesdropperbases[i] == DG: 
                        eavesdropperstates.append(rd.choice(DGstates))
                    else: 
                        raise Exception("There is an issue with your eavesdropper bases.")
                        
            return eavesdropperbases, eavesdropperstates
    else:
        return senderbases, senderstates

def receivesignal(eavesdropactive,RLstates,DGstates,bases,senderbases,senderstates, nbits):
    if eavesdropactive == False: 
        receiverbases = rd.choices(bases, k = nbits)
        receiverstates = []
        if len(receiverbases) != len(senderbases):
            raise Exception("You cannot receive a message that is longer or shorter than the one sent.")
        else: 
            for i in range(0,len(receiverbases)): 
                if receiverbases[i] == senderbases[i]: 
                    receiverstates.append(senderstates[i]) 
                elif receiverbases[i] != senderbases[i]:
                    if receiverbases[i] == RL:
                        receiverstates.append(rd.choice(RLstates))
                    elif receiverbases[i] == DG: 
                        receiverstates.append(rd.choice(DGstates))
                    else: 
                        raise Exception("There is an issue with your receiver bases.")
    
    return receiverbases, receiverstates

rectestbases, recteststates = receivesignal(False, RLstates, DGstates, bases, testbases, teststates, 10)

                    
