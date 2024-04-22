#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Author  : youshu.Ji
import uuid
from datetime import datetime

import gradio as gr
from sqlalchemy import create_engine
import pandas as pd

DB_NAME = "instruct"
TABLE_NAME = "instruct"
title = "Prompt-DIY"

candidate_prompts = [
    "按照下面样例格式生成NER结果",
    "润色下面这段文本",
    "对指定内容进行多个版本的改写，以避免文本重复。",
    "改写这篇文章",
    "根据以下介绍，写一个小说开头",
    "根据以下介绍，写一个小说大纲",
    "根据以下大纲，扩写该章节",
    "给这个故事添加一个反转的剧情",
    "给这个故事改成一个有反转的剧情",
    "写一个小说开头",
    "按照下面的需求写代码",
    "其他",
    ""
]
# 连接SQLite数据库
engine = create_engine(f'sqlite:///{DB_NAME}.db?check_same_thread=False', echo=True)


# 定义函数，将文本框中的内容写入数据库
def write_to_db(prompt: str, input: str, output: str, reference: str):
    if output == reference:
        reference = ""

    df = pd.DataFrame(
        {
            "insert_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prompt": prompt,
            "input": input,
            "output": output,
            "rejected": reference
        },
        index=[str(uuid.uuid4())]
    )
    df.to_sql(TABLE_NAME, engine, if_exists="append")
    return "数据已成功写入数据库！"


# 依据prompt和input的输入，调用接口生成output
def write_to_output(prompt: str, input: str, method):
    print(prompt, input, method)
    try:
        if method == "chatgpt":
            # 接口需要自己设定
            from generate_api import chatgpt
            return chatgpt(prompt + "\n" + input)
        elif method == "chatglm":
            from generate_api import chatglm
            return chatglm(prompt + "\n" + input)
        elif method == "moss":
            from generate_api import chatmoss
            return chatmoss(prompt + "\n" + input)

        else:
            return ""
    except:
        return ""


def func_clear(prompt, input, reference, output, flag):
    return "", "", "", "", ""


# examples = [[i, "", ""] for i in candidate_prompts],

# 定义Gradio界面
with gr.Blocks() as iface:
    gr.Markdown("Build yourself prompt")
    with gr.Tab("Build"):
        text_prompt = gr.inputs.Textbox(label="prompt")
        examples = gr.Examples(examples=candidate_prompts,
                               inputs=[text_prompt])

        text_input = gr.inputs.Textbox(label="input")
        x = gr.Radio(["chatglm", "chatgpt", "moss", "none"])
        btn_generate = gr.Button("生成")
        text_reference = gr.inputs.Textbox(label="reference")
        btn_generate.click(write_to_output, inputs=[text_prompt, text_input, x], outputs=text_reference)
        btn_transfer = gr.Button("⬇")
        text_output = gr.inputs.Textbox(label="output")
        btn_submit = gr.Button("提交")
        text_flag = gr.outputs.Textbox(label="写入情况")
        btn_clear = gr.Button("清空")
        btn_transfer.click(lambda x: x, inputs=[text_reference], outputs=[text_output])
        btn_submit.click(write_to_db, inputs=[text_prompt, text_input, text_output, text_reference], outputs=text_flag)
        btn_clear.click(func_clear, inputs=[text_prompt, text_input, text_reference, text_output, text_flag],
                        outputs=[text_prompt, text_input, text_output, text_flag])
        text_clipboard = gr.Textbox(label="clipboard")

# 启动Gradio界面
iface.launch()
