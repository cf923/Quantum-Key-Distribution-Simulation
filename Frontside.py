import streamlit as st
import numpy as np
import random as rd
import matplotlib.pyplot as plt

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


# Explanation of Bases and Quantum States
st.header("Relationship Between Bases and Quantum States in QKD")
st.write("""
In Quantum Key Distribution (QKD), **Bases** and **Quantum States** are fundamental concepts that ensure secure communication. Here's how they relate:

### 1. **Bases**
Bases are reference frames used to measure quantum states. In QKD, two common bases are used:
- **Rectilinear Basis (+ Basis)**:
  - Used to measure vertical (|0⟩) and horizontal (|1⟩) polarization.
- **Diagonal Basis (× Basis)**:
  - Used to measure diagonal polarization (|↗⟩ and |↖⟩).

### 2. **Quantum States**
Quantum states represent the polarization of photons and encode binary information:
- In the Rectilinear Basis:
  - Vertical polarization (|) represents **1**.
  - Horizontal polarization (-)presents **0**.
- In the Diagonal Basis:
  - Diagonal right (|↗⟩) or Forwards slash represents **1**.
  - Diagonal left (|↖⟩) or Backslash represents **0**.

### 3. **Relationship Between Bases and Quantum States**
- If the receiver (Bob) uses the **same basis** as the sender (Alice), the quantum state is measured correctly.
- If the receiver uses a **different basis**, the measurement result is random.
- Matching bases are essential for key generation. Only when Alice and Bob use the same basis do they retain the corresponding quantum state as part of the key.
- The randomness of basis selection ensures security. An eavesdropper (Eve) cannot correctly measure the quantum states without introducing errors.

### 4. **Example in BB84 Protocol**
1. Alice randomly selects a basis and sends a corresponding quantum state.
2. Bob randomly selects a basis to measure the received quantum state.
3. Alice and Bob publicly compare their bases (but not the quantum states).
4. They retain only the quantum states where their bases match and convert them into a binary key.
5. If errors are detected (e.g., due to eavesdropping), they discard the key and start over.
""")

#"""
#Quantum Key Distribution Simulation, WIP

#@author: Alexandra Höhl
#"""

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





#"""
#Frontside
#Haoqian Jiang
#""
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

# Check if key was generated
if not key:
        st.warning("Unable to generate key. Please adjust the number of bits or error threshold.")

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
    
    # Sender state
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Bases:**")
        st.write(testbases)
    
    with col2:
        st.write("**Quantum States:**")
        st.write(teststates)

    st.subheader("Receiver's Bases and Quantum States")

    #Eavesdropper state
    col3, col4 = st.columns(2)
    
    with col3:
        st.write("**Bases:**")
        st.write(eavbases)
    
    with col4:
        st.write("**Quantum States:**")
        st.write(eavstates)

    st.subheader("Receiver's Bases and Quantum States")
    #receiver state
    col5, col6 = st.columns(2)
    
    with col5:
        st.write("**Bases:**")
        st.write(rectestbases)
    
    with col6:
        st.write("**Quantum States:**")
        st.write(recteststates)

    st.subheader("Error Detection")
    st.write("Number of errors detected:", testerrors) 

    # Display Generated Key
    st.subheader("Generated Key")
    col7, col8, col9 = st.columns(3)
    with col7:
        st.write("**Sender's Key:**")
        st.write(senderkey)
    with col8:
        st.write("**Receiver's Key:**")
        st.write(receiverkey)
    with col9:
        st.write("**Final Binary Key:**")
        st.write(key)

        import streamlit as st

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Title
st.title("Quantum Key Distribution (QKD) Quiz")

# Question 1: Multiple Choice
st.subheader("Question 1: Bases in QKD")
st.write("In QKD, which of the following are valid bases for measuring quantum states?")
options = ["Rectilinear (+)", "Diagonal (×)", "Circular (○)", "Linear (|)"]
user_answer = st.radio("Select the correct options:", options)

# Check answer for Question 1
if st.button("Submit Answer for Question 1"):
    if user_answer in ["Rectilinear (+)", "Diagonal (×)"]:
        st.success("Correct! Rectilinear and Diagonal are valid bases in QKD.")
    else:
        st.error("Incorrect. Rectilinear and Diagonal are the valid bases.")

# Question 2: Fill in the Blank
st.subheader("Question 2: Quantum States")
st.write("In the Rectilinear basis, what does the vertical polarization state represent?")
user_input = st.text_input("Enter your answer:")

# Check answer for Question 2
if st.button("Submit Answer for Question 2"):
    if user_input.lower() in ["1", "one"]:
        st.success("Correct! Vertical polarization represents the binary value 1.")
    else:
        st.error("Incorrect. Vertical polarization represents the binary value 1.")

