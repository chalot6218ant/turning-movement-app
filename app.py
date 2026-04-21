import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Turning Movement Diagram", layout="wide")

# --- CSS ขั้นสูงเพื่อเลียนแบบผังวิศวกรรม (Absolute Positioning) ---
st.markdown("""
<style>
    .junction-wrapper {
        display: flex;
        justify-content: center;
        background-color: #f0f2f6;
        padding: 50px;
        border-radius: 20px;
    }
    .junction-container {
        position: relative;
        width: 800px;
        height: 700px;
        background: #fff;
        border: 2px solid #333;
        font-family: 'Courier New', Courier, monospace;
    }
    /* วาดถนนกลางทางแยก */
    .road-h { position: absolute; top: 250px; left: 0; width: 100%; height: 200px; border-top: 3px solid #000; border-bottom: 3px solid #000; }
    .road-v { position: absolute; top: 0; left: 300px; width: 200px; height: 100%; border-left: 3px solid #000; border-right: 3px solid #000; }
    
    /* กล่องตัวเลขเลน (เหมือนใน Excel) */
    .lane-box {
        position: absolute;
        border: 1px solid #000;
        width: 55px;
        height: 35px;
        text-align: center;
        line-height: 35px;
        font-weight: bold;
        background: #fff;
        font-size: 14px;
    }
    /* ลูกศรจราจร */
    .arrow { position: absolute; font-size: 28px; font-weight: bold; color: #000; }
    .road-name { position: absolute; font-weight: bold; font-size: 16px; color: #333; }
    .total-box { position: absolute; font-weight: bold; border: 2px solid #000; padding: 5px 10px; background: #f9f9f9; min-width: 60px; text-align: center; }
    
    /* เข็มทิศ */
    .compass { position: absolute; top: 40px; right: 60px; text-align: center; font-weight: bold; font-size: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Intersection Turning Movement Diagram (Year 2006 AM)")

# --- Sidebar สำหรับกรอกข้อมูลจราจร ---
with st.sidebar:
    st.header("📍 ใส่ข้อมูล PCU/Hr")
    legs = ["North (N)", "South (S)", "East (E)", "West (W)"]
    in_v, out_v = [], []
    for leg in legs:
        st.subheader(f"ทิศ {leg}")
        c1, c2 = st.columns(2)
        v_in = c1.number_input(f"Inbound", min_value=0, value=1000, key=f"v_in_{leg}")
        v_out = c2.number_input(f"Outbound", min_value=0, value=1000, key=f"v_out_{leg}")
        in_v.append(v_in)
        out_v.append(v_out)
    
    st.divider()
    u_p = st.slider("สัดส่วน U-Turn (%)", 0, 10, 2)
    s_p = st.slider("สัดส่วน ตรงไป (%)", 40, 95, 75)

# --- ฟังก์ชันคำนวณ Matrix (Fratar/Growth Method) ---
def calc_tm(inbound, outbound, labels, up, sp):
    n = len(inbound)
    seed = np.ones((n, n)) * ((100-up-sp)/(n-1))
    for i in range(n):
        for j in range(n):
            if i==j: seed[i,j] = up
            elif abs(i-j)==2: seed[i,j] = sp
    in_v, out_v = np.array(inbound, dtype=float), np.array(outbound, dtype=float)
    if in_v.sum()>0: out_v = out_v * (in_v.sum()/out_v.sum())
    m = seed.copy()
    for _ in range(50):
        m = m * (in_v / np.where(m.sum(axis=1)==0, 1, m.sum(axis=1)))[:, np.newaxis]
        m = m * (out_v / np.where(m.sum(axis=0)==0, 1, m.sum(axis=0)))
    return pd.DataFrame(m, index=labels, columns=labels)

# --- ส่วนแสดงผล ---
df = calc_tm(in_v, out_v, legs, u_p, s_p)
N, S, E, W = df.loc[legs[0]], df.loc[legs[1]], df.loc[legs[2]], df.loc[legs[3]]

# วาดผังทางแยก
st.markdown(f"""
<div class="junction-wrapper">
    <div class="junction-container">
        <div class="road-h"></div><div class="road-v"></div>
        <div class="compass">N<br>▲<br>|</div>
        
        <div class="road-name" style="top:120px; left:305px; transform: rotate(-90deg);">ติวานนท์</div>
        <div class="total-box" style="top:50px; left:310px;">{in_v[0]}</div>
        <div class="total-box" style="top:50px; left:410px;">{out_v[0]}</div>
        <div class="lane-box" style="top:210px; left:305px;">{N.iloc[3]:.0f}</div>
        <div class="lane-box" style="top:210px; left:372px;">{N.iloc[1]:.0f}</div>
        <div class="lane-box" style="top:210px; left:438px;">{N.iloc[2]:.0f}</div>
        <div class="arrow" style="top:245px; left:315px;">↴</div>
        <div class="arrow" style="top:245px; left:385px;">↓</div>
        <div class="arrow" style="top:245px; left:455px;">↧</div>

        <div class="road-name" style="bottom:120px; left:305px; transform: rotate(90deg);">แคราย</div>
        <div class="total-box" style="bottom:50px; left:310px;">{in_v[1]}</div>
        <div class="total-box" style="bottom:50px; left:410px;">{out_v[1]}</div>
        <div class="lane-box" style="top:455px; left:305px;">{S.iloc[2]:.0f}</div>
        <div class="lane-box" style="top:455px; left:372px;">{S.iloc[0]:.0f}</div>
        <div class="lane-box" style="top:455px; left:438px;">{S.iloc[3]:.0f}</div>
        <div class="arrow" style="top:420px; left:315px;">↥</div>
        <div class="arrow" style="top:420px; left:385px;">↑</div>
        <div class="arrow" style="top:420px; left:455px;">↱</div>

        <div class="road-name" style="top:325px; left:520px;">งามวงศ์วาน</div>
        <div class="total-box" style="top:260px; left:650px;">{out_v[2]}</div>
        <div class="total-box" style="bottom:260px; left:650px;">{in_v[2]}</div>
        <div class="lane-box" style="top:255px; left:505px;">{E.iloc[0]:.0f}</div>
        <div class="lane-box" style="top:332px; left:505px;">{E.iloc[3]:.0f}</div>
        <div class="lane-box" style="top:410px; left:505px;">{E.iloc[1]:.0f}</div>
        <div class="arrow" style="top:255px; left:465px;">↤</div>
        <div class="arrow" style="top:332px; left:465px;">←</div>
        <div class="arrow" style="top:410px; left:465px;">↵</div>

        <div class="total-box" style="top:260px; left:80px;">{in_v[3]}</div>
        <div class="total-box" style="bottom:260px; left:80px;">{out_v[3]}</div>
        <div class="lane-box" style="top:255px; left:235px;">{W.iloc[1]:.0f}</div>
        <div class="lane-box" style="top:332px; left:235px;">{W.iloc[2]:.0f}</div>
        <div class="lane-box" style="top:410px; left:235px;">{W.iloc[0]:.0f}</div>
        <div class="arrow" style="top:255px; left:275px;">↳</div>
        <div class="arrow" style="top:332px; left:275px;">→</div>
        <div class="arrow" style="top:410px; left:275px;">↦</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.success("✅ คำนวณเสร็จสมบูรณ์: ตัวเลขในกล่องคือปริมาณรถรายเลน (Left | Straight | Right) หน่วยเป็น PCU/Hr.")
