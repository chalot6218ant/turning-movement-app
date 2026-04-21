import streamlit as st
import pandas as pd

st.title("Turning Movement Calculator")

# 1. เลือกประเภททางแยกเพื่อกำหนดโครงสร้าง
junction_type = st.radio("ประเภททางแยก", ["3 แยก (T-Junction)", "4 แยก (Cross-Junction)"], horizontal=True)

# กำหนดขาของทางแยก
if junction_type == "3 แยก (T-Junction)":
    legs = ["North", "East", "West"] # สมมติว่าไม่มี South
else:
    legs = ["North", "East", "South", "West"]

st.subheader("1. ปริมาณรถเข้าแต่ละขา (Inflow)")
inflow_data = {}
for leg in legs:
    inflow_data[leg] = st.number_input(f"รถที่เข้าจากขา {leg}", min_value=0, value=100, key=f"in_{leg}")

st.subheader("2. กำหนดสัดส่วนการเลี้ยว (%)")
# สร้าง Matrix สำหรับกรอกสัดส่วน
turning_ratios = {}

for origin in legs:
    st.write(f"**จากขา {origin} ไปยัง:**")
    cols = st.columns(len(legs))
    ratios = {}
    
    for i, destination in enumerate(legs):
        if origin == destination:
            # ปกติไม่เลี้ยวกลับเข้าขาตัวเอง (U-Turn) ถ้าจะเอาก็แก้ตรงนี้
            ratios[destination] = 0
            cols[i].write(f"{destination}: 0%")
        else:
            ratios[destination] = cols[i].number_input(f"{destination} (%)", min_value=0, max_value=100, value=0, key=f"rt_{origin}_{destination}")
    
    turning_ratios[origin] = ratios

# 3. ส่วนการคำนวณ
if st.button("คำนวณ Turning Movement"):
    results = []
    
    for origin in legs:
        total_in = inflow_data[origin]
        ratios = turning_ratios[origin]
        
        # ตรวจสอบว่ารวม % ได้ 100 หรือไม่ (ป้องกัน Error)
        total_pct = sum(ratios.values())
        
        for destination, pct in ratios.items():
            if total_pct > 0:
                # คำนวณจำนวนรถ: (Inflow * สัดส่วน %) / 100
                volume = (total_in * pct) / 100
            else:
                volume = 0
                
            results.append({
                "From": origin,
                "To": destination,
                "Percentage": f"{pct}%",
                "Calculated Volume": volume
            })

    # แสดงผลเป็น DataFrame
    df_result = pd.DataFrame(results)
    
    # กรองเฉพาะค่าที่ไม่ใช่ 0 เพื่อความสะอาด
    df_display = df_result[df_result["Calculated Volume"] > 0]
    
    st.success("คำนวณสำเร็จ!")
    st.dataframe(df_display)

    # 4. ตรวจสอบ Error เบื้องต้น
    for origin in legs:
        if sum(turning_ratios[origin].values()) != 100 and inflow_data[origin] > 0:
            st.warning(f"⚠️ ขา {origin}: ผลรวมสัดส่วนการเลี้ยวไม่เท่ากับ 100% (รวมได้ {sum(turning_ratios[origin].values())}%)")
