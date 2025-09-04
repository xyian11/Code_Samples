import pandas as pd
import plotly.express as px

# Load and clean your data
df = pd.read_csv("/Users/thechez/Desktop/Avista_Analysis/Data/AvistaFinalMasterData.csv")
df.columns = df.columns.str.strip().str.replace(' ', '_')

# Normalize and filter
df['Gas_Utility'] = df['Gas_Utility'].astype(str).str.strip().str.upper()
df['Ceiling_Type'] = df['Ceiling_Type'].astype(str).str.strip()
df_filtered = df[
    (df['Gas_Utility'] == 'AVISTA') &
    df['Ceiling_Area'].notnull() &
    (df['Ceiling_Type'].str.upper() != 'UNKNOWN')
].copy()

# Convert Ceiling_Area to numeric
df_filtered['Ceiling_Area'] = pd.to_numeric(df_filtered['Ceiling_Area'], errors='coerce')

# Plotly violin plot with color by Ceiling_Type
fig = px.violin(
    df_filtered,
    x='Ceiling_Type',
    y='Ceiling_Area',
    color='Ceiling_Type',  # 🎨 This assigns a unique color to each type
    box=True,
    points='all',
    hover_data=['Ceiling_Framing_Material', 'Ceiling_Insulation_Type_1'],
    title="Ceiling Area by Ceiling Type (AVISTA Gas Customers)"
)

fig.show()
