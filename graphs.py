import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import  streamlit as st
import os
st.set_page_config(page_title="📊  Exchange office Dashboard",layout="wide")
upload_file = st.file_uploader("Upload your excel file", type=["xlsx"])
if upload_file :
     df=pd.read_excel(upload_file)
     df["Date Ope"] =pd.to_datetime(df['Date Ope'])
     st.subheader("Rw data preview")
     st.dataframe(df.head())
     st.file_uploader(upload_file)
    
