#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Author  : youshu.Ji
import uuid

import gradio as gr
from sqlalchemy import create_engine
import pandas as pd

DB_NAME = "instruct"
TABLE_NAME = "instruct"
title = "Prompt-DIY"

candidate_prompts = [
    "润色下面这段文本",
    "其他",
    ""
]
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


# 依据prompt和input的输入，调用接口生成output
def write_to_output(prompt: str, input: str):
    # 接口需要自己设定
    from generate_api import chatgpt
    return chatgpt(prompt + input)


def func_clear(prompt, input, output, flag):
    return "", "", "", ""


# examples = [[i, "", ""] for i in candidate_prompts],

# 定义Gradio界面
with gr.Blocks() as iface:
    gr.Markdown("Build yourself prompt")
    with gr.Tab("Build"):
        text_prompt = gr.inputs.Textbox(label="prompt")
        text_input = gr.inputs.Textbox(label="input")
        text_output = gr.inputs.Textbox(label="output")
        text_flag = gr.outputs.Textbox(label="写入情况")
        btn_generate = gr.Button("生成")
        btn_submit = gr.Button("提交")
        btn_clear = gr.Button("清空")
        btn_generate.click(write_to_output, inputs=[text_prompt, text_input], outputs=text_output)
        btn_submit.click(write_to_db, inputs=[text_prompt, text_input, text_output], outputs=text_flag)
        btn_clear.click(func_clear, inputs=[text_prompt, text_input, text_output, text_flag],
                        outputs=[text_prompt, text_input, text_output, text_flag])

# 启动Gradio界面
iface.launch()
