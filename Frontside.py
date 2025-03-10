import streamlit as st
import matplotlib.pyplot as plt
from numpy import arange
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
from random import choice
import Quantum_Key_Distribution_Simulation as qk
st.title("Quantum Key Distribution: The Unbreakable Lock for Secrets")
execution_count: None

st.subheader("Description")

st.write("""
Imagine you want to send a secret message to your best friend.
You lock the message in a special box that only you and your friend can open.
Here’s the magic: if a sneaky spy tries to peek or tamper with the box along the way,
the lock will automatically change or the message will self-destruct,
alerting you that someone tried to snoop.
In other words, the spy gets nothing,
and you immediately know your secret wasn’t safe. 
This idea of a tamper-proof, unbreakable lock is at the heart
of what we’re about to explore.
Now, replace that box and lock with the laws of quantum physics
– this is how Quantum Key Distribution (QKD) works in real life.
Instead of a physical box,
QKD sends information using tiny particles of light (photons) as the “keys.”
Thanks to quantum physics, any attempt to eavesdrop on these photons instantly changes their properties.
It’s like the act of peeking jumbles the lock. 

So if an eavesdropper (often nicknamed “Eve”) tries to intercept the key,
the very act of spying leaves a telltale signal.
The legitimate sender and receiver (let’s call them Alice and Bob)
will notice something’s off and know someone tried to listen in.

The result is ultra-secure communication.
QKD lets Alice and Bob share a secret encryption key with confidence that only they possess it.
If a spy intervenes, the disturbance is detected and the faulty key can be thrown away,
ensuring no information is compromised.
It’s as if their message is protected by an unbreakable quantum lock
that not only keeps intruders out but also reports any break-in attempt.
In simple terms, QKD uses the strange rules of quantum physics to guarantee
that two people can share secrets securely
– a level of security so strong that it’s often called “unconditional,”
relying on nature’s physics rather than tricky math​
. With a quantum key in hand, Alice and Bob can communicate with peace of mind,
knowing their conversation is locked up tight by the fundamental laws of physics –
a new era of secrecy where eavesdroppers are left in the dark.
""")

st.header("Relationship Between Bases and Quantum States in QKD")
st.write("""
In Quantum Key Distribution (QKD), **Bases** and **Quantum States** are 
undamental concepts that ensure secure communication. Here's how they relate:

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
- If the receiver (Bob) uses the **same basis** as the sender (Alice),
the quantum state is measured correctly.
- If the receiver uses a **different basis**, the measurement result is random.
- Matching bases are essential for key generation.
Only when Alice and Bob use the same basis do they retain the corresponding
quantum state as part of the key.
- The randomness of basis selection ensures security.
An eavesdropper (Eve) cannot correctly measure the quantum states without introducing errors.

### 4. **Example in BB84 Protocol**
1. Alice randomly selects a basis and sends a corresponding quantum state.
2. Bob randomly selects a basis to measure the received quantum state.
3. Alice and Bob publicly compare their bases (but not the quantum states).
4. They retain only the quantum states where their bases match and convert them into a binary key.
5. If errors are detected (e.g., due to eavesdropping), they discard the key and start over.
""")

st.title("Quantum Key Distribution Simulation")
cols = ["Red", "Blue", "Green", "Yellow"]
colmap = ListedColormap(cols)
nbits = st.number_input("Number of bits for key", min_value=1, max_value=100, value=10)
eavesdropactive = st.checkbox("Enable eavesdropper")
error_bound = st.slider("Error threshold", min_value=0, max_value=100, value=0)

def plot_arrays(arrays, titles, color_map, ncols=4):
    if not eavesdropactive and titles[0]!="Sender Key":
        del arrays[1]
        del titles[1]
    fig, axes = plt.subplots(len(arrays), 1, figsize=(10, len(arrays)*1.5))
    if len(arrays)==1:
        axes = [axes]
    for ax, array, title in zip(axes, arrays, titles):
        ax.imshow(array.reshape(1, -1), aspect='auto', cmap=color_map, vmin=0, vmax=3)
        ax.set_xticks(arange(len(array)))
        ax.set_yticks([])
        ax.set_title(title)
    plt.legend(handles=[Patch(color=cols[i], label=str(i)) for i in range(ncols)],
               bbox_to_anchor=(1, -0.5), borderaxespad=0, ncol=ncols)
    plt.tight_layout()
    return fig

