import streamlit as st
import pandas as pd
import plotly.express as px

#reading and cleaning 2021 data and keeping 2021 and 2020 data
url="https://www.michigan.gov/msp/-/media/Project/Websites/msp/micr-assets/2021/Agency-Crime-Stats_2021.xlsx?rev=f073f9242f524c5188e8b7a4a459d2bc&hash=8CF27427D05B34CED651F41E9EE137C7"
df=pd.read_excel(url, sheet_name="Agency Crime Stats", header=1)
df=df.fillna(method="ffill")
df=df.iloc[1: , :]
df['ORI - Agency'] = df['ORI - Agency'].str.split('-').str[1]
df['MICR Offense'] = df['MICR Offense'].str.split('-').str[1]
df = df[df['MICR Offense'].str.contains("[Tt]otal") == False]
df = df[df["Crime Against"].str.contains("[Tt]otal") == False]
df = df[df['ORI - Agency'].str.contains("MSP") == False]
df['ORI - Agency'] = df['ORI - Agency'].str.replace('[Tt]otal', '')
df['ORI - Agency'] = df['ORI - Agency'].str.replace('[Gg]rand :', '')
df['ORI - Agency'] = df['ORI - Agency'].str.lstrip()
df['MICR Offense'] = df['MICR Offense'].str.lstrip()
old_cols = df.columns.values 
new_cols= ['ORI - Agency', "Crime Against", 'MICR Offense', '2021 Crimes', "2020 Crimes"]
df = df.reindex(columns=new_cols)

#reading and cleaning 2020 data and keeping 2019 data
url="https://www.michigan.gov/msp/-/media/Project/Websites/msp/micr-assets/2020/agency_crime_statistics_report.xlsx?rev=43577a0bfb944b199a6dda29ecd724cc&hash=402A6F33ED9EB223CAB01934C2335ACC"
df1=pd.read_excel(url, sheet_name="Agency Crime Stats", header=1)
df1=df1.fillna(method="ffill")
df1=df1.iloc[1: , :]
df1['ORI - Agency'] = df1['ORI - Agency'].str.split('-').str[1]
df1['MICR Offense'] = df1['MICR Offense'].str.split('-').str[1]
df1 = df1[df1['MICR Offense'].str.contains("[Tt]otal") == False]
df1 = df1[df1["Crime Against"].str.contains("[Tt]otal") == False]
df1 = df1[df1['ORI - Agency'].str.contains("MSP") == False]
df1['ORI - Agency'] = df1['ORI - Agency'].str.replace('[Tt]otal', '')
df1['ORI - Agency'] = df1['ORI - Agency'].str.replace('[Gg]rand :', '')
df1['ORI - Agency'] = df1['ORI - Agency'].str.lstrip()
df1['MICR Offense'] = df1['MICR Offense'].str.lstrip()
old_cols = df1.columns.values 
new_cols= ['ORI - Agency', "Crime Against", 'MICR Offense', '2019 Crimes']
df1= df1.reindex(columns=new_cols)
df1['2019 Crimes'] = df1['2019 Crimes'].astype(int)

df3=df[['ORI - Agency', "Crime Against", 'MICR Offense', '2021 Crimes']]

#Create dropdown with ori selector
ori_list = sorted(df3['ORI - Agency'].unique())
ori_selection = st.selectbox('Select an ORI - Agency:', ori_list, index=0)

#filtered data by ORI
filtered_df = df3[df3['ORI - Agency'] == ori_selection]
filtered_df=filtered_df.groupby('MICR Offense').sum()

# Display filtered data in Streamlit
st.write(f'### Michigan Crime Data (2021) - {ori_selection}')
st.write(filtered_df.style.set_table_styles([{'selector': 'thead', 'props': [('background-color', '#393939'), ('color', 'white')]}, {'selector': 'tbody', 'props': [('border-color', '#393939')]}]), full_width=True)


# Show bar chart of crime types for filtered data
st.write(f'### Top 5 Crimes - {ori_selection}')
crime_counts = filtered_df.nlargest(5, "2021 Crimes")
fig = px.pie(crime_counts, values='2021 Crimes', names=crime_counts.index)
st.plotly_chart(fig)



df4=df[df['ORI - Agency'] == ori_selection]
df4=df4.nlargest(1, '2021 Crimes')
filtered_df1=df1[df1["ORI - Agency"]==ori_selection]
filtered_df1=filtered_df1.nlargest(1, '2019 Crimes')
df4['2019 Crimes']=filtered_df1['2019 Crimes'].astype('int64')
st.write(df4)

# Create a line chart using Plotly Express



st.write('All data displayed is current as of 2021 as that is the most up-to-date publicly available Michigan crime data. Additional crime data can be found here: https://www.michigan.gov/msp/divisions/cjic/micr/annual-reports')
