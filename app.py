import streamlit as st

st.set_page_config(page_title="Social Media Audit for Athletes", layout="wide")

st.title("🏀 Social Media Audit Tool for Student-Athletes & Coaches")

st.markdown("This tool helps analyze your social media presence and identify red flags, engagement scores, and comparison insights.")

# Step 1: Social Handle Input
st.header("Step 1: Enter Your Social Media Handles")
col1, col2, col3 = st.columns(3)
with col1:
    instagram = st.text_input("Instagram Handle")
with col2:
    twitter = st.text_input("Twitter/X Handle")
with col3:
    tiktok = st.text_input("TikTok Handle")

# Step 2: Audit Features
st.header("Step 2: Select What You Want to Audit")
profile_score = st.checkbox("🔍 Profile Score (Followers, Engagement, Demographics)", value=True)
content_flags = st.checkbox("🚩 Content Flag Review (Captions, Hashtags, Tone)", value=True)
peer_comparison = st.checkbox("👥 Peer Account Comparison")

# Step 3: AI Level
st.header("Step 3: AI Review Depth")
audit_level = st.selectbox("Select Audit Level", ["Quick Check", "Standard", "Deep Dive"])

# Step 4: Run Button
st.header("Step 4: Generate Your Audit")
if st.button("Run My Audit"):
    st.success("✅ Audit Submitted Successfully. Processing...")
    
    st.subheader("🔎 Sample Output")
    st.markdown("- **Instagram Engagement:** 3.2% (Above average for athletes)")
    st.markdown("- **Red Flags:** 2 posts flagged for slang/controversial hashtags")
    st.markdown("- **Top Suggestions:**")
    st.markdown("    - Clean up bio and pinned post")
    st.markdown("    - Add call-to-action video with contact info")
    st.markdown("    - Compare tone to @cleanathlete or @nextlevelqb")

# Sidebar
st.sidebar.title("📊 App Info")
st.sidebar.markdown("""
- Version: 1.0 Wireframe  
- Built for: Student-Athletes  
- Stack: Streamlit + RapidAPI + GPT  
""")
