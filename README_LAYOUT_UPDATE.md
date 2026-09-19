# 个人主页全站统一修订 v2.2

版本标识：`20260919-v2-2`。七个栏目、原有子栏目、正文记录及媒体资源保留；未发布到线上。

## 这次改了什么

全站采用同一无衬线字体栈，移除外链字体依赖。履历、课程、学生指导、活动的标题／职位／附注采用同一套语义样式，消除 Teaching 中相同学校名称一处14px、一处16px的问题。论文年份仍为桌面20px／手机18px，小于栏目标题24px／22px。论文引用和资源行保持严格对齐与2px间距。

CV HTML 明确包含数字年月：博士2022.9–2026.8、剑桥和Downing均2023.5–2023.11等。学校名称在七页及侧栏均不加链接；导师姓名和论文资源链接保留。导航、侧栏学术图标及头像边缘的视觉处理更克制。

HTML 包含完整导航和侧栏，JavaScript 不再负责生成核心页面内容。编码、公共片段和缓存版本一并统一。

## 更新网站：不能只替换 CSS

**推荐直接使用完整源码包。** 将 `li-ruidong.github.io-main` 文件夹里的内容放入原网站仓库根目录，保持原来的目录层级；不要把这个文件夹再嵌套到已有的网站根目录下面。

使用覆盖包时，解压后把其中所有文件和目录按原层级覆盖到仓库根目录。覆盖包包括七页 HTML、公共 CSS、JS 及辅助文件，不重复包含未改动的图片和 PDF。它不是一个可以脱离旧资源目录独立运行的网站。

提交并按原有方式部署后，确认网页源代码含有 `data-layout-version="20260919-v2-2"`，以及 `cv/index.html` 中能找到 `2022.9`。CSS/JS 新版本参数只能更新资源引用，不能替代页面HTML的上传。浏览器需要时使用 Ctrl+F5 刷新。

本次没有操作用户的 GitHub 仓库或线上网站。

## 本地查看

Windows 可双击 `preview.bat`。也可以在网站根目录执行：

```sh
python preview.py
```

需要 Python 3，不需要额外安装Python包；脚本会启动仅本机可访问的服务并打开浏览器。默认端口8000占用时使用 `python preview.py --port 8001`。按 Ctrl+C 停止。

不要直接双击某个 `index.html` 来检查网站；现有资源使用以 `/assets/` 开头的站点根路径，需要通过HTTP预览。

## 以后怎么保持一致

排版标准：`docs/STYLE_STANDARD.md`。公共样式只有 `assets/css/academic-site.css` 一份。

修改公共侧栏／导航：编辑 `includes/profile.html`、`includes/header.html` 后运行：

```sh
python tools/sync_shared.py
python tools/sync_shared.py --check
python tools/check_site.py
```

无需Node、构建框架或额外Python包。这里的静态检查不能替代浏览器视觉检查；本次浏览器验收结果放在 `docs/VALIDATION.md` 和 `docs/browser-validation.json`。

## 内容范围

本轮没有新增论文、改写身份状态或重新翻译职务。学校名称的链接移除不会改动相应文字。**下载用的英文CV PDF仍是原文件，不是更新后的网页CV导出件。** 原始图片、PDF没有修改；上传的新中文简历也没有被直接发布到网站。

不确定的项目月份和存在冲突的日期保持原样，不编造月份。
