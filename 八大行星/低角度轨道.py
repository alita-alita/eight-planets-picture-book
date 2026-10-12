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
c=canvas.Canvas(str(p/'资料/低角度轨道立体图.pdf'),pagesize=(W,H));rows=[]
blue='#7BDFFF';white='#EDF4FF';muted='#B3C4E2';gold='#FFD16B'
data=[('水星','PIA15160',0.034,'几乎直着转。','水星的自转轴倾角约零点零三四度，非常接近零度，可以想成几乎直着转。'),('金星','金星可见光',177.4,'方向倒过来了！','金星的自转轴倾角约一百七十七点四度，接近一百八十度。轴的箭头几乎向下，表示自转方向和地球相反，不是倾角只有二点六度。'),('地球','地球',23.4,'歪一点，四季会变化。','地球的自转轴倾角约二十三点四度。地球带着倾斜的地轴绕太阳走，各地得到阳光的情况会变化，这是四季形成的重要原因。'),('火星','火星',25.2,'和地球倾斜得很接近。','火星的自转轴倾角约二十五点二度，和地球很接近。火星也有四季，但它绕太阳一圈更久。'),('木星','PIA00343',3.1,'只歪了一点点。','木星的自转轴倾角约三点一度，比地球小得多，可以想成比较直着转。'),('土星','土星',26.7,'和地球、火星相近。','土星的自转轴倾角约二十六点七度，和地球、火星比较接近。这里量的是自转轴，不是照片上光环的斜度。'),('天王星','PIA18182',97.8,'像侧着身子转。','天王星的自转轴倾角约九十七点八度，比九十度还多一点，像侧着身子转。原来书中写约九十八度，是把这个数字取整。'),('海王星','PIA01492',28.3,'也歪着身子转。','海王星的自转轴倾角约二十八点三度，比地球稍大。它也会经历季节变化，但绕太阳一圈要约一百六十五个地球年。')]
def t(x,y,s,z=18,col=white,font='CN'):
 c.setFont(font,z);c.setFillColor(HexColor(col));c.drawString(x,y,s)
def photo(key,x,y,w,h):
 im=Image.open(p/'图片'/(key+'.jpg'));iw,ih=im.size;vw=iw/2-45 if key=='金星可见光' else iw;r=min(w/vw,h/ih);xx=x+(w-vw*r)/2;yy=y+(h-ih*r)/2
 c.saveState();c.setBlendMode('Screen')
 if vw!=iw:
  q=c.beginPath();q.rect(xx,yy,vw*r,ih*r);c.clipPath(q,stroke=0,fill=0)
 c.drawImage(str(p/'图片'/(key+'.jpg')),xx,yy,iw*r,ih*r);c.restoreState()


c.setFillColor(HexColor('#0B1430'));c.rect(0,0,W,H,fill=1,stroke=0)
t(44,774,'把视线放低，看见轨道的倾斜',34)
t(44,726,'以水星与地球为例 / 两张轨道平面，像两张微微张开的纸',20,blue)
t(44,686,'淡蓝色是地球轨道参考面；金色是水星轨道平面。',17)
cx,cy=430,459;view=math.radians(10);inc=math.radians(7);node=math.radians(40)
def proj(r,ang,i=0):
 u=math.radians(ang)-node
 X=r*(math.cos(node)*math.cos(u)-math.sin(node)*math.sin(u)*math.cos(i))
 Y=r*(math.sin(node)*math.cos(u)+math.cos(node)*math.sin(u)*math.cos(i))
 Z=r*math.sin(u)*math.sin(i)
 return cx+X,cy+Y*math.sin(view)+Z*math.cos(view)
def plane(r,i,col,alpha):
 q=c.beginPath()
 for j in range(361):
  x,y=proj(r,j,i)
  if j==0:q.moveTo(x,y)
  else:q.lineTo(x,y)
 q.close();c.saveState();c.setFillColor(HexColor(col));c.setFillAlpha(alpha);c.drawPath(q,fill=1,stroke=0);c.restoreState()
def orbit(r,i,col):
 c.setStrokeColor(HexColor(col));c.setLineWidth(1.8)
 q=c.beginPath()
 for j in range(361):
  x,y=proj(r,j,i)
  if j==0:q.moveTo(x,y)
  else:q.lineTo(x,y)
 c.drawPath(q,fill=0,stroke=1)
