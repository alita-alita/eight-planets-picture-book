from pathlib import Path
import math,csv
p=Path(__file__).parent
base=(p/'重制A3.py').read_text().split('footer(2);c.save()')[0]
# 主题：深空蓝、星云紫、冰蓝与星光金。
base=base.replace("ink='#172F40'; blue='#186AAD'; yellow='#F9CC52'", "ink='#EDF4FF'; blue='#7BDFFF'; yellow='#FFD16B'")
base=base.replace("'#FFFFFF'", "'#0B1430'").replace("'#EAF4FA'", "'#191737'")
base=base.replace("'#536875'", "'#B3C4E2'").replace("'#BDD0DC'", "'#46567B'")
# 明确恢复深色底上的白色正文。
base=base.replace("53,'#0B1430'", "53,'#EDF4FF'").replace("21,'#0B1430'", "21,'#EDF4FF'")
base=base.replace("'#0B1430' if dark else ink", "'#EDF4FF' if dark else ink")
# 用真实天体影像替代大小比较中的纯色圆；照片展示不宣称同比例。
a=base.index("c.setFillColor(HexColor('#D7AF69'));c.circle(240,500")
b=base.index("text(44,300",a)
base=base[:a]+"""c.drawImage(str(p/'土星真实照片.jpg'),44,365,width=370,height=277.5)
c.drawImage(str(p/'地球真实影像.jpg'),446,460,width=54,height=54)
text(185,345,'土星',20);text(448,435,'地球',17)
"""+base[b:]
base=base.replace('两圆直径按约9.14∶1绘制。','照片非同比例；平均直径比约9.14。')
base=base.replace('图中土星不含光环。','直径数据不含光环。')
# 科学与图文一致性审校。
base=base.replace('把地球当作一把小尺子。','比较平均直径，先不算光环。')
base=base.replace('地球约12,742公里；照片非同比例；平均直径比约9.14。','照片分别缩放；大小请比较数字。平均直径比约9.14。')
base=base.replace("text(44,300,'平均直径',17)", "text(44,300,'平均直径（体积等效）',17)")
base=base.replace("rule(44,199,half-88)","text(44,204,'地球平均直径约12,742公里。地球影像为NASA观测数据合成。',10,'#B3C4E2')\nrule(44,192,half-88)")
base=base.replace('地球约23.9小时。土星转一圈用时更短！','地球约23.9小时；日常说的一天约24小时。')
base=base.replace('真实影像局部 · 光环上有明暗不同的环带','观测影像局部 · 有明暗不同的环带；版面做背景融合')
base=base.replace('Cassini自然色合成影像 / NASA/JPL-Caltech/SSI/Cornell','原图：Cassini自然色合成；版面背景融合 / NASA/JPL-Caltech/SSI/Cornell')
base=base.replace("'S04','比一比'", "'S04','找环带'")
# 在PDF排版层采用滤色混合，让照片黑底融入页面；不修改源照片。
base=base.replace("ink='#EDF4FF'", """original_draw_image=c.drawImage
def blended_image(*args, **kwargs):
 c.saveState()
 c.setBlendMode('Screen')
 result=original_draw_image(*args, **kwargs)
 c.restoreState()
 return result
c.drawImage=blended_image
ink='#EDF4FF'""")
exec(base)
footer(2);c.showPage()
def start(left='#0B1430',right='#191737'):
 box(0,0,half,H,left);box(half,0,half,H,right)
def title(x,t,sub):
 text(x,H-68,t,34);text(x,H-108,sub,18)
def para(x,y,ss):lines(x,y,ss,21,ink,34)
def note(x,y,ss):lines(x,y,ss,12,'#B3C4E2',20)
def end(n):footer(n);c.showPage()
def photo(name,x,y,w,h):
 im=Image.open(p/name);iw,ih=im.size;scale=min(w/iw,h/ih)
 c.drawImage(str(p/name),x+(w-iw*scale)/2,y+(h-ih*scale)/2,iw*scale,ih*scale)
