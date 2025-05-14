#2025-05-14 01:42:36
"""
new Env('柒猫海盗船');
柒猫小说 - APP
抓包搜：xiaoshuo.wtzw.com 请求头里的 authorization 和 qm-params
变量填写 例如：        多账号 @ 或者 换行 进行分割
export qmcookie='authorization#qm-params#名称'  名称随便填，区分帐号用
export qmtoken='卡密'
定时一天一次即可
"""
WnI=print
Wnd=True
Wni=None
WnD=False
Wnh=str
WnF=int
Wnb=Exception
Wnr=range
Wna=exit
Wnj=open
WnG=len
import random
WnH=random.randint
import requests
WnO=requests.session
import base64
WnB=base64.b64decode
import time
WnX=time.sleep
Wnk=time.time
Wnt=time.localtime
WnC=time.strftime
import json
WnV=json.loads
import os
WnJ=os.environ
from functools import partial
WnI=partial(WnI,flush=Wnd)
Wno='柒猫海盗船'
Wnc="1662816800435"
WnE=WnB("MTIwLjQ4LjU5Ljg0").decode()
Wns='webviewversion/0'
def WnQ():
 Wnq=WnC('%Y-%m-%d %H:%M:%S',Wnt(Wnk()))
 return Wnq
def Wnw(taskid):
 try:
  WnP=WnK(taskid)
  if WnP["url"]==Wni:
   return WnD
  if WnP["code"]==200:
   WnU=WnN('post',Wnh(WnP["url"]),Wnh(WnP["params"]),Wnh(WnP["sign"]))
   Wnp=WnV(WnU)
   if "data" in Wnp:
    WnI('柒猫海盗船 '+Wnh(WnR)+' 账号['+WnA+']看视频成功 金币+'+Wnp["data"]["coin"])
    return WnF(Wnp["data"]["times"])
   else:
    WnI('柒猫海盗船 '+Wnh(WnR)+' 账号['+WnA+']'+Wnp["errors"]["title"])
    return 0
 except Wnb as e:
  WnI('error: '+Wnh(e))
def WnK(taskid):
 Wng="http://"+WnE+":3394/qimao/qm_api.php"
 Wnm={"token":Wnu,"method":"calculate","taskid":taskid,"auth":Wnl,"qmparams":WnL,"version":Wnc}
 for Wnz in Wnr(1,5):
  try:
   WnU=s.post(url=Wng,json=Wnm).text.strip()
   Wnp=WnV(WnU)
   if Wnp["code"]==200:
    WnI("柒猫海盗船 token剩余次数:"+Wnh(Wnp["num"])+"  token过期时间:"+Wnh(Wnp["date"]))
    return Wnp
   else:
    WnI("柒猫海盗船 api请求失败："+Wnp["msg"])
    Wna()
  except Wnb as e:
   WnI('柒猫海盗船 api请求失败，尝试第'+Wnh(Wnz+1)+'次获取！')
   WnX(5)
 WnI('柒猫海盗船 api请求失败！不再尝试获取。')
 Wna()
 return-1
def Wny():
 Wng="http://"+WnE+":3394/qimao/qm_api.php"
 Wnm={"token":Wnu,"method":"check","version":Wnc}
 for Wnz in Wnr(1,5):
  try:
   WnU=s.post(url=Wng,json=Wnm).text.strip()
   Wnp=WnV(WnU)
   if Wnp["code"]==200:
    WnI("柒猫海盗船 token剩余次数:"+Wnh(Wnp["num"])+"  token过期时间:"+Wnh(Wnp["date"]))
    return Wnd
   else:
    WnI("柒猫海盗船 api请求失败："+Wnp["msg"])
    Wna()
  except Wnb as e:
   WnI('柒猫海盗船 api请求失败，尝试第'+Wnh(Wnz+1)+'次获取！')
   WnX(5)
 WnI('柒猫海盗船 api请求失败！不再尝试获取。')
 Wna()
 return-1
def WnN(method,Wng,Wnm,sign):
 WnM={"net-env":"4","channel":"qm-xiaomi_lf","is-white":"0","platform":"android","app-version":"7172020","application-id":"com.kmxs.reader","authorization":Wnl,"qm-params":WnL,"user-agent":Wns,"sign":sign,"content-type":"application/x-www-form-urlencoded"}
 if method=='post':
  WnU=s.post(url=Wng,headers=WnM,data=Wnm).text
 else:
  WnU=s.get(url=Wng,headers=WnM).text
 return WnU
if __name__=='__main__':
 s=WnO()
 Wnu=WnJ.get("qmtoken")
 if not Wnu:
  WnI("qmtoken不能为空")
  Wna()
 try:
  if "@" in WnJ.get("qmcookie"):
   Wne=WnJ["qmcookie"].split("@")
  else:
   Wne=WnJ["qmcookie"].split("\n")
 except:
  with Wnj('qmcookie.txt','r')as f:
   Wne=f.read().split('\n')
 WnI('??'+Wno,flush=Wnd)
 WnI('==================共找到'+Wnh(WnG(Wne))+'个ck==================')
 WnI('==================脚本执行- 北京时间(UTC+8)：'+WnQ()+'=====================\n')
 Wny()
 WnR=0
 for tk in Wne:
  WnR+=1
  WnI(f'----- 开始【第 '+Wnh(WnR)+' 个账号】-----')
  Wnv=tk.split("#")
  if WnG(Wnv)<=2:
   WnA="账号"+Wnh(WnR)
  else:
   WnA=Wnv[2]
  Wnl=Wnv[0]
  WnL=Wnv[1]
  for i in Wnr(1,8):
   WnI('柒猫海盗船 '+Wnh(WnR)+' 账号['+WnA+']开始看视频-第'+Wnh(i)+'档')
   Wnz=Wnw(Wnh(i))
   if Wnz is not Wni:
    if Wnz<=0:
     continue
    while Wnz>=1:
     Wnz=Wnw(Wnh(i))
     WnX(WnH(3,5))
 WnI('==================脚本完毕-北京时间(UTC+8)：'+WnQ()+'=====================\n')
