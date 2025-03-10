import streamlit as st, matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
import subprocess
import numpy as np

st.title("Quantum Key Distribution Simulation")
cols = ["Red", "Blue", "Green", "Yellow"]
colmap = ListedColormap(cols)
st.markdown("#### QKD Simulation, n = 10, eavesdropper active, error threshold 0")
st.markdown("""This is an example of using a binary instead of python to run the simulation.
            It would be more useful for computing large values, e.g. statistics,
            as it runs much faster.""")
st.markdown("note this is a proof of concept and not throroughly checked for bugs")
def plot_arrays(arrays, titles, color_map, ncols=4):
    fig, axes = plt.subplots(len(arrays), 1, figsize=(10, len(arrays)*1.5))
    if len(arrays)==1:
        axes = [axes]
    for ax, array, title in zip(axes, arrays, titles):
        ax.imshow(array.reshape(1, -1), aspect='auto', cmap=color_map, vmin=0, vmax=3)
        ax.set_xticks(np.arange(len(array)))
        ax.set_yticks([])
        ax.set_title(title)
    plt.legend(handles=[Patch(color=cols[i], label=str(i)) for i in range(ncols)],
               bbox_to_anchor=(1, -0.5), borderaxespad=0, ncol=ncols)
    plt.tight_layout()
    return fig

if st.button("Run"):
    result = subprocess.run(['/home/cj/IRC/Quantum_Key_Distribution_Simulation'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    lines = output.strip().split('\n')
    vals = [np.array(i.split(), dtype=np.uint8) for i in lines]
    st.header("Bases:")
    st.pyplot(plot_arrays([vals[0], vals[2], vals[4]], ["Sender Bases", "Eavesdropper Bases", "Receiver Bases"], colmap, ncols=2))
    st.header("States:")
    st.pyplot(plot_arrays([vals[1], vals[3], vals[5]], ["Sender States", "Eavesdropper States", "Receiver States"], colmap))
    if len(vals)==9 and vals[8][0]!=5:
        st.header("Keys:")
        st.pyplot(plot_arrays([vals[6], vals[7], vals[8]], ["Sender Key", "Receiver Key", "Resulting Key"], colmap))
    else:
        st.markdown("### Keys not generated - error rate too high")
        if len(vals)>6:
            st.markdown("#### Sender and Receiver keys generated:")
            st.pyplot(plot_arrays([vals[6], vals[7]], ["Sender Key", "Receiver Key"], colmap))