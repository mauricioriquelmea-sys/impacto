import streamlit as st
import numpy as np
from PIL import Image
import os

# Configuración de Nivel Élite para Structural Lab
st.set_page_config(page_title="Structural Lab | Análisis de Impacto", layout="wide")

def main():
    st.title("🔨 ANÁLISIS DE IMPACTO EN VIGAS DE ACERO")
    st.markdown("Cálculo de factores dinámicos y tensiones por caída de carga.")
    st.markdown("---")

    # Layout de dos columnas estilo ForkLoadsWeb.py
    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.header("📋 Parámetros de Entrada")
        
        with st.expander("Propiedades de la Viga", expanded=True):
            L = st.number_input("Luz de la viga (L) [cm]:", value=300.0, step=10.0)
            E = st.number_input("Módulo de Elasticidad (E) [kgf/cm²]:", value=2.1e6, format="%.1e")
            Jx = st.number_input("Inercia de la sección (Jx) [cm⁴]:", value=5500.0, step=100.0)
            Wx = st.number_input("Módulo de sección (Wx) [cm³]:", value=407.0, step=10.0)

        with st.expander("Condiciones de Impacto", expanded=True):
            Q = st.number_input("Peso de la carga (Q) [kgf]:", value=100.0, step=10.0)
            h = st.number_input("Altura de caída (h) [cm]:", value=10.0, step=1.0)

        if st.button("CALCULAR IMPACTO", type="primary"):
            # 1. Flecha Estática (Carga puntual al centro)
            y_est = (Q * L**3) / (48 * E * Jx)

            # 2. Coeficiente Dinámico (Kdin)
            # Kdin = 1 + sqrt(1 + (2h / y_est))
            k_din = 1 + np.sqrt(1 + (2 * h / y_est))

            # 3. Tensiones (Estática vs Dinámica)
            m_flec = (Q * L) / 4
            sigma_est = m_flec / Wx
            sigma_din = sigma_est * k_din

            # --- PRESENTACIÓN DE RESULTADOS ---
            st.markdown("---")
            st.success("### Resultados del Análisis")
            
            res_1, res_2 = st.columns(2)
            res_1.metric("Flecha Estática ($y_{est}$)", f"{y_est:.4f} cm")
            res_2.metric("Coef. Dinámico ($K_{din}$)", f"{k_din:.2f}")
            
            res_3, res_4 = st.columns(2)
            res_3.metric("Tensión Estática ($\sigma_{est}$)", f"{sigma_est:.1f} kgf/cm²")
            res_4.metric("Tensión Dinámica ($\sigma_{din}$)", f"{sigma_din:,.1f} kgf/cm²")

            if sigma_din > 1400: # Límite de fluencia referencial
                st.error("❌ LA TENSIÓN DINÁMICA SUPERA EL LÍMITE ADMISIBLE")
            else:
                st.info("✅ Tensión dinámica dentro de rangos operativos")

    with col2:
        st.info("💡 Esquema de Carga en Movimiento")
        
        # Carga exclusiva de F1.jpg
        img_path = "F1.jpg"
        if os.path.exists(img_path):
            st.image(img_path, caption="Referencia: Carga Q cayendo desde altura h sobre viga simplemente apoyada")
        else:
            st.warning(f"⚠️ Archivo '{img_path}' no encontrado en el directorio.")
            st.info("Para visualizar el esquema, sube la imagen con el nombre exacto 'F1.jpg'.")

if __name__ == "__main__":
    main()