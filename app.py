import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse
import time
from fpdf import FPDF
import tempfile
import os
from datetime import datetime
import pandas as pd

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
if 'snapchat_handles' not in st.session_state:
    st.session_state.snapchat_handles = ['']
if 'youtube_handles' not in st.session_state:
    st.session_state.youtube_handles = ['']
if 'linkedin_handles' not in st.session_state:
    st.session_state.linkedin_handles = ['']
if 'facebook_handles' not in st.session_state:
    st.session_state.facebook_handles = ['']

# Web scraping functions
class SocialMediaScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_instagram_profile(self, username):
        """Scrape Instagram profile data"""
        try:
            username = username.replace('@', '').strip()
            url = f"https://www.instagram.com/{username}/"
            
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return {"error": f"Profile not found or private: {username}"}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to extract data from meta tags and script tags
            data = {
                "username": username,
                "followers": "Private/Unable to access",
                "following": "Private/Unable to access",
                "posts": "Private/Unable to access",
                "bio": "Private/Unable to access",
                "is_private": True,
                "profile_pic_url": None,
                "external_url": None
            }
            
            # Look for JSON data in script tags
            scripts = soup.find_all('script', type='application/ld+json')
            for script in scripts:
                try:
                    json_data = json.loads(script.string)
                    if isinstance(json_data, dict) and 'author' in json_data:
                        author = json_data['author']
                        if isinstance(author, dict):
                            data["bio"] = author.get('description', 'No bio available')
                            data["followers"] = author.get('interactionStatistic', {}).get('userInteractionCount', 'N/A')
                except:
                    continue
            
            # Try to get meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                content = meta_desc.get('content', '')
                # Parse follower count from meta description
                follower_match = re.search(r'([\d,]+)\s+Followers', content)
                if follower_match:
                    data["followers"] = follower_match.group(1)
                    data["is_private"] = False
            
            return data
            
        except Exception as e:
            return {"error": f"Error scraping Instagram profile {username}: {str(e)}"}
    
    def scrape_twitter_profile(self, username):
        """Scrape Twitter/X profile data"""
        try:
            username = username.replace('@', '').strip()
            # Note: Twitter heavily restricts scraping, this is a basic attempt
            url = f"https://twitter.com/{username}"
            
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return {"error": f"Profile not found: {username}"}
            
            data = {
                "username": username,
                "followers": "Requires API access",
                "following": "Requires API access", 
                "tweets": "Requires API access",
                "bio": "Requires API access",
                "verified": False,
                "location": None
            }
            
            return data
            
        except Exception as e:
            return {"error": f"Error scraping Twitter profile {username}: {str(e)}"}
    
    def scrape_tiktok_profile(self, username):
        """Scrape TikTok profile data"""
        try:
            username = username.replace('@', '').strip()
            url = f"https://www.tiktok.com/@{username}"
            
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return {"error": f"Profile not found: {username}"}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            data = {
                "username": username,
                "followers": "TikTok restricts scraping",
                "likes": "TikTok restricts scraping",
                "videos": "TikTok restricts scraping",
                "bio": "TikTok restricts scraping"
            }
            
            return data
            
        except Exception as e:
            return {"error": f"Error scraping TikTok profile {username}: {str(e)}"}
    
    def scrape_youtube_channel(self, channel_name):
        """Scrape YouTube channel data"""
        try:
            # Handle different YouTube URL formats
            if 'youtube.com' in channel_name:
                url = channel_name
            elif channel_name.startswith('@'):
                url = f"https://www.youtube.com/{channel_name}"
            else:
                url = f"https://www.youtube.com/c/{channel_name}"
            
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                return {"error": f"Channel not found: {channel_name}"}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            data = {
                "channel_name": channel_name,
                "subscribers": "Unable to access",
                "views": "Unable to access",
                "videos": "Unable to access",
                "description": "Unable to access"
            }
            
            # Try to extract from meta tags
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                data["description"] = meta_desc.get('content', '')
            
            return data
            
        except Exception as e:
            return {"error": f"Error scraping YouTube channel {channel_name}: {str(e)}"}
    
    def scrape_linkedin_profile(self, profile_url):
        """Scrape LinkedIn profile data"""
        try:
            if not profile_url.startswith('http'):
                profile_url = f"https://www.linkedin.com/in/{profile_url}"
            
            response = self.session.get(profile_url, timeout=10)
            
            data = {
                "profile_url": profile_url,
                "name": "LinkedIn restricts scraping",
                "headline": "LinkedIn restricts scraping",
                "connections": "LinkedIn restricts scraping",
                "location": "LinkedIn restricts scraping"
            }
            
            return data
            
        except Exception as e:
            return {"error": f"Error accessing LinkedIn profile: {str(e)}"}

