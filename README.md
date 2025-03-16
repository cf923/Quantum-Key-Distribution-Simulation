# Quantum Key Distribution Simulation

A simulation of the BB84 quantum key distribution protocol.

Quantum computing has increasingly entered public awareness, so it is important for people to understand what is actually meant by the terms which are used in media (e.g. quantum cryptography). This is a simplified, interactive, visual representation, focusing on approachability for those unfamiliar with the underlying maths.

This is a simulation describing the process of two correspondents generating a shared key using quantum mechanical principles in accordance with the BB84 protocol, with an eavesdropper which can be toggled active or inactive.

---

To use the simulation on your computer, clone the repo, open a terminal, change the directory to where you've cloned, and enter:

```Shell
streamlit run Frontend.py
```

Note that the Simulation tab uses compiled C scripts which you compile yourself.

---

In all simulations but QKDSim.py, bases and states are encoded in the following way:

```Python
bases_lookup = {0: "Rectilinear", 1: "Diagonal"}
states_lookup = {0: "vertical", 1: "horizontal", 2: "backslash", 3: "forwardslash"}
```

(nothing actually uses these dictionaries but you could look up the values produced by the simulation by passing them though the dictionaries)

---
To compile C files for your system:

As an example, Quantum_Key_Distribution_Simulation.c can be compiled as follows:

#### Windows
```Shell
gcc Quantum_Key_Distribution_Simulation.c -o Quantum_Key_Distribution_Simulation.exe
```
Alternatively use VSCode or WSL

#### macOS
```Shell
gcc Quantum_Key_Distribution_Simulation.c -o Quantum_Key_Distribution_Simulation
```

Alternatively use Xcode (CLang)

#### Linux
```Shell
gcc Quantum_Key_Distribution_Simulation.c -o Quantum_Key_Distribution_Simulation
```

The simulations using C expect a binary with no extension, thus if you compile to an exe you must modify the code as such.
The code uses relative paths as your directory structure cannot be magically guessed, but for your system, absolute paths are recommended.
