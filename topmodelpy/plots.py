"""Module of functions for generating plots.

"""

from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpld3
import numpy as np
from scipy import stats
from textwrap import wrap


COLORS = {
    "temperature": "orange",
    "precipitation": "SkyBlue",
    "flow_observed": "gray",
    "flow_predicted": "blue",
    "saturation_deficit_avgs": "black",
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

    fig, ax = plt.subplots(subplot_kw=dict(axisbg="#EEEEEE"))
    fig.set_size_inches(12, 10)

    if COLORS.get(name):
        colorstr = COLORS.get(name)
    else:
        colorstr = "k"

    ax.grid(color="white", linestyle="solid")
    ax.set_title("{0} ({1})".format(name, units), fontsize=20)

    ax.plot(dates, values, color=colorstr, linewidth=2)

    # Connect plugin
    mpld3.plugins.connect(fig, MousePositionDatePlugin())

    return mpld3.fig_to_html(fig)


def plot_timeseries(dates, values, label, filename):
    """Plot timeseries."""

    fig, ax = plt.subplots()
    fig.set_size_inches(12, 10)

    label = label.replace("_", " ").capitalize()

    ax.grid()
    ax.set_title(label)
    ax.set_xlabel("Date")
    ax.set_ylabel(label)

    for key, value in COLORS.items():
        if label in key:
            colorstr = value
        else:
            colorstr = "k"

    ax.plot(dates, values, linewidth=2, color=colorstr)

    # Rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")

    # Add text of descriptive stats to figure
    mean = np.round(np.mean(values), 2)
    median = np.round(np.median(values), 2)
    mode = np.round(stats.mode(values)[0][0], 2)
    max = np.round(np.max(values), 2)
    min = np.round(np.min(values), 2)

    text = (
        "mean = {0}\n"
        "median = {1}\n"
        "mode = {2}\n"
        "max = {3}\n"
        "min = {4}\n"
        "".format(mean, median, mode, max, min)
    )

    patch_properties = {
        "boxstyle": "round",
        "facecolor": "white",
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

    plt.savefig(filename, format="png")
