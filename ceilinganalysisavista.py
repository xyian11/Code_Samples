import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Load and clean data
df = pd.read_csv("/Users/thechez/Desktop/Avista_Analysis/Data/AvistaFinalMasterData.csv")
df.columns = df.columns.str.strip().str.replace(' ', '_')

# Normalize fields
df['Gas_Utility'] = df['Gas_Utility'].astype(str).str.strip().str.upper()
df['Ceiling_Type'] = df['Ceiling_Type'].astype(str).str.strip().str.replace('_', ' ')
df['Ceiling_Framing_Material'] = df['Ceiling_Framing_Material'].astype(str).str.strip().str.replace('_', ' ')
df['Ceiling_Insulation_Type_1'] = df['Ceiling_Insulation_Type_1'].astype(str).str.strip().str.replace('_', ' ')

# Filter for AVISTA gas customers and valid insulation types
df_filtered = df[
    (df['Gas_Utility'] == 'AVISTA') &
    df['Ceiling_Area'].notnull() &
    df['Ceiling_Insulation_Type_1'].notnull() &
    (df['Ceiling_Insulation_Type_1'].str.strip() != '')
].copy()

# Convert Ceiling_Area to numeric
df_filtered['Ceiling_Area'] = pd.to_numeric(df_filtered['Ceiling_Area'], errors='coerce')

# Rename columns for clarity
df_filtered = df_filtered.rename(columns={
    'Ceiling_Type': 'Ceiling Type',
    'Ceiling_Area': 'Ceiling Area',
    'Ceiling_Framing_Material': 'Ceiling Framing Material',
    'Ceiling_Insulation_Type_1': 'Ceiling Insulation Type'
})

with PdfPages("/Users/thechez/Desktop/Avista_Analysis/Analysis/CeilingArea/CeilingArea_AllPlots.pdf") as pdf:

    # Plot 1: Ceiling Type
    plt.figure(figsize=(16, 8))
    sns.violinplot(data=df_filtered, x='Ceiling Type', y='Ceiling Area', inner='quart', hue='Ceiling Type', palette='Set2')
    medians = df_filtered.groupby('Ceiling Type')['Ceiling Area'].median().round(1)
    new_labels = [f"{label}\nMedian: {medians[label]:.1f} ft²" for label in medians.index]
    plt.xticks(ticks=range(len(new_labels)), labels=new_labels)
    plt.title("Ceiling Area by Ceiling Type (AVISTA Gas Customers)")
    plt.tight_layout()
    plt.savefig("/Users/thechez/Desktop/Avista_Analysis/Analysis/CeilingArea/CeilingArea_by_Type.png", dpi=1200)  # PNG
    pdf.savefig(dpi=1200)  # PDF
    plt.show()

    # Plot 2: Framing Material
    plt.figure(figsize=(16, 8))
    sns.violinplot(data=df_filtered, x='Ceiling Framing Material', y='Ceiling Area', inner='quart', hue='Ceiling Framing Material', palette='Set3')
    medians = df_filtered.groupby('Ceiling Framing Material')['Ceiling Area'].median().round(1)
    new_labels = [f"{label}\nMedian: {medians[label]:.1f} ft²" for label in medians.index]
    plt.xticks(ticks=range(len(new_labels)), labels=new_labels, rotation=45)
    plt.title("Ceiling Area by Framing Material (AVISTA Gas Customers)")
    plt.tight_layout()
    plt.savefig("/Users/thechez/Desktop/Avista_Analysis/Analysis/CeilingArea/CeilingArea_by_Framing.png", dpi=1200)
    pdf.savefig(dpi=1200)
    plt.show()

    # Plot 3: Insulation Type
    plt.figure(figsize=(16, 8))
    sns.violinplot(data=df_filtered, x='Ceiling Insulation Type', y='Ceiling Area', inner='quart', hue='Ceiling Insulation Type', palette='Pastel1')
    medians = df_filtered.groupby('Ceiling Insulation Type')['Ceiling Area'].median().round(1)
    new_labels = [f"{label}\nMedian: {medians[label]:.1f} ft²" for label in medians.index]
    plt.xticks(ticks=range(len(new_labels)), labels=new_labels, rotation=45)
    plt.title("Ceiling Area by Insulation Type (AVISTA Gas Customers)")
    plt.tight_layout()
    plt.savefig("/Users/thechez/Desktop/Avista_Analysis/Analysis/CeilingArea/CeilingArea_by_Insulation.png", dpi=1200)
    pdf.savefig(dpi=1200)
    plt.show()

