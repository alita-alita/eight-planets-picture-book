# -*- coding: utf-8 -*-
from pathlib import Path
import math,csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from PIL import Image
p=Path(__file__).resolve().parent;W,H=landscape(A3)
pdfmetrics.registerFont(TTFont('CN','/System/Library/Fonts/STHeiti Medium.ttc',subfontIndex=1));pdfmetrics.registerFont(TTFont('NUM','/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf'))
c=canvas.Canvas(str(p/'资料/自转轴倾角.pdf'),pagesize=(W,H));rows=[]
blue='#7BDFFF';white='#EDF4FF';muted='#B3C4E2';gold='#FFD16B'
data=[('水星','PIA15160',0.034,'几乎直着转。','水星的自转轴倾角约零点零三四度，非常接近零度，可以想成几乎直着转。'),('金星','金星可见光',177.4,'方向倒过来了！','金星的自转轴倾角约一百七十七点四度，接近一百八十度。轴的箭头几乎向下，表示自转方向和地球相反，不是倾角只有二点六度。'),('地球','地球',23.4,'歪一点，四季会变化。','地球的自转轴倾角约二十三点四度。地球带着倾斜的地轴绕太阳走，各地得到阳光的情况会变化，这是四季形成的重要原因。'),('火星','火星',25.2,'和地球倾斜得很接近。','火星的自转轴倾角约二十五点二度，和地球很接近。火星也有四季，但它绕太阳一圈更久。'),('木星','PIA00343',3.1,'只歪了一点点。','木星的自转轴倾角约三点一度，比地球小得多，可以想成比较直着转。'),('土星','土星',26.7,'和地球、火星相近。','土星的自转轴倾角约二十六点七度，和地球、火星比较接近。这里量的是自转轴，不是照片上光环的斜度。'),('天王星','PIA18182',97.8,'像侧着身子转。','天王星的自转轴倾角约九十七点八度，比九十度还多一点，像侧着身子转。也可以把它取整，说约九十八度。'),('海王星','PIA01492',28.3,'也歪着身子转。','海王星的自转轴倾角约二十八点三度，比地球稍大。它也会经历季节变化，但绕太阳一圈要约一百六十五个地球年。')]
def t(x,y,s,z=18,col=white,font='CN'):
 c.setFont(font,z);c.setFillColor(HexColor(col));c.drawString(x,y,s)
def photo(key,x,y,w,h):
 im=Image.open(p/'图片'/(key+'.jpg'));iw,ih=im.size;vw=iw/2-45 if key=='金星可见光' else iw;r=min(w/vw,h/ih);xx=x+(w-vw*r)/2;yy=y+(h-ih*r)/2
 c.saveState();c.setBlendMode('Screen')
 if vw!=iw:
  q=c.beginPath();q.rect(xx,yy,vw*r,ih*r);c.clipPath(q,stroke=0,fill=0)
 c.drawImage(str(p/'图片'/(key+'.jpg')),xx,yy,iw*r,ih*r);c.restoreState()
for page in range(2):
 c.setFillColor(HexColor('#0B1430'));c.rect(0,0,W,H,fill=1,stroke=0)
 t(44,774,'星球转起来，身体歪多少？',34);t(44,731,'自转轴倾角 / '+('水星 · 金星 · 地球 · 火星' if page==0 else '木星 · 土星 · 天王星 · 海王星'),19,blue)
 t(44,690,'先想象一根穿过星球中心的转轴，再和“直立参考线”比较。',19)
 for j,(name,key,a,desc,script) in enumerate(data[page*4:page*4+4]):
  x=44+j*282;cx=x+119
  t(x,638,name,27);t(x,590,str(a)+'°',38,blue,'NUM');t(x,554,desc,16)
  photo(key,x,375,240,150)
  t(x,352,'观测影像（部分赋色）/ 来源见各章',10,muted)
  cy=232;L=62
  c.setStrokeColor(HexColor('#46567B'));c.setDash(4,4);c.setLineWidth(1);c.line(cx,cy-76,cx,cy+76);c.setDash()
  c.line(x+22,cy,x+218,cy);t(x+27,cy-20,'公转轨道平面（侧视）',11,muted)
  theta=math.radians(a);dx=math.sin(theta)*L;dy=math.cos(theta)*L
  c.setStrokeColor(HexColor(gold));c.setFillColor(HexColor(gold));c.setLineWidth(3);c.line(cx-dx,cy-dy,cx+dx,cy+dy)
  ex,ey=cx+dx,cy+dy;ux,uy=math.sin(theta),math.cos(theta)
  q=c.beginPath();q.moveTo(ex,ey);q.lineTo(ex-ux*11-uy*5,ey-uy*11+ux*5);q.lineTo(ex-ux*11+uy*5,ey-uy*11-ux*5);q.close();c.drawPath(q,fill=1,stroke=0)
  c.circle(cx,cy,3,fill=1,stroke=0)
  c.setStrokeColor(HexColor(blue));c.setLineWidth(1.2);c.arc(cx-28,cy-28,cx+28,cy+28,90-a,a)
  t(x+25,cy+85,'虚线：垂直于轨道的参考线',11,muted)
  code='AX'+f'{page*4+j+1:02d}';c.setStrokeColor(HexColor(blue));c.circle(x+18,104,17,fill=0,stroke=1);t(x+5,101,code,8,blue,'NUM');t(x+45,99,'听倾角',14)
  rows.append(['倾角补充',code,'听倾角',script,'待填写','待填写'])
 t(44,57,'金色箭头是自转轴方向的示意；箭头按右手规则定义，用来区分正向与逆向自转。',12,muted)
 t(44,36,'照片朝向、星球大小均不用于量角度。倾角相对各自轨道的垂线；不是轨道倾角。数值为近似值。',11,muted)
 t(44,17,'数据：NASA Planetary Fact Sheet / nssdc.gsfc.nasa.gov/planetary/factsheet/',10,muted)
 c.showPage()
c.save()
with (p/'资料/倾角点读对应表.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['章节','内容编号','标签','旁白','JOJO G3贴纸编号','小猴皮皮SE贴纸编号']);w.writerows(rows)
