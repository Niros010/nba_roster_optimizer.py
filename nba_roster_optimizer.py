# NBA Roster Optimizer by Nir Oron - Full Streamlit App
# Requirements: streamlit, pandas, matplotlib

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
import requests

st.set_page_config(page_title="NBA Roster Optimizer by Nir Oron", layout="wide")
st.markdown("# 🏀 NBA Roster Optimizer by Nir Oron")

# Load NBA player data (static CSV or online source)
@st.cache_data

def load_data():
    url = "https://raw.githubusercontent.com/basketball-reference/play-by-play-datasets/main/nba_clutch_sample.csv"
    df = pd.read_csv(url)
    return df

data = load_data()

# Filter example teams (demo: Boston, Lakers, Denver)
teams = data['Team'].dropna().unique()
team_selected = st.selectbox("Select a team", sorted(teams))
team_data = data[data['Team'] == team_selected]

st.subheader(f"Team Roster – {team_selected}")
st.dataframe(team_data.reset_index(drop=True), use_container_width=True)

# Function to plot radar chart for two players
def plot_radar(player1, player2):
    labels = ["Clutch Eff", "FTA", "AST", "STL", "REB"]
    keys = ["Clutch Efficiency Delta", "Clutch FTA Delta", "Clutch AST Delta", "Clutch STL Delta", "Clutch REB Delta"]
    
    p1 = team_data[team_data["Name"] == player1].iloc[0]
    p2 = team_data[team_data["Name"] == player2].iloc[0]

    values1 = [p1[k] for k in keys] + [p1[keys[0]]]
    values2 = [p2[k] for k in keys] + [p2[keys[0]]]
    angles = [n / float(len(labels)) * 2 * pi for n in range(len(labels))] + [0]

    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angles, values1, label=player1)
    ax.fill(angles, values1, alpha=0.3)
    ax.plot(angles, values2, label=player2)
    ax.fill(angles, values2, alpha=0.3)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("Clutch Radar Comparison")
    ax.legend()
    st.pyplot(fig)

# Dropdowns to select players for radar comparison
players = team_data['Name'].unique()
p1 = st.selectbox("Player 1", players, index=0)
p2 = st.selectbox("Player 2", players, index=1 if len(players) > 1 else 0)

if st.button("Compare Clutch Radar"):
    plot_radar(p1, p2)

# Basic slot matching (example logic)
st.subheader("📊 Slot Matching Overview")
slot_definitions = {
    "Clutch Performer": "Clutch Efficiency Delta",
    "Veteran Leader": "Playoff Games",
    "3&D Wing": "3PT%",
    "Defensive Anchor": "DEFRTG",
    "Hustle Role Player": "Deflections",
    "Shot Blocker": "BLK%",
    "Rebounder": "DRB%"
}

for slot, metric in slot_definitions.items():
    top_player = team_data.sort_values(by=metric, ascending=False).iloc[0]
    value = top_player[metric]
    st.markdown(f"**{slot}:** {top_player['Name']} – {metric}: `{value}`")
