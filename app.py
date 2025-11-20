import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from faker import Faker
import random
import time

# --- Konfiguration ---
st.set_page_config(
    page_title="Humlab Mission Control",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initiera Faker för svenska data
fake = Faker('sv_SE')

# --- Step A: Generate Deep Data (RPG Style) ---
def generate_data():
    # Real Humlab Repos grouped by "Teams"
    teams_structure = {
        "Welfare State Analytics": ["penelope", "welfare-state-analytics", "retriever"],
        "Digital Humanities": ["humlab-sead", "the_culture_of_international_relations", "disutrano"],
        "Infrastructure": ["cwb-container", "neatline-deployment"],
        "Tools": ["amazon-scraper", "excel-translator", "excel-translator-client"]
    }
    
    data = []
    
    for team, repos in teams_structure.items():
        # Team Level Stats (RPG Attributes)
        team_stats = {
            "Security": random.randint(40, 90),      # Cyber defense
            "Documentation": random.randint(30, 95), # Accessibility
            "Velocity": random.randint(20, 100),     # Speed of dev
            "Community": random.randint(10, 80)      # Open source love
        }
        
        for repo in repos:
            # Simulate compliance checks
            has_license = random.choice([True, True, True, False])
            vulns = random.randint(0, 5)
            last_update_days = random.randint(1, 200)
            
            # Calculate Score based on team stats + repo specifics
            base_score = (team_stats["Security"] + team_stats["Documentation"]) / 2
            score = base_score - (vulns * 5)
            if not has_license: score -= 20
            score = max(0, min(100, score))
            
            status = "🟢 Stable"
            if score < 50: status = "🔴 Critical"
            elif score < 80: status = "🟡 Warning"
            
            data.append({
                "Team": team,
                "Repository": repo,
                "Compliance_Score": int(score),
                "Vulnerabilities": vulns,
                "License": "✅" if has_license else "❌",
                "Status": status,
                "Last_Scan": f"{last_update_days}d ago",
                # Hidden stats for radar chart
                "Stat_Security": team_stats["Security"],
                "Stat_Docs": team_stats["Documentation"],
                "Stat_Velocity": team_stats["Velocity"],
                "Stat_Community": team_stats["Community"]
            })
            
    return pd.DataFrame(data)

# Ladda data
if 'df' not in st.session_state:
    st.session_state.df = generate_data()
    st.session_state.total_xp = st.session_state.df['Compliance_Score'].sum()
    st.session_state.actions_taken = 0
    st.session_state.achievements = []
    st.session_state.stats = {'vulns_fixed': 0, 'fikas': 0, 'hackathons': 0}
    # Active Quest System
    st.session_state.quest = {"title": "Operation: Open Science", "goal": 5, "current": 0, "desc": "Publicera 5 dataset eller repos öppet."}

df = st.session_state.df

# --- Helper: Game Logic ---
def perform_action(team_name, action_type):
    """Updates scores based on actions taken"""
    boost = 0
    msg = ""
    
    # Update Stats & Check Achievements
    if action_type == "fix_vuln":
        st.session_state.stats['vulns_fixed'] += 1
        boost = 10
        msg = "Säkerhetshål täppt! Systemet stabiliseras."
        # Update Radar Stat: Security
        if team_name != "Alla":
            st.session_state.df.loc[st.session_state.df['Team'] == team_name, 'Stat_Security'] += 5
            
    elif action_type == "docs":
        boost = 5
        msg = "Dokumentation uppdaterad. Kunskap säkrad."
        if team_name != "Alla":
            st.session_state.df.loc[st.session_state.df['Team'] == team_name, 'Stat_Docs'] += 5

    elif action_type == "social":
        st.session_state.stats['fikas'] += 1
        boost = 5
        msg = "Kaffe intaget. Moralen ökar!"
        if team_name != "Alla":
            st.session_state.df.loc[st.session_state.df['Team'] == team_name, 'Stat_Community'] += 5
            
    elif action_type == "hackathon":
        st.session_state.stats['hackathons'] += 1
        boost = 20
        msg = "HACKATHON! Velocity och Community maxas!"
        st.session_state.df['Stat_Velocity'] += 10
        st.session_state.df['Stat_Community'] += 10

    # Apply Score Boost
    if team_name == "Alla":
        st.session_state.df['Compliance_Score'] = st.session_state.df['Compliance_Score'].apply(lambda x: min(100, x + boost))
    else:
        mask = st.session_state.df['Team'] == team_name
        st.session_state.df.loc[mask, 'Compliance_Score'] = st.session_state.df.loc[mask, 'Compliance_Score'].apply(lambda x: min(100, x + boost))

    st.session_state.actions_taken += 1
    st.session_state.total_xp = st.session_state.df['Compliance_Score'].sum()
    
    # Quest Progress
    if st.session_state.quest['current'] < st.session_state.quest['goal']:
        st.session_state.quest['current'] += 1
        if st.session_state.quest['current'] >= st.session_state.quest['goal']:
            st.balloons()
            st.toast(f"QUEST COMPLETE: {st.session_state.quest['title']}! 🌟", icon="⚔️")
    
    return msg

# --- Step B: Visual Design & Layout ---

# Ultra-Modern CSS
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: linear-gradient(to bottom right, #0e1117, #1a1c24);
    }
    
    /* Card Styling */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #00CC96;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #00CC96, #36F1CD);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        font-size: 1rem;
        color: #a0a0a0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Humlab Mission Control")
st.markdown("### *Digital Research Infrastructure Status*")

# --- Top Level Stats (The "HUD") ---
col1, col2, col3, col4 = st.columns(4)

total_health = int(df['Compliance_Score'].mean())
vuln_count = df['Vulnerabilities'].sum()
active_repos = len(df)

with col1:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">System Health</div><div class="metric-value">{total_health}%</div></div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Active Repos</div><div class="metric-value">{active_repos}</div></div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Vulnerabilities</div><div class="metric-value" style="-webkit-text-fill-color: #FF4B4B;">{vuln_count}</div></div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="metric-card"><div class="metric-label">Ops Performed</div><div class="metric-value">{st.session_state.actions_taken}</div></div>""", unsafe_allow_html=True)

st.markdown("---")

# --- Main Content Tabs ---
tab1, tab2, tab3 = st.tabs(["🕸️ Team Radar", "📊 Leaderboard", "📂 Deep Dive"])

with tab1:
    st.header("Team Capabilities Analysis")
    col_radar1, col_radar2 = st.columns([1, 2])
    
    with col_radar1:
        st.markdown("Select a team to analyze their strengths and weaknesses.")
        radar_team = st.selectbox("Select Team for Analysis", df['Team'].unique())
        
        # Get stats for selected team (take first repo as proxy for team stats)
        team_row = df[df['Team'] == radar_team].iloc[0]
        
        st.info(f"""
        **Analysis for {radar_team}:**
        - 🛡️ **Security**: {team_row['Stat_Security']}
        - 📝 **Docs**: {team_row['Stat_Docs']}
        - ⚡ **Velocity**: {team_row['Stat_Velocity']}
        - 🤝 **Community**: {team_row['Stat_Community']}
        """)
        
    with col_radar2:
        categories = ['Security', 'Documentation', 'Velocity', 'Community']
        values = [team_row['Stat_Security'], team_row['Stat_Docs'], team_row['Stat_Velocity'], team_row['Stat_Community']]
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line_color='#00CC96'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )
        st.plotly_chart(fig_radar, use_container_width=True)

