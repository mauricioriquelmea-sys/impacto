import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. CONFIGURACIÓN ESTRUCTURAL LAB
st.set_page_config(page_title="Structural Lab | Análisis de Impacto", layout="wide", page_icon="🔨")

def main():
    st.title("🔨 ANÁLISIS DE IMPACTO EN VIGAS")
    st.caption("Director de Proyectos Estructurales EIRL | Algorithm-Aided Engineering")
    st.markdown("---")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.header("📋 Parámetros de Entrada")
        
        with st.expander("Propiedades de la Viga", expanded=True):
            L = st.number_input("Luz de la viga (L) [cm]:", value=300.0, step=10.0)
            E = st.number_input("Módulo de Elasticidad (E) [kgf/cm²]:", value=2.1e6, format="%.1e")
            Jx = st.number_input("Inercia de la sección (Ixx) [cm⁴]:", value=5500.0, step=100.0)
            Wx = st.number_input("Módulo de sección (Wx) [cm³]:", value=407.0, step=10.0)

        with st.expander("Condiciones de Impacto", expanded=True):
            Q = st.number_input("Peso de la carga (Q) [kgf]:", value=100.0, step=10.0)
            h_input = st.number_input("Altura de caída (h) [cm]:", value=10.0, step=1.0)

        # CÁLCULOS BASE
        y_est = (Q * L**3) / (48 * E * Jx)
        m_flec = (Q * L) / 4
        sigma_est = m_flec / Wx
        
        # Factor Dinámico Real
        k_din_actual = 1 + np.sqrt(1 + (2 * h_input / y_est))
        sigma_din_actual = sigma_est * k_din_actual

        st.markdown("---")
        st.success("### Resultados del Análisis")
        res_1, res_2 = st.columns(2)
        res_1.metric("Flecha Estática ($y_{est}$)", f"{y_est:.4f} cm")
        res_2.metric("Coef. Dinámico ($K_{din}$)", f"{k_din_actual:.2f}")
        
        st.metric("Tensión Dinámica ($\sigma_{din}$)", f"{sigma_din_actual:,.1f} kgf/cm²")

        if sigma_din_actual > 1400:
            st.error("⚠️ CRÍTICO: Supera límite elástico admisible")

    with col2:
        # --- PARTE SUPERIOR: ESQUEMA TÉCNICO ---
        img_path = "F1.jpg"
        if os.path.exists(img_path):
            st.image(img_path, caption="Esquema: Carga Q en caída libre sobre centro de luz", use_container_width=True)
        
        st.markdown("---")
        st.info("📊 Sensibilidad: Incremento de Carga vs Altura")

        # --- GENERACIÓN DEL GRÁFICO DE IMPACTO ---
        # Rango de alturas de impacto de 0 a h*2 (o 50cm mínimo)
        h_max = max(h_input * 2.5, 30.0)
        h_range = np.linspace(0.001, h_max, 100)
        
        # Función de incremento
        k_range = 1 + np.sqrt(1 + (2 * h_range / y_est))
        sigma_range = sigma_est * k_range

        fig, ax1 = plt.subplots(figsize=(8, 5))

        # Eje para Factor Dinámico
        color = 'tab:blue'
        ax1.set_xlabel('Altura de Impacto h [cm]', fontweight='bold')
        ax1.set_ylabel('Factor Dinámico Kdin', color=color, fontweight='bold')
        ax1.plot(h_range, k_range, color=color, lw=2, label='Evolución Kdin')
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.grid(True, alpha=0.3, ls=':')

        # Eje para Tensión Dinámica (Secundario)
        ax2 = ax1.twinx()
        color = 'tab:red'
        ax2.set_ylabel('Tensión Dinámica σdin [kgf/cm²]', color=color, fontweight='bold')
        ax2.plot(h_range, sigma_range, color=color, ls='--', lw=2, label='Evolución σdin')
        ax2.tick_params(axis='y', labelcolor=color)

        # Punto de operación actual
        ax1.plot(h_input, k_din_actual, 'ko', markersize=8, label='Punto de Diseño')
        ax1.annotate(f'h={h_input}cm', (h_input, k_din_actual), xytext=(5, 5), textcoords='offset points')

        plt.title(f"Comportamiento Dinámico para Q = {Q} kgf", fontsize=12, fontweight='bold')
        fig.tight_layout()
        st.pyplot(fig)

if __name__ == "__main__":
    main()