# Question 3: Simulation
st.subheader("Question 3: Simulate QKD")
st.write("Choose a basis to measure the quantum state and see the result.")

# Define bases and quantum states
bases = ["Rectilinear (+)", "Diagonal (×)"]
quantum_states = {
    "Rectilinear (+)": ["Vertical (1)", "Horizontal (0)"],
    "Diagonal (×)": ["Backslash (1)", "Forwardslash (0)"]
}

# User selects a basis
selected_basis = st.selectbox("Select a basis:", bases)

# Simulate measurement
if st.button("Measure Quantum State"):
    # Randomly select a quantum state based on the chosen basis
    result = rd.choice(quantum_states[selected_basis])
    st.write(f"Measurement Result: {result}")

    # Explain the result
    if "Vertical" in result or "Backslash" in result:
        st.write("This represents the binary value **1**.")
    else:
        st.write("This represents the binary value **0**.")

    # Visualization
    st.subheader("Visualization of Quantum State")
    fig, ax = plt.subplots()

    # Draw the quantum state
    if "Vertical" in result:
        ax.arrow(0, 0, 0, 1, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
        ax.set_title("Vertical Polarization (1)")
    elif "Horizontal" in result:
        ax.arrow(0, 0, 1, 0, head_width=0.1, head_length=0.1, fc='red', ec='red')
        ax.set_title("Horizontal Polarization (0)")
    elif "Backslash" in result:
        ax.arrow(0, 0, 1, 1, head_width=0.1, head_length=0.1, fc='green', ec='green')
        ax.set_title("Backslash Polarization (1)")
    elif "Forwardslash" in result:
        ax.arrow(0, 0, 1, -1, head_width=0.1, head_length=0.1, fc='purple', ec='purple')
        ax.set_title("Forwardslash Polarization (0)")

    # Set plot limits and labels
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.grid(True)

    # Display the plot
    st.pyplot(fig)

# Final Feedback
st.subheader("How did you do?")
st.write("Check your answers above and see if you got them right!")

#--------------------------------------------------------------------------------
# Title
st.title("Quantum Key Distribution (QKD) Receiver Simulation")

# Define bases and quantum states
bases = ["Rectilinear (+)", "Diagonal (×)"]
quantum_states = {
    "Rectilinear (+)": ["Vertical (1)", "Horizontal (0)"],
    "Diagonal (×)": ["Backslash (1)", "Forwardslash (0)"]
}

# Sender's data
st.subheader("Sender's Data")
st.write("The sender (Alice) has sent the following quantum states:")

# Randomly generate sender's bases and quantum states
sender_bases = [rd.choice(bases) for _ in range(5)]  # 5 random bases
sender_states = [rd.choice(quantum_states[basis]) for basis in sender_bases]

# Display sender's bases and quantum states
st.write("**Sender's Bases:**", sender_bases)
st.write("**Sender's Quantum States:**", sender_states)

# Receiver's task
st.subheader("Receiver's Task")
st.write("Based on the sender's data, predict what the receiver (Bob) will measure.")

# User inputs for receiver's bases
st.write("Enter the bases that the receiver will use for measurement:")
receiver_bases = []
for i in range(len(sender_bases)):
    receiver_bases.append(st.selectbox(f"Basis for bit {i+1}:", bases, key=f"basis_{i}"))

# Simulate receiver's measurement
if st.button("Simulate Receiver's Measurement"):
    st.subheader("Receiver's Measurement Results")
    receiver_states = []
    for i in range(len(sender_bases)):
        if receiver_bases[i] == sender_bases[i]:
            # If bases match, receiver measures the same state
            receiver_states.append(sender_states[i])
        else:
            # If bases don't match, receiver randomly measures a state
            receiver_states.append(rd.choice(quantum_states[receiver_bases[i]]))

    # Display receiver's results
    st.write("**Receiver's Bases:**", receiver_bases)
    st.write("**Receiver's Quantum States:**", receiver_states)

    # Check if user's prediction is correct
    st.subheader("Check Your Prediction")
    user_prediction = st.text_area("Enter your prediction for the receiver's quantum states (comma-separated):")
    if user_prediction:
        user_prediction = [s.strip() for s in user_prediction.split(",")]
        if user_prediction == receiver_states:
            st.success("Correct! Your prediction matches the receiver's measurement.")
        else:
            st.error("Incorrect. Your prediction does not match the receiver's measurement.")
            st.write("Correct receiver's quantum states:", receiver_states)

# Final Feedback
st.subheader("How did you do?")
st.write("Check your prediction and see if it matches the receiver's measurement!")