with tab2:
    st.header("🏆 Team Leaderboard")
    team_scores = df.groupby("Team")["Compliance_Score"].mean().reset_index().sort_values(by="Compliance_Score", ascending=True)
    
    fig_bar = px.bar(
        team_scores, 
        x="Compliance_Score", 
        y="Team", 
        orientation='h',
        text="Compliance_Score",
        color="Compliance_Score",
        color_continuous_scale=["#FF4B4B", "#FFD700", "#00CC96"],
        title="Average Compliance Score per Team"
    )
    fig_bar.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.header("Repository Deep Dive")
    teams = df['Team'].unique()
    for team in teams:
        with st.expander(f"📂 {team}", expanded=True):
            team_data = df[df['Team'] == team]
            cols = st.columns(len(team_data))
            for i, (index, row) in enumerate(team_data.iterrows()):
                with cols[i]:
                    st.markdown(f"**{row['Repository']}**")
                    st.caption(f"Last Scan: {row['Last_Scan']}")
                    st.write(f"Status: {row['Status']}")
                    st.write(f"License: {row['License']}")
                    st.progress(row['Compliance_Score'] / 100)

# --- Sidebar: Command Center ---
with st.sidebar:
    st.header("🛸 Command Center")
    
    # Quest Tracker
    st.markdown("### ⚔️ Active Quest")
    q = st.session_state.quest
    st.info(f"**{q['title']}**\n\n{q['desc']}")
    st.progress(q['current'] / q['goal'])
    st.caption(f"Progress: {q['current']}/{q['goal']}")
    
    st.markdown("---")
    st.markdown("### 🎮 Actions")
    
    all_teams = list(df['Team'].unique())
    selected_team = st.selectbox("Target Team:", all_teams + ["Alla"])
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🛡️ Patch Vuln"):
            perform_action(selected_team, "fix_vuln")
            st.toast("Security Patch Deployed!", icon="🛡️")
        if st.button("☕ Team Fika"):
            perform_action(selected_team, "social")
            st.toast("Morale Boosted!", icon="☕")
            
    with col_b:
        if st.button("📝 Update Docs"):
            perform_action(selected_team, "docs")
            st.toast("Knowledge Base Updated!", icon="📝")
        if st.button("🚀 Hackathon"):
            perform_action("Alla", "hackathon")
            st.toast("Velocity Maxed Out!", icon="🚀")

    st.markdown("---")
    st.markdown("### 📡 Live Log")
    for _ in range(3):
        st.text(f"[{fake.time()}] {fake.bs().capitalize()}")
