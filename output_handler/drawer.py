from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType


def draw_map(all_sols, file_name):
    geo = Geo(opts.InitOpts('1600px', '900px'))
    geo.add_schema(maptype='china', zoom=1.0)

    for idx0, sol in enumerate(all_sols):
        arc_list = list()
        for idx, node in enumerate(sol):
            if idx < len(sol) - 1:
                next_node = sol[idx + 1]
                arc_list.append((node, next_node))
        node_list = [(node, 0) for node in sol]

        is_selected = idx0 == 0
        geo.add(f'结果{idx0}-城市',
                node_list,
                type_=ChartType.SCATTER,
                is_selected=is_selected,
                effect_opts=opts.EffectOpts(is_show=False),
                symbol_size=8,
                label_opts=opts.LabelOpts(is_show=False))
        geo.add(f'结果{idx0}-路线',
                arc_list,
                type_=ChartType.LINES,
                is_selected=is_selected,
                effect_opts=opts.EffectOpts(is_show=False),
                symbol_size=3,
                linestyle_opts=opts.LineStyleOpts(curve=0.1,
                                                  width=3,
                                                  opacity=0.8),
                label_opts=opts.LabelOpts(is_show=False))
    geo.set_global_opts(title_opts=opts.TitleOpts(
        title='全国城市接龙', pos_top='middle'))
    geo.render(file_name)
    return
