# Load environment variables
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(
    dotenv_path=Path(__file__).resolve().parent / ".env"
)

from .quant.polars_accessors import *
from . import data
from . import charts
from . import quant
