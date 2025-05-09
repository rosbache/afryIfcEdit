import streamlit as st
import ifcopenshell
from datetime import date
import ifcopenshell.util.element
import afry_bimlib_streamlit
from io import BytesIO
import os

def update_file_bytes():
    '''Update filebytes to temp before writing to file'''

    # Write the modified IFC file to a temporary file on disk
    temp_file_path = "temp_updated_file.ifc"
  
    st.session_state['ifc_file'].write(temp_file_path)
    
    # Read the file into a BytesIO object
    updated_file_bytes = BytesIO()
    with open(temp_file_path, 'rb') as f:
        updated_file_bytes.write(f.read())
    updated_file_bytes.seek(0)

    # Optional: Delete the temporary file if it's no longer needed
    os.remove(temp_file_path)

    return updated_file_bytes


st.markdown("# Ifc Project, Site, Building, Storey Editor ❄️")

col1, col2 = st.columns(2) # Two colums created

with col2:
    st.markdown("##### Description")
    st.write('Project name could be: E18VK')

with col1: 
    st.markdown("##### File hierachy resume")

    # # IfcProject
    # st.write("IfcProject: " + str(afry_bimlib_streamlit.get_ifc_project(st.session_state["ifc_file"]).Name))
    # new_project_name= st.text_input(label="New IfcProject name:", value=None, key="project_name", help='I.e.: E18VK')
    # new_project_description = None #st.text_input(label="New project description", value=None, key="project_description" )
    # st.session_state["ifc_file"] = afry_bimlib_streamlit.update_ifc_project(st.session_state["ifc_file"], new_project_name, new_project_description)

    # # IfcSite
    # st.write('IfcSite: '+ str(afry_bimlib_streamlit.get_ifc_site(st.session_state["ifc_file"]).Name))
    # new_site_name= st.text_input(label='New IfcSite name:', value=None, key='site_name', help='I.e.: E105')
    # new_site_description=None
    # st.session_state["ifc_file"] = afry_bimlib_streamlit.update_ifc_site(st.session_state["ifc_file"], new_site_name, new_site_description)

    # # IfcBuilding
    # st.write('IfcBuilding: '+ str(afry_bimlib_streamlit.get_ifc_building(st.session_state["ifc_file"]).Name))
    # new_building_name = st.text_input(label='New IfcBuilding name: ', value=None, key='building_name', help='I.e.: DSG')
    # new_building_description= None
    # st.session_state["ifc_file"] = afry_bimlib_streamlit.update_ifc_building(st.session_state["ifc_file"], new_building_name, new_building_description)

    # # IfcStorey TODO what if several storeys?
    # st.write(afry_bimlib_streamlit.get_building_storeys(st.session_state["ifc_file"]))
    # st.write('IfcBuildingStorey: '+ str(afry_bimlib_streamlit.get_building_storeys(st.session_state["ifc_file"]['Storey']).Name))

    # new_storey_name = st.text_input(label='New BuildingStorey name: ', value=None, key='building_storey', help='I.e.: 15040')
    # new_building_description= None
    # st.session_state["ifc_file"] = afry_bimlib_streamlit.update_ifc_building(st.session_state["ifc_file"], new_storey_name, new_building_description)
    


