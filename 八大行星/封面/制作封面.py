# -*- coding: utf-8 -*-
from pathlib import Path
import math,random
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.colors import HexColor,Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
p=Path(__file__).resolve().parent;assets=p.parent/'图片';W,H=landscape(A3)
pdfmetrics.registerFont(TTFont('CN','/System/Library/Fonts/STHeiti Medium.ttc',subfontIndex=1));pdfmetrics.registerFont(TTFont('NUM','/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf'))
c=canvas.Canvas(str(p/'八大行星_A3封面.pdf'),pagesize=(W,H));c.setTitle('八大行星 · 小小宇航员 · A3横向封面')
INK='#EDF4FF';BLUE='#7BDFFF';GOLD='#FFD16B';MUTED='#A9BEDF';NAVY='#08132D'
def text(x,y,s,size,col=INK,font='CN'):
 c.setFont(font,size);c.setFillColor(HexColor(col));c.drawString(x,y,s)
def rule(x,y,w,col=BLUE):c.setStrokeColor(HexColor(col));c.setLineWidth(.7);c.line(x,y,x+w,y)
c.setFillColor(HexColor(NAVY));c.rect(0,0,W,H,fill=1,stroke=0)
# 印刷友好的矢量辉光，星点与轨道为装饰，行星保持源影像。
for cx,cy,rmax,col,alpha in [(970,440,620,'#204594',.008),(820,650,300,'#423C99',.008),(860,210,320,'#177999',.006)]:
 c.saveState();c.setFillColor(HexColor(col));c.setFillAlpha(alpha)
 for r in range(rmax,20,-12):c.circle(cx,cy,r,fill=1,stroke=0)
 c.restoreState()
rng=random.Random(20261010)
for i in range(340):
 x=rng.uniform(52,W-32);y=rng.uniform(25,H-25)
 if x<545 and 210<y<720:continue
 rad=rng.choice([.25,.4,.6,.8,1.1]);c.saveState();c.setFillAlpha(rng.uniform(.2,.85));c.setFillColor(HexColor(rng.choice([BLUE,INK,MUTED,GOLD])));c.circle(x,y,rad,fill=1,stroke=0);c.restoreState()
for x,y in [(594,725),(1100,478),(720,146),(1135,755),(562,330)]:
 c.saveState();c.setStrokeColor(HexColor(BLUE));c.setLineWidth(.7);c.line(x-4,y,x+4,y);c.line(x,y-4,x,y+4);c.setFillColor(HexColor(INK));c.circle(x,y,1,fill=1,stroke=0);c.restoreState()
# 弧线引导目光穿过行星群；不作为科学轨道图。
for rx,ry,rot in [(350,190,36),(300,245,18)]:
 c.saveState();c.translate(857,429);c.rotate(rot);c.setStrokeColor(HexColor('#395982'));c.setLineWidth(.65);c.setStrokeAlpha(.65);c.ellipse(-rx,-ry,rx,ry,fill=0,stroke=1);c.restoreState()
def photo(key,cx,cy,w,h=None):
 h=h or w;im=Image.open(assets/(key+'.jpg'));iw,ih=im.size;vw=iw/2-45 if key=='金星可见光' else iw;r=min(w/vw,h/ih);xx=cx-vw*r/2;yy=cy-ih*r/2
 c.saveState()
 # 小范围深蓝底遮住经过星球的装饰线，不改动源照片。
 c.setFillColor(HexColor(NAVY))
 if key=='土星':c.ellipse(cx-w*.49,cy-h*.37,cx+w*.49,cy+h*.37,fill=1,stroke=0)
 else:c.circle(cx,cy,min(w,h)*.475,fill=1,stroke=0)
 c.setBlendMode('Screen')
 if vw!=iw:
  q=c.beginPath();q.rect(xx,yy,vw*r,ih*r);c.clipPath(q,fill=0,stroke=0)
 c.drawImage(str(assets/(key+'.jpg')),xx,yy,iw*r,ih*r);c.restoreState()
# 各星球独立缩放；八颗均出现，真实影像与装饰留白并重。
photo('PIA18182',738,716,64)
photo('PIA01492',1082,682,86)
photo('PIA15160',625,603,37)
photo('PIA00343',946,580,186)
photo('金星可见光',638,420,66)
photo('火星',645,229,88)
photo('地球',820,385,264)
photo('土星',1012,211,292,240)
# 左侧编辑式标题版面。
text(70,757,'小 小 宇 航 员',21,GOLD)
rule(70,732,65,GOLD)
text(64,631,'八大行星',96)
text(70,574,'给小小宇航员的太空科普书',25)
text(71,524,'从我们的地球出发，',19,MUTED)
text(71,491,'去认识太阳的八位行星伙伴。',19,MUTED)
# 底边保留装订与印刷安全距离。
text(70,76,'为好奇心，打开一片星空。',20,GOLD)
c.save();print('A3封面已生成')
