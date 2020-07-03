import logging
import os
import pymel.core as pmc
from pymel.core.system import Path


log = logging.getLogger(__name__)


class SceneFile(object):
	"""Class used to represent a DCC software scene file

	The class will be a conventient object that we can use to manipulate our scene files.
	Examples features include the ability to predefine our naming conventions and automatically increment.

	Attributes:
		dir (Path, optional): Directory to the scene file. Defaults to ''.
		descriptor (str, optional): Short descriptor of the scene file. Defaults to "main".
		version (int, optional): Version number. Defaults to 1.
		ext (str, optional): Extension. Defaults to "ma"

	"""
	def __init__(self, dir='', descriptor='main', version=1, ext='ma'):
		if pmc.system.isModified():
		    self._dir = Path(dir)
		    self.descriptor = descriptor
		    self.version = version
		    self.ext = ext
		else:
		    current_path = Path(pmc.system.sceneName())
		    self.dir = current_path.parent
		    file_name = current_path.name
		    try:
		        self.descriptor = file_name.split("_v")[0]
		        file_version = file_name.split("_v")[1]
		        file_version_final = file_version.split(".")[0]
		        self.version = int(file_version_final)
		        self.ext = file_version.split(".")[1]
		    except IndexError:
		        self.descriptor = file_name.split("_")[0]
		        file_version = file_name.split("_")[1]
		        file_version_final = file_version.split(".")[0]
		        self.version = int(file_version_final)
		        self.ext = file_version.split(".")[1]

	@property
	def dir(self):
		return self._dir

	@dir.setter
	def dir(self, val):
		self._dir = Path(val)

	def basename(self):
		"""Return a scene file name.

		e.g. ship_001.ma, car_011.hip

		Returns:
			str: The name of the scene file.

		"""
		v = 'v'
		name_pattern = "{descriptor}_{let}{version:03d}.{ext}"
		name = name_pattern.format(descriptor=self.descriptor,
								   let=v,
								   version=self.version,
								   ext=self.ext)
		return name

	def path(self):
		"""The functions returns a path to scene file.

		This includes the drive letter, any directory path and the file name.

		Returns:
			Path: The path to the scene file.

		"""

		return Path(self.dir) / self.basename()

	def save(self):
		"""Saves the scene file

		Returns:
			:obj: 'Path': THe path to the scene file if successful, None, otherwise.

		"""
		try:
			pmc.system.saveAs(self.path())
		except RuntimeError:
			log.warning("Missing directories. Attempting to create directories.")
			self.dir.makedirs_p()
			pmc.system.saveAs(self.path())

			print("File Saved Successfully!")

	def increment_and_save(self):
		"""Checks to see if existing version of file exist, if so then it should
		increment and save from the largest version in file. If not, then save the scene file.
		"""

		file_list = pmc.getFileList(folder=self.dir)

		scene_list = list()
		for file in file_list:
			    file_path = Path(file)
			    scene = file_path.name
			    scene_list.append(scene)

		top_version = self.version
		try:
		    for scene in scene_list:
			        descriptor = scene.split("_v")[0]

			        if descriptor == self.descriptor:
			    	        version_name = scene.split("_v")[1]
			    	        version_name_final = version_name.split(".")[0]
			    	        version = int(version_name_final)

			    	        if version > self.version:
			    	    	    top_version = version
		except IndexError:
		    for scene in scene_list:
			        descriptor = scene.split("_")[0]

			        if descriptor == self.descriptor:
			    	        version_name = scene.split("_")[1]
			    	        version_name_final = version_name.split(".")[0]
			    	        version = int(version_name_final)

			    	        if version > self.version:
			    	    	    top_version = version
		self.version = top_version + 1
		self.save()
			