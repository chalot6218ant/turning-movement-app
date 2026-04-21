# --- 2. การคำนวณวิเคราะห์ (ปรับปรุงใหม่เพื่อรองรับ 3 แยก) ---
t_in = np.array([in_n, in_s, in_e, in_w], dtype=float)
t_out = np.array([out_n, out_s, out_e, out_w], dtype=float)

total_in = int(np.sum(t_in))
total_out = int(np.sum(t_out))
diff = int(abs(total_in - total_out))
p_diff = (diff / total_in * 100) if total_in > 0 else 0

# 1. สร้าง Seed Matrix (N, S, E, W)
# กำหนดสัดส่วนเบื้องต้น (Straight: 0.7, Left/Right: 0.15)
seed = np.array([
    [0.0, 0.7, 0.15, 0.15], # จาก N
    [0.7, 0.0, 0.15, 0.15], # จาก S
    [0.15, 0.15, 0.0, 0.7], # จาก E
    [0.15, 0.15, 0.7, 0.0]  # จาก W
])

# 2. บังคับให้ทิศที่เป็น 0 ใน Input มีค่าเป็น 0 ใน Matrix ตลอดกาล
for i in range(4):
    if t_in[i] == 0:
        seed[i, :] = 0  # แถว i (ขาเข้าทิศนั้น) เป็น 0
    if t_out[i] == 0:
        seed[:, i] = 0  # คอลัมน์ i (ขาออกทิศนั้น) เป็น 0

mat = seed.copy()

# 3. เริ่มกระบวนการ Balancing (IPF Method)
if total_in > 0:
    for _ in range(50): # เพิ่มรอบให้ Convergence แม่นยำขึ้น
        # ปรับตาม Row (Inbound)
        row_sums = mat.sum(axis=1)
        row_indices = row_sums > 0
        mat[row_indices] = (mat[row_indices].T * (t_in[row_indices] / row_sums[row_indices])).T
        
        # ปรับตาม Column (Outbound)
        col_sums = mat.sum(axis=0)
        col_indices = col_sums > 0
        mat[:, col_indices] = mat[:, col_indices] * (t_out[col_indices] / col_sums[col_indices])

# ฟังก์ชันดึงค่าไปใช้งาน
def gv(o, d): 
    val = mat[o, d]
    return int(round(val)) if not np.isnan(val) else 0

res = {
    'nl': gv(0, 2), 'nt': gv(0, 1), 'nr': gv(0, 3),
    'sl': gv(1, 3), 'st': gv(1, 0), 'sr': gv(1, 2),
    'el': gv(2, 1), 'et': gv(2, 3), 'er': gv(2, 0),
    'wl': gv(3, 0), 'wt': gv(3, 2), 'wr': gv(3, 1)
}
