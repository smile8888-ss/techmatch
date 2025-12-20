import streamlit as st
import pandas as pd

# --- 1. SETUP: ตั้งค่าหน้าจอแบบ WIDE และโหลด Font ---
st.set_page_config(
    page_title="TechChoose - Smart Gadget Finder",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CONNECT DATABASE (GOOGLE SHEETS) ---
@st.cache_data(ttl=60)
def load_data():
    # 👇👇👇 วางลิงก์ CSV ของพี่ตรงนี้ (ในฟันหนู) 👇👇👇
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv"
    # 👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆👆

    try:
        df = pd.read_csv(sheet_url)
        return df
    except Exception as e:
        return pd.DataFrame()

# --- 3. PREMIUM US-STYLE CSS: แต่งหน้าตาให้ดูแพง ---
st.markdown("""
<style>
    /* Import Font 'Inter' ยอดฮิต */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    /* พื้นหลังและฟอนต์หลัก */
    .stApp {
        background-color: #111827; /* สีดำเทาเข้ม Modern Dark */
        color: #F9FAFB; /* สีขาวนวล */
        font-family: 'Inter', sans-serif;
    }

    h1, h2, h3 { font-weight: 800; letter-spacing: -0.025em; }

    /* สีเน้น (Accent Color) - สีทอง Amazon */
    .highlight { color: #F59E0B; text-shadow: 0 0 15px rgba(245, 158, 11, 0.4); }
    .blue-highlight { color: #3B82F6; }

    /* แก้ไขส่วนแสดงราคาตัวใหญ่ (Metric) ให้เด่น */
    [data-testid="stMetricValue"] {
        color: #FBBF24 !important; /* สีทองสว่าง */
        font-size: 3rem !important; /* ใหญ่สะใจ */
        font-weight: 900 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #9CA3AF !important; /* สีเทาอ่อน */
        font-size: 1.1rem !important;
    }

    /* การ์ดสินค้า (Runners-up) */
    .product-card {
        background-color: #1F2937;
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid #374151;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    .product-card:hover {
        transform: translateY(-7px); /* ลอยขึ้นเมื่อชี้ */
        border-color: #F59E0B;
        box-shadow: 0 15px 25px -5px rgba(0, 0, 0, 0.2);
    }

    /* ราคาในการ์ดเล็ก */
    .card-price {
        color: #FBBF24; font-weight: 800; font-size: 1.3em;
    }

    /* ปุ่มกดสไตล์ Amazon Premium Gradient */
    .amazon-btn {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        color: white !important;
        padding: 14px 28px;
        border-radius: 10px;
        text-align: center;
        font-weight: 800;
        font-size: 1.2em;
        text-decoration: none;
        display: block;
        margin-top: 25px;
        box-shadow: 0 10px 15px -3px rgba(245, 158, 11, 0.4);
        transition: all 0.2s;
    }
    .amazon-btn:hover {
        transform: scale(1.03);
        box-shadow: 0 20px 25px -5px rgba(245, 158, 11, 0.5);
        background: linear-gradient(135deg, #FBBF24 0%, #B45309 100%);
    }
    
    /* ปรับสี Progress Bar */
    .stProgress > div > div { background-color: #3B82F6; }
    hr { border-color: #374151; }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🚀 TechChoose")
    st.caption("US Market Edition")
    st.divider()
    
    st.header("🎯 Your Preferences")
    w_perf = st.slider("⚡ Performance", 1, 10, 8)
    w_cam = st.slider("📸 Camera Quality", 1, 10, 8)
    w_batt = st.slider("🔋 Battery Life", 1, 10, 5)
    w_val = st.slider("💰 Value for Money", 1, 10, 6)
    
    st.divider()
    if st.button("🔄 Refresh Results", type="primary"):
        load_data.clear()
        st.rerun()

# --- 5. MAIN CONTENT ---
st.title("🇺🇸 Find Your Perfect Device.")
st.markdown("### Unbiased recommendations based on US market data.")
st.divider()

df = load_data()

if not df.empty:
    # คำนวณคะแนน
    df['score_raw'] = (df['performance'] * w_perf) + (df['camera'] * w_cam) + (df['battery'] * w_batt) + (df['value'] * w_val)
    max_possible = (10*w_perf) + (10*w_cam) + (10*w_batt) + (10*w_val)
    df['match_percent'] = (df['score_raw'] / max_possible) * 100
    df = df.sort_values(by='match_percent', ascending=False).reset_index(drop=True)
    winner = df.iloc[0]

    col1, col2 = st.columns([1.8, 1.2], gap="large")
    
    # --- Winner Section (Left) ---
    with col1:
        st.markdown(f"<h2 class='highlight'>🏆 TOP PICK: {winner['match_percent']:.0f}% Match</h2>", unsafe_allow_html=True)
        st.markdown(f"# {winner['name']}")
        
        # แสดงราคาตัวใหญ่ๆ (แก้ปัญหาที่มองไม่เห็น)
        st.metric("Estimated US Price", f"${winner['price']:,}")
        
        st.write("---")
        st.write("📊 **Key Specs Breakdown:**")
        st.progress(int(winner['performance']*10), text=f"⚡ Performance: {winner['performance']}/10")
        st.progress(int(winner['camera']*10), text=f"📸 Camera: {winner['camera']}/10")
        st.progress(int(winner['battery']*10), text=f"🔋 Battery: {winner['battery']}/10")

        st.markdown(f"""
            <a href="{winner['link']}" target="_blank" class="amazon-btn">
                🛒 Check Today's Price on Amazon
            </a>
        """, unsafe_allow_html=True)

    # --- Runners-up Section (Right) ---
    with col2:
        st.subheader("🥈 Great Alternatives")
        for i, row in df.iloc[1:].iterrows():
            st.markdown(f"""
            <div class="product-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <b style="font-size:1.2em;">{row['name']}</b>
                    <span class="blue-highlight" style="font-weight:900; font-size:1.3em;">{row['match_percent']:.0f}%</span>
                </div>
                <div style="margin-bottom:15px;">
                    <span style="color:#9CA3AF;">Est. Price:</span> 
                    <span class="card-price">${row['price']:,}</span>
                </div>
                <a href="{row['link']}" target="_blank" style="color:#F59E0B; text-decoration:none; font-weight:800; display:flex; align-items:center;">
                    👉 See Deal on Amazon
                </a>
            </div>
            """, unsafe_allow_html=True)

else:
    st.error("⚠️ Data connect error. Please check your CSV link.")