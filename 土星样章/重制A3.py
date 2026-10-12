from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from PIL import Image
p=Path(__file__).parent
pdfmetrics.registerFont(TTFont('CN','/System/Library/Fonts/STHeiti Medium.ttc',subfontIndex=1))
pdfmetrics.registerFont(TTFont('NUM','/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf'))
W,H=landscape(A3); half=W/2
c=canvas.Canvas(str(p/'土星样章_A3真实照片版.pdf'),pagesize=(W,H))
c.setTitle('小小宇航员 | 土星 | A3真实照片样章')
ink='#172F40'; blue='#186AAD'; yellow='#F9CC52'
def box(x,y,w,h,color):
 c.setFillColor(HexColor(color));c.rect(x,y,w,h,stroke=0,fill=1)
def text(x,y,s,size=20,color=ink,font='CN'):
 c.setFillColor(HexColor(color));c.setFont(font,size);c.drawString(x,y,s)
def lines(x,y,ss,size=23,color=ink,lead=39):
 for j,s in enumerate(ss):text(x,y-j*lead,s,size,color)
def rule(x,y,w,color='#BDD0DC'):
 c.setStrokeColor(HexColor(color));c.setLineWidth(.7);c.line(x,y,x+w,y)
def spot(x,y,code,label,dark=False):
 c.setStrokeColor(HexColor(yellow if dark else blue));c.setLineWidth(1);c.circle(x,y,17,stroke=1,fill=0)
 text(x-11,y-3,code,9,yellow if dark else blue,'NUM');text(x+27,y-6,label,15,'#FFFFFF' if dark else ink)
def footer(n,dark=False):
 text(42,25,'小小宇航员 / 土星站',10,'#B8B8B8' if dark else '#536875');text(W-62,25,str(n),11,ink,'NUM')
