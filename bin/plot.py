#!/usr/bin/env python3

import pygal
from pygal.style import Style

import glob
import os
import sys
import time
import csv

# globals
image_dir = "../images"

class CustomStyle(Style):
    """A light style with strong colors"""
    background = '#FFFFFF'
    plot_background = '#FFFFFF'
    foreground = '#000000'
    foreground_strong = '#000000'
    foreground_subtle = '#828282'
    opacity = '.8'
    opacity_hover = '.9'
    transition = '100ms'
    colors = ('#FFD000', '#345995', '#01A337', '#ED2B1A')

    label_font_size = 18
    major_label_font_size = 20
    value_font_size = 22
    value_label_font_size = 20
    tooltip_font_size = 20
    title_font_size = 24
    legend_font_size = 20
    no_data_font_size = 64

# helpers
def sat(point):
    return "sat" in point[2] and "unsat" not in point[2]

def unsat(point):
    return "unsat" in point[2]

def error(point):
    return "error" in point[2]

def timeout(point):
    return "timeout" in point[2]

def unknown(point):
    return "unknown" in point[2]

def sat_unsat(point):
    return sat(point) or unsat(point)

def get_category_data(data):
    category_data = {}
    for solver, points in sorted(data.items()):
        for point in points:
            cat = point[0].rsplit('/', 1)[-1]
            if cat in category_data:
                if solver in category_data[cat]:
                    category_data[cat][solver].append(point)
                else:
                    category_data[cat][solver] = [point]
            else:
                category_data[cat] = {}
    return category_data

def plot_cacti(data):
    overall = get_cactus(data, "SAT/UNSAT Cactus: Overall (%s)" %(time.strftime("%d/%m/%Y")))
    overall.render_to_file("%s/%s"%(image_dir, "overall_cactus.svg"))
    category_data = get_category_data(data)
    for category, cat_data in sorted(category_data.items()):
        cactus = get_cactus(cat_data, "SAT/UNSAT Cactus: %s" %(category.upper()))
        cactus.render_to_file("%s/%s"%(image_dir, "%s_cactus.svg" % category))

def get_cactus(data, title):
    cactus = pygal.XY(stroke=False, title=title, y_title="Time (s)", dots_size=5, tooltip_border_radius=10, style=CustomStyle, legend_at_bottom=True, legend_at_bottom_columns=4)
    for solver, points in sorted(data.items()):
        points = [p for p in sorted(points, key=lambda x: x[-1]) if sat_unsat(p)]
        points = zip(range(len(points)), points)
        points = [{'value': (i, p[-1]), 'label': "%s: %s"%(p[1], p[-2]), 'xlink':"%s/%s"%(p[0], p[1])} for (i, p) in points]
        cactus.add(solver, points)
    return cactus

def plot_bars(data):
    overall = get_bar(data, "Result Distribution: Overall (%s)" %(time.strftime("%d/%m/%Y")))
    overall.render_to_file("%s/%s"%(image_dir, "overall_bar.svg"))
    category_data = get_category_data(data)
    for category, cat_data in sorted(category_data.items()):
        bar = get_bar(cat_data, "Result Distribution: %s" %(category.upper()))
        bar.render_to_file("%s/%s"%(image_dir, "%s_bar.svg" % category))

def get_bar(data, title):
    overall = pygal.Bar(title=title, tooltip_border_radius=10, style=CustomStyle, legend_at_bottom=True, legend_at_bottom_columns=4)
    overall.x_labels = ["SAT", "UNSAT", "UNKNOWN", "TIMEOUT", "ERROR"]
    totals = {}
    for solver, points in sorted(data.items()):
        if solver not in totals:
            totals[solver] = [0,0,0,0,0]
        for point in points:
            if sat(point):
                totals[solver][0] += 1
            elif unsat(point):
                totals[solver][1] += 1
            elif unknown(point):
                totals[solver][2] += 1
            elif timeout(point):
                totals[solver][3] += 1
            elif error(point):
                totals[solver][4] += 1
    for solver, vals in sorted(totals.items()):
        overall.add(solver, vals)
    return overall

def plot_time_for_model(data):
    solver_data = {}
    for solver, points in sorted(data.items()):
        if solver not in solver_data:
            solver_data[solver] = []
        for psat in points:
            if sat(psat):
                if "model" not in psat[1]:
                    category = psat[0]
                    name = psat[1][:-len(".smt25")]+ "-model.smt25"
                    tsat = psat[-1]
                    for pmodel in points:
                        if pmodel[1] == name:
                            if not error(pmodel):
                                tmodel = pmodel[-1]
                                solver_data[solver].append([tsat, tmodel, category, name])
                            break

    cactus = pygal.XY(stroke=False, title="Get-Sat Vs. Get-Model by Instance", x_title="Get-Sat (s)", y_title="Get-Model (s)", dots_size=5, tooltip_border_radius=10, style=CustomStyle, legend_at_bottom=True, legend_at_bottom_columns=4)
    for solver, points in sorted(solver_data.items()):
        points = [{'value': (p[0], p[1]), 'label': p[-1], 'xlink':"%s/%s"%(p[2], p[3])} for p in points]
        cactus.add(solver, points)
    cactus.render_to_file("%s/%s"%(image_dir, "models_dots.svg"))

    overall = pygal.Bar(title="Get-Sat Vs. Get-Model Average", y_title="Time (s)", tooltip_border_radius=10, style=CustomStyle, legend_at_bottom=True, legend_at_bottom_columns=4)
    overall.x_labels = ["Get-Sat", "Get-Model"]
    for solver, points in sorted(solver_data.items()):
        number = len(points)
        tsat = sum([p[0] for p in points])/float(number)
        tmodel = sum([p[1] for p in points])/float(number)
        overall.add(solver, [tsat, tmodel])
    overall.render_to_file("%s/%s"%(image_dir, "models_bars.svg"))

def main():
    global image_dir

    # get args
    results_dir = sys.argv[1]
    image_dir   = sys.argv[2]

    # get result files
    results_glob = os.path.join(results_dir, "*.csv")
    result_files = glob.glob(results_glob)

    points = {}

    # generate data
    for result in result_files:
        solver = os.path.basename(result)[:-len(".csv")]
        with open(result, "r") as data:
            reader = csv.reader(data)
            next(reader, None) #skip header
            for row in reader:
                point = row[:-1] + [float(row[-1])]
                if solver in points:
                    points[solver].append(point)
                else:
                    points[solver] = [point]

    # generate graphs
    plot_cacti(points)
    plot_bars(points)
    # plot_time_for_model(points)

if __name__ == '__main__':
    main()