if st.button("Run Simulation"):
    send_bases, send_states = qk.sendsignal(nbits)
    eavbases, eavstates = qk.eavesdrop(eavesdropactive, send_bases, send_states, nbits)
    rec_bases, rec_states = qk.receive_signal(eavbases, eavstates, nbits)
    errors = qk.recognise_error(send_bases, send_states, rec_bases, rec_states)
    senderkey, receiverkey, key = qk.generate_key(errors, send_bases, send_states, rec_bases, rec_states, error_bound)

    st.header("Bases:")
    st.pyplot(plot_arrays([send_bases, eavbases, rec_bases], ["Sender Bases", "Eavesdropper Bases", "Receiver Bases"], colmap, ncols=2))
    st.header("States:")
    st.pyplot(plot_arrays([send_states, eavstates, rec_states], ["Sender States", "Eavesdropper States", "Receiver States"], colmap))
    st.write(f"Detected  {errors} error"+"s"*(errors!=1))
    if key is not None:
        st.header("Keys:")
        st.pyplot(plot_arrays([senderkey, receiverkey, key], ["Sender Key", "Receiver Key", "Resulting Key"], colmap))
    else:
        st.markdown("### Keys not generated - error rate too high")
        if senderkey is not None:
            st.markdown("#### Sender and Receiver keys generated:")
            st.pyplot(plot_arrays([senderkey, receiverkey], ["Sender Key", "Receiver Key"], colmap))
    
    st.subheader("Sender's Bases and Quantum States")

st.title("Quantum Key Distribution (QKD) Quiz")

st.subheader("Question 1: Bases in QKD")
st.write("In QKD, which of the following are valid bases for measuring quantum states?")
options = ["Rectilinear (+)", "Diagonal (×)", "Circular (○)", "Linear (|)"]
user_answer = st.radio("Select the correct options:", options)

if st.button("Submit Answer for Question 1"):
    if user_answer in ["Rectilinear (+)", "Diagonal (×)"]:
        st.success("Correct! Rectilinear and Diagonal are valid bases in QKD.")
    else:
        st.error("Incorrect. Rectilinear and Diagonal are the valid bases.")

st.subheader("Question 2: Quantum States")
st.write("In the Rectilinear basis, what does the vertical polarization state represent?")
user_input = st.text_input("Enter your answer:")

if st.button("Submit Answer for Question 2"):
    if user_input.lower() in ["1", "one"]:
        st.success("Correct! Vertical polarization represents the binary value 1.")
    else:
        st.error("Incorrect. Vertical polarization represents the binary value 1.")

st.subheader("Question 3: Simulate QKD")
st.write("Choose a basis to measure the quantum state and see the result.")

bases = ["Rectilinear (+)", "Diagonal (×)"]
quantum_states = {
    "Rectilinear (+)": ["Vertical (1)", "Horizontal (0)"],
    "Diagonal (×)": ["Backslash (1)", "Forwardslash (0)"]
}

selected_basis = st.selectbox("Select a basis:", bases)


if st.button("Measure Quantum State"):
    result = choice(quantum_states[selected_basis])
    st.write(f"Measurement Result: {result}")


    if "Vertical" in result or "Backslash" in result:
        st.write("This represents the binary value **1**.")
    else:
        st.write("This represents the binary value **0**.")


    st.subheader("Visualization of Quantum State")
    fig, ax = plt.subplots()


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

    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.grid(True)
    
    st.pyplot(fig)

st.subheader("How did you do?")
st.write("Check your answers above and see if you got them right!")

st.title("Quantum Key Distribution (QKD) Receiver Simulation")

bases = ["Rectilinear (+)", "Diagonal (×)"]
quantum_states = {
    "Rectilinear (+)": ["Vertical (1)", "Horizontal (0)"],
    "Diagonal (×)": ["Backslash (1)", "Forwardslash (0)"]
}

st.subheader("Sender's Data")
st.write("The sender (Alice) has sent the following quantum states:")

sender_bases = [choice(bases) for _ in range(5)]
sender_states = [choice(quantum_states[basis]) for basis in sender_bases]

st.write("**Sender's Bases:**", sender_bases)
st.write("**Sender's Quantum States:**", sender_states)

st.subheader("Receiver's Task")
st.write("Based on the sender's data, predict what the receiver (Bob) will measure.")

st.write("Enter the bases that the receiver will use for measurement:")
receiver_bases = []
for i in range(len(sender_bases)):
    receiver_bases.append(st.selectbox(f"Basis for bit {i+1}:", bases, key=f"basis_{i}"))

if st.button("Simulate Receiver's Measurement"):
    st.subheader("Receiver's Measurement Results")
    receiver_states = []
    for i in range(len(sender_bases)):
        if receiver_bases[i] == sender_bases[i]:
            receiver_states.append(sender_states[i])
        else:
            receiver_states.append(choice(quantum_states[receiver_bases[i]]))

    st.write("**Receiver's Bases:**", receiver_bases)
    st.write("**Receiver's Quantum States:**", receiver_states)
    st.subheader("Check Your Prediction")
    user_prediction = st.text_area("Enter your prediction for the receiver's quantum states (comma-separated):")
    if user_prediction:
        user_prediction = [s.strip() for s in user_prediction.split(",")]
        if user_prediction == receiver_states:
            st.success("Correct! Your prediction matches the receiver's measurement.")
        else:
            st.error("Incorrect. Your prediction does not match the receiver's measurement.")
            st.write("Correct receiver's quantum states:", receiver_states)
st.subheader("How did you do?")
st.write("Check your prediction and see if it matches the receiver's measurement!")
