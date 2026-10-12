# -*- coding: utf-8 -*-
import subprocess,re,json,uuid,urllib.request,urllib.error,base64
from pathlib import Path
root=Path('/Users/yangdl/Documents/YDL/儿童科普书')
s=subprocess.check_output(['textutil','-convert','txt','-stdout',str(root/'api.rtf')]).decode()
keys=re.findall(r'[A-Za-z0-9_\-+.=/]{25,}',s)
if len(keys)!=1:
 print(json.dumps({'status':'密钥字段需确认','count':len(keys)},ensure_ascii=False));raise SystemExit
key=keys[0]
source=(root/'土星样章/点读旁白.md').read_text()
blocks=re.findall(r'## (S\d+) · ([^\n]+)\n\s*([^#]+)',source)
selected={'S01','S06','S07','S08'}
for code,title,script in blocks:
 if code not in selected:continue
 script=script.strip()
 body={'user':{'uid':'planet_book'},'req_params':{'text':script,'speaker':'zh_male_tiancaitongsheng_uranus_bigtts','audio_params':{'format':'mp3','speech_rate':-10}}}
 req=urllib.request.Request('https://openspeech.bytedance.com/api/v3/tts/unidirectional',data=json.dumps(body).encode(),headers={'Content-Type':'application/json','X-Api-Key':key,'X-Api-Resource-Id':'seed-tts-2.0','X-Api-Request-Id':str(uuid.uuid4())})
 try:
  chunks=[]
  with urllib.request.urlopen(req,timeout=45) as r:
   for line in r:
    line=line.strip()
    if not line:continue
    if line.startswith(b'data:'):line=line[5:]
    try:d=json.loads(line)
    except ValueError:continue
    if d.get('code',0) not in [0,20000000]:
     print(json.dumps({'status':'接口拒绝','code':d.get('code'),'message':str(d.get('message','')).replace(key,'[隐藏]')[:400]},ensure_ascii=False));raise SystemExit
    if d.get('data'):chunks.append(base64.b64decode(d['data']))
  if not chunks:print('无音频返回');raise SystemExit
  p=root/'八大行星/音频试听/天才童声2.0';p.mkdir(exist_ok=True);f=p/(code+'_'+title+'.mp3');f.write_bytes(b''.join(chunks))
  (p/(code+'_'+title+'.txt')).write_text(script)
  print(json.dumps({'status':'success','path':str(f),'bytes':f.stat().st_size},ensure_ascii=False),flush=True)
 except urllib.error.HTTPError as e:
  print(json.dumps({'status':'HTTP错误','http':e.code,'message':e.read().decode(errors='replace').replace(key,'[隐藏]')[:600]},ensure_ascii=False));raise SystemExit
 except Exception as e:print(type(e).__name__);raise SystemExit
