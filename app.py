import streamlit as st
import pandas as pd

# --- 1. SETUP: ตั้งค่าหน้าจอแบบ WIDE และ Global Theme ---
st.set_page_config(
    page_title="TechMatch Global",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONNECT DATABASE (GOOGLE SHEETS) ---
@st.cache_data(ttl=60) # อัปเดตข้อมูลทุก 60 วินาที
def load_data():
    # 👇👇👇 เอาลิงก์ CSV จาก Google Sheets มาวางทับตรงนี้ (ในฟันหนู) 👇👇👇
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv" 
    # 👆👆👆 (เช่น "https://docs.google.com/.../pub?output=csv")
    
    try:
        df = pd.read_csv(sheet_url)
        return df
    except Exception as e:
        return pd.DataFrame()

# --- 3. GLOBAL STYLE: แต่งหน้าตาให้ดูอินเตอร์ (Dark & Gold) ---
st.markdown("""
<style>
    /* พื้นหลังสีเข้ม ดู Pro */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
        font-family: 'Inter', sans-serif;
    }
    
    /* การ์ดสินค้า */
    .product-card {
        background-color: #1F2937;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #374151;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .product-card:hover {
        transform: scale(1.02);
        border-color: #F59E0B; /* สีทอง Amazon */
    }
    
    /* ตัวหนังสือเน้นสี */
    .highlight {
        color: #3B82F6; /* สีฟ้า */
        font-weight: 800;
    }
    
    /* ปุ่มกดสไตล์ Amazon */
    .amazon-btn {
        background: linear-gradient(to bottom, #f7dfa5, #f0c14b);
        border-color: #a88734 #9c7e31 #846a29;
        color: #111;
        padding: 10px 20px;
        border-radius: 3px;
        text-align: center;
        font-weight: bold;
        text-decoration: none;
        display: block;
        margin-top: 10px;
    }
    .amazon-btn:hover {
        background: linear-gradient(to bottom, #f5d78e, #eeb933);
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR: แผงควบคุม (ภาษาอังกฤษ) ---
with st.sidebar:
    st.title("🌎 TechMatch")
    st.caption("Global Gadget Finder")
    st.write("---")
    
    st.header("🎚️ Your Priorities")
    w_perf = st.slider("🚀 Performance (Gaming/Work)", 1, 10, 8)
    w_cam = st.slider("📸 Camera Quality", 1, 10, 8)
    w_batt = st.slider("🔋 Battery Life", 1, 10, 5)
    w_val = st.slider("💰 Value for Money", 1, 10, 6)
    
    st.write("---")
    if st.button("🔄 Refresh Data"):
        load_data.clear()
        st.rerun()

# --- 5. MAIN CONTENT: พื้นที่แสดงผล ---
st.title("Find the Perfect Device for YOU.")
st.markdown("### Data-Driven Recommendations. No Bias.")
st.divider()

# โหลดข้อมูล
df = load_data()

if not df.empty:
    # --- LOGIC คำนวณคะแนน ---
    df['score_raw'] = (df['performance'] * w_perf) + \
                      (df['camera'] * w_cam) + \
                      (df['battery'] * w_batt) + \
                      (df['value'] * w_val)
    
    max_possible = (10*w_perf) + (10*w_cam) + (10*w_batt) + (10*w_val)
    df['match_percent'] = (df['score_raw'] / max_possible) * 100
    
    # เรียงลำดับ (มากไปน้อย)
    df = df.sort_values(by='match_percent', ascending=False).reset_index(drop=True)
    winner = df.iloc[0]

    # แบ่งหน้าจอ ซ้าย-ขวา
    col1, col2 = st.columns([2, 1.5])
    
    # --- ส่วนแสดงผลผู้ชนะ (Winner) ---
    with col1:
        st.markdown(f"<h2 class='highlight'>🏆 TOP PICK: {winner['match_percent']:.0f}% Match</h2>", unsafe_allow_html=True)
        
        with st.container():
            c1, c2 = st.columns([1, 1])
            with c1:
                try:
                    st.image(winner['image'], use_container_width=True)
                except:
                    st.warning("Image not found")
            with c2:
                st.subheader(winner['name'])
                st.metric("Estimated Price", f"${winner['price']:,}") # แสดงราคาเป็น USD
                
                st.write("📊 **Key Specs:**")
                st.progress(int(winner['performance']*10), text="Performance")
                st.progress(int(winner['camera']*10), text="Camera")
                
                # ปุ่มไป Amazon
                st.markdown(f"""
                    <a href="{winner['link']}" target="_blank" style="text-decoration:none;">
                        <div class="amazon-btn">
                            🛒 Check Price on Amazon
                        </div>
                    </a>
                """, unsafe_allow_html=True)

    # --- ส่วนแสดงผลตัวรอง (Runners-up) ---
    with col2:
        st.subheader("🥈 Runners-up")
        for i, row in df.iloc[1:].iterrows():
            st.markdown(f"""
            <div class="product-card">
                <div style="display:flex; justify-content:space-between;">
                    <b>{row['name']}</b>
                    <span style="color:#3B82F6; font-weight:bold;">{row['match_percent']:.0f}%</span>
                </div>
                <div style="font-size:0.9em; color:#CCC; margin-bottom:5px;">Est. Price: ${row['price']:,}</div>
                <a href="{row['link']}" target="_blank" style="color:#F59E0B; text-decoration:none; font-weight:bold;">
                    View Deal >
                </a>
            </div>
            """, unsafe_allow_html=True)

else:
    # กรณีโหลดข้อมูลไม่เจอ
    st.error("⚠️ Data not found! Please check your Google Sheet link in app.py")
    st.info("Make sure you Published to Web as CSV format.")