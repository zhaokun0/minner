
urls=[
] #这里是需要获取的网页
for i in range(11,60):
    url="http://192.168.0.{:d}:22333/api/v1/status".format(i)
    urls.append(url)

#用于判断各项指标是否正常
#哈希率，温度值，功耗值,第四个用于计数使用
stateEvaluation={
    'GeForce RTX 3060':[44,60,135,0,0,0],
    'GeForce GTX 1660 SUPER':[30,60,90,0,0,0],
    'GeForce GTX 1060 6GB':[20,60,100,0,0,0],
    'GeForce RTX 3060 Ti':[60,55,118,0,0,0],
    'GeForce RTX 2060 SUPER':[38,60,150,0,0,0],
    'GeForce RTX 2060':[35,70,85,0,0,0],
    'GeForce RTX 3060 Laptop GPU':[48,75,96,0,0,0],
    'GeForce GTX 1060 5GB':[16,60,70,0,0,0],
    'Graphics Device':[30,60,85,0,0,0],#这是1066s
    'NVIDIA GeForce RTX 3060':[44,65,135,0,0,0],
    'GeForce GTX 1060':[8.3,79,95,0,0,0],#1063笔记本
    'GeForce GTX 1080':[35,65,130,0,0,0],#1080笔记本
    'GeForce GTX 1080 Ti':[45,65,210,0,0,0],#1080ti笔记本
}