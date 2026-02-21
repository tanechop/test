import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import  streamlit as st
import plotly.express as px
import plotly.graph_objects as go

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
# convert colum to string
df['Crédit'] = df['Crédit'].astype(str).str.replace(',', '').str.strip()
df['Débit'] = df['Débit'].astype(str).str.replace(',', '').str.strip()
df['Solde'] = df['Solde'].astype(str).str.replace(',', '').str.strip()
df['Date Ope'] = df['Date Ope'].astype(str).str.replace(',', '').str.strip()
#convert string to float
df['Crédit'] = pd.to_numeric(df['Crédit'], errors='coerce')
df['Débit'] = pd.to_numeric(df['Débit'], errors='coerce')
df['Date Ope'] = pd. to_datetime(df['Date Ope'], errors='coerce')
df['Solde'] = pd.to_numeric(df['Solde'] , errors='coerce')
#remove row where the is no operation of Date Ope
df = df.dropna(subset=['Date Ope'])
# Vérifier les types
print("\nTypes des colonnes :")
print(df[['Crédit', 'Débit', 'Taux']].dtypes)

# Calcul du profit
df['balance'] = df['Crédit'] - df['Débit']

# Afficher les 10 premières lignes avec le profit
print("\nAperçu des crédits, débits  :")
print(df[['Crédit', 'Débit', 'balance']].head(10))


# Calculs globaux

avg_buy_rate = df[df['Débit'] > 0]['Taux'].sum()
avg_sell_rate = df[df['Crédit'] > 0]['Taux'].sum()


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
daily_transcation =df.groupby(df['Date Ope'].dt.date).size().reset_index(name="Transaction")
st.header("all Transcaction")
st.dataframe(df[['Date Ope','Crédit','Débit',"Taux","Solde"]])
st.subheader("Daily Transaction")
st.dataframe(daily_transcation)

df["Date only"] = df["Date Ope"].dt.date
# Ensure 'Date Ope' column is in datetime format
print(daily_transcation[daily_transcation['Date Ope'].isna()])

#getting the working directory of the load_excel_data.py
st.subheader("Key Performance Indicator(KPI)")
last_Solde =df['Solde'].iloc[-1]
last_Solde =df['Solde'].tail(1).values[0]
print("balance =" ,last_Solde)
balance =df['Solde'].iloc[-1]
initial_balance = 51626
st.write("column in file:",df.columns.tolist())
df_Crédit = pd.read_excel(file_path)
df_Débit = pd.read_excel(file_path)
df_Crédit.columns = df_Crédit.columns.str.strip().str.lower()

avg_rate = float(df["Taux"].mean())
total_Crédit = df['Crédit'].sum()
total_Débit = df['Débit'].sum()
df["profit"] = df["Crédit"] - df["Débit"]


uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx"])

daily_transcation['Date Ope'] = pd.to_datetime(daily_transcation['Date Ope'], errors='coerce')
daily_transcation['DateOnly'] = daily_transcation['Date Ope'].dt.date

if uploaded_file is not None:

    df = pd.read_excel(uploaded_file)
    col1, col2,col3,col4,col5,col6 = st.columns(6)

    columns=df.columns.tolist()
    col1.metric("Total Crédit (in)",f"{total_Crédit:,.5f}","532,231,21")
    col2.metric("Total Débit (out)",f"{total_Débit:,.5f}","519,081,44")
    
    col4.metric("avg.rate",f"{avg_rate:.3f}","173.301")
    with col3:
        st. metric("initiat Solde(DHS)", f"{initial_balance:,.0f}","51626")

       
        st.markdown("")
        st.dataframe(df.style.format({
            'Crédit':'{:.2f}',
            'Débit':'{:.2f}',
            'Solde':'{:.2f}',
            'avg rate':'{:.2f}'
            }))
    with col5:
       #we want to analyse our data  per month in a brieft way
        st. metric("final Solde(DHS)", f"{balance:,.0f}","1,366,603")
    
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
        #We want to determine the most frequent client+
st.header("Most Frequent Client")
import re
if "Libelle" in df.columns:
            Client_counts =df["Libelle"].value_counts()
            value_Client = Client_counts.index[0]
            value_count = Client_counts.iloc[0]
            st.success(f"the most frequent client is having **{value_count} transcation** witn ID 14000075.")
            st.write("Top 5 Clients:")
            st.table(Client_counts.head(5).reset_index().rename( columns={"index":"Client","Libelle":"Transaction"}))
else:
            st.warning("columns 'Libelle' not found in excel file.")

st.header("Daily Transaction over time")        
st.bar_chart(daily_transcation.set_index(daily_transcation["Date Ope"].dt.date) ["Transaction"])
daily_net = df.groupby("Date Ope").agg({'Crédit':'sum',"Débit":'sum'}).reset_index()
daily_net['Net Flow'] = daily_net['Crédit'] - daily_net['Débit']
daily_net['balance'] = initial_balance + daily_net['Net Flow'].cumsum()
st.header("Balance(Solde) over time")
st.line_chart(daily_net.set_index(daily_net["Date Ope"].dt.date) ["balance"])

