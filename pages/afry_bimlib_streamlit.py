#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
AFRY BIMlib to be used with streamlit.io app

'''

import os
import json
# import tomllib

# import panda as pd # not needed in
import ifcopenshell
import ifcopenshell.util.element
import ifcopenshell.util.pset
import ifcopenshell.api.pset
import ifcopenshell.api.owner


__author__ = 'Eirik Rosbach'
__copyright__ = 'Copyright 2024, Eirik Rosbach'
__license__ = ""
__version__ = '0.1'
__email__ = 'eirik.rosbach@afry.com'
__status__ = ' Prototype'

def get_ifc_project(ifc_file):
    ''' '''

    return ifc_file.by_type("IfcProject")[0]

def get_ifc_site(ifc_file):
    ''''''

    # Assumes only one IfcSIte
    return ifc_file.by_type('IfcSite')[0]


def get_ifc_building(ifc_file):
    ''''''
    # Get IfcSite
    # Assumes only one IfcSIte
    return ifc_file.by_type('IfcBuilding')[0] 

def get_building_storeys(ifc_file):
    '''fd'''
    
    return ifc_file.by_type('IfcBuildingStorey')[0] 

def update_ifc_site(ifc_file, new_site_name, new_site_description=None):
    '''Update IfcSite with new name and description'''

    # Get IfcSite
    # Assumes only one IfcSIte
    ifc_site = ifc_file.by_type('IfcSite')[0] 
    
    # Update values
    ifc_site.Name = new_site_name
    if new_site_description is not None:
        ifc_site.Description = new_site_description

    return ifc_file

def update_ifc_project(ifc_file, new_project_name, new_project_descritpion=None):
    '''Update IfcProject with new name and description.'''

    # Get IfcProject
    ifc_project = ifc_file.by_type('IfcProject')[0]
    
    # Update values
    ifc_project.Name = new_project_name
    
    # Update only if new description is given
    if new_project_descritpion is not None: 
        ifc_project.Description = new_project_descritpion

    return ifc_file 


def update_ifc_building(ifc_file, new_building_name, new_building_description=None):
    '''Update ifcBuilding with new name and description'''

    # Get IfcBuilding
    # Assumes only one IfcBuilding
    ifc_building = ifc_file.by_type('IfcBuilding')[0] 
    
    # Update values
    ifc_building.Name = new_building_name
    if new_building_description is not None:
        ifc_building.Description = new_building_description

    return ifc_file

def update_building_storey(ifc_file, new_building_storey_name, new_building_storey_description):
    '''Update IfcBuildingStorey with new name and description'''
    
    # Get IfcBuildingStorey
    # Assumes only one IfcBuildingStorey
    ifc_building_storey = ifc_file.by_type('IfcBuildingStorey')[0] 
    
    # Update values
    ifc_building_storey.Name = new_building_storey_name
    ifc_building_storey.Description = new_building_storey_description

    return ifc_file

def get_objects_data_by_class(file, class_type):
    '''Description '''

    def add_pset_attributes(psets):
        ''''''
        for pset_name, pset_data in psets.items():
            for property_name in pset_data.keys():
                pset_attributes.add(
                    f"{pset_name}.{property_name}"
                ) if property_name != "id" else None

    objects = file.by_type(class_type)
    objects_data = []
    pset_attributes = set()

    for object in objects:
        qtos = ifcopenshell.util.element.get_psets(object, qtos_only=True)
        add_pset_attributes(qtos)
        psets = ifcopenshell.util.element.get_psets(object, psets_only=True)
        add_pset_attributes(psets)
        objects_data.append(
            {
                "ExpressId": object.id(),
                "GlobalId": object.GlobalId,
                "Class": object.is_a(),
                "PredefinedType": ifcopenshell.util.element.get_predefined_type(object),
                "Name": object.Name,
                "Level": ifcopenshell.util.element.get_container(object).Name
                if ifcopenshell.util.element.get_container(object)
                else "",
                "Type": ifcopenshell.util.element.get_type(object).Name
                if ifcopenshell.util.element.get_type(object)
                else "",
                "QuantitySets": qtos,
                "PropertySets": psets,
            }
        )
    return objects_data, list(pset_attributes)

def get_attribute_value(object_data, attribute):
    '''Description'''

    if "." not in attribute:
        return object_data[attribute]
    elif "." in attribute:
        pset_name = attribute.split(".", 1)[0]
        prop_name = attribute.split(".", -1)[1]
        if pset_name in object_data["PropertySets"].keys():
            if prop_name in object_data["PropertySets"][pset_name].keys():
                return object_data["PropertySets"][pset_name][prop_name]
            else:
                return None
        elif pset_name in object_data["QuantitySets"].keys():
            if prop_name in object_data["QuantitySets"][pset_name].keys():
                return object_data["QuantitySets"][pset_name][prop_name]
            else:
                return None
        else:
            return None
        
def create_pandas_dataframe(data, pset_attributes):
    ''' '''
    import pandas as pd

    ## List of Attributes
    attributes = [
        "ExpressId",
        "GlobalId",
        "Class",
        "PredefinedType",
        "Name",
        "Level",
        "Type",
    ] + pset_attributes

    ## Export Data to Pandas
    pandas_data = []
    for object_data in data:
        row = []
        for attribute in attributes:
            value = get_attribute_value(object_data, attribute)
            row.append(value)
        pandas_data.append(tuple(row))
    return pd.DataFrame.from_records(pandas_data, columns=attributes)


def read_json_file(json_file):
    '''Read a given json file as is. No conversion of datatype.'''

    # Load the JSON file
    try:
        with open(json_file, 'r') as file:
            json_data = json.load(file)

    except FileNotFoundError:
        print(f"Error: The file {json_file} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {json_file} is not a valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return json_data