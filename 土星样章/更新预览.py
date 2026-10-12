# -*- coding: utf-8 -*-
from pathlib import Path
import fitz,random
from PIL import Image
p=Path(__file__).parent;f=p/'土星样章_A3真实照片版.pdf';d=fitz.open(f)
for i,page in enumerate(d):
 random.seed(92+i)
 for n in range(42):
  x=random.uniform(25,1165);y=random.uniform(8,28);r=random.choice([.5,.7,1.1]);col=random.choice([(.48,.87,1),(.73,.69,1),(1,.82,.42)]);page.draw_circle(fitz.Point(x,y),r,color=None,fill=col)
 for b in page.get_text('blocks'):
  if b[6]==0:assert b[0]>=0 and b[1]>=0 and b[2]<=page.rect.width and b[3]<=page.rect.height,(i,b)
 page.get_pixmap(matrix=fitz.Matrix(1.2,1.2)).save(p/f'A3预览-{i+1}.png')
 assert abs(page.rect.width-1190.551)<.01 and abs(page.rect.height-841.89)<.01
assert len(d)==6
d.save(p/'temp.pdf');d.close();(p/'temp.pdf').replace(f)
out=Image.new('RGB',(1428,1515),'#070c20')
for i in range(6):
 im=Image.open(p/f'A3预览-{i+1}.png');im.thumbnail((714,505));out.paste(im,((i%2)*714,(i//2)*505))
out.save(p/'全章缩略预览.jpg')
f=p/'土星样章.html';s=f.read_text().replace('background:#e3e8ed','background:#070C20').replace('color:#172f40','color:#EDF4FF')
# 清除多轮更新残留的重复说明，并集中到一处。
a=s.index('<aside>');b=s.index('</aside>')+8
s=s[:a]+'''<aside>6个A3横向跨页，对折单页A4。点读位S01—S24为内容编号，尚未绑定实际贴纸或音频。<br>图片使用NASA观测影像及注明的科学模型；地球Blue Marble为观测数据合成。图片分别缩放，不可按图测量大小比例。版面采用背景融合，显示颜色会受底色影响。<br>原始影像：<a href="https://science.nasa.gov/photojournal/jewel-of-the-solar-system/">土星</a> / <a href="https://science.nasa.gov/resource/blue-marble-2002/">地球</a> / <a href="https://science.nasa.gov/resource/saturn-interior-cutaway-illustration/">内部模型</a> / <a href="https://science.nasa.gov/photojournal/titan-in-natural-color/">土卫六</a> / <a href="https://science.nasa.gov/saturn/moons/enceladus/">土卫二</a> / <a href="https://science.nasa.gov/resource/saturns-streaming-hexagon-storm/">六边形假彩色影像</a>。<br>数据来源：<a href="https://nssdc.gsfc.nasa.gov/planetary/factsheet/saturnfact.html">NASA数值表</a>；口径和审校记录见配套说明。土卫六原始影像分辨率较低，放大后较柔软，不能把插值放大视为新增细节。<br>本文件是阅读样张，尚未做整本装订拼版、出血和实物印刷打样。</aside>'''+s[b:]
f.write_text(s)
print('6张A3尺寸、文字边界与预览同步检查通过。')
