# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
"""
Functions to check that python versions, libraries... used by the program are correct.
"""


import signal
import sys
from typing import TYPE_CHECKING

import dial_core
from dial_core.utils import log

if TYPE_CHECKING:
    import argparse


LOGGER = log.get_logger(__name__)


def initialize(args: "argparse.Namespace"):
    """Performs all the necessary steps before running the application. This checks
    python version, installed modules, graphics configurations, initialize logging
    system...

    Raises:
        ImportError: If couldn't import a necessary module.
        SystemError: If the Python version isn't compatible.
    """
    try:

        dial_core.utils.initialization.initialize(args)
        __gui_initialization(args)

    except (ImportError, SystemError) as err:
        LOGGER.exception(err)

        from dial_gui.utils import tkinter as dial_tkinter

        dial_tkinter.showerror(str(err))
        sys.exit(1)


def __gui_initialization(args: "argparse.Namespace"):
    """Performs all the initialization of the GUI components.

    Args:
        args: App configuration namespace."""
    # State the signals handled by this application
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Initialize PySide2
    from PySide2.QtWidgets import QApplication

    app = QApplication()
    app.setApplicationName("dial")
