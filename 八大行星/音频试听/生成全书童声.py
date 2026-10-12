# -*- coding: utf-8 -*-
import subprocess,re,json,uuid,urllib.request,urllib.error,base64,csv,shutil,time
from pathlib import Path
root=Path('/Users/yangdl/Documents/YDL/儿童科普书');book=root/'八大行星';out=book/'点读音频_天才童声2.0';out.mkdir(exist_ok=True)
s=subprocess.check_output(['textutil','-convert','txt','-stdout',str(root/'api.rtf')]).decode();keys=re.findall(r'[A-Za-z0-9_\-+.=/]{25,}',s)
assert len(keys)==1,'密钥字段需确认'
key=keys[0]
with open(book/'全书点读对应表.csv',encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
manifest=[]
for i,row in enumerate(rows,1):
 code,title,script=row['内容编号'],row['标签'],row['旁白'];folder=out/row['章节'];folder.mkdir(exist_ok=True);mp3=folder/(code+'_'+title+'.mp3');wav=mp3.with_suffix('.wav')
 sample=book/'音频试听/天才童声2.0'/(code+'_'+title+'.mp3')
 sampletxt=sample.with_suffix('.txt')
 if not mp3.exists() and sample.exists() and sampletxt.exists() and sampletxt.read_text().strip()==script.strip():shutil.copy2(sample,mp3)
 if not mp3.exists():
  body={'user':{'uid':'planet_book'},'req_params':{'text':script,'speaker':'zh_male_tiancaitongsheng_uranus_bigtts','audio_params':{'format':'mp3','speech_rate':-10}}}
  req=urllib.request.Request('https://openspeech.bytedance.com/api/v3/tts/unidirectional',data=json.dumps(body).encode(),headers={'Content-Type':'application/json','X-Api-Key':key,'X-Api-Resource-Id':'seed-tts-2.0','X-Api-Request-Id':str(uuid.uuid4())})
  try:
   chunks=[]
   with urllib.request.urlopen(req,timeout=50) as r:
    for line in r:
     line=line.strip()
     if not line:continue
     if line.startswith(b'data:'):line=line[5:]
     try:d=json.loads(line)
     except ValueError:continue
     if d.get('code',0) not in [0,20000000]:raise RuntimeError(str(d.get('code'))+': '+str(d.get('message','')))
     if d.get('data'):chunks.append(base64.b64decode(d['data']))
   if not chunks:raise RuntimeError('未返回音频')
   mp3.write_bytes(b''.join(chunks))
  except Exception as e:
   msg=str(e).replace(key,'[隐藏]');print(json.dumps({'failed':code,'error':msg[:400]},ensure_ascii=False),flush=True);raise SystemExit(1)
 if not wav.exists():subprocess.run(['afconvert','-f','WAVE','-d','LEI16@24000','-c','1',str(mp3),str(wav)],check=True,capture_output=True)
 info=subprocess.check_output(['afinfo',str(mp3)]).decode();duration=float(re.search(r'estimated duration: ([\d.]+)',info).group(1));assert duration>0
 row.update({'MP3文件':str(mp3.relative_to(out)),'WAV文件':str(wav.relative_to(out)),'时长秒':round(duration,3),'音色':'天才童声2.0','语速参数':-10});manifest.append(row)
 if i%10==0 or i==len(rows):print(json.dumps({'completed':i,'total':len(rows)},ensure_ascii=False),flush=True)
with open(out/'音频与贴纸对应表.csv','w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(manifest[0]));w.writeheader();w.writerows(manifest)
(out/'使用说明.txt').write_text('八大行星点读音频：天才童声2.0，语速参数-10。\n每个点读编号对应独立音频，MP3及WAV内容相同。WAV为24kHz、16位、单声道。\n当前文件名是书中内容编号，不是录音贴编号，不能直接按现名导入。请先确认各笔要求的格式、目录和实际贴纸编号，再复制、重命名导入。\n两支笔均尚未实机测试；贴纸编号预留栏待填写。\n音频已检查可解码和时长，尚未逐段人工听审。\n',encoding='utf-8')
print(json.dumps({'done':len(manifest),'total_minutes':round(sum(x['时长秒'] for x in manifest)/60,1)},ensure_ascii=False),flush=True)
