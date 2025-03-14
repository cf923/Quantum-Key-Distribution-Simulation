import streamlit as st
import matplotlib.pyplot as plt
from random import choice
import frontend_graphs as fg
st.title("Quantum Key Distribution - BB84 Protocol Simulation")
execution_count: None

about, sim, quiz, source = st.tabs(["About", "Simulation", "Quiz", "Sources & More"])

with about:
    st.header("What is encryption and why should I care about it?")
    
    st.write("""
    If you were told that modern society is built on technology, 
    you would most likely be inclined to agree. 
    We use computers for everything. 
    However, as convenient as that is, 
    it means that your personal data is stored in databases which could, if unprotected, 
    be accessed by anyone knowledgable enough. 
    This data includes not just harmless chat logs but also deeply sensitive information such as bank details or medical information.
    
    One important layer of protection is encryption, 
    which is intended to prevent a malicious third party from making use of your data, 
    in the event that they get their hands on it. 
    The basic idea is that a key is used to encrypt the data, 
    which can then be utilised by the intended user to decrypt and use the data. 
    This is similar to the process of converting a secret message into a cipher, 
    and only allowing the recipient to see the key. 
    
    The security of common classical encryption methods is based on the fact that it would take a normal computer an unfeasible amount of time to break the encryption,
    based on mathematical principles. 
    A quantum computer, however, poses a potential threat to common encryption schemes due to its ability to efficiently break them. 
    (See Shor's algorithm if you want to know more - warning: complicated).
    """)
     
    st.header("Quantum Key Distribution and the BB84 Protocol")
    
    st.write("""
    One approach to making data "quantum-safe",
    i.e. making its encryption sturdy enough to withstand quantum computers (research on which continues to progress rapidly),
    is quantum key distribution (QKD). 
    QKD makes use of quantum mechanical particle-waves like photons - "light particles" - which you will have met in highschool, 
    to detect the presence of an eavesdropper. 
    It does this by making use of wave-function collapse (if you want to know more, the wikipedia page is a good starting point, but I also recommend "Introduction to Quantum Mechanics" by David J. Griffiths),
    which impacts the state of the particle when it is observed. 
    Basically: the message changes whenever it is read, so you would know if someone intercepted your secret message. 
    The following example should make it clearer how this works. 
    
    One of the most fundamental implementations of such a key distribution protocol is the BB84 protocol, which is simulated below.
    To help you understand what is happening, we first have to establish some definitions:
        
    ### 1. **Bases**
    """)
    with st.expander("Click to expand"):
        st.write("""
        Bases are pairs of quantum states which cannot be measured at the same time, they represent the reference frames used to measure certain quantum states.
        Think of this as using different filters in front of your camera, 
        so that only photons that are polarised a certain way make it through. Here, we use the following two bases:
        - **Rectilinear Basis (+ Basis)**:
          - Used to measure vertical (|↑⟩) and horizontal (|→⟩) states.
        - **Diagonal Basis (× Basis)**:
          - Used to measure diagonal states (|↗⟩ and |↖⟩).    
        
        Note that this means you cannot measure a state from another basis if you are not making your measurement in that basis.
        For example, if you measure in the diagonal basis, it is impossible to detect vertical and horizontal states and vice versa. 
        """)
    
    st.write("### 2. **States**")
    with st.expander("Click to expand"):
        st.write("""
        Quantum states are mathematical formulations that tell us about the properties of a system, like its position, momentum and energy. 
        In our case, the states that we are interested in represent how our light is polarised.
        We will also represent these in binary, so that eventually a binary string can be used as a key:
        - In the Rectilinear Basis: 
          - Vertical (|↑⟩) represents **1**.
          - Horizontal (|→⟩) presents **0**.
        - In the Diagonal Basis:
          - Diagonal right (|↗⟩) or Forward slash represents **1**.
          - Diagonal left (|↖⟩) or Backslash represents **0**.
          """)
      
    st.write("### 3. **Relationship Between Bases and Quantum States**")
    with st.expander("Click to expand"):
        st.write("""
        Say a sender (let's call them Alice) randomly selects a list of bases.
        Then for each item in that list ("bit"), they randomly pick one of the two states belonging to the respective basis for that bit. 
        Alice keeps a note of what bases she used and what states she sent. 
        Consider Alice sending individual photons, which are polarised in accordance with the states above (|↑⟩, |→⟩, |↗⟩, |↖⟩).
        Now, when a receiver ("Bob") wants to read the list of states, he has to randomly choose bases to measure them in. 
        Then for each bit:
        - If Alice's and Bob's bases match, Bob measures the same state as that sent by Alice. 
        - If their bases do not match, Bob randomly measures one of the two states associated with his chosen basis. 
        Effectively, this is Bob holding a filter in front of his camera and recording what he detects. 
        This is also the principle behind eavesdropper recognition. 
        
        In particular, the **BB84** protocol functions as follows:
        - Alice sends particles as described above. 
        - An eavesdropper ("Eve") intercepts Alice's particles to spy on the communication. 
        - Eve chooses random bases for her measurements.
        - Whenever her basis matches Alice's, she measures the same state. 
        - When the basis does not match Alice's, the measured state has a 50/50 chance of being either of the states belonging to Eve's chosen basis.
        - Eve passes the particles that she has now measured onto Bob (she cannot make a copy of them due to the no-cloning theorem).
        - Bob makes a measurement of his own, and the following outcomes may occur for each bit:
            1. If Eve chose the same basis as Alice, and Bob chooses that basis too, he will measure the same state as Alice. 
            2. If Eve chose the same basis as Alice, but Bob chooses the other basis, he will randomly measure one of the two states belonging to that basis. 
            3. If Eve chose a different basis compared to Alice, but Bob chooses the same basis as Eve, then he measures the same state as Eve. 
            4. If Eve chose a different basis compared to Alice, and Bob chooses the same basis as Alice, then he has a 50/50 chance of measuring the same state as Alice. 
        
        Notice that in 4., if there was no eavesdropper, it would be impossible for Bob to measure anything but Alice's state. 
        If this does occur, we call this an error. It is a sign that there may be an eavesdropper - in a realistic scenario, there may be other sources of error. 
        Because this process is inherently probabilistic, there is a certain probability of finding the eavesdropper, meaning that if Alice does not send enough bits, 
        there is a chance that they will not detect Eve. 
        """)
        
    st.write("### 4. **The Key**")
    with st.expander("Click to expand"):
        st.write("""
        After Bob has received the bits, Alice and him both publically share the bases they used for their measurements and compare them. 
        They discard the bits in the list of states for which the bases do not match, because these do not offer them any information. 
        For the bits where they did choose the same bases (say this is m bits, where m is an integer), 
        they randomly pick m/2 bits and compare whether their measured states agree.
        If any of them disagree, that indicates an error - possible eavesdropping. 
        If Alice and Bob are satisfied that the amount of errors detected does not surpass a certain threshold, 
        meaning they are reasonably certain their communication is secure,
        they utilise the remaining m/2 bits which they did not disclose to anyone in order to create a key that only they know. 
        For example, this key could be a string of 1s and 0s, used to encode future messages. 
        Of course, this key is limited in length depending on how many bits they sent in the first place and how many were discarded. 
        """)

