import streamlit as st
import ifcopenshell
from datetime import date
import ifcopenshell.util.element
import afry_bimlib_streamlit
# import ifchelper
from io import BytesIO
import os

st.markdown("# Ifc Project, Site, Building, Storey Editor ❄️")
st.sidebar.markdown("# Page 2 ❄️")

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

    # # IfcStorey
    # st.write(afry_bimlib_streamlit.get_building_storeys(st.session_state["ifc_file"]))
    # st.write('IfcBuildingStorey: '+ str(afry_bimlib_streamlit.get_building_storeys(st.session_state["ifc_file"]['Storey']).Name))

    # new_storey_name = st.text_input(label='New BuildingStorey name: ', value=None, key='building_storey', help='I.e.: 15040')
    # new_building_description= None
    # st.session_state["ifc_file"] = afry_bimlib_streamlit.update_ifc_building(st.session_state["ifc_file"], new_storey_name, new_building_description)
    


