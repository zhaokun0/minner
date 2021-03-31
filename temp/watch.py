#coding=utf-8
'''
Description: 
Author: liutq
Date: 2021-02-18 21:14:15
LastEditTime: 2021-02-24 16:36:44
LastEditors: liutq
Reference: 
'''
from enum import Flag
import AliSendmail as Alis
import requests
import re
import time
import math
#对ASCII编码的进行解码
import chardet 
import commons as cm
receivers = ['17863118591@163.com']# 接收邮件，可设置为你的QQ邮箱或者其他邮箱
urls=cm.urls
stateEvaluation=cm.stateEvaluation
notice=[]
Flagtime=0
workersLast=0
workersFlag=0#用于判定workers是不是新增或者掉线，连续三次即确认
while True:
    sumrate=0
    workers=0
    power=0
    for url in urls:
        try:
            content=requests.get(url,timeout=1).content
            encode_type = chardet.detect(content)
            content = content.decode(encode_type['encoding'])
            if('Unable to round-trip http request to upstream' in content):
                continue
            a=content.split('{"accepted_shares":')
            for i in range(1,len(a)-1):
                info=a[i]
                info=info.replace('\"','').replace('}','').replace('{','')
                item=info.split(',')
                cardName=item[9].replace('info:','')
                hashrate=float(re.findall(r"\d+\.?\d*",item[4])[0])
                sumrate+=hashrate
                workers+=1
                tempreature=int(item[16].replace(']','').replace('temperature:',''))
                P=int(item[14].replace('power:',''))
                power+=P
              
                #温度预警
                if(tempreature>stateEvaluation[cardName][1]):
                    if(stateEvaluation[cardName][3]==0):
                        msg='机器{},温度过高，已经达到{}°。'.format(cardName,tempreature)
                        notice.append(msg)
                    stateEvaluation[cardName][3]=0 if stateEvaluation[cardName][3]>100 else stateEvaluation[cardName][3]+1  
                #算力预警
                if(hashrate<stateEvaluation[cardName][0]):
                    if(stateEvaluation[cardName][4]==0):
                        msg='机器{},算力较低：{}M/s。'.format(cardName,hashrate)
                        notice.append(msg)
                    stateEvaluation[cardName][4]=0 if stateEvaluation[cardName][4]>100 else stateEvaluation[cardName][4]+1  
                #功耗预警
                if(P>stateEvaluation[cardName][2]):
                    if(stateEvaluation[cardName][5]==0):
                        msg='机器{},功耗高：{}W。'.format(cardName,P)
                        notice.append(msg)
                    stateEvaluation[cardName][5]=0 if stateEvaluation[cardName][5]>100 else stateEvaluation[cardName][5]+1  
                    
        except:
            continue
    info="workers:{},".format(workers)+"Total hashrate={:.2f}, ".format(sumrate)+"All power:{}W".format(power)
    print(info)
    #print("##############################################################")
    ##连续10次确认到的矿机数量
    if(workers!=workersLast):
        workersFlag+=1
        if(workersFlag==5):
            if(workersLast-workers>0):
                msg="矿机掉线了{}台,现有{}张卡工作中，总的算力为{:.2f}。".format(workersLast-workers,workers,sumrate)
                notice.append(msg)
            else:
                msg="新增了{}台矿机,现有{}张卡工作中，总的算力为{:.2f}。".format(workers-workersLast,workers,sumrate)
                notice.append(msg)
            workersLast=workers
    else:
        workersFlag=0
        # workersLast=workers
    # time.sleep(1)
    if(len(notice)): 
        Alis.sendmail(notice,receivers[0])
        notice.clear()

