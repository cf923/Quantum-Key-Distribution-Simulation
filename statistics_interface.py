import subprocess
import matplotlib.pyplot as plt
import streamlit as st
def run():
    process = subprocess.run(['./statistics'], capture_output=True, text=True, check=True)
    output_lines = process.stdout.strip().split('\n')
    no_eavesdropper_vals = [float(x) for x in output_lines[0].split()]
    eavesdropper_vals = [float(x) for x in output_lines[1].split()]
    fig = plt.figure()
    plt.plot(range(len(no_eavesdropper_vals)), no_eavesdropper_vals, label="no eavesdropper")
    plt.plot(range(len(eavesdropper_vals)), eavesdropper_vals, label="with eavesdropper")
    plt.xlabel("number of bits")
    plt.ylabel("percent of keys generated")
    plt.legend(loc='best')
    st.pyplot(fig)
