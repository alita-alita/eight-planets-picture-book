# -*- coding: utf-8 -*-
from pathlib import Path
import fitz,csv,json
from fontTools.ttLib import TTFont
p=Path(__file__).resolve().parent.parent;d=fitz.open(p/'八大行星_A3合订稿.pdf');bad=[];over=[];fontmissing=[]
fonts={'Heiti':TTFont('/System/Library/Fonts/STHeiti Medium.ttc',fontNumber=1).getBestCmap(),'DIN':TTFont('/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf').getBestCmap()}
for i,pg in enumerate(d):
 if abs(pg.rect.width-1190.55)>1 or abs(pg.rect.height-841.89)>1:bad.append((i+1,'纸张尺寸'))
 ss=[s for b in pg.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans']]
 for s in ss:
  r=fitz.Rect(s['bbox'])
  if r.x0<0 or r.y0<0 or r.x1>pg.rect.width or r.y1>pg.rect.height or (7<=i<58 and r.x0<pg.rect.width/2-2<r.x1):bad.append((i+1,s['text']))
  cmap=fonts['DIN' if 'DIN' in s['font'] else 'Heiti']
  for ch in s['text']:
   if ord(ch) not in cmap:fontmissing.append((i+1,ch,s['font']))
 for j,a in enumerate(ss):
  for b in ss[j+1:]:
   r=fitz.Rect(a['bbox'])&fitz.Rect(b['bbox'])
   if not r.is_empty and r.height>4 and r.width>5:over.append((i+1,a['text'],b['text']))
with (p/'全书点读对应表.csv').open(encoding='utf-8-sig') as f:rows=list(csv.reader(f))[1:]
codes=[r[1] for r in rows];rendercodes=[]
for pg in d:
 for word in pg.get_text('words'):
  if word[4] in codes:rendercodes.append(word[4])
result={'A3跨页数':len(d),'阅读页数':2*len(d),'点读文稿数':len(rows),'唯一编号数':len(set(codes)),'纸面点读位数':len(rendercodes),'纸面与文稿编号一致':set(codes)==set(rendercodes),'文字越界':bad,'文字重叠':over,'缺字':fontmissing}
print(json.dumps(result,ensure_ascii=False,indent=2));(p/'资料'/'最终审查.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
(p/'审校记录.md').write_text('# 八大行星 · 审校记录\n\n核对日期：2026年10月10日。\n\n'+ '\n'.join('- '+k+'：'+str(v) for k,v in result.items())+'\n\n## 内容与图片修正\n\n- 水星的体积比与质量比分开，分别约0.056与0.055。\n- 直径采用体积等效平均值，赤道速度估算另用赤道直径。\n- 水星、金星区分自转周期和太阳日；地球、火星也分别标注。\n- 火卫一、火卫二使用最长尺寸，不冒充平均直径；火卫二原图是同一颗卫星的两次观测。\n- 月球图片来源核对为伽利略号，不使用错误的LRO或克莱门汀号署名。\n- 金星照片裁掉原档版本间的白色分隔线；雷达地图与三维地形重建明确标注非可见光实拍。\n- 木卫一近似自然色、木卫二近似自然色拼接与局部补色分别说明；韦布图片注明近红外赋色。\n- 内部页面的观测照片只显示外部，不把它当作剖面照片。\n- 原土星章节直接合入定稿；保留已认可的版面。\n- 低角度轨道、侧视轨道倾角与自转轴倾角四个跨页移至导读部分，目录及PDF书签同步。\n- 金星PIA23791改标橙光与紫外滤镜赋色合成，不再标作可见光实拍。\n- 全书语音稿数字、百分比、摄氏温度统一为口语读法；删除修订过程用语。\n- 全部新增章节使用简体中文字体，检查字体覆盖与PDF实际文字；渲染后逐章检查预览。\n- 部分音频已生成，现保持暂停；校订稿变动已列入音频复核清单。贴纸编号尚未绑定。A3稿仍需按最终装订方式做拼版和出血。\n')