with sim: 
    st.title("QKD Simulation")
    nbits = st.number_input("Number of bits for key (recommended: 10)", min_value=1, max_value=100, value=10)
    eavesdropactive = st.checkbox("Enable eavesdropper")
    error_bound = st.slider("Error threshold", min_value=0, max_value=100, value=0)
    
    
    if st.button("Run Simulation"):
        fg.run(nbits, eavesdropactive, error_bound)
        
    st.divider()
    
    st.subheader("Simulate a single measurement")
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


        st.subheader("Visual Representation of Quantum State (Not True to Real Life)")
        fig, ax = plt.subplots()


        if "Vertical" in result:
            ax.arrow(0, 0, 0, 1, head_width=0.1, head_length=0.1, fc='blue', ec='blue')
            ax.set_title("Vertical Polarization (1)")
        elif "Horizontal" in result:
            ax.arrow(0, 0, 1, 0, head_width=0.1, head_length=0.1, fc='red', ec='red')
            ax.set_title("Horizontal Polarization (0)")
        elif "Backslash" in result:
            ax.arrow(0, 0, 1, -1, head_width=0.1, head_length=0.1, fc='green', ec='green')
            ax.set_title("Backslash Polarization (1)")
        elif "Forwardslash" in result:
            ax.arrow(0, 0, 1, 1, head_width=0.1, head_length=0.1, fc='purple', ec='purple')
            ax.set_title("Forwardslash Polarization (0)")

        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.grid(True)
        
        st.pyplot(fig)
        
