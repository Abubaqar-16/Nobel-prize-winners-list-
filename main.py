import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

url = 'https://api.nobelprize.org/2.1/nobelPrizes?limit=100000'
r = requests.get(url)
prizes_list = r.json()['nobelPrizes']

def prize_info(one_entry):
    output = one_entry.copy()
    for key, value in output.items():
        if key == 'awardYear':
            output[key] = int(value)
        if isinstance(value, dict) and 'en' in value:
            output[key] = value['en']
        if key.startswith('date'):
            output[key] = pd.to_datetime(value)  # Convert individual date values to datetime
    for one_key in ['links', 'categoryFullName']:
        output.pop(one_key)
    return output

new_prizes_list = [prize_info(one_entry) for one_entry in prizes_list]
prizes_df = pd.DataFrame(new_prizes_list)

# Streamlit UI
st.title('Nobel Prize Data')

# Dropdown menu for selecting display type
display_type = st.selectbox('Select Display Type', ['Graph', 'List'])

if display_type == 'Graph':
    # Dropdown menu for selecting plot type
    plot_type = st.selectbox('Select Plot Type', ['Bar Chart', 'Line Chart'])

    # Generate the selected plot
    if plot_type == 'Bar Chart':
        st.subheader('Bar Chart')
        # Create a bar chart based on the data
        bar_data = prizes_df['category'].value_counts()
        plt.figure(figsize=(10, 6))
        plt.bar(bar_data.index, bar_data.values)
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Category')
        plt.ylabel('Number of Prizes')
        plt.tight_layout()
        st.pyplot(plt)

    elif plot_type == 'Line Chart':
        st.subheader('Line Chart')
        # Create a line chart based on the data
        line_data = prizes_df.groupby('awardYear').size()
        plt.figure(figsize=(10, 6))
        plt.plot(line_data.index, line_data.values, marker='o', color='b')
        plt.xlabel('Year')
        plt.ylabel('Number of Prizes')
        plt.grid(True)
        plt.tight_layout()
        st.pyplot(plt)

elif display_type == 'List':
    st.subheader('List of Nobel Prize Winners')
    st.dataframe(prizes_df)
