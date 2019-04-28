---
title: hexo搭建博客
tags:
- hexo
---
通常我们可以使用github pages 来搭建静态博客，建立一个username.github.io的项目就可以了，如果要将其他项目也作为页面展示，可以将代码推送到gh-pages分支。

GitHub pages木有默认样式，所以如果你不会自己写css，博客很难看的，所以有了hexo.
### 准备
先安装好git node hexo
#### 初始化
```javascript
$ hexo init blog
INFO  Cloning hexo-starter to D:\code\hexo\blog
Cloning into 'D:\code\hexo\blog'...
remote: Enumerating objects: 68, done.
remote: Total 68 (delta 0), reused 0 (delta 0), pack-reused 68
Unpacking objects: 100% (68/68), done.
Submodule 'themes/landscape' (https://github.com/hexojs/hexo-theme-landscape.git) registered for path 'themes/landscape'
Cloning into 'D:/code/hexo/blog/themes/landscape'...
remote: Enumerating objects: 5, done.
remote: Counting objects: 100% (5/5), done.
remote: Compressing objects: 100% (5/5), done.
remote: Total 846 (delta 0), reused 1 (delta 0), pack-reused 841
Receiving objects: 100% (846/846), 2.55 MiB | 16.00 KiB/s, done.
Resolving deltas: 100% (445/445), done.
Submodule path 'themes/landscape': checked out '73a23c51f8487cfcd7c6deec96ccc7543960d350'
INFO  Install dependencies
yarn install v1.9.4
info No lockfile found.
[1/4] Resolving packages...
warning hexo > titlecase@1.1.2: no longer maintained
warning hexo > nunjucks > postinstall-build@5.0.3: postinstall-build's behavior is now built into npm! You should migrate off of postinstall-build and use the new `prepare` lifecycle script with npm 5.0.0 or greater.
[2/4] Fetching packages...
info fsevents@1.2.4: The platform "win32" is incompatible with this module.
info "fsevents@1.2.4" is an optional dependency and failed compatibility check. Excluding it from installation.
[3/4] Linking dependencies...
[4/4] Building fresh packages...
success Saved lockfile.
Done in 18.06s.
INFO  Start blogging with Hexo!

$ cd blog
hexo的目录结构
.
├── .deploy       #需要部署的文件
├── node_modules  #Hexo插件
├── public        #生成的静态网页文件
├── scaffolds     #模板
├── source        #博客正文和其他源文件, 404 favicon CNAME 等都应该放在这里
|   ├── _drafts   #草稿
|   └── _posts    #文章
├── themes        #主题
├── _config.yml   #全局配置文件
└── package.json
$ npm install
npm WARN deprecated titlecase@1.1.2: no longer maintained
npm WARN deprecated postinstall-build@5.0.3: postinstall-build's behavior is now built into npm! You should migrate off of postinstall-build and use the new `prepare` lifecycle script with npm 5.0.0 or greater.

> nunjucks@3.1.4 postinstall D:\code\hexo\blog\node_modules\nunjucks
> node postinstall-build.js src

npm WARN rollback Rolling back node-pre-gyp@0.10.0 failed (this is probably harmless): EPERM: operation not permitted, rmdir 'D:\code\hexo\blog\node_modules\fsevents\node_modules'
npm notice created a lockfile as package-lock.json. You should commit this file.
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@1.2.4 (node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@1.2.4: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})

added 101 packages, removed 40 packages and updated 321 packages in 23.882s

$ ls
_config.yml    package.json       scaffolds/  themes/
node_modules/  package-lock.json  source/     yarn.lock

$ hexo g
INFO  Start processing
INFO  Files loaded in 655 ms
INFO  Generated: index.html
INFO  Generated: archives/index.html
INFO  Generated: fancybox/jquery.fancybox.css
INFO  Generated: fancybox/blank.gif
INFO  Generated: fancybox/fancybox_loading@2x.gif
INFO  Generated: fancybox/fancybox_sprite@2x.png
INFO  Generated: fancybox/jquery.fancybox.js
INFO  Generated: fancybox/jquery.fancybox.pack.js
INFO  Generated: fancybox/fancybox_sprite.png
INFO  Generated: fancybox/fancybox_overlay.png
INFO  Generated: archives/2018/11/index.html
INFO  Generated: fancybox/fancybox_loading.gif
INFO  Generated: css/fonts/FontAwesome.otf
INFO  Generated: fancybox/helpers/jquery.fancybox-thumbs.css
INFO  Generated: js/script.js
INFO  Generated: fancybox/helpers/jquery.fancybox-buttons.js
INFO  Generated: fancybox/helpers/jquery.fancybox-media.js
INFO  Generated: fancybox/helpers/jquery.fancybox-buttons.css
INFO  Generated: css/fonts/fontawesome-webfont.eot
INFO  Generated: css/fonts/fontawesome-webfont.woff
INFO  Generated: fancybox/helpers/fancybox_buttons.png
INFO  Generated: fancybox/helpers/jquery.fancybox-thumbs.js
INFO  Generated: css/style.css
INFO  Generated: css/fonts/fontawesome-webfont.ttf
INFO  Generated: archives/2018/index.html
INFO  Generated: css/images/banner.jpg
INFO  Generated: css/fonts/fontawesome-webfont.svg
INFO  Generated: 2018/11/20/hello-world/index.html
INFO  28 files generated in 1.26 s


$ hexo s
INFO  Start processing
INFO  Hexo is running at http://localhost:4000 . Press Ctrl+C to stop

$ hexo d
ERROR Deployer not found: git

```
### GitHub key 配置
```javascript
1.生成指定名字的密钥 
ssh-keygen -t rsa -C “xx@sina.com” -f ~/.ssh/github_sushengbuhuo 
会生成 github_sushengbuhuo 和 github_sushengbuhuo.pub 这两个文件

2.密钥复制到托管平台上 
vim ~/.ssh/github_sushengbuhuo.pub ，把内容复制至代码托管平台上

3.修改config文件 vim ~/.ssh/config #修改config文件，如果没有创建 config

Host sushengbuhuo.github.com
HostName github.com
User git
IdentityFile ~/.ssh/github_sushengbuhuo

Host github.com
HostName github.com
User git
IdentityFile ~/.ssh/github
4.测试验证
$ ssh -T git@github.com:
ssh: Could not resolve hostname github.com:: Name or service not known

$ ssh -T git@github.com
git@github.com: Permission denied (publickey).

$ ssh -T  git@sushengbuhuo.github.com
Hi sushengbuhuo! You've successfully authenticated, but GitHub does not provide shell access.
```
#### 配置config.yml
```javascript
deploy:
  type: git
  repository: git@sushengbuhuo.github.com:sushengbuhuo/sushengbuhuo.github.io.git
  branch: master
  
theme: next
```
### 推送到GitHub
```javascript
$ hexo clean && hexo g
INFO  Deleted database.
INFO  Deleted public folder.
INFO  Start processing
INFO  Files loaded in 545 ms
INFO  Generated: index.html
INFO  Generated: archives/index.html
INFO  Generated: fancybox/fancybox_loading.gif
INFO  Generated: fancybox/fancybox_sprite@2x.png
INFO  Generated: fancybox/jquery.fancybox.js
INFO  Generated: fancybox/fancybox_overlay.png
INFO  Generated: fancybox/jquery.fancybox.css
INFO  Generated: fancybox/jquery.fancybox.pack.js
INFO  Generated: fancybox/blank.gif
INFO  Generated: fancybox/fancybox_loading@2x.gif
INFO  Generated: fancybox/fancybox_sprite.png
INFO  Generated: css/fonts/FontAwesome.otf
INFO  Generated: archives/2018/11/index.html
INFO  Generated: css/fonts/fontawesome-webfont.eot
INFO  Generated: archives/2018/index.html
INFO  Generated: fancybox/helpers/fancybox_buttons.png
INFO  Generated: fancybox/helpers/jquery.fancybox-thumbs.js
INFO  Generated: css/fonts/fontawesome-webfont.woff
INFO  Generated: fancybox/helpers/jquery.fancybox-buttons.css
INFO  Generated: js/script.js
INFO  Generated: fancybox/helpers/jquery.fancybox-buttons.js
INFO  Generated: css/style.css
INFO  Generated: fancybox/helpers/jquery.fancybox-thumbs.css
INFO  Generated: 2018/11/20/hello-world/index.html
INFO  Generated: css/fonts/fontawesome-webfont.ttf
INFO  Generated: css/fonts/fontawesome-webfont.svg
INFO  Generated: css/images/banner.jpg
INFO  Generated: fancybox/helpers/jquery.fancybox-media.js
INFO  28 files generated in 1.13 s

$ hexo d
ERROR Deployer not found: git

$ npm install hexo-deployer-git --save
npm WARN deprecated swig@1.4.2: This package is no longer maintained
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@1.2.4 (node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@1.2.4: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})

+ hexo-deployer-git@0.3.1
added 31 packages in 17.866s

$ hexo d
INFO  Deploying: git
INFO  Setting up Git deployment...
Initialized empty Git repository in D:/code/hexo/blog/.deploy_git/.git/
[master (root-commit) 9c86786] First commit
 Committer: unknown <xxx@sina.com.cn>
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
You can suppress this message by setting them explicitly:

    git config --global user.name "Your Name"
    git config --global user.email you@example.com

After doing this, you may fix the identity used for this commit with:

    git commit --amend --reset-author

 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 placeholder
INFO  Clearing .deploy_git folder...
INFO  Copying files from public folder...
INFO  Copying files from extend dirs...
warning: LF will be replaced by CRLF in 2018/11/20/hello-world/index.html.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in archives/2018/11/index.html.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in archives/2018/index.html.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in archives/index.html.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in css/style.css.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/helpers/jquery.fancybox-buttons.css.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/helpers/jquery.fancybox-buttons.js.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/helpers/jquery.fancybox-media.js.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/helpers/jquery.fancybox-thumbs.css.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/helpers/jquery.fancybox-thumbs.js.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/jquery.fancybox.css.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/jquery.fancybox.js.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/jquery.fancybox.pack.js.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in index.html.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in js/script.js.
The file will have its original line endings in your working directory.
[master b7f7580] Site updated: 2018-11-20 11:51:50
 Committer: unknown <xxx@sina.com.cn>
Your name and email address were configured automatically based
on your username and hostname. Please check that they are accurate.
You can suppress this message by setting them explicitly:

    git config --global user.name "Your Name"
    git config --global user.email you@example.com

After doing this, you may fix the identity used for this commit with:

    git commit --amend --reset-author

 29 files changed, 5777 insertions(+)
 create mode 100644 2018/11/20/hello-world/index.html
 create mode 100644 archives/2018/11/index.html
 create mode 100644 archives/2018/index.html
 create mode 100644 archives/index.html
 create mode 100644 css/fonts/FontAwesome.otf
 create mode 100644 css/fonts/fontawesome-webfont.eot
 create mode 100644 css/fonts/fontawesome-webfont.svg
 create mode 100644 css/fonts/fontawesome-webfont.ttf
 create mode 100644 css/fonts/fontawesome-webfont.woff
 create mode 100644 css/images/banner.jpg
 create mode 100644 css/style.css
 create mode 100644 fancybox/blank.gif
 create mode 100644 fancybox/fancybox_loading.gif
 create mode 100644 fancybox/fancybox_loading@2x.gif
 create mode 100644 fancybox/fancybox_overlay.png
 create mode 100644 fancybox/fancybox_sprite.png
 create mode 100644 fancybox/fancybox_sprite@2x.png
 create mode 100644 fancybox/helpers/fancybox_buttons.png
 create mode 100644 fancybox/helpers/jquery.fancybox-buttons.css
 create mode 100644 fancybox/helpers/jquery.fancybox-buttons.js
 create mode 100644 fancybox/helpers/jquery.fancybox-media.js
 create mode 100644 fancybox/helpers/jquery.fancybox-thumbs.css
 create mode 100644 fancybox/helpers/jquery.fancybox-thumbs.js
 create mode 100644 fancybox/jquery.fancybox.css
 create mode 100644 fancybox/jquery.fancybox.js
 create mode 100644 fancybox/jquery.fancybox.pack.js
 create mode 100644 index.html
 create mode 100644 js/script.js
 delete mode 100644 placeholder
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
FATAL Something's wrong. Maybe you can find the solution here: http://hexo.io/docs/troubleshooting.html
Error: git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.

    at ChildProcess.<anonymous> (D:\code\hexo\blog\node_modules\hexo-util\lib\spawn.js:37:17)
    at emitTwo (events.js:126:13)
    at ChildProcess.emit (events.js:214:7)
    at ChildProcess.cp.emit (D:\code\hexo\blog\node_modules\cross-spawn\lib\enoent.js:40:29)
    at maybeClose (internal/child_process.js:925:16)
    at Socket.stream.socket.on (internal/child_process.js:346:11)
    at emitOne (events.js:116:13)
    at Socket.emit (events.js:211:7)
    at Pipe._handle.close [as _onclose] (net.js:557:12)

$ hexo d
INFO  Deploying: git
INFO  Clearing .deploy_git folder...
INFO  Copying files from public folder...
INFO  Copying files from extend dirs...
warning: LF will be replaced by CRLF in 2018/11/20/hello-world/index.html.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in archives/2018/11/index.html.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in archives/2018/index.html.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in archives/index.html.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in css/style.css.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/helpers/jquery.fancybox-buttons.css.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/helpers/jquery.fancybox-buttons.js.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/helpers/jquery.fancybox-media.js.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/helpers/jquery.fancybox-thumbs.css.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/helpers/jquery.fancybox-thumbs.js.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/jquery.fancybox.css.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/jquery.fancybox.js.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in fancybox/jquery.fancybox.pack.js.
The file will have its original line endings in your working directory.
warning: LF will be replaced by CRLF in js/script.js.
The file will have its original line endings in your working directory.
On branch master
nothing to commit, working tree clean
Branch 'master' set up to track remote branch 'master' from 'git@sushengbuhuo.github.com:sushengbuhuo/sushengbuhuo.github.io.git'.
To sushengbuhuo.github.com:sushengbuhuo/sushengbuhuo.github.io.git
 + 3037877...b7f7580 HEAD -> master (forced update)
INFO  Deploy done: git

$ git clone https://github.com/iissnan/hexo-theme-next themes/next
Cloning into 'themes/next'...
remote: Enumerating objects: 12033, done.
remote: Total 12033 (delta 0), reused 0 (delta 0), pack-reused 12033
Receiving objects: 100% (12033/12033), 12.95 MiB | 79.00 KiB/s, done.
Resolving deltas: 100% (6966/6966), done.

$ hexo clean && hexo g
INFO  Deleted database.
INFO  Deleted public folder.
INFO  Start processing
$ hexo d

$ hexo s
INFO  Start processing
WARN  ===============================================================
WARN  ========================= ATTENTION! ==========================
WARN  ===============================================================
WARN   NexT repository is moving here: https://github.com/theme-next
WARN  ===============================================================
WARN   It's rebase to v6.0.0 and future maintenance will resume there
WARN  ===============================================================
INFO  Hexo is running at http://localhost:4000 . Press Ctrl+C to stop
```
### 安装插件
登录[admin](http://localhost:4000/admin) 即可看到我们所有的文章内容
```javascript
λ npm i hexo-admin --save
npm WARN deprecated minimatch@2.0.10: Please update to minimatch 3.0.2 or higher to avoid a RegExp DoS issue
npm WARN deprecated connect@2.7.11: connect 2.x series is deprecated
npm WARN deprecated cryptiles@2.0.5: This version is no longer maintained. Please upgrade to the latest version.
npm WARN deprecated boom@2.10.1: This version is no longer maintained. Please upgrade to the latest version.
npm WARN deprecated hoek@2.16.3: This version is no longer maintained. Please upgrade to the latest version.
npm WARN acorn-dynamic-import@4.0.0 requires a peer of acorn@^6.0.0 but none is installed. You must install peer dependencies yourself.
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@1.2.4 (node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@1.2.4: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})

+ hexo-admin@2.3.0
added 251 packages in 23.975s


   ╭─────────────────────────────────────╮
   │                                     │
   │   Update available 5.6.0 → 6.4.1    │
   │       Run npm i npm to update       │
   │                                     │
   ╰─────────────────────────────────────╯

#网站底部字数统计
d:\code\hexo\blog
λ npm install hexo-wordcount --save
npm WARN rollback Rolling back node-pre-gyp@0.10.0 failed (this is probably harmless): EPERM: operation not permitted, scandir 'd:\code\hexo\blog\node_modules\fsevents\node_modules'
npm WARN acorn-dynamic-import@4.0.0 requires a peer of acorn@^6.0.0 but none is installed. You must install peer dependencies yourself.
npm WARN optional SKIPPING OPTIONAL DEPENDENCY: fsevents@1.2.4 (node_modules\fsevents):
npm WARN notsup SKIPPING OPTIONAL DEPENDENCY: Unsupported platform for fsevents@1.2.4: wanted {"os":"darwin","arch":"any"} (current: {"os":"win32","arch":"x64"})

+ hexo-wordcount@6.0.1
added 1 package in 10.289s

搜索npm install hexo-generator-searchdb --save 
npm install hexo-generator-search  --save

在根目录下的/theme/next/_config.yml文件中添加配置：
search:
  path: search.xml
  field: post
  format: html
  limit: 10000
  
 在根目录下的/theme/next/_config.yml文件中搜索local_search，将enable改为true：
 local_search:
   enable: true 
  
```
### 问题
中文乱码

将config.yml 和md文件编码转为utf-8

修改config.yml `language: zh-Hans`
### 新建文章

``` bash
$ hexo new "PHP依赖注入"
```
Hexo 默认以标题做为文件名称，但您可编辑_config.yml `new_post_name` 参数来改变默认的文件名称，举例来说，设为 :year-:month-:day-:title.md 可让您更方便的通过日期来管理文章。
### 标签分类
```javascript
主菜单设置 blog/_config.yml 添加如下配置
menu:
  home: /
  archives: /archives
  categories: /categories   #手动新建
  tags: /tags               #手动新建
  commonweal: /404.html     #手动新建
  about: /about             #手动新建
 
 
  next/_config.yml 添加如下配置
menu:
  home: / || home
  about: /about/ || user
  tags: /tags/ || tags
  categories: /categories/ || th
  archives: /archives/ || archive
  
  
标签云 页面
命令

hexo new page tags
页面设置

title: tags
date: 2015-09-19 22:37:08
type: "tags"
comments: false
---
关于 页面
命令

hexo new page about
页面设置

title: about
date: 2015-09-19 22:37:08
comments: false
---
About Me #这里编辑 '关于我' 的内容
分类 页面
命令

hexo new page categories
页面设置

title: categories
date: 2015-09-19 22:37:08
type: "categories"
comments: false
---

```
### 显示统计字数和估计阅读时长
```javascript
npm install hexo-wordcount --save
vi blog\themes\hexo-theme-next\_config.yml
post_wordcount:
  item_text: true
  wordcount: true
  min2read: true
  totalcount: false
  separated_meta: false
vi blog\themes\hexo-theme-next\layout\_macro\ **post.swig**文件
 {{ wordcount(post.content) }} 字
   {{ min2read(post.content) }} 分钟 
```
### 显示总访客数和总浏览量
```javascript
vi  D:\blog\themes\hexo-theme-next\layout_partials\ footer.swig
首行添加如下代码：
<script async src="https://dn-lbstatics.qbox.me/busuanzi/2.3/busuanzi.pure.mini.js"></script>

#接着修改相应代码：
# 添加总访客量
<span id="busuanzi_container_site_uv">
  访客数:<span id="busuanzi_value_site_uv"></span>人次
</span>

{% if theme.footer.powered %}
  <!--<div class="powered-by">{#
  #}{{ __('footer.powered', '<a class="theme-link" target="_blank" href="https://hexo.io">Hexo</a>') }}{#
#}</div>-->
{% endif %}

# 添加'|'符号
{% if theme.footer.powered and theme.footer.theme.enable %}
  <span class="post-meta-divider">|</span>
{% endif %}


{% if theme.footer.custom_text %}
  <div class="footer-custom">{#
  #}{{ theme.footer.custom_text }}{#
#}</div>
{% endif %}

# 添加总访问量
<span id="busuanzi_container_site_pv">
   总访问量:<span id="busuanzi_value_site_pv"></span>次
</span>

# 添加'|'符号
{% if theme.footer.powered and theme.footer.theme.enable %}
  <span class="post-meta-divider">|</span>
{% endif %}

# 添加博客全站共：
<div class="theme-info">
  <div class="powered-by"></div>
  <span class="post-count">博客全站共{{ totalcount(site) }}字</span>
</div>
```
[新写文章文档](https://hexo.io/zh-cn/docs/writing.html)

### 资源
[打造个性超赞博客Hexo+NexT+GitHubPages的超深度优化](https://reuixiy.github.io/technology/computer/computer-aided-art/2017/06/09/hexo-next-optimization.html#附上我的-custom-styl)

[用Github+Hexo搭建你的个人博客：美化篇](https://www.makcyun.top/hexo02.html)

[hexo文档](https://hexo.io/docs/)

[hexo问题交流](https://hexo.io/docs/troubleshooting.html) 
 
[Deployment](https://hexo.io/docs/deployment.html)

[绝配：hexo+next主题及我走过的坑](https://www.jianshu.com/p/21c94eb7bcd1)

[Hexo+Pages静态博客-Next主题篇](https://blog.csdn.net/mango_haoming/article/details/78207534)

[hexo部署到服务器](https://laravel-china.org/articles/20991)

[关于HEXO搭建个人博客的点点滴滴](https://juejin.im/post/5a6ee00ef265da3e4b770ac1#heading-6)

[搭建博客](https://alvabill.ml/hexo%E6%90%AD%E5%BB%BA%E4%B8%AA%E4%BA%BA%E5%8D%9A%E5%AE%A2--%E5%9F%BA%E7%A1%80%E7%AF%87/)

[手把手教你用Hexo搭建个人技术博客](https://juejin.im/post/5abcd2286fb9a028d66440ba)

[基于CentOS搭建Hexo博客](https://segmentfault.com/a/1190000012907499)

[最快的 Hexo 博客搭建方法](https://blog.coding.net/blog/CS-Hexo)

[超详细Hexo+Github博客搭建小白教程](https://zhuanlan.zhihu.com/p/35668237)

[在Github上备份Hexo博客](https://lrscy.github.io/2018/01/26/Hexo-Github-Backup/)

[最快的 Hexo 博客搭建方法](https://blog.coding.net/blog/CS-Hexo)

[Hugo是由Go语言实现的静态网站生成器](http://www.gohugo.org/)

[yilia主题](https://github.com/litten/hexo-theme-yilia)

[使用 Hugo 搭建博客](https://segmentfault.com/a/1190000012975914#articleHeader7)

[博客发布上线方案 — Hexo](https://www.fanhaobai.com/2018/03/hexo-deploy.html)

[hexo博客](https://github.com/fan-haobai/blog)

[使用HEXO搭建博客](http://coderlt.coding.me/2015/09/21/blog-with-hexo/)

[部署Hexo博客到Coding](http://coderlt.coding.me/2015/09/24/hexo-to-coding-150924/)

[用Github+Hexo搭建你的个人博客：美化篇](https://www.makcyun.top/hexo02.html)

[无后端评论系统](https://valine.js.org/)

[hexo博客添加标签功能](https://swoole.app/2016/07/23/hexo%E5%8D%9A%E5%AE%A2%E6%B7%BB%E5%8A%A0%E6%A0%87%E7%AD%BE%E5%8A%9F%E8%83%BD/)