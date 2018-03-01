# coding: utf-8
# 17-10-6, created by tuitu
import random

# agent 生成

def get():
    user_agent_list = []
    f = open('user_agent.txt','r')
    for date_line in f:
        user_agent_list.append(date_line.replace('\n',''))
    f.close()
    return random.choice(user_agent_list)