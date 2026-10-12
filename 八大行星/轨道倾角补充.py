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
c=canvas.Canvas(str(p/'资料/公转轨道倾角.pdf'),pagesize=(W,H));rows=[]
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

items=[('水星','PIA15160',7.0,'七'),('金星','金星可见光',3.4,'三点四'),('地球','地球',0.0,'零'),('火星','火星',1.8,'一点八'),('木星','PIA00343',1.3,'一点三'),('土星','土星',2.5,'二点五'),('天王星','PIA18182',.8,'零点八'),('海王星','PIA01492',1.8,'一点八')]
c.setFillColor(HexColor('#0B1430'));c.rect(0,0,W,H,fill=1,stroke=0)
t(44,774,'绕太阳的路，也有一点斜',34)
t(44,729,'公转轨道倾角 / 地球轨道平面是0°参考平面',20,blue)
t(44,687,'这次比较“绕太阳的路”，不是星球自己转时的轴。',19)
for j,(name,key,inc,spoken) in enumerate(items):
 x=44+(j%4)*282;top=620-(j//4)*255
 photo(key,x,top-70,78,78);t(x+95,top-14,name,24);t(x+95,top-53,('0' if inc==0 else str(inc))+'°',30,blue,'NUM')
 cx=x+124;cy=top-128;L=103
 c.setStrokeColor(HexColor('#526793'));c.setLineWidth(1);c.setDash(4,3);c.line(cx-L,cy,cx+L,cy);c.setDash()
 a=math.radians(inc);dx=L*math.cos(a);dy=L*math.sin(a)
 c.setStrokeColor(HexColor(gold));c.setLineWidth(2.4);c.line(cx-dx,cy-dy,cx+dx,cy+dy)
 c.setFillColor(HexColor(blue));c.circle(cx,cy,3,fill=1,stroke=0)
 if inc>0:
  c.setLineWidth(1);c.setStrokeColor(HexColor(blue));c.arc(cx-72,cy-72,cx+72,cy+72,0,inc)
 t(x+18,top-167,'蓝虚线：地球轨道平面',12,muted)
 t(x+18,top-188,'金实线：该行星轨道平面',12,gold)
 code='OI'+f'{j+1:02d}';c.setStrokeColor(HexColor(blue));c.circle(x+18,top-219,15,fill=0,stroke=1);t(x+6,top-222,code,8,blue,'NUM');t(x+43,top-224,'听轨道',13)
 script=('把地球绕太阳的轨道平面当作参考，它的轨道倾角记为零度。' if name=='地球' else name+'的公转轨道倾角约为'+spoken+'度，是和地球轨道平面比较的角度。')
 script+='这和自转轴倾角不是同一件事。'
 if name=='天王星':script+='天王星虽然像侧着身子自转，但绕太阳的轨道只倾斜约零点八度。'
 if name=='水星':script+='八大行星中，水星的这个角度最大，但也不是竖着绕太阳转。'
 rows.append(['轨道倾角补充',code,'听轨道',script,'待填写','待填写'])
t(44,99,'每个小图都单独沿两轨道平面的交线方向侧视，分别对齐参考线；不是同一方向拍下的合影。',12,muted)
t(44,75,'线条角度按所列近似值绘制，没有夸张。距离、线长与照片大小不按真实比例。',12,muted)
t(44,51,'地球0°是参考平面的定义，并不表示地球的自转轴没有倾斜。轨道角度会缓慢变化。',12,muted)
t(44,27,'数据：NASA Planetary Fact Sheet；主图空间朝向参考JPL J2000近似轨道要素。',11,muted)
c.showPage();c.save()
with (p/'资料/轨道倾角点读对应表.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(['章节','内容编号','标签','旁白','JOJO G3贴纸编号','小猴皮皮SE贴纸编号']);w.writerows(rows)
