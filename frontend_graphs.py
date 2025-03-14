import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
from numpy import arange
import streamlit as st
import Quantum_Key_Distribution_Simulation as qk

cols = ["Red", "Blue", "Green", "Yellow"]
states_bases_list = [["vertical", "horizontal", "backslash", "forwardslash"], ["Rectilinear", "Diagonal"]]
colmap = ListedColormap(cols)

def plot_arrays(arrays, titles, eavesdropactive, color_map, ncols=4):
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
    plt.legend(handles=[Patch(color=cols[i], label=states_bases_list[ncols==2][i]) for i in range(ncols)],
               bbox_to_anchor=(1, -0.5), borderaxespad=0, ncol=ncols)
    plt.tight_layout()
    return fig

def plotkey(key, color_map):
    if len(key)==1:
        key=[key]
    fig, ax = plt.subplots(1, 1, figsize=(10, 0.6))
    ax.imshow(key.reshape(1, -1), aspect='auto', cmap=color_map, vmin=0, vmax=3)
    ax.set_xticks(arange(len(key)))
    ax.set_yticks([])
    ax.set_title("key generated")
    plt.legend(handles=[Patch(color="Red",label=0), Patch(color="Blue",label=1)], bbox_to_anchor=(1, -0.6), borderaxespad=0, ncols=2)
    return fig

def run(nbits, eavesdropactive, error_bound):
    send_bases, send_states = qk.sendsignal(nbits)
    eavbases, eavstates = qk.eavesdrop(eavesdropactive, send_bases, send_states, nbits)
    rec_bases, rec_states = qk.receive_signal(eavbases, eavstates, nbits)
    errors = qk.recognise_error(send_bases, send_states, rec_bases, rec_states)
    senderkey, receiverkey, key = qk.generate_key(errors, send_bases, send_states, rec_bases, rec_states, error_bound)
    st.markdown("x-axes are bits")
    st.header("Bases:")
    st.pyplot(plot_arrays([send_bases, eavbases, rec_bases], ["Sender Bases", "Eavesdropper Bases", "Receiver Bases"], eavesdropactive, colmap, ncols=2))
    st.header("States:")
    st.pyplot(plot_arrays([send_states, eavstates, rec_states], ["Sender States", "Eavesdropper States", "Receiver States"], eavesdropactive, colmap))
    st.write(f"Detected  {errors} error"+"s"*(errors!=1))
    if senderkey is not None:
        st.markdown("#### Sender and Receiver keys generated:")
        st.pyplot(plot_arrays([senderkey, receiverkey], ["Sender Key", "Receiver Key"], eavesdropactive, colmap))
    if key is not None:
        st.pyplot(plotkey(key, colmap))
    if key is None:
        st.markdown("### Keys not generated - error rate too high")
    return
