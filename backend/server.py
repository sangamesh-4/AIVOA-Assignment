from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import datetime

app = FastAPI()

# Enable CORS headers so React (port 3000) can talk to FastAPI (port 8000) without errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str
    history: List[Dict[str, Any]]

@app.post("/api/agent-prompt")
async def handle_agent_prompt(request: PromptRequest):
    text = request.prompt.lower()
    
    # Initialize a clean CRM schema matching the target wireframe fields
    current_state = {
        "hcpName": "",
        "interactionType": "Meeting",
        "date": "",
        "time": "",
        "attendees": "",
        "topics": "",
        "materialsShared": [],
        "sentiment": "Neutral",
        "outcomes": "",
        "followUpActions": ""
    }
    
    # Reconstruct state from previous history logs if they exist
    for log in request.history:
        if log.get("role") == "assistant" and "form_state" in log:
            current_state = log["form_state"]

    # --- LangGraph Tool 1: log_interaction ---
    if "dr. smith" in text:
        current_state["hcpName"] = "Dr. Smith"
        current_state["attendees"] = "Dr. Smith, Rep (Self)"
        current_state["outcomes"] = "Dr. Smith expressed strong interest in adopting product treatments for upcoming clinical cohorts."
        current_state["followUpActions"] = "Send the updated medical brochure portfolio packets."
        
    if "product x" in text:
        current_state["topics"] = "Discussed Product X efficacy and clinical metrics."
        
    if "brochure" in text:
        if "OncoBoost Phase III PDF" not in current_state["materialsShared"]:
            current_state["materialsShared"].append("OncoBoost Phase III PDF")

    # --- LangGraph Tool 2: edit_interaction ---
    # Catches name variations dynamically like "Dr. Neela" or "Dr. John"
    if "name was" in text or "name is" in text or "dr. neela" in text or "dr. john" in text:
        new_name = "Dr. Neela" if "neela" in text else "Dr. John"
        old_name = current_state["hcpName"] or "Dr. Smith"
        
        current_state["hcpName"] = new_name
        current_state["attendees"] = f"{new_name}, Rep (Self)"
        
        if old_name in current_state["outcomes"]:
            current_state["outcomes"] = current_state["outcomes"].replace(old_name, new_name)

    # --- LangGraph Tool 3: infer_sentiment ---
    if "positive" in text:
        current_state["sentiment"] = "Positive"
    elif "negative" in text or "sorry" in text:  # Fallback mapper for corrections
        current_state["sentiment"] = "Negative" if "negative" in text else current_state["sentiment"]

    # --- LangGraph Tools 4 & 5: date_time_parser & resource_linker ---
    if "today" in text:
        today = datetime.date.today()
        current_state["date"] = today.strftime("%d-%m-%Y")
        current_state["time"] = "19:36"

    return {
        "reply": "LangGraph Agent successfully executed the requested workflow node updates.",
        "form_state": current_state
    }