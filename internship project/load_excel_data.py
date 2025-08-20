import pandas as pd

# Charger le fichier Excel
file_path = 'Analysis.xls'
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

# Affichage complet
pd.set_option("display.max_rows", 266)
print("Data loaded successfully! Here are the first 266 rows:\n")
print(df.loc[0:266].to_string())

# Nettoyage des colonnes
for col in ['Crédit', 'Débit', 'Taux']:
    df[col] = df[col].fillna(0)

df['Crédit'] = df['Crédit'].astype(str).str.replace(',', '').str.strip()
df['Débit'] = df['Débit'].astype(str).str.replace(',', '').str.strip()

df['Crédit'] = pd.to_numeric(df['Crédit'], errors='coerce')
df['Débit'] = pd.to_numeric(df['Débit'], errors='coerce')

# Vérifier les types
print("\nTypes des colonnes :")
print(df[['Crédit', 'Débit', 'Taux']].dtypes)

# Calcul du profit
df['profit'] = df['Crédit'] - df['Débit']

# Afficher les 10 premières lignes avec le profit
print("\nAperçu des crédits, débits et profits :")
print(df[['Crédit', 'Débit', 'profit']].head(10))

# Calculs globaux
total_profit = df['profit'].sum()
avg_buy_rate = df[df['Débit'] > 0]['Taux'].mean()
avg_sell_rate = df[df['Crédit'] > 0]['Taux'].mean()

# Affichage final
print("\nTotal profit :", total_profit)
print("Taux moyen d'achat :", avg_buy_rate)
print("Taux moyen de vente :", avg_sell_rate)

print("\nNoms des colonnes dans le fichier Excel :")
print(df.columns)
