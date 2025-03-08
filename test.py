import streamlit as st
import numpy as np
import random as rd

st.title("Quantum Key Distribution: The Unbreakable Lock for Secrets")
execution_count: None

st.subheader("Description")


st.write("""
Imagine you want to send a secret message to your best friend. You lock the message in a special box that only you and your friend can open. Here’s the magic: if a sneaky spy tries to peek or tamper with the box along the way, the lock will automatically change or the message will self-destruct, alerting you that someone tried to snoop. In other words, the spy gets nothing, and you immediately know your secret wasn’t safe. 

This idea of a tamper-proof, unbreakable lock is at the heart of what we’re about to explore. Now, replace that box and lock with the laws of quantum physics – this is how Quantum Key Distribution (QKD) works in real life. Instead of a physical box, QKD sends information using tiny particles of light (photons) as the “keys.” Thanks to quantum physics, any attempt to eavesdrop on these photons instantly changes their properties. It’s like the act of peeking jumbles the lock. 

So if an eavesdropper (often nicknamed “Eve”) tries to intercept the key, the very act of spying leaves a telltale signal. The legitimate sender and receiver (let’s call them Alice and Bob) will notice something’s off and know someone tried to listen in.

The result is ultra-secure communication. QKD lets Alice and Bob share a secret encryption key with confidence that only they possess it. If a spy intervenes, the disturbance is detected and the faulty key can be thrown away, ensuring no information is compromised. It’s as if their message is protected by an unbreakable quantum lock that not only keeps intruders out but also reports any break-in attempt. In simple terms, QKD uses the strange rules of quantum physics to guarantee that two people can share secrets securely – a level of security so strong that it’s often called “unconditional,” relying on nature’s physics rather than tricky math​
. With a quantum key in hand, Alice and Bob can communicate with peace of mind, knowing their conversation is locked up tight by the fundamental laws of physics – a new era of secrecy where eavesdroppers are left in the dark.
""")




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





"""
Frontside
Haoqian Jiang
"""
# Define bases and quantum states
RL = "Rectilinear"
DG = "Diagonal"
bases = [RL, DG]
v = "vertical"
h = "horizontal"
b = "backslash"
f = "forwardslash"
RLstates = [v, h]
DGstates = [b, f]

# Error threshold
error_trsh = 0

# Frontend title
st.title("Quantum Key Distribution Simulator")

# Input section
nbits = st.number_input("Enter the number of bits for the key", min_value=1, max_value=10, value=2)
eavesdropactive = st.checkbox("Enable eavesdropper")
error_trsh = st.slider("Set error threshold", min_value=0, max_value=10, value=0)

# Run button
if st.button("Run Simulation"):
    # Call backend functions
    testbases, teststates = sendsignal(RLstates, DGstates, bases, nbits)
    eavbases, eavstates = eavesdrop(eavesdropactive, RLstates, DGstates, bases, testbases, teststates, nbits)
    rectestbases, recteststates = receivesignal(RLstates, DGstates, bases, eavbases, eavstates, nbits)
    testerrors = recognise_error(testbases, teststates, rectestbases, recteststates)
    senderkey, receiverkey, key = generate_key(testerrors, testbases, teststates, rectestbases, recteststates)

    # Display results
    st.subheader("Sender's Bases and Quantum States")
    st.write("Bases:", testbases)
    st.write("Quantum States:", teststates)

    st.subheader("Eavesdropper's Bases and Quantum States")
    st.write("Bases:", eavbases)
    st.write("Quantum States:", eavstates)

    st.subheader("Receiver's Bases and Quantum States")
    st.write("Bases:", rectestbases)
    st.write("Quantum States:", recteststates)

    st.subheader("Error Detection")
    st.write("Number of errors detected:", testerrors)

    st.subheader("Generated Key")
    st.write("Sender's Key:", senderkey)
    st.write("Receiver's Key:", receiverkey)
    st.write("Final Binary Key:", key)

