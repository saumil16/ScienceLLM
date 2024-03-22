from fastapi import FastAPI
import gradio as gr

from extract_info import demo

app = FastAPI()

@app.get('/')
async def root():
    app = gr.mount_gradio_app(app,demo,path='/home')
    return app

app = gr.mount_gradio_app(app,demo,path='/home')
