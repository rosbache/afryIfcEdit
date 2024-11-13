import streamlit as st
import afry_bimlib_streamlit
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
st.sidebar.markdown("# Page 3 ❄️")

def find_pset(entity, pset_name):
    '''Find a pset'''

    for definition in entity.IsDefinedBy:
        if definition.is_a('IfcRelDefinesByProperties'):
            pset = definition.RelatingPropertyDefinition
            if pset.is_a('IfcPropertySet') and pset.Name == pset_name:
                
                return pset
    return None

# Function to update psets
def update_psets(ifc_element, psets):
    for pset_name, variables in psets.items():
        # print(f'*pset_name*: {pset_name}')
        # pset = ifc_element.get_pset(pset_name)
        pset = find_pset(entity=ifc_element, pset_name=pset_name)
        # print(f'pset: {pset} ' + str(type(pset)))
        if pset.Name == pset_name:# is not None:
            # print(f'match on pset: {pset}')
            # Update the variables in the pset
            for var_name, var_value in variables.items():
                for prop in pset.HasProperties:
                    if prop.Name == var_name: # Property found
                        prop.NominalValue.wrappedValue = var_value
                        # print(f'prop updated: {prop.NominalValue}')
                


def group_properties(row):
    grouped = {'psets': {}}
    for col in row.index:
        if '.' in col:
            pset, prop = col.split('.')
            if pset not in grouped['psets']:
                grouped['psets'][pset] = {}
            grouped['psets'][pset][prop] = row[col]
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
    st.write('More text to come!')

    st.write('File currently editing: ' + original_file_name)
    st.write('File to be written: ' + updated_file_name)
    st.markdown("""---""")

    # Grab current session
    # session = st.session_state
 
    # Set up dataframe and dataeditor    
    edited_df = st.data_editor(st.session_state['DataFrame'])
    st.toast(body='Dataframe editor setup complete')

    # Group properties per pset before update
    grouped_data = edited_df.apply(group_properties, axis=1).tolist()

    st.write(grouped_data)

    #  Iterate over all elements and update psets

    # Keys aka pset to keep from all psets
    keys_to_keep = ['04 Fagspesfikk', '03 Objektinformasjon', '01 Prosjektinformasjon', '02 Modellinformasjon']
    # Filtered dictionary
    # psets = {key: original_psets[key] for key in keys_to_keep}
    for element in st.session_state['ifc_file'].by_type('IfcElement'):
        for item in grouped_data:
            original_psets = item['psets']
            psets = {key: original_psets[key] for key in keys_to_keep}
            if element.GlobalId == item['GlobalId']:
                # update_psets(element, item['psets'])
                update_psets(element, psets)

    updated_file = update_file_bytes()                                
    st.download_button("Download updated file",
                       data = updated_file, # st.session_state['ifc_file']
                       file_name=updated_file_name,
                        mime="application/octet-stream" # Provide the appropriate name
                       )
    
   
execute()