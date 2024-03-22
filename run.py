from fastapi import FastAPI
import gradio as gr

from extract_info import demo

app = FastAPI()

@app.get('/')
async def root():
    return "This is the root path!"

# Mount Gradio app on the root path
app = gr.mount_gradio_app(app, demo, path='/')

