"""
Generic utility helper functions
================================

.. autosummary::
    ~running_in_queueserver
    ~debug_python
    ~mpl_setup
    ~is_notebook
"""

import logging

from bluesky_queueserver import is_re_worker_active
from IPython import get_ipython

from ..configs.loaders import iconfig

logger = logging.getLogger(__name__)
logger.info(__file__)


def running_in_queueserver():
    """Detect if running in the bluesky queueserver."""
    try:
        active = is_re_worker_active()
        # print(f"{active=!r}")
        return active
    except Exception as cause:
        print(f"{cause=}")
        return False


def debug_python():
    """"""
    # terse error dumps (Exception tracebacks)
    _ip = get_ipython()
    if _ip is not None:
        _xmode_level = iconfig.get("XMODE_DEBUG_LEVEL", "Minimal")
        _ip.run_line_magic("xmode", _xmode_level)
        logger.info("xmode exception level: '%s'", _xmode_level)


def is_notebook():
    """
    Detect if running in a notebook.

    see: https://stackoverflow.com/a/39662359/1046449
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)

    except NameError:
        return False  # Probably standard Python interpreter


def mpl_setup():
    """
    MatPlotLib setup.
    """
    if not running_in_queueserver():
        import matplotlib.pyplot as plt

        if not is_notebook():
            plt.ion()
