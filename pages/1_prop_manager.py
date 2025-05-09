import streamlit as st
import ifcopenshell
from datetime import date
import os
from pathlib import Path
from io import BytesIO

st.set_page_config(
    layout= "wide",
    page_title= "IFC Property Set Editor")#,
    # page_icon= icon,
# )

st.markdown("# Ifc Property Set Editor ❄️")
# st.sidebar.markdown("# Page 3 ❄️")

def find_pset(entity, pset_name):
    '''Find a pset'''

    for definition in entity.IsDefinedBy:
        if definition.is_a('IfcRelDefinesByProperties'):
            pset = definition.RelatingPropertyDefinition
            if pset.is_a('IfcPropertySet') and pset.Name == pset_name:
                
                return pset
    return None

def update_psets(ifc_element, psets):
    '''Update an proeprty value in a given pset'''

    for pset_name, variables in psets.items():
        pset = find_pset(entity=ifc_element, pset_name=pset_name)
        if pset.Name == pset_name:# is not None:
            # Update the variables in the pset
            for var_name, var_value in variables.items():
                for prop in pset.HasProperties:
                    if prop.Name == var_name: # Property found
                        prop.NominalValue.wrappedValue = var_value

def group_properties(row):
    '''Group properties in dataframe and filter'''

    grouped = {'psets': {}}
    for col in row.index:
        if '.' in col:
            pset, prop = col.split('.')
            if pset not in grouped['psets']:
                grouped['psets'][pset] = {}
            grouped['psets'][pset][prop] = row[col]
            # Only take with Pset and 01/02/03/04 TODO make general or input from user
        elif col.startswith(('Pset_', '01', '02', '03', '04')):
            if 'psets' not in grouped:
                grouped['psets'] = {}
            grouped['psets'][col] = row[col]
        else:
            grouped[col] = row[col]

    return grouped

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

def execute():
    if st.session_state.get("ifc_file") is None:
        st.warning("No file provided. Please upload a file.")

     # Get the original file 
    original_file_name = st.session_state["file_name"]

    # Create the updated file name with the current date
    updated_file_name = original_file_name.split(".")[0] + "_updated_" + str(date.today()) + ".ifc"

    st.markdown(
        """ 
        #####  Investigate and update ifc file before export an updated .ifc files
        """
    )
    st.markdown("""---""")
    st.markdown("##### Instructions:")
    st.write('1. Edit in dataframe as in you do in excel. Drag a cell to copy value to the next cell. No formulas is allowed. !')
    st.write('2. Click on the button "Execute updtates" above the dataframe editorto update values in the ifc-file')
    st.write('Only values in pset can be changed at this time')
    st.write('3. Click on the button below the dataframe editor" Download File')
    
    st.markdown("""---""")
    st.write('File currently editing: ' + original_file_name)
    st.write('File to be written: ' + updated_file_name)
    st.markdown("""---""")

    # Group properties per pset before update
    execute_button = st.button(label='Execute updates')

    # Set up dataframe and dataeditor    
    edited_df = st.data_editor(st.session_state['DataFrame'])
    st.toast(body='Dataframe editor setup complete')
  
    # initiate value to not get a ubound error
    updated_file = ''

    # Update in pset and file. TODO have as own function
    if execute_button:
        # Group data in dataframe editor (pset1.pset1value1, pset2.pset2value1)
        grouped_data = edited_df.apply(group_properties, axis=1).tolist()
       
        # Keys aka pset to keep from all psets
        # TODO make general or input from user
        keys_to_keep = ['04 Fagspesfikk', '03 Objektinformasjon', '01 Prosjektinformasjon', '02 Modellinformasjon']

        for element in st.session_state['ifc_file'].by_type('IfcElement'):
            for item in grouped_data:
                # Psets in element
                original_psets = item['psets']
                # Filtered psets. Ignor empty pset {} if not found
                psets = {key: original_psets.get(key, {}) for key in keys_to_keep if original_psets.get(key, {})}
                # Match on GlobalId
                if element.GlobalId == item['GlobalId']:
                    # Update psets
                    update_psets(element, psets)
        st.toast(body='Psets updated with new values')

        # Update in file
        st.toast(body='Started to write updated file to temp location')
        updated_file = update_file_bytes()
        st.toast(body='Updated file written to temp location')

    # Prepare a download button
    download_button = st.download_button("Download updated file",
                        data = updated_file,
                        file_name=updated_file_name,
                            mime="application/octet-stream" # Provide the appropriate name
                        )

execute()