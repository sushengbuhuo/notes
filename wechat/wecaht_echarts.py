# coding: utf-8
from wxpy import Bot, Chat
import re

from snapshot_selenium import snapshot as driver
from pyecharts.render import make_snapshot
from pyecharts import options as opts
from pyecharts.charts import Geo, Map, WordCloud


class Demo(Chat):

    @staticmethod
    def get_friend():
        bot = Bot()
        friends = bot.friends(update=True)

        friend_data = []
        for friend in friends:
            if friend.sex == 1:
                sex = "男"
            elif friend.sex == 2:
                sex = "女"
            else:
                sex = ""
            friend_dict = {
                "city": friend.city,
                "province": friend.province,
                "sex": sex,
                "signature": friend.signature,

            }
            friend_data.append(friend_dict)

        return friend_data

    @staticmethod
    def get_data(friend):

        city_data = [d['city'] for d in friend if d['city']]
        province_data = [d['province'] for d in friend if d['province']]

        city_dict = {}
        for city in city_data:

            if not re.sub("[a-z A-Z]", "", city):
                continue

            city_dict.setdefault(city, 0)
            city_dict[city] += 1

        city_list = []
        for key, value in city_dict.items():
            d = [key, value]
            city_list.append(d)

        province_dict = {}
        for province in province_data:

            if not re.sub("[a-z A-Z]", "", province):
                continue

            province_dict.setdefault(province, 0)
            province_dict[province] += 1

        province_list = []
        for key, value in province_dict.items():
            d = [key, value]
            province_list.append(d)

        return city_list, province_list

    @staticmethod
    def geo_base(data):

        city_list, province_list = data

        # 好友全国省份分布图
        geo = Geo(init_opts=opts.InitOpts(theme="vintage"))
        for city in city_list:
            try:
                geo.add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(color="gray"))
                geo.add("微信好友分布地图", [city], type_="effectScatter", symbol_size=10)
                geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(), title_opts=opts.TitleOpts(title="微信好友分布地图"), )
            except:
                pass

        print("正在制作好友全国分布图")
        make_snapshot(driver, geo.render(), "geo.png")

        # 广东好友热力图
        # geo = Geo(init_opts=opts.InitOpts(theme="vintage"))
        # for city in city_list:
        #     try:
        #         geo.add_schema(maptype="广东", itemstyle_opts=opts.ItemStyleOpts(color="gray"))
        #         geo.add("广东好友热力图", [city], type_="heatmap", symbol_size=10)
        #         geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        #         geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(), title_opts=opts.TitleOpts(title="热力图"),
        #                             toolbox_opts=opts.ToolboxOpts())
        #     except:
        #         pass
        #
        # print("正在制作好友广东热力图")
        # make_snapshot(driver, geo.render(), "heat.png")

        # 好友全国地理图https://github.com/GoJerry/wxFriend/blob/master/echarts.py
        maps = Map()
        maps.add("", province_list, "china")
        maps.set_global_opts(title_opts=opts.TitleOpts(title="微信好友分布图"), visualmap_opts=opts.VisualMapOpts())

        print("正在制作好友地理图")
        make_snapshot(driver, geo.render(), "map.png")

        # 词云图
        c = (
            WordCloud()
            .add("", city_list, word_size_range=[15, 50], shape="diamond", word_gap=10)
            .set_global_opts(title_opts=opts.TitleOpts(title="diamond"))
        )
        print("正在制作好友城市词云图")
        make_snapshot(driver, c.render(), "world.png")


if __name__ == "__main__":
    f = Demo.get_friend()
    fd = Demo.get_data(f)
    Demo.geo_base(fd)