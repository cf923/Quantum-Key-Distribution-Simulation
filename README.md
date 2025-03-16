# Quantum Key Distribution Simulation
A simulation of the BB84 quantum key distribution protocol.

Quantum computing has increasingly entered public awareness, so it is important for people to understand what is actually meant by the terms which are used in media (e.g. quantum cryptography). This is a simplified, interactive, visual representation, focusing on approachability for those unfamiliar with the underlying maths.

This is a simulation describing the process of two correspondents generating a shared key using quantum mechanical principles in accordance with the BB84 protocol, with an eavesdropper which can be toggled active or inactive.
---
To use the simulation on your computer, download Frontend.py, open a terminal, change the directory to where you've saved Frontend.py and enter 
```Shell
streamlit run Frontend.py
```
---
To use the Quantum-Key-Distribution-Simulation.py script and get strings from the uint8's, lookup each element of output arrays in the dictionaries:
```Python
bases_lookup = {0: "Rectilinear", 1: "Diagonal"}
states_lookup = {0: "vertical", 1: "horizontal", 2: "backslash", 3: "forwardslash"}
```
The same can be done for Quantum_Key_Distribution_Simulation.c

Replace <Quantum_Key_Distribution_Simulation_binary_location> with the absolute path to the compiled C script.

To compile Quantum_Key_Distribution_Simulation.c for your system:

#### Windows
```Shell
gcc Quantum-Key-Distribution-Simulation.c -o Quantum-Key-Distribution-Simulation.exe
```
Alternatively use VSCode or WSL

#### macOS
```Shell
gcc Quantum-Key-Distribution-Simulation.c -o Quantum-Key-Distribution-Simulation
```

Alternatively use Xcode (CLang)

#### Linux
```Shell
gcc Quantum-Key-Distribution-Simulation.c -o Quantum-Key-Distribution-Simulation.o
```
