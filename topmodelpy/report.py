"""Module that contains functions to render an html file.

"""

from jinja2 import PackageLoader, Environment


def render_report(df, plots, comparison_data, flow_duration_curve_data, filename):
    """Render an html page of the model output data.

    :param data: Data to fill template with
    :param type: dictionary
    :param template_filename: The filename of the template to fill
    :type template_filename: string
    """
    loader = PackageLoader("topmodelpy", "templates")
    env = Environment(loader=loader)
    template = env.get_template("report_template.html")

    return template.render(df=df,
                           plots=plots,
                           comparison_data=comparison_data,
                           flow_duration_curve_data=flow_duration_curve_data)


def save(df, plots, comparison_data, flow_duration_curve_data, filename):
    """Save summary as a restructured text file.

    :param data: Data to fill template with
    :param type: dictionary
    :param filename: The full path with filename of the output file to write
    :type filename: string
    """
    with open(filename, "w") as f:
        f.write(
            render_report(df, plots, comparison_data, flow_duration_curve_data, filename)
        )
