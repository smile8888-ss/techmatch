import streamlit as st
import pandas as pd
import random

# --- 1. CONFIG ---
st.set_page_config(
    page_title="TechChoose - Top 4 Picks",
    page_icon="🤖",
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
        border: 2px solid #F59E0B;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: 0 0 30px rgba(245, 158, 11, 0.15);
    }
    
    /* AI Verdict Box (ส่วนที่เพิ่มใหม่) */
    .ai-verdict {
        background-color: #172554;
        border-left: 5px solid #3B82F6;
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

    /* Tags */
    .tag-green { background: #064E3B; color: #34D399; padding: 3px 8px; border-radius: 5px; font-size: 0.8em; border: 1px solid #059669; }
    .tag-blue { background: #172554; color: #60A5FA; padding: 3px 8px; border-radius: 5px; font-size: 0.8em; border: 1px solid #2563EB; }

    /* Button */
    .amazon-btn {
        background: linear-gradient(to bottom, #FFD814, #F7CA00);
        color: #000000 !important; padding: 12px 30px; border-radius: 8px;
        text-decoration: none; font-weight: 800; display: inline-block;
        margin-top: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .amazon-btn:hover { transform: scale(1.02); }
    
    .price-big { color: #FBBF24; font-weight: 900; font-size: 2.2em; }
</style>
""", unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.title("🎯 TechChoose")
    st.caption("AI-Powered Recommendation")
    st.write("---")
    
    os_choice = st.radio("📱 Ecosystem:", ["Any", "iOS (iPhone)", "Android"], index=0)
    st.write("---")
    
    def get_score(label): return {"Ignore": 1, "Nice to have": 5, "Important": 8, "Must have": 10}[label]

    p = get_score(st.select_slider("🚀 Speed", ["Ignore", "Nice to have", "Important", "Must have"], "Important"))
    c = get_score(st.select_slider("📸 Camera", ["Ignore", "Nice to have", "Important", "Must have"], "Important"))
    b = get_score(st.select_slider("🔋 Battery", ["Ignore", "Nice to have", "Important", "Must have"], "Nice to have"))
    v = get_score(st.select_slider("💰 Value", ["Ignore", "Nice to have", "Important", "Must have"], "Nice to have"))

    st.write("---")
    if st.button("🔥 Run Analysis", type="primary"):
        st.rerun()

# --- 5. HELPER FUNCTION (สร้างคำพูด AI) ---
def generate_verdict(row):
    reasons = []
    if row['performance'] >= 9: reasons.append("an absolute powerhouse for gaming")
    if row['camera'] >= 9: reasons.append("a professional-grade camera system")
    if row['battery'] >= 9: reasons.append("all-day battery life")
    if row['value'] >= 8: reasons.append("unbeatable value for money")
    
    if not reasons: return "This device offers the most balanced specs for your specific needs."
    
    # รวมประโยคให้ดูเป็นธรรมชาติ
    text = f"This is your #1 pick because it features **{reasons[0]}**"
    if len(reasons) > 1: text += f" and **{reasons[1]}**."
    else: text += "."
    return text

def get_pros(row):
    pros = []
    if row['performance'] >= 9: pros.append("🚀 Top-tier Performance")
    if row['camera'] >= 9: pros.append("📸 Excellent Camera")
    if row['battery'] >= 9: pros.append("🔋 Long-lasting Battery")
    if row['value'] >= 8: pros.append("💰 Great Price Point")
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

    # --- WINNER (HERO SECTION) ---
    with col1:
        st.markdown(f"""
        <div class='winner-box'>
            <span style='background:#F59E0B; color:black; padding:5px 15px; border-radius:20px; font-weight:bold;'>🏆 #1 WINNER ({winner['match']:.0f}%)</span>
            <h1 style='margin-top:15px;'>{winner['name']}</h1>
            <div class='price-big'>${winner['price']:,}</div>
        """, unsafe_allow_html=True)

        # 🔥 ส่วน AI Verdict (พูดกับลูกค้า)
        verdict_text = generate_verdict(winner)
        st.markdown(f"""
        <div class='ai-verdict'>
            <b>💡 AI Verdict:</b><br>
            {verdict_text}
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        # 🔥 ส่วน Pros (ข้อดี)
        pros_list = get_pros(winner)
        for pro in pros_list:
            st.markdown(f"<div class='pros-text'>✅ {pro}</div>", unsafe_allow_html=True)

        st.markdown(f"""
            <a href="{winner['link']}" target="_blank" class="amazon-btn">
                🛒 Check Today's Price
            </a>
        </div>
        """, unsafe_allow_html=True)

    # --- TOP 3 ALTERNATIVES ---
    with col2:
        st.subheader("🥈 Runner-ups (Top 3)")
        
        for i, row in df.iloc[1:4].iterrows():
            diff = winner['price'] - row['price']
            tag_html = ""
            if diff > 0: tag_html = f"<div class='tag-green'>💰 Save ${diff:,}</div>"
            elif row['match'] >= (winner['match'] - 2): tag_html = f"<div class='tag-blue'>🔥 Close Match</div>"
            
            st.markdown(f"""
            <div class="product-card">
                <div style="display:flex; justify-content:space-between; align-items:start;">
                    <div>
                        <b style="font-size:1.1em;">{i}. {row['name']}</b>
                        <div style="color:#94A3B8; font-size:0.9em;">Est. ${row['price']:,}</div>
                        {tag_html}
                    </div>
                    <div style="text-align:right;">
                        <span style="color:#3B82F6; font-weight:900;">{row['match']:.0f}%</span>
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