with quiz: 
    st.title("QKD Quiz")
    
    st.subheader("Question 1: Bases")
    st.write("In the context of the BB84 protocol, what is a measurement basis?")
    options1 = ["The core of the quantum computer", "Two quantum states that can be measured simultaneously", "The reason for making the measurement", "A pair of states which can't be measured at the same time"]
    user_answer1 = st.radio("Select the correct option:", options1, key=1)
    
    if st.button("Submit Answer for Question 1"):
        if user_answer1 == "A pair of states which can't be measured at the same time":
            st.success("Correct! It is important that the measurement yields a clear result (not a superposition), which is why the states must not be able to be measured simultaneously.")
        else:
            st.error("Incorrect: A measurement basis is a pair of states which can't be measured at the same time - otherwise, you may measure a mix of states and the protocol does not function as intended.")
    
    st.subheader("Question 2: Quantum States")
    st.write("If Alice makes a measurement in the Rectilinear (+) basis, what states can she measure?")
    options2 = ["Vertical (|↑⟩)", "Diagonal right (|↗⟩)", "Diagonal left (|↖⟩)", "Horizontal (|→⟩)"]
    user_answer2 = st.radio("Select the correct options:", options2, key=2)
    
    if st.button("Submit Answer for Question 2"):
        if user_answer2 in ["Vertical (|↑⟩)", "Horizontal (|→⟩)"]:
            st.success("Correct!")
        else:
            st.error("Incorrect. She can only measure the states which make up that basis, i.e. vertical and horizontal.")
            
    st.subheader("Question 3: Receiver using the same basis")
    st.write("Assume there is no eavesdropper for this question. If Alice uses the (×) basis to send a bit in the state |↖⟩ and Bob chooses to make his measurement in the (×) basis, what does he measure?")
    options3 = ["Vertical (|↑⟩)", "Diagonal right (|↗⟩)", "Diagonal left (|↖⟩)", "Horizontal (|→⟩)"]
    user_answer3 = st.radio("Select the correct options:", options3, key=3)
    
    if st.button("Submit Answer for Question 3"):
        if user_answer3 == "Diagonal left (|↖⟩)":
            st.success("Correct! He cannot measure any states belonging to the rectilinear basis, and since there is no eavesdropper, there is no possibility of him measuring diagonal right.")
        else:
            st.error("Incorrect. Because there is no eavesdropper, he will certainly measure diagonal left. He also can't measure any states of the rectilinear basis.")
            
    st.subheader("How did you do?")
    st.write("Check your answers above and see if you got them right!")

    st.divider()

    st.title("Receiver's Prediction Game")
    
    bases = ["Rectilinear (+)", "Diagonal (×)"]
    quantum_states = {
        "Rectilinear (+)": ["Vertical (1)", "Horizontal (0)"],
        "Diagonal (×)": ["Backslash (1)", "Forwardslash (0)"]
    }
    with st.expander("Click to expand"):
        
        st.subheader("Receiver's Task")
        st.write("Based on the sender's data, predict what the receiver (Bob) will measure.")
        
        st.write("First, enter the bases that the receiver will choose for measurement:")
        receiver_bases = []
        for i in range(5):
            receiver_bases.append(st.selectbox(f"Basis for bit {i+1}:", bases, key=f"basis_{i}"))
        
        st.subheader("Sender's Data")
        st.write("The sender (Alice) has sent the following quantum states:")
        
        @st.cache_data
        def sender_info(bases,states):
            sender_bases = [choice(bases) for _ in range(5)]
            sender_states = [choice(quantum_states[basis]) for basis in sender_bases]
            
            return sender_bases, sender_states
        
        sender_bases, sender_states = sender_info(bases,quantum_states)
        st.write("**Sender's Bases:**", sender_bases)
        st.write("**Sender's Quantum States:**", sender_states)
        
        user_prediction = st.text_area("Use this text box to note down your prediction for the receiver's quantum states:")
        
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
            
        st.subheader("How did you do?")
        st.write("""
        Check your prediction and see if it matches the receiver's measurement! If it does not match, can you see why? Where the bases are not the same, it may just be that you were unlucky in your choice of state!
                 
        If you would like another go, you need to **clear the cache** and reload the page. 
        You can do the former by clicking on the three dots in the upper right corner and selecting Clear cache.
                 
        """)

with source:
    st.subheader("Sources & Further Reading for those interested")
    st.write("""
    1. Singh P, Kaur K. Database security using encryption. In: Proceedings of the 2015 International Conference on Futuristic Trends on Computational Analysis and Knowledge Management (ABLAZE); Greater Noida, India. IEEE; 2015. 353-358. doi: 10.1109/ABLAZE.2015.7155019.
    2. Griffiths DJ, Schroeter DF. Introduction to Quantum Mechanics. 3rd ed. Cambridge: Cambridge University Press; 2018.         
    3. Obloev KH. The Importance of Data Encryption in Information Security. Psixologiya va Sotsiologiya Ilmiy Jurnali. 2024;9: 89-94. 
    4. Scarani V, Bechmann-Pasquinucci H, Cerf NJ et al. The Security of Practical Quantum Key Distribution. Rev. Mod. Phys. 2009;81(3): 1301-1350. https://doi.org/10.48550/arXiv.0802.4155.
    5. Bennett, C. H., & Brassard, G. Quantum Cryptography: Public Key Distribution and Coin Tossing. Theoretical Computer Science. 1984; 560: 7-11. https://doi.org/10.48550/arXiv.2003.06557.
    6. A. Aji, K. Jain and P. Krishnan A Survey of Quantum Key Distribution (QKD) Network Simulation Platforms.  2021 2nd Global Conference for Advancement in Technology (GCAT). 2021. pp. 1-8 doi: 10.1109/GCAT52182.2021.9587708.
    7. Jasim OK, Abbas S, El-Horbaty EM, Salem AM. Quantum key distribution: Simulation and characterizations. Procedia Comput Sci. 2015;65: 701-10. doi: 10.1016/j.procs.2015.09.014.
    8. Adu-Kyere A, Nigussie E, Isoaho J. Quantum Key Distribution: Modeling and Simulation through BB84 Protocol Using Python3. Sensors. 2022; 22(16): 6284. https://doi.org/10.3390/s22166284.
             """)
