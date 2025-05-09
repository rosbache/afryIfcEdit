'''
Description
'''

import os
import streamlit as st
import pandas as pd
import ifcopenshell
import datetime
import afry_bimlib_streamlit
from datetime import date
from datetime import datetime
from pathlib import Path
from io import BytesIO
import subprocess
import sys

def get_filename():
    '''Get filename of upladed file in session'''

    return st.session_state.get("file_name", "")

def get_file_creation_date(ifc_file_path):
    '''Description'''

    ifc_file = ifc_file_path
    owner_history = ifc_file.by_type("IfcOwnerHistory")[0]
    creation_date = owner_history.CreationDate
    date_time = datetime.fromtimestamp(creation_date)
    formatted_date = date_time.strftime("%Y-%m-%d ")
    
    return formatted_date

def callback_upload():
    '''Callback function for upload ifc file widget'''

    st.session_state["file_name"] = st.session_state["uploaded_file"].name
    # st.session_state["array_buffer"] = st.session_state["uploaded_file"].getvalue()
    st.session_state["ifc_file"] = ifcopenshell.file.from_string(st.session_state["uploaded_file"].getvalue().decode("utf-8"))
    st.session_state["is_file_uploaded"] = True
    
    st.toast(body='Uploading ifc file') # Give info to user
    
def extract_create_df():
    '''Create a dataframe of the pset of the elements in the ifc file'''

    # Create the DataFrame and store it in the session state
    
    st.toast(body='Extracting data')
    # Extract data
    data, pset_attributes = afry_bimlib_streamlit.get_objects_data_by_class(st.session_state["ifc_file"], "IfcProduct")

    # Create a panda dataframe 
    st.session_state["DataFrame"] = afry_bimlib_streamlit.create_pandas_dataframe(data, pset_attributes)

    st.toast('Data extracted')

def remove_uploaded_file():
    '''Remove file from session'''

    st.session_state["file_name"] = ""
    st.session_state["array_buffer"] = None
    st.session_state["ifc_file"] = None
    st.session_state["is_file_uploaded"] = False

def main():
    '''Description'''


    # Set page configuration
    st.set_page_config(
        layout="wide",
        page_title="AFRY IFC Editor",
        initial_sidebar_state="expanded",)
#         # page_icon=icon, # TODO create icon
#     )

    # st.title("Streamlit, Deployed on Koyeb")
    # st.subheader("Let's celebrate!")

    # Add some styling and text to page
    st.markdown("<h1 style='color: #C0C0C0;'>AFRY IFC Data Editor</h1>", unsafe_allow_html=True)
    st.markdown(
        """ 
        #####  Investigate and update ifc file before export an updated .ifc files
        """
    )
    st.markdown("""---""")
    st.logo(image='AFRY logo.png', size='large')
    # st.sidebar.markdown("Main page 🎈")

    # Initialize session state variables
    if "file_name" not in st.session_state:
        st.session_state["file_name"] = ""
    if "array_buffer" not in st.session_state:
        st.session_state["array_buffer"] = None
    if "ifc_file" not in st.session_state:
        st.session_state["ifc_file"] = None
    if "is_file_uploaded" not in st.session_state:
        st.session_state["is_file_uploaded"] = False
    
    col1, col2 = st.columns(2) # Two colums created

    with col1: # Output to column one on the left
        st.markdown("##### Instructions:")
        st.write('1. Upload ifc file using upload tool in sidebar (expand sidebar if necessary)')
        st.write('2. An error is displayed until a IFC file us uploaded (for now)')
        st.write('3. If a IFC file is uploaded, a resume of the file is given to the right.')
        st.write('4. Use the side Project manager to update IfcProject, Site, Building and Storeys')
        st.write('5. Use the side Prop manager to edit psets for all elements in the IFC file. An updated file can be downloaded.')
        st.write('6. USe the side IDS checker to check a uploaded file against a IDS file (TODO)')
        st.write('More text to come!')
        st.markdown("""---""")

    # Set up sidebar with file uploader
    # This is the uploaded file
    st.sidebar.write('Upload a IFC model:')
    uploaded_file = st.sidebar.file_uploader("Choose a file", key="uploaded_file", on_change=callback_upload)
    st.toast(body='File uploaded')

    # Extract pset and attributes and add to session.state as panda dataframe
    extract_create_df()

    if st.sidebar.button("Remove File"):
        remove_uploaded_file()

    if st.session_state["is_file_uploaded"]:
        st.sidebar.success("Project successfully loaded")
        
    if st.session_state["file_name"] != "":
        # col1, col2 = st.columns(2) # Two colums created

        if st.session_state["ifc_file"] is None:
            st.warning("No file provided. Please upload a file.")

        else:
            # Extract some data from the IFC file and show it to the user
            original_file_name = st.session_state["file_name"]

            # with col1: # Output to column one on the left
            #     st.markdown("##### Instructions:")
            #     st.write('1. Upload ifc file using upload tool in sidebar (expand if necessary)')
            #     st.write('More text to come!')
            #     st.markdown("""---""")
            with col2: # Output to column two on the right
                st.markdown("##### File resume:")
                st.write("A resume of the main parts of the file is given below:")
                st.write(f"File name: {get_filename()}")
                st.write("IFC schema in file: " + "".join(str(item) for item in st.session_state["ifc_file"].schema))
                creation_date = get_file_creation_date(st.session_state["ifc_file"])
                st.write("Creation date: " + str(creation_date))

                project = afry_bimlib_streamlit.get_ifc_project(st.session_state['ifc_file'])
                site = afry_bimlib_streamlit.get_ifc_site(st.session_state["ifc_file"])
                building = afry_bimlib_streamlit.get_ifc_building(st.session_state['ifc_file'])
                building_storeys = afry_bimlib_streamlit.get_building_storeys(st.session_state['ifc_file'])
                st.write('IfcProject:' + project.Name)
                st.write('IfcSite: ' + site.Name)
                st.write('IfcBuilding: ' + building.Name)
                st.write('IfcBuildingStorey: ' + str(building_storeys[0]))
                st.markdown("""---""")

if __name__ == "__main__":
    main()