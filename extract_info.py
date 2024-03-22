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
        <h1 style="text-align: center; font-weight: bold; left-border: 50px"> Welcome to <b>SciQuest</b></h1>
        <h2 style="text-align: center; font-weight: bold; left-border: 50px"> Dive Deep in the world of science ...</h2>
        """)
    textbox = gr.Textbox(label="Question:")
    with gr.Row():
        button = gr.Button("Submit", variant="primary")
    with gr.Column():
        #output2 = gr.Textbox(lines=1, max_lines=20, label="Output")   
        spacer = gr.Markdown("<br><br>")  # Adding empty Markdown for spacing 
        output2 = gr.Textbox(lines=1, max_lines=10, label="Output")

    button.click(query_data, textbox, outputs=[output2])        
    
#demo.launch()
