from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.document_loaders import DirectoryLoader
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import gradio as gr
from gradio.themes.base import Base
import key_param 
import os
from dotenv import load_dotenv
import key_param

load_dotenv()

client = MongoClient(key_param.MONGO_URL)
dbName = "pro"
collectionName = "llmproject"
collection = client[dbName][collectionName]

embeddings = OpenAIEmbeddings(openai_api_key=key_param.openai_api_key)

vectorStore = MongoDBAtlasVectorSearch(collection, embeddings)

def query_data(query):
    llm = OpenAI(openai_api_key=key_param.openai_api_key,temperature=0)
    retriever = vectorStore.as_retriever()
    qa = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=retriever)
    retriever_output = qa.run(query)
    return retriever_output  

with gr.Blocks (theme=Base(), title="LLM") as demo:
    gr.Markdown(
        """
        Science LLM
        """)
    textbox = gr.Textbox(label="Question:")
    with gr.Row():
        button = gr.Button("Submit", variant="primary")
    with gr.Column():
        output2 = gr.Textbox(lines=1, max_lines=10, label="Output")    
    button.click(query_data, textbox, outputs=[output2])        
    
demo.launch()