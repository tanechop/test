import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import  streamlit as st
import os
# Charger le fichier Excel
file_path = 'Analysis.xls'
df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()
print(df.columns.tolist())
# Affichage complet
pd.set_option("display.max_rows", 1000)
print("Data loaded successfully! Here are the first 966 rows:\n")
print(df.loc[0:1000].to_string())

# remplacé NAN avec 0
for col in ['Crédit', 'Débit', 'Taux']:
    df[col] = df[col].fillna(0)

df['Crédit'] = df['Crédit'].astype(str).str.replace(',', '').str.strip()
df['Débit'] = df['Débit'].astype(str).str.replace(',', '').str.strip()
df['Solde'] = df['Solde'].astype(str).str.replace(',', '').str.strip()
df['Date Ope'] = df['Date Ope'].astype(str).str.replace(',', '').str.strip()

df['Crédit'] = pd.to_numeric(df['Crédit'], errors='coerce')
df['Débit'] = pd.to_numeric(df['Débit'], errors='coerce')
df['Date Ope'] = pd.to_numeric(df['Date Ope'], errors='coerce')
df['Solde'] = pd.to_numeric(df['Solde'] , errors='coerce')
# Vérifier les types
print("\nTypes des colonnes :")
print(df[['Crédit', 'Débit', 'Taux']].dtypes)

# Calcul du profit
df['balance'] = df['Crédit'] - df['Débit']

# Afficher les 10 premières lignes avec le profit
print("\nAperçu des crédits, débits et profits :")
print(df[['Crédit', 'Débit', 'balance']].head(10))


# Calculs globaux

avg_buy_rate = df[df['Débit'] > 0]['Taux'].mean()
avg_sell_rate = df[df['Crédit'] > 0]['Taux'].mean()


# Affichage final

print("Taux moyen d'achat :", avg_buy_rate)
print("Taux moyen de vente :", avg_sell_rate)

print("\nNoms des colonnes dans le fichier Excel :")
print(df.columns)
import matplotlib.pyplot as plt
fig, ax = plt.subplots()

df['Solde'].plot(title='profit over time')
plt.show()
df['Date Ope'] = pd.to_datetime(df['Date Ope'])
#regroupe la date par jour et calculé la sum et la moyen

daily_avg_buy_rate = df[df['Débit'] > 0].groupby('Date Ope')['Taux'].mean()
daily_avg_sell_rate = df[df['Débit'] > 0].groupby('Date Ope')['Taux'].mean()
# set page configuration
st. set_page_config(page_title="Data Visualiser",layout="centered",page_icon="📊")
#title
st.title("📊Data visauliser .  App")
#getting the working directory of the load_excel_data.py
st.subheader("Key Performance Indicator(KPI)")

balance= float(df['Solde'].sum() )

total_Débit =float(df[df['Débit'] > 0]['Taux'].mean())
total_Crédit = float(df[df['Crédit'] > 0]['Taux'].mean())
profit = float(total_Débit - total_Crédit)
avg_rate = float(df["Taux"].mean())
uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx"])

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)
    col1, col2,col3,col4,col5,col6 = st.columns(6)

    columns=df.columns.tolist()
    col1.metric("Total Crédit (in)",f"{total_Crédit:,.5f}","173.4")
    col2.metric("Total Débit (out)",f"{total_Débit:,.5f}","171.7")
    
    col4.metric("avg.rate",f"{avg_rate:.3f}","172.9")
    with col3:
        st.metric("balance", f"{balance:,.5f}","582,684,460")
        st.markdown("")
        st.dataframe(df.style.format({
            'Crédit':'{:.2f}',
            'Débit':'{:.2f}',
            'Solde':'{:.2f}',
            'avg rate':'{:.2f}'
            }))
        col5.metric(label="Profit", value=f"{profit:,.5f}")
       #we want to analyse our data  per month in a brieft way
        st.markdown("--")
        st.subheader(" Monthly Analysis qauntity")
        df["Date Ope"] =  pd.to_datetime(df["Date Ope"],errors='coerce')
        df["Month"] = df["Date Ope"].dt.month
        monthly = df.groupby('Month').agg(
            Crédit=("Crédit","sum"),
            Débit=("Débit","sum"),
            Net= ("Solde","sum"),
            ops=("Solde","count"),
        ).reset_index()
        st.dataframe(monthly)
        fig, ax = plt.subplots()
ax.plot(df["Date Ope"], df["Solde"], marker='o')
ax.set_title("Solde over Time")
ax.set_xlabel("Date")
ax.set_ylabel("Solde")
plt.xticks(rotation=45)
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(fig)


      
        
        
        #We want to determine the most frequent client
st.header("Most Frequent Client")
if "Libelle" in df.columns:
            Client_counts =df["Libelle"].value_counts()
            value_Client = Client_counts.index[0]
            value_count = Client_counts.iloc[0]
            st.success(f"the most frequent client is having **{value_count}transcation**.")
            st.write("Top 5 Clients:")
            st.table(Client_counts.head(5).reset_index().rename( columns={"index":"Client","Libelle":"Transaction"}))
else:
            st.warning("columns 'Libelle' not found in excel file.")
            



