# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QFileDialog, QWidget

from dial_core.project import ProjectManager
from dial_core.utils import log

from .project_gui import ProjectGUI

LOGGER = log.get_logger(__name__)


class ProjectManagerGUI(QObject, ProjectManager):
    new_project_added = Signal(ProjectGUI)

    def __init__(self, default_project: "ProjectGUI", parent=None):
        QObject.__init__(self, parent)
        ProjectManager.__init__(self, default_project)

    def add_project(self, project: "ProjectGUI"):
        super().add_project(project)

        self.new_project_added.emit(project)

    @Slot()
    def open_project(self):
        LOGGER.debug("Opening dialog for pickling a file...")

        file_path = QFileDialog.getOpenFileName(
            QWidget(), "Open Dial project", "~", "Dial Files (*.dial)"
        )[0]

        LOGGER.info("File path selected for opening: %s", file_path)

        if file_path:
            super().open_project(file_path)
        else:
            LOGGER.info("Invalid file path. Loading cancelled.")

    @Slot()
    def save_project(self):
        try:
            super().save_project()

        except ValueError:
            LOGGER.warning("Project doesn't have a file path set!")

            self.save_project_as()

    @Slot()
    def save_project_as(self):
        LOGGER.debug("Opening dialog for picking a save file...")

        selected_file_path = QFileDialog.getSaveFileName(
            QWidget(), "Save Dial project", "~", "Dial Files (*.dial)"
        )[0]

        LOGGER.info("File path selected for saving: %s", selected_file_path)

        if selected_file_path:
            super().save_project_as(selected_file_path)

        else:
            LOGGER.info("Invalid file path. Saving cancelled.")
