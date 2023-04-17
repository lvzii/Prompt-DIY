#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Author  : youshu.Ji
import uuid

import gradio as gr
from sqlalchemy import create_engine
import pandas as pd

DB_NAME = "instruct"
TABLE_NAME = "instruct"

# 连接SQLite数据库
engine = create_engine(f'sqlite:///{DB_NAME}.db?check_same_thread=False', echo=True)


# 定义函数，将文本框中的内容写入数据库
def write_to_db(prompt: str, input: str, output: str):
    df = pd.DataFrame(
        {
            "prompt": prompt,
            "input": input,
            "output": output
        },
        index=[str(uuid.uuid4())]
    )
    df.to_sql(TABLE_NAME, engine, if_exists="append")
    return "数据已成功写入数据库！"


# 定义Gradio界面
iface = gr.Interface(
    fn=write_to_db,
    inputs=[
        gr.inputs.Textbox(label="prompt"),
        gr.inputs.Textbox(label="input"),
        gr.inputs.Textbox(label="output")
    ],
    outputs=gr.outputs.Textbox(label="写入情况")
)

# 启动Gradio界面
iface.launch()
