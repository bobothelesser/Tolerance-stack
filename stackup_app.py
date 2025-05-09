import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Tolerance Stack-Up Visualizer", layout="centered")
st.title("🔧 Tolerance Stack-Up Visualizer")
st.markdown("Enter dimensions and their ± tolerances:")

# Input form
num_rows = st.number_input("How many features?", min_value=1, max_value=20, value=3, step=1)
data = []

for i in range(num_rows):
    col1, col2 = st.columns(2)
    with col1:
        length = st.number_input(f"Length {i+1} (mm)", key=f"len_{i}")
    with col2:
        tol = st.number_input(f"Tolerance {i+1} (± mm)", key=f"tol_{i}")
    data.append((length, tol))

lengths = [d[0] for d in data]
tolerances = [d[1] for d in data]

# Results
total_length = sum(lengths)
worst_case = sum(tolerances)
rss = math.sqrt(sum(t**2 for t in tolerances))

st.markdown("### 📊 Results")
st.write(f"**Total Nominal Length:** {total_length:.2f} mm")
st.write(f"**Worst-Case Stack-Up:** ±{worst_case:.2f} mm")
st.write(f"**RSS Stack-Up:** ±{rss:.3f} mm")

# Chart 1: Individual tolerance bar chart
st.markdown("### 📈 Tolerance Breakdown")

fig, ax = plt.subplots(figsize=(8, 4))
features = [f'F{i+1}' for i in range(num_rows)]
bars = ax.bar(features, tolerances, color=['#4c72b0' if i % 2 == 0 else '#55a868' for i in range(num_rows)])

ax.set_ylabel("Tolerance (± mm)")
ax.set_xlabel("Feature")
ax.set_title("Feature-by-Feature Tolerance")
ax.grid(True, axis='y', linestyle='--', alpha=0.6)
ax.set_ylim(0, max(tolerances) * 1.4 if tolerances else 1)

# Label each bar
for bar, tol in zip(bars, tolerances):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, f"{tol:.2f}", 
            ha='center', va='bottom', fontsize=8)

st.pyplot(fig)

# Chart 2: Total stack-up range chart
st.markdown("### 📐 Overall Stack-Up Range")

fig2, ax2 = plt.subplots(figsize=(8, 2))
bar_y = 0.5
bar_height = 0.2

# Worst-case and RSS bars
ax2.barh(bar_y + 0.3, width=2 * worst_case, left=total_length - worst_case,
         height=bar_height, color='#d62728', alpha=0.6, label='Worst-Case Range')

ax2.barh(bar_y, width=2 * rss, left=total_length - rss,
         height=bar_height, color='#1f77b4', alpha=0.6, label='RSS Range')

# Nominal line
ax2.axvline(total_length, color='black', linestyle='--', label='Nominal Length')

ax2.set_yticks([bar_y, bar_y + 0.3])
ax2.set_yticklabels(['RSS', 'Worst Case'])
ax2.set_xlabel("Total Length (mm)")
ax2.set_xlim(total_length - worst_case * 1.5, total_length + worst_case * 1.5)
ax2.set_title("Stack-Up Total Range")
ax2.legend()
ax2.grid(True, axis='x', linestyle='--', alpha=0.5)

st.pyplot(fig2)

