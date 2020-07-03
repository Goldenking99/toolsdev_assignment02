import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance

import mayautils

def maya_main_window():
	"""Return the maya main window widget"""
	main_window = omui.MQtUtil.mainWindow()
	return wrapInstance(long(main_window), QtWidgets.QWidget)


class SmartSaveUI(QtWidgets.QDialog):
	""" Smart Save UI class """

	def __init__(self):
		"""Constructor"""
		# Passing the object SmartSaveUI as an argument to super()
		# makes this line python 2 and 3 compatible
		super(SmartSaveUI, self).__init__(parent=maya_main_window())
		self.scene = mayautils.SceneFile()

		self.setWindowTitle("SmartSaveUI")
		self.resize(500,200)
		self.setWindowFlags(self.windowFlags() ^
							QtCore.Qt.WindowContextHelpButtonHint)
		self.create_widgets()
		self.create_layout()
		self.create_connections()

	def create_widgets(self):
		"""Create widgets for our UI"""
		self.title_lbl = QtWidgets.QLabel("Smart Save UI")
		self.title_lbl.setStyleSheet("font: bold 40px")

		self.dir_lbl = QtWidgets.QLabel("Directory")
		self.dir_le = QtWidgets.QLineEdit()
		self.dir_le.setText(self.scene.dir)
		self.dir_le.setText(self.scene.dir)

		self.browse_btn = QtWidgets.QPushButton("Browse...")

		self.descriptor_lbl = QtWidgets.QLabel("Descriptor")
		self.descriptor_le = QtWidgets.QLineEdit()
		self.descriptor_le.setText(self.scene.descriptor)

		self.version_lbl = QtWidgets.QLabel("Version")
		self.version_spinbox = QtWidgets.QSpinBox()
		self.version_spinbox.setValue(self.scene.version)

		self.ext_lbl = QtWidgets.QLabel("Extension")
		self.ext_le = QtWidgets.QLineEdit()
		self.ext_le.setText(self.scene.ext)

		self.save_btn = QtWidgets.QPushButton("Save")
		self.increment_save_btn = QtWidgets.QPushButton("Increment and Save")
		self.cancel_btn = QtWidgets.QPushButton("Cancel")

	def create_layout(self):
		"""Lay out our widgets in the UI"""

		"""Directory Layout"""
		self.directory_lay = QtWidgets.QHBoxLayout()
		self.directory_lay.addWidget(self.dir_lbl)
		self.directory_lay.addWidget(self.dir_le)
		self.directory_lay.addWidget(self.browse_btn)

		"""Descriptor Layout"""
		self.descriptor_lay = QtWidgets.QHBoxLayout()
		self.descriptor_lay.addWidget(self.descriptor_lbl)
		self.descriptor_lay.addWidget(self.descriptor_le)

		"""Version Layout"""
		self.version_lay = QtWidgets.QHBoxLayout()
		self.version_lay.addWidget(self.version_lbl)
		self.version_lay.addWidget(self.version_spinbox)

		"""Extension Layout"""
		self.ext_lay = QtWidgets.QHBoxLayout()
		self.ext_lay.addWidget(self.ext_lbl)
		self.ext_lay.addWidget(self.ext_le)


		"""Bottom Button Layout"""
		self.bottom_btn_lay = QtWidgets.QHBoxLayout()
		self.bottom_btn_lay.addWidget(self.increment_save_btn)
		self.bottom_btn_lay.addWidget(self.save_btn)
		self.bottom_btn_lay.addWidget(self.cancel_btn)

		"""Main layout (Window elements arrangement should adhere to this order"""
		self.main_layout = QtWidgets.QVBoxLayout()
		self.main_layout.addWidget(self.title_lbl)
		self.main_layout.addLayout(self.directory_lay)
		self.main_layout.addLayout(self.descriptor_lay)
		self.main_layout.addLayout(self.version_lay)
		self.main_layout.addLayout(self.ext_lay)

		"""Stretch space between above Elements and below Elements"""
		self.main_layout.addStretch()

		"""Bottom Button Layout"""
		self.main_layout.addLayout(self.bottom_btn_lay)
		self.setLayout(self.main_layout)

	def create_connections(self):
		"""Connect our widgets signals to slots"""
		self.cancel_btn.clicked.connect(self.cancel)
		self.save_btn.clicked.connect(self.save)
		self.increment_save_btn.clicked.connect(self.increment_save)
		self.browse_btn.clicked.connect(self.browse)

	def _populate_scenefile_properties(self):
		"""Populates the SceneFile object's properties from the UI"""
		self.scene.dir = self.dir_le.text()
		self.scene.descriptor = self.descriptor_le.text()
		self.scene.version = self.version_spinbox.value()
		self.scene.ext = self.ext_le.text()

	@QtCore.Slot()
	def cancel(self):
		"""Quits the dialog"""

		self.close()

	@QtCore.Slot()
	def increment_save(self):
		"""Automatically finds the next available version on disk and saves up."""
		self._populate_scenefile_properties()
		self.scene.increment_and_save()

	@QtCore.Slot()
	def save(self):
		"""Saves the scene file"""
		self._populate_scenefile_properties()
		self.scene.save()

	@QtCore.Slot()
	def browse(self):
		"""Browses the directory using File Explorer"""
		browse_dir = str(QtWidgets.QFileDialog.getExistingDirectory())

		if not browse_dir == "":
			    self.dir_le.setText(browse_dir)