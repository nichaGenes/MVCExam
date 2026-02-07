from pathlib import Path
from fastapi.templating import Jinja2Templates
from datetime import date, datetime

def format_date(value, format_string='%d/%m/%Y'):
    if value is None:
        return ""
    if isinstance(value, (date, datetime)):
        return value.strftime(format_string)
    return str(value)

# Setup templates with correct directory
templates = Jinja2Templates(directory=Path(__file__).parent / "views")

# Register the custom filter
templates.env.filters["strftime"] = format_date
