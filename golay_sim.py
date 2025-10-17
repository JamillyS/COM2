import streamlit as st
import komm
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=42)
komm.global_rng.set(rng)

# Parâmetros do sistema
modulador = komm.PSKConstellation(2)
codigo = komm.GolayCode(True)
decodificador = komm.ExhaustiveSearchDecoder(codigo)
fonte = komm.DiscreteMemorylessSource(2)

# Funções principais
def ber_teorico_bpsk(ebn0_linear):
    return komm.gaussian_q(np.sqrt(2 * ebn0_linear))

def simular_ber(ebn0_linear, n_bits=24000):
 
    energia_bit = modulador.mean_energy() / codigo.rate
    sigma = np.sqrt(energia_bit / (2 * ebn0_linear))
    
    bits = fonte.emit(n_bits)
    bits_cod = codigo.encode(bits)
    simbolos = modulador.indices_to_symbols(bits_cod)
    ruido = np.random.normal(scale=sigma, size=len(simbolos))
    recebido = simbolos + ruido
    bits_decod = modulador.closest_indices(recebido)
    bits_final = decodificador.decode(bits_decod)
    
    return np.mean(bits != bits_final)

# Simulação automática
ebn0_db = np.arange(-2, 7)
ebn0_lin = 10 ** (ebn0_db / 10)

ber_cod = [simular_ber(v) for v in ebn0_lin]
ber_nao_cod = [ber_teorico_bpsk(v) for v in ebn0_lin]


# Gráfico
fig, ax = plt.subplots(figsize=(8, 5))
ax.semilogy(ebn0_db, ber_cod, "-or", label="Com Codificação Golay")
ax.semilogy(ebn0_db, ber_nao_cod, "-sb", label="Sem Codificação")
ax.set_xlabel("Eb/N₀ (dB)")
ax.set_ylabel("Taxa de Erro de Bit (BER)")
ax.set_title("BPSK com e sem Codificação Golay")
ax.grid()
ax.legend()
st.pyplot(fig)

