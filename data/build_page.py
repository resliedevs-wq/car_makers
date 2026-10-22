"""Inject data/cars2025.json into web/template.html -> web/index.html."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = open(os.path.join(ROOT, "data", "cars2025.json")).read().replace("</", "<\\/")
page = open(os.path.join(ROOT, "web", "template.html")).read().replace("__DATA__", data)
open(os.path.join(ROOT, "web", "index.html"), "w").write(page)
print("web/index.html", len(page), "bytes")