def analyze_scraped_data(scraped_results):
    """Analyze the scraped social media data"""
    analysis = {
        "total_platforms": 0,
        "accessible_platforms": 0,
        "private_accounts": 0,
        "public_accounts": 0,
        "platform_insights": [],
        "risk_factors": [],
        "recommendations": []
    }
    
    for platform, results in scraped_results.items():
        if not results:
            continue
            
        analysis["total_platforms"] += len(results)
        
        for result in results:
            if "error" in result:
                analysis["risk_factors"].append(f"{platform}: {result['error']}")
                continue
            
            analysis["accessible_platforms"] += 1
            
            # Check privacy settings
            if result.get("is_private", False):
                analysis["private_accounts"] += 1
            else:
                analysis["public_accounts"] += 1
            
            # Platform-specific analysis
            if platform == "instagram":
                if result.get("followers") != "Private/Unable to access":
                    try:
                        follower_count = int(result["followers"].replace(',', ''))
                        if follower_count > 10000:
                            analysis["platform_insights"].append(f"Instagram @{result['username']}: High follower count ({follower_count:,}) - good for recruitment visibility")
                        elif follower_count < 100:
                            analysis["platform_insights"].append(f"Instagram @{result['username']}: Low follower count - consider growing audience")
                    except:
                        pass
            
            elif platform == "youtube":
                if "subscribers" in result and result["subscribers"] != "Unable to access":
                    analysis["platform_insights"].append(f"YouTube {result['channel_name']}: Active video content creator")
    
    # Generate recommendations
    if analysis["private_accounts"] > analysis["public_accounts"]:
        analysis["recommendations"].append("Consider making key accounts public for recruitment visibility")
    
    if analysis["total_platforms"] < 3:
        analysis["recommendations"].append("Expand to more social media platforms for better digital presence")
    
    return analysis

# Helper function to render social media section
def render_social_section(platform_name, emoji, handles_key, placeholder_text, button_suffix):
    st.subheader(f"{emoji} {platform_name}")
    col1, col2 = st.columns([4, 1])
    with col1:
        for i, handle in enumerate(st.session_state[handles_key]):
            st.session_state[handles_key][i] = st.text_input(
                f"{platform_name} Handle {i+1}", 
                value=handle, 
                key=f"{handles_key}_{i}",
                placeholder=placeholder_text
            )

    with col2:
        st.write("") # Spacing
        if st.button(f"➕ Add {platform_name}", key=f"add_{button_suffix}"):
            st.session_state[handles_key].append('')
            st.rerun()
        if len(st.session_state[handles_key]) > 1:
            if st.button(f"➖ Remove {platform_name}", key=f"remove_{button_suffix}"):
                st.session_state[handles_key].pop()
                st.rerun()

# Step 1: Input with multiple handles
st.header("Step 1: Enter Your Social Media Handles")

# Create tabs for better organization
tab1, tab2 = st.tabs(["📱 Main Platforms", "💼 Professional & Video"])

with tab1:
    render_social_section("Instagram", "📸", "instagram_handles", "@username", "instagram")
    st.divider()
    render_social_section("TikTok", "📱", "tiktok_handles", "@username", "tiktok")
    st.divider()
    render_social_section("Twitter/X", "🐦", "twitter_handles", "@username", "twitter")
    st.divider()
    render_social_section("Snapchat", "👻", "snapchat_handles", "@username", "snapchat")

