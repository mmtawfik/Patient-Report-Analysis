#importing Labraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import scipy
import streamlit as st
import plotly.express as px
import altair as alt
from io import BytesIO
import base64
import zipfile36 as zipfile
import openpyxl
from PyInstaller.utils.hooks import copy_metadata
datas = copy_metadata('streamlit')

##
##
# The Title of App 
st.title('Patient Report Analysis - Integrakare')

# Reset page button
if st.button('Reset Page'):
    st.experimental_rerun()

# Upload Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

# Read Excel file if uploaded
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, engine='openpyxl', usecols=["Date", "Date_Time", "Temperature (°C)", "Heart Rate", "systolic blood pressure", "diastolic blood pressure", "Oxygen Saturation"])
    
    # Show DataFrame
    st.write(df)

    
    # Convert 'Date_Time' column to datetime object
    df['Date_Time'] = pd.to_datetime(df['Date_Time'])


    # Convert 'Date_Time' column to datetime object
    df['Date_Time'] = pd.to_datetime(df['Date_Time'])

    # Create line plot of heart rate over time using Seaborn
    fig, ax = plt.subplots(figsize=(14, 10))
    sns.lineplot(x="Date_Time", y="Heart Rate", data=df, ax=ax, color='blue', label='Heart Rate')
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Heart Rate (BPM)', fontsize=18)
    ax.set_title('Heart Rate over Time', fontsize=20)
    ax.legend(fontsize=16, markerscale=2)

    # Show x-axis ticks for each day
    days = pd.date_range(start=df['Date_Time'].min().date(), end=df['Date_Time'].max().date(), freq='D')
    plt.xticks(days, [day.date() for day in days], rotation=60, ha='right', fontsize=16)

    st.write("Line plot of heart rate over time:")
    st.pyplot(fig)
    

    # Create line plot of average blood pressure over time using Seaborn
    bp_df = df.groupby("Date")["systolic blood pressure", "diastolic blood pressure"].mean().reset_index()
    bp_df_melted = pd.melt(bp_df, id_vars=["Date"], value_vars=["systolic blood pressure", "diastolic blood pressure"], var_name="Blood Pressure Type", value_name="Blood Pressure Value")
    fig, ax = plt.subplots(figsize=(14,10))
    sns.lineplot(x="Date", y="Blood Pressure Value", hue="Blood Pressure Type", data=bp_df_melted, ax=ax)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Blood Pressure (mm Hg)', fontsize=18)
    ax.set_title('Average Blood Pressure over Time', fontsize=20)
    ax.legend(fontsize=16, markerscale=2)
    st.pyplot(fig)
     
    # Create line plot of average blood pressure over time using Seaborn
    bp_df = df.groupby("Date")["systolic blood pressure", "diastolic blood pressure"].mean().reset_index()
    bp_df_melted = pd.melt(bp_df, id_vars=["Date"], value_vars=["systolic blood pressure", "diastolic blood pressure"], var_name="Blood Pressure Type", value_name="Blood Pressure Value")
    fig, ax = plt.subplots(figsize=(14,10))
    sns.lineplot(x="Date", y="Blood Pressure Value", hue="Blood Pressure Type", data=bp_df_melted, ax=ax)
    
        
    
    
    
    # Create line plot of heart rate over time using Seaborn
    hr_df = df.groupby("Date")["Heart Rate"].mean().reset_index()
    sns.lineplot(data=hr_df, x="Date", y="Heart Rate", color="red", label="Heart Rate", ax=ax)
    ax.set_xlabel('Date', fontsize=18)
    ax.set_ylabel('Measurement Value', fontsize=18)
    ax.set_title('Average Blood Pressure and Heart Rate over Time', fontsize=20)
    ax.legend(fontsize=16, markerscale=2)
    st.pyplot(fig)
   

    # create the plot Oxygen Saturation
    
    # set style and palette
    sns.set_style("whitegrid")
    sns.set_palette("husl")

    # create the plot
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.lineplot(x="Date_Time", y="Oxygen Saturation", data=df, ax=ax, color='blue')
    sns.scatterplot(x="Date_Time", y="Oxygen Saturation", data=df, ax=ax, color='red')
    ax.set_xlabel('Date')
    ax.set_ylabel('Oxygen Saturation (%)')  # add percentage sign to y-axis label
    ax.set_title('Oxygen Saturation over Time')
    plt.xticks(rotation=45)

    # set y-axis tick labels as percentages without repeating values and in the range of 97% to 101%
    vals = np.arange(0.97, 1.00, 0.01)  # set y-axis tick values as multiples of 1%
    ax.set_yticks(vals)
    ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])

    # display the plot in Streamlit
    st.pyplot(fig)
          
        
    # Create histogram of temperature measurements using Matplotlib and Seaborn
    plt.figure(figsize=(18, 16))
    sns.histplot(data=df, x='Temperature (°C)', bins=20, kde=True, color='blue')
    plt.title('Distribution of Body Temperatures', fontsize=24)
    plt.xlabel('Temperature (°C)', fontsize=22)
    plt.ylabel('Frequency', fontsize=22)
    plt.xticks(fontsize=22)
    plt.yticks(fontsize=22)
    plt.grid(axis='y', alpha=0.75)

    # Add a vertical line for the median temperature
    median_temp = df['Temperature (°C)'].median()
    plt.axvline(x=median_temp, color='red', linestyle='--', label=f'Median Temperature: {median_temp:.2f}°C')

    # Add a vertical line for the mean temperature
    mean_temp = df['Temperature (°C)'].mean()
    plt.axvline(x=mean_temp, color='green', linestyle='--', label=f'Mean Temperature: {mean_temp:.2f}°C')

    # Set the limits of the y-axis and x-axis
    plt.ylim(0, 50)
    plt.xlim(35.8, 38)

    # Add a legend to the plot
    plt.legend(fontsize=18)

    st.pyplot(plt)
    # Download all images button
    if st.button('Download all images'):
        # Create a ZipFile object to store the images
        img_zip = BytesIO()
        with zipfile.ZipFile(img_zip, mode='w') as zipf:
            # Loop through all the figures and save them as PNG images to the ZipFile object
            for i, fig in enumerate(plt.get_fignums()):
                buffer = BytesIO()
                plt.figure(fig).savefig(buffer, format='png')
                zipf.writestr(f'plot{i+1}.png', buffer.getvalue())

        # Encode the ZipFile object as a base64 string
        img_zip_base64 = base64.b64encode(img_zip.getvalue()).decode()

        # Create an HTML download link for the ZipFile
        href = f'<a href="data:application/zip;base64,{img_zip_base64}" download="plots.zip">Download all images</a>'

        # Display the download link
        st.markdown(href, unsafe_allow_html=True)

else:
    st.write("Please upload an Excel file.")
