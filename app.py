# Local LLM Integration using Ollama
import requests
import json

def use_local_llm_analysis(handles_data, athlete_name):
    """
    Uses local Ollama LLM for analysis
    Install: curl -fsSL https://ollama.ai/install.sh | sh
    Run: ollama pull llama2  # or another model
    """
    
    # Prepare prompt for local LLM
    prompt = f"""
    Analyze this social media presence for student-athlete {athlete_name}:
    
    Platforms and handles:
    """
    
    for platform, handles in handles_data.items():
        if handles:
            prompt += f"- {platform.replace('_handles', '')}: {len(handles)} accounts\n"
    
    prompt += """
    
    Please provide:
    1. Overall assessment (1-100 score)
    2. Top 3 recommendations  
    3. Risk assessment
    4. Recruitment readiness
    
    Keep response concise and focused on student-athlete needs.
    """
    
    try:
        # Call local Ollama API
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   "model": "llama2",  # or your preferred model
                                   "prompt": prompt,
                                   "stream": False
                               })
        
        if response.status_code == 200:
            result = response.json()
            return result['response']
        else:
            return None
            
    except requests.exceptions.RequestException:
        return None

# Fallback to rule-based if LLM unavailable
def hybrid_analysis(handles_data, athlete_name, audit_level):
    """
    Try local LLM first, fallback to rule-based analysis
    """
    
    # Try local LLM
    llm_result = use_local_llm_analysis(handles_data, athlete_name)
    
    if llm_result:
        return f"""
{athlete_name}'s AI-Powered Social Media Analysis

=== LOCAL AI ANALYSIS ===
{llm_result}

=== TECHNICAL DETAILS ===
Analysis Method: Local LLM (Ollama)
Model: Llama2
Processing Time: Real-time
Privacy: Complete - no data sent to external servers
        """
    else:
        # Fallback to rule-based
        from template_based_analyzer import generate_intelligent_report
        return generate_intelligent_report(handles_data, athlete_name, audit_level)[0]
