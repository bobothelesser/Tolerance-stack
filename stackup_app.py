import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Tolerance Stack-Up Visualizer")

st.title("🔧 Tolerance Stack-Up Visualizer")

st.markdown("Enter dimensions and their ± tolerances:")

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

total_length = sum(lengths)
worst_case = sum(tolerances)
rss = math.sqrt(sum(t**2 for t in tolerances))

st.markdown("### 📊 Results")
st.write(f"**Total Nominal Length:** {total_length:.2f} mm")
st.write(f"**Worst-Case Stack-Up:** ±{worst_case:.2f} mm")
st.write(f"**RSS Stack-Up:** ±{rss:.3f} mm")

# Optional chart
st.markdown("### 📈 Tolerance Breakdown")
df = pd.DataFrame({
    'Feature': [f'Feature {i+1}' for i in range(num_rows)],
    'Length (mm)': lengths,
    'Tolerance (± mm)': tolerances
})

st.bar_chart(df.set_index('Feature')['Tolerance (± mm)'])
