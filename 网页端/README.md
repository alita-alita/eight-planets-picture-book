# 八大行星 · 网页点读书

在线访问：https://little-astronaut-planets.xingya-shi.chatgpt.site

英语小课堂：https://little-astronaut-planets.xingya-shi.chatgpt.site/english.html

## 功能

- 60页中文绘本，222段点读配音。
- 竖屏单页、横屏跨页；滑动翻页、双指缩放、连续朗读和自动翻页。
- 八大行星及太阳的英语学习页，40段单词、短句和游戏提示音频。
- 听音找星球、排列太阳系小游戏；中文名称可切换。
- 手机英语学习页底部固定上一颗、下一颗及中文科普入口。

## 本地预览

在本目录运行：

```sh
python3 -m http.server 8765 --directory dist
```

然后访问 http://localhost:8765 。文件无需安装前端依赖或构建。

## 目录

- `dist/`：完整可部署网页，包含页面图片及中英文MP3。
- `prepare.py`：根据原书生成网页资源，运行时需调整本地路径并安装PyMuPDF、Pillow。
- `make_english_audio.py`：英语配音生成脚本，需要自行提供火山引擎密钥；仓库不含密钥。
- `.openai/hosting.json`：现有Sites站点配置。

部署顺序：先将网页修改提交并推送到本GitHub仓库，核对提交，再发布同一份网页资源到现有Sites站点。网站公开访问与GitHub仓库私有权限互相独立。
