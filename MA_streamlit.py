import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#python3 -m streamlit run main.py

st.title("Quantum Key Distribution Simulation")

tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])
with tab1:
    st.write("You are in tab 1")

with tab2:
    st.write("You are in tab 2")

with tab3:
    st.write("You are in tab 3")

st.header("What is our project about?")
st.subheader("_Brief_ _Summary_:")

st.caption("Hope you enjoy!")


"A simulation of the BB84 quantum key distribution protocol."

"Quantum computing has increasingly entered public awareness, so it is important for people to understand what is actually meant by the terms which are used in media (e.g. quantum cryptography). This is a simplified, interactive, visual representation, focusing on approachability for those unfamiliar with the underlying maths."

"This is a simulation describing the process of two correspondents generating a shared key using quantum mechanical principles in accordance with the BB84 protocol, with an eavesdropper which can be toggled active or inactive."

st.divider()

#with st.container(border=true) -for creating borders
#st.image(os.path.join(os.getcwd(), "static", "BG.jpg"))

col1, col2, col3 = st.columns(3)
with col1:
    st.header("Column 1")

with col2:
    st.header("Column 2")

with col3:
    st.header("Column 3")


pressed = st.button("Press me")
print("First:", pressed)

pressed2 = st.button("Second Button")
print("second:", pressed2)

st.divider()

with st.expander("Expand"):
    st.write("input additional info")

st.divider()

st.title("Potential graphs we can use")

chart_data = pd.DataFrame(
    np.random.randn(20,3),
    columns=['A', 'B', 'C']
)

st.subheader("Area Chart")
st.area_chart(chart_data)

st.subheader("Area Chart")
st.bar_chart(chart_data)

st.subheader("Area Chart")
st.line_chart(chart_data)

st.sidebar.title("Sidebar")
st.sidebar.write("For elements likemsliders, buttons & texts")
sidebar_input = st.sidebar.text_input("Enter something in the sidebar")


