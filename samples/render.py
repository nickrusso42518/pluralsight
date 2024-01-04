from jinja2 import Environment, FileSystemLoader
import csv

j2_env = Environment(
    loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
)
template = j2_env.get_template("template.j2")

with open("ps-clips.csv") as handle:
    rows = csv.reader(handle)
    for row in rows:
        output = template.render(data=row)
        print(60 * "-")
        print(output)
