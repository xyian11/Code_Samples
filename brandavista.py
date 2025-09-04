import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import mplcursors

# Step 1: Load and clean data
df = pd.read_csv("/Users/thechez/Desktop/Avista_Analysis/Data/AvistaFinalMasterData.csv")
df.columns = df.columns.str.strip().str.replace(' ', '_')


# Normalize fields to avoid filtering issues
df['Electric_Utility'] = df['Electric_Utility'].astype(str).str.strip().str.upper()
df['Make'] = df['Make'].astype(str).str.strip()
df['City'] = df['City'].astype(str).str.strip()

# Step 2: Filter for AVISTA CORPORATION electric customers with valid Brand and City
df_filtered = df[
    (df['Electric_Utility'] == 'AVISTA CORPORATION') &
    df['Make'].notnull() &
    df['City'].notnull()
]

# Step 3: Group by City and Brand and count frequency
df_counts = df_filtered.groupby(['City', 'Make']).size().reset_index(name='Make_Count')

# Step 4: Create bubble plot
plt.figure(figsize=(35, 10))
scatter = sns.scatterplot(
    data=df_counts,
    x='City',
    y='Make',
    size='Make_Count',
    hue='Make_Count',  # Gradient color based on count
    palette='coolwarm', 
    sizes=(50, 1200),
    alpha=0.7,
    legend=False
)

# Add interactive tooltips
cursor = mplcursors.cursor(scatter.collections[0], hover=True)

@cursor.connect("add")
def on_add(sel):
    city = df_counts.iloc[sel.index]['City']
    brand = df_counts.iloc[sel.index]['Make']
    count = df_counts.iloc[sel.index]['Make_Count']
    sel.annotation.set_text(f"{brand} in {city}\nCount: {count}")

plt.title("Washing Machine Brand Frequency by City (AVISTA CORPORATION Electric Customers)", fontsize=20)
plt.xlabel("City")
plt.ylabel("Brand")
plt.xticks(rotation=45)
plt.tight_layout()
# Save the plot as a high-res PNG (before showing it)
plt.savefig("/Users/thechez/Desktop/Avista_Analysis/Analysis/Bubbleplot_by_Make-AVISTA/BubblePlot_BrandCity_AVISTA.png", dpi=300)
# Display the bubble plot
plt.show()
print("✅ Plot by Washing Machine Brand Frequency by City of Avista saved as BubblePlot_BrandCity_AVISTA.png")