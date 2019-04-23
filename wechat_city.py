import itchat
from pyecharts import Map

#Python生成微信好友位置分布图
#import提示找不到pyecharts_snapshot  pip install pyecharts_snapshot  https://github.com/pyecharts/pyecharts/issues/750 
List = []
a = {}
name = []
value = []
# 登录微信
itchat.login()
# 获取所有好友信息
owner = itchat.get_friends()
# 获取所有好友的所在位置
for i in owner:
    province = i['Province']
    List.append(province)
# 获取每个位置对应的好友人数
for s in List:
    if List.count(s) >= 1:
        a[s] = List.count(s)
# 把去重后的位置添加到列表name中
for j in a:
    name.append(j)
# 把每个位置对应的好友人数添加到列表values中
for v in a.values():
    value.append(v)
# 生成地图
maps = Map('微信好友位置分布图', width=1500, height=900)     # 设置地图的宽和高
# 把数据添加到地图中
print(name)
print(value)
maps.add('', name, value, maptype='china', is_visualmap=True, visual_text_color='#000', is_label_show=True, visual_range=[0, 20])
# is_visualmap        --->    是否使用视觉映射组件
# visual_text_color   --->    两端文本颜色
# is_label_show       --->    是否正常显示标签。标签即各点的数据项信息
# visual_range        --->    指定允许的最小值与最大值
maps.render('微信好友位置分布图.html')       # 生成HTML文件