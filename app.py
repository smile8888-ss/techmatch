import streamlit as st
import pandas as pd

# --- 1. CONFIG ---
st.set_page_config(
    page_title="TechChoose - Lifestyle Match",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. LOAD DATA ---
@st.cache_data(ttl=60)
def load_data():
    # 👇👇👇 ลิงก์ CSV ของพี่ครับ 👇👇👇
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQqoziKy640ID3oDos-DKk49txgsNPdMJGb_vAH1_WiRG88kewDPneVgo9iSHq2u5DXYI_g_n6se14k/pub?output=csv" 
    try:
        df = pd.read_csv(sheet_url)
        df['os_type'] = df['name'].apply(lambda x: 'iOS' if 'iPhone' in str(x) else 'Android')
        return df
    except:
        return pd.DataFrame()

# --- 3. STYLE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');
    
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }

    /* Winner Box */
    .winner-box {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
        border: 2px solid #3B82F6; /* สีฟ้าให้ดู Smart */
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.2);
    }
    
    /* Persona Badge */
    .persona-badge {
        background: #3B82F6; color: white; font-weight: bold;
        padding: 5px 15px; border-radius: 20px; font-size: 0.8em;
        text-transform: uppercase; letter-spacing: 1px;
        margin-bottom: 10px; display: inline-block;
    }

    /* AI Verdict Box */
    .ai-verdict {
        background-color: #172554;
        border-left: 5px solid #F59E0B;
        padding: 15px;
        margin-top: 20px;
        text-align: left;
        border-radius: 5px;
        font-size: 0.95em;
        line-height: 1.5;
    }

    /* Pros List */
    .pros-text { color: #4ADE80; font-size: 0.9em; margin-bottom: 5px; text-align: left; }
    
    /* Product Card */
    .product-card {
        background: #1E293B; border: 1px solid #334155;
        padding: 20px; border-radius: 15px; margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .product-card:hover { border-color: #3B82F6; transform: translateX(5px); }

    /* Button */
    .amazon-btn {
        background: linear-gradient(to bottom, #FFD814, #F7CA00);
        color: #000000 !important; padding: 12px 30px; border-radius: 8px;
        text-decoration: none; font-weight: 800; display: inline-block;
        margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .amazon-btn:hover { transform: scale(1.02); }
    
    .price-big { color: #FBBF24; font-weight: 900; font-size: 2.2em; }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #3B82F6 0%, #60A5FA 100%);
    }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR (The Persona Logic) ---
with st.sidebar:
    st.title("🎯 TechChoose")
    st.caption("Select your lifestyle:")
    st.write("---")
    
    os_choice = st.radio("📱 Ecosystem:", ["Any", "iOS (iPhone)", "Android"], index=0)
    st.write("---")
    
    # 🔥 New Feature: Lifestyle Selector
    lifestyle = st.radio(
        "👤 Who are you?",
        [
            "🎮 Hardcore Gamer", 
            "📸 Content Creator", 
            "💼 Business / Work", 
            "💰 Student / Budget Saver", 
            "🛠️ Custom (Manual Setup)"
        ]
    )

    # Auto-Set Weights based on Lifestyle
    if lifestyle == "🎮 Hardcore Gamer":
        p, c, b, v = 10, 3, 8, 5
        st.info("✅ Setting: Max Speed + Battery")
    elif lifestyle == "📸 Content Creator":
        p, c, b, v = 7, 10, 8, 5
        st.info("✅ Setting: Max Camera + Storage")
    elif lifestyle == "💼 Business / Work":
        p, c, b, v = 8, 6, 9, 6
        st.info("✅ Setting: Balanced + Reliability")
    elif lifestyle == "💰 Student / Budget Saver":
        p, c, b, v = 5, 5, 7, 10
        st.info("✅ Setting: Best Value for Money")
    else:
        # Custom Mode: Show Sliders
        st.write("---")
        st.caption("⚙️ Manual Adjustment")
        def get_score(label): return {"Ignore": 1, "Nice to have": 5, "Important": 8, "Must have": 10}[label]
        p = get_score(st.select_slider("🚀 Speed", ["Ignore", "Nice to have", "Important", "Must have"], "Important"))
        c = get_score(st.select_slider("📸 Camera", ["Ignore", "Nice to have", "Important", "Must have"], "Important"))
        b = get_score(st.select_slider("🔋 Battery", ["Ignore", "Nice to have", "Important", "Must have"], "Nice to have"))
        v = get_score(st.select_slider("💰 Value", ["Ignore", "Nice to have", "Important", "Must have"], "Nice to have"))

    st.write("---")
    if st.button("🔥 Find My Phone", type="primary"):
        st.rerun()

# --- 5. HELPER FUNCTION ---
def generate_verdict(row, mode):
    # ปรับคำพูด AI ตามโหมดที่เลือก
    if "Gamer" in mode:
        return f"For gaming, the **{row['name']}** is a beast! With a performance score of {row['performance']}/10, it handles AAA games easily."
    elif "Creator" in mode:
        return f"If you love photos, **{row['name']}** is the one. Its camera system ({row['camera']}/10) captures stunning details."
    elif "Student" in mode or "Budget" in mode:
        return f"Smart choice! The **{row['name']}** gives you the best bang for your buck at ${row['price']:,}."
    else:
        return f"The **{row['name']}** is the best all-rounder for you, balancing performance, battery, and price perfectly."

def get_pros(row):
    pros = []
    if row['performance'] >= 9: pros.append("🚀 Ultimate Performance")
    if row['camera'] >= 9: pros.append("📸 Pro-Grade Camera")
    if row['battery'] >= 9: pros.append("🔋 All-Day Battery")
    if row['value'] >= 8: pros.append("💰 Best Value Pick")
    return pros

# --- 6. MAIN LOGIC ---
df = load_data()

if not df.empty:
    if "iOS" in os_choice: df = df[df['os_type'] == 'iOS']
    elif "Android" in os_choice: df = df[df['os_type'] == 'Android']

    # Score Calculation
    df['score'] = (df['performance']*p) + (df['camera']*c) + (df['battery']*b) + (df['value']*v)
    max_score = (10*p) + (10*c) + (10*b) + (10*v)
    df['match'] = (df['score'] / max_score) * 100
    df = df.sort_values(by='match', ascending=False).reset_index(drop=True)
    
    winner = df.iloc[0]

    col1, col2 = st.columns([1.5, 1.2], gap="large")

    # --- WINNER ---
    with col1:
        st.markdown(f"""
        <div class='winner-box'>
            <span class='persona-badge'>Selected for: {lifestyle.split(' ')[1]}</span><br>
            <span style='color:#F59E0B; font-weight:bold; font-size:1.2em;'>🏆 #1 RECOMMENDATION</span>
            <h1 style='margin-top:10px;'>{winner['name']}</h1>
            <div class='price-big'>${winner['price']:,}</div>
        """, unsafe_allow_html=True)

        # 🔥 AI Verdict (พูดตามไลฟ์สไตล์)
        verdict_text = generate_verdict(winner, lifestyle)
        st.markdown(f"""
        <div class='ai-verdict'>
            <b>💡 Why this matches you:</b><br>
            {verdict_text}
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        pros_list = get_pros(winner)
        for pro in pros_list:
            st.markdown(f"<div class='pros-text'>✅ {pro}</div>", unsafe_allow_html=True)

        st.markdown(f"""
            <a href="{winner['link']}" target="_blank" class="amazon-btn">
                🛒 Check Price on Amazon
            </a>
        </div>
        """, unsafe_allow_html=True)

    # --- TOP 3 ALTERNATIVES ---
    with col2:
        st.subheader(f"🥈 Best Alternatives for {lifestyle.split(' ')[1]}")
        
        for i, row in df.iloc[1:4].iterrows():
            diff = winner['price'] - row['price']
            tag_html = ""
            if diff > 0: 
                tag_html = f"<span style='color:#34D399; background:#064E3B; padding:2px 8px; border-radius:4px; font-size:0.8em;'>💰 Save ${diff:,}</span>"
            
            st.markdown(f"""
            <div class="product-card">
                <div style="display:flex; justify-content:space-between; align-items:start;">
                    <div>
                        <b style="font-size:1.1em;">{i}. {row['name']}</b>
                        <div style="color:#94A3B8; font-size:0.9em;">Est. ${row['price']:,}</div>
                        {tag_html}
                    </div>
                    <div style="text-align:right;">
                        <span style="color:#3B82F6; font-weight:900;">{row['match']:.0f}% Match</span>
                        <br>
                        <a href='{row['link']}' target='_blank' style='color:#F59E0B; font-weight:bold; font-size:0.85em; text-decoration:none;'>
                            View Deal >
                        </a>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")
    st.caption("Disclaimer: TechChoose is a participant in the Amazon Services LLC Associates Program.")

else:
    st.error("Please connect your Google Sheet.")