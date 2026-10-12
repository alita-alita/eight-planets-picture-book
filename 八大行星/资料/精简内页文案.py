from pathlib import Path
import fitz, shutil, json
p=Path(__file__).resolve().parents[1]
exact={
'A3横向跨页 / 简体中文 / 适合亲子共读',
'内容编号不是厂商点读码；部分音频已生成，现暂停；新增稿件待配音。',
'每张A3是阅读跨页，中央对折后单页A4。',
'看真实影像 · 听星球故事 · 玩数字游戏',
'在前面的图片和数字里找线索。',
'平均距离采用轨道半长轴的科普口径。',
'时间线间距为排版示意；照片和任务年份不同。',
'质量与体重不同；这些数值不是拿星球泡水测出来的。',
'内部并非整齐的同心球壳，许多细节仍在研究。',
'使用真实观测影像。轨道线与光晕是示意；接下来用低视角与侧视图比较轨道倾斜。',
'观测影像（部分赋色）/ 来源见各章',
'北极六边形影像 / PIA17652',
'NASA/JPL-Caltech/Space Science Institute',
'看第1跨页的真实照片。','看第2跨页：比较的是什么？','看第3跨页：它有固体地面吗？','看第4跨页：雨滴是什么？','用手指沿着图案走一圈。',
}
# 保留正文、数字、点读编号及科学限定；只处理制作信息与重复引导。
def unwanted(s):
 return s in exact or s.startswith('小小宇航员 / ') or s.startswith('数据：NASA Planetary Fact Sheet')
files=[p/'八大行星_A3合订稿.pdf',p/'资料/导读与总结.pdf',p/'资料/低角度轨道立体图.pdf',p/'资料/公转轨道倾角.pdf',p/'资料/自转轴倾角.pdf']+list((p/'章节').glob('*/*_A3.pdf'))+[p.parent/'土星样章/土星样章_A3真实照片版.pdf']
log=[]
for f in files:
 if not f.exists():continue
 backup=p/'资料/精简前备份'/f.name
 if not backup.exists():shutil.copy2(f,backup)
 d=fitz.open(f); count=0
 for i,pg in enumerate(d):
  pix=pg.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False)
  for b in pg.get_text('dict')['blocks']:
   for line in b.get('lines',[]):
    s=''.join(x['text'] for x in line['spans']).strip()
    if not unwanted(s):continue
    r=fitz.Rect(line['bbox']);x=5 if r.x0<pg.rect.width/2 else int(pg.rect.width/2+5);y=min(pix.height-1,max(0,int(r.y0)))
    color=tuple(v/255 for v in pix.pixel(x,y)[:3])
    pg.add_redact_annot(r,fill=color,cross_out=False);log.append({'文件':f.name,'页':i+1,'删除':s});count+=1
  pg.apply_redactions(images=0,graphics=0)
 if count:
  tmp=f.with_suffix('.clean.pdf');d.save(tmp,garbage=4,deflate=True);d.close();tmp.replace(f)
 else:d.close()
(p/'资料/内页文案精简记录.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
# 直接从清理后的合订稿更新阅读预览，不触碰音频与语音稿。
d=fitz.open(p/'八大行星_A3合订稿.pdf')
targets=['导读预览-1.png','导读预览-2.png','导读预览-3.png','低角度轨道立体预览.png','公转轨道倾角预览.png','倾角预览-1.png','倾角预览-2.png']
for n in ['水星','金星','地球','火星','木星','土星','天王星','海王星']:
 targets.extend(f'章节/{n}/预览-{i+1}.png' for i in range(7 if n in ['地球','火星','木星'] else 6))
targets.append('总结预览.png')
for pg,t in zip(d,targets):pg.get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(p/t)
print('合订稿页数',len(d),'删除行数',sum(x['文件']=='八大行星_A3合订稿.pdf' for x in log))
