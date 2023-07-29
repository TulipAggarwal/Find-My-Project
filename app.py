from st_on_hover_tabs import on_hover_tabs
import os
import openpyxl
import json
import requests
import streamlit as st
import time
import pandas as pd
import numpy as np
import smtplib
from email.message import EmailMessage
from streamlit_lottie import st_lottie
from st_aggrid import AgGrid
from datetime import datetime
import streamlit.components.v1 as components
import altair as alt
from annotated_text import annotated_text
import time
import streamlit as st

st.set_page_config(layout="wide")
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)

#Defining the side hover bar of the website
with st.sidebar:
    tabs = on_hover_tabs(tabName=['Home', 'App', 'Contact', 'About'], 
                         iconName=['home', 'code', 'mail', 'feed'],
                         styles = {'navtab': 
                                   {'background-color':'#111','color': '#D2DADA','font-size': '18px','transition': '.3s','white-space': 'nowrap','text-transform': 'capitalize'},
                                   'tabOptionsStyle': {':hover :hover': {'color': '#FFD700','cursor': 'pointer'}},
                                   'iconStyle':{'position':'fixed','left':'7.5px','text-align': 'left'},
                                   'tabStyle' : {'list-style-type': 'none','margin-bottom': '30px','padding-left': '30px'}}, 
                key="1")

