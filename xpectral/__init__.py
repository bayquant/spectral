#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from pathlib import Path

# Other imports
from dotenv import load_dotenv
from . import charts
from . import data
from . import quant

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

load_dotenv(
    dotenv_path=Path(__file__).resolve().parent / ".env"
)
