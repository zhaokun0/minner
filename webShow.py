#coding=utf-8
from flask import Flask
from flask import render_template
import requests
import re
import time
import math
#对ASCII编码的进行解码
import chardet 
import commons as cm

#内容打包
import pickle
#多进程操作
from multiprocessing import Process
import os


urls=cm.urls
stateEvaluation=cm.stateEvaluation

def readall():
    cards=[]
    workers=0 #卡数
    sumrate=0 #总哈希率
    powers=0 #总功率
    for url in urls:
            try:
                content=requests.get(url,timeout=5).content
                encode_type = chardet.detect(content)
                content = content.decode(encode_type['encoding'])
                if('Unable to round-trip http request to upstream' in content):
                    continue
                a=content.split('{"accepted_shares":')
                for i in range(1,len(a)-1):
                    #获取卡的工作状态
                    info=a[i]
                    
                    info=info.replace('\"','').replace('}','').replace('{','')
                    item=info.split(',')
                    cardName=item[9].replace('info:','')
                    hashrate=float(re.findall(r"\d+\.?\d*",item[4])[0])
                    fan=int(item[3].replace('fan:',''))
                    temperature=int(item[16].replace(']','').replace('temperature:',''))
                    power=int(item[14].replace('power:',''))
                    #判定卡的状态是否是异常的
                    hashState=0
                    tempState=0
                    powerState=0
                    if(hashrate<stateEvaluation[cardName][0]):
                        hashState=1
                    if(temperature>stateEvaluation[cardName][1]):
                        tempState=1
                    if(power>stateEvaluation[cardName][2]):
                        powerState=1
                    # print(hashState,tempState,powerState)
                    #print(cardName,'：\n','hashrate:',hashrate,'M',' \t| ','fan:',fan,' \t| ','temperature:',temperature,' \t| ','power:',power)
                    cards.append([cardName,hashrate,fan,temperature,power,[hashState,tempState,powerState]])#构造传入html的参数
                    sumrate+=hashrate
                    workers+=1
                    powers+=power
            except:
                continue
    summary=[workers,round(sumrate,2),powers]
    return cards,summary


def writeTofile(doc):
    webFile=open('webinfo.pkl','wb')
    pickle.dump(doc,webFile)


def readFromfile():
    try:
        webFile=open('webinfo.pkl','rb')
        doc=pickle.load(webFile)
        cards=doc[0]
        summary=doc[1]
    except:
        cards=None
        summary=None
    return  cards,summary
        

def msgprocess():
    while True:
        cards,summary=readall()
        doc=[cards,summary]
        writeTofile(doc)
        time.sleep(30)

app = Flask(__name__)

@app.route('/')
def hello():
    cards,summary=readFromfile()
    return render_template('web.html', cards=cards,summary=summary)
def startweb():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    p1 = Process(target=msgprocess)
    p2 = Process(target=startweb)
    print('Child process will start.')
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print('Child process end.')
    