# 第一张 A3：一个跨页，中央为折线，主体与文字均避开折线。
box(0,0,W,H,'#FFFFFF');box(0,0,half,H,'#000000')
text(43,H-62,'太阳系的第六颗行星',17,yellow)
text(40,H-146,'你好，土星！',53,'#FFFFFF')
text(44,H-180,'SATURN',16,'#AAAAAA','NUM')
c.drawImage(str(p/'土星真实照片.jpg'),18,205,width=half-36,height=(half-36)*.75)
lines(44,173,['这不是画出来的星球。','这是探测器拍到的真实土星！'],21,'#FFFFFF',34)
spot(62,72,'S01','听一听',True);spot(262,72,'S02','找光环',True)
x=half+44
text(x,H-77,'它的圈圈，',40);text(x,H-132,'藏着什么？',40)
box(x,H-170,58,7,yellow)
lines(x,H-222,['远远看，像一张大唱片。','其实，光环不是一整块。'],24)
# 使用真实影像的光环局部，保留摄影纹理，不生成冰块伪照片。
im=Image.open(p/'土星真实照片.jpg');im.crop((1100,100,2600,600)).save(p/'光环局部.jpg')
c.drawImage(str(p/'光环局部.jpg'),x,342,width=half-88,height=(half-88)/3)
text(x,324,'真实影像局部 · 光环上有明暗不同的环带',12,'#536875')
lines(x,269,['里面主要是冰粒，','还有岩石和尘埃。','许多碎片，一起绕土星转！'],23,ink,37)
spot(x+18,91,'S03','光环的秘密');spot(x+247,91,'S04','比一比')
text(x,53,'Cassini自然色合成影像 / NASA/JPL-Caltech/SSI/Cornell',8,'#536875')
footer(1,True);c.showPage()
# 第二张 A3：左边大小和质量，右边时间与速度。
box(0,0,W,H,'#FFFFFF');box(half,0,half,H,'#EAF4FA')
text(44,H-67,'土星，到底有多大？',34)
text(44,H-103,'把地球当作一把小尺子。',20)
# 两圆按体积等效平均直径9.14:1绘制。
c.setFillColor(HexColor('#D7AF69'));c.circle(240,500,125,fill=1,stroke=0)
c.setFillColor(HexColor(blue));c.circle(456,500,125/9.14,fill=1,stroke=0)
text(210,347,'土星',20);text(431,457,'地球',17)
text(44,300,'平均直径',17);text(44,247,'116,500',54,blue,'NUM');text(291,250,'公里',19)
text(44,221,'地球约12,742公里；两圆直径按约9.14∶1绘制。',12,'#536875')
rule(44,199,half-88)
text(44,163,'764',43,ink,'NUM');text(149,170,'倍体积',20)
text(320,163,'95',43,ink,'NUM');text(389,170,'倍质量',20)
text(44,132,'地球的体积算作1',13,'#536875');text(320,132,'地球的质量算作1',13,'#536875')
spot(62,73,'S05','听数字');spot(300,73,'S06','猜一猜')
x=half+44
text(x,H-67,'谁转得更快？',34)
text(x,H-115,'自己转一圈，叫自转。',22)
text(x,H-183,'10.7',55,blue,'NUM');text(x+147,H-178,'小时',20)
text(x+254,H-170,'土星',20)
text(x,H-218,'地球约23.9小时。土星转一圈用时更短！',16)
rule(x,H-243,half-88)
text(x,H-289,'绕太阳一圈，叫公转。',22)
text(x,H-355,'29.4',55,blue,'NUM');text(x+147,H-350,'年',20)
text(x,H-390,'地球绕太阳一圈，约要1年。',17)
rule(x,H-416,half-88)
text(x,H-458,'速度加油站',20)
text(x,H-496,'绕太阳跑，平均每秒约',17)
text(x+260,H-498,'9.7',29,blue,'NUM');text(x+312,H-496,'公里',17)
text(x,H-535,'赤道随自转移动，估算每小时约',17)
text(x,H-579,'35,000',38,blue,'NUM');text(x+150,H-575,'公里',17)
text(x,H-606,'这是随自转移动的估算速度，不是风速。',12,'#536875')
spot(x+18,73,'S07','听数字');spot(x+247,73,'S08','动一动')
text(x,43,'数值均为约数，年和小时使用地球单位；图中土星不含光环。',9,'#536875')
footer(2);c.save()
# 在原来打开的HTML路径呈现新稿，便于刷新。
(p/'土星样章.html').write_text('''<!doctype html><html lang="zh"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>土星样章 · A3真实照片版</title><style>body{margin:0;background:#e3e8ed;font-family:system-ui;color:#172f40}header{padding:24px 4%;display:flex;align-items:center;justify-content:space-between}a{color:inherit}main{max-width:1400px;margin:auto}img{display:block;width:100%;margin:0 0 30px}aside{padding:20px 4% 40px;font-size:14px;line-height:1.9}button{padding:10px 20px}@media print{header,aside{display:none}body{background:white}img{margin:0;break-after:page;width:420mm;height:297mm}@page{size:A3 landscape;margin:0}}</style><header><div><b>小小宇航员 · 土星</b>　A3 横向 / 420 × 297 mm</div><a href="土星样章_A3真实照片版.pdf">打开印刷PDF</a></header><main><img src="A3预览-1.png" alt="土星真实照片与光环知识跨页"><img src="A3预览-2.png" alt="土星数字比较跨页"></main><aside>每张A3为一个跨页，中间对折后单页A4。贴纸位S01—S08为内容编号，尚未绑定实际贴纸或音频。<br>真实影像：<a href="https://science.nasa.gov/photojournal/jewel-of-the-solar-system/">NASA Cassini / PIA17474</a>，由探测器三种滤色片的36张影像拼接为自然色图像。光环小图为原图局部裁切。<br>数据：<a href="https://nssdc.gsfc.nasa.gov/planetary/factsheet/saturnfact.html">NASA Saturn Fact Sheet</a>、<a href="https://science.nasa.gov/saturn/facts/">NASA Saturn Facts</a>。体积比由平均半径比的三次方计算。质量不同于体重；平均直径不等于赤道直径。土星自转约10.7小时采用NASA公众科普口径；赤道线速度由赤道周长÷该周期估算。<br>这是跨页阅读样张，尚未做整本书的装订拼版和出血设置。</aside></html>''')
print('A3 PDF与新预览页已完成')
