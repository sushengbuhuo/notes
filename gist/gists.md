# 我的第一个GitHub项目

这是项目 [helloworld](https://github.com/gotgithub/helloworld) ，
欢迎访问。

这个项目的版本库是 **Git格式** ，在 Windows、Linux、Mac OS X
平台都有客户端工具可以访问。虽然版本库只提供Git一种格式，
但是你还是可以用其他用其他工具访问，如 ``svn`` 和 ``hg`` 。

## 版本库地址

支持三种访问协议：

* HTTP协议: `https://github.com/gotgithub/helloworld.git` 。
* Git协议: `git://github.com/gotgithub/helloworld.git` 。
* SSH协议: `ssh://git@github.com/gotgithub/helloworld.git` 。

## 克隆版本库

操作示例：

    $ git clone git://github.com/gotgithub/helloworld.git


Git的分支就是保存在.git/refs/heads/命名空间下的引用。引用文件的内容是该分支对应的提交ID。当前版本库中的默认分支master就对应于文件.git/refs/heads/master。

当前master文件的内容是https://github.com/mingyun/mingyun/commit/c39d2180031739f667373543253bef1db5364705
中的c39d2180031739f667373543253bef1db5364705



touch README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin https://github.com/mingyun/susheng.github.io.git
git push -u origin master

git remote add origin https://github.com/mingyun/susheng.github.io.git
git push -u origin master
