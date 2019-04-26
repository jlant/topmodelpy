"""Module that contains functions to render an html file.

"""

from jinja2 import PackageLoader, Environment


def render_report(data):
    """Render an html page of the model output data.

    :param data: Data to fill template with
    :param type: dictionary
    :param template_filename: The filename of the template to fill
    :type template_filename: string
    """
    loader = PackageLoader("topmodelpy", "templates")
    env = Environment(loader=loader)
    template = env.get_template("report_template.html")

    return template.render(data=data)


def save(data, filename):
    """Save summary as a restructured text file.

    :param data: Data to fill template with
    :param type: dictionary
    :param filename: The full path with filename of the output file to write
    :type filename: string
    """
    with open(filename, "w") as f:
        f.write(render_report(data))

