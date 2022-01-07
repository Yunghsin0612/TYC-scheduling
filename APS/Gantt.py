# -*- coding: utf-8 -*-
"""
Title: Job Shop Scheduling Module
Version: 0.1
Author: Kuan-Chen Tseng k.c.tseng@ie.nthu.edu.tw
Copyright: Belongs to DAlab Solutions x Associates Co.,Ltd.
"""
import pandas as pd
import plotly.express as px
import plotly.io as pio
import datetime
pio.renderers.default = "browser"

def print_gantt(schedule, CURRENTTIME):
    CURRENTTIME = CURRENTTIME.timestamp()
    output_list = []
    for mc_id, mc in schedule.items():
        
        for bucket in mc.bucket_list:
            for block in bucket.block_list:
                # if 'A21' in block.op_id:
                output_list.append(
                    dict(Task=mc.id,
                     Start=datetime.datetime.fromtimestamp(block.start+CURRENTTIME),
                     Finish=datetime.datetime.fromtimestamp(block.end+CURRENTTIME),
                     Resource=str(block.name)
                     )
                    )
    # print(output_list)
    df = pd.DataFrame(
        output_list
    )
    
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Resource")
    # otherwise tasks are listed from the bottom up
    fig.update_yaxes(autorange="reversed")

    # 用以調整bar寬度
    fig.update_traces(width=0.5)

    fig.layout.xaxis.tickangle = -45
    # print(fig['data'])
    fig.show()
    