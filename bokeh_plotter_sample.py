from bokeh.io import output_notebook, push_notebook, show
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource, FactorRange
from bokeh.models import GMapPlot, GMapOptions, Circle, Range1d
from bokeh.models import BoxZoomTool, ResetTool, HoverTool
from bokeh.models import CustomJS, Slider
from bokeh.models import TextInput
from bokeh.layouts import row, column, gridplot
from random import random

# p = figure(plot_width = 400, plot_height = 400)
# p.line ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], line_width = 2)
# p.step ([1, 2, 3, 4, 5], [5, 4, 3, 2, 1], line_width = 20, mode = "center")
# p.multi_line ([[1, 2, 3, 4, 5], [5, 4, 3, 2, 1]], [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]], color = ["firebrick", "navy"], alpha = [0.8, 0.3], line_width = 4) """
# p.square ([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size = 20, color = "#FF0000", alpha = 0.4)
# p.circle ([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size = 20, color = "#FF0000", alpha = 0.4)
# p.vbar (x = [1, 2, 3], width = 0.5, bottom = 0, top = [1.2, 2.5, 3.7], color = "firebrick")
# p.hbar (y = [1, 2, 3], height = 0.5, left = 0, right = [1.2, 2.5, 3.7], color = "navy")

# # MIX GRAPH
# factors = ["Q1", "Q2", "Q3", "Q4"]
# y = [10, 12, 16, 9]
# p = figure(x_range = factors, plot_height = 250)
# p.vbar(x = factors, top = y, width = 0.9, alpha = 0.5)
# p.line(x = factors, y = [12, 9, 13, 14], color = "red", line_width = 20)
# p.x_range.range_padding = 0.3
# p.y_range.start = 0

# # CATEGORIZE + COLOR:
# fruits = ["Apples", "Pears", "Nectarines", "Plums", "Grapes", "Strawberries"]
# p = figure(x_range = fruits, plot_height = 250, title = "Fruit Counts")
# p.vbar(x = fruits, top = [5, 3, 4, 2, 4, 6], color = Spectral6, width = 0.9)
# p.y_range.start = 0

# # COLUMN DATA SOURCE
# fruits = ["Apples", "Pears", "Nectarines", "Plums", "Grapes", "Strawberries"]
# counts = [5, 3, 4, 2, 4, 6]
# source = ColumnDataSource (data = dict(fruits = fruits, counts = counts, color = Spectral6))
# p = figure(x_range = fruits, y_range = (0, 9), plot_height = 250, title = "Fruit Counts")
# p.vbar(x = 'fruits', top = 'counts', width = 0.9, color = 'color', source = source)

# # FACTOR RANGE
# factors = [   
#     ("Q1", "Jan"), ("Q1", "Feb"), ("Q1", "Mar"),
#     ("Q2", "Jan"), ("Q2", "Feb"), ("Q2", "Mar"),
#     ("Q3", "Jan"), ("Q3", "Feb"), ("Q3", "Mar"),
#     ("Q4", "Jan"), ("Q4", "Feb"), ("Q4", "Mar"),   ]
# p = figure(x_range = FactorRange(*factors), plot_height = 250)
# y = [10, 12, 16, 9, 10, 8, 12, 13, 14, 14, 12, 16]
# p.vbar(x = factors, top = y, width = 0.9, alpha = 0.5)
# p.y_range.start = 0
# p.x_range.range_padding = 0.1
# p.xgrid.grid_line_color = None

# # LEGEND
# fruits = ["Apples", "Pears", "Nectarines", "Plums", "Grapes", "Strawberries"]
# counts = [5, 3, 4, 2, 4, 6]
# source = ColumnDataSource (data = dict(fruits = fruits, counts = counts, color = Spectral6))
# p = figure(x_range = fruits, y_range = (0, 9), plot_height = 250, title = "Fruit Counts", tools = [BoxZoomTool(), ResetTool()])
# p.vbar(x = 'fruits', top = 'counts', width = 0.9, color = 'color', legend = 'fruits', source = source)
# p.legend.orientation = "horizontal"
# p.legend.location = "top_right"

