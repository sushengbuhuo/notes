# sushengbuhuo.github.io


#多账号ssh配置
[Git常用命令清单笔记](https://segmentfault.com/a/1190000002479970)

1.生成指定名字的密钥
ssh-keygen -t rsa -C "邮箱地址" -f ~/.ssh/github_sushengbuhuo 
会生成 github_sushengbuhuo 和 github_sushengbuhuo.pub 这两个文件

2.密钥复制到托管平台上
vim ~/.ssh/github_sushengbuhuo.pub 
打开公钥文件 github_sushengbuhuo.pub ，并把内容复制至代码托管平台上

3.修改config文件
vim ~/.ssh/config #修改config文件，如果没有创建 config
```php
Host sushengbuhuo.github.com
HostName github.com
User git
IdentityFile ~/.ssh/github_sushengbuhuo

Host abc.github.com
HostName github.com
User git
IdentityFile ~/.ssh/github_abc
```
4.测试
```js
ssh -T  git@sushengbuhuo.github.com # @后面跟上定义的Host

Hi sushengbuhuo! You've successfully authenticated, but GitHub does not provide shell access.#说明成功了
```
5.git clone git@sushengbuhuo.github.com:sushengbuhuo/sushengbuhuo.github.io

`print('n'.join([''.join([('Love'[(x-y) % len('Love')] if ((x0.05)2+(y0.1)2-1)3-(x0.05)2(y0.1)*3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(30, -30, -1)]))`
```php

               veLoveLov           veLoveLov
           eLoveLoveLoveLove   eLoveLoveLoveLove
         veLoveLoveLoveLoveLoveLoveLoveLoveLoveLov
        veLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveL
       veLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLov
       eLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLove
       LoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveL
       oveLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLo
       veLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLov
       eLoveLoveLoveLoveLoveLoveLoveLoveLoveLoveLove
        oveLoveLoveLoveLoveLoveLoveLoveLoveLoveLove
         eLoveLoveLoveLoveLoveLoveLoveLoveLoveLove
         LoveLoveLoveLoveLoveLoveLoveLoveLoveLoveL
           eLoveLoveLoveLoveLoveLoveLoveLoveLove
            oveLoveLoveLoveLoveLoveLoveLoveLove
             eLoveLoveLoveLoveLoveLoveLoveLove
               veLoveLoveLoveLoveLoveLoveLov
                 oveLoveLoveLoveLoveLoveLo
                   LoveLoveLoveLoveLoveL
                      LoveLoveLoveLov
                         LoveLoveL
                            Lov
                             v
 ```                            
[搭建博客](https://alvabill.ml/hexo%E6%90%AD%E5%BB%BA%E4%B8%AA%E4%BA%BA%E5%8D%9A%E5%AE%A2--%E5%9F%BA%E7%A1%80%E7%AF%87/) 

[hexo](https://www.jianshu.com/p/21c94eb7bcd1)

[Hexo+Pages静态博客-Next主题篇](https://blog.csdn.net/mango_haoming/article/details/78207534)

[绝配：hexo+next主题及我走过的坑](https://www.jianshu.com/p/21c94eb7bcd1)
