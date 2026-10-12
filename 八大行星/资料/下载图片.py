# -*- coding: utf-8 -*-
from pathlib import Path
import urllib.request,urllib.parse,json,concurrent.futures,re,shutil
p=Path(__file__).resolve().parent.parent
chosen={'PIA15160':('PIA15160',0),'PIA00343':('PIA00343',0),'PIA18182':('PIA18182',0),'PIA01492':('PIA01492',0),'PIA00271':('PIA00271',0),'PIA01544':('PIA01544',0),'PIA01490':('PIA01490',0),'PIA01384':('PIA01384',0),'水星盆地':('水星盆地',0),'水星陡崖':('水星陡崖',0),'金星可见光':('金星可见光',0),'金星火山':('金星火山',0),'地球极光':('地球极光',0),'奥林帕斯山':('奥林帕斯山',0),'水手峡谷':('水手峡谷',0),'火卫一':('火卫一',0),'火卫二':('火卫二',0),'木卫一':('木卫一',0),'木卫二':('PIA19048',0),'木卫三':('木卫三',0),'木卫四':('木卫四',0),'海卫一':('海卫一',0),'火星':('PIA00407',0),'月球':('PIA00405',0)}
def get(kv):
 k,(j,idx)=kv
 try:
  fn=p/'资料'/(j+'.json')
  if not fn.exists():
   d=json.load(urllib.request.urlopen('https://images-api.nasa.gov/search?q='+urllib.parse.quote(j)+'&media_type=image',timeout=25));fn.write_text(json.dumps(d,ensure_ascii=False))
  else:d=json.loads(fn.read_text())
  a=d['collection']['items'][idx];links=a.get('links',[]);url=next((l['href'] for l in links if l.get('rel')=='canonical' and l['href'].endswith(('.jpg','.png'))),None)
  if not url:
   v=json.load(urllib.request.urlopen(a['href'],timeout=20));url=next((u for u in v if u.endswith('~orig.jpg')),None) or next(l['href'] for l in links if l.get('render')=='image')
  target=p/'图片'/(k+'.jpg')
  if not target.exists():target.write_bytes(urllib.request.urlopen(url,timeout=35).read())
  return k,dict(url=url,id=a['data'][0]['nasa_id'],title=a['data'][0]['title'],description=a['data'][0].get('description',''),credit=a['data'][0].get('secondary_creator',a['data'][0].get('center','NASA')))
 except Exception as e:return k,dict(error=str(e))
res={}
for k,d in concurrent.futures.ThreadPoolExecutor(8).map(get,chosen.items()):res[k]=d;print(k,d.get('title',d),flush=True)
for name,src in [('地球','地球真实影像.jpg'),('太阳','太阳SDO观测.jpg'),('土星','土星真实照片.jpg')]:
 shutil.copyfile(p.parent/'土星样章'/src,p/'图片'/(name+'.jpg'));res[name]=dict(url='沿用土星定稿来源',title=name)
# 官方Webb原始发布图，不使用AI生成图。
for name,u in [('天王星环','https://esawebb.org/images/weic2310a/'),('海王星环','https://esawebb.org/images/weic2214c/')]:
 try:
  h=urllib.request.urlopen(u,timeout=25).read().decode();(p/'资料'/(name+'.html')).write_text(h)
  matches=re.findall(r'href="([^"]+\.jpg)"',h);url=next(x for x in matches if '/large/' in x)
  if url.startswith('/'):url='https://esawebb.org'+url
  (p/'图片'/(name+'.jpg')).write_bytes(urllib.request.urlopen(url,timeout=30).read());res[name]=dict(url=url,page=u,title=name,credit='NASA, ESA, CSA, STScI')
  print(name,url,flush=True)
 except Exception as e:res[name]=dict(error=str(e));print(name,e,flush=True)
(p/'图片来源.json').write_text(json.dumps(res,ensure_ascii=False,indent=2))
