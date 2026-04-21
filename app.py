import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Turning Movement Analysis", layout="wide")

st.title("📊 Turning Movement Analysis with Diagram")

# --- 1. Sidebar ---
with st.sidebar:
    st.header("📍 ตั้งค่าทางแยก")
    j_type = st.radio("ประเภททางแยก", ["4 แยก", "3 แยก"])
    legs = ["North (N)", "South (S)", "East (E)", "West (W)"] if j_type == "4 แยก" else ["North (N)", "South (S)", "East (E)"]
    
    inbound, outbound = [], []
    for leg in legs:
        st.subheader(f"ทิศ {leg}")
        c1, c2 = st.columns(2)
        v_in = c1.number_input(f"In", min_value=0, value=1000, key=f"i_{leg}")
        v_out = c2.number_input(f"Out", min_value=0, value=1000, key=f"o_{leg}")
        inbound.append(v_in)
        outbound.append(v_out)

    u_pct = st.slider("U-Turn (%)", 0, 20, 2)
    s_pct = st.slider("ตรงไป (%)", 40, 90, 70)

# --- 2. Logic ---
def calculate_tmc(in_f, out_f, labels, u_p, s_p):
    n = len(in_f)
    seed = np.ones((n, n)) * ((100 - s_p - u_p) / (n - 1 if n > 1 else 1))
    for i in range(n):
        for j in range(n):
            if i == j: seed[i,j] = u_p
            elif abs(i-j) == 2 or (n==4 and abs(i-j)==2): seed[i,j] = s_p
    in_f, out_f = np.array(in_f, dtype=float), np.array(out_f, dtype=float)
    if in_f.sum() != out_f.sum(): out_f = out_f * (in_f.sum() / out_f.sum())
    matrix = seed.copy()
    for _ in range(100):
        matrix = matrix * (in_f / np.where(matrix.sum(axis=1)==0, 1, matrix.sum(axis=1)))[:, np.newaxis]
        matrix = matrix * (out_f / np.where(matrix.sum(axis=0)==0, 1, matrix.sum(axis=0)))
    return pd.DataFrame(matrix, index=labels, columns=labels)

# --- 3. Diagram Function ---
def draw_diagram(df):
    fig = go.Figure()
    # พิกัดจำลองของทิศ N, S, E, W
    pos = {"North (N)": [0, 1], "South (S)": [0, -1], "East (E)": [1, 0], "West (W)": [-1, 0]}
    
    for i, start in enumerate(df.index):
        for j, end in enumerate(df.columns):
            val = df.iloc[i, j]
            if val > 0:
                p1, p2 = pos[start], pos[end]
                # วาดเส้นลูกศร
                fig.add_trace(go.Scatter(
                    x=[p1[0], p2[0]*0.7], y=[p1[1], p2[1]*0.7],
                    mode='lines+markers',
                    line=dict(width=val/100 if val > 100 else 1, color='royalblue'),
                    name=f"{start} -> {end}",
                    hoverinfo='text',
                    text=f"{start} ไป {end}: {val:.0f} คัน"
                ))
    
    fig.update_layout(title="ผังจำลองการเลี้ยว (Movement Diagram)", showlegend=False,
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      height=500, margin=dict(l=20, r=20, t=40, b=20))
    return fig

# --- 4. Main Display ---
if st.button("🚀 คำนวณและวาด Diagram"):
    df = calculate_tmc(inbound, outbound, legs, u_pct, s_pct)
    
    # ส่วนของ Diagram
    st.subheader("📍 Movement Diagram")
    st.plotly_chart(draw_diagram(df), use_container_width=True)
    
    st.divider()
    st.subheader("✅ ผลการคำนวณแยกตามรายขาเข้า")
    for i, origin in enumerate(legs):
        with st.container():
            st.markdown(f"#### 📍 จากทิศทาง: **{origin}**")
            cols = st.columns(len(legs) + 1)
            total_row = 0
            for j, dest in enumerate(legs):
                val = df.iloc[i, j]
                total_row += val
                cols[j].metric("U-Turn" if origin == dest else f"ไป {dest}", f"{val:.0f}")
            cols[-1].metric("รวมขาเข้า", f"{total_row:.0f}")
            st.divider()