# # LAYOUT - COLUMN & ROW + GRIDPLOT
# x = list(range(11))
# y0 = x
# y1 = [10 - i for i in x]
# y2 = [abs(i - 5) for i in x]
# # plot 1
# s1 = figure (plot_width = 250, plot_height = 250, title = None)
# s1.circle (x, y0, size = 10, color = "navy", alpha = 0.5)
# # plot 2
# s2 = figure (plot_width = 250, plot_height = 250, title = None)
# s2.triangle (x, y1, size = 10, color = "firebrick", alpha = 0.5)
# # plot 3
# s3 = figure (plot_width = 250, plot_height = 250, title = None)
# s3.square (x, y2, size = 10, color = "olive", alpha = 0.5)
# # show w/ row & column
# # show(column(s1, s2, s3))
# # show(row(s1, s2, s3))
# # show w/ grid
# grid = gridplot([[s1], [None, s2], [None, None, s3]])
# show(grid)

# # LINEAR REGRESSION

# # GOOGLE MAP
# map_options = GMapOptions(lat = 25.04, lng = 121.52, map_type = "roadmap", zoom = 12)
# plot = GMapPlot(x_range = Range1d(), y_range = Range1d(), map_options = map_options)
# plot.api_key = "AIzaSyDLR-TU8-NNuuSK7d6IgczGc-kye03wfxg"
# source = ColumnDataSource (
#     data = dict (
#         lat = [25.05, 25.07, 25.09],
#         lng = [121.51, 121.54, 121.53],
#     )
# )
# circle = Circle(x = "lng", y = "lat", size = 25, fill_color = "red", fill_alpha = 0.8, line_color = None)
# plot.add_glyph(source, circle)

# # HOVERTOOL
# source = ColumnDataSource (
#     data = dict (
#         x = [1, 2, 3, 4, 5],
#         y = [2, 5, 8, 2, 7],
#         desc = ['A', 'B', 'C', 'D', 'E'],
#     )
# )
# hover = HoverTool(
#     tooltips = [
#         ("index", "$index"),
#         ("(x, y)", "($x, $y)"),
#         ("desc", "@desc"),
#     ]
# )
# p = figure(plot_width = 400, plot_height = 400, tools = [hover], title = "HOVER")
# p.circle('x', 'y', size = 2, source = source)

# # SLIDE BAR + TEXT INPUT
# x = [x * 0.005 for x in range(0, 200)]
# y = x
# source = ColumnDataSource(data = dict(x = x, y = y))
# plot = figure(plot_width = 400, plot_height = 400)
# plot.line('x', 'y', source = source, line_width = 3, line_alpha = 0.6)
# callback = CustomJS(args = dict(source = source), code = """
#     var data = source.data
#     var f = cb_obj.value
#     x = data['x'] // array
#     y = data['y'] // array
#     for (i = 0; i < x.length; i++) {
#         y[i] = Math.pow(x[i], f)
#     }
#     source.change.emit()
# """)
# # choose one
# slider = Slider(start = 0.1, end = 4, value = 1, step = .01, title = "power")
# slider.js_on_change('value', callback)
# layout = column(slider, plot)
# text_input = TextInput(placeholder = "Input a number from 1-4", value = "1")
# text_input.js_on_change('value', callback)
# layout = column(text_input, plot)

# LASSO SELECT
x = [random() for x in range(500)]
y = [random() for y in range(500)]
color = ["navy"] * len(x)
s = ColumnDataSource(data = dict(x = x, y = y, color = color))
p = figure(plot_width = 400, plot_height = 400, tools = "lasso_select", title = "Select Me")
p.circle ('x', 'y', color = 'color', size = 8, source = s, alpha = 0.4)
s2 = ColumnDataSource(data = dict(x = [0, 1], yline = [0.5, 0.5]))
p.line(x = 'x', y = 'yline', color = "orange", line_width = 5, alpha = 0.6, source = s2)
s.callback = CustomJS(args = dict(s2 = s2), code = """
    var inds = cb_obj.selected['1d'].indices;
    console.log(cb_obj);
    var d = cb_obj.data;
    var yline = 0;
    if (inds.length == 0) { return; }
    for (var i = 0; i < inds.length; i++) {
        d['color'][inds[i]] = "firebrick";
        yline += d['y'][inds[i]];
    }
    yline /= inds.length;
    s2.data['yline'] = [yline, yline]
    cb_obj.change.emit();
    s2.change.emit();
""")

show(p)
# show(plot)
# show(layout)
# output_notebook()
output_file("figure.html")
