import specklepy.api.models
import streamlit as st
from specklepy.api import operations
from specklepy.api.client import SpeckleClient
import specklepy.api.client
from specklepy.api.credentials import get_default_account,get_local_accounts
from specklepy.transports.server import ServerTransport
from specklepy.api.credentials import get_account_from_token
import specklepy.api
import specklepy.api.credentials
from streamlit.components.v1 import iframe
from specklepy.objects import Base
from specklepy.api import operations
from specklepy.api.wrapper import StreamWrapper
from typing import Any,List
import json
from specklepy.objects.geometry import Point

HOST=st.secrets["speckle_host_xyz"]
HOST2=st.secrets["speckle_host"]
token=st.secrets["speckle_test_001_token"]
server_url=st.secrets["speckle_server"]
demo_token=st.secrets["demo_token"]


class speckleFun(object):
    @staticmethod
    def get_authenticated_client() -> SpeckleClient:
        """
        speckle_host = "app.speckle.systems"
        """
        client = SpeckleClient(host=HOST2)
        account = get_account_from_token(token=token,server_url=server_url)
        
        client.authenticate_with_account(account)

        return client
    def get_authenticated_local_client() -> SpeckleClient:
        local_client = SpeckleClient(host="localhost:3000", use_ssl=False)
        local_account = next(
            a for a in get_local_accounts() if "localhost" in a.serverInfo.url
        )
        local_client.authenticate(token=local_account.token)

        return local_client

    @staticmethod
    def not_working_get_client_host_xyz() -> specklepy.api.client.SpeckleClient:
        '''
        this server is old and not working
        '''
        client=SpeckleClient(host="speckle.xyz")
        return client


    
    
    @staticmethod
    def get_user_info(account: specklepy.api.credentials.Account):
        return account.userInfo

    @staticmethod
    def get_stream_list(client: specklepy.api.client.SpeckleClient) -> list[specklepy.api.client.stream.Stream]:
        
        return client.stream.list()
    
    @staticmethod
    def get_stream_name_list(client: specklepy.api.client.SpeckleClient) -> list[str]:
        return [stream.name for stream in speckleFun.get_stream_list(client)]

    @staticmethod
    def get_stream_by_name(client: specklepy.api.client.SpeckleClient, stream_name:str) -> specklepy.api.client.stream.Stream:
        stream=[stream for stream in speckleFun.get_stream_list(client) if stream.name==stream_name]
        if stream:
            st=client.stream.get(stream[0].id)
            return st
        else:
            return None

    @staticmethod
    def get_stream_by_id(client:SpeckleClient, stream_id) -> specklepy.api.client.stream.Stream:
        stream = client.stream.get(stream_id)        
        return stream
    
    @staticmethod
    def get_stream_branches(stream: specklepy.api.client.stream.Stream):
        '''only get 10 branches'''
        return stream.branches.items
    
    @staticmethod
    def get_stream_branches_item_list(client: SpeckleClient, stream: specklepy.api.client.stream.Stream,branches_limit:int=100,commit_limit:int=10) -> list[specklepy.api.client.branch.Branch]:
        '''
        item is final branch 
        '''
        branches= client.branch.list(stream.id,branches_limit,commit_limit) 
        return branches
    
    @staticmethod 
    def get_branch_by_name(client: SpeckleClient, stream: specklepy.api.client.stream.Stream, branch_name: str="main") -> specklepy.api.client.branch.Branch:
        branch = [branch for branch in speckleFun.get_stream_branches_item_list(client, stream) if branch.name==branch_name][0]
        return branch
    
    @staticmethod
    def get_embed_url_by_stream_and_branch(stream: specklepy.api.client.stream.Stream, branch: specklepy.api.client.branch.Branch) -> str:
        embed_url= f"https://app.speckle.systems/projects/{stream.id}/models/{branch.id}#embed=%7B%22isEnabled%22%3Atrue%7D"
        return embed_url
    @staticmethod    
    def get_embed_url_by_stream_id_and_branch_id(stream_id: str, branch_id: str) -> str:
        embed_url= f"https://app.speckle.systems/projects/{stream_id}/models/{branch_id}#embed=%7B%22isEnabled%22%3Atrue%7D"
        return embed_url
    @staticmethod 
    def get_embed_url_by_stream_and_branch_Name(stream: specklepy.api.client.stream.Stream, branch_name:str="main") -> str:
        '''
        this function only work for top level branch folder
        '''
        
        embed_url= f"https://app.speckle.systems/projects/{stream.id}/models/${branch_name}#embed=%7B%22isEnabled%22%3Atrue%7D"
        return embed_url
    
    @staticmethod
    def add_iframe_view_by_stream_and_branch(stream : specklepy.api.client.stream.Stream,branch: specklepy.api.client.branch.Branch,width:int|None=600,height:int|None=400):
        embed_url=speckleFun.get_embed_url_by_stream_and_branch(stream,branch)
        iframe(src=embed_url, width=width, height=height)
        
    @staticmethod
    def add_iframe_view_by_stream_id_and_branch_id(stream_id: str,branch_id: str,width:int|None=600 ,height:int|None=400):
        embed_url=speckleFun.get_embed_url_by_stream_id_and_branch_id(stream_id,branch_id)
        iframe(src=embed_url, width=width, height=height)
        
    @staticmethod
    def get_commit_list_by_stream(client: SpeckleClient, stream: specklepy.api.client.stream.Stream,commit_limit:int=100) -> list[specklepy.api.client.commit.Commit]:
        commits=client.commit.list(stream.id,commit_limit)
        return commits
    @staticmethod
    def get_commit_list_by_branch(branch: specklepy.api.client.branch.Branch) -> list[specklepy.api.client.commit.Commit]:
        commits=branch.commits.items
        return commits
    
    @staticmethod
    def get_model_url(stream_id: str,branch_id: str) -> str:
        '''
        this is the url of the model
        '''
        commit_url = f"https://app.speckle.systems/projects/{stream_id}/models/{branch_id}"
        return commit_url
    @staticmethod
    def not_working_get_commit_url_please_use_get_model_url(stream_id: str,commit_id: str) -> str:
        '''
        this server is old and not working
        '''
        commit_url = f"app.speckle.systems/steams/{stream_id}/commits/{commit_id}"
        return commit_url
    @staticmethod
    def get_stream_id_by_stream_name(client: specklepy.api.client.SpeckleClient, stream_name: str) -> str:
        streamlist= speckleFun.get_stream_list(client)
        streamid_list=[x.id for x in streamlist if x.name==stream_name]
        if streamid_list:
            return streamid_list[0]
        else:
            return None
    @staticmethod
    def receive_data(client: SpeckleClient, stream_id: str, branch: specklepy.api.client.branch.Branch) -> Base:
        url=speckleFun.get_model_url(stream_id,branch.id)                
        wrapper=StreamWrapper(url)

        transport=wrapper.get_transport(token=token)
        commit = branch.commits.items[0]
        
        data = operations.receive(commit.referencedObject, transport)

        return data
    @staticmethod
    def get_Transport_by_stream_id_and_url(client:SpeckleClient, stream_id:str,url:str) -> ServerTransport:
        transport=ServerTransport(stream_id=stream_id,client=client,url=url)
        return transport
    @staticmethod
    def get_Transport_by_stream_id_and_branch(stream_id: str, branch: specklepy.api.client.branch.Branch) -> ServerTransport:
        url=speckleFun.get_model_url(stream_id,branch.id)                
        wrapper=StreamWrapper(url)

        transport=wrapper.get_transport(token=token)

        return transport
    @staticmethod
    def convert_Base_data_to_json(data:Base,json_save_path:str="data.json"):
        json_string=operations.serialize(data)
        jsondata = json.loads(json_string) 
        
        with open(json_save_path, "w") as json_file:
            json.dump(jsondata, json_file, indent=4) 

    @staticmethod
    def get_json_by_Base_data(data:Base):
        json_string=operations.serialize(data)
        jsondata = json.loads(json_string) 
        return jsondata
    @staticmethod
    def get_models(client:SpeckleClient,streamid:str, models_limit:int=100):
        models=client.model.get_models(streamid,models_limit=models_limit)
        return models
    @staticmethod
    def get_model_by_name(client:SpeckleClient,streamid:str,modelname:str="your model name",models_limit:int=100):
        models=client.model.get_models(streamid,models_limit=models_limit)
        search_model=[m for m in models.items if m.name==modelname]
        if search_model:
            return search_model[0]
        else:
            return None


    class GeometryFun(object):
        @staticmethod
        def send_point(transport:ServerTransport,x:float,y:float,z:float,text:str="temp point",number:int=0):
            newobj=Base()
            newobj["myTextProp"]= text
            newobj["myNumberProp"]= number
            newobj["mySpeckleProp"]= Point.from_coords(x,y,z)
            newHash=operations.send(base=newobj,transports=[transport])
            return newHash
    

