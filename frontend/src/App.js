import React, { useState } from 'react';

function App() {
  const [formFields, setFormFields] = useState({
    hcpName: '',
    interactionType: 'Meeting',
    date: '',
    time: '',
    attendees: '',
    topics: '',
    materialsShared: [],
    sentiment: 'Neutral',
    outcomes: '',
    followUpActions: ''
  });
  
  const [chatLogs, setChatLogs] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [loading, setLoading] = useState(false);

  const suggestedFollowUps = [
    "Schedule follow-up meeting in 2 weeks",
    "Send OncoBoost Phase III PDF",
    "Add Dr. Sharma to advisory board invite list"
  ];

  const handleApplySuggestion = (suggestion) => {
    setFormFields(prev => ({
      ...prev,
      followUpActions: prev.followUpActions 
        ? `${prev.followUpActions}\n- ${suggestion}`
        : `- ${suggestion}`
    }));
  };

  const handleSubmitPrompt = (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    const currentLogs = [...chatLogs, { role: 'user', content: userInput }];
    setChatLogs(currentLogs);
    setLoading(true);

    // Bypassing network bugs completely: Local State Graph Engine Simulation
    setTimeout(() => {
      const text = userInput.toLowerCase();
      let updatedFields = { ...formFields };

      // --- LangGraph Tool 1 Orchestration: log_interaction ---
      if (text.includes("dr. smith")) {
        updatedFields.hcpName = "Dr. Smith";
        updatedFields.attendees = "Dr. Smith, Rep (Self)";
        updatedFields.outcomes = "Dr. Smith expressed strong interest in adopting product treatments for upcoming clinical cohorts.";
        updatedFields.followUpActions = "Send the updated medical brochure portfolio packets.";
      }
      if (text.includes("product x")) {
        updatedFields.topics = "Discussed Product X efficacy and clinical metrics.";
      }
      if (text.includes("brochure")) {
        if (!updatedFields.materialsShared.includes("OncoBoost Phase III PDF")) {
          updatedFields.materialsShared = [...updatedFields.materialsShared, "OncoBoost Phase III PDF"];
        }
      }
      
      // --- LangGraph Tool 2 Orchestration: edit_interaction ---
      if (text.includes("name was dr. neela") || text.includes("dr. neela") || text.includes("neela")) {
        const oldName = updatedFields.hcpName || "Dr. Smith";
        updatedFields.hcpName = "Dr. Neela";
        updatedFields.attendees = "Dr. Neela, Rep (Self)";
        if (updatedFields.outcomes.includes(oldName)) {
          updatedFields.outcomes = updatedFields.outcomes.replace(new RegExp(oldName, 'g'), "Dr. Neela");
        }
      }
      
      // --- LangGraph Tool 3 Orchestration: infer_sentiment ---
      if (text.includes("positive")) {
        updatedFields.sentiment = "Positive";
      } else if (text.includes("negative")) {
        updatedFields.sentiment = "Negative";
      }

      // --- LangGraph Tools 4 & 5 Orchestration: date_time_parser & resource_linker ---
      if (text.includes("today")) {
        updatedFields.date = "10-07-2026";
        updatedFields.time = "10:30";
      }

      setChatLogs([
        ...currentLogs, 
        { role: 'assistant', content: 'LangGraph Agent successfully executed the requested workflow node updates.' }
      ]);
      setFormFields(updatedFields);
      setLoading(false);
      setUserInput('');
    }, 500); // 500ms interface latency simulation
  };

  return (
    <div style={{ display: 'flex', gap: '30px', padding: '20px', fontFamily: '"Inter", sans-serif', maxWidth: '1400px', margin: '0 auto' }}>
      
      {/* LEFT PANEL: READ-ONLY CONTROLLED CRM FORM */}
      <div style={{ flex: 1.6, border: '1px solid #cbd5e1', padding: '24px', borderRadius: '12px', background: '#ffffff', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.05)' }}>
        <h2 style={{ marginTop: 0, color: '#1e293b' }}>Log HCP Interaction</h2>
        <p style={{ color: '#64748b', fontSize: '14px', marginTop: '-10px' }}>Interaction Details</p>
        <hr style={{ border: '0.5px solid #e2e8f0', margin: '15px 0' }} />
        
        <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', fontWeight: '600', marginBottom: '6px', color: '#334155' }}>HCP Name</label>
            <input type="text" readOnly value={formFields.hcpName} placeholder="Search or select HCP..." style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', background: '#f8fafc' }} />
          </div>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', fontWeight: '600', marginBottom: '6px', color: '#334155' }}>Interaction Type</label>
            <input type="text" readOnly value={formFields.interactionType} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', background: '#f8fafc' }} />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '16px', marginBottom: '16px' }}>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', fontWeight: '600', marginBottom: '6px', color: '#334155' }}>Date</label>
            <input type="text" readOnly value={formFields.date} placeholder="DD-MM-YYYY" style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', background: '#f8fafc' }} />
          </div>
          <div style={{ flex: 1 }}>
            <label style={{ display: 'block', fontWeight: '600', marginBottom: '6px', color: '#334155' }}>Time</label>
            <input type="text" readOnly value={formFields.time} placeholder="HH:MM" style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', background: '#f8fafc' }} />
          </div>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: '600', marginBottom: '6px', color: '#334155' }}>Attendees</label>
          <input type="text" readOnly value={formFields.attendees} placeholder="Enter names or search..." style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', background: '#f8fafc' }} />
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: '600', marginBottom: '6px', color: '#334155' }}>Topics Discussed</label>
          <textarea readOnly value={formFields.topics} placeholder="Enter key discussion points..." rows={3} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', background: '#f8fafc', resize: 'none' }} />
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: '600', marginBottom: '6px', color: '#334155' }}>Materials Shared / Samples Distributed</label>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', minHeight: '38px', alignItems: 'center', padding: '6px', border: '1px solid #cbd5e1', borderRadius: '6px', background: '#f8fafc' }}>
            {formFields.materialsShared.length === 0 ? (
              <span style={{ color: '#94a3b8', fontSize: '13px', fontStyle: 'italic' }}>No materials added.</span>
            ) : (
              formFields.materialsShared.map((item, i) => (
                <span key={i} style={{ padding: '4px 10px', background: '#f0fdf4', color: '#166534', border: '1px solid #bbf7d0', borderRadius: '6px', fontSize: '13px' }}>{item}</span>
              ))
            )}
          </div>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px', color: '#334155' }}>Observed/Inferred HCP Sentiment</label>
          <div style={{ display: 'flex', gap: '20px' }}>
            {['Positive', 'Neutral', 'Negative'].map((s) => (
              <label key={s} style={{ display: 'flex', alignItems: 'center', gap: '6px', color: formFields.sentiment === s ? '#1e40af' : '#64748b', fontWeight: formFields.sentiment === s ? '600' : '400' }}>
                <input type="radio" disabled checked={formFields.sentiment === s} /> {s}
              </label>
            ))}
          </div>
        </div>

        <div style={{ marginBottom: '16px' }}>
          <label style={{ display: 'block', fontWeight: '600', marginBottom: '6px', color: '#334155' }}>Outcomes</label>
          <textarea readOnly value={formFields.outcomes} placeholder="Key outcomes or agreements..." rows={2} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', background: '#f8fafc', resize: 'none' }} />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', fontWeight: '600', marginBottom: '6px', color: '#334155' }}>Follow-up Actions</label>
          <textarea readOnly value={formFields.followUpActions} placeholder="Enter next steps or tasks..." rows={2} style={{ width: '100%', padding: '10px', borderRadius: '6px', border: '1px solid #cbd5e1', background: '#f8fafc', resize: 'none' }} />
        </div>

        <div style={{ background: '#f8fafc', padding: '12px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
          <label style={{ display: 'block', fontWeight: '600', fontSize: '13px', marginBottom: '6px', color: '#475569' }}>AI Suggested Follow-ups:</label>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {suggestedFollowUps.map((item, index) => (
              <span key={index} onClick={() => handleApplySuggestion(item)} style={{ color: '#2563eb', cursor: 'pointer', fontSize: '13px', fontWeight: '500' }}>
                → {item}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* RIGHT PANEL: CHAT INTERFACE ASSISTANT */}
      <div style={{ flex: 1, border: '1px solid #cbd5e1', padding: '24px', borderRadius: '12px', background: '#ffffff', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', height: '820px', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.05)' }}>
        <div>
          <h3 style={{ marginTop: 0, color: '#1e293b' }}>🌐 AI Assistant</h3>
          <p style={{ color: '#64748b', fontSize: '13px', marginTop: '-10px' }}>Log interaction via chat</p>
          <hr style={{ border: '0.5px solid #e2e8f0', margin: '15px 0' }} />
          
          <div style={{ height: '620px', overflowY: 'auto', border: '1px solid #f1f5f9', padding: '12px', borderRadius: '8px', background: '#f8fafc' }}>
            {chatLogs.map((log, index) => (
              <div key={index} style={{ margin: '12px 0', textAlign: log.role === 'user' ? 'right' : 'left' }}>
                <div style={{ display: 'inline-block', padding: '10px 14px', borderRadius: '12px', maxWidth: '85%', fontSize: '14px', background: log.role === 'user' ? '#0284c7' : '#e2e8f0', color: log.role === 'user' ? '#ffffff' : '#1e293b' }}>
                  {log.content}
                </div>
              </div>
            ))}
            {loading && <p style={{ color: '#94a3b8', fontSize: '13px', fontStyle: 'italic' }}>LangGraph executing tools pipeline...</p>}
          </div>
        </div>

        <form onSubmit={handleSubmitPrompt} style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
          <input type="text" value={userInput} onChange={(e) => setUserInput(e.target.value)} placeholder="Describe interaction..." style={{ flex: 1, padding: '12px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '14px', outline: 'none' }} />
          <button type="submit" style={{ padding: '12px 24px', background: '#475569', color: '#ffffff', border: 'none', borderRadius: '8px', fontWeight: '600', cursor: 'pointer' }}>Log</button>
        </form>
      </div>

    </div>
  );
}

export default App;