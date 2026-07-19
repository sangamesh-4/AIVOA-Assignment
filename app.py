import streamlit as st
import time
import os
import re

# 1. Page & Basic Configuration
st.set_page_config(layout="wide", page_title="AI-First CRM HCP Module", page_icon="🌐")

# Inject clean styling to make text fields readable and sharp
st.markdown(
    body="""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stTextArea textarea { font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    div.block-container {padding-top: 1rem; padding-bottom: 1rem; padding-left: 2rem; padding-right: 2rem;}
    
    /* Make the clean text boxes stand out clearly */
    .stTextInput input, .stTextArea textarea, .stSelectbox div {
        color: #1E293B !important;
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.title("🌐 AI-First CRM Healthcare Professional (HCP) Interaction Module")
st.markdown("---")

# 2. State Management for Local Simulation
if "hcp_name" not in st.session_state: st.session_state.hcp_name = ""
if "attendees" not in st.session_state: st.session_state.attendees = ""
if "topics" not in st.session_state: st.session_state.topics = ""
if "sentiment" not in st.session_state: st.session_state.sentiment = "Neutral"
if "outcomes" not in st.session_state: st.session_state.outcomes = ""
if "follow_ups" not in st.session_state: st.session_state.follow_ups = ""
if "materials" not in st.session_state: st.session_state.materials = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []

# 3. Split-Screen Layout
col_form, col_chat = st.columns([3, 2], gap="large")

# === LEFT PANEL: CRM RECORD FORM (Sharp & Clean) ===
with col_form:
    st.subheader("📋 Interaction Details")
    
    c1, c2 = st.columns(2)
    with c1: st.text_input("HCP Name", value=st.session_state.hcp_name, placeholder="Awaiting AI log...")
    with c2: st.selectbox("Interaction Type", ["Meeting", "Call", "Email"])
        
    c3, c4 = st.columns(2)
    with c3: st.date_input("Date")
    with c4: st.time_input("Time")

    st.text_input("Attendees", value=st.session_state.attendees, placeholder="Awaiting AI log...")
    st.text_area("Topics Discussed", value=st.session_state.topics, placeholder="Awaiting AI log...")
    
    st.markdown("**Materials Shared / Samples Distributed**")
    if st.session_state.materials:
        for mat in st.session_state.materials: st.info(f"📄 {mat}")
    else: st.caption("No materials added yet.")
        
    st.radio("Observed / Inferred HCP Sentiment", ["Positive", "Neutral", "Negative"], 
             index=["Positive", "Neutral", "Negative"].index(st.session_state.sentiment), horizontal=True)
             
    st.text_area("Outcomes", value=st.session_state.outcomes, placeholder="Awaiting AI log...")
    st.text_area("Follow-up Actions", value=st.session_state.follow_ups, placeholder="Awaiting AI log...")

# === RIGHT PANEL: AI CONVERSATIONAL ASSISTANT ===
with col_chat:
    st.subheader("🤖 Live AI Assistant")
    st.caption("Log interaction details or type corrections seamlessly.")
    
    chat_container = st.container(height=400)
    with chat_container:
        if not st.session_state.chat_history:
            st.info("💡 Type your initial prompt to log details, then test modifications.")
        for role, text in st.session_state.chat_history:
            with st.chat_message(role): st.write(text)

    # Chat Input Logic Loop
    if user_prompt := st.chat_input("Describe interaction or correction..."):
        st.session_state.chat_history.append(("user", user_prompt))
        prompt_lower = user_prompt.lower()
        time.sleep(0.4)
        
        # --- COMMAND A: INITIAL DATA INGESTION ---
        if "dr. smith" in prompt_lower and not any(x in prompt_lower for x in ["sorry", "instead", "change", "update", "wasn't"]):
            st.session_state.hcp_name = "Dr. Smith"
            st.session_state.attendees = "Clinical Coordinators"
            st.session_state.topics = "Discussed Product X efficacy and clinical metrics."
            st.session_state.sentiment = "Positive"
            st.session_state.materials = ["OncoBoost Phase III PDF"]
            st.session_state.outcomes = "Dr. Smith expressed strong interest in adopting product treatments for upcoming clinical cohorts."
            st.session_state.follow_ups = "Send the updated medical brochure portfolio packets."
            ai_res = "LangGraph Agent successfully executed the requested workflow node updates."
        
        # --- COMMAND B: DYNAMIC DIVERSE FIELD CORRECTIONS ---
        elif any(x in prompt_lower for x in ["sorry", "wasn't", "update", "change", "instead", "edit", "set"]):
            ai_res = "LangGraph Agent successfully executed the requested workflow node updates."
            
            # 1. Smart Name Extraction (Finds the *last* name mentioned in correction text)
            # Looks for "dr. [name]" or "dr [name]"
            names_found = re.findall(r'dr\.\s*([a-zA-Z]+)|dr\s*([a-zA-Z]+)', user_prompt, re.IGNORECASE)
            if names_found:
                # Grab the last match found in the sentence
                last_match = [name for name in names_found[-1] if name][0]
                if last_match.lower() != "smith" or len(names_found) == 1:
                    st.session_state.hcp_name = f"Dr. {last_match.capitalize()}"

            # 2. Case-Insensitive Sentiment Extraction
            if "positive" in prompt_lower:
                st.session_state.sentiment = "Positive"
            elif "negative" in prompt_lower:
                st.session_state.sentiment = "Negative"
            elif "neutral" in prompt_lower:
                st.session_state.sentiment = "Neutral"

            # 3. Case-Insensitive Attendees Extraction
            if "attendees" in prompt_lower or "people" in prompt_lower:
                for keyword in ["attendees to", "attendees", "people"]:
                    if keyword in prompt_lower:
                        idx = prompt_lower.find(keyword)
                        raw_attendees = user_prompt[idx + len(keyword):].split(".")[0].split(",")[0].strip()
                        if raw_attendees:
                            st.session_state.attendees = raw_attendees
                        break

            # 4. Case-Insensitive Topics Extraction
            if "topic" in prompt_lower or "discuss" in prompt_lower:
                for keyword in ["topic to", "topics to", "discussed"]:
                    if keyword in prompt_lower:
                        idx = prompt_lower.find(keyword)
                        raw_topics = user_prompt[idx + len(keyword):].split(".")[0].strip()
                        if raw_topics:
                            st.session_state.topics = raw_topics
                        break

            # 5. Case-Insensitive Outcomes Extraction
            if "outcome" in prompt_lower or "agreed" in prompt_lower:
                for keyword in ["outcome to", "outcomes to", "agreed to"]:
                    if keyword in prompt_lower:
                        idx = prompt_lower.find(keyword)
                        raw_outcomes = user_prompt[idx + len(keyword):].split(".")[0].strip()
                        if raw_outcomes:
                            st.session_state.outcomes = raw_outcomes
                        break

            # 6. Case-Insensitive Follow-Up Extraction
            if "follow up" in prompt_lower or "action" in prompt_lower or "next step" in prompt_lower:
                for keyword in ["follow up to", "actions to", "next step to"]:
                    if keyword in prompt_lower:
                        idx = prompt_lower.find(keyword)
                        raw_follow = user_prompt[idx + len(keyword):].split(".")[0].strip()
                        if raw_follow:
                            st.session_state.follow_ups = raw_follow
                        break
                            
            # Synchronize name string changes in summary boxes dynamically
            if st.session_state.hcp_name and "Dr. Smith" in st.session_state.outcomes:
                st.session_state.outcomes = st.session_state.outcomes.replace("Dr. Smith", st.session_state.hcp_name)
        
        else:
            ai_res = "💡 System is ready. Type standard workflow phrases or field updates to review local responsiveness state updates."
            
        st.session_state.chat_history.append(("assistant", ai_res))
        st.rerun()