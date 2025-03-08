To use the Quantum-Key-Distribution-Simulation.py script and get strings from the uint8's, lookup each element of output arrays in the dictionaries:
```Python
bases_lookup = {0: "Rectilinear", 1: "Diagonal"}
states_lookup = {0: "vertical", 1: "horizontal", 2: "backslash", 3: "forwardslash"}
```
The same can be done for Quantum_Key_Distribution_Simulation.c

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
