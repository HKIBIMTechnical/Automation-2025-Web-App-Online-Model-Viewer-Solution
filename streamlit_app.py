import streamlit as st
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport
from specklepy.api.credentials import get_account_from_token
from specklepy.objects import Base
from specklepy.api.wrapper import StreamWrapper
from specklepy.api import operations
from specklepy.transports.memory import MemoryTransport


from speckleFun import speckleFun,jsonFun
from streamlit.components.v1 import iframe

from specklepy.objects import Base
from specklepy.serialization.base_object_serializer import BaseObjectSerializer

import json  

import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide",page_icon="GT.png",page_title="GT_Online_Models")

st.markdown("""
    <style>
        .stMultiSelect [data-baseweb=select] span,
        .stForm .stMultiSelect [data-baseweb=select] span {
            max-width: 500px;
            font-size: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

HOST=st.secrets["speckle_host_xyz"]
HOST2=st.secrets["speckle_host"]
token=st.secrets["speckle_test_001_token"]


client=speckleFun.get_authenticated_client()
streamlist= speckleFun.get_stream_list(client)
stream=speckleFun.get_stream_by_name(client,"Models")
branchlist=[branch for branch in speckleFun.get_stream_branches_item_list(client,stream) if "your model name" in branch.name and "nwc/" in branch.name]
branch_name_id_dict={branch.name:branch.id for branch in branchlist}
branch_id_list=[branch.id for branch in branchlist]
form=st.form("Models",clear_on_submit=True,border=True)

#------------------------------------------------------------------------------------------------

st.sidebar.image("logo.png",width=200)

st.sidebar.title("Models")
selected_option = st.sidebar.selectbox("Model Select Options", branch_name_id_dict.keys())
branch=speckleFun.get_branch_by_name(client,stream,selected_option)

model_url = speckleFun.get_model_url(stream.id,branch.id)


wrapper=StreamWrapper(model_url)
wrapper_client=wrapper.get_client()
commit=client.commit.get(wrapper.stream_id,wrapper.commit_id)
transport=wrapper.get_transport()
data=speckleFun.receive_data(client,stream.id,branch)


data_json=speckleFun.get_json_by_Base_data(data)
rvt_elements=jsonFun.nwc_rvt_json_find_elements_with_keys_return_first_match_obj(data_json,["Element","Revit Type"])
c3d_elements=jsonFun.nwc_c3d_json_find_elements_with_keys_return_first_match_obj(data_json,["Category Code"])    
#------------------------------------------------------------------------------------------------

st.header("Viewer")
selected_branch_id=branch_name_id_dict[selected_option]
speckleFun.add_iframe_view_by_stream_id_and_branch_id(stream.id,selected_branch_id,None,400)

#------------------------------------------------------------------------------------------------

parameters=[]
selected_parameters=[]
form=st.sidebar.form("Parameters",border=True)
with form:
    if "/rvt/" in branch.name:
        revit_element_parameters=[]
        for element in rvt_elements:
            try:
                for key in element["properties"]["Element"].keys():
                    if "Element|"+key not in revit_element_parameters:
                        revit_element_parameters.append("Element|"+key)
            except:
                pass
        with form:
            selected_parameters=st.multiselect("Element Parameters",revit_element_parameters)
    elif "/c3d/" in branch.name:
        c3d_element_parameters=[]
        for element in c3d_elements:
            try:
                for key in element["properties"]["Category Code"].keys():
                    if "Category Code|"+key not in c3d_element_parameters:
                        c3d_element_parameters.append("Category Code|"+key)
            except:
                pass
            try:
                for key in element["properties"]["Item_"].keys():
                    if "Item_|"+key not in c3d_element_parameters:
                        c3d_element_parameters.append("Item_|"+key)
            except:
                pass
            try:
                for key in element["properties"]["TS Asset Registration Code"].keys():
                    if "TS Asset Registration Code|"+key not in c3d_element_parameters:
                        c3d_element_parameters.append("TS Asset Registration Code|"+key)
            except:
                pass
            try:
                for key in element["properties"]["Drawing Information"].keys():
                    if "Drawing Information|"+key not in c3d_element_parameters:
                        c3d_element_parameters.append("Drawing Information|"+key)   
            except:
                pass
            try:
                for key in element["properties"]["Civil3D"].keys():
                    if "Civil3D|"+key not in c3d_element_parameters:
                        c3d_element_parameters.append("Civil3D|"+key)      
            except:
                pass   
        with form:
            selected_parameters=st.multiselect("Element Parameters",c3d_element_parameters)

    submit=form.form_submit_button("Submit")         
        
#------------------------------------------------------------------------------------------------
      
#plotly pie charts      
if "/rvt/" in branch.name:
    display_data_dict={"CAT Code":[],"Family":[],"Drawing Info":[]}
    for element in rvt_elements:
        try:
            display_data_dict["CAT Code"].append(element["properties"]["Element"]["CAT Code"])
        except:
            display_data_dict["CAT Code"].append(None)
        try:
            display_data_dict["Family"].append(element["properties"]["Element"]["Family"])
        except:
            display_data_dict["Family"].append(None)
        try:
            display_data_dict["Drawing Info"].append(element["properties"]["Element"]["Drawing Info"])
        except:
            display_data_dict["Drawing Info"].append(None) 
            
    display_df=pd.DataFrame(display_data_dict)
    col1,col2,col3=st.columns(3,gap="medium")
    with col1:
        fig = px.pie(display_df, names='CAT Code',labels="CAT Code", title='Distribution of CAT Codes',hole=0.6)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
    with col2:
        fig = px.pie(display_df, names='Family',labels="Family", title='Distribution of Families',hole=0.6)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
    with col3:
        fig = px.pie(display_df, names='Drawing Info',labels="Drawing Info", title='Distribution of Drawing Info',hole=0.6)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
elif "/c3d/" in branch.name:
    display_data_dict={"CAT Code":[],"Area":[],"Drawing Info":[],"Type":[]}
    
    for element in c3d_elements:
        try:
            display_data_dict["CAT Code"].append(element["properties"]["Category Code"]["CAT Code"])
        except:
            display_data_dict["CAT Code"].append(None)
        try:
            display_data_dict["Area"].append(element["properties"]["GT_Properties"]["Area"])
        except:
            display_data_dict["Area"].append(None)
        try:
            display_data_dict["Drawing Info"].append(element["properties"]["Drawing Information"]["Drawing Info"])
        except:
            display_data_dict["Drawing Info"].append(None)
        try:
            display_data_dict["Type"].append(element["properties"]["Item_"]["Type"])
        except:
            display_data_dict["Type"].append(None)  
    
    display_df=pd.DataFrame(display_data_dict)
    col1,col2,col3,col4=st.columns(4,gap="medium")
    with col1:
        fig = px.pie(display_df, names='CAT Code',labels="CAT Code", title='Distribution of CAT Codes',hole=0.6)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
    with col2:
        fig = px.pie(display_df, names='Area',labels="Area", title='Distribution of Areas',hole=0.6)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
    with col3:
        fig = px.pie(display_df, names='Drawing Info',labels="Drawing Info", title='Distribution of Drawing Info',hole=0.6)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
    with col4:
        fig = px.pie(display_df, names='Type',labels="Type", title='Distribution of Types',hole=0.6)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
        
        
        
        
        
# ------------------------------------------------------------------------------------------------
        
        
if submit:
    data_dict={}
    if "/rvt/" in branch.name:
        for parameter in selected_parameters:
            data_dict[parameter]=[]
            for element in rvt_elements:
                try:    
                    data_dict[parameter].append(element["properties"]["Element"][parameter.split("|")[1]])
                except:
                    data_dict[parameter].append(None)
        
    elif "/c3d/" in branch.name:
        for parameter in selected_parameters:
            data_dict[parameter]=[]
            for element in c3d_elements:
                try:    
                    data_dict[parameter].append(element["properties"][parameter.split("|")[0]][parameter.split("|")[1]])
                except:
                    data_dict[parameter].append(None)
    
    df=pd.DataFrame(data_dict)  
    st.dataframe(df,use_container_width=True)


if submit:
    st.download_button("Download",df.to_csv(),file_name=branch.name.split("/")[-1]+"_data.csv",on_click=lambda: None)



    

print("faf")





    