# -*- coding: utf-8 -*-
import urllib.request,urllib.parse,json,concurrent.futures,time
from pathlib import Path
p=Path(__file__).resolve().parent.parent
queries={'水星盆地':'Mercury Caloris basin','水星陡崖':'Mercury scarps','金星可见光':'Venus Mariner 10 visible','金星火山':'Venus Sapas Mons','月球':'Moon full disk LRO','地球极光':'Earth aurora ISS','火星':'PIA00407','奥林帕斯山':'Olympus Mons Viking','水手峡谷':'Valles Marineris mosaic','火卫一':'PIA10368','火卫二':'PIA11826','木卫一':'PIA02308','木卫二':'PIA00502','木卫三':'PIA00716','木卫四':'PIA03456','天王星环':'Uranus rings Webb 2023','海卫一':'PIA00317','海王星环':'Neptune rings Webb 2022'}
def f(kv):
 k,q=kv; fn=p/'资料'/(k+'.json')
 for _ in range(2):
  try:
   if fn.exists():d=json.loads(fn.read_text())
   else:
    d=json.load(urllib.request.urlopen('https://images-api.nasa.gov/search?q='+urllib.parse.quote(q)+'&media_type=image',timeout=20));fn.write_text(json.dumps(d,ensure_ascii=False))
   a=d['collection']['items'];return k,[(x['data'][0]['nasa_id'],x['data'][0]['title'],x['data'][0].get('description','')[:500]) for x in a[:4]]
  except Exception as e:err=str(e)
 return k,err
for r in concurrent.futures.ThreadPoolExecutor(8).map(f,queries.items()):print(r,flush=True)
