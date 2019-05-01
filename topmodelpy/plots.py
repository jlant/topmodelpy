"""Module of functions for generating plots.

"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mpld3
from pandas.plotting import register_matplotlib_converters
import numpy as np
from scipy import stats

from topmodelpy import hydrocalcs


# Register for pandas
register_matplotlib_converters()

COLORS = {
    "temperature": "orange",
    "precipitation": "navy",
    "pet": "green",
    "precip_minus_pet": "darkgreen",
    "flow_observed": "darkblue",
    "flow_predicted": "blue",
    "saturation_deficit_avgs": "gray",
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


def plot_timeseries_html(dates, values, label):
    """Return an html string of the figure"""

    fig, ax = plt.subplots(subplot_kw=dict(facecolor="#EEEEEE"))
    fig.set_size_inches(10, 6)

    colorstr = "k"
    for key, value in COLORS.items():
        if key in label:
            colorstr = value

    label = label.replace("_", " ").capitalize()

    ax.grid(color="white", linestyle="solid")
    ax.set_title("{}".format(label), fontsize=20)

    ax.plot(dates, values, color=colorstr, linewidth=2)

    # Connect plugin
    mpld3.plugins.connect(fig, MousePositionDatePlugin())

    return mpld3.fig_to_html(fig)


def plot_timeseries_comparison_html(dates, observed, modeled, absolute_error, label):
    """Return an html string of the figure"""

    fig, axes = plt.subplots(2, 1, sharex=True, subplot_kw=dict(facecolor="#EEEEEE"))
    fig.set_size_inches(10, 8)

    # Connect plugin
    mpld3.plugins.connect(fig, MousePositionDatePlugin())

    # Plot comparison on first row
    axes[0].grid(True)
    axes[0].set_title("Observed flow vs. Modeled flow")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel(label)

    # Explicitly using matplotlibs new default color palette (blue and orange)
    axes[0].plot(dates, observed, linewidth=2, color="#1f77b4",
                 label="Observed")
    axes[0].plot(dates, modeled, linewidth=2, color="#ff7f0e",
                 label="Modeled")

    # Legend
    handles, labels = axes[0].get_legend_handles_labels()
    legend = axes[0].legend(handles, labels, fancybox=True)
    legend.get_frame().set_alpha(0.5)

    axes[1].plot(dates, absolute_error, linewidth=2, color="black")

    # Rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    axes[1].fmt_xdata = mdates.DateFormatter("%Y-%m-%d")

    return mpld3.fig_to_html(fig)


def plot_timeseries(dates,
                    values,
                    mean,
                    median,
                    mode,
                    max,
                    min,
                    label,
                    filename):
    """Plot timeseries."""
    fig, ax = plt.subplots()
    fig.set_size_inches(12, 10)

    colorstr = "k"
    for key, value in COLORS.items():
        if key in label:
            colorstr = value

    label = label.replace("_", " ").capitalize()

    ax.grid()
    ax.set_title(label)
    ax.set_xlabel("Date")
    ax.set_ylabel(label)

    ax.plot(dates, values, linewidth=2, color=colorstr)

    # Rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    ax.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")

    # Add text of descriptive stats to figure
    text = (
        "Mean = {0:.2f}\n"
        "Median = {1:.2f}\n"
        "Mode = {2:.2f}\n"
        "Max = {3:.2f}\n"
        "Min = {4:.2f}"
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


def plot_timeseries_comparison(dates,
                               observed,
                               modeled,
                               absolute_error,
                               nash_sutcliffe,
                               mean_squared_error,
                               label,
                               filename):
    """Plot difference between timeseries."""

    fig, axes = plt.subplots(2, 1, sharex=True)
    fig.set_size_inches(12, 10)

    label = label.replace("_", " ").capitalize()

    # Plot comparison on first row
    axes[0].grid(True)
    axes[0].set_title("Observed flow vs. Modeled flow")
    axes[0].set_xlabel("Date")
    axes[0].set_ylabel(label)

    # Explicitly using matplotlibs new default color palette (blue and orange)
    axes[0].plot(dates, observed, linewidth=2, color="#1f77b4",
                 label="Observed")
    axes[0].plot(dates, modeled, linewidth=2, color="#ff7f0e",
                 label="Modeled")

    # Legend
    handles, labels = axes[0].get_legend_handles_labels()
    legend = axes[0].legend(handles, labels, fancybox=True)
    legend.get_frame().set_alpha(0.5)

    # Add text of stats to figure
    text_nash_sutcliffe = (
        "Nash-Sutcliffe = {:.2f}"
        "".format(nash_sutcliffe)
    )

    patch_properties = {
        "boxstyle": "round",
        "facecolor": "white",
        "alpha": 0.5
    }

    axes[0].text(0.05,
                 0.95,
                 text_nash_sutcliffe,
                 transform=axes[0].transAxes,
                 fontsize=14,
                 verticalalignment="top",
                 horizontalalignment="left",
                 bbox=patch_properties)

    # Plot absolute error on second row
    axes[1].grid(True)
    axes[1].set_title("Absolute Error: Observed - Modeled")
    axes[1].set_xlabel("Date")
    axes[1].set_ylabel("Error (mm/day)")

    axes[1].plot(dates, absolute_error, linewidth=2, color="black")

    # Rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    axes[1].fmt_xdata = mdates.DateFormatter("%Y-%m-%d")

    # Add text of stats to figure
    text_mse = (
        "Mean Squared Error = {:.2f}"
        "".format(mean_squared_error)
    )

    axes[1].text(0.05,
                 0.95,
                 text_mse,
                 transform=axes[1].transAxes,
                 fontsize=14,
                 verticalalignment="top",
                 horizontalalignment="left",
                 bbox=patch_properties)

    plt.savefig(filename, format="png")
