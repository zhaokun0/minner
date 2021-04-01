
from selenium import webdriver
import re
import time
import AliSendmail as Alis

browser = webdriver.Chrome()
time.sleep(1)
browser.get('填写蜜蜂矿池的观察者链接')
time.sleep(1)
html=browser.page_source
#填矿工的名称。
temp=re.findall(r"<tr data-worker=\"矿工名\">.*? <!----> <!---->",html)
temp0=re.findall(r"\d+\.?\d*MH/s",temp[0])
temp1=re.findall(r'\d+\.?\d*',temp0[2])
qjhash=float(temp1[0])
browser.close()

browser = webdriver.Chrome()
time.sleep(1)
browser.get('https://www.beepool.com/income/top?gpu=')
time.sleep(1)
html=browser.page_source
rs=re.findall(r'ETH</span></td><td>(\d+\.?\d*)',html)
rs1=re.findall(r'class="day_income">¥ (\d+\.?\d*)',html)
money=float(rs1[0])/float(rs[0])*qjhash*0.98
browser.close()
msg="当日结算金额：{:d}￥".format(round(money))
print(msg)
#填写收件人邮件地址
Alis.sendmail(msg,'17863118591@163.com')

