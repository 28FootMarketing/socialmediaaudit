from fpdf import FPDF
import streamlit as st

# Streamlit Config
st.set_page_config(page_title="Social Media Audit", layout="wide")

st.title("🏀 Social Media Audit Tool for Student-Athletes & Coaches")

# Step 1: Input
st.header("Step 1: Enter Your Social Media Handles")
col1, col2, col3 = st.columns(3)
with col1:
    instagram = st.text_input("Instagram Handle")
with col2:
    twitter = st.text_input("Twitter/X Handle")
with col3:
    tiktok = st.text_input("TikTok Handle")

# Step 2: Options
st.header("Step 2: Select What to Audit")
profile_score = st.checkbox("🔍 Profile Score", value=True)
content_flags = st.checkbox("🚩 Content Review", value=True)
peer_comparison = st.checkbox("👥 Peer Comparison", value=True)

# Step 3: Depth
st.header("Step 3: Audit Level")
audit_level = st.selectbox("Choose Depth", ["Quick Check", "Standard", "Deep Dive"])

# Step 4: Generate
st.header("Step 4: Generate GPT Audit + PDF Report")

if st.button("Run My Audit"):
    st.success("✅ Processing your personalized report...")

    # 🧠 Mock GPT Summary (Replace with GPT API call if needed)
    athlete_name = instagram or "Sample Athlete"
    gpt_summary = f"""
{athlete_name}'s Social Media Audit Report

Name: {athlete_name}
Sport: Basketball
Graduation Year: 2025

Instagram Followers: 2,145
Engagement Rate: 3.2%
Red Flags: 2 captions with slang
Trending Hashtags: #grindmode, #gameday
Twitter Activity: Low
Bio Score: 7/10
Consistency Score: 6/10
Overall Rating: 78/100

Peer Benchmark: @nextlevelqb (4.8% Engagement)
Key Difference: Pinned post, clean bio, direct contact info

Top 3 Recommendations:
1. Update Instagram bio with grad year and email.
2. Archive flagged posts.
3. Post 1 short-form video weekly.

Next Step Playbook:
- Update bio this week
- Clean up older captions
- Launch a weekly “Game Ready” TikTok series
- Ask your coach to review your profiles
"""

    st.text_area("📋 GPT Summary", gpt_summary, height=300)

    # PDF Generator
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", '', 12)
    for line in gpt_summary.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf_file_path = "Social_Media_Audit_Report.pdf"
    pdf.output(pdf_file_path)

    with open(pdf_file_path, "rb") as file:
        st.download_button(
            label="📥 Download Your PDF Report",
            data=file,
            file_name=pdf_file_path,
            mime="application/pdf"
        )
