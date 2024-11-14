'''
Description
'''

import os
import streamlit as st
import pandas as pd
import ifcopenshell
import datetime
# import ifchelper
import afry_bimlib_streamlit
from datetime import date
from datetime import datetime
from pathlib import Path
from io import BytesIO

def update_file_bytes():
    '''Update filebytes to temp before writing to file'''

    # Write the modified IFC file to a temporary file on disk
    temp_file_path = "temp_updated_file.ifc"
  
    st.session_state['ifc_file'].write(temp_file_path) #aka ifcopenshell.ifc_file.write()
    
    # Read the file into a BytesIO object
    updated_file_bytes = BytesIO()
    with open(temp_file_path, 'rb') as f:
        updated_file_bytes.write(f.read())
    updated_file_bytes.seek(0)

    # Optional: Delete the temporary file if it's no longer needed
    os.remove(temp_file_path)

    return updated_file_bytes

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
    '''Description'''

    
    st.session_state["file_name"] = st.session_state["uploaded_file"].name
    # st.session_state["array_buffer"] = st.session_state["uploaded_file"].getvalue()
    st.session_state["ifc_file"] = ifcopenshell.file.from_string(st.session_state["uploaded_file"].getvalue().decode("utf-8"))
    st.session_state["is_file_uploaded"] = True
    
    st.toast(body='Uploading file') # Give info to user
    
def extract_create_df():
    '''Descr'''

    # Create the DataFrame and store it in the session state
    # Extract data
    st.toast(body='Extracting data')
    data, pset_attributes = afry_bimlib_streamlit.get_objects_data_by_class(st.session_state["ifc_file"], "IfcProduct")

    # Create a panda dataframe # TODO create multiple to handle project, site separetawely?
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

    # Add some styling and text to page
    st.markdown("<h1 style='color: #C0C0C0;'>AFRY IFC Data Editor</h1>", unsafe_allow_html=True)
    st.markdown(
        """ 
        #####  Investigate and update ifc file before export an updated .ifc files
        """
    )
    st.markdown("""---""")
    # st.markdown("# Hovedside 🎈")
    st.logo(image='AFRY logo.png', size='large')
    st.sidebar.markdown("Main page 🎈")
    # st.write("Here's our first attempt at using data to create a app")
   

    # Initialize session state variables
    if "file_name" not in st.session_state:
        st.session_state["file_name"] = ""
    if "array_buffer" not in st.session_state:
        st.session_state["array_buffer"] = None
    if "ifc_file" not in st.session_state:
        st.session_state["ifc_file"] = None
    if "is_file_uploaded" not in st.session_state:
        st.session_state["is_file_uploaded"] = False

    # Set up sidebar with file uploader
    # This is the uploaded file
    uploaded_file = st.sidebar.file_uploader("Choose a file", key="uploaded_file", on_change=callback_upload)
    st.toast(body='File uploaded')
    # Extract pset and attributes and add to session.state as panda dataframe
    extract_create_df()

    if st.sidebar.button("Remove File"):
        remove_uploaded_file()

    if st.session_state["is_file_uploaded"]:
        st.sidebar.success("Project successfully loaded")
        
    if st.session_state["file_name"] != "":
        col1, col2 = st.columns(2) # Two colums created

        if st.session_state["ifc_file"] is None:
            st.warning("No file provided. Please upload a file.")

        else:
            original_file_name = st.session_state["file_name"]

            with col1: # Output to column one on the left
                st.markdown("##### Instructions:")
                st.write('1. Upload ifc file using upload tool in sidebar (expand if necessary)')
                st.write('More text to come!')
                st.markdown("""---""")
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
    
            # with col2: # Outpyut to column 2
            #     st.markdown("##### Download updated file:")
            #     st.write('After changes is done in the file, use the download button to download an updated file.')
                # updated_file = update_file_bytes()                                
                # st.download_button("Download updated file",
                #                    data = updated_file, # st.session_state['ifc_file']
                #                    file_name=updated_file_name,
                #                     mime="application/octet-stream" # Provide the appropriate name
                #                    )

if __name__ == "__main__":
    main()