import streamlit as st
import komm
import numpy as np
import matplotlib.pyplot as plt

st.title("Códigos de bloco")

filename = "mario.txt"
with open(filename) as f:
    image = []
    for line in f:
        line = [int(x) for x in line.strip()]
        image.append(line)
image = np.array(image)
image = np.kron(image, np.ones((4, 4), dtype=int))

height, width = image.shape

p = st.slider(
    label = "Probabilidade de troca do BSC ($p$)",
    min_value = 0.0,
    max_value = 0.5,
    value=0.08,
)

def plot_bits(bits):
    image_bits = bits.reshape(height, width)
    fig, ax = plt.subplots()
    ax.matshow(image_bits, cmap="binary")
    ax.axis("off")
    st.pyplot(fig)


bsc = komm.BinarySymmetricChannel(p)
u = image.reshape(height*width)

# Não codificado
b_nc = bsc.transmit(u)
# image_b_nc = b_nc.reshape(height*width)

cols = st.columns(2)
with cols[0]:
    plot_bits(u)
with cols[1]:
    plot_bits(b_nc)
    