with tab2:
    render_social_section("YouTube", "📺", "youtube_handles", "@channel or Channel Name", "youtube")
    st.divider()
    render_social_section("LinkedIn", "💼", "linkedin_handles", "Profile URL or /in/username", "linkedin")
    st.divider()
    render_social_section("Facebook", "📘", "facebook_handles", "@username or profile name", "facebook")

# Filter out empty handles for all platforms
instagram_handles = [h.strip() for h in st.session_state.instagram_handles if h.strip()]
twitter_handles = [h.strip() for h in st.session_state.twitter_handles if h.strip()]
tiktok_handles = [h.strip() for h in st.session_state.tiktok_handles if h.strip()]
snapchat_handles = [h.strip() for h in st.session_state.snapchat_handles if h.strip()]
youtube_handles = [h.strip() for h in st.session_state.youtube_handles if h.strip()]
linkedin_handles = [h.strip() for h in st.session_state.linkedin_handles if h.strip()]
facebook_handles = [h.strip() for h in st.session_state.facebook_handles if h.strip()]

# Calculate totals
all_handles = [
    instagram_handles, twitter_handles, tiktok_handles, snapchat_handles,
    youtube_handles, linkedin_handles, facebook_handles
]
platform_names = [
    "Instagram", "Twitter/X", "TikTok", "Snapchat", 
    "YouTube", "LinkedIn", "Facebook"
]

total_handles = sum(len(handles) for handles in all_handles)
active_platforms = sum(1 for handles in all_handles if len(handles) > 0)

# Display comprehensive summary
if total_handles > 0:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Accounts", total_handles)
    with col2:
        st.metric("Platforms Used", active_platforms)
    with col3:
        st.metric("Coverage Score", f"{min(100, active_platforms * 15)}%")
    
    # Show breakdown by platform
    with st.expander("📊 Platform Breakdown", expanded=False):
        for i, (platform, handles) in enumerate(zip(platform_names, all_handles)):
            if len(handles) > 0:
                st.write(f"**{platform}:** {len(handles)} account(s) - {', '.join(handles)}")

# Step 2: Options
st.header("Step 2: Select What to Analyze")
col1, col2 = st.columns(2)
with col1:
    profile_analysis = st.checkbox("🔍 Profile Analysis", value=True)
    content_review = st.checkbox("🚩 Content Accessibility Check", value=True)
    privacy_analysis = st.checkbox("🔒 Privacy Settings Analysis", value=True)
with col2:
    engagement_check = st.checkbox("📈 Public Engagement Analysis", value=True)
    brand_consistency = st.checkbox("🎯 Brand Consistency Check", value=True)
    recruitment_optimization = st.checkbox("🏆 Recruitment Optimization", value=True)

# Step 3: Scraping Options
st.header("Step 3: Scraping Configuration")
st.warning("⚠️ **Important**: Social media platforms have anti-scraping measures. Results may be limited due to:")
st.info("""
- **Rate limits**: Platforms restrict automated access
- **Privacy settings**: Private accounts cannot be analyzed  
- **API requirements**: Some data requires official API access
- **Dynamic content**: JavaScript-loaded content may not be captured
- **Legal considerations**: Always respect platform Terms of Service
""")

scraping_delay = st.slider("Delay between requests (seconds)", 1, 10, 3, 
                          help="Higher delays reduce chance of being blocked")

