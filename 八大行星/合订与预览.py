# -*- coding: utf-8 -*-
from pathlib import Path
import fitz,csv,sys,json
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).resolve().parent
sys.path.insert(0,str(p));from 内容 import P
ordered=['水星','金星','地球','火星','木星','土星','天王星','海王星']
full=fitz.open();guide=fitz.open(p/'资料'/'导读与总结.pdf');full.insert_pdf(guide,from_page=0,to_page=2)
html=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>小小宇航员 · 八大行星</title><style>*{box-sizing:border-box}body{margin:0;background:#070e20;color:#edf4ff;font-family:system-ui,"Heiti SC",sans-serif}header{padding:32px 4%;max-width:1400px;margin:auto}h1{font-size:30px;margin:8px 0 18px}p{color:#b3c4e2;line-height:1.8}a{color:#7bdfff;text-decoration:none}nav{display:flex;gap:20px;flex-wrap:wrap;padding:18px 0}main{max-width:1400px;margin:auto}section{padding:24px 0}h2{padding:0 3%;font-size:24px}.spread{display:block;width:100%;height:auto;margin:0 0 24px;box-shadow:0 6px 24px #0006}footer{padding:25px 4%;line-height:1.9;color:#b3c4e2}.btn{display:inline-block;background:#7bdfff;color:#0b1430;padding:12px 20px;border-radius:7px;margin-right:18px}@media print{header,nav,h2,footer{display:none}.spread{margin:0;break-after:page;width:420mm;height:297mm}@page{size:A3 landscape;margin:0}}</style><header><p>小小宇航员 · 亲子共读</p><h1>八大行星，真实影像与数字之旅</h1><p>59个A3横向跨页 · 118个阅读页 · 222段点读文稿<br>保留土星定稿，其余章节沿用同一大纲；地球、火星、木星各增加一个跨页。</p><a class="btn" href="八大行星_A3合订稿.pdf">打开全书PDF</a><a href="全书点读对应表.csv">点读对应表</a><nav>'+''.join('<a href="#'+n+'">'+n+'</a>' for n in ordered)+'<a href="#全景图">八大行星环绕图</a></nav></header><main>']
for i in range(3):
 pg=guide[i];pg.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(str(p/('导读预览-'+str(i+1)+'.png')));html.append(('<a id="全景图"></a>' if i==2 else '')+'<img class="spread" src="导读预览-'+str(i+1)+'.png" alt="导读" loading="lazy">')
allrows=[];font=ImageFont.truetype('/System/Library/Fonts/STHeiti Medium.ttc',18,index=1)
low=fitz.open(p/'资料/低角度轨道立体图.pdf');full.insert_pdf(low)
low[0].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(str(p/'低角度轨道立体预览.png'))
html.append('<section id="低角度"><h2>低角度看轨道倾斜</h2><img class="spread" src="低角度轨道立体预览.png" alt="水星与地球轨道平面的低角度立体示意"></section>')
with (p/'资料/低角度点读对应表.csv').open(encoding='utf-8-sig') as f:allrows.extend(list(csv.reader(f))[1:])
orb=fitz.open(p/'资料/公转轨道倾角.pdf');full.insert_pdf(orb)
orb[0].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(str(p/'公转轨道倾角预览.png'))
html.append('<section id="轨道倾角"><h2>公转轨道倾角</h2><img class="spread" src="公转轨道倾角预览.png" alt="公转轨道倾角侧视比较"></section>')
with (p/'资料/轨道倾角点读对应表.csv').open(encoding='utf-8-sig') as f:allrows.extend(list(csv.reader(f))[1:])
tilt=fitz.open(p/'资料/自转轴倾角.pdf');full.insert_pdf(tilt)
html.append('<section id="倾角"><h2>八大行星自转轴倾角</h2>')
for i,pg in enumerate(tilt):
 target=p/('倾角预览-'+str(i+1)+'.png');pg.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(str(target));html.append('<img class="spread" src="'+target.name+'" alt="自转轴倾角" loading="lazy">')
html.append('</section>')
with (p/'资料/倾角点读对应表.csv').open(encoding='utf-8-sig') as f:allrows.extend(list(csv.reader(f))[1:])
for n in ordered:
 if n=='土星':
  chapter=p.parent/'土星样章'/'土星样章_A3真实照片版.pdf'
  out=p/'章节'/'土星';out.mkdir(exist_ok=True)
  with (p.parent/'土星样章'/'点读脚本与贴纸对应表.csv').open(encoding='utf-8-sig') as f:
   r=list(csv.reader(f));allrows.extend([[n]+x for x in r[1:]])
 else:
  out=p/'章节'/n;chapter=out/(n+'_A3.pdf')
  with (out/'点读脚本与贴纸对应表.csv').open(encoding='utf-8-sig') as f:allrows.extend(list(csv.reader(f))[1:])
 d=fitz.open(chapter);full.insert_pdf(d);html.append('<section id="'+n+'"><h2>'+n+'</h2>')
 sheets=[]
 for i,pg in enumerate(d):
  target=out/('预览-'+str(i+1)+'.png');pg.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(str(target));im=Image.open(target).convert('RGB');im.thumbnail((700,496));sheets.append(im)
  html.append('<img class="spread" src="章节/'+n+'/'+target.name+'" alt="'+n+'第'+str(i+1)+'跨页" loading="lazy">')
 html.append('</section>');contact=Image.new('RGB',(1400,((len(sheets)+1)//2)*520),'#050a15');draw=ImageDraw.Draw(contact)
 for i,im in enumerate(sheets):
  x=(i%2)*700;y=(i//2)*520;contact.paste(im,(x,y));draw.text((x+18,y+498),n+' · '+str(i+1),font=font,fill='#7bdfff')
 contact.save(out/'全章预览.jpg',quality=92)
full.insert_pdf(guide,from_page=3,to_page=3)
full.set_metadata(dict(title='小小宇航员 · 八大行星 · A3合订稿',author='亲子共读科普',subject='八大行星真实影像、数字比较与点读文稿'))
toc=[[1,'从地球出发',1],[1,'八大行星环绕太阳全景',3],[1,'低角度看轨道倾斜',4],[1,'公转轨道倾角侧视比较',5],[1,'八大行星自转轴倾角',6]];page=8
for n in ordered:
 toc.append([1,n,page]);page+=(7 if n in ['地球','火星','木星'] else 6)
toc.append([1,'数字大比拼与太空护照',page]);full.set_toc(toc)
full.save(p/'八大行星_A3合订稿.pdf',garbage=4,deflate=True)
full[-1].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(str(p/'总结预览.png'));html.append('<img class="spread" src="总结预览.png" alt="数字总表与太空护照" loading="lazy"></main><footer>图片类型与来源见《家长说明与图片来源》。黑色影像背景在排版层融合，源图保留。<br>内容编号不是点读码，部分音频已生成，当前暂停；请分别绑定JOJO G3与小猴皮皮SE的配套录音贴。<br>A3为420×297毫米的阅读跨页，中央对折后单页A4；尚未做装订拼版及出血。</footer></html>')
(p/'八大行星.html').write_text(''.join(html))
with (p/'全书点读对应表.csv').open('w',encoding='utf-8-sig',newline='') as f:
 wr=csv.writer(f);wr.writerow(['章节','内容编号','标签','旁白','JOJO G3贴纸编号','小猴皮皮SE贴纸编号']);wr.writerows(allrows)
from 语音校订 import export_reviewed
export_reviewed(p,allrows)
print('合订稿',len(full),'个A3跨页；',len(allrows),'段点读文稿')

# 输出时统一清理制作备注与重复提示。
import runpy
runpy.run_path(str(p/"资料/精简内页文案.py"))
