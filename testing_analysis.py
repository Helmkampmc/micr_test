import streamlit as st
import pandas as pd
import plotly.express as px
import re

#reading and cleaning 2021 data and keeping 2021 and 2020 data
data = pd.read_excel('Agency Crime Stats_2021.xlsx', sheet_name='Agency Crime Stats', skiprows=1)
data=data.ffill()
data = data.iloc[1: , :]


data['Agency'] = data['ORI - Agency'].apply(lambda x: re.split('^(.*?)-', x, 1)[-1])
data['Criminal Offense'] = data['MICR Offense'].apply(lambda x: re.split('^(.*?)-', x, 1)[-1])

old_cols = data.columns.values 
new_cols= ['Agency', "Crime Against", 'Criminal Offense', "Offenses", 'Incidents', '2020 Crimes', "2021 Crimes"]
data = data.reindex(columns=new_cols)

data = data[data['Criminal Offense'].str.contains("[Tt]otal") == False]
data = data[data["Crime Against"].str.contains("[Tt]otal") == False]
data = data[data["Agency"].str.contains("MSP") == False]
data = data[data["Agency"].str.contains("County") == False]

data['Agency'] = data['Agency'].str.lstrip()
data['Criminal Offense'] = data['Criminal Offense'].str.lstrip()
data['Agency'] = data['Agency'].str.replace(" Grand Total:| Total:", "", regex=True).str.lstrip()
data['Criminal Offense'] = data['Criminal Offense'].replace('Nonaggravated Assault', 'Non-Aggravated Assault')

data22 = pd.read_excel('Agency Crime Stats_2022.xlsx', sheet_name='Agency Crime Stats', skiprows=1)
data22=data22.ffill()
data22 = data22.iloc[1: , :]

data22['Agency'] = data22['ORI - Agency'].apply(lambda x: re.split('^(.*?)-', x, 1)[-1])
data22['Criminal Offense'] = data22['MICR Offense'].apply(lambda x: re.split('^(.*?)-', x, 1)[-1])

old_cols = data22.columns.values 
new_cols= ['Agency', "Crime Against", 'Criminal Offense', "Offense", 'Incident', '2022 Crimes']
data22 = data22.reindex(columns=new_cols)

data22 = data22[data22['Criminal Offense'].str.contains("[Tt]otal") == False]
data22 = data22[data22["Crime Against"].str.contains("[Tt]otal") == False]
data22 = data22[data22["Agency"].str.contains("MSP") == False]
data22 = data22[data22["Agency"].str.contains("County") == False]

data22['Agency'] = data22['Agency'].str.lstrip()
data22['Criminal Offense'] = data22['Criminal Offense'].str.lstrip()
data22['Agency'] = data22['Agency'].str.replace(" Grand Total:| Total:", "", regex=True).str.lstrip()

# Merge the datasets on 'Agency' and 'Criminal Offense'
merged_data = pd.merge(data22, data[['Agency', 'Criminal Offense', '2021 Crimes', '2020 Crimes']], 
                       on=['Agency', 'Criminal Offense'], how='left')

# Replace NaN with 0 in the merged dataset
merged_data[['2021 Crimes', '2020 Crimes']] = merged_data[['2021 Crimes', '2020 Crimes']].fillna(0)

# If you want, you can also convert the '2021 Crimes' and '2020 Crimes' columns to integer after filling NaN
merged_data['2021 Crimes'] = merged_data['2021 Crimes'].astype(int)
merged_data['2020 Crimes'] = merged_data['2020 Crimes'].astype(int)

df3=data22[['Agency', "Crime Against", 'Criminal Offense', '2022 Crimes']]

#Create dropdown with ori selector
ori_list = sorted(df3['Agency'].unique())
ori_selection = st.selectbox('Select an Agency:', ori_list, index=0)

#filtered data by ORI
filtered_df = df3[df3['Agency'] == ori_selection]
filtered_df=filtered_df.groupby('Criminal Offense').sum()

# Display filtered data in Streamlit
st.write(f'### Michigan Crime Data (2022) - {ori_selection}')
st.write(filtered_df.style.set_table_styles([{'selector': 'thead', 'props': [('background-color', '#393939'), ('color', 'white')]}, {'selector': 'tbody', 'props': [('border-color', '#393939')]}]))



# Show bar chart of crime types for filtered data
st.write(f'### Top 5 Crimes - {ori_selection}')
crime_counts = filtered_df.nlargest(5, "2022 Crimes")
fig = px.pie(crime_counts, values='2022 Crimes', names=crime_counts.index)
st.plotly_chart(fig)


import plotly.express as px

# Filter merged_data DataFrame by ORI
filtered_merged_data = merged_data[merged_data['Agency'] == ori_selection]

# Melt the DataFrame to long-form to plot line chart for each year
melted_df = filtered_merged_data.melt(id_vars=['Agency', 'Criminal Offense', 'Crime Against', 'Offense', 'Incident'],
                                      value_vars=['2020 Crimes', '2021 Crimes', '2022 Crimes'],
                                      var_name='Year',
                                      value_name='Number of Crimes')

# Create the line graph
fig = px.line(melted_df,
              x='Year',
              y='Number of Crimes',
              color='Criminal Offense',
              title=f'Crime Trends Over Years for {ori_selection}',
              labels={'Number of Crimes': 'Number of Crimes', 'Year': 'Year'},
              line_shape='linear')

# Customize the layout if needed
fig.update_layout(autosize=True)

# Display the line graph in Streamlit
st.plotly_chart(fig)


# Create a line chart using Plotly Express



st.write('All data displayed is current as of 2022 as that is the most up-to-date publicly available Michigan crime data. Additional crime data can be found here: https://www.michigan.gov/msp/divisions/cjic/micr/annual-reports')
