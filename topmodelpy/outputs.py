"""Module of functions for generating output files and plots.

"""

import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpld3
import os
from pathlib import Path
from textwrap import wrap


COLORS = {
    "temperature": "orange",
    "precipitation": "SkyBlue",
    "flow_predicted": "blue",
}


class MousePositionDatePlugin(mpld3.plugins.PluginBase):
    """Plugin for displaying mouse position with a datetime x axis."""

    JAVASCRIPT = """
    mpld3.register_plugin("mousepositiondate", MousePositionDatePlugin);
    MousePositionDatePlugin.prototype = Object.create(mpld3.Plugin.prototype);
    MousePositionDatePlugin.prototype.constructor = MousePositionDatePlugin;
    MousePositionDatePlugin.prototype.requiredProps = [];
    MousePositionDatePlugin.prototype.defaultProps = {
    fontsize: 12,
    xfmt: "%Y-%m-%d %H:%M:%S",
    yfmt: ".2f"
    };
    function MousePositionDatePlugin(fig, props) {
    mpld3.Plugin.call(this, fig, props);
    }
    MousePositionDatePlugin.prototype.draw = function() {
    var fig = this.fig;
    var xfmt = d3.time.format(this.props.xfmt);
    var yfmt = d3.format(this.props.yfmt);
    var coords = fig.canvas.append("text").attr("class", "mpld3-coordinates").style("text-anchor", "end").style("font-size", this.props.fontsize).attr("x", this.fig.width - 5).attr("y", this.fig.height - 5);
    for (var i = 0; i < this.fig.axes.length; i++) {
      var update_coords = function() {
        var ax = fig.axes[i];
        return function() {
          var pos = d3.mouse(this);
          x = ax.xdom.invert(pos[0]);
          y = ax.ydom.invert(pos[1]);
          coords.text("(" + xfmt(x) + ", " + yfmt(y) + ")");
        };
      }();
      fig.axes[i].baseaxes.on("mousemove", update_coords).on("mouseout", function() {
        coords.text("");
      });
    }
    };
    """

    def __init__(self, fontsize=14, xfmt="%Y-%m-%d %H:%M:%S", yfmt=".2f"):
        self.dict_ = {
            "type": "mousepositiondate",
            "fontsize": fontsize,
            "xfmt": xfmt,
            "yfmt": yfmt
        }


def plot_timeseries_html(dates, values, name, units):
    """Return an html string of the figure"""

    # instantiate figure
    fig, ax = plt.subplots(subplot_kw=dict(axisbg="#EEEEEE"))
    fig.set_size_inches(12, 10)

    # colors
    if COLORS.get(name):
        colorstr = COLORS.get(name)
    else:
        colorstr = "k"

    # labels
    ax.grid(color="white", linestyle="solid")
    ax.set_title("{0} ({1})".format(name, units), fontsize=20)

    # plot
    line = ax.plot(dates, values, color=colorstr, linewidth=2)

    # connect plugin
    mpld3.plugins.connect(fig, MousePositionDatePlugin())

    return mpld3.fig_to_html(fig)


def plot_timeseries(dates, values, mean, max, min, name, units, path=""):
    """Show and optionally save plot."""

    # instantiate figure
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 10)

    # labels
    ax.grid()
    ax.set_title("{0} ({1})".format(name, units))
    ax.set_xlabel("Date")
    ax.set_ylabel("{0}\n({1})".format(name, wrap(units, 60)[0]))

    # colors
    if COLORS.get(name):
        colorstr = COLORS.get(name)
    else:
        colorstr = "k"

    # plot
    line = ax.plot(dates, values, linewidth=2, color=colorstr)

    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")

    # show text of mean, max, min values
    text = "mean = {0:>#0.2f}\nmax = {1:>#0.2f}\nmin = {2:>#0.2f}".format(mean,
                                                                          max,
                                                                          min)
    patch_properties = {
        "boxstyle": "round",
        "facecolor": "wheat",
        "alpha": 0.5
    }
    ax.text(0.05,
            0.95,
            text,
            transform=ax.transAxes,
            fontsize=14,
            verticalalignment="top",
            horizontalalignment="left",
            bbox=patch_properties)

    # save or show
    if path:
        plt.savefig(path)
    else:
        plt.show()


def write_timeseries_csv(path, filename, fieldnames, units, dates, data):
    """Writes a csv file of a timeseries of data.

    """

    fullpath = os.path.join(path, filename)

    rows = []
    for i in range(len(dates)):
        row = []
        row.append(dates[i].strftime("%Y-%m-%d"))
        for key in data.keys():
            row.append("{:.9f}".format(data[key][i]))

        rows.append(row)

    with open(fullpath, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fieldnames)
        writer.writerow(units)
        writer.writerows(rows)


def write_timeseries_twi_bin_based_csv(path,
                                       filename,
                                       fieldnames,
                                       units,
                                       dates,
                                       data,
                                       num_twi_bins):
    """Writes a csv file of a timeseries of data based on twi bins.

    Writes a csv file of a timeseries of data based on twi bins, meaning
    for each timestamp, the row contains data values for each twi increments.
    For example, if the twi data has 30 bins, then each timestamp row will have
    30 data values.

    Used for:
      - saturation deficit local
      - root zone storage
      - unsaturated zone storage

    Parameters
    ----------
    path : str
        Path to write
    filename : str
        Filename to write
    dates : np.ndarray
        Array of datetimes
    twi_bins : np.ndarray
        Array of twi bins
    fieldname : str
        Fieldname to write
    data : np.ndarray
        Multidimenstional array of data:
            nrows = len(dates)
            ncols = len(twi_bins)

    """

    fullpath = os.path.join(path, filename)

    rows = []
    for i in range(len(dates)):
        row = []
        row.append(dates[i].strftime("%Y-%m-%d"))
        for j in range(len(data[i])):
            row.append("{:.2f}".format(data[i][j]))

        rows.append(row)

    with open(fullpath, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fieldnames)
        writer.writerow(units)
        writer.writerows(rows)
