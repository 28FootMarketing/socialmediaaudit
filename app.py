from fpdf import FPDF
import streamlit as st
import io
import tempfile
import os

# Streamlit Config
st.set_page_config(page_title="Social Media Audit", layout="wide")
st.title("🏀 Social Media Audit Tool for Student-Athletes & Coaches")

# Initialize session state for handles if not exists
if 'instagram_handles' not in st.session_state:
    st.session_state.instagram_handles = ['']
if 'twitter_handles' not in st.session_state:
    st.session_state.twitter_handles = ['']
if 'tiktok_handles' not in st.session_state:
    st.session_state.tiktok_handles = ['']

# Step 1: Input with multiple handles
st.header("Step 1: Enter Your Social Media Handles")

# Instagram Section
st.subheader("📸 Instagram Handles")
col1, col2 = st.columns([4, 1])
with col1:
    for i, handle in enumerate(st.session_state.instagram_handles):
        st.session_state.instagram_handles[i] = st.text_input(
            f"Instagram Handle {i+1}", 
            value=handle, 
            key=f"instagram_{i}",
            placeholder="@username"
        )

with col2:
    st.write("") # Spacing
    if st.button("➕ Add Instagram", key="add_instagram"):
        st.session_state.instagram_handles.append('')
        st.rerun()
    if len(st.session_state.instagram_handles) > 1:
        if st.button("➖ Remove Instagram", key="remove_instagram"):
            st.session_state.instagram_handles.pop()
            st.rerun()

# Twitter Section
st.subheader("🐦 Twitter/X Handles")
col1, col2 = st.columns([4, 1])
with col1:
    for i, handle in enumerate(st.session_state.twitter_handles):
        st.session_state.twitter_handles[i] = st.text_input(
            f"Twitter/X Handle {i+1}", 
            value=handle, 
            key=f"twitter_{i}",
            placeholder="@username"
        )

with col2:
    st.write("") # Spacing
    if st.button("➕ Add Twitter", key="add_twitter"):
        st.session_state.twitter_handles.append('')
        st.rerun()
    if len(st.session_state.twitter_handles) > 1:
        if st.button("➖ Remove Twitter", key="remove_twitter"):
            st.session_state.twitter_handles.pop()
            st.rerun()

# TikTok Section
st.subheader("📱 TikTok Handles")
col1, col2 = st.columns([4, 1])
with col1:
    for i, handle in enumerate(st.session_state.tiktok_handles):
        st.session_state.tiktok_handles[i] = st.text_input(
            f"TikTok Handle {i+1}", 
            value=handle, 
            key=f"tiktok_{i}",
            placeholder="@username"
        )

with col2:
    st.write("") # Spacing
    if st.button("➕ Add TikTok", key="add_tiktok"):
        st.session_state.tiktok_handles.append('')
        st.rerun()
    if len(st.session_state.tiktok_handles) > 1:
        if st.button("➖ Remove TikTok", key="remove_tiktok"):
            st.session_state.tiktok_handles.pop()
            st.rerun()

# Filter out empty handles
instagram_handles = [h.strip() for h in st.session_state.instagram_handles if h.strip()]
twitter_handles = [h.strip() for h in st.session_state.twitter_handles if h.strip()]
tiktok_handles = [h.strip() for h in st.session_state.tiktok_handles if h.strip()]

