import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc

st.title("Shot Chart Viewer")

# Upload CSVsss
uploaded_file = st.file_uploader("Upload your game shots CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload a CSV file to continues.")
    st.stop()

# Team selection
team = st.selectbox("Select Team", sorted(df['team'].dropna().unique()))

# PLAYER MULTISELECT WITH "All" OPTION
all_players = sorted(df[df['team'] == team]['player'].dropna().unique())
player_selection = st.multiselect("Select Player(s)", ["All"] + all_players, default=["All"])
players_filtered = all_players if "All" in player_selection else player_selection

# QUARTER MULTISELECT WITH "All" OPTION
df['quarter'] = df['quarter'].astype(str)  # Ensure quarters are strings for comparison
all_quarters = sorted(df[df['team'] == team]['quarter'].dropna().unique())
quarter_selection = st.multiselect("Select Quarter(s)", ["All"] + all_quarters, default=["All"])
quarters_filtered = all_quarters if "All" in quarter_selection else quarter_selection

# Filtered DataFrame
filtered_df = df[(df['team'] == team) & (df['player'].isin(players_filtered)) & (df['quarter'].isin(quarters_filtered))]

# Drawing functions
def draw_court(ax=None, color='#BBBBBB', lw=2, outer_lines=True):
    if ax is None:
        ax = plt.gca()
    hoop = Circle((0, -25), radius=22.86, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-90, -120), 180, -1, linewidth=lw, color=color)
    outer_box = Rectangle((-245, -157.5), 490, 580, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-180, -157.5), 360, 580, linewidth=lw, color=color, fill=False)
    top_free_throw = Arc((0, 422.5), 360, 360, theta1=0, theta2=180, linewidth=lw, color=color)
    bottom_free_throw = Arc((0, 422.5), 360, 360, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')
    restricted = Arc((0, 0), 250, 250, theta1=0, theta2=180, linewidth=lw, color=color)
    corner_three_a = Rectangle((-660, -157.5), 0, 305, linewidth=lw, color=color)
    corner_three_b = Rectangle((660, -157.5), 0, 305, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 1350, 1350, theta1=12, theta2=168, linewidth=lw, color=color)

    court_elements = [hoop, backboard, outer_box, inner_box, restricted, top_free_throw,
                      bottom_free_throw, corner_three_a, corner_three_b, three_arc]
    if outer_lines:
        court_elements.append(Rectangle((-750, -157.5), 1500, 1300, linewidth=lw, color=color, fill=False))
    for element in court_elements:
        ax.add_patch(element)
    return ax

# Plot
fig = plt.figure()
ax = draw_court(color="#BBBBBB", lw=2)

made = filtered_df[filtered_df['made'].str.contains('made', na=False)]
missed = filtered_df[filtered_df['made'].str.contains('missed', na=False)]

ax.plot(made['left'], made['bottom'], 'o', markersize=15, label='Made', color='#4caf50')
for _, row in missed.iterrows():
    ax.add_patch(plt.Circle((row['left'], row['bottom']), 15, color='white', zorder=2))
    ax.plot(row['left'], row['bottom'], 'x', markersize=10, markeredgewidth=3, color='#e57373', zorder=3)

ax.set_facecolor("#0d1b2a")
plt.xlim(-800, 800)
plt.ylim(-200, 1300)
plt.axis('off')
plt.title(f"Shot Chart - Team: {team}", fontsize=18, color="white", weight="bold")
plt.legend(frameon=True, loc='upper right', fontsize=14, facecolor="white", edgecolor="grey")

st.pyplot(fig)
