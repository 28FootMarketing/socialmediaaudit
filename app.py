# Template-Based Social Media Analyzer
import random
from datetime import datetime

class SocialMediaAnalyzer:
    def __init__(self):
        self.platform_weights = {
            'instagram': 20, 'tiktok': 18, 'twitter': 15, 'youtube': 17,
            'linkedin': 12, 'snapchat': 8, 'facebook': 10, 'twitch': 6,
            'discord': 4, 'threads': 8, 'bereal': 5, 'vsco': 7
        }
        
        self.recommendations_db = {
            'low_platforms': [
                "Expand to Instagram and TikTok for maximum reach",
                "Consider YouTube for longer content storytelling",
                "LinkedIn is crucial for recruitment visibility"
            ],
            'high_platforms': [
                "Focus on 3-5 core platforms rather than spreading thin",
                "Consolidate similar accounts for better engagement",
                "Create content cross-promotion strategy"
            ],
            'good_diversity': [
                "Great platform mix - maintain consistency",
                "Consider content calendar for coordination",
                "Leverage each platform's unique strengths"
            ]
        }
        
        self.risk_factors = [
            "Multiple accounts on same platform may dilute engagement",
            "Gaming platforms require careful content curation",
            "Professional platforms need different tone than casual ones",
            "Too many platforms can lead to inconsistent posting"
        ]

    def analyze_presence(self, handles_data, audit_level):
        total_handles = sum(len(handles) for handles in handles_data.values())
        active_platforms = sum(1 for handles in handles_data.values() if handles)
        
        # Calculate weighted score
        weighted_score = 0
        for platform, handles in handles_data.items():
            if handles:
                platform_key = platform.replace('_handles', '')
                weight = self.platform_weights.get(platform_key, 5)
                # More accounts = slightly lower efficiency score
                account_efficiency = max(0.5, 1 - (len(handles) - 1) * 0.2)
                weighted_score += weight * account_efficiency
        
        overall_score = min(100, int(weighted_score * 1.2))
        
        return {
            'overall_score': overall_score,
            'total_handles': total_handles,
            'active_platforms': active_platforms,
            'recommendations': self._get_recommendations(active_platforms, total_handles),
            'risk_assessment': self._assess_risks(handles_data),
            'platform_analysis': self._analyze_platforms(handles_data)
        }
    
    def _get_recommendations(self, platforms, handles):
        if platforms < 3:
            return random.sample(self.recommendations_db['low_platforms'], 
                               min(len(self.recommendations_db['low_platforms']), 3))
        elif platforms > 8:
            return random.sample(self.recommendations_db['high_platforms'],
                               min(len(self.recommendations_db['high_platforms']), 3))
        else:
            return random.sample(self.recommendations_db['good_diversity'],
                               min(len(self.recommendations_db['good_diversity']), 3))
    
    def _assess_risks(self, handles_data):
        risks = []
        
        # Check for multiple accounts per platform
        for platform, handles in handles_data.items():
            if len(handles) > 2:
                risks.append(f"Multiple {platform.replace('_handles', '')} accounts may confuse audience")
        
        # Check for gaming platforms
        if handles_data.get('twitch_handles') or handles_data.get('discord_handles'):
            risks.append("Gaming platforms require careful content curation for athlete brand")
            
        # Check for professional vs casual mix
        has_professional = bool(handles_data.get('linkedin_handles'))
        has_casual = bool(handles_data.get('snapchat_handles') or handles_data.get('bereal_handles'))
        
        if has_professional and has_casual:
            risks.append("Maintain different tones for professional vs casual platforms")
            
        return risks[:3]  # Limit to top 3 risks
    
    def _analyze_platforms(self, handles_data):
        analysis = {}
        
        platform_insights = {
            'instagram_handles': "High engagement potential - focus on visual storytelling",
            'tiktok_handles': "Viral content opportunities - stay on trend but authentic", 
            'twitter_handles': "Real-time engagement - great for live event coverage",
            'youtube_handles': "Long-form content builds deeper connections with audience",
            'linkedin_handles': "Professional networking - crucial for recruitment",
            'snapchat_handles': "Intimate friend circle - keep content authentic",
            'facebook_handles': "Community building - good for family/local supporters",
            'twitch_handles': "Gaming community - ensure content aligns with athlete image",
            'discord_handles': "Team coordination tool - maintain professional presence",
            'threads_handles': "Text-based discussions - share thoughts and engage",
            'bereal_handles': "Authentic moments - consistency is key to engagement",
            'vsco_handles': "Artistic expression - showcase creativity and aesthetics"
        }
        
        for platform, handles in handles_data.items():
            if handles:
                analysis[platform] = {
                    'account_count': len(handles),
                    'insight': platform_insights.get(platform, "Maintain consistent brand presence"),
                    'priority': 'High' if len(handles) == 1 else 'Medium' if len(handles) == 2 else 'Consider consolidating'
                }
        
        return analysis

# Usage in Streamlit:
def generate_intelligent_report(handles_data, athlete_name, audit_level):
    analyzer = SocialMediaAnalyzer()
    results = analyzer.analyze_presence(handles_data, audit_level)
    
    report = f"""
{athlete_name}'s Intelligent Social Media Analysis

=== SMART ANALYSIS RESULTS ===
Overall Presence Score: {results['overall_score']}/100
Active Platforms: {results['active_platforms']}
Total Accounts: {results['total_handles']}
Analysis Date: {datetime.now().strftime('%B %d, %Y')}

=== KEY RECOMMENDATIONS ==="""
    
    for i, rec in enumerate(results['recommendations'], 1):
        report += f"""
{i}. {rec}"""
    
    report += """

=== RISK ASSESSMENT ==="""
    
    if results['risk_assessment']:
        for risk in results['risk_assessment']:
            report += f"""
⚠️ {risk}"""
    else:
        report += """
✅ No significant risks identified - well-managed presence"""
    
    return report, results
