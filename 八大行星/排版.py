# -*- coding: utf-8 -*-
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from PIL import Image
import csv,json,math,random
from 内容 import P
p=Path(__file__).resolve().parent
pdfmetrics.registerFont(TTFont('CN','/System/Library/Fonts/STHeiti Medium.ttc',subfontIndex=1))
pdfmetrics.registerFont(TTFont('NUM','/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf'))
W,H=landscape(A3);half=W/2;CW=half-88
INK='#EDF4FF';BLUE='#7BDFFF';GOLD='#FFD16B';MUTED='#B3C4E2'
C=None;D=None;rows=[];widthlog=[]
def rect(x,y,w,h,col):
 C.setFillColor(HexColor(col));C.rect(x,y,w,h,fill=1,stroke=0)
def txt(x,y,s,size=20,col=INK,font='CN',fit=None):
 if fit:
  while pdfmetrics.stringWidth(s,font,size)>fit and size>10:size-=.25
 C.setFont(font,size);C.setFillColor(HexColor(col));C.drawString(x,y,s)
 if pdfmetrics.stringWidth(s,font,size)>CW and font=='CN' and x not in [42]:widthlog.append((D['name'] if D else '导读',s,size))
def wrap(s,size,w=CW):
 out=[];line=''
 for ch in s:
  if pdfmetrics.stringWidth(line+ch,'CN',size)>w and line:
   if ch in '，。？！：；、）》”％%':line+=ch;out.append(line);line=''
   else:out.append(line);line=ch
  else:line+=ch
 if line:out.append(line)
 return out

def para(x,y,ss,size=21,lead=34,col=INK,w=CW):
 for s in ss:
  for line in wrap(s,size,w):txt(x,y,line,size,col);y-=lead
 return y

def note(x,y,ss):return para(x,y,ss,11.5,18,MUTED)
def rule(x,y,w=CW):
 C.setStrokeColor(HexColor('#46567B'));C.setLineWidth(.7);C.line(x,y,x+w,y)
def photo(key,x,y,w,h,blend=True):
 f=p/'图片'/(key+'.jpg');im=Image.open(f);iw,ih=im.size
 original_iw=iw
 if key=='金星可见光':iw=iw/2-45
 r=min(w/iw,h/ih)
 C.saveState()
 if blend:C.setBlendMode('Screen')
 if key=='金星可见光':
  clip=C.beginPath();clip.rect(x+(w-iw*r)/2,y+(h-ih*r)/2,iw*r,ih*r);C.clipPath(clip,stroke=0,fill=0)
 C.drawImage(str(f),x+(w-iw*r)/2,y+(h-ih*r)/2,original_iw*r,ih*r)
 C.restoreState()
 # 在排版层淡化红外影像边缘，让深色底融入页面；源观测图不改动。
 if key in ['天王星环','海王星环']:
  px=x+(w-iw*r)/2;py=y+(h-ih*r)/2;pw=iw*r;ph=ih*r
  bg='#0B1430' if x<half else '#191737';feather=32
  C.saveState();C.setFillColor(HexColor(bg))
  for j in range(32):
   C.setFillAlpha((1-j/32)**1.6);q=j*feather/32;dd=feather/32+.1
   C.rect(px+q,py,dd,ph,fill=1,stroke=0);C.rect(px+pw-q-dd,py,dd,ph,fill=1,stroke=0)
   C.rect(px,py+q,pw,dd,fill=1,stroke=0);C.rect(px,py+ph-q-dd,pw,dd,fill=1,stroke=0)
  C.restoreState()
def start():
 rect(0,0,half,H,'#0B1430');rect(half,0,half,H,'#191737')
 rng=random.Random(471+(D['order'] if D else 0))
 for j in range(64):
  x=rng.uniform(20,W-20);y=rng.uniform(H-35,H-8)
  C.setFillColor(HexColor(rng.choice([BLUE,GOLD,MUTED])));C.circle(x,y,rng.choice([.45,.65,1.0]),fill=1,stroke=0)
