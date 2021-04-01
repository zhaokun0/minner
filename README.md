# 简介
    此代码主要实现web端远程监视矿机，以及采用邮件的方式报告矿机工作状态的变动与异常状况。
#### 示例：
[机器状态示范](http://101.132.155.12:5000/)
![Image text](https://github.com/zhaokun0/minner/blob/master/IMG/web.png)
邮件通知：

![Image text](https://github.com/zhaokun0/minner/blob/master/IMG/mail.png)

# 教程
## 1.运行环境搭建(Windows)
   默认您已有python3环境，相关依赖包有flask、requests，可执行以下代码安装：

               `pip install flask requests`
   在不同网络下的机器，可以使用zerotier one 搭建虚拟局域网，此内容自行研究。
   若想通过外网访问，需要服务部署在服务器上，或是自己有公网ip，这部分请自行发挥。邮件通知功能不需要。
## 2.各文件功能及说明
   子模块commons.py中，urls所存放的是各个机器的访问页面链接，需要根据自己的机器填写，stateEvaluation设定的是显卡的名称，算力报警、温度报警、功耗报警的阈值，stateEvaluation必须加入自己卡的信息。
   
   子模块AliSendmail.py用于发送邮件，代码中发件人地址和密码、收件人地址，需要自行填写：  
               ` username = '***@aliyun.com'#阿里云邮箱`  
               ` password = '****'`  
               ` rcptto = '17863118591@163.com'`  
           
   webShow.py是用于将各个矿机的数据整合到一起，通过网页进行显示，其网页的模板在templates\web.html中，根据自己网络的延迟情况，设定timeout参数，较差的网络需要设置高一些，不然有些机器找不到。  
               ` content=requests.get(url,timeout=5).content`  
   机器的状态会被写入到webinfo.plk，以便之后网页快速加载内容。
   
   watch.py用于发送邮件通知，填写自己的邮件地址即可。
   
## 运行程序
                `python webShow.py`
                `python watch.py`

   
   
   
           
   