"""temp file to generate a large test file."""

import json
import sys

from rich.progress import track
from datetime import datetime as dt

from next_task.services import models

data_file = "tests/data_mocks/performance_small/.tasks.json"

def generate():
    data = models.TemplateTaskFile().__dict__
    for n in track(range(1, 301), description="Generating Tasks..."):
        data["task_count"] = n
        summary = f"Task Itteration {n}"
        data["tasks"].append(models.Task(n, summary, dt.now()).__dict__)
    
    with open(data_file, "w+") as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    sys.exit(generate())
