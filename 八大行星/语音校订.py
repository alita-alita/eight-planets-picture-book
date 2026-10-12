# -*- coding: utf-8 -*-
import re,csv,json
D='零一二三四五六七八九'
def integer(n):
 n=int(n)
 if n==0:return '零'
 if n>=10000:
  q,r=divmod(n,10000);return integer(q)+'万'+(('零' if r<1000 else '')+integer(r) if r else '')
 result='';zero=False
 for base,unit in [(1000,'千'),(100,'百'),(10,'十'),(1,'')]:
  v,n=divmod(n,base)
  if v:
   if zero:result+='零';zero=False
   result+=('' if base==10 and v==1 and not result else D[v])+unit
  elif result and n:zero=True
 return result
def number(s):
 s=s.replace(',','');s=s.rstrip('0').rstrip('.') if '.' in s else s;parts=s.split('.');return integer(parts[0])+('点'+''.join(D[int(x)] for x in parts[1]) if len(parts)>1 else '')
def spoken(s):
 s=re.sub(r'(?<=\d)地球([日年])',r'个地球\1',s)
 s=s.replace('这里的数字是71%左右的表面积被水覆盖。','地球表面约有71%被水覆盖。')
 s=re.sub(r'(?<=\d),(?=\d{3})','',s)
 s=re.sub(r'(\d+(?:\.\d+)?)\s*%',lambda m:'百分之'+number(m[1]),s)
 s=re.sub(r'[−-](\d+(?:\.\d+)?)\s*℃',lambda m:'零下'+number(m[1])+'摄氏度',s)
 s=re.sub(r'(\d+(?:\.\d+)?)\s*℃',lambda m:number(m[1])+'摄氏度',s)
 s=re.sub(r'(?<!\d)(\d{4})年',lambda m:''.join(D[int(x)] for x in m[1])+'年',s)
 s=re.sub(r'\d+(?:\.\d+)?',lambda m:number(m[0]),s)
 s=s.replace('公里/小时','公里每小时').replace('克/立方厘米','克每立方厘米').replace('°','度').replace('E环','英文字母E所标记的环')
 return s

def export_reviewed(p,rows):
 rows=[[r[0],r[1],r[2],spoken(r[3]),r[4],r[5]] for r in rows]
 header=['章节','内容编号','标签','旁白','JOJO G3贴纸编号','小猴皮皮SE贴纸编号']
 with (p/'全书点读对应表.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(header);w.writerows(rows)
 text='# 八大行星 · 全书点读语音稿（校订版）\n\n按新书序排列。内容编号保持不变；数字已改为口语读法。音频生成暂停，现有音频需按修改清单复核后再续制。\n'
 chapter=None
 for r in rows:
  if r[0]!=chapter:chapter=r[0];text+='\n# '+chapter+'\n'
  text+='\n## '+r[1]+' · '+r[2]+'\n\n'+r[3]+'\n'
 (p/'全书点读语音稿.md').write_text(text)
 old={}
 from pathlib import Path
 previous=Path('/tmp/planet_audio_before.csv')
 if previous.exists():
  with previous.open(encoding='utf-8-sig') as f:old={r['内容编号']:r['旁白'] for r in csv.DictReader(f)}
 changes=[]
 for r in rows:
  if old.get(r[1])!=r[3]:
   files=list((p/'点读音频_天才童声2.0').glob('*/'+r[1]+'_*.mp3'))
   changes.append([r[1],r[0],'已有音频，续制前复核' if files else '尚待生成',old.get(r[1],''),r[3]])
 with (p/'语音稿修改与音频复核清单.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.writer(f);w.writerow(['内容编号','章节','音频状态','原稿','校订稿']);w.writerows(changes)
 # 分章稿也同步到同一版本。
 for chapter in {r[0] for r in rows}:
  out=p/'章节'/chapter
  if out.exists():
   rr=[r for r in rows if r[0]==chapter]
   (out/'点读旁白.md').write_text('# '+chapter+' · 校订点读旁白\n\n'+'\n\n'.join('## '+r[1]+' · '+r[2]+'\n\n'+r[3] for r in rr))
   with (out/'点读脚本与贴纸对应表.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(header);w.writerows(rr)