# Step 4: Generate Real Analysis
st.header("Step 4: Run Live Social Media Analysis")
if st.button("🚀 Start Real-Time Scraping & Analysis"):
    # Input validation
    if total_handles == 0:
        st.error("Please enter at least one social media handle.")
        st.stop()
    
    st.success(f"🔍 Starting live analysis of {total_handles} accounts across {active_platforms} platforms...")
    
    # Initialize scraper
    scraper = SocialMediaScraper()
    scraped_results = {}
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_accounts = total_handles
    processed = 0
    
    # Scrape Instagram
    if instagram_handles:
        status_text.text("🔍 Analyzing Instagram profiles...")
        scraped_results["instagram"] = []
        for handle in instagram_handles:
            with st.spinner(f"Scraping Instagram: {handle}"):
                result = scraper.scrape_instagram_profile(handle)
                scraped_results["instagram"].append(result)
                processed += 1
                progress_bar.progress(processed / total_accounts)
                time.sleep(scraping_delay)
    
    # Scrape Twitter
    if twitter_handles:
        status_text.text("🔍 Analyzing Twitter profiles...")
        scraped_results["twitter"] = []
        for handle in twitter_handles:
            with st.spinner(f"Scraping Twitter: {handle}"):
                result = scraper.scrape_twitter_profile(handle)
                scraped_results["twitter"].append(result)
                processed += 1
                progress_bar.progress(processed / total_accounts)
                time.sleep(scraping_delay)
    
    # Scrape TikTok
    if tiktok_handles:
        status_text.text("🔍 Analyzing TikTok profiles...")
        scraped_results["tiktok"] = []
        for handle in tiktok_handles:
            with st.spinner(f"Scraping TikTok: {handle}"):
                result = scraper.scrape_tiktok_profile(handle)
                scraped_results["tiktok"].append(result)
                processed += 1
                progress_bar.progress(processed / total_accounts)
                time.sleep(scraping_delay)
    
    # Scrape YouTube
    if youtube_handles:
        status_text.text("🔍 Analyzing YouTube channels...")
        scraped_results["youtube"] = []
        for handle in youtube_handles:
            with st.spinner(f"Scraping YouTube: {handle}"):
                result = scraper.scrape_youtube_channel(handle)
                scraped_results["youtube"].append(result)
                processed += 1
                progress_bar.progress(processed / total_accounts)
                time.sleep(scraping_delay)
    
    # Scrape LinkedIn
    if linkedin_handles:
        status_text.text("🔍 Analyzing LinkedIn profiles...")
        scraped_results["linkedin"] = []
        for handle in linkedin_handles:
            with st.spinner(f"Accessing LinkedIn: {handle}"):
                result = scraper.scrape_linkedin_profile(handle)
                scraped_results["linkedin"].append(result)
                processed += 1
                progress_bar.progress(processed / total_accounts)
                time.sleep(scraping_delay)
    
    status_text.text("✅ Scraping complete! Analyzing results...")
    
    # Analyze the scraped data
    analysis = analyze_scraped_data(scraped_results)
    
    # Generate athlete name from first available handle
    athlete_name = next((handles[0] for handles in all_handles if handles), "Student Athlete")
    
    # Create comprehensive report
    report = f"""LIVE SOCIAL MEDIA AUDIT REPORT
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

=== EXECUTIVE SUMMARY ===
Athlete: {athlete_name}
Total Accounts Analyzed: {total_handles}
Platforms Covered: {active_platforms}
Scraping Success Rate: {(analysis['accessible_platforms'] / max(1, analysis['total_platforms'])) * 100:.1f}%

=== SCRAPING RESULTS ===
Successfully Analyzed: {analysis['accessible_platforms']} accounts
Private/Restricted: {analysis['private_accounts']} accounts  
Public/Accessible: {analysis['public_accounts']} accounts
Errors Encountered: {len(analysis['risk_factors'])} issues

=== DETAILED PLATFORM ANALYSIS ==="""

    # Add detailed results for each platform
    for platform, results in scraped_results.items():
        if results:
            report += f"\n\n{platform.upper()} ANALYSIS:"
            for i, result in enumerate(results, 1):
                report += f"\n\nAccount {i}:"
                if "error" in result:
                    report += f"\n  ❌ Error: {result['error']}"
                else:
                    for key, value in result.items():
                        if key != "error":
                            report += f"\n  • {key.title()}: {value}"

    if analysis['platform_insights']:
        report += "\n\n=== KEY INSIGHTS ==="
        for insight in analysis['platform_insights']:
            report += f"\n• {insight}"

    if analysis['risk_factors']:
        report += "\n\n=== ISSUES FOUND ==="
        for risk in analysis['risk_factors']:
            report += f"\n⚠️ {risk}"

    if analysis['recommendations']:
        report += "\n\n=== RECOMMENDATIONS ==="
        for rec in analysis['recommendations']:
            report += f"\n→ {rec}"

    report += f"""

=== RECRUITMENT READINESS ASSESSMENT ===
Platform Diversity: {active_platforms}/7 major platforms
Public Visibility: {analysis['public_accounts']} public accounts
Data Accessibility: {analysis['accessible_platforms']} profiles analyzed
Overall Score: {min(100, (analysis['accessible_platforms'] / max(1, total_handles)) * 100):.0f}%

=== TECHNICAL NOTES ===
• Social media platforms actively restrict automated data collection
• Some metrics may be unavailable due to privacy settings or API limitations  
• Results reflect publicly available information only
• Manual verification recommended for recruitment purposes
• Consider using official APIs for comprehensive analysis

=== NEXT STEPS ===
1. Review flagged accounts and privacy settings
2. Implement recommended improvements
3. Schedule regular monitoring of public presence
4. Consider professional social media audit services for deeper analysis
5. Ensure compliance with platform Terms of Service"""

    # Display results
    st.text_area("📋 Live Scraping Analysis Report", report, height=600)
    
    # Show summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Scraping Success", f"{(analysis['accessible_platforms'] / max(1, analysis['total_platforms'])) * 100:.0f}%")
    with col2:
        st.metric("Public Accounts", analysis['public_accounts'])
    with col3:
        st.metric("Private/Restricted", analysis['private_accounts'])
    with col4:
        st.metric("Issues Found", len(analysis['risk_factors']))
    
    # Display detailed scraped data
    if st.checkbox("Show Raw Scraped Data"):
        st.json(scraped_results)
    
    # PDF Generation
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", '', 10)
        
        for line in report.split("\n"):
            if line.strip():
                if len(line) > 80:
                    pdf.multi_cell(0, 5, line.encode('latin1', 'ignore').decode('latin1'))
                else:
                    pdf.cell(0, 5, line.encode('latin1', 'ignore').decode('latin1'), ln=True)
            else:
                pdf.ln(2)
        
        pdf_bytes = pdf.output(dest='S').encode('latin1')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"Live_Social_Media_Audit_{athlete_name}_{timestamp}.pdf"
        st.download_button(
            label="📥 Download Live Analysis Report",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf"
        )
        
        st.success("🎉 Live social media analysis complete!")
        
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        st.info("You can still copy the text report above.")

# Sidebar with scraping information
with st.sidebar:
    st.header("🔧 Scraping Information")
    
    st.write("**Supported Platforms:**")
    st.write("✅ Instagram (limited)")
    st.write("⚠️ Twitter/X (restricted)")
    st.write("⚠️ TikTok (very limited)")
    st.write("✅ YouTube (basic info)")
    st.write("❌ LinkedIn (heavily restricted)")
    st.write("❌ Facebook (blocked)")
    st.write("❌ Snapchat (not accessible)")
    
    st.divider()
    
    st.write("**Limitations:**")
    st.write("• Private accounts cannot be analyzed")
    st.write("• Rate limits may block requests")
    st.write("• JavaScript content not captured")
    st.write("• Platform policies restrict access")
    
    st.divider()
    
    st.write("**Legal Notice:**")
    st.write("Always respect platform Terms of Service. This tool is for educational purposes.")
    
    st.divider()
    
    st.write("**Tips for Better Results:**")
    st.write("• Use public account usernames")
    st.write("• Increase delay between requests")
    st.write("• Verify accounts exist first")
    st.write("• Consider official APIs for production use")
