from pathlib import Path
import subprocess,re,json,urllib.request,urllib.error,base64,uuid
p=Path(__file__).parent/'dist';names=['Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune','Sun'];facts=['Mercury is small.','Venus is hot.','Earth is our home.','Mars is red.','Jupiter is big.','Saturn has rings.','Uranus spins on its side.','Neptune is far away.','The Sun is a star.']
clips={}
for i,name in enumerate(names):
 clips[f'word-{i}']=name+'.';clips[f'sentence-{i}']=('This is the Sun.' if i==8 else f'This is {name}.');clips[f'fact-{i}']=facts[i]
 if i<8:clips[f'find-{i}']=f'Find {name}.'
clips.update({'yes':'Yes! Well done!','retry':'Try again.','start':'Start with Mercury.','done':'You did it! All eight planets!','next':'Which planet comes next?'})
(p/'english-audio/scripts.json').write_text(json.dumps(clips,indent=2))
s=subprocess.check_output(['textutil','-convert','txt','-stdout','/Users/yangdl/Documents/YDL/儿童科普书/api.rtf']).decode();keys=re.findall(r'[A-Za-z0-9_\-+.=/]{25,}',s);assert len(keys)==1;key=keys[0]
for code,script in clips.items():
 out=p/'english-audio'/f'{code}.mp3'
 if out.exists() and out.stat().st_size>100:continue
 body={'user':{'uid':'planet_english'},'req_params':{'text':script,'speaker':'ICL_uranus_en_female_charlie_tob','audio_params':{'format':'mp3','speech_rate':-12}}}
 req=urllib.request.Request('https://openspeech.bytedance.com/api/v3/tts/unidirectional',data=json.dumps(body).encode(),headers={'Content-Type':'application/json','X-Api-Key':key,'X-Api-Resource-Id':'seed-tts-2.0','X-Api-Request-Id':str(uuid.uuid4())})
 try:
  chunks=[]
  with urllib.request.urlopen(req,timeout=45) as r:
   for line in r:
    line=line.strip()
    if line.startswith(b'data:'):line=line[5:]
    if not line:continue
    data=json.loads(line)
    if data.get('code',0) not in [0,20000000]:raise RuntimeError(str(data.get('code'))+':'+str(data.get('message','')).replace(key,'[redacted]')[:150])
    if data.get('data'):chunks.append(base64.b64decode(data['data']))
  assert chunks;out.write_bytes(b''.join(chunks));print(code,'OK',flush=True)
 except Exception as e:print('STOP',type(e).__name__,str(e).replace(key,'[redacted]')[:150],flush=True);raise SystemExit(1)
print('40 clips completed')