def title(x,t,sub):txt(x,H-68,t,34,fit=CW);txt(x,H-107,sub,18,fit=CW)
def spot(x,y,idx,label,script):
 code=D['code']+f'{idx:02d}'
 C.setStrokeColor(HexColor(BLUE));C.setLineWidth(.8);C.circle(x,y,17,stroke=1,fill=0)
 txt(x-12,y-3,code,8,BLUE,'NUM');txt(x+26,y-5,label,14)
 rows.append([D['name'],code,label,script,'待填写','待填写'])
def pair(x,a,b,ls,rs):
 spot(x+18,66,a,ls[0],ls[1]);spot(x+280,66,b,rs[0],rs[1])
def end(n):
 txt(42,25,'小小宇航员 / '+D['name']+'站',10,MUTED);txt(W-62,25,str(n),11,INK,'NUM');C.showPage()
def pan(x,obj,a,b):
 title(x,obj['title'],obj['sub']);photo(obj['img'],x,390,CW,300)
 note(x,372,[obj['caption']]);para(x,315,obj['body'])
 if obj['number']:
  txt(x,154,obj['number'],43,BLUE,'NUM');off=pdfmetrics.stringWidth(obj['number'],'NUM',43)+20
  txt(x+off,160,obj['unit'],16,fit=CW-off)
 para(x,112,[obj['activity']],17,23,MUTED)
 narration=''.join(obj['body'])+(('这里的数字是'+obj['number']+obj['unit']+'。') if obj['number'] else '')
 pair(x,a,b,('听秘密',narration),('想一想',obj['activity']+obj['answer']))

