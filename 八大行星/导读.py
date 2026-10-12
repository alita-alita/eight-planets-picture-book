# -*- coding: utf-8 -*-
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.colors import HexColor
from PIL import Image
import random,math
p=Path(__file__).resolve().parent;W,H=landscape(A3);half=W/2
pdfmetrics.registerFont(TTFont('CN','/System/Library/Fonts/STHeiti Medium.ttc',subfontIndex=1))
pdfmetrics.registerFont(TTFont('NUM','/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf'))
INK='#EDF4FF';BLUE='#7BDFFF';MUTED='#B3C4E2';GOLD='#FFD16B'
c=canvas.Canvas(str(p/'资料'/'导读与总结.pdf'),pagesize=(W,H))
def t(x,y,s,z=20,col=INK,f='CN'):c.setFont(f,z);c.setFillColor(HexColor(col));c.drawString(x,y,s)
def ls(x,y,ss,z=21,lead=35):
 for s in ss:t(x,y,s,z);y-=lead

def start(unified=False):
 if unified:
  c.setFillColor(HexColor('#0B1430'));c.rect(0,0,W,H,fill=1,stroke=0)
 else:
  for x,col in [(0,'#0B1430'),(half,'#191737')]:c.setFillColor(HexColor(col));c.rect(x,0,half,H,fill=1,stroke=0)
 r=random.Random(22)
 for i in range(70):
  c.setFillColor(HexColor(r.choice([BLUE,GOLD,MUTED])));c.circle(r.uniform(15,W-15),r.uniform(H-35,H-8),r.uniform(.3,1),fill=1,stroke=0)
def photo(k,x,y,w,h):
 f=p/'图片'/(k+'.jpg');im=Image.open(f);iw,ih=im.size
 crop=k=='金星可见光';vw=iw/2-45 if crop else iw;r=min(w/vw,h/ih);xx=x+(w-vw*r)/2;yy=y+(h-ih*r)/2
 c.saveState()
 if globals().get('panorama_compressed',False):
  c.translate(0,y+h/2);c.scale(1,1/.80);c.translate(0,-y-h/2)
 c.setBlendMode('Screen')
 if crop:
  path=c.beginPath();path.rect(xx,yy,vw*r,ih*r);c.clipPath(path,stroke=0,fill=0)
 c.drawImage(str(f),xx,yy,iw*r,ih*r);c.restoreState()
