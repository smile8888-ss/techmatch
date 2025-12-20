import streamlit as st
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(
    page_title="TechChoose - Smart Comparison",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if 'compare_item' not in st.session_state:
    st.session_state.compare_item = None

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # 👇👇👇 ลิงก์ CSV ของพี่ 👇👇👇
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv" 
    try:
        df = pd.read_csv(sheet_url)
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        return df
    except:
        return pd.DataFrame()

# --- 3. STYLE (แก้เรื่องปุ่มมองไม่เห็น + ดีไซน์ใหม่) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');
    
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }

    /* กล่องเปรียบเทียบ (ย้ายมาไว้ข้างล่าง) */
    .vs-box {
        background-color: #1E293B;
        border: 2px solid #3B82F6;
        border-radius: 20px;
        padding: 30px;
        margin-top: 40px;
        animation: slideUp 0.5s ease-out;
    }
    @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

    /* Winner Badge */
    .winner-badge {
        background: #F59E0B; color: black; font-weight: bold;
        padding: 5px 10px; border-radius: 5px; font-size: 0.8em;
    }

    /* Card สินค้า */
    .product-card {
        background: #1E293B; border: 1px solid #334155;
        padding: 15px; border-radius: 12px; margin-bottom: 15px;
    }

    /* ปุ่ม Amazon หลัก */
    .amazon-btn {
        background: linear-gradient(to bottom, #FFD814, #F7CA00);
        color: black !important; padding: 12px 25px; border-radius: 30px;
        text-decoration: none; font-weight: 800; display: inline-block;
        margin-top: 15px; transition: transform 0.2s;
    }
    .amazon-btn:hover { transform: scale(1.05); }
    
    /* ตัวเลขราคา */
    .price-text { color: #FBBF24; font-weight: 900; font-size: 1.4em; }
    
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🎯 Filter")
    st.divider()
    os_choice = st.radio("System:", ["Any", "iOS (iPhone)", "Android"], index=0)
    st.write("---")
    
    def get_score(label):
        return {"Don't Care": 1, "Nice to Have": 5, "Important": 8, "Essential!": 10}[label]

    p_opt = st.select_slider("Speed & Gaming", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Important")
    c_opt = st.select_slider("Camera Quality", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Important")
    b_opt = st.select_slider("Battery Life", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Nice to Have")
    v_opt = st.select_slider("Price / Value", ["Don't Care", "Nice to Have", "Important", "Essential!"], "Nice to Have")

    w_perf, w_cam, w_batt, w_val = get_score(p_opt), get_score(c_opt), get_score(b_opt), get_score(v_opt)

    st.divider()
    if st.button("🚀 Find My Match", type="primary"):
        st.session_state.compare_item = None
        st.rerun()

# --- 5. MAIN LOGIC ---
df = load_data()

if not df.empty:
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']

    # Calc Score
    df['score_raw'] = (df['performance']*w_perf) + (df['camera']*w_cam) + (df['battery']*w_batt) + (df['value']*w_val)
    max_possible = (10*w_perf) + (10*w_cam) + (10*w_batt) + (10*w_val)
    df['match_percent'] = (df['score_raw'] / max_possible) * 100
    df = df.sort_values(by='match_percent', ascending=False).reset_index(drop=True)
    winner = df.iloc[0]

    col1, col2 = st.columns([1.5, 1.2], gap="large")

    # --- ส่วนแสดง Winner (ซ้าย) ---
    with col1:
        st.markdown(f"<div style='padding:20px; border:1px solid #F59E0B; border-radius:15px; background:linear-gradient(180deg, #1E293B 0%, #0F172A 100%); text-align:center;'>", unsafe_allow_html=True)
        st.markdown(f"<span class='winner-badge'>🏆 #1 TOP PICK ({winner['match_percent']:.0f}%)</span>", unsafe_allow_html=True)
        st.markdown(f"<h1>{winner['name']}</h1>", unsafe_allow_html=True)
        st.markdown(f"<div class='price-text'>${winner['price']:,}</div>", unsafe_allow_html=True)
        
        st.write("---")
        st.progress(int(winner['performance']*10), f"⚡ Speed: {winner['performance']}/10")
        st.progress(int(winner['camera']*10), f"📸 Camera: {winner['camera']}/10")
        st.progress(int(winner['battery']*10), f"🔋 Battery: {winner['battery']}/10")
        
        st.markdown(f"""
            <a href="{winner['link']}" target="_blank" class="amazon-btn">
                🛒 Buy on Amazon
            </a>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- ส่วนแสดงรายการอื่น (ขวา) ---
    with col2:
        st.subheader("🥈 Alternatives")
        for i, row in df.iloc[1:6].iterrows():
            with st.container():
                st.markdown(f"""
                <div class="product-card">
                    <div style="display:flex; justify-content:space-between;">
                        <b>{row['name']}</b>
                        <span style="color:#3B82F6; font-weight:bold;">{row['match_percent']:.0f}%</span>
                    </div>
                    <div style="color:#94A3B8; margin-bottom:10px;">Est. ${row['price']:,}</div>
                """, unsafe_allow_html=True)
                
                # ปุ่มกด Compare (ใช้ st.button ปกติ จะได้ไม่มีปัญหาเรื่องสี)
                c_btn1, c_btn2 = st.columns([1, 1.5])
                with c_btn1:
                    if st.button(f"🆚 Compare", key=f"btn_{i}"):
                        st.session_state.compare_item = row
                        st.rerun() # รีเฟรชเพื่อโชว์กล่องข้างล่าง
                with c_btn2:
                     st.markdown(f"<a href='{row['link']}' target='_blank' style='color:#F59E0B; text-decoration:none; font-weight:bold; font-size:0.9em;'>View Deal ></a>", unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

    # --- 🥊 COMPARISON SECTION (ย้ายมาล่างสุด) ---
    if st.session_state.compare_item is not None:
        challenger = st.session_state.compare_item
        
        # คำนวณส่วนต่าง
        diff_price = winner['price'] - challenger['price']
        price_msg = ""
        if diff_price > 0:
            price_msg = f"Save ${diff_price:,} if you choose {challenger['name']}"
        elif diff_price < 0:
            price_msg = f"{winner['name']} is cheaper by ${abs(diff_price):,}"
        else:
            price_msg = "Both have the same price."

        st.markdown("<div id='compare_section'></div>", unsafe_allow_html=True) # Anchor
        st.markdown(f"""
        <div class="vs-box">
            <h2 style="text-align:center; color:#F8FAFC;">🥊 Head-to-Head Analysis</h2>
            <div style="display:flex; justify-content:space-around; align-items:center; text-align:center; margin-top:20px;">
                <div style="width:40%;">
                    <h3 style="color:#FBBF24;">{winner['name']}</h3>
                    <div style="font-size:1.5em; font-weight:bold;">${winner['price']:,}</div>
                    <div class="winner-badge" style="margin-top:10px;">WINNER</div>
                </div>
                <div style="font-size:2em; font-weight:900; color:#64748B;">VS</div>
                <div style="width:40%;">
                    <h3 style="color:#F8FAFC;">{challenger['name']}</h3>
                    <div style="font-size:1.5em; font-weight:bold;">${challenger['price']:,}</div>
                </div>
            </div>
            
            <hr style="border-color:#334155; margin:30px 0;">
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                <div style="background:#0F172A; padding:15px; border-radius:10px;">
                    <h4 style="color:#3B82F6;">📊 Specs Difference</h4>
                    <p>⚡ <b>Speed:</b> {winner['performance']} vs {challenger['performance']}</p>
                    <p>📸 <b>Camera:</b> {winner['camera']} vs {challenger['camera']}</p>
                    <p>🔋 <b>Battery:</b> {winner['battery']} vs {challenger['battery']}</p>
                </div>
                <div style="background:#0F172A; padding:15px; border-radius:10px;">
                    <h4 style="color:#F59E0B;">💰 Price & Verdict</h4>
                    <p style="font-size:1.1em; font-weight:bold; color:#22C55E;">{price_msg}</p>
                    <p style="color:#94A3B8; font-size:0.9em;">
                        *Score Gap: {(winner['match_percent'] - challenger['match_percent']):.1f}% better match for you.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Auto Scroll (Optional Hack) - หรือแค่ให้มันเด้งขึ้นมาก็พอ

    # --- Footer ---
    st.write("---")
    st.caption("Disclaimer: TechChoose is a participant in the Amazon Services LLC Associates Program. Prices are subject to change.")

else:
    st.error("Please connect your Google Sheet CSV.")