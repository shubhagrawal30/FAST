import json
from google.cloud import firestore
from google.oauth2 import service_account
import streamlit as st

@st.cache_resource
def get_database():
    firestore_key = json.loads(st.secrets["FIRESTORE_KEY"])
    creds = service_account.Credentials.from_service_account_info(firestore_key)
    return firestore.Client(credentials=creds)

def get_doc_ref( db, collection_name, document_name):
    return db.collection(collection_name).document(document_name)

def get_doc(db, collection_name, document_name):
    return get_doc_ref(db, collection_name, document_name).get()

def update_doc_val(db, collection_name, document_name, field_name, val):
    get_doc_ref(db, collection_name, document_name).update({field_name: val})

def update_doc_dict(db, collection_name, document_name, dict_vals):
    get_doc_ref(db, collection_name, document_name).update(dict_vals)
    
def set_doc_dict(db, collection_name, document_name, dict_vals):
    get_doc_ref(db, collection_name, document_name).set(dict_vals)
    
def set_doc_val(db, collection_name, document_name, field_name, val):
    get_doc_ref(db, collection_name, document_name).set({field_name: val})