#Defining the main home page of the website
if tabs =='Home':

    col1, col2 = st.columns(2)
    with col1:
        st.title("Welcome to Find My Project! ")
        st.subheader("A Project Recommendation Website")
        st.markdown("")
        st.markdown("Find My Project is a data powered website that suggests users the most appropriate project based on their chosen technology, language, tags and libraries.")
        st.markdown("The program scans through various projects hosted on GitHub to provide users with the best recommendations tailored to their needs. ")
        
    with col2:
        def load_lottieurl(url:str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        lottie_animation = load_lottieurl("https://lottie.host/2973be8b-d627-4cf1-9103-6cbcf7bc3f3a/HvqShH2SRQ.json")
        st_lottie(lottie_animation, key="animation")   

#Defining the main webpage page
elif tabs == 'App':
    st.title("Find My Project ")
    st.subheader("Enter the details below to Find Your Project! ")
    st.caption("Please wait while we get your potential recommendations ready for you!")
    st.markdown("")

    def load_data():
        data = pd.read_excel('Repositories_Final.xlsx', engine='openpyxl')
        return data
    data = load_data()

    #Creating the first filter using topic column
    topic_values = data["topic"].unique()

    search_value_topic = st.selectbox("Select a project topic that you are interested in: ", topic_values, format_func=lambda x: 'Select an option' if x == '.' else x)
    topic_data = data[data["topic"] == search_value_topic]

    #Creating the second filter using language column
    language_values = topic_data["language"].unique()
    search_value_language = st.selectbox("Select a language that you are interested in: ", sorted(language_values), format_func=lambda x: 'Select an option' if x == '.' else x)
    language_data = topic_data[topic_data["language"] == search_value_language]

    #Creating the third filter using tags column
    delimiter = ',' 
    column_with_multiple_entries = "tags"  
    combined_list = []
    language_data[column_with_multiple_entries] = language_data[column_with_multiple_entries].astype(str)
    for row in language_data[column_with_multiple_entries]:
        elements = [element.strip() for element in str(row).split(delimiter)]
        combined_list.extend(elements)

    #Extracted unique tags from the data so far filtered
    unique_tags_value = list(set(combined_list))

    search_value_tags = st.multiselect("Select the top 10 tags of your wish: ", sorted(unique_tags_value), max_selections=10, format_func=lambda x: 'Select an option' if x == '.' else x)
    tags_data = language_data[language_data["tags"].apply(lambda x: any(tag in x for tag in search_value_tags))]

    columns_to_display = ["name", "owner", "description", "stars", "link"]

    #Dictionary to map original column names to display names
    display_names = {
        "name": "Project Name",
        "owner": "Owner Name", 
        "description": "Description (if any)",       
        "stars": "Star Count",
        "link": "GitHub Repository Link"
    }
    
    tags_data_display = tags_data[columns_to_display].rename(columns=display_names)

    #Displaying the final table
    #Generate HTML table with center-aligned headers and without the index
    html_table = tags_data_display.to_html(render_links=True, escape=False, index=False)
    
    html_table = html_table.replace('<thead>', '<thead style="text-align: center;">')
    html_table = html_table.replace('<th>', '<th style="text-align: center;">')

    #Display the modified HTML table using Markdown
    st.markdown(html_table, unsafe_allow_html=True)

#Defining the contact page
elif tabs == 'Contact':
    col1, col2 = st.columns(2)
    with col1:
        st.title("Contact me! ")
        st.subheader('Fill out the form to contact me.')
        st.markdown("")
        
        def load_lottieurl(url:str):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()
        lottie_animation_1 = load_lottieurl("https://lottie.host/88388127-1326-42e4-825a-2688f1501dce/3gmaAzsf2L.json")
        st_lottie(lottie_animation_1, key="animation1")   
    
    with col2:
        st.title(" ")
        #Defining the form fields
        with st.form('Contact Form'):
            name = st.text_input('Name')
            email = st.text_input('Email')
            number = st.text_input('Phone Number')
            message = st.text_area('Message')
            submit_button = st.form_submit_button(label='Submit')

        #Processing the form submission
        if submit_button:
            print(f'Name: {name}')
            print(f'Email: {email}')
            print(f'Phone Number : {number}')
            print(f'Message: {message}')
            st.success('Thank you for reaching out to me. I will get back to you as soon as possible.')
            st.balloons()

#Defining the about page of the project
elif tabs == 'About':

    st.title("About Find My Project")
    st.markdown("### A deeper dive into the project!")

    st.markdown("#### Description")
    annotated_text("Find My Project is ", (" a data powered website ", " ", "#fea"), " that suggests users the most appropriate project based on their chosen technology, language, tags and libraries. The program scans through various projects hosted on GitHub to provide users with the best recommendations tailored to their needs. ")
    
    st.markdown("#### Motivation")
    annotated_text("Struggling to decide on the perfect engineering project is a common dilemma for every aspiring student. The vast array of technologies and endless possibilities can be overwhelming, leaving students unsure of where to begin their journey. This uncertainty can hinder creativity and hinder the development of critical skills. To address this challenge, I propose the creation of a unique and empowering project: ", (" Find My Project. ", " " , "#fea"), " The motivation behind this project is to provide a valuable solution that aids engineering students in discovering exciting and relevant project ideas based on their preferred technologies.")
    
    st.markdown("#### Goal")
    annotated_text("The primary goal of Find My Project is to ", (" inspire students and guide them towards projects that align with their interests and ambitions. ", " ", "#fea") ," Through a user-friendly web application, students will have the opportunity to input their preferred technologies and Find My Project will then fetch and display a collection of the ", (" most popular and admired projects", " ", "#fea"), " that match those criteria.") 
    
    st.markdown("#### Links")
    annotated_text("Github Repository ",("[link to the project](https://github.com/TulipAggarwal/Find-My-Project)","  " ,"#fea"), " and ", ("[link to the Dataset](https://docs.google.com/spreadsheets/d/e/2PACX-1vTmIIOHVpRrtU77eVrK-2cU-8MLwMZbuNYVYbBVF6WbS7xnJYvzyZKf99DCJ8hK51wUsm8PI0tBOvND/pubhtml)","  " ,"#fea"), " used in this project.", (""))
    
    st.markdown("#### Connect with me")
    linkedin_button = '<a href="https://www.linkedin.com/in/tulipaggarwal/" target="_blank" style="text-align: center; margin: 0px 10px; padding: 5px 10px; border-radius: 5px; color: white; background-color: #0077B5; text-decoration: none">LinkedIn</a>'
    github_button = '<a href="https://github.com/TulipAggarwal" target="_blank" style="text-align: center; margin: 0px 10px; padding: 5px 10px; border-radius: 5px; color: white; background-color: #24292E; text-decoration: none">GitHub</a>' 
    st.markdown("Connect with me on my socials - " f'{linkedin_button}{github_button} ', unsafe_allow_html=True)