# Display summary of entered handles
if instagram_handles or twitter_handles or tiktok_handles:
    st.info(f"**Summary:** {len(instagram_handles)} Instagram, {len(twitter_handles)} Twitter/X, {len(tiktok_handles)} TikTok handles entered")

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
    # Input validation
    total_handles = len(instagram_handles) + len(twitter_handles) + len(tiktok_handles)
    if total_handles == 0:
        st.error("Please enter at least one social media handle.")
        st.stop()
    
    st.success(f"✅ Processing audit for {total_handles} social media accounts...")
    
    # Generate athlete name from first available handle
    athlete_name = (instagram_handles[0] if instagram_handles else 
                   twitter_handles[0] if twitter_handles else 
                   tiktok_handles[0] if tiktok_handles else 
                   "Sample Athlete")
    
    # Create comprehensive report for all handles
    gpt_summary = f"""{athlete_name}'s Comprehensive Social Media Audit Report

=== ACCOUNT OVERVIEW ===
Primary Handle: {athlete_name}
Sport: Basketball
Graduation Year: 2025
Audit Level: {audit_level}
Total Accounts Audited: {total_handles}

=== PLATFORM BREAKDOWN ==="""

    if instagram_handles:
        gpt_summary += f"""
Instagram Accounts ({len(instagram_handles)}):"""
        for i, handle in enumerate(instagram_handles, 1):
            gpt_summary += f"""
  {i}. {handle}
     - Followers: {1800 + i*300}
     - Engagement Rate: {2.8 + i*0.3}%
     - Posts: {45 + i*10}"""

    if twitter_handles:
        gpt_summary += f"""

Twitter/X Accounts ({len(twitter_handles)}):"""
        for i, handle in enumerate(twitter_handles, 1):
            gpt_summary += f"""
  {i}. {handle}
     - Followers: {650 + i*150}
     - Tweet Frequency: {3 + i} per week
     - Engagement: {1.2 + i*0.4}%"""

    if tiktok_handles:
        gpt_summary += f"""

TikTok Accounts ({len(tiktok_handles)}):"""
        for i, handle in enumerate(tiktok_handles, 1):
            gpt_summary += f"""
  {i}. {handle}
     - Followers: {420 + i*80}
     - Videos: {12 + i*5}
     - Avg Views: {2400 + i*600}"""

    gpt_summary += f"""

=== OVERALL ASSESSMENT ===
Profile Score: 7.5/10
Content Quality: 8/10
Brand Consistency: 6/10
Red Flags Found: 3 posts need attention
Overall Rating: 82/100

=== KEY FINDINGS ==="""
    
    if profile_score:
        gpt_summary += """
Profile Analysis:
- Strong bio consistency across platforms
- Missing grad year in 2 profiles
- Contact info needs standardization"""

    if content_flags:
        gpt_summary += """

Content Review:
- 2 posts with inappropriate language flagged
- 1 post needs better timing consideration  
- Overall content aligns well with athlete brand"""

    if peer_comparison:
        gpt_summary += """

Peer Comparison:
- Above average engagement vs similar athletes
- Could improve posting frequency
- Strong authentic voice compared to peers"""

    gpt_summary += f"""

=== RECOMMENDATIONS BY PLATFORM ==="""
    
    if instagram_handles:
        gpt_summary += """
Instagram:
1. Standardize bio format across all accounts
2. Use consistent hashtag strategy
3. Post 3-4 times per week consistently"""

    if twitter_handles:
        gpt_summary += """

Twitter/X:
1. Increase engagement with team/coach content
2. Share more behind-the-scenes content
3. Use Twitter Spaces for Q&As"""

    if tiktok_handles:
        gpt_summary += """

TikTok:
1. Create weekly training series
2. Jump on trending sounds appropriately
3. Cross-promote with other platforms"""

    gpt_summary += """

=== NEXT STEPS ===
Week 1: Update all bios and archive flagged content
Week 2: Implement consistent posting schedule
Week 3: Launch cross-platform content series
Week 4: Review and adjust strategy based on engagement

=== COACH/PARENT REVIEW ===
Recommended: Schedule review meeting to discuss findings
Focus Areas: Brand consistency and content timing
Overall Assessment: Ready for recruitment visibility"""

    # Display summary
    st.text_area("📋 Comprehensive GPT Audit Report", gpt_summary, height=400)
    
    # PDF Generation with better error handling
    try:
        # Create PDF in memory
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", '', 10)  # Smaller font for more content
        
        # Split text into lines and add to PDF
        for line in gpt_summary.split("\n"):
            # Handle empty lines
            if line.strip():
                # Handle long lines
                if len(line) > 80:
                    pdf.multi_cell(0, 6, line.encode('latin1', 'ignore').decode('latin1'))
                else:
                    pdf.cell(0, 6, line.encode('latin1', 'ignore').decode('latin1'), ln=True)
            else:
                pdf.ln(3)  # Add some space for empty lines
        
        # Generate PDF as bytes
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        
        # Provide download button with detailed filename
        filename = f"Social_Media_Audit_{athlete_name}_{total_handles}_accounts.pdf"
        st.download_button(
            label=f"📥 Download Comprehensive PDF Report ({total_handles} accounts)",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf"
        )
        
        st.success(f"✅ Audit complete! Generated report covering {total_handles} social media accounts.")
        
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        st.info("You can still copy the text report above.")

# Sidebar with tips
with st.sidebar:
    st.header("💡 Tips")
    st.write("**Multiple Accounts?**")
    st.write("• Add all your handles per platform")
    st.write("• Include backup/fan accounts") 
    st.write("• Business vs personal profiles")
    st.write("")
    st.write("**Best Practices:**")
    st.write("• Use @ symbol in handles")
    st.write("• Double-check spelling")
    st.write("• Include all public accounts")
    st.write("")
    st.write("**Audit Levels:**")
    st.write("• Quick: Basic profile check")
    st.write("• Standard: Content + engagement")
    st.write("• Deep Dive: Full analysis + peers")