class jsonFun(object):
    @staticmethod
    def nwc_rvt_json_find_elements_with_keys_return_first_match_obj( obj:json, target_keys:list[str]) -> list[dict]:
        results = []
        
        def recursive_search(current_obj):
            if isinstance(current_obj, dict):
                if "properties" in current_obj:
                    props = current_obj["properties"]
                    if isinstance(props, dict) and all(key in props for key in target_keys):
                        results.append(current_obj)  
                        return 
                
                for value in current_obj.values():
                    recursive_search(value)
                    
            elif isinstance(current_obj, list):
                for item in current_obj:
                    recursive_search(item)
        
        recursive_search(obj)
        return results
    
    @staticmethod
    def nwc_c3d_json_find_elements_with_keys_return_first_match_obj( obj:json, target_keys:list[str]) -> list[dict]:
        results = []
        
        def recursive_search(current_obj):
            if isinstance(current_obj, dict):
                if "properties" in current_obj:
                    props = current_obj["properties"]
                    if isinstance(props, dict) and all(key in props for key in target_keys):
                        results.append(current_obj) 
                        return  
                
                for value in current_obj.values():
                    recursive_search(value)
                    
            elif isinstance(current_obj, list):     
                for item in current_obj:
                    recursive_search(item)
        
        recursive_search(obj)
        return results
    
if  __name__=='__main__':

    print("bbb")
    
    