from .base import *
from .security import *
from .static import *
from .mail import *
from .celery_settings import *
from .spider import *
# from .misc import *

# Load a `local.py` module, if it exists
try:
    from .local import *
except ImportError:
    pass