def generate(d):
 global C,D,rows
 D=d;rows=[];name=d['name'];out=p/'章节'/name;out.mkdir(exist_ok=True)
 C=canvas.Canvas(str(out/(name+'_A3.pdf')),pagesize=(W,H));C.setTitle('小小宇航员 · '+name+' · A3真实影像版')
 # 1 认识星球
 start();txt(44,H-62,'太阳系的第'+str(d['order'])+'颗行星',17,GOLD)
 txt(42,H-146,'你好，'+name+'！',50,fit=CW);txt(44,H-180,d['en'],16,MUTED,'NUM')
 photo(d['img'],32,245,half-64,360);note(44,225,[d['cap']])
 para(44,184,d['intro'],20,32)
 pair(44,1,2,('听一听','你好，我是'+name+'。'+''.join(d['intro'])),('找一找','找一找照片里的'+name+'。'+(('它的云层把地面遮住了。旁边的雷达图才显示云下地形。') if name=='金星' else d['cover']['activity']+d['cover']['answer'])))
 pan(half+44,d['cover'],3,4);end(1)
 # 2 数字比较
 start();title(44,name+'，到底有多大？','比较平均直径；照片分别缩放。')
 if name=='地球':
  photo('地球',52,391,320,280);photo('月球',411,481,118,118);txt(161,366,'地球',18);txt(441,450,'月球',16)
 else:
  photo(d['img'],44,391,350,280);photo('地球',430,478,78,78);txt(170,366,name,18);txt(448,450,'地球',16)
 txt(44,321,'平均直径（体积等效）',17)
 txt(44,265,f"{d['diam']:,}",53,BLUE,'NUM');txt(310,271,'公里',19)
 note(44,237,['地球平均直径约12,742公里；图中照片不能用来量比例。'])
 rule(44,216)
 txt(44,175,d['vol'],37,BLUE,'NUM');txt(44,145,'倍地球体积',17)
 txt(320,175,d['mass'],37,BLUE,'NUM');txt(320,145,'倍地球质量',17)
 note(44,116,['把地球的体积、质量分别算作1；数值均为约数。'])
 pair(44,5,6,('听数字',name+'的平均直径约'+str(d['diam'])+'公里。体积约是地球的'+d['vol']+'倍，质量约是地球的'+d['mass']+'倍。照片分别缩放，不能按图片测量大小。'),('比一比','体积说的是占多大空间，质量说的是物质有多少。'+('地球在这本书里是比较的基准，体积和质量都算作一。' if name=='地球' else '看一看两个倍数，比较的项目不一样，数字也可能不同。')))
 x=half+44;title(x,'自己转，绕太阳转','自转和公转，是两种不同的运动。')
 txt(x,683,'自转一圈',21);txt(x,624,d['rotation'],53,BLUE,'NUM');off=pdfmetrics.stringWidth(d['rotation'],'NUM',53)+20;txt(x+off,630,d['rotunit'],19)
 para(x,588,d['rotlines'],16,26);rule(x,526)
 txt(x,486,'公转一圈',21);txt(x,429,d['orbit'],53,BLUE,'NUM');off=pdfmetrics.stringWidth(d['orbit'],'NUM',53)+20;txt(x+off,435,d['orbunit'],19)
 note(x,397,d['rotfoot']);rule(x,344)
 txt(x,306,'速度加油站',20);txt(x,271,'平均公转速度',17);txt(x+210,270,d['speed'],30,BLUE,'NUM');txt(x+310,274,'公里/秒',15)
 v=math.pi*d['eqdiam']/d['roth'];vs=(f'{v:,.0f}' if v>=100 else f'{v:.1f}')
 txt(x,230,'赤道随自转移动，估算每小时约',16);txt(x,185,vs,37,BLUE,'NUM');txt(x+180,190,'公里',17)
 note(x,152,['这是赤道随自转移动的估算速度，不是风速。','小时、日和年均使用地球单位；大气行星周期为约值。'])
 pair(x,7,8,('听时间',name+'自转一圈约'+d['rotation']+d['rotunit']+'。公转一圈约'+d['orbit']+d['orbunit']+'。平均公转速度每秒约'+d['speed']+'公里。赤道随自转移动每小时约'+vs+'公里，这不是风速。'+''.join(d['rotfoot'])),('动一动','慢慢原地转一圈，模仿自转；请大人当太阳，慢慢绕着大人走，模仿公转。'))
 end(2)
 # 3 内部与密度
 start();title(44,'里面，藏着什么？','看见外面，研究看不见的内部。')
 photo(d['img'],68,413,CW-48,266);note(44,391,['照片只显示外部；以下结构来自观测和科学模型。'])
 para(44,335,d['structure'],21,36)
 note(44,164,[d['landing'],'内部并非整齐的同心球壳，许多细节仍在研究。'])
 pair(44,9,10,('听身体秘密',''.join(d['structure'])+'科学家借助观测、实验和模型研究内部，不是直接拍到了内部照片。'),('能站上去吗',d['landing']))
 x=half+44;title(x,'一样大，谁更重？','先取一样大的体积，再比较质量。')
 photo(d['img'],x+65,450,CW-130,210)
 txt(x,417,name+'（整体平均）',16);txt(x+280,417,'水（约）',16)
 txt(x,362,d['density'],49,BLUE,'NUM');txt(x+280,362,'1',49,BLUE,'NUM')
 txt(x,331,'克/立方厘米',16);txt(x+280,331,'克/立方厘米',16)
 para(x,281,['密度说的是：','一样大的空间里，有多少质量。',name+'的平均密度，比水大。'],21,35)
 note(x,143,['比较的是整体平均密度，不是某一层的样品。','质量与体重不同；这些数值不是拿星球泡水测出来的。'])
 pair(x,11,12,('听密度',name+'的平均密度约每立方厘米'+d['density']+'克，水约每立方厘米一克。一样大的体积里，'+name+'按整体平均计算比水重。'),('猜轻重','星球大，就一定密度大吗？不一定。大小、总质量和密度是不同的比较项目。'))
 end(3)
 # 4 特色或卫星
 start();pan(44,d['features'][0],13,14);pan(half+44,d['features'][1],15,16);end(4)
 # 5 天气、日心距离
 start();pan(44,d['weather'],17,18)
 x=half+44;title(x,'离太阳有多远？','远近不同，绕太阳的路也不同。')
 txt(x,666,'平均距离约',20);txt(x,605,d['distance'],56,BLUE,'NUM');off=pdfmetrics.stringWidth(d['distance'],'NUM',56)+20;txt(x+off,611,d['distunit'],23)
 cx=x+245;cy=450;C.setStrokeColor(HexColor('#526793'));C.setLineWidth(1)
 # 只表示内外关系，不按实际偏心率、距离或天体大小绘图。
 if name=='地球':rs=[(185,105)]
 else:rs=[(85,49),(214,119)]
 for rx,ry in rs:C.ellipse(cx-rx,cy-ry,cx+rx,cy+ry,stroke=1,fill=0)
 photo('太阳',cx-35,cy-35,70,70);txt(cx-18,cy-61,'太阳',15)
 if name=='地球':
  photo('地球',cx+160,cy-20,40,40);txt(cx+160,cy+31,'地球',14)
 elif d['au']<1:
  photo(d['img'],cx+67,cy-18,36,36);txt(cx+65,cy+30,name,14)
  photo('地球',cx-234,cy-20,40,40);txt(cx-233,cy+31,'地球',14)
 else:
  photo('地球',cx+67,cy-17,34,34);txt(cx+67,cy+29,'地球',14)
  photo(d['img'],cx-242,cy-27,58,54);txt(cx-238,cy+35,name,14)
 note(x,303,['轨道形状、位置、天体大小与距离均为示意。','太阳：NASA/SDO/HMI观测，橙色为赋色。'])
 if name=='地球':ss=['地球到太阳的平均距离，','也常用作一把“太空尺子”。','这个长度单位，叫天文单位。']
 else:ss=['地球到太阳，平均约1.5亿公里。',name+'到太阳，平均约是它的'+f"{d['au']:.2f}"+'倍。','距离会变化，所以这里用平均值。']
 para(x,251,ss,20,34)
 note(x,125,['平均距离采用轨道半长轴的科普口径。'])
 pair(x,19,20,('听大距离',name+'到太阳的平均距离约'+d['distance']+d['distunit']+'。'+''.join(ss)),('找轨道','找找太阳和'+name+'。轨道线只是示意，天体的大小和距离没有按真实比例画。'))
 end(5)
 # 6 探索故事与复习
 start();title(44,'谁帮我们去认识'+name+'？','用望远镜、卫星和探测器找答案。')
 for y,(year,h,ss) in zip([650,503,356,209],d['timeline']):
  txt(44,y,year,36,BLUE,'NUM');txt(165,y+3,h,21,fit=CW-121);para(165,y-33,ss,18,29,w=CW-121)
 note(44,101,['时间线间距为排版示意；照片和任务年份不同。'])
 pair(44,21,22,('听探索故事',''.join(y+'年，'+h+'。'+''.join(ss) for y,h,ss in d['timeline'])),('排年份','从最早的年份开始，依次指一指。年份按先后排序，不代表图上的间距就是实际时间长度。'))
 x=half+44;title(x,name+'小侦探，出发！','先自己想一想，再点读听答案。')
 for j,(q,ans) in enumerate(d['quiz']):
  y=663-j*99;txt(x,y,str(j+1),28,BLUE,'NUM');para(x+36,y+2,[q],18,26,w=CW-36);txt(x+36,y-33,'在前面的图片和数字里找线索。',12,MUTED);rule(x,y-48)
 txt(x,127,'我的新问题：',19);rule(x+130,124,CW-130)
 pair(x,23,24,('听答案',''.join('第'+str(j+1)+'题，'+a for j,(q,a) in enumerate(d['quiz']))),('我的问题','现在轮到你提问题啦。你还想知道'+name+'的什么秘密？请爸爸妈妈帮你记下来。'))
 end(6)
 if 'extra' in d:
  start();pan(44,d['extra'][0],25,26);pan(half+44,d['extra'][1],27,28);end(7)
 C.save()
 with (out/'点读脚本与贴纸对应表.csv').open('w',encoding='utf-8-sig',newline='') as f:
  wr=csv.writer(f);wr.writerow(['章节','内容编号','标签','旁白','JOJO G3贴纸编号','小猴皮皮SE贴纸编号']);wr.writerows(rows)
 (out/'点读旁白.md').write_text('# '+name+' · 点读旁白\n\n内容编号不是厂商贴纸码；部分音频已生成，当前暂停；以全书校订语音稿为准。\n\n'+'\n\n'.join('## '+r[1]+' · '+r[2]+'\n\n'+r[3] for r in rows))
 return rows
ALL=[]
for d in P:ALL.extend(generate(d))
with (p/'全书点读对应表.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f);wr.writerow(['章节','内容编号','标签','旁白','JOJO G3贴纸编号','小猴皮皮SE贴纸编号']);wr.writerows(ALL)
(p/'资料'/'排版宽度记录.json').write_text(json.dumps(widthlog,ensure_ascii=False,indent=2))
print('七颗行星章节已生成，点读段数',len(ALL))
