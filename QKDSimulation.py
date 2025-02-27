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

# define error threshold above which key generation is aborted
error_trsh = 0

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



def eavesdrop(eavesdropactive, RLstates, DGstates, bases, senderbases, senderstates,nbits):
    if eavesdropactive: 
        eavesdropperbases = rd.choices(bases, k = nbits)
        eavesdropperstates = []
        if len(eavesdropperbases) != len(senderbases):
            raise Exception("You cannot eavesdrop on a message that is longer or shorter than the one sent.")
            
        else: 
            for i in range(0,len(eavesdropperbases)):
                if eavesdropperbases[i] == senderbases[i]:
                    eavesdropperstates.append(senderstates[i])
                elif eavesdropperbases[i] != senderbases[i]:
                    if eavesdropperbases[i] == RL: 
                        eavesdropperstates.append(rd.choice(RLstates))
                    elif eavesdropperbases[i] == DG: 
                        eavesdropperstates.append(rd.choice(DGstates))
                    else: 
                        raise Exception("There is an issue with your eavesdropper bases.")                        
        return eavesdropperbases, eavesdropperstates
    
    else:
        return senderbases, senderstates

def receivesignal(RLstates, DGstates, bases, eavesdropperbases, eavesdropperstates, nbits):
    receiverbases = rd.choices(bases, k = nbits)
    receiverstates = []
    if len(receiverbases) != len(eavesdropperbases):
        raise Exception("You cannot receive a message that is longer or shorter than the one sent.")
        
    else: 
        for i in range(0,len(receiverbases)): 
            if receiverbases[i] == eavesdropperbases[i]: 
                receiverstates.append(eavesdropperstates[i]) 
            elif receiverbases[i] != eavesdropperbases[i]:
                if receiverbases[i] == RL:
                    receiverstates.append(rd.choice(RLstates))
                elif receiverbases[i] == DG: 
                    receiverstates.append(rd.choice(DGstates))
                else: 
                    raise Exception("There is an issue with your receiver bases.")
    
    return receiverbases, receiverstates

def recognise_error(senderbases,senderstates,receiverbases,receiverstates):
    errors = 0
    for i in range(0,len(senderbases)):
        if senderbases[i]==receiverbases[i] and senderstates[i] != receiverstates[i]:
            errors += 1
        else:
            continue
    if errors > 0: 
        print("Eavesdropper detected: ", errors, " errors")
        
    return errors

def generate_key(errors,senderbases,senderstates,receiverbases,receiverstates):
    senderkey = []
    receiverkey =[]
    key = []
    if errors > error_trsh:
        print("No key was generated due to the error count exceeding the threshold value.")
        return  senderkey, receiverkey, key
        
    else: 
        for i in range(0,len(senderbases)):
            if senderbases[i]==receiverbases[i]:
                senderkey.append(senderstates[i])
                receiverkey.append(receiverstates[i]) # these keys should be the same, otherwise error threshold too high. 
                
            else: 
                continue
        
        if senderkey == receiverkey: # this bit behaves a bit peculiarly if I try to make it more compact unfortunately.
            for word in senderkey: # convert strings into 1s and 0s for key
                
                if word == 'vertical':
                    key.append(1)
                    continue
                
                elif word == "backslash":
                    key.append(1)
                    continue
                
                elif word == 'horizontal':
                    key.append(0)
                    continue
                
                elif word == 'forwardslash':
                    key.append(0)
                    continue
                
        
    if senderkey == [] or receiverkey == []: 
        print("No key could be established because there were no matching bases or the error threshold is too high.")
        return senderkey, receiverkey, key
    
    else: 
        return senderkey, receiverkey, key
    
# testing below
testbases, teststates = sendsignal(RLstates, DGstates, bases, 10)
eavbases, eavstates = eavesdrop(False, RLstates, DGstates, bases, testbases, teststates, 10)
rectestbases, recteststates = receivesignal(RLstates, DGstates, bases, eavbases, eavstates, 10)
testerrors = recognise_error(testbases, teststates, rectestbases, recteststates)
senderkey, receiverkey, key = generate_key(testerrors, testbases, teststates, rectestbases, recteststates)



                    
