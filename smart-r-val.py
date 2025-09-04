import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm

# Load dataset
df = pd.read_csv("/Users/thechez/Desktop/Avista_Analysis/Data/AvistaFinalMasterData.csv")

# Clean column names
df.columns = df.columns.str.strip().str.replace(' ', '_')

# Filter for Smart Home Devices Present = YES and valid R-values
df_filtered = df[
    (df['Smart_Home_Devices_Present'].str.strip().str.upper() == 'YES') &
    df['Ceiling_Insulation_R-Value'].notnull() &
    (df['Ceiling_Insulation_R-Value'].astype(str).str.strip() != '')
].copy()

# Convert R-value to numeric
df_filtered['Ceiling_Insulation_R-Value'] = pd.to_numeric(df_filtered['Ceiling_Insulation_R-Value'], errors='coerce')

# Drop any rows with NaN after conversion
df_filtered = df_filtered.dropna(subset=['Ceiling_Insulation_R-Value'])

# Plot 1: Histogram of R-values
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(df_filtered['Ceiling_Insulation_R-Value'], bins=20, edgecolor='black', density=True)

# Apply gradient coloring
from matplotlib import cm
from matplotlib.colors import Normalize

norm = Normalize(vmin=min(bins), vmax=max(bins))
cmap = matplotlib.colormaps.get_cmap('viridis')

for bin_left, patch in zip(bins, patches):
    color = cmap(norm(bin_left))
    patch.set_facecolor(color)

# Overlay KDE using Seaborn
sns.kdeplot(df_filtered['Ceiling_Insulation_R-Value'], color='blue', linewidth=2)

plt.title("Ceiling Insulation R-Values (Smart Home Devices Present = YES)")
plt.xlabel("Ceiling Insulation R-Value")
plt.ylabel("Density")
plt.tight_layout()
plt.savefig("/Users/thechez/Desktop/Avista_Analysis/Analysis/SmartHomeR-Val/SmartHome_RValue_GradientHistogram_KDE.png", dpi=1200)
plt.show()

# Plot 2: Boxplot for R-values
plt.figure(figsize=(8, 4))
sns.boxplot(x=df_filtered['Ceiling_Insulation_R-Value'], color='lightgreen')
plt.title("Boxplot of Ceiling Insulation R-Values\n(Smart Home Devices Present = YES)")
plt.xlabel("Ceiling Insulation R-Value")
plt.tight_layout()
plt.savefig("/Users/thechez/Desktop/Avista_Analysis/Analysis/SmartHomeR-Val/SmartHome_RValue_Boxplot.png", dpi=1200)
plt.show()
print("✅ Distribution Plot Showing R-Value by Customers With Smart Devices saved as SmartHome_RValue_Histogram.png ")