def line(x,y,w):c.setStrokeColor(HexColor('#46567B'));c.line(x,y,x+w,y)
planets=[('水星','PIA15160'),('金星','金星可见光'),('地球','地球'),('火星','火星'),('木星','PIA00343'),('土星','土星'),('天王星','PIA18182'),('海王星','PIA01492')]
start();t(44,775,'给爱问“有多大”的小朋友',18,GOLD)
t(42,692,'小小宇航员',54);t(42,621,'八大行星',54);t(44,578,'看真实影像 · 听星球故事 · 玩数字游戏',18,MUTED)
for i,(n,k) in enumerate(planets):
 x=44+(i%4)*128;y=332-(i//4)*154;photo(k,x,y,110,110);t(x+20,y-25,n,17)
t(44,94,'和爸爸妈妈一起，从地球出发。',21);t(44,45,'A3横向跨页 / 简体中文 / 适合亲子共读',12,MUTED)
x=half+44;t(x,773,'这本书，怎么玩？',34);ls(x,709,['每次认识一颗行星。','先看大图，再听一个小故事。','数字很多，可以挑最喜欢的读。'])
for y,num,head,ss in [(548,'01','看一看',['找颜色、找云带、找撞击坑。','照片放大程度不同，别直接量大小。']),(399,'02','比一比',['先说清楚比什么：宽、体积，还是质量？','“一天”也要分自转周期和太阳日。']),(250,'03','点一点',['圆圈里的编号，对应点读文稿。','贴好两支笔各自的录音贴，再绑定音频。'])]:
 t(x,y,num,35,BLUE,'NUM');t(x+70,y+2,head,24);ls(x+70,y-37,ss,17,29)
ls(x,103,['内容编号不是厂商点读码；部分音频已生成，现暂停；新增稿件待配音。','每张A3是阅读跨页，中央对折后单页A4。'],12,22);c.showPage()
start();t(44,773,'太阳的一家',34);ls(44,718,['太阳是一颗恒星，会自己发光发热。','八大行星都围绕太阳运动。'],22,36)
photo('太阳',80,286,400,400);t(44,233,'太阳不是八大行星中的一颗。',23)
ls(44,180,['太阳：NASA/SDO/HMI观测影像，橙色为赋色。','书中行星与太阳的图片不按同一比例摆放。','冥王星属于矮行星，不列入八大行星。'],13,24)
x=half+44;t(x,773,'从近到远，排好队',34)
starts=[8,14,20,27,34,41,47,53]
# 完整合订稿：7个导读跨页，然后各章节；这里使用阅读页而非印刷拼版页。
for i,((n,k),s) in enumerate(zip(planets,starts)):
 y=682-i*75;photo(k,x,y-8,55,55);t(x+78,y+11,str(i+1),24,BLUE,'NUM');t(x+117,y+12,n,23);t(x+330,y+14,'第'+str(s)+'跨页',15,MUTED)
ls(x,64,['这里只表示距太阳的先后，不按真实距离排列。','外侧四颗都有环，内侧四颗没有行星环。'],11.5,19);c.showPage()
# 斜上方观察的立体公转示意；共面轨道以明暗与遮挡表现纵深。
start(unified=True);t(44,773,'八大行星，都围着太阳转',34)
t(44,727,'每颗行星，都沿着自己的轨道绕太阳走。',20)
t(44,688,'从太阳系北侧斜着看 · 箭头表示公转方向',13,MUTED)
t(44,662,'地球轨道平面作基准（0°），其余轨道略有倾斜。',13,BLUE)
cx=550;cy=470
radii=[85,135,185,235,300,365,435,520]
angles=[135,320,60,230,150,330,55,205]
# JPL J2000近似轨道要素：轨道倾角与升交点经度（度）。
incls=[7.00497902,3.39467605,0,1.84969142,1.30439695,2.48599187,.77263783,1.77004347]
nodes=[48.33076593,76.67984255,0,49.55953891,100.47390909,113.66242448,74.01692503,131.78422574]
inc_labels=['7.0','3.4','0','1.8','1.3','2.5','0.8','1.8']
def project(rx,ang):
 idx=radii.index(rx);inc=math.radians(incls[idx]);node=math.radians(nodes[idx]);u=math.radians(ang)-node
 X=rx*(math.cos(node)*math.cos(u)-math.sin(node)*math.sin(u)*math.cos(inc))
 Y=rx*(math.sin(node)*math.cos(u)+math.cos(node)*math.sin(u)*math.cos(inc))
 Z=rx*math.sin(u)*math.sin(inc)
 return cx+X,cy+.30*Y+math.sqrt(.91)*Z
sizes=[28,38,44,34,72,100,58,58]
periods=['88天','224.7天','1年','687天','11.9年','29.4年','84年','165年']
# 微弱的轨道平面光晕，只表示观察视角，不是太空中的实体。
c.saveState()
for j in range(16):
 c.setFillColor(HexColor('#254B7A'));c.setFillAlpha(.008)
 r=520-j*14;c.ellipse(cx-r,cy-r*.30,cx+r,cy+r*.30,fill=1,stroke=0)
c.restoreState()
def orbit_arc(rx,startangle,extent,col,width):
 c.setStrokeColor(HexColor(col));c.setLineWidth(width)
 q=c.beginPath()
 for step in range(181):
  xx,yy=project(rx,startangle+extent*step/180)
  if step==0:q.moveTo(xx,yy)
  else:q.lineTo(xx,yy)
 c.drawPath(q,fill=0,stroke=1)
def direction(rx,ang):
 x,y=project(rx,ang);x2,y2=project(rx,ang+.1)
 dx=x2-x;dy=y2-y;ll=math.hypot(dx,dy);dx/=ll;dy/=ll
 c.setFillColor(HexColor(BLUE));q=c.beginPath();q.moveTo(x+dx*7,y+dy*7);q.lineTo(x-dx*5-dy*3,y-dy*5+dx*3);q.lineTo(x-dx*5+dy*3,y-dy*5-dx*3);q.close();c.drawPath(q,fill=1,stroke=0)
for i,rx in enumerate(radii):
 orbit_arc(rx,0,180,'#324565',.8)
 orbit_arc(rx,180,180,'#7598C9',1.25)
 for angle in [20+i*7,245+i*5]:direction(rx,angle)
# 太阳光晕；真实太阳照片盖住背后的轨道线。
c.saveState()
for r in range(65,35,-2):
 c.setFillColor(HexColor('#FFB14B'));c.setFillAlpha(.012);c.circle(cx,cy,r,fill=1,stroke=0)
c.restoreState()
photo('太阳',cx-37,cy-37,74,74);t(cx-20,cy-67,'太阳',20,GOLD)
for i,((name,key),rx,ang,size) in enumerate(zip(planets,radii,angles,sizes)):
 xx,yy=project(rx,ang)
 c.setFillColor(HexColor('#0B1430'))
 if name=='土星':c.ellipse(xx-size/2,yy-size*.375,xx+size/2,yy+size*.375,fill=1,stroke=0)
 else:c.circle(xx,yy,size*.48,fill=1,stroke=0)
 photo(key,xx-size/2,yy-size/2,size,size)
 tw=pdfmetrics.stringWidth(name,'CN',19)
 ly=yy+size/2+13 if i in [0,2,4,6] else yy-size/2-25
 c.setFillColor(HexColor('#0B1430'));c.rect(xx-tw/2-2,ly-3,tw+4,23,fill=1,stroke=0)
 t(xx-tw/2,ly,name,19)
 label='轨道倾角约'+inc_labels[i]+'°';pw=pdfmetrics.stringWidth(label,'CN',11)
 c.setFillColor(HexColor('#0B1430'));c.rect(xx-pw/2-2,ly-20,pw+4,14,fill=1,stroke=0)
 t(xx-pw/2,ly-17,label,11,MUTED)
# 内侧四颗局部放大，便于辨认；仍是示意间距。
t(846,773,'内侧四颗 · 放大看',16,BLUE)
icx=978;icy=690
for j,r in enumerate([22,42,65,91]):
 c.setStrokeColor(HexColor('#526793'));c.setLineWidth(.65);q=c.beginPath()
 for step in range(181):
  px,py=project(radii[j],step*2);xx=icx+(px-cx)*r/radii[j];yy=icy+(py-cy)*r/radii[j]
  if step==0:q.moveTo(xx,yy)
  else:q.lineTo(xx,yy)
 c.drawPath(q,fill=0,stroke=1)
photo('太阳',icx-9,icy-9,18,18)
for j,((n,k),r,ang) in enumerate(zip(planets[:4],[22,42,65,91],[145,320,60,210])):
 px,py=project(radii[j],ang);xx=icx+(px-cx)*r/radii[j];yy=icy+(py-cy)*r/radii[j]
 c.setFillColor(HexColor('#0B1430'));c.circle(xx,yy,8,fill=1,stroke=0);photo(k,xx-7,yy-7,14,14)
 t(838+j*74,627,str(j+1)+' '+n,12,BLUE if j==2 else INK)
t(44,250,'八颗行星的轨道，倾斜多少？',18,GOLD)
t(694,250,'蓝色：地球参考面  /  金色：各行星轨道面',12,MUTED)
# 各小图沿各自交线方向选取相同低视角，真实倾角不夸张。
for i,(name,key) in enumerate(planets):
 xx=104+i*139; yy=167; r=58
 t(xx-31,215,str(i+1)+' '+name,16,BLUE if i==2 else INK)
 def disk(inc,col):
  q=c.beginPath()
  for j in range(121):
   a=2*math.pi*j/120; X=r*math.cos(a); Y=r*math.sin(a)
   # 倾斜面绕画面横向交线旋转，再以10度仰角投影。
   v=Y*math.sin(math.radians(10+inc))
   if j==0:q.moveTo(xx+X,yy+v)
   else:q.lineTo(xx+X,yy+v)
  q.close();c.saveState();c.setFillColor(HexColor(col));c.setFillAlpha(.12)
  c.setStrokeColor(HexColor(col));c.setLineWidth(1);c.drawPath(q,fill=1,stroke=1);c.restoreState()
 disk(0,BLUE);disk(incls[i],GOLD)
 c.saveState();c.setStrokeColor(HexColor(MUTED));c.setDash(2,3);c.setLineWidth(.5);c.line(xx-r,yy,xx+r,yy);c.restoreState()
 c.setFillColor(HexColor('#0B1430'));c.circle(xx,yy,8,fill=1,stroke=0)
 photo('太阳',xx-7,yy-7,14,14)
 a=math.radians(145);px=xx+r*math.cos(a);py=yy+r*math.sin(a)*math.sin(math.radians(10+incls[i]))
 c.setFillColor(HexColor('#0B1430'));c.circle(px,py,6,fill=1,stroke=0);photo(key,px-7,py-7,14,14)
 t(xx-17,116,inc_labels[i]+'°',23,BLUE,'NUM')
t(44,88,'以地球轨道平面为0°；倾角未夸张。每幅图分别选取观察方向，图上的投影夹角不能直接测量。',11,MUTED)
ls(44,59,['立体投影：按JPL近似轨道倾角与升交点方向绘制；为便于观察，轨道用圆环近似，半径未按比例。','角度以地球轨道平面为基准，是公转轨道倾角，不是自转轴倾角；行星位置不代表当前时刻。','使用真实观测影像。轨道线与光晕是示意；接下来用低视角与侧视图比较轨道倾斜。'],11,18)
c.showPage()
start();t(44,773,'数字大比拼',34);t(44,732,'把地球当基准，先看清比较的项目。',18)
headers=['行星','平均直径 / 公里','体积倍数','质量倍数'];xs=[44,133,345,465]
for x,h in zip(xs,headers):t(x,672,h,14,GOLD)
nums=[('水星','4,879','0.056','0.055'),('金星','12,104','0.857','0.815'),('地球','12,742','1','1'),('火星','6,779','0.151','0.107'),('木星','139,822','1,321','318'),('土星','116,500','764','95'),('天王星','50,724','63.1','14.5'),('海王星','49,244','57.7','17.1')]
for i,row in enumerate(nums):
 y=618-i*55
 for j,(x,s) in enumerate(zip(xs,row)):t(x,y,s,18,INK,'CN' if j==0 else 'NUM')
 line(44,y-18,half-88)
ls(44,128,['直径采用体积等效平均直径，数值为约数。','体积、质量分别以地球为1；行星环不计入直径。','体积倍数不是说能把这么多地球小球塞进去。'],12,23)
x=half+44;t(x,773,'我的太空护照',34);t(x,724,'每读完一颗，和家人一起做个记号。',18)
for i,(n,k) in enumerate(planets):
 col=i%2;row=i//2;xx=x+col*250;yy=566-row*119
 photo(k,xx,yy,72,72);t(xx+85,yy+43,n,21);line(xx+85,yy+14,110)
ls(x,119,['我最喜欢的星球：________________','我还想知道：____________________'],19,40)
c.save();print('导读和总结完成')