def points(cx,cy,r,n=6):return [(cx+r*math.cos(math.pi/6+i*math.tau/n),cy+r*math.sin(math.pi/6+i*math.tau/n)) for i in range(n)]
# 3：结构和密度。区分模型示意与照片。
start();title(44,'可以站在土星上吗？','穿过云层，往里面看看。')
photo('土星科学剖面.jpg',44,339,half-88,343)
note(44,315,['NASA/JPL-Caltech简化模型（2017），非实拍；层次不按比例。'])
para(44,267,['外面：厚厚的大气和云。','深处：压力越来越大，','氢会呈现液态等不同状态。','更深处：还有重元素丰富的核心区域。'])
note(44,112,['弯曲线条表示磁场，不是星球上的实体线。','内部怎样分层，科学家仍在不断研究。'])
spot(62,66,'S09','听身体的秘密');spot(326,66,'S10','能着陆吗')
x=half+44;title(x,'又大又重，也能“轻”？','试试区分：总质量和平均密度。')
text(x,665,'质量大，不等于密度大。',23)
photo('土星真实照片.jpg',x,425,half-88,200)

text(x,405,'土星（整体平均）',15);text(x+245,405,'水',15)
text(x,366,'0.69',47,blue,'NUM');text(x+245,366,'1',47,blue,'NUM')
text(x,334,'每立方厘米约0.69克',15);text(x+245,334,'每立方厘米约1克',15)
para(x,284,['取一样大的空间来比较，','土星的平均密度比水小。','但整颗土星仍比地球重得多！'])
note(x,151,['比较的是一样大的体积，不是整颗星球和一杯水。','常说土星“能浮在水上”，只是密度类比：','现实中没有能容纳土星的水池，星球也不是小球。'])
spot(x+18,66,'S11','听密度');spot(x+280,66,'S12','猜轻重');end(3)
# 4：两颗卫星
start('#0B1430','#101C38');title(44,'橙色的伙伴：土卫六','它还有一个名字，叫泰坦。');x=half+44;title(x,'冰壳下的海：土卫二','它还有一个名字，叫恩克拉多斯。')
photo('土卫六.jpg',56,372,half-112,320);photo('土卫二.jpg',x,372,half-88,320)
note(44,350,['原图：自然色合成；版面背景融合 / NASA/JPL/Space Science Institute'])
note(x,350,['观测影像；版面背景融合 / NASA/JPL-Caltech/Space Science Institute'])
para(44,311,['厚厚的雾霾，把它裹成橙色。','它有湖泊、河流，也会下雨，','但那里的雨主要是液态甲烷，','和地球上的水雨很不一样。'])
text(44,145,'5,150',37,blue,'NUM');text(170,150,'公里左右的直径',17)
note(44,118,['它是土星最大的卫星，比水星还宽一些。'])
para(x,311,['外面是冰，下面藏着海洋。','南极附近的裂缝会喷出','水蒸气和冰粒，像太空喷泉。','这些喷出物还会补充土星的E环！'])
text(x,145,'504',37,blue,'NUM');text(x+90,150,'公里左右的直径',17)
note(x,118,['两张照片各自放大展示，没有按同一比例。'])
spot(62,66,'S13','听泰坦');spot(326,66,'S14','雨一样吗');spot(x+18,66,'S15','听冰下海洋');spot(x+280,66,'S16','比直径');end(4)
# 5：天气+位置
start();title(44,'风也会画六边形？','到土星北极，看看云中的大图案。')
photo('六边形.jpg',60,338,half-120,350)
note(44,313,['真实观测影像 / 假彩色处理，用颜色突出大气结构。','图中颜色不是人眼在现场看到的自然颜色。'])
para(44,252,['一股高速气流，围出六边形。','这不是石头砌成的墙，','而是会流动的大气结构。'])
text(44,111,'沿着照片里的六边形，数一数它的边。',18)
spot(62,66,'S17','听风的故事');spot(326,66,'S18','数六条边')
x=half+44;title(x,'离太阳有多远？','土星在更外面，绕太阳的路也更长。')
text(x,666,'平均距离约',20);text(x,600,'14.3',58,blue,'NUM');text(x+150,606,'亿公里',23)
# route diagram right half only, scale expressly schematic
cy=452;cx=x+240
c.setStrokeColor(HexColor('#526793'));c.setLineWidth(1)
for rx,ry in [(80,44),(213,116)]:c.ellipse(cx-rx,cy-ry,cx+rx,cy+ry,stroke=1,fill=0)
c.drawImage(str(p/'太阳SDO观测.jpg'),cx-36,cy-36,width=72,height=72)
text(cx-20,cy-61,'太阳',16)
c.drawImage(str(p/'地球真实影像.jpg'),cx+66,cy-14,width=28,height=28)
c.drawImage(str(p/'土星真实照片.jpg'),cx-250,cy-28,width=74,height=55.5)
text(cx+60,cy+25,'地球',14);text(cx-235,cy+35,'土星',14)
note(x,310,['轨道形状、位置和大小均为示意，只画地球与土星。','太阳：NASA/SDO/HMI观测影像，橙色为赋色。'])
para(x,262,['地球到太阳，平均约1.5亿公里。','土星到太阳，平均约是它的9.6倍。','距离会变化，所以这里用平均值。'])
note(x,140,['北极六边形影像 / PIA17652','NASA/JPL-Caltech/Space Science Institute'])
spot(x+18,66,'S19','听大距离');spot(x+280,66,'S20','找轨道');end(5)
# 6：探测故事+quiz
start('#0B1430','#191737');title(44,'谁帮我们去看土星？','不载人的探测器，带着仪器去旅行。')
# meaningful ordered timeline
for y,year,head,ss in [(653,'1997','从地球出发',['卡西尼带着惠更斯探测器，','开始长途旅行。']),(505,'2004','到达土星',['飞了接近7年，','终于进入绕土星的轨道。']),(357,'2005','降落土卫六',['惠更斯撑开降落伞，','到达土卫六的表面。']),(209,'2017','任务完成',['卡西尼进入土星大气，','把最后的观测数据传回地球。'])]:
 text(44,y,year,36,blue,'NUM');text(165,y+3,head,23);lines(165,y-33,ss,18,ink,29)