plane(365,0,blue,.13);plane(280,inc,gold,.12)
# 参考面的网格帮助观察空间投影。
c.saveState();c.setStrokeColor(HexColor('#355171'));c.setLineWidth(.5)
for angle in [0,30,60,90,120,150]:
 x,y=proj(365,angle);xx,yy=proj(365,angle+180);c.line(x,y,xx,yy)
c.restoreState();orbit(365,0,blue);orbit(280,inc,gold)
# 两平面交线穿过太阳；这是平面交线，并不是两行星轨道相交。
x,y=proj(365,40);xx,yy=proj(365,220);c.setStrokeColor(HexColor('#B3C4E2'));c.setDash(4,4);c.line(x,y,xx,yy);c.setDash()
c.setFillColor(HexColor('#0B1430'));c.circle(cx,cy,34,fill=1,stroke=0)
photo('太阳',cx-35,cy-35,70,70);t(cx-20,cy-62,'太阳',19,gold)
mx,my=proj(280,130,inc);base_x,base_y=proj(280,130,0)
c.setStrokeColor(HexColor(gold));c.setDash(2,3);c.line(mx,my,base_x,base_y);c.setDash();c.setFillColor(HexColor('#0B1430'));c.circle(mx,my,23,fill=1,stroke=0);photo('PIA15160',mx-23,my-23,46,46)
t(mx-25,my+43,'水星',21);t(mx-65,my+21,'金色：水星轨道平面',13,gold)
ex,ey=proj(365,323,0);c.setFillColor(HexColor('#0B1430'));c.circle(ex,ey,27,fill=1,stroke=0);photo('地球',ex-28,ey-28,56,56);t(ex-24,ey-54,'地球',21)
t(70,365,'淡蓝色：地球轨道平面（0°）',17,blue)
t(70,336,'金色轨道有一半高于参考面，另一半低于参考面。',15)
# 单独沿平面交线方向看，真实7度才能直接画成纸面的7度。
t(849,641,'换个方向，量角度',24)
t(849,604,'沿两平面的交线方向侧视',14,muted)
ox,oy=872,482;L=255;a=math.radians(7)
c.setStrokeColor(HexColor(blue));c.setLineWidth(1.5);c.line(ox,oy,ox+L,oy)
c.setStrokeColor(HexColor(gold));c.setLineWidth(2.4);c.line(ox,oy,ox+L*math.cos(a),oy+L*math.sin(a))
c.setStrokeColor(HexColor(white));c.setLineWidth(1);c.arc(ox-170,oy-170,ox+170,oy+170,0,7)
t(930,549,'7°',52,blue,'NUM');t(849,432,'水星公转轨道倾角约7°',18)
t(849,399,'这里的7°没有夸张。',15,muted)
t(849,371,'主图里的投影夹角不能直接量。',14,muted)
c.setStrokeColor(HexColor('#355171'));c.setLineWidth(.7);c.line(44,292,W-44,292)
t(44,254,'找一找：金色平面在哪里高一点？在哪里低一点？',22)
t(44,215,'这说的是绕太阳的“路”倾斜多少，不是星球自身转轴歪多少。',19)
t(44,177,'平面相交，不代表水星轨道和地球轨道相交；它们离太阳的距离不同。',16,muted)
for x,code,label,script in [(62,'LV01','听立体轨道','淡蓝色的面代表地球绕太阳的轨道平面。金色的面代表水星轨道平面，两张平面微微张开，夹角约七度。水星沿着自己的轨道走，会经过参考面上方和下方。两张平面相交，不表示两颗行星的轨道相交。'),(615,'LV02','换个方向看','主图是立体投影，看见的夹角不一定就是真实角度。沿两张平面的交线方向侧着看，右边小图才能直接画出七度。公转轨道倾角与自转轴倾角不同。')]:
 c.setStrokeColor(HexColor(blue));c.circle(x,111,17,fill=0,stroke=1);t(x-12,108,code,8,blue,'NUM');t(x+29,106,label,14);rows.append(['低角度立体补充',code,label,script,'待填写','待填写'])
t(44,65,'轨道平面用圆盘示意，不是实体；轨道用圆环近似。大小、距离和行星位置均为示意，非当前时刻。',11,muted)
t(44,43,'主图以7°构建空间关系；观察方向经过选择，便于理解。右图为单独的正侧视角。',11,muted)
t(44,21,'数据：NASA Planetary Fact Sheet / 水星公转轨道倾角约7°，相对地球轨道平面。',10,muted)
c.showPage();c.save()
with (p/'资料/低角度点读对应表.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['章节','内容编号','标签','旁白','JOJO G3贴纸编号','小猴皮皮SE贴纸编号']);w.writerows(rows)
