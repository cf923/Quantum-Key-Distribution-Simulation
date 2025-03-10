import streamlit as st, matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap
from numpy import arange
import Quantum_Key_Distribution_Simulation as qk

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

if st.button("Run"):
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