note(44,99,['时间线间距为排版示意；卡西尼没有载着宇航员。'])
spot(62,57,'S21','听旅行故事');spot(326,57,'S22','排年份')
x=half+44;title(x,'土星小侦探，出发！','先自己想一想，再点读听答案。')
qs=[('光环是一个结实的大圆盘吗？','看第1跨页的真实照片。'),('土星的体积和质量，都是95倍吗？','看第2跨页：比较的是什么？'),('可以像登月一样站在土星上吗？','看第3跨页：它有固体地面吗？'),('土卫六下的雨，和地球一样吗？','看第4跨页：雨滴是什么？'),('土星北极的图案有几条边？','用手指沿着图案走一圈。')]
for j,(q,hint) in enumerate(qs):
 y=663-j*99;text(x,y,str(j+1),28,blue,'NUM');text(x+37,y+2,q,18);text(x+37,y-28,hint,13,'#B3C4E2');rule(x,y-48,half-88)
text(x,127,'我的新问题：',19);rule(x+130,124,half-218)
spot(x+18,66,'S23','听答案');spot(x+280,66,'S24','我的问题');footer(6);c.save()
# preview and parent sources booklet in Markdown
sources=[('太阳SDO/HMI影像','https://sdo.gsfc.nasa.gov/assets/img/browse/2026/08/30/20260830_000000_4096_HMIIC.jpg'),('太阳观测通道说明','https://sdo.gsfc.nasa.gov/data/channels.php'),('土星事实与内部结构','https://science.nasa.gov/saturn/facts/'),('土星数值表','https://nssdc.gsfc.nasa.gov/planetary/factsheet/saturnfact.html'),('光环与成分','https://science.nasa.gov/mission/cassini/science/rings/'),('土卫六事实','https://science.nasa.gov/saturn/moons/titan/facts/'),('土卫六直径','https://science.nasa.gov/asset/webb/titan-cassini/'),('土卫二事实与影像','https://science.nasa.gov/saturn/moons/enceladus/'),('土卫二直径','https://science.nasa.gov/wp-content/uploads/2023/09/20070424_CHARM_Spencer.pdf'),('北极六边形观测','https://science.nasa.gov/resource/saturns-streaming-hexagon-storm/'),('任务时间线','https://science.nasa.gov/mission/cassini/the-journey/timeline/'),('内部模型（2017）','https://science.nasa.gov/resource/saturn-interior-cutaway-illustration/'),('地球数据合成影像','https://science.nasa.gov/resource/blue-marble-2002/'),('土星主图','https://science.nasa.gov/photojournal/jewel-of-the-solar-system/'),('土卫六照片','https://science.nasa.gov/photojournal/titan-in-natural-color/')]
(p/'家长说明与来源.md').write_text('# 土星扩充样章\n\n6张A3横向跨页，12个阅读页。每张420×297毫米，对折单页A4。不是装订拼版；不含印刷出血。点读编号为内容编号，并非厂商码；无录音文件。\n\n平均直径由体积等效平均半径计算；体积比约764，质量比约95。质量不同于体重。地球自转23.9小时采用恒星周期。土星自转约10.7小时采用NASA公众科普口径，不同测量定义会有差异。赤道线速度由赤道周长÷该周期估算，不是风速。轨道速度为平均值。密度比较使用土星整体平均值，不是某一层的样品。体积比较不表示实际球体装填数量。\n\n地球为NASA Blue Marble观测数据合成，非单次快照。大小比较照片分别缩放，不可据图测量比例。结构图是2017年简化模型示意，无真实厚度与清晰层界含义；土星核心可与上层混合。科学家仍在研究。平均日心距离采用轨道半长轴的科普口径。轨道图非比例，椭圆表现不用于判断真实偏心率。源主图为自然色合成，版面滤色混合会使颜色受底色影响，不能视为原始自然色或用于颜色测量。六边形图为假彩色观测数据；卫星照片分别缩放。\n\n资料核对日期：2026年10月10日。\n\n'+ '\n'.join(f'- [{a}]({b})' for a,b in sources))
# append and update point-reading scripts
with (p/'点读脚本与贴纸对应表.csv').open(encoding='utf-8-sig') as f:old=list(csv.reader(f))
extra=[('S09','内部结构','土星主要由氢和氦组成。外面是大气和云，越往里压力越大，氢会呈现液态等不同状态，更深处还有重元素丰富的核心区域。这张图是科学模型的简化示意，不是真实照片，各层也不一定有清楚的分界。'),('S10','能着陆吗','可以像登月一样站在土星的固体地面上吗？不可以。土星没有像地球那样的固体表面。我们看到的是外面的云层。它也不是一个空心气球！'),('S11','平均密度','一样大的空间里，装的质量越多，密度就越大。土星的平均密度约每立方厘米零点六九克，水约每立方厘米一克。所以土星的平均密度比水小。但整颗土星很大，总质量仍约是地球的九十五倍。'),('S12','猜轻重','取一样大的空间比较，土星物质按整体平均密度算，和水相比哪个更轻？答案是土星物质。但现实中没有容得下土星的水池，不能真的把土星当作小球放进水里。'),('S13','泰坦','土卫六又叫泰坦，是土星最大的卫星。它的直径约五千一百五十公里，比水星还宽一些。厚厚的大气和雾霾让它看起来橙橙的。那里有湖泊和河流，液体主要是甲烷和乙烷。'),('S14','雨一样吗','土卫六的雨主要是液态甲烷，地球的雨是液态水。名字都叫雨，液体却不相同。照片里橙色的主要是大气中的雾霾，并不是整片橙色的海洋。'),('S15','冰下海洋','土卫二又叫恩克拉多斯，直径约五百零四公里。外面有冰壳，下面有海洋。南极附近裂缝喷出水蒸气和冰粒。这些喷出物还给土星的E环补充材料。'),('S16','卫星比大小','土卫六直径约五千一百五十公里，土卫二约五百零四公里。谁更宽？答案是土卫六，它的直径大约是土卫二的十倍。书里照片分别放大，不能直接比照片的大小。'),('S17','六边形气流','土星北极有六边形的大气结构，是高速气流形成的形状，不是六面石墙。图片经过假彩色处理，方便科学家观察大气结构，颜色不代表人眼现场看到的样子。'),('S18','数边','用手指沿着照片里的六边形走一圈。一、二、三、四、五、六！有六条边。真实云中的边缘没有尺子画得那么笔直。'),('S19','大距离','土星到太阳的平均距离约十四点三亿公里，地球约一点五亿公里。土星到太阳的平均距离约是地球到太阳的九点六倍。轨道上的位置一直变化，所以这里说平均距离。'),('S20','找轨道','找一找图里的太阳、地球和土星。哪一条轨道更外面？土星的轨道！这张图只画两颗行星，不代表其他行星不存在，大小和距离也没有按真实比例画。'),('S21','探测器旅行','一九九七年，卡西尼带着惠更斯出发。二零零四年，经过接近七年的旅行，到达土星。二零零五年，惠更斯降落土卫六。二零一七年，卡西尼进入土星大气，结束任务。这是一趟没有宇航员乘坐的探测旅行。'),('S22','排年份','看看四个年份：一九九七、二零零四、二零零五、二零一七。请按从早到晚的顺序指一指。哪一年惠更斯降落土卫六？答案是二零零五年。'),('S23','侦探答案','第一题，光环不是结实的大圆盘，而是许多碎片。第二题，体积约七百六十四倍，质量约九十五倍。第三题，土星没有像地球那样的固体地面。第四题，土卫六主要下液态甲烷雨。第五题，六边形有六条边！'),('S24','我的问题','现在轮到你提问题啦。你还想知道土星的什么秘密？告诉爸爸妈妈，请他们记在书上的横线上。科学家的发现，也常常从一个新问题开始。')]
rows=old[1:9]+[[a,b,s,'待填写','待填写'] for a,b,s in extra]
with (p/'点读脚本与贴纸对应表.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(old[0]);w.writerows(rows)
(p/'点读旁白.md').write_text('# 土星章节：24段点读旁白\n\n内容编号不是实际贴纸编号，尚未生成音频。\n\n'+'\n\n'.join(f'## {r[0]} · {r[1]}\n\n{r[2]}' for r in rows))
# HTML: retain current URL and existing PDF filename
html=(p/'土星样章.html').read_text()
a=html.index('<main>');b=html.index('</main>')+7
html=html[:a]+'<main>'+''.join(f'<img src="A3预览-{i}.png" alt="土星扩充章节第{i}跨页">' for i in range(1,7))+'</main>'+html[b:]
html=html.replace('A3 横向 / 420 × 297 mm','A3 横向 / 6个跨页 · 12个阅读页').replace('每张A3为一个跨页','扩充内容：结构与密度、卫星、天气与距离、探测任务和小侦探游戏。<br>每张A3为一个跨页').replace('贴纸位S01—S08','贴纸位S01—S24')
(p/'土星样章.html').write_text(html)
print('6个跨页及24段脚本已完成')
