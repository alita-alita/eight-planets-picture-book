from pathlib import Path
import fitz,csv,json,shutil,sys
from PIL import Image
ROOT=Path('/Users/yangdl/Documents/YDL/儿童科普书/八大行星');OUT=Path(__file__).parent/'dist';(OUT/'pages').mkdir(exist_ok=True);(OUT/'audio').mkdir(exist_ok=True);(OUT/'planets').mkdir(exist_ok=True)
with (ROOT/'点读音频_天才童声2.0/音频与贴纸对应表.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
lookup={r['内容编号']:r for r in rows}
for code,r in lookup.items():shutil.copy2(ROOT/'点读音频_天才童声2.0'/r['MP3文件'],OUT/'audio'/f'{code}.mp3')
doc=fitz.open(ROOT/'八大行星_A3完整打印版_含封面.pdf');toc=doc.get_toc();pages=[];ids=[]
for i,pg in enumerate(doc):
 pix=pg.get_pixmap(matrix=fitz.Matrix(1.7,1.7));im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples);im.save(OUT/'pages'/f'{i+1:02d}.webp',quality=87)
 points=[]
 for w in pg.get_text('words'):
  code=w[4]
  if code not in lookup:continue
  r=lookup[code];points.append({'id':code,'label':r['标签'],'text':r['旁白'],'x':round((w[0]+w[2])/2/pg.rect.width,5),'y':round((w[1]+w[3])/2/pg.rect.height,5)});ids.append(code)
 chapter=next(t[1] for t in reversed(toc) if t[2]<=i+1)
 pages.append({'number':i+1,'chapter':chapter,'image':f'pages/{i+1:02d}.webp','points':points,'text':pg.get_text()})
assert len(ids)==222 and len(set(ids))==222
sys.path.insert(0,str(ROOT));from 内容 import P
names=['水星','金星','地球','火星','木星','土星','天王星','海王星'];chapters=[]
for name in names:
 obj=next((x for x in P if x['name']==name),None);src=ROOT/'图片'/((obj['img'] if obj else '土星')+'.jpg');im=Image.open(src);im=im.crop((0,0,1090,1096)) if name=='金星' else im;im.thumbnail((360,300));im.convert('RGB').save(OUT/'planets'/f'{name}.webp',quality=88)
 chapters.append({'name':name,'page':next(t[2] for t in toc if t[1]==name),'image':f'planets/{name}.webp','intro':(obj['intro'][0] if obj else '我的光环，藏着许多秘密。')})
shutil.copy2(ROOT/'家长说明与图片来源.md',OUT/'图片来源与家长说明.txt')
(OUT/'book.json').write_text(json.dumps({'pages':pages,'chapters':chapters,'toc':[{'title':t[1],'page':t[2]} for t in toc]},ensure_ascii=False))
print('60页、222个点读位置、222段MP3已准备')
