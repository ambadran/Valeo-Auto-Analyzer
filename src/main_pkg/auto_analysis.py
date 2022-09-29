'''
A Script to automate the analysis of C files.

This Script does three things:
	1- Reads WorkItems from Polarian outputed as CSV files (WorkItem classes)
	2- Analyse the C file (Block_template classes)
	3- Exports Data

The Analysis step is made of 6 steps:
	1- Code Function Coverage Analysis
	2- Dead Code Analysis
	3- Code Switches Analysis
	4- Code Comment Analysis
	5- Detailed Design Analysis
	6- Code Review
'''


########################################################################################################################################
# File Attributes
__all__ = ['read_assign_all_CSVs', 'create_blocks', 'Component', 'set_wanted_directory', 'export_csv', 'GoogleSheet']
__author__ = 'AbdulRahman Mohsen Badran'
__version__ = '1.0.0'

########################################################################################################################################



########################################################################################################################################
###### imports ######

### Standard Library Modules
import csv
import os
from typing import List, Tuple, Dict
from abc import ABC, abstractmethod
from dataclasses import dataclass
import re
from pathlib import Path
from copy import deepcopy
import pickle
from zipfile import ZipFile
import subprocess
import json
from pprint import pprint

### 3rd party library modules
# html2text
try:
	from html2text import html2text
except ModuleNotFoundError:
	print("\n\n Module 'html2text' not installed, Commencing the installation!\n\n")
	os.system('pip3 install html2text')
	print("\n Done Installing 'html2text' module!\n")
	from html2text import html2text

# pyperclip
try:
	import pyperclip
except ModuleNotFoundError:
	print("\n\n Module 'pyperclip' not installed, Commencing the installation!\n\n")
	os.system('pip3 install pyperclip')
	print("\n Done Installing 'pyperclip' module!\n")
	import pyperclip

# Google API libraries
try: 
	from google.auth.transport.requests import Request
	from google.oauth2.credentials import Credentials
	from google_auth_oauthlib.flow import InstalledAppFlow
	from googleapiclient.discovery import build
	from googleapiclient.errors import HttpError
except ModuleNotFoundError:
	print("\n\n Google Sheet API modules are not installed, Commencing the installation!\n\n")
	os.system("pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
	print("\n Installation is Done!!\n")
	from google.auth.transport.requests import Request
	from google.oauth2.credentials import Credentials
	from google_auth_oauthlib.flow import InstalledAppFlow
	from googleapiclient.discovery import build
	from googleapiclient.errors import HttpError
########################################################################################################################################



########################################################################################################################################
### constants

global DISABLE_REPORT_SEARCH
DISABLE_REPORT_SEARCH = False
global MANUAL_CAT3_MODE_INPUT
MANUAL_CAT3_MODE_INPUT = None
global DEBUG_FUNC_DEFS
DEBUG_FUNC_DEFS = False
########################################################################################################################################



########################################################################################################################################
# Database

class WorkItem(ABC):
	'''
	Doc String of WorkItem class
	This is the parent of all present 'workitems'
	'''

	#### CLASS VARIABLES ####
	''' Maps which coloumn in the csv file points to which wanted attribute of an object
	the key: str is the name of the column which will match one expected_attribute.keys()
	the value: int is the order of which column was they key in in the csv file
	not yet assigned, will be when get_all_from_csv() is called '''
	dict_mapping: Dict[str, int] = None 
	
	''' Map column titles from the CSV to attribute names of the object
	keys are the name of the columns in the exported csv file from polarian
	values are the names of the attribute of the object to be initiated
	e.g in csv file there is a column 'Space / Document', after object initiation, there will be obj.document '''
	expected_attributes: Dict[str, str] = None

	''' Maps names of WorkItem classes to the keyword they are linked with in attribute self.linked_work_items
	keys are the name of the classes, e.g- 'Component', 'DetailedDesign', etc..
	values are the linking keyword in linked_work_items, e.g- 'is parent of', 'has parent', 'realizes', etc.. '''
	link_keywords: Dict[str, str] = None

	''' Maps self.linked keys (name of the attribute objects linked) to the wanted name in the end
	keys are the actual keys in the self.linked
	values are the attributes to be called with, implemented using __getattr__
	e.g- self._linked['DetailedDesign'] has all the linked DetailedDesign objects to the current object
	instead of calling self._linked['DetailedDesign'] every time 
	the cls.linked_attrib_names will provide mapping to the long unwanted name 'DetailedDesign' to an easier name (also makes more sense) 'detailed_designs'
	and now after implementing __getattr__, we can call DD objects using self.detailed_designs which == self._linked['DetailedDesign'] '''
	linked_attrib_names: Dict[str, str] = None


	def __init__(self, ID=None, title=None, row=None, **kwargs):
		'''
		Generalized Constructor for any workitem
		'''
		# initiating the ABC class
		super().__init__()

		# Prevent initiate mode conflict
		if (ID or title) and (row):
			raise ValueError("Can't input both attributes and (row) arguments\nObject initiation will only work in direct initiation mode where all attributes are passed at ones\nOR csv reading mode where a csv row and column to title mapping dictionary is passed")

		# Direct Initiation Mode
		if ID or title:  
			
			self.ID = ID
			self.title = title
			self.__dict__.update(kwargs)

		# CSV Initiation Mode
		elif row: 

			### Initiating the Object
			obj_dict = {}
			for attrib in self.expected_attributes.keys():
				if attrib not in self.dict_mapping.keys():
					raise ValueError(f"The read csv file doens't have a '{attrib}' column.\nPlease export another csv file from polarian that has these fields: {self.expected_attributes.keys()}")
				else:
					exec(f"self.{self.expected_attributes[attrib]} = row[{self.dict_mapping[attrib]}]")

			#### Special treatment for some attributes
			# variant
			if 'variant' in self.expected_attributes.values():
				self.variant = self.variant.split(', ')

			# linked work items
			# this is a MUST attribute, every workitem should have linked work items if exported from CSV
			dict_ = deepcopy(self.linked_work_items)
			self.linked_work_items = {}
			tmps = dict_.split(', ')
			for tmp in tmps:  # remove the numerate
				colon = tmp.find(': ')

				if colon != -1:
					key = tmp[:colon]
					value = tmp[colon+2:]
					if ' ' in value:
						value = value[:value.find(' ')]

					if key in self.linked_work_items.keys():
						self.linked_work_items[key].append(value)
					else:
						self.linked_work_items[key] = [value]

				else:
					if 'unknown' in self.linked_work_items.keys():
						self.linked_work_items['unknown'].append(tmp)
					else:
						self.linked_work_items['unknown'] = [tmp]

		### linking attributes
		# checks whether to be linked WorkItems are linked or not
		self.workitems_type_set = {name: False for name in self.link_keywords.keys()}

		# This is an internal Dict which groups all types of linked WorkItem objects (initiated, aka actual objects, not just IDs like in self.linked_work_items)
		self._linked = {name: [] for name in self.link_keywords.keys()}

		# if it's initiated form CSV, then the CSV is assumed to be outputed from Polarian
		self.found_in_polarian = True

	def __getattr__(self, name):
		'''
		this is to make getting linked work items from self._linked easier
		:name: is expected to be small case class name with 's' in the end
				e.g requirements for Requirement objects
		'''
		return self._linked[self.linked_attrib_names[name]]

	@classmethod
	@abstractmethod
	def filter_object_list(cls, object):
		'''
		to filter the unwanted objects in get_all_from_csv()
		every workitem has a different filter
		'''
		pass

	@classmethod
	def get_all_from_csv(cls, assign_class_variable, hash_key=None):
		"""
		if has_key is none then return a list of object_list
		else return a dictionary with key -> hash_key

		returns all object_list from polarian ouptut of cls.__name__ csv file
		"""
		object_list = []

		# Check if the class CSV file is there
		Path(f"input_files/polarian_csv_outputs/").mkdir(parents=True, exist_ok=True)
		try:
			f = open(f'input_files/polarian_csv_outputs/{cls.__name__}.csv', 'r')
			f.close()
		except FileNotFoundError:
			raise FileNotFoundError(f"\n\nPlease put csv file of {cls.__name__}.csv exported from polarian in the designated folder")

		# Found the file. Commencing reading the CSV
		with open(f"input_files/polarian_csv_outputs/{cls.__name__}.csv", 'r', encoding='utf-8') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter = ';')
			
			#  find where to start to save data
			for row in csv_reader:
				if row:
					if 'ID' in row:  # title row detected
						cls.dict_mapping = {row[n]: n for n in range(len(row))}
						break

			# testing if all expected attributes are present in the csv file
			for col_name in cls.expected_attributes.keys():
				if col_name not in cls.dict_mapping.keys():
					raise ValueError(f"\n\n{cls.__name__}.csv doesn't have attribute '{col_name}'\nplease export another csv file from polarian with this attribute")

			# Creating the Objects from the CSV entries
			for row in csv_reader:
				object_list.append(cls(row=row))

		# filtering unwanted objects
		filtered = cls.filter_object_list(object_list)

		# return as:
		if hash_key == None:

			# assigning class variable with all objects form csv
			if assign_class_variable:
				cls.all_objects = filtered

			return filtered  # a plain list

		else:  # creating hash map (as a dictionary)
			object_dict = {}

			if hash_key == "ID":  # only ID hash_key is garanteed to have only one workitem attached item
				for obj in filtered:
					object_dict[obj.ID] = obj
			else:
				for obj in filtered:
					hash_value = eval(f"obj.{hash_key}").lower()
					if hash_value not in object_dict.keys():
						object_dict[hash_value] = [obj]
					else:
						object_dict[hash_value].append(obj)

			# assigning class variable with all objects form csv
			if assign_class_variable:
				cls.all_objects = object_dict
			
			return object_dict

	@property
	def is_linked(self) -> bool:
		'''
		checks if an object is linked to all other workitems it should be linked to
			- checks if False in self.workitems_type_set
		'''
		return not (False in self.workitems_type_set.values())

	@classmethod
	def assign_validate_polarian_link(cls, my_polarian_web_link: str):
		'''
		makes sure the variable my_polarian_web_link is valid
		Then assigns class variable
		:param my_polarian_web_link: string of web link to my polarian openned in the wanted project
		'''
		try:
			stop_ind = my_polarian_web_link.index("mypolarion")
		
		except ValueError:
			raise ValueError("This is link is invalid. It must be the 'My Polarion' web page openned in your desired project!")

		cls.my_polarian_web_link = my_polarian_web_link[:stop_ind]

	@property
	def polarian_link(self) -> str:
		'''
		return link to polarian web page of the workitem
		'''
		return f"{WorkItem.my_polarian_web_link}workitem?id={self.ID}"

	def link(self, choosen_class: type):
		'''
		MUST ONLY BE RUN AFTER RUNNING  
		get_all_from_csv(assign_class_variable=True, hash_key='ID')
		in the specific class to be connected with

		generalized link function :)

		:param choosen_class: the class to be connected to
		'''
		# making sure linking of this object didn't happen before
		target_name = choosen_class.__name__
		if not self.workitems_type_set[target_name]:
			self.workitems_type_set[target_name] = True

			if type(self.link_keywords[target_name]) == str:
				# link WorkItem to another WorkItem that has only one link_keyword
				
				if self.link_keywords[target_name] in self.linked_work_items.keys():
					for ID in self.linked_work_items[self.link_keywords[target_name]]:
						obj = choosen_class.all_objects.get(ID, None)
						if obj is not None:
							self._linked[target_name].append(obj)
							choosen_class.all_objects[ID].link(type(self))
			
			elif type(self.link_keywords[target_name]) == tuple:  
				# a workitem linked to another workitem by more than one keyword, e.g- interfaces linked to component by 'is used by' and 'is provided by'	
				for keyword in self.link_keywords[target_name]:
					# creating custom entry in the linked dictionary then will combine them normally
					new_custome_name = f"{target_name}_{keyword.replace(' ', '_')}"
					self._linked[new_custome_name] = []

					# doing the normal stuff
					if keyword in self.linked_work_items.keys():
						for ID in self.linked_work_items[keyword]:
							obj = choosen_class.all_objects.get(ID, None)
							if obj is not None:
								self._linked[new_custome_name].append(obj)
								choosen_class.all_objects[ID].link(type(self))

					# now combining the different stuff like normal attributes
					self._linked[target_name].extend(self._linked[new_custome_name])

			else:
				raise ValueError("HOW?!??!?!?!")

	def link_all(self):
		'''
		link workitems to all other workitem types it should be linked to
		'''
		for workitem in self.link_keywords.keys():
			self.link(eval(workitem))


class Component(WorkItem):
	'''
	Doc String of Components Class
	'''

	##################################################
	# class variables
	expected_attributes = {"ID": 'ID', "Title": "title", "Variant": 'variant', "Linked Work Items": 'linked_work_items',
							 "Severity": 'severity', "Status": 'status', "Space / Document": 'document'} #, "Comments": 'comments'}  # these must be just like how it's outputed from polarian

	link_keywords = {'DetailedDesign': 'is parent of',
					 'Requirement': 'realizes',
					 'Diagnostic': 'realizes',
					 'Interface': ('uses', 'provides')}

	linked_attrib_names = {'detailed_designs': 'DetailedDesign',
						   'requirements': 'Requirement',
						   'diagnostics': 'Diagnostic',
						   'interfaces': 'Interface',
						   'interfaces_uses': "Interface_uses",
						   'interfaces_provides': 'Interface_provides'}
	##################################################

	def __init__(self, ID: str = None, title: int = None, variant: str = None, status: str = None, 
				document: str = None, detailed_designs: list = [], requirements: list = [], diagnostics: list = [],
				interfaces: list = [], interfaces_uses: list = [], interfaces_provides: list = [],
				row: list = []):
		"""
		Constructor
		"""

		### Running the generalized constructor
		super().__init__(ID, title, row, variant=variant, status=status, document=document, detailed_designs=detailed_designs, 
						requirements=requirements, diagnostics=diagnostics, interfaces=interfaces, interfaces_uses=interfaces_uses, 
						interfaces_provides=interfaces_provides)

		### Extra things special to Component class objects only
		# making sure the component has a variant
		if len(self.variant) == 0:
			raise ValueError("This component has no variant (base+/-) ?!?!")

		# just to deal with wrappers ;)
		self.wrapper_stat = False  

	@property
	def true_title(self):
		"""
		if title is like this "SFTY <real_title> 01", it will return the <real_title>
		"""
		if " " in self.title:  # needs filtering
			words = self.title.split(" ")
			if words[0].upper() == words[0]:
				output =  words[1]  # assumes the title looks like this "SFTY <real_title> 01" or "SFTY <real_title>""
			else:
				output =  words[0]  # assumes the title looks like this "<real_title> 01"
		else:
			output =  self.title  # no spaces in title; title is one word

		if self.wrapper_stat:
			return output + '_wrpr'
		else:
			return output

	@classmethod
	def filter_object_list(cls, components):
		'''
		filtering Component work item objects
		'''
		# filtering non-HC (hard copy) component; removing model based components (MBC)
		# filtering obsolete components
		filtered = []
		for component in components:
			if component.status.lower() == 'obsolete':
				continue
			if 'model' in component.document.lower():
				continue
			if component.variant  == '':
				continue
			# print(component.comments)

			filtered.append(component)

		return filtered

	@classmethod
	def get_component(cls, component_to_search, CAT_num, branch, components = None):  # title, cat_num
		"""
		returns the component to search for by calling get_components and searching through all components
		"""
		if components is None:
			components = cls.get_all_from_csv(assign_class_variable=False, hash_key='true_title')  # get a list of all the components

		# dealing with wrapper components
		wrapper_stat = False
		if 'Wrpr' in component_to_search: 
			wrapper_stat = True

			print('Wrapper component detected!')

			# removing '_Wrpr' from its name
			component_to_search = component_to_search[:component_to_search.find('_Wrpr')]

		######################  searching the SW component list for matching title of the component we want ################################
		possible_components = components.get(component_to_search.lower(), None)

		if not possible_components:
			if CAT_num == 3:
				print("\nDidn't find this component in Polarian!")
				print("Since this is a CAT 3 component, Polarian work item presence is not essential.")
				return cls.get_component_manual(component_to_search, CAT_num)
			else:
				raise LookupError(f"\nDidn't find this CAT {CAT_num} component in Polarian!")

		if len(possible_components) == 1:
			wanted_component = possible_components[0]
			wanted_component.CAT_num = CAT_num
		else:
			print(f"Detected multiple components with same title:")
			for comp in possible_components:
				print(f"- {comp.title}, {comp.ID}, {comp.status}, {comp.document}")

			print()

		############################################### filtering possible components ############################################
		for component in possible_components:
			# search for component.document which has the same branch as the branch we are in
			if branch in component.document:
				wanted_component = component
				wanted_component.CAT_num = CAT_num
				break
		
		else:  ##### document filter
			possible_components2 = []  # here are components with valid document, no unvalid branch name
			# look for document names which doesn't have a release in them and either end with a number or nothing
			unwanted_keywords = ['obsolete']
			for component in possible_components:
				word = component.document.split(' ')
				if len(word) > 1:  # for multi-word document name
					wanted = word[-1]
					for keyword in unwanted_keywords:
						if '_' not in wanted and keyword not in component.document:  # checking if document is like SFTY SftyLibApp 01_P289
							possible_components2.append(component)
				else:  # document is one word
					possible_components2.append(component)
			
			else:  ##### status filter
				if possible_components2:  # components with valid document name found
					status_released_components = [component for component in possible_components2 if component.status == 'Released']
					status_released_components_len = len(status_released_components)
					if status_released_components_len > 1:
						# raise ValueError(f"\n\nMore than one component with valid document name and stat released detected:\n{[(component.title, component.status, component.ID, component.document) for component in status_released_components]}")
						# just for now to deal with components that's not possible to detect which one to choose from
						global DOCUMENT_CHOOSEN_NUMBER
						try:
							if DOCUMENT_CHOOSEN_NUMBER != None:
								wanted_component = status_released_components[DOCUMENT_CHOOSEN_NUMBER]  # FOR NOW
							else:
								wanted_component = status_released_components[cls.choose_component_manual(status_released_components)]
						except NameError:  # when running from CLI
							wanted_component = status_released_components[cls.choose_component_manual(status_released_components)]
						
						wanted_component.CAT_num = CAT_num

					elif status_released_components_len == 1:
						wanted_component = status_released_components[0]
						wanted_component.CAT_num = CAT_num
					
					elif status_released_components_len == 0:
						if len(possible_components2) > 1:
							# raise ValueError(f"\n\nNo component with valid document name has status released. Meanwhile, multiple components with valid document name but status not released is detected:\n{[(component.title, component.ID, component.status, component.document) for component in status_released_components]}")
							wanted_component = possible_components2[cls.choose_component_manual(possible_components2)]
							wanted_component.CAT_num = CAT_num

						else:

							wanted_component = possible_components2[cls.choose_component_manual(possible_components2)]
							wanted_component.CAT_num = CAT_num
				else:
					raise ValueError(f"""\n\nNo valid component document name found for components: {(component.title, component.document) for component in possible_components} is not valid""")


		if wrapper_stat:
			wanted_component.wrapper_stat = True


		#### linking all workitems together
		print("Linking all Work Items together...")
		wanted_component.link_internals_all()
		# In case a component doens't have linkedworkitem
		if wanted_component.is_linked:
			print("Done linking\n\n")

		return wanted_component

	@classmethod
	def choose_component_manual(cls, status_released_components):
		comps = [(component.title, component.status, component.ID, component.document) for component in status_released_components]
		print(f"\n\nMore than one component with valid document name and stat released detected:")
		for ind, comp in enumerate(comps):
			print(f"Number {ind+1}: - {comp}")

		choosen_ind = int(input("\nPlease check polarian and Enter the number of the component you want to choose: ")) - 1

		return choosen_ind

	@classmethod
	def get_component_manual(cls, title, CAT_num):
		'''
		for CAT3 components which doesn't need to be in polarian
		'''

		if MANUAL_CAT3_MODE_INPUT == None:
			variant = input('Please input variant: ').capitalize()
		else:
			variant = MANUAL_CAT3_MODE_INPUT

		component = Component(title=title, variant=variant)
		component.CAT_num = CAT_num
		component.found_in_polarian = False

		if MANUAL_CAT3_MODE_INPUT == None:
			q = input(f"Will initiate Component object with as this:\n{component}\n\nDo you want to continue? (y/n): ")
			while q != 'y':
				if q == 'n':
					raise ValueError("User chooose to terminate the script!")
				print('\nInvalid answer!\n')
				q = input(f"Will initiate Component object with as this:\n{component}\n\nDo you want to continue? (y/n): ")


		return component

	def do_one_dd_to_dd(self, dd):
		'''
		DD in linked work item of DD in linked work item in component  -- DD**2 :)
		if found it will link it for the component and NOT for the dd itself
		'''
		if 'is parent of' in dd.linked_work_items.keys():
			for ID2 in dd.linked_work_items['is parent of']:
				dd2 = DetailedDesign.all_objects.get(ID2, None)
				if dd2 is not None:
					self.detailed_designs.append(dd2)
					# MUST NOT LINK DD TO COMPONENT, only component to dd 
					# DetailedDesign.all_objects[ind2].link(Component)  # a function can only be in one component
					self.do_one_dd_to_dd(dd2)

	def link_dd_in_interface(self):
		'''
		interface in linked work item of DD is linked to component
		if found it will link it for the component and NOT for the dd itself
		'''
		for interface in self.interfaces:
			for dd in interface.detailed_designs:
				self.detailed_designs.append(dd)

	def link(self, choosen_class: type):
		'''
		redefining the link method to include the DD issue
		when there is a dd linked to component through other dd(s)
		'''
		if choosen_class == DetailedDesign:

			target_name = choosen_class.__name__
			if not self.workitems_type_set[target_name]:
				self.workitems_type_set[target_name] = True
				# execute the 'str' condition from super.link() as normal BUT
				if self.link_keywords[target_name] in self.linked_work_items.keys():
						for ID in self.linked_work_items[self.link_keywords[target_name]]:
							obj = choosen_class.all_objects.get(ID, None)
							if obj is not None:
								self._linked[target_name].append(obj)
								choosen_class.all_objects[ID].link(type(self))

								# This is the extra function that will be called only 
								# in the Component class
								self.do_one_dd_to_dd(obj)
		else:
			# for the rest of workitems, will execute normal link() method from super()
			super().link(choosen_class)

	def link_internals_all(self):
		'''
		link comp to all
		link dd to all
		link dd to comp which is linked through interfaces
		link dd to comp which is linked through other dds
		link req to all 
		link diag to all

		'''
		if self.found_in_polarian:

			self.link_all()

			for dd in self.detailed_designs:
				dd.link_all()

			for req in self.requirements:
				req.link_all()

			for diag in self.diagnostics:
				diag.link_all()

			for interface in self.interfaces:
				interface.link_all()


			self.link_dd_in_interface()
		
		else:
			print("Couldn't link component to other workitems as it's not found in polarian")

	def __str__(self):
		# for key, value in self.__dict__.items():
		# 	if key != "_Component__mapping_csv_title_csv_col":
		# 		print(key)
		return str({key: value for key, value in self.__dict__.items()})


class Requirement(WorkItem):
	'''
	Doc String of Requirements Class
	'''

	##################################################
	# class variables
	expected_attributes = {"ID": 'ID', "Title": "title", "Variant": 'variant', "Linked Work Items": 'linked_work_items',
							 "Status": 'status', "Space / Document": 'document', 'Description': 'description'}  # these must be just like how it's outputed from polarian
	
	link_keywords = {'Component': 'is realized in',
					 'DetailedDesign': 'is realized in'}
	
	linked_attrib_names = {'detailed_designs': 'DetailedDesign',
						   'components': 'Component'}
	##################################################

	def __init__(self, ID: str = None, title: int = None, status: str = None, components: list = [], detailed_designs: list = [], row: list = []):
		'''
		Constructor
		'''

		### Running the generalized constructor
		super().__init__(ID, title, row, status=status, components=components, detailed_designs=detailed_designs)

		### Extra things special to Component class objects only

	@classmethod
	def filter_object_list(cls, requirements):
		'''
		filters obsolete requirements
		'''
		# filtering obsolete components
		filtered = []
		for requirement in requirements:

			# filters
			if requirement.status.lower() == 'obsolete':
				continue

			filtered.append(requirement)

		return filtered

	def __str__(self):
		'''

		'''
		return str({key: value for key, value in self.__dict__.items() if str(key) != "dict_mapping" and str(key) != 'description'})


class Diagnostic(WorkItem):
	'''
	Doc String of Diagnostic Class
	'''

	##################################################
	# class variables
	expected_attributes = {"ID": 'ID', "Title": "title", "Variant": 'variant', "Linked Work Items": 'linked_work_items',
							 "Status": 'status', "Space / Document": 'document', 'Description': 'description'}  # these must be just like how it's outputed from polarian
	
	link_keywords = {'Component': 'is realized in',
					 'DetailedDesign': 'is realized in'}
	
	linked_attrib_names = {'detailed_designs': 'DetailedDesign',
						   'components': 'Component'}
	##################################################

	def __init__(self, ID: str = None, title: int = None, status: str = None, components: list = [], detailed_designs: list = [], row: list = []):
		'''
		Constructor
		'''

		### Running the generalized constructor
		super().__init__(ID, title, row, status=status, components=components, detailed_designs=detailed_designs)

		### Extra things special to Component class objects only
		
	@classmethod
	def filter_object_list(cls, requirements):
		'''
		filters obsolete requirements
		'''
		# filtering obsolete components
		filtered = []
		for requirement in requirements:

			# filters
			if requirement.status.lower() == 'obsolete':
				continue

			filtered.append(requirement)

		return filtered

	def __str__(self):
		'''

		'''
		return str({key: value for key, value in self.__dict__.items() if str(key) != 'description'})


class DetailedDesign(WorkItem):
	'''
	Doc String of DetailedDesign Class
	'''

	##################################################
	# class variables
	expected_attributes = {"ID": 'ID', "Title": "title", "Variant": 'variant', "Linked Work Items": 'linked_work_items',
							 "Severity": 'severity', "Status": 'status', "Space / Document": 'document', 'Description': 'description'}  # these must be just like how it's outputed from polarian
	
	link_keywords = {'Component': 'has parent',
					 'Requirement': 'realizes',
					 'Diagnostic': 'realizes',
					 'Interface': 'has parent'}
	
	linked_attrib_names = {'component': 'Component',
						   'requirements': 'Requirement',
						   'diagnostics': 'Diagnostic',
						   'interfaces': 'Interface'}
	##################################################

	def __init__(self, ID: str = None, title: int = None, variant: list = [], status: str = None, component: str = None, requirements: list = [], 
		diagnostics: list = None, interfaces: list = [], row: list = []):
		'''
		Constructor
		'''
		
		### Running the generalized constructor
		super().__init__(ID, title, row, variant=variant, status=status, component=component, requirements=requirements, 
						diagnostics=diagnostics, interfaces=interfaces)

		### Extra things special to Component class objects only
		# title adjustments; remove () if it's there
		if '(' in self.title:
			self.title = self.title[:self.title.find('(')]

	@classmethod
	def filter_object_list(cls, requirements):
		'''
		filters obsolete requirements
		'''
		# filtering obsolete components
		filtered = []
		for requirement in requirements:

			# filters
			if requirement.status.lower() == 'obsolete':
				continue

			filtered.append(requirement)

		return filtered

	def check_sw_component(self):
		'''

		'''
		return not not self.component

	def check_req_diag(self):
		"""
		checks if dd has sw requirements or diagnostics
		"""
		return not not (self.requirements or self.diagnostics)

	def __str__(self):
		'''

		'''
		return str({key: value for key, value in self.__dict__.items() if str(key) != 'description'})


class Interface(WorkItem):
	'''
	Doc String of Interface Class
	'''

	##################################################
	# class variables
	expected_attributes = {"ID": 'ID', "Title": "title", "Variant": 'variant', "Linked Work Items": 'linked_work_items',
							 "Status": 'status', "Space / Document": 'document', 'Description': 'description'}  # these must be just like how it's outputed from polarian
	
	link_keywords = {'Component': ('is used by', 'is provided by'),
					 'DetailedDesign': 'is parent of'}
	
	linked_attrib_names = {'detailed_designs': 'DetailedDesign',
						   'components_is_used_by': "Component_is_used_by",
						   'components_is_provided_by': 'Component_is_provided_by',
						   'components': 'Component'}
	##################################################

	def __init__(self, ID: str = None, title: int = None, variant: list = [], status: str = None, detailed_designs: list = [],
				components: list = [], components_is_used_by: list = [], components_is_provided_by: list = [], row: list = []):
		'''
		Constructor
		'''
		### Running the generalized constructor
		super().__init__(ID, title, row, variant=variant, status=status, components=components, components_is_used_by=components_is_used_by, 
						components_is_provided_by=components_is_provided_by, detailed_designs=detailed_designs)

		### Extra things special to Component class objects only

	@classmethod
	def filter_object_list(cls, requirements):
		'''
		filters obsolete requirements
		'''
		# filtering obsolete components
		filtered = []
		for requirement in requirements:

			# filters
			if requirement.status.lower() == 'obsolete':
				continue

			filtered.append(requirement)

		return filtered

	def __str__(self):
		'''

		'''
		return str({key: value for key, value in self.__dict__.items() if str(key) != 'description'})
########################################################################################################################################



########################################################################################################################################
# Data Structures

class Node:
	def __init__(self, state, parent):
		self.state = state
		self.parent = parent

	def to_list(self) -> list:
		'''
		convert node to list
		'''
		node = deepcopy(self)

		list_ = [node.state]

		while node.parent is not None:
			node = node.parent
			list_.append(node.state)

		list_.reverse()

		return list_

class Stack:
	"""
	singly linkedlist with LIFO settings
	"""
	def __init__(self):
		self._container = []

	def push(self, value):
		self._container.append(value)

	def pop(self):
		return self._container.pop()

	@property
	def empty(self):
		return not self._container

	def __repr__(self):
		return repr(self._container)
########################################################################################################################################



########################################################################################################################################
# Algorithms

def goal_test_general(wanted_goal: Component.true_title):
	"""
	argument of DFS/BFS/A* Algorithms to test if goal is reached or not

	:param wanted_goal: should be of type Component, self.true_title
	defining a first class function so that we can use this for multiple applications
	used in searching for the right search_key file
	"""
	def goal_test(current_state) -> bool:
		"""
		:param current_state: path we are in right now
		checks if the current node has the correct search_key file
		checks if the name of the component is the same and the file is of type .html
		"""
		if '.zip' not in current_state:
			for file in os.listdir(current_state):
				test3 = re.search(fr"^{wanted_goal.lower()}_?\d*[\.]?c?.html", file.lower())
				if test3:
					return True
			else:
				return False
		else:
			return not not re.search(fr"[\\/]{wanted_goal.lower()}_?\d*[\.]?c?.html", current_state.lower())

	return goal_test

def successor_general(variant, branch, search_key, path_to_reports):
	'''
	Argument of DFS/BFS/A* Algorithms to return next possible moves
	'''

	def successor(current_state) -> list:
		"""
		:param current_state: path we are in right now
		To know which layer we are in we'll count the number of '/'
		# 1- rolling build OR Release
		# 2- get all files that has self.component.branch in their names, e.g- P330
		# 3- look for Reports, if not found find self.variant, then look for Reports
		# 4- Look for {search_key} or {search_key}_ADIS
		# 5- look into all folders except if they have PSM or ASM in them
		#		PSM for base+, ASM for base-
		#		ignore set of files ['log']
		# 6- look for reporter, error if not found
		# 7- search the .html {search_key} files for the name of the component
		
		returns list of the next file to search for depending on the current state
		"""
		output = []

		current_layer = current_state.count('/') - path_to_reports.count('\\')
		
		# for step 3 must -1 if base+ was inside the folders as reports/ or base+/reports are the same step
		if 'ForInternalUse' in current_state:
			current_layer -= 2
		elif variant.capitalize() in current_state:
			current_layer -= 1

		# for zipped files we must add 1 manually
		# if '.zip' in current_state:
		# 	current_layer += 1

		# print(current_layer)
		# print(current_state)

		if '.zip' not in current_state:
			files = os.listdir(current_state)

		if current_layer == 0:
			# rolling build or release
			if 'RollingBuild' in files:
				output.append(current_state + '/RollingBuild')
			if 'Release' in files:
				output.append(current_state + '/Release')

		elif current_layer == 1:
			# searching for the right branch
			for file in files:
				if branch in file:
					output.append(current_state + '/' + file)

		elif current_layer == 2:
			### searching for reports folder			
			
			# sometimes they're inside a folder of the variant name
			if variant.capitalize() in files:
				if 'ForInternalUse' in os.listdir(f"{current_state}/{variant.capitalize()}"):
					if 'Reports' in os.listdir(f"{current_state}/{variant.capitalize()}/ForInternalUse"):
						output.append(f"{current_state}/{variant.capitalize()}/ForInternalUse/Reports")  # third place to look in
				
				if 'Reports' in os.listdir(f"{current_state}/{variant.capitalize()}"):
					output.append(f"{current_state}/{variant.capitalize()}/Reports")  # second place to look in

			# sometimes they're just out there
			if 'Reports' in files:
				output.append(current_state + '/' + 'Reports')  # first place to look in

		elif current_layer == 3:
			
			if f"{search_key}_ADIS.zip" in files:  # forth, zipped {search_key}_ADIS
				output.append(f"{current_state}/{search_key}_ADIS.zip")

			if f"{search_key}_ADIS" in files:  # third, normal {search_key}_ADIS
				output.append(current_state + '/' + f'{search_key}_ADIS')

			if f'{search_key}.zip' in files:  # second, zipped {search_key}
				output.append(f"{current_state}/{search_key}.zip")

			if f"{search_key}" in files:  # first, normal {search_key}
				output.append(current_state + '/' + f'{search_key}')

		elif current_layer == 4:
			# layer 5, 1- we must take only folders except log
			#			2- take in folders that doesn't end with PSM/ASM
			#			3- take in folders that does end with PSM if base+, ASM if base-
			#	if zipped file ;)
			
			valid_ends = {'Base+': 'PSM', 'Base-': 'ASM'}
			not_wanted_ends = [value for key, value in valid_ends.items() if key != variant.capitalize()]
			
			if '.zip' in current_state:
				# do step 5 and 6 at once (4 & 5 in code) because once .zip file is there it can't be continued in the algorithm as a normal, it can't be openned

				# get all paths
				with ZipFile(current_state, 'r') as zipobj:
					paths = zipobj.namelist()

				paths = [path[5:] for path in paths if path[5:] != '']  # filtering the self.search_key in the beggining
				
				# step 5, the layer name folders
				step5_folder_names = set()
				for path in paths:
					if '/' in path and 'log' not in path:  # if folder and not log
						file = path[:path.find('/')]
						if not True in [file.endswith(end) for end in not_wanted_ends]:  # if file name doesn't end with an unwanted name, e.g if the component is base+, it shouldn't end with ASM
							step5_folder_names.add(file)
				
				# step 6, get reporter
				for path in paths:
					for element in step5_folder_names:
						if path.startswith(element) and 'mcr_data' in path and search_key == 'QAC':
							output.append(f"{current_state}/{path}")
						if path.startswith(element) and 'Reporter' in path:
							output.append(f"{current_state}/{path}")

			else:
				
				for file in files:
					if os.path.isdir(f"{current_state}/{file}") and file != 'log':  # if folder and not log
						if not True in [file.endswith(end) for end in not_wanted_ends]:  # if file name doesn't end with an unwanted name, e.g if the component is base+, it shouldn't end with ASM
							output.append(current_state + '/' + file)

		elif current_layer == 5:
			# find Reporter or mcr_data for QAC
			if search_key == "QAC":
				if 'mcr_data' in files:
					output.append(current_state + '/' + 'mcr_data')

			if 'Reporter' in files:
				output.append(current_state + '/' + 'Reporter')

		elif current_layer == 6:
			return []

		return output
	
	return successor

def DFS(initial, goal_test, successor):
	"""
	Generic Implementation of Depth-First-Search Algorithm
	"""
	frontier = Stack()
	frontier.push(Node(initial, None))
	explored = {initial}

	while not frontier.empty:
		current_node = frontier.pop()
		current_state = current_node.state

		if goal_test(current_state):
			return current_node

		for path in successor(current_state):
			if path in explored:
				continue

			explored.add(path)
			frontier.push(Node(path, current_node))

	return None
########################################################################################################################################



########################################################################################################################################
# Data Classes

@dataclass
class QAC:
	code: str
	start_line_num: int

@dataclass
class CodeSwitch:
	title: str
	end: str
	code: str
	function: str
	line_num: int
	end_line_num: int
	is_enabled: bool
	has_nested_code_switch: bool

@dataclass
class CodeComment:
	'''
	Any Comment in the components
	'''
	comment: str
	start_line_num: int
	end_line_num: int
	type_: str = "Script didn't search for type"
	function: str = "Script didn't search for function"
	func_type: bool = False

@dataclass
class FuncComment:  
	code_comment: CodeComment
	name: str = None
	params: list = None
	retval: str = None
	brief: str = None
	returns: str = None
	ref: str = None

@dataclass
class Func:
	name: str
	params: list
	retval: str
	# ref: str  #TODO:
	body: str  
	start_line_num: int
	end_line_num: int
	is_local: bool
	variant: list
	func_comment: FuncComment = None

	@property
	def matches_comment(self) -> bool:
		if self.func_comment:

			# checking name
			name_check = (self.name == self.func_comment.name)

			# param check
			if self.func_comment.params:
				params_check = []
				for comment_param in self.func_comment.params:  # list of str
					for real_param in self.params:  # list of tuple of str
						if comment_param in real_param[0] or comment_param in real_param[1]:
							params_check.append(True)
							break
					else:
						params_check.append(False)

				param_check = not (False in params_check)
			else:
				param_check = False

			# Total
			return name_check and param_check

		else:
			return True

	def __str__(self):
		'''
		str for Func
		'''
		return str({key: value for key, value in self.__dict__.items() if str(key) != "body"})

@dataclass
class CodeReview:
	'''
	contains the data needed for code review, func data from code NOT from dd NOT from func comment
	'''
	func: Func
	dd: DetailedDesign
	does_variant_match_dd: bool = None

class Memory:
	def __init__(self, mem_path):
		self.mem_path = mem_path

		#  checking to see if it's the first time
		try:
			f = open(self.mem_path, 'r')
			f.close()
		
		except FileNotFoundError:  # dealing with first time runs
			
			# creating the path
			print("Creating memory")
			self.first_time_run()

			return None  # stop init function here

		########### Initiating a memory object not run for first time ##############
		# loading memory
		self.load_memory()

	def first_time_run(self):
		'''
		Creating the file
		'''
		mem_path = self.mem_path[:self.mem_path.find('/')]
		Path(mem_path).mkdir(parents=True, exist_ok=True)
		os.system(f'attrib +h f{mem_path}')

	def load_memory(self):
		with open(self.mem_path, 'rb') as pkl:
			loaded = pickle.load(pkl)
			self.__dict__.update(loaded)
########################################################################################################################################



########################################################################################################################################
# Blocks

class BlockTemplate(ABC):
	'''
	Block Template Parent class for all blocks
	'''

	num_empty_rows_between_tables = 2

	# Abstract class variables
	analysis_name = "name of analysis"
	stat = "Stat of This Type of Analysis"

	def __init__(self, component):
		self.component = component
		super().__init__()

	def get_link_text(self):
		'''
		return the text that should be printed in the place of the hyperlink for the sheets
		'''
		return f"Analysis of {self.analysis_name} for the SW component {self.component.true_title}.c"

	@abstractmethod
	def get_checklist_table(self) -> List[List]:
		"""
		meant to create the lists that will be the argument to csv_writer (the rows in the csv file)
		"""
		pass

	@abstractmethod
	def get_analysis_table(self) -> List[List]:
		'''
		
		'''
		pass

	@abstractmethod
	def merges(self) -> List[Dict]:
		'''
		call GoogleSheet.get_list_of_merges
		customized merge for every table
		'''
		pass

	@abstractmethod
	def get_stat(self) -> bool:
		'''
		Should be either True or False or None
		Indicate whether this analysis block for the wanted component passed or not
		'''
		pass

	def get_str_analysis_table(self) -> List[List[str]]:
		'''
		makes sure all the values of the output table are of type string

		makes sure all rows are of the same length, adds empty strings to rows with less values than others

		This functions get the table ready for GoogleSheet API
		'''
		str_output = []
		for row in self.analysis_table:
			str_output.append([])
			for value in row:
				str_output[-1].append(str(value))

		# finding maximum length of rows in this table
		max_value = 0
		for row in str_output:
			current_len = len(row)
			if current_len > max_value:
				max_value = current_len

		# appending empty strings in rows with lower len()
		for row_ind in range(len(str_output)):
			while len(str_output[row_ind]) < max_value:
				str_output[row_ind].append('')

		return str_output

	@classmethod
	@property
	def table(cls):
		'''
		The cell that mentions that the next cell is the link to the analysis table
		'''
		return f"Link to {cls.analysis_name.replace('_', ' ')} report analysis: "

	@staticmethod
	def get_checklist_tables(blocks) -> List[List[str]]:
		'''
		collects checklist_table of all blocks
		'''
		all_rows = []
		for ind, block in enumerate(blocks):
			for row in block.checklist_table:
				all_rows.append(row)

			
			# Add extra rows only in between tables
			if ind+1 != len(blocks):
				for _ in range(BlockTemplate.num_empty_rows_between_tables):
					all_rows.append([])

		return all_rows

	@staticmethod
	def get_analysis_tables(blocks) -> List[List[str]]:
		'''
		collects checklist_table of all blocks
		'''
		all_rows = []
		for block in blocks[1:]:
			for row in block.str_analysis_table():
				all_rows.append(row)
			
			# Add extra rows only in between tables
			if ind+1 != len(blocks):
				for _ in range(BlockTemplate.num_empty_rows_between_tables):
					all_rows.append([])

		return all_rows

class FirstBlock(BlockTemplate):
	"""
	1. Category of SW module for detailed software analysis.	
	"""

	# possible analysis stats
	class AnalysisStatus:
		not_started = "Not Started"
		in_progress = "In Progress"
		ok = "OK"
		nok = "NOK"

	description = '1. Category of SW module for detailed software analysis.'
	name = 'SW component : '
	CAT_num = 'SW component CAT type : '
	stat = 'SWC analysis status : '
	variant = 'Code variant : '
	SW_release = 'Software release : '

	def __init__(self, component: Component, variant, branch, paths_to_code, path_to_reports, path_to_tcc, my_polarian_web_link):
		self.component = component
		self.name = component.true_title
		self.CAT_num = component.CAT_num
		self.stat = self.get_stat()
		self.variant = variant
		self.SW_release = branch

		self.paths_to_code = paths_to_code
		self.path_to_reports = path_to_reports
		self.path_to_tcc = path_to_tcc
		self.my_polarian_web_link = my_polarian_web_link

		# output tables
		self.checklist_table = self.get_checklist_table()
		### no analysis_table for first block
		# self.analysis_table = self.get_analysis_table()
		# self.str_analysis_table = self.get_str_analysis_table()  

	def get_checklist_table(self) -> List[List]:
		output = []
		output.append([FirstBlock.description])
		output.append([FirstBlock.name, self.name + '.c']) #TODO: detect whether component is .h or .c
		output.append([FirstBlock.CAT_num, f"CAT{self.CAT_num}"])
		output.append([FirstBlock.stat, self.stat])
		output.append([FirstBlock.variant, self.variant])
		output.append([FirstBlock.SW_release, self.SW_release])
		return output

	def get_analysis_table(self) -> None:
		'''
		There is no analysis table for the general description block
		'''
		pass

	def merges(self, *args, **kwargs):
		'''
		no merges needed here as no analysis table for first block
		'''
		pass

	def get_stat(self, blocks=None) -> bool:
		'''
		checks if all .stat attribute of each block and 
		then accordingly returns the apropriate value from 
		class variable analysis_status_formats_list

		ASSUMES .stat of each block could either be True or False or None
		if all are True

		:param blocks: list of all the executed blocks
		'''

		# When there are no blocks yet!
		if blocks == None:
			return FirstBlock.AnalysisStatus.in_progress

		for block in blocks:
			if block.stat == False:
				# Found False block
				return FirstBlock.AnalysisStatus.nok
		else:
			for block in blocks:
				if block.stat == None:
					# not False but there is stat None
					return FirstBlock.AnalysisStatus.in_progress
			else:
				# All stat are True
				return FirstBlock.AnalysisStatus.ok

	def update_analysis_stat(self, blocks) -> None:
		'''
		updates the .stat attribute
		'''
		self.stat = self.get_stat(blocks)

	def __str__(self):
		'''
		string representatoin of First_block
		'''
		return str(self.__dict__)


class SecondBlock(BlockTemplate):
	"""
	2. Code coverage analysis.	
	"""

	analysis_name = "code_coverage"
	search_key = 'RTRT'

	description = "2. Code coverage analysis.	"
	report_found = "Does the SW component has code coverage report?"
	report_path = "Link to code coverage report : "
	stat = "Does the SW component has 100% coverage?"
	code_coverage_table = "Link to code coverage report analysis : "

	def __init__(self, first_block):
		self.first_block = first_block
		self.component = first_block.component
		self.variant = first_block.variant
		self.branch = first_block.SW_release
		self.path_to_reports = first_block.path_to_reports

		self.sole_files = []

		global DISABLE_REPORT_SEARCH
		if DISABLE_REPORT_SEARCH:
			self.report = None  # TEMPORARY FOR SERVER CUT
		else:
			self.report = self.find_report()

		if not self.report:  # no report found
			self.report_found = False
			self.report_path = None
			self.stat = None
		else:
			self.report_found = True
			self.code_coverage = self.get_entries()
			self.stat = self.get_stat()

		# output tables
		self.checklist_table = self.get_checklist_table()
		self.analysis_table = self.get_analysis_table()  # initializes self.table_start_row_inds
		self.str_analysis_table = self.get_str_analysis_table()
				
	def get_stat(self) -> float:
		"""
		returns summary % of all code coverage (summary of summary)
		"""
		if self.code_coverage:
			total = [0, 0]
			for score in self.code_coverage['Summary'].items():
				total[0] += score[1][0]
				total[1] += score[1][1]

			return total[0]/total[1]

	def get_entries(self):
		"""
		reads self.report and parses CodeCoverageEntry objects from it
		"""

		output = {}  # dictionary of dictionaries
					 # {function_name: {attribute: List[Tuple[score, total]]}}  # note that there is a list of tuples to account for the output of all the html files

		raws = self.report
		report_coverage_part = []
		for ind, raw in enumerate(raws):
			ind_1 = raw.find("Report coverage")
			if ind_1 != -1:
				print(f"{self.search_key} report Read", end='')
				if self.sole_files != []:  # aka file gotten by putting it into input files, find_report() not called
					print(f' for file {self.sole_files[ind]}')

				report_coverage_part.append(raw[ind_1:])
			else:
				if self.sole_files != []:  # aka file gotten by putting it into input files, find_report() not called
					print(f"{self.search_key} Report {self.sole_files[ind]} doesn't have 'Report coverage' in it!!!!!!!!!!")
				else:
					print(f"{self.search_key} Report doesn't have 'Report coverage' in it!!!!!!!!!!")
		

		partitioned = [raw.split("**")[1:] for raw in report_coverage_part]  # breaking up the text in each html into values in a list [name, block, name, block, etc..]
		
		# now even indexed values are the function names, and the following odd indexed values are the blocks which need to be parsed
		even_ind = True
		for ind_p in range(len(partitioned)):
			for ind_f in range(len(partitioned[ind_p])):
				if even_ind:  # function name

					even_ind = not even_ind  # the next index is the opposite

					# word filter, currently there is nothing i want to filter
					# not_wanted_keywords = ['File']  # add here the words you want to remove
					# for word in not_wanted_keywords:
					# 	if word in partitioned[ind_p][ind_f]:
					# 		# partitioned[ind_p][ind_f] = partitioned[ind_p][ind_f][partitioned[ind_p][ind_f].index(word)+len(word)+1:]  # assumes the unwanted word is in the beggining
					# 		partitioned[ind_p][ind_f] = partitioned[ind_p][ind_f].replace(word, "")

					name = partitioned[ind_p][ind_f].strip()
					if name not in output.keys():
						output[name] = {}

				else:  # block
					even_ind = not even_ind

					not_wanted_keywords = ['---']  # add here the words you want to remove
					for word in not_wanted_keywords:
						if word in partitioned[ind_p][ind_f]:
							partitioned[ind_p][ind_f] = partitioned[ind_p][ind_f].replace(word, "")
					
					block = partitioned[ind_p][ind_f].strip()
					block_partitioned = re.split(r"\||\n", block)

					even2 = True
					for part in block_partitioned:
						if even2:  # attribute name
							attrib = part.strip()

							if attrib not in output[name].keys():
								output[name][attrib] = []

							even2 = not even2

						else:  # value to be parsed into a tuple
							tmp = part.strip()

							values_considered_none = ['no', 'none', 'yes', 'n/a']  # add values that means None here

							if not attrib == 'Hit':
								for val in values_considered_none:
									if val in tmp:
										output[name][attrib].append(None)
										break
								else:
									output[name][attrib].append((int(tmp[tmp.index("(")+1:tmp.index("/")]) , int(tmp[tmp.index("/")+1:tmp.index(")")])))
							else:
								output[name][attrib].append(tmp)
							
							even2 = not even2

		# turning the list of tuples/None into one value, either one tuples or a None value. This tuple is the correct one to take out of all the htmls
		for function in output.keys():
			for attrib in output[function].keys():
				list_scores = [tuple_[0] for tuple_ in output[function][attrib] if type(tuple_) == tuple]
				if list_scores:
					output[function][attrib] = (max(list_scores), output[function][attrib][0][1])
				elif attrib == 'Hit':
					pass
				else:  # list is empty meaning all values inside the list are not tuples (score, total), HOPEFULLY, they're all None, i didn't see any other case till now :)
												# i just made it so that it's not none the hit will be = tmp
					output[function][attrib] = None

		# print(len(output))
		# for name, dict_ in output.items():
		# 	print(name, dict_)

		# correcting the "Summary" key in the dictionary
		# First of all, clear the values and make it a list instead of a tuple; needs to be mutable
		for attrib in output['Summary'].keys():
			output['Summary'][attrib] = [0, 0]
		# summ all except the first block, which is the file itself not a function
		first_flag = True  # assuming the file is always the first block ###################################
		for function in output.keys():
			for attrib in output[function].keys():
				if attrib != "Hit" and output[function][attrib] != None and function != "Summary" and not first_flag:
					output['Summary'][attrib][0] += output[function][attrib][0]
					output['Summary'][attrib][1] += output[function][attrib][1]
				# if attrib == 'Hit':
				# 	print(function, output[function][attrib])
				if first_flag:
					first_flag = False

		# saving not covered functions
		self.not_covered_funcs = {}  # {func: {}}
		for func in output.keys():
			if 'Hit' in output[func]:
				if 'yes' in output[func]['Hit']:
					for attrib in output[func].keys():
						if output[func][attrib] != None and func != "Summary" and attrib != 'Hit':
							if output[func][attrib][0] != output[func][attrib][1]:
								if func not in self.not_covered_funcs.keys():
									self.not_covered_funcs[func] = {}
								else:
									self.not_covered_funcs[func][attrib] = output[func][attrib]
			else:
				for attrib in output[func].keys():
					if output[func][attrib] != None and func != "Summary" and attrib != 'Hit':
						if output[func][attrib][0] != output[func][attrib][1]:
							if func not in self.not_covered_funcs.keys():
								self.not_covered_funcs[func] = {}
							else:
								self.not_covered_funcs[func][attrib] = output[func][attrib]

		# viewing the output just for testing
		# for key in self.not_covered_funcs.keys():
		# 	print(key)
		# 	for key2, item in self.not_covered_funcs[key].items():
		# 		print(key2, item)

		print(f"Done Reading and Parsing {self.search_key} file\n")

		return output	

	def search_for_report(self) -> List[str]:
		'''
		Implements a backtracking algorithm (DFS) to search for report
		return list of html file raw, (with the tags and everything)
		(should be processed with html2text)
		'''
		output: List[str] = []
		path = self.path_to_reports
		path = self.filter_backslash(path)

		# making sure the path_to_reports exists
		#TODO:

		##### Mechanism of Search:  #####
		# 1- rolling build OR Release
		# 2- get all files that has self.component.branch in their names, e.g- P330
		# 3- look for Reports then self.variant/Reports, then self.variant/ForInternalUse/Reports
		# 4- Look for {search_key} or {search_key}_ADIS
		# 5- look into all folders except if they have PSM or ASM in them
		#		PSM for base+, ASM for base-
		#		ignore set of files ['log']
		# 6- look for reporter, error if not found
		# 7- search the .html {search_key} files for the name of the component
		# 8- if found return, else recurse to the last valid step

		goal_test = goal_test_general(self.component.true_title)
		successor = successor_general(self.variant, self.branch, self.search_key, self.path_to_reports)

		report_path = DFS(path, goal_test, successor)

		if report_path == None:
			print(f"Didn't find {self.component.true_title} {self.search_key} report\n\n")
			return None

		else:
			report_path = report_path.state
			print(f"\nDepth First Search Algorithm Result: {report_path}\n\n")

			if '.zip' not in report_path:
				self.report_path = report_path
				files = os.listdir(self.report_path)
				for file in files:
					if re.search(fr"{self.component.true_title.lower()}_?\d*[\.]?c?.html", file.lower()):  # to avoid name_cfg, we only want name_x where x is a number
						print(f"Found file {file}")
						self.sole_files.append(file)
						with open(f"{self.report_path}/{file}", 'r') as file:
							output.append(file.read())
			else:
				# finish_ind = -(report_path[::-1].find('/')+1)  # index where the name of the html file starts
				finish_ind = report_path.find('.zip')
				zip_path = report_path[:finish_ind+4]
				self.report_path = zip_path
				with ZipFile(zip_path, 'r') as zipobj:
					paths = zipobj.namelist()
					for path in paths:
						if re.search(fr"{self.component.true_title.lower()}_?\d*[\.]?c?.html", path.lower()) and 'Cvi' not in path:
							print(f"Found file {zip_path}/{path}")
							self.sole_files.append(path)
							with zipobj.open(path, 'r') as p:
								output.append(p.read().decode())

		return output

	def find_report(self):
		"""
		it will look in "input_files/reports/{self.variant}/{self.search_key}/self.component.true_title" first, if not found it will search otherwise it'll use it.

		find self.search_key report in the reports section if not found return None else returns html content as string
		"""
		output = []
		Path(f"input_files/reports/{self.variant}/{self.search_key}/").mkdir(parents=True, exist_ok=True)
		reports = os.listdir(f"input_files/reports/{self.variant}/{self.search_key}/")

		if reports:
			for report in reports:
				if self.component.true_title in report:  # found self.search_key report file in input_files folder, Thus will not search
					### found the report

					# getting raw file
					print(f"Found Report in input_files: input_files/reports/{self.variant}/{self.search_key}/{report} for component: {self.component.true_title}")
					with open(f"input_files/reports/{self.variant}/{self.search_key}/{report}", 'r') as file:
						output.append(file.read())

					# getting link
					self.report_path = "Report found in input files. Therefore unable to know link"
					break

			else:  # Didn't find self.search_key report, Thus will commence searching for self.search_key in server files
				print(f"{self.component.true_title} {self.search_key} report not found, Searching for {self.search_key} report in\n{self.path_to_reports}\n")
				output = self.search_for_report()
		else:   # Didn't find self.search_key report, Thus will commence searching for self.search_key in server files
			print(f"{self.component.true_title} {self.search_key} report not found, Searching for {self.search_key} report in\n{self.path_to_reports}\n")
			output = self.search_for_report()

		if output == None:
			return None
		else:
			raws = [html2text(report) for report in output]

		return raws

	def filter_backslash(self, path):
		for ind in range(len(path)):
			if path[ind] == "\\":
				path = path[:ind] + '/' + path[ind+1:]
		return path

	def merges(self, *args, **kwargs):
		'''
		no merges for code coverage analysis, no repeated data
		'''
		return []

	def get_checklist_table(self) -> List[List[str]]:
		output = []
		output.append([SecondBlock.description])
		output.append([SecondBlock.report_found, "Yes" if self.report_found else "No"])
		paths = " , ".join([f"{self.report_path}/{file}" for file in self.sole_files])
		output.append([SecondBlock.report_path, "" if not self.report_path else paths])
		output.append([SecondBlock.stat, "" if self.stat is None else "Yes" if self.stat == 1.0 else "No"])
		output.append([SecondBlock.table, self.get_link_text()])
		return output

	def get_analysis_table(self) -> List[List[str]]:
		"""
		for the link to table part; table of not covered function
		"""
		output = []

		self.table_start_row_inds = [0]

		SN = 1
		output.append(["SN", "SW function that not fully covered in unit test coverage report",	"Comment", "Action"])
		try:
			if self.code_coverage and self.stat != 1.0:
				for func in self.not_covered_funcs.keys():
					comment = ""
					for attrib in self.not_covered_funcs[func].keys():
						comment += f"{attrib}: {self.not_covered_funcs[func][attrib]}, "
					output.append([SN, func, comment, ""])
					SN += 1
			else:
				output.append(['1-', 'No Output'])
		except AttributeError:
			output.append(['1-', 'No Output'])

		return output


class ThirdBlock(SecondBlock):
	"""
	3. Dead code analysis.	
	"""

	analysis_name = "dead_code"
	search_key = 'QAC'

	description = "3. Dead code analysis.	"
	report_found = "Does the SW component has QAC report?"
	report_path = "Link to QAC report : "
	stat = "Does all lines of is reachable/there is 'no dead' code?"

	def __init__(self, first_block):
		self.first_block = first_block
		self.component = first_block.component
		self.variant = first_block.variant
		self.branch = first_block.SW_release
		self.path_to_reports = first_block.path_to_reports

		self.sole_files = []

		global DISABLE_REPORT_SEARCH
		if DISABLE_REPORT_SEARCH:
			self.report = None  # TEMPORARY FOR SERVER CUT
		else:
			self.report = self.find_report()

		if not self.report:  # no report found
			self.report_found = False
			self.report_path = None
			self.stat = None
		else:
			self.report_found = True
			self.dead_code = self.get_entries()
			self.stat = self.get_stat()

		# output tables
		self.checklist_table = self.get_checklist_table()
		self.analysis_table = self.get_analysis_table()  # initializes self.table_start_row_inds
		self.str_analysis_table = self.get_str_analysis_table()

	def get_stat(self) -> bool:
		'''
		whether there are dead code or not
		'''
		return not not self.get_entries()

	def get_entries(self) -> List[QAC]:
		'''
		if unreachable in report, use helix QAC to generate QAC object 
		and report them in table

		FOR NOW, it will return a boolean of whether it found 'unreachable or not'
		'''
		for report in self.report:
			if 'unreachable' in report:
				print("QAC report has 'unreachable' in it!!!!!!!!!!!!!!!!!!!!!")
				return True
		else:
			print("QAC report doesn't have 'unreachable' in it\n")
			return False

	def filter_backslash(self, path):
		for ind in range(len(path)):
			if path[ind] == "\\":
				path = path[:ind] + '/' + path[ind+1:]
		return path

	def merges(self, *args, **kwargs):
		'''
		no merges for QAC analysis, no repeated data
		'''
		return []

	def get_checklist_table(self) -> List[List[str]]:
		output = []
		output.append([ThirdBlock.description])
		output.append([ThirdBlock.report_found, "Yes" if self.report_found else "No"])
		paths = " , ".join([f"{self.report_path}/{file}" for file in self.sole_files])
		output.append([ThirdBlock.report_path, "" if not self.report_path else paths])
		output.append([ThirdBlock.stat, "" if self.stat is None else "Yes" if not self.stat else "No"])
		output.append([ThirdBlock.table, self.get_link_text()])
		return output

	def get_analysis_table(self) -> List[List[str]]:
		'''
		return analysis table
		'''
		output = []

		self.table_start_row_inds = [0]

		output.append(["SN", "SW function with dead code from QAC report.", "Comment", "Action"])
		if self.stat:
			output.append(['1-', "'unreachable' found in QAC report!!!!"])
		elif self.report:
			output.append(['1-', "No 'unreachable' in QAC report"])
		else:
			output.append(['1-', 'No Output'])

		return output


class ForthBlock(BlockTemplate):
	"""
	4. Code switches identification analysis.	
	"""

	analysis_name = "code_switch"

	description = "4. Code switches identification analysis."
	stat = "Does the SW component has code switches?"
	code_switch_necessity = "If SW component has code switch, Is this code switch required in VW requirements?"

	def __init__(self, first_block):
		self.first_block = first_block
		self.component = first_block.component
		self.variant = first_block.variant
		self.paths_to_code = first_block.paths_to_code
		self.path_to_tcc = first_block.path_to_tcc
		
		self.enabled_disabled_result: Dict[str: bool] = {}  # str= statetment e.g- (ASM==1), bool=enabled/disabled -> True/False

		self.all_files = None
		self.code_file_both = self.get_code_file(self.component.true_title)
		self.code_file, self.code_file_path = self.code_file_both
		print(f"Will be reading code from file found at {self.code_file_path}\n\n")
		self.include_files_to_search_in = {}
		
		# csv attributes
		if self.code_file:  # code file is found
			
			self.code_switches_all = self.get_code_switches_all()
			self.func_defs = self.get_all_funcs(self.code_file, self.code_switches_all)
			print(f"Detected {len(self.func_defs)} functions implemented in code")
			
			# for debugging func_defs
			if DEBUG_FUNC_DEFS:
				print(len(self.func_defs))
				for func in self.func_defs:
					print(func)

			self.code_switches = self.get_code_switches(self.code_switches_all)


			self.stat = self.get_stat()
			self.code_switch_necessity = self.get_code_switch_necessity()
		else:  # code file is not found

			self.code_switches_all = None
			self.code_switches = None
			self.func_defs = None

			self.stat = "Code not found, please insert file manually in input_files/code"
			self.code_switch_necessity = "Code not found, please insert file manually in input_files/code"
		
		# output tables
		self.checklist_table = self.get_checklist_table()
		self.analysis_table = self.get_analysis_table()  # initializes self.table_start_row_inds
		self.str_analysis_table = self.get_str_analysis_table()

	def get_stat(self) -> bool:
		'''
		stat for ForthBlock
		'''
		return not not self.code_switches

	def get_code_switch_necessity(self) -> bool:
		"""
		hamza told me don't do it, FGL is responsible for it
		"""
		pass

	def get_outside_function(self, func_defs: List[Func], line_num: int) -> str:
		"""
		Generalized function where function definitions is passed as one string
		and line number of the code you want to know what function 
		it's in

		return name of the function it's in OR None if it's not in any function
		"""
		for func in func_defs:
			if line_num > func.start_line_num and line_num <= func.end_line_num:
				return func.name
		else:
			return None

	def assign_enabled_stat(self, code_switches) -> bool:
		'''
		:param statement: is the statement to be evaluated
						aka the condition of the code switch
						e.g- #IF ASM == 1
		searches the #includes for the value of all #defines
		then executes a c file that outputs the evaluation of the #if
		:returns: True if enabled, False if disabled
		'''
		if not code_switches:
			return code_switches
		else:		

			#### getting hash defines values if they're not already fet hes
			unwanted_includes = ['MemMap.h']
			if not self.include_files_to_search_in:
				print("searching for and reading all #includes...\n")

				files_to_search_in = []
				for line in self.code_file.split("\n"):
					match = re.findall(r"#include <?\"?\'?([\w\.\_]+)>?\"?\'?", line)
					if match:
						if not match[0] in unwanted_includes and not match[0] in self.include_files_to_search_in:
							self.include_files_to_search_in[match[0]] = ''
				
				for file in self.include_files_to_search_in.keys():
					code, path = self.get_code_file(file, True, True)
					if code:
						self.include_files_to_search_in[file] = code
				
				### starting to create the c_file
				# getting all #define
				explored = set()
				c_file = "#include <stdio.h>\n#include <stdint.h>\n#include <stdbool.h>\n\n" # :)
				#adding the defined() function
				c_file += "\nbool defined(int input) {\n\treturn (bool)input;\n}\n\n"
				for code in self.include_files_to_search_in.values():
					for line in code.split("\n"):
						match = re.findall(r'^\#define[ \t]+([\w_\d]+)[ \t]+([\w_\d\(\)\*\\]*)', line.strip())
						if match:
							match = match[0][0]
							if match not in explored:  # to prevent multiple definitions
								c_file += line.strip()
								c_file += '\n'
								explored.add(match)

				if '#define' not in c_file:
					print("In searching for enabled/disabled stat for code switches, No #include read, thus no #defines read!")
					return code_switches

				c_file += '\n\n'
				self.c_file = c_file
			#########################################################

			### get all the code switches and put printf("number") inside them
			c_file = deepcopy(self.c_file)
			c_file += 'int main () {\n'
			current_end = None
			for ind, code_switch in enumerate(code_switches):

				#### to handle #elif not to get printed twice
				if current_end != code_switch.title:
					c_file += f"\t{code_switch.title}\n"

				c_file += f"\t\tprintf(\"{ind}\\n\");\n"

				#### to handle 
				# #IF
				#	#IF
				#	#endif
				# #else
				# #endif
				# should not print the end of the mother #IF, aka should not put #else
				# men el akher -> DON'T PUT END STATMENT IF NEXT CODE SWITCH IS NESTED
				if '#endif' in code_switch.end:
					c_file += f"\t{code_switch.end}\n"
				elif not code_switch.has_nested_code_switch:
					c_file += f"\t{code_switch.end}\n"

				current_end = code_switch.end
			
			c_file += '\treturn 0;\n}'


			# creating the c file :)
			Path(f"internals/c_files").mkdir(parents=True, exist_ok=True)
			with open('internals/c_files/test.c', 'w') as f:
				f.write(c_file)


			# executing and creating a log file with the output :)
			command = f"powershell \"{self.path_to_tcc}\\tcc.exe -run internals\\c_files\\test.c"
			result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode().strip()
			try:  # assumes output are only numbers seperated by \r, \n, ' '
				if result != '':
					enabled_code_switches_indexes = [int(res.strip()) for res in result.split('\n')]
				else:
					enabled_code_switches_indexes = []
			
			except Exception:  # probably an error arrised
				print(result)
				print("An Error arised when compiling the c code to evaluate code switch enabled/disabled. Thus, couldn't assign enabled/disabled stat to code switches")
				return code_switches

			# assigning the output numbers as enabled and the rest as disabled
			for ind in range(len(code_switches)):
				if ind in enabled_code_switches_indexes:
					code_switches[ind].is_enabled = True
				else:
					code_switches[ind].is_enabled = False
			print('Executed the code switches c code file successfully and assigned output!')
			
			return code_switches
		
	@staticmethod
	def KILL_ALL_COMMENTS(text: str, passive_mode = False) -> str:
		'''
		takes a text as input and removes all comments from it
		'''
		comment_keywords = {'/*': '*/',
						   '//': '\n'}

		for openner, closer in comment_keywords.items():
			while openner in text:
				for ind in range(len(text)):
					if text[ind:ind+2] == openner:
						# found a comment openning >:(
						# finding the end of the comment
						for ind2 in range(len(text[ind+3:])):

							# for two word closer -> */ - removes it all the two characters */
							if text[ind+3+ind2 : ind+3+ind2+2] == closer:
								# found the end of the comment
								
								# KILL THE COMMENT >:)
								text = text[:ind] + text[ind+3+ind2+2:]
								
								break

							# for one word closer -> \n - will not remove the \n
							if text[ind+3+ind2] == closer:
								# found the end of the comment
								
								# KILL THE COMMENT >:)
								text = text[:ind] + text[ind+3+ind2:]
								
								break

						else:
							line_num = text[:ind+3].count('\n')
							if passive_mode or openner == '//':
								return text[:text.find(openner)]
							else:
								raise ValueError(f"A comment is openned and never closed\nLook at line {line_num} {text}")
						break

		return text

	def KILL_ALL_CODE_SWITCHES(self, text: str = None, code_switches: List[CodeSwitch] = None) -> str:
		'''
		:text: if text is None it performs this action on self.code_file
				aka the actual component c file
				else: it performs the algorithm on the argument 'text'
		:code_switches: if code_switches is None it assumes the code_switches are self.code_switches_all
						aka the actual component c file code switches
						else: it performs the algorithm on the argument 'code_switches'

		:returns: text with removed disabled code switches with their content
							removed enabled code switch titles and their #endif
							according to the 'code_switches' given
		'''
		if text == None:
			text = deepcopy(self.code_file)
		if code_switches == None:
			if self.code_switches_all == None:
				return text
			else:
			 code_switches = self.code_switches_all

		text_lines = text.split('\n')
		output_lines = []

		# this algorithm depnds on a sorted list
		code_switches.sort(key=lambda x: x.line_num)
		current_end_line_num = 0
		for code_switch in code_switches:
			
			if code_switch.is_enabled:
				# enabled code switch, add until current code switch title (NOT INCLUDED), then add body, then set next start line number to line after current code switch ending
				output_lines.extend(text_lines[current_end_line_num:code_switch.line_num-1])  # from previous code switch ending to openning of current code switch
				output_lines.extend(text_lines[code_switch.line_num:code_switch.end_line_num-1])  # the body of the enabled code switch
				current_end_line_num = code_switch.end_line_num  # assigning starting line number for the next iteration, after the closing of this code switch
			
			else:
				# disabled code switch, remove the title, the body and the #endif
				output_lines.extend(text_lines[current_end_line_num:code_switch.line_num-1])  # from previous code switch ending to openning of current code switch
				current_end_line_num = code_switch.end_line_num  # assigning starting line number for the next iteration, after the closing of this code switch

		# adding the rest of the code file
		output_lines.extend(text_lines[current_end_line_num:])

		output = "\n".join(output_lines)

		return output
		
	def get_code_switches_all(self):
		'''
		get ALL code switches
		'''
		code_switches: List[CodeSwitch] = []

		terms_to_search_for = ["#ifndef", "#if", "#ifdef", "#elif", "#else"]

		opennings = ["#ifndef", "#if", "#ifdef"]
		closings = ["#elif", "#else", "#endif"]

		lines = self.code_file.split("\n")
		for line_num, line in enumerate(lines):
			for term in terms_to_search_for:
				if term in ForthBlock.KILL_ALL_COMMENTS(line, passive_mode=True):  # code switch term found in a code line

					# getting the index of the line with the next #endif or #elif or #else -> getting the block
					opennings_count = 1
					closings_count = 0
					for line_num2, line2 in enumerate(lines[line_num+1:]):

						# counting openings
						for opening in opennings:
							if opening in ForthBlock.KILL_ALL_COMMENTS(line2, passive_mode=True):
								opennings_count += 1
								break

						# counting closings
						for closing in closings:
							if closing in ForthBlock.KILL_ALL_COMMENTS(line2, passive_mode=True):
								closings_count += 1
								break

						# # for debugging only
						# if line_num == 893 and line_num2 == 32:
						# 	print(line_num+1, line2, "kdjfkd")
						# 	print(opennings_count, closings_count, "abc")

						if opennings_count == closings_count:
							end_line_num = line_num+line_num2+1
							break

					if end_line_num < line_num:
						raise ValueError("COULDN'T FIND END OF CODE SWITCH BLOCK", line_num, end_line_num)

					# Found valid code witch with openning and ending
					code_lines = lines[line_num:end_line_num+1]  # block of code switch, from #if/ifndef/ifdef to #else/elif/endif

					# filtering comments from first line ( the one that has the opening statement, e.g- #IF)
					title = ForthBlock.KILL_ALL_COMMENTS(code_lines[0]).strip()
					
					# filtering comments from last line ( the one that has the opening statement, e.g- #IF)
					ending = ForthBlock.KILL_ALL_COMMENTS(code_lines[-1]).strip()

					function = 'Not assigned yet'

					is_enabled = None

					has_nested_code_switch = False
					if opennings_count > 1:
						has_nested_code_switch = True

					code_switches.append(CodeSwitch(title, ending, code_lines, function, line_num+1, end_line_num+1, is_enabled, has_nested_code_switch))
					break

		if not code_switches:  # didn't find any code switches
			return None

		# finding enabled_disabled stat of every code switch
		code_switches = self.assign_enabled_stat(code_switches)

		return code_switches

	def get_code_switches(self, code_switches):
		"""
		searches the code file for code switches
		"""
		if code_switches:

			# filtering unit testing, swit(hooks)
			# if these keywords are found in the block of the code switch, unwanted keyword filter will not run
			wanted_keywords = ["FUNC(", "LOCAL_INLINE", "STATIC"] #, " if(", " if (", " for(", " for (", " while(", " while ("]  
			# unwanted keyword filter, will only run if no wanted keywords are found within the code switch block
			unwanted_keywords = ["SWIT_", "UNIT_TESTING", "UNIT_TEST"]
			filtered = []
			for ind, code_switch in enumerate(code_switches):

				# getting the corresponding function :) now it's easy
				code_switches[ind].function = self.get_outside_function(self.func_defs, code_switch.line_num)

				title_and_code = code_switch.title + "\n" + "\n".join(code_switch.code)

				for wanted_keyword in wanted_keywords:
					if wanted_keyword in title_and_code:
						filtered.append(code_switch)
						break  # go to next iteration without executing unwanted keyword filter
				else: 
					
					for keyword in unwanted_keywords:
						if keyword in title_and_code:
							break
					else:
						filtered.append(code_switch)

			print(f"Detected {len(filtered)} code switches out of total {len(code_switches)} code switches in the c file")
			return filtered

	def get_code_file(self, component_true_title, raw_search_mode = False, passive_search_mode = False):
		"""
		:param raw_search_mode: passes the argument directly as keyword to search for
								else adetailed_designs .c
		:param passive_search_mode: normally an error is raised if file not found, else only a print() will be executed
		return "<content of .c file", "<path to file>"
		"""

		# getting all_files hashed, only once
		if self.all_files == None:
			self.all_files = {}
			for path in self.paths_to_code:
				path_to_serach_in = self.filter_backslash(path)
				walk_output = os.walk(path_to_serach_in)
				files_not_readable_yet = ['.xlsm', '.png', '.xlsx', '.xls', '.zip', '.docx', '.doc', '.jar', '.gif', '.exe', '.dll', '.bmp', '.lzma', '.xz', '.pdf', '.xdm', '.dat', '.lib', '.tdb', '.a', '.elf', '.jbc', '.pof', '.err']
				for tuple_ in walk_output:
					for file in tuple_[2]:
						if not file[file.find('.', -5):] in files_not_readable_yet:
							
							new_file = self.filter_backslash(tuple_[0] + '/' + file)
							
							# filtering variant files
							if 'Base' in new_file:
								if self.first_block.variant.capitalize() not in new_file:
									continue
							
							last_name = new_file.split('/')[-1].lower()

							if last_name not in self.all_files.keys():
								self.all_files[last_name] = [new_file]
							else:
								self.all_files[last_name].append(new_file)

		# processing search key
		if raw_search_mode:
			name = component_true_title.lower()
		else:
			name = f"{component_true_title}.c".lower()

		### getting the wanted file
		try:
			if len(self.all_files[name]) > 1:
				
				# detected more than one file with the same name
				choosen_file_ind = self.manually_choose_c_file(self.all_files[name])-1

				path = self.all_files[name][choosen_file_ind]
				with open(path, 'r') as f:
					result = f.read()

			else:
				path = self.all_files[name][0]
				with open(path, 'r') as f:
					result = f.read()
		
		except KeyError:
			result = None
			path = None
			if passive_search_mode:
				print(f"\nCouldn't find {name} file in {self.paths_to_code}\n")
			else:
				raise FileNotFoundError(f"\n\nCouldn't find {name} file in {self.paths_to_code}")

		return result, path

	@staticmethod
	def filter_backslash(path):
		"""
		Main use is to let python read paths to a file
		input path as string with backslashes 
		return path with backslashes converted to forwardslashes
		"""
		for ind in range(len(path)):
			if path[ind] == "\\":
				path = path[:ind] + '/' + path[ind+1:]
		return path

	def manually_choose_c_file(self, options):
		'''
		when multiple c file with the same name arise from paths_to_code
		a prompt will arise to ask user which c file to choose form
		'''
		print("Multiple C files of the same name detected:")
		
		###############################################################
		# trying to filter automatically
		filtered = []
		unwanted_keywords = ['/eclipse/plugins/']
		wrong_option_detected = False
		for ind, option in enumerate(options):
			for keyword in unwanted_keywords:
				if '/eclipse/plugins/' in option:
					wrong_option_detected = True
					break

			if wrong_option_detected:
				wrong_option_detected = False  # resetting flag
			else:
				filtered.append(ind)

		if len(filtered) == 1:
			# found one correct file
			return filtered[0]
		###############################################################


		###############################################################
		# automatic filter didn't work, must choose manually
		for ind, option in enumerate(options):
			print(f"{ind+1} - {option}")
		print()

		def recurse(options):
			k = input("Please Enter the number beside the path you want: ")

			# dealing with inputs which couldn't be casted
			try:
				k = int(k)
			except Exception:
				print("Invalid Input, Please input a number!")
				k = recurse(options)

			max_num = len(options)

			if k <= 0 or k > max_num:
				print("Invalid Input, Please enter a number within the displayed range!")
				k = recurse(options)

			return k

		return recurse(options)

	def get_all_funcs(self, code, code_switches, without_code_switch_test = True) -> List[Func]:
		"""
		This function implements an intricate algorithm to detect all C functions, capture them
		and parse them into a Func dataclass, defining all its attributes.

		The main algorithm is made out of 3 steps:
			1- FUNCTION DEF DETECTION ALGORITHM
			2- FUNCTION DEF CAPTURING ALGORITHM
			3- FUNCTION DEF PARSING ALGORITHM

		:param without_code_switch_test: this is by default enabled, it tests the output of func_defs list from a 
										normal c file compared to the output of func_defs output of a file without 
										any code switches.
		"""
		func_defs = []

		code_lines = code.split('\n')

		func_defs_raw = []

		########################################################################################
		# (1) & (2) DETECT AND CAPTURE ALGORITHM
		unwanted_pattern = r'[ \t\n](if|for|while|switch|#if|#elif|#ifdef|#ifndef)[ \t\n]*\('
		code_switch_trigger_words = ['#if', '#ifndef', '#ifdef', '#elif', '#else', '#endif']
		possibly_a_func_counter = 0
		for ind, char in enumerate(code):


			##########################################################################################
			#### (1) FUNCTION DEF DETECTION ALGORITHM
			# Captures all code blocks, if, for, while, etc..
			possibly_a_func = False
			if char == "{": ## { detected
				# test if this really is a function:
				comment_flag = False
				code_switch_flag = False
				is_there_comment = False
				for ind2, char2 in enumerate(code[:ind][::-1]):
					
					# ignoring code switches, activating code_switch_flag
					if char2 == 'f':  # could be the start of a code switch
						# dealing func declaration code that's inside a code switch see VW-MEB project, Branch Q330, Component Idp.c, line: 1696
						# checking if it's an #endif
						if code[:ind][::-1][ind2:ind2+6] == '#endif'[::-1]:
							code_switch_flag = True

					# deactivating code_switch_flag
					if char2 == '#':
						code_switch_flag = False
						continue

					# ignoring comments
					if char2 == '/':
						comment_flag = not comment_flag
						continue

					# ignoring spaces and newlines
					if char2 == ' ' or char2 == '\n' or comment_flag or code_switch_flag:
						continue
					elif char2 == ')':
						#  { detected with ) directly behind it (ignoring comments, spaces and \n)
						# finding the starter of the ) detected
						possibly_a_func = True  # possibly ;)

					break
			########################################################################################



			########################################################################################
			# (2) FUNCTION DEF CAPTURING ALGORITHM
			# capturing functions declaration code (only if it's indeed a function) Algorithm
			if possibly_a_func:

				possibly_a_func_counter += 1
				# ############## FOR DEBUGGING ONLY No.1 ###############
				# # here is look for the text before the { of the function missing
				# if without_code_switch_test:
				# 	print("\n\n############ ONLY FOR DEBUGGING FUNCTION CAPTURING ALGORITHM ##########")
				# 	print(f"Possibly a func counter: {possibly_a_func_counter}:")
				# 	THRESHOLD = 100
				# 	print(code[ind-THRESHOLD:ind])
				# 	print("#######################################################################\n\n")
				# #######################################################

				# extracting function declaration code (could be if/while/etc..) 
				close_brack_count = 0
				open_brack_count = 0
				open_bracket_found = False
				to_be_ignored_chars = [' ', '\t', '\n']
				character_found = False
				for ind3, char3 in enumerate(code[:ind][::-1]):
					
					if not open_bracket_found:
						# finding the openning bracket of the param defs
						# no special case for comments or code switches because it will search for the first bracket
						# VULNERABILITY : if a comment has brackets :(
						if char3 == '(':
							open_brack_count += 1
						if char3 == ')':
							close_brack_count += 1

						if open_brack_count == close_brack_count and open_brack_count != 0:
							# found the end of the bracket, param defs finished
							open_bracket_found = True

							# ############## FOR DEBUGGING ONLY No.2 ###############
							# # if wanted function is found from No.1 debugging
							# # put it here to make sure this step worked
							# if possibly_a_func_counter == 25:
							# 	print("reached herere, Debug No. 2 !!!!!!")
							# 	print(code[:ind][::-1][ind3:ind3+20][::-1])
							# ######################################################

							continue
					
					elif not character_found:
						# finding the nearst character
						if char3 not in to_be_ignored_chars:
							# found a character let's find the start of this line
							character_found = True

							# ############## FOR DEBUGGING ONLY No.3 ###############
							# # if wanted function is found from No.1 debugging
							# # put it here to make sure this step worked
							# if possibly_a_func_counter == 25:
							# 	print("reached herere, Debug No. 3 !!!!!!")
							# 	print(code[:ind][::-1][ind3:ind3+20][::-1])
							# ######################################################

							continue
					else:
						# now we assume we found the last character of the func name (if it's a func block)
						# and we assume the rest of the func def is in the same line
						# and we assume this is a function defined in global scope, not inside another function
						# so now finding the index of the nearst \n 
						if char3 == '\n':
							func_def_start_ind = ind-ind3-1

							# ############## FOR DEBUGGING ONLY No.4 ###############
							# # if wanted function is found from No.1 debugging
							# # put it here to make sure this step worked
							# if possibly_a_func_counter == 25:
							# 	print("reached herere, Debug No. 4 !!!!!!")
							# 	print(code[:ind][::-1][ind3:ind3+20][::-1])
							# ######################################################


							break
				else:
					problem_at_line_num = code[:ind].count('\n')
					print(f"\nPASSIVE ERROR:\nFunction Def Capturing Algorithm loop reached Top of the file.\nStates:\nOpen Bracket Found:{open_bracket_found}\nNormal Character Found: {character_found}\nLook in line: {problem_at_line_num}\n\n")
					continue

				possibly_a_func_def = code[func_def_start_ind:ind]

				# ############## FOR DEBUGGING ONLY No.5 ###############
				# # if wanted function is found from No.1 debugging
				# # put it here to make sure this step worked
				# if possibly_a_func_counter == 25:
				# 	print("reached herere, Debug No. 5 !!!!!!")
				# 	print(possibly_a_func_def)
				# ######################################################
				
				### Filter for func blocks only
				if not re.findall(unwanted_pattern, possibly_a_func_def):
					##### finally a func def is detected and saved ####
					raw_func_def_code = possibly_a_func_def.strip()

					### capturing line number
					start_line_num = code[:ind+1].count("\n")

					### capturing function block
					# look for the next } with understanding of count
					body_start_index = ind+1
					open_brack_count = 0
					close_brack_count = 0
					for ind4, char4 in enumerate(code[ind:]):
						if char4 == '{':
							open_brack_count += 1
						if char4 == '}':
							close_brack_count += 1
						if open_brack_count == close_brack_count:
							body_end_index = ind+ind4
							break
					
					body = code[body_start_index:body_end_index].strip()
					
					### capturing end line number of the body
					end_line_num = code[:body_end_index].count("\n") + 1

					func_defs_raw.append((raw_func_def_code, start_line_num, end_line_num, body))
				
				# ############## FOR DEBUGGING ONLY No.6 ###############
				# else:
				# 	# if wanted function is found from No.1 debugging
				# 	# put it here to make sure this step worked
				# 	if possibly_a_func_counter == 25:
				# 		print("reached herere, Debug No. 6 !!!!!!")
				# 		print("THE FUNCTION IS WRONGLY FILTERED!!!!!")
				# 		print(re.findall(unwanted_pattern, possibly_a_func_def))
				# ######################################################
			########################################################################################


		# ############## FOR DEBUGGING ONLY No.7 ###############
		# if without_code_switch_test:
		# 	name_of_unshown_func = 'CheckNvmReady'
		# 	print("\n\n######## ONLY FOR DEBUGGING FUNCTION CAPTURING ALGORITHM##########")
		# 	for func_def_raw_only in [fn[0] for fn in func_defs_raw]:
		# 		if name_of_unshown_func in func_def_raw_only:
		# 			print(f"FUNC DEF CAPTURING algorithm IS working for FUNC: {name_of_unshown_func}")
		# 			break
		# 	else:
		# 		print(f"FUNC DEF CAPTURING algorithm ISN'T working for FUNC: {name_of_unshown_func}")
		# 	print("##################################################################\n\n")
		# ######################################################


		########################################################################################
		# (3) FUNCTION DEF PARSING ALGORITHM
		# seperating retval and name from parameters and initiating Func
		local_keywords = ['local', 'static']
		for fn, start_line_num, end_line_num, body in func_defs_raw:

			# KILLING ALL COMMENTS >:( 
			fn = ForthBlock.KILL_ALL_COMMENTS(fn).strip()
			fn = fn.replace('#endif', '')
			
			# # for debugging
			# print(fn, start_line_num, end_line_num)

			close_brack_count = 0
			open_brack_count = 0
			found_param_start_ind = False
			for ind, char in enumerate(fn[::-1]):
				# finding param first
				if not found_param_start_ind:
					if char == '(':
						open_brack_count += 1
					if char == ')':
						close_brack_count += 1

					if open_brack_count == close_brack_count and open_brack_count != 0:
						param_start_ind = len(fn) - ind
						found_param_start_ind = True
						param_raw = fn[param_start_ind:-1]
						the_rest = fn[:param_start_ind-1].strip()
						break

			the_rest_words = the_rest.split(" ")
			retval = " ".join(the_rest_words[:-1])
			name = the_rest_words[-1]
			
			# dealing with the freakish parameter attribute
			param_raw_seperated = []
			open_brack_count = 0
			close_brack_count = 0
			new_ind = 0
			for ind6, param in enumerate(param_raw):
				if param == '(':
					open_brack_count += 1
				if param == ')':
					close_brack_count += 1

				if open_brack_count == close_brack_count:
					if param == ',':
						param_raw_seperated.append(param_raw[new_ind:ind6].strip())
						new_ind = ind6+1
			param_raw_seperated.append(param_raw[new_ind:].strip())

			params = []
			for param in param_raw_seperated:
				if " " in param:
					datatype = param.split(" ")[:-1]  # taking everything except the last word, as it is defeinitly the name of the parameter
					datatype = " ".join(datatype)  # ignoring pointer stuff
					if '*' in param.split(" ")[-1]:
						datatype += '*'
						param_name = param.split(" ")[-1].strip(" *")
					else:
						param_name = param.split(" ")[-1].strip()
					params.append((datatype, param_name))
				else:
					list_ = [param]
					params.append(tuple(list_))

			for keyword in local_keywords:
				if keyword in fn.lower():
					is_local = True
					break
			else:
				is_local = False
			
			func_def = Func(name=name, retval=retval, params=params, body=body, start_line_num=start_line_num, end_line_num=end_line_num, is_local=is_local, variant=[])
			
			# # for debugging
			# print(func_def)
			# print()
			# print()
			
			func_defs.append(func_def)

		# finding variant of func def, look for code switch with (ASM/PSM)
		if without_code_switch_test:
			print("NOTE: WHEN FINDING VARIANT OF FUNC DEF IN CODE, PSM IS HARDCODED AS BASE+ AND ASM IS HARDCODED AS BASE-")
			mapping = {True: '+', False: '-'}
			if code_switches:
				for ind, func in enumerate(func_defs):
					for code_switch in code_switches:
						if func.start_line_num > code_switch.line_num and func.start_line_num <= code_switch.end_line_num:
							# this function is inside this codeswitch
							
							# check if this is an ASM/PSM code switch
							base_check = re.search(r"([AaPp][Ss][Mm]) *={0,2} *(\d*)", code_switch.title)
							if base_check:
								base_type, value = base_check.groups()
								if value != '': 
									v = not ('PSM' in base_type or 'psm' in base_type) ^ (not not int(value))
								else:
									v = ('PSM' in base_type or 'psm' in base_type)
								func_defs[ind].variant.append(f"Base{mapping[v]}")
								break
							
					else:
						# function is not inside any code switch, thus thus function is not bound to a specific variant, thus depend on component whether it's both not not
						func_defs[ind].variant.extend(self.component.variant)
		########################################################################################


		########################################################################################
		# Executing this same algorithm for the c file without code switches (remove disabled code switch content 
		#							as well as all code switche statements; titles and endings, e.g #if, #endif)
		if without_code_switch_test:
			
			code_without_code_switches = self.KILL_ALL_CODE_SWITCHES()
			
			func_defs_without_code_switches = self.get_all_funcs(code_without_code_switches, code_switches=None, without_code_switch_test=False)

			names_in_with_code_switches = [func.name for func in func_defs]
			for func in func_defs_without_code_switches:
				if func.name not in names_in_with_code_switches:
					print(f"\nDetected a function {func.name} that could only be detected after removing code switches from C file!!!\nThis could be due to #if/n/def before function initiation block\n")
					func_defs.append(func)
		########################################################################################


		return func_defs

	def merges(self, *args, **kwargs):
		'''
		no merges for code switch analysis, no repeated data
		'''
		return []

	def get_checklist_table(self) -> List[List[str]]:
		'''
		Checklist table
		'''
		output = []
		output.append([ForthBlock.description])
		output.append([ForthBlock.stat, "" if self.stat is None else "Yes" if self.stat else "No"])
		output.append([ForthBlock.code_switch_necessity, "" if self.code_switch_necessity is None else "Yes" if self.code_switch_necessity else "No"])
		output.append([ForthBlock.table, self.get_link_text()])
		return output

	def get_analysis_table(self) -> List[List[str]]:
		'''
		Analysis table
		'''
		output = []

		self.table_start_row_inds = [0]

		output.append(["SN", "SW function with code switch.", "Code switch", "Code switch type", "Comment", "Action"])
		if self.code_switches:
			for sn, code_switch in enumerate(self.code_switches):
				comment = f"Start line num: {code_switch.line_num}, End line num: {code_switch.end_line_num}"
				enabled_disabled_state = '-' if code_switch.is_enabled == None else 'Enabled' if code_switch.is_enabled else 'Disabled'
				output.append([sn+1, code_switch.function, code_switch.title, enabled_disabled_state, comment, ''])
		return output


class FifthBlock(BlockTemplate):
	"""
	5. Code comment for un-required code analysis.		
	"""

	analysis_name = "code_comment"

	description = "5. Code comment for un-required code analysis.	"
	stat = "Does the SW component has comment points to un-intended code?"
	
	def __init__(self, first_block, forth_block):
		self.first_block = first_block
		self.component = self.first_block.component
		self.variant = self.first_block.variant

		self.code_file, self.code_file_path = forth_block.code_file_both
		self.func_defs = forth_block.func_defs
		self.code_comments_all = self.get_code_comments_all()
		self.func_comments, self.non_func_comments = self.get_func_comments()
		self.get_outside_function = forth_block.get_outside_function

		# csv attributes
		if self.code_file:  # code file is found
			
			self.code_comments = self.get_code_comments()

			self.stat = self.get_stat()
			self.code_comment_table = "link the code_coverage_table csv file here"
		else:  # code file is not found

			self.code_comments = None

			self.stat = "Code not found, please insert file manually in input_files/code/code_file"
			self.code_comment_table = "link the code_coverage_table csv file here"

		# output tables
		self.checklist_table = self.get_checklist_table()
		self.analysis_table = self.get_analysis_table()  # initializes self.table_start_row_inds
		self.str_analysis_table = self.get_str_analysis_table()

	def get_stat(self) -> bool:
		'''
		True if it finds either a problematic function comment or a comment with a problematic keyword ['todo', 'fixme', etc..]
		False if nocomments found at all including no non-determinable comments
		'''
		if len(self.code_comments) == 2:
			# aka no comments found except the 2 description comments which are always entered
			return False

		for ind, code_comment in enumerate(self.code_comments):
			if code_comment.comment is not None:
				if "The next comments are ones' that are not possible for the script to detect whether they're problematic or not" in code_comment.comment:
					if ind > 4:
						return True

	def get_code_comments_all(self) -> List[CodeComment]:
		"""
		:returns ALL comments in the file
		"""
		code_comments: List[CodeComment]  = []
		
		code = deepcopy(self.code_file)

		# getting raw comments
		code_comments_raw= []
		opennings = re.finditer(r'[/][*]', code)
		closings = re.finditer(r'[*][/]', code)
		for _ in range(code.count('/*')):

			next_o = next(opennings).span()[0]
			s_line = code[:next_o].count('\n') + 1

			next_c = next(closings).span()[0] + 2
			e_line = code[:next_c].count('\n') + 1

			code_comments_raw.append(CodeComment(comment=code[next_o:next_c], start_line_num=s_line, end_line_num=e_line))

		# grouping group comments into one comment. group comments comments /**..***/ that are not seperated with non comment lines and they start from the beggining of the line
		openned = False
		for ind in range(len(code_comments_raw)-1):

			comment_line = self.code_file.split('\n')[code_comments_raw[ind+1].start_line_num-1].strip()  # to make sure the comment is not next to some piece of code
																										# e.g void func(param)  /* blah blah comment */
																										# it is the raw code file
			if openned:
				if code_comments_raw[ind+1].start_line_num != code_comments_raw[ind].end_line_num + 1 or not comment_line.startswith('/*'):
					openned = False
					comment = "\n".join([code_comment_in.comment for code_comment_in in code_comments_raw[start_ind:ind+1]])
					block_comment = CodeComment(comment, start_line, code_comments_raw[ind].end_line_num)
					code_comments.append(block_comment)
		
			else:
				if code_comments_raw[ind+1].start_line_num == code_comments_raw[ind].start_line_num + 1 and comment_line.startswith('/*'):
					openned = True
					start_ind = ind
					start_line = code_comments_raw[ind].start_line_num
				else:
					code_comments.append(code_comments_raw[ind])
		#134 98
		# detect // \n comments ;)
		code = deepcopy(self.code_file)
		for ind, char in enumerate(code):
			if code[ind:ind+2] == '//':
				
				### detected // comment
				# end index is from where we found the comment plus all the characters until end of line
				next_new_line = ind+2 + code[ind+2:].find('\n')  
				comment = code[ind+2 : next_new_line]
				
				# line number is found by counting all previous '\n'
				start_line_num = code[:ind+1].count('\n') + 1
				end_line_num = start_line_num  # since all // comment ends by starting a newline
				
				code_comments.append(CodeComment(comment, start_line_num, end_line_num))

		return code_comments

	def get_func_comments(self) -> Tuple[List[FuncComment], List[CodeComment]]:
		"""
		Find if a function has a description comment
		Parses the data inside the description comment into a FuncComment
		"""
		func_comments: List[FuncComment] = []
		non_func_comments: List[CodeComment] = []

		#  getting function description comments
		func_comments_raw = []
		for code_comment in self.code_comments_all:
			if "*******************************" in code_comment.comment and ('\\fn' in code_comment.comment or '\\n' in code_comment.comment):
				func_comments_raw.append(code_comment)
			else:
				non_func_comments.append(code_comment)

		#  connecting function description comments with the function definitions
		#  ASSUMES EVERY FUNCTION DESCRIPTION COMMENT HAS A FUNCTION DECLARATION IN CODE
		#  look for the nearst function definition after the end line num of the code comment
		func_defs_start_line_nums = [func_def.start_line_num for func_def in self.func_defs]
		refrence_FF = {func_def.start_line_num: ind for ind, func_def in enumerate(self.func_defs)}
		for code_comment in func_comments_raw:
			line_FF = code_comment.end_line_num
			while line_FF not in func_defs_start_line_nums:
				line_FF += 1
				if line_FF > self.code_file.count('\n'):
					raise ValueError(f"This should never run (infinite loop prevented)\nProbably a function comment is there without a function declaration afterwards\nLook at line {code_comment.end_line_num}")
			code_comment.type_ = ''
			code_comment.function = ''
			self.func_defs[refrence_FF[line_FF]].func_comment = FuncComment(code_comment=code_comment)

			##### parsing name, param, retval, brief, returns and ref from function description comment
			# name			
			if self.func_defs[refrence_FF[line_FF]].name in code_comment.comment:
					self.func_defs[refrence_FF[line_FF]].func_comment.name = self.func_defs[refrence_FF[line_FF]].name
			else:
				name_matches = re.findall(r"[\\][Ff][Nn] +([\w_*; ]+)\(?", code_comment.comment)  # name; is assumed to be only one
				if name_matches:
					name = name_matches[0].strip().split(' ')[-1]
					self.func_defs[refrence_FF[line_FF]].func_comment.name = name
				else:
					print(f"Couldn't parse 'name' data from function comment:\n{code_comment.comment}")


			# param
			# finding param matches
			# finding line index of param paragraphs 
			for param in self.func_defs[refrence_FF[line_FF]].params:
				if param[-1] not in code_comment.comment:  # param not in comment, trying to find if there is another wrong parameter
					# print("happened\n\n")
					break
			else:
				self.func_defs[refrence_FF[line_FF]].func_comment.params = [i[-1] for i in self.func_defs[refrence_FF[line_FF]].params]
		
			# brief
			brief_matches = re.findall(r"[\\][Bb]rief +([\w\d \n*]+)[\\]?/?", code_comment.comment)  # brief; is assumed to be only one
			if brief_matches:
				brief = brief_matches[0]
				self.func_defs[refrence_FF[line_FF]].func_comment.brief = brief

		func_comments = [func.func_comment for func in self.func_defs if func.func_comment != None]

		return func_comments, non_func_comments

	def get_code_comments(self) -> List[CodeComment]:
		"""
		searches code file and filters for the one line code comment as well as one with obvious keywords
		:returns: problematic code comments that will be put in the output
		"""
		
		# extracting function comments that doesn't match the functions they're commenting
		problematic_comments = []
		problematic_func_comments = []
		found_problematic_func_comment = False
		for func in self.func_defs:
			if not func.matches_comment:
				found_problematic_func_comment = True
				problematic_func_comments.append(func.func_comment)
				problematic_comments.append(func.func_comment.code_comment)

		if not found_problematic_func_comment:
			problematic_comments.append(CodeComment("Scipt didn't find any function desciping comment that doesn't match the function declaration it's commenting", None, None, type_=None, function=None))

		print(f"number of function comments: {len(self.func_comments)}")
		print("function comments that don't match function declaration code: ", len(problematic_func_comments))
		
		# extracting definitly prolematic
		problematic_patterns = [r"todo", r"fixme", r"don't use", r"do not use", r"remove", r"why", r"cz", r"not implemented"]
		non_func_comments_filtered = []
		found_problematic_pattern = False
		print("length of non_func_comments:", len(self.non_func_comments))
		for code_comment in self.non_func_comments:
			for pattern in problematic_patterns:
				if pattern in code_comment.comment.lower():
					code_comment.type_ = pattern.upper()
					code_comment.function = self.get_outside_function(self.func_defs, code_comment.start_line_num)
					problematic_comments.append(code_comment)
					found_problematic_pattern = True
					break
			else:
				non_func_comments_filtered.append(code_comment)

		if not found_problematic_pattern:
			problematic_comments.append(CodeComment(f"Script didn't find any comment with keywords: {problematic_patterns}", None, None, type_=None, function=None))


		# Filtering all normal comments
		non_problematic_patterns = ["********", "================", "\\defgroup", "do nothing", "series_production", "a2l_type", "@{", "@}", '@@', 'PRQA']  # REMEMBER** write the keywords in non-capital letters as all comments are .lower() before testing
		remaining_undecided_comments = []
		for code_comment in non_func_comments_filtered:
			for pattern in non_problematic_patterns:
				if pattern in code_comment.comment.lower():
					break
			else:
				code_comment.type_ = ''
				code_comment.function = self.get_outside_function(self.func_defs, code_comment.start_line_num)
				remaining_undecided_comments.append(code_comment)

		print("remaining_undecided_comments: ", len(remaining_undecided_comments))

		# returning problematic comments first, then a note, then the remaining undecided comments
		result = []
		result.extend(problematic_comments)
		result.append(CodeComment(None, None, None))
		result.append(CodeComment(None, None, None))
		result.append(CodeComment(None, None, None))
		result.append(CodeComment("The next comments are ones' that are not possible for the script to detect whether they're problematic or not", None, None, type_=None, function=None))
		result.append(CodeComment(None, None, None))
		result.append(CodeComment(None, None, None))
		result.append(CodeComment(None, None, None))
		result.extend(remaining_undecided_comments)

		return result

	def merges(self, *args, **kwargs):
		'''
		no merges for code comment analysis, no repeated data
		'''
		return []

	def get_checklist_table(self) -> List[List[str]]:
		'''
		Checklist table
		'''
		output = []
		output.append([FifthBlock.description])
		output.append([FifthBlock.stat, "" if self.stat is None else "Yes" if self.stat else "No"])
		output.append([FifthBlock.table, self.get_link_text()])
		return output

	def get_analysis_table(self) -> List[List[str]]:
		'''
		Analysis Table
		'''
		output = []

		self.table_start_row_inds = [0]

		output.append(["SN", "SW function with code comment.", "Code comment", "Code comment type", "Comment", "Action"])
		if self.code_comments:
			for sn, code_comment in enumerate(self.code_comments):
				if code_comment.func_type: #TODO: this line doesn't work anymore!!!!
					comment = f"This function description comment doesn't match the function it's descriping at line either by name or param: {code_comment.start_line_num}"
					output.append([sn+1, code_comment.function, code_comment.comment, code_comment.type_, comment, ""])
				elif code_comment.comment == None:
					output.append([sn+1])
				else:
					comment = f"Starts at line:{code_comment.start_line_num} and ends at line: {code_comment.end_line_num}"
					output.append([sn+1, code_comment.function, code_comment.comment, code_comment.type_, comment, ""])
		return output


class SixthBlock(BlockTemplate):
	"""
	6. Detailed design contained function analysis.	
	"""

	analysis_name = 'detailed_design'

	description = '6. Detailed design contained function analysis.	'
	stat = "Does all the DD functions required in the SW component by SW requirements?"

	def __init__(self, first_block, fifth_block):
		self.first_block = first_block
		self.component = self.first_block.component
		self.variant = self.first_block.variant
		# self.func_comments = fifth_block.func_comments_output  #TODO: delete this line
		self.func_defs = fifth_block.func_defs

		self.dd_func_name_unmatch = None
		self.func_dd_name_unmatch = None
		self.req_with_no_dd = None
		self.diag_with_no_dd = None
		self.dd_no_comp_matches = None
		self.detailed_design = self.get_detailed_design()

		self.stat = self.get_stat()

		# output tables
		self.checklist_table = self.get_checklist_table()
		self.analysis_table = self.get_analysis_table()  # initializes self.table_start_row_inds
		self.str_analysis_table = self.get_str_analysis_table()

	def get_stat(self) -> bool:
		'''
		True if it didn't find any non 'Yes' comments, aka no problematic detailed_designs
		'''
		for dd in self.detailed_design:
			if dd.comment != 'Yes':
				return False
		else:
			return True

	def get_detailed_design(self) -> List[DetailedDesign]:
		"""
		reads polarian's output of DD's, matches them to their SW component then check whether they have SW requirements or Diagnostics or not
		** special treatment for wrappers ;(( **

		return list of problematic DetailedDesign Objects
		"""
		output = []

		for ind, dd in enumerate(self.component.detailed_designs):
			dd.comment = ""

			# check if DD has a variant
			if not dd.variant:
				dd.comment += "- This DD has Empty Variant Attribute\n"
			
			# if it does have a variant it should be a variant we are analyzing
			elif not self.first_block.variant.capitalize() in dd.variant:
				dd.comment += "- The variant of this DD is different from the variant of the current component being analysed\n"

			# check if DD has a component attached to it
			if not dd.check_sw_component():
				dd.comment += "- DD is not attached to SW component\n"
			
			# checking if DD has requirements or diagnostics			
			if not dd.check_req_diag():  # checking if component has req or diag
				dd.comment += "- No requirements or Diagnostics found\n"

			# checking each req in the dd if the req itself is linked to the dd. Same for diagnostics
			else:  
				for req in dd.requirements:
					for dd2 in req.detailed_designs:
						if dd2.ID == dd.ID:
							# print(req.title, dd.title, dd2.title, 'MATCH!!!')
							break
					else:
						comment += f"- Requirement: '{req.title}' with ID '{req.ID} doesn't have DD: '{DD.title}' with ID: '{dd.ID}' in its attributes while the DD has the requirement in its attributes\n"
						print(req.title, dd.title, dd2.title, 'No match found')

				for diag in dd.diagnostics:
					for dd2 in diag.detailed_designs:
						if dd2.ID == dd.ID:
							# print(diag.title, dd.title, dd2.title, 'MATCH!!!')
							break
					else:
						comment += f"- Diagnostic: '{diag.title}' with ID '{diag.ID} doesn't have DD: '{DD.title}' with ID: '{dd.ID}' in its attributes while the DD has the diagnostic in its attributes\n"
						print(diag.title, dd.title, dd2.title, 'no match found')

			if dd.comment == '':
				dd.comment = 'Yes'

			self.component.detailed_designs[ind] = dd

		output.extend(self.component.detailed_designs)

		# checking that all dd has SW component
		dd_no_comp_matches = []
		for dd in self.component.detailed_designs:
			if not dd.component:
				print(f"DD: {dd.title} has no component attached to it")
				dd_no_comp_matches.append(dd)
		if dd_no_comp_matches:
			self.dd_no_comp_matches = dd_no_comp_matches

		# checking that all function in code has dd
		dd_func_name_unmatch = []
		dd_names = [dd.title.lower() for dd in self.component.detailed_designs]
		for func in self.func_defs:
			if func.name.lower() not in dd_names:
				dd_func_name_unmatch.append(func)
				print(f"Function: {func.name} doesn't have DD")
		if dd_func_name_unmatch:
			self.dd_func_name_unmatch = dd_func_name_unmatch

		# checking that all dd has a function in code
		func_dd_name_unmatch = []
		func_names = [func.name.lower() for func in self.func_defs]
		for dd in self.component.detailed_designs:
			if dd.title.lower() not in func_names:
				func_dd_name_unmatch.append(dd)
				print(f"DD: {dd.title} doesn't have function")
		if func_dd_name_unmatch:
			self.func_dd_name_unmatch = func_dd_name_unmatch

		# checking the requirements/diagnostics attached to the component if they have dd or not at all(doens't matter if they have dd not attached to component)
		req_with_no_dd = []
		for req in self.component.requirements:
			if not req.detailed_designs:
				req_with_no_dd.append(req)
		if req_with_no_dd:
			self.req_with_no_dd = req_with_no_dd

		diag_with_no_dd = []
		for diag in self.component.diagnostics:
			if not diag.detailed_designs:
				diag_with_no_dd.append(diag)
		if diag_with_no_dd:
			self.diag_with_no_dd = diag_with_no_dd


		return self.component.detailed_designs

	def merges(self, starting_row_num, sheet_id):
		'''
		For DD analysis table need to merge SN, DD ID and DD name columns
		as they do sometimes get repeated becaues one DD might have more 
		than one requirement or diagnostic

		:return: list of merge data (gridRange Json data) that will be put in .extend in the all_merges list 
		when creating it in GoogleSheet.get_all_analysis_sheet_merges()
		'''
		merge_data = GoogleSheet.get_merges_list(self.str_analysis_table, [0, 1, 2], starting_row_num, sheet_id)

		return merge_data

	def get_checklist_table(self):
		output = []
		output.append([SixthBlock.description])
		output.append([SixthBlock.stat, "" if self.stat is None else "Yes" if self.stat else "No"])
		output.append([SixthBlock.table, self.get_link_text()])
		return output

	def get_analysis_table(self):
		output = []
		
		#### MAIN TABLE	####
		output.append(["SN", "D.D function ID", "D.D function", "Linked SW requirement", "SW Requirement ID", "Is DD function against SW requiremnet required by VW?", "variant", "Comments"])
		
		self.table_start_row_inds = [0]

		counter = 1
		if self.detailed_design:
			for dd in self.detailed_design:

				if dd.status == 'Created':
					extra_column = 'DD has status Created'
				else:
					extra_column = ''

				if dd.check_req_diag():

					for req in dd.requirements:
						# output.append([counter, dd.ID, dd.title, req.title, req.ID, dd.comment, f"Applicable for: {req.variant}", extra_column,
						# 	'Please remove the next two cells after manually checking', dd.description, req.description])
						output.append([counter, dd.ID, dd.title, req.title, req.ID, dd.comment, f"Applicable for: {req.variant}", extra_column])

					for diag in dd.diagnostics:
						# output.append([counter, dd.ID, dd.title, diag.title, diag.ID, dd.comment, f"Applicable for: {diag.variant}", extra_column,
						# 	'Please remove the next two cells after manually checking',dd.description ,diag.description])
						output.append([counter, dd.ID, dd.title, diag.title, diag.ID, dd.comment, f"Applicable for: {diag.variant}", extra_column])

				else:
					output.append([counter, dd.ID, dd.title, '', '', dd.comment, '', extra_column])
				
				counter += 1
		
		else:  # what happens if no dd found at all for the whole component?!?
			output.append(["This component has no detailed_designs"])  


		#### EXTRA TABLES ####
		# DDS that doesn't have a component attached to
		if self.dd_no_comp_matches:

			output.append(["detailed_designs that doesn't have component attached to it"])
			
			self.table_start_row_inds.append(len(output))

			output.append(['No.', 'Name', 'ID'])
			counter = 1
			for dd in self.dd_no_comp_matches:
				output.append([counter, dd.title, dd.ID])
				counter += 1

		# DDs that doesn't have a function in code
		if self.dd_func_name_unmatch:

			output.append(["Functions that doesn't have detailed design in polarian"])

			self.table_start_row_inds.append(len(output))

			output.append(['No.', 'Name', 'Comment'])
			counter = 1
			for func in self.dd_func_name_unmatch:
				output.append([counter, func.name, f"line number: {func.start_line_num+1}"])
				counter += 1

		# Functions in code that doesn't have a DD
		if self.func_dd_name_unmatch:
			
			output.append(["detailed_designs that doesn't have a function implementation in code "])
			
			self.table_start_row_inds.append(len(output))
			
			output.append(['No.', "Name", "ID", "Comment"])
			counter = 1
			for dd in self.func_dd_name_unmatch:
				output.append([counter, dd.title, dd.ID])
				counter += 1

		# Requirements that doesn't have any DD attached to it
		if self.req_with_no_dd:

			output.append(["Requirements that doesn't have detailed designs attached to it"])

			self.table_start_row_inds.append(len(output))

			output.append(['No.', 'Name', "ID"])
			counter = 1
			for req in self.req_with_no_dd:
				output.append([counter, req.title, req.ID])
				counter += 1

		# Diagnostics that doesn't have any DD attached to it
		if self.diag_with_no_dd:

			output.append(["Diagnostics that doesn't have detailed designs attached to it"])

			self.table_start_row_inds.append(len(output))

			output.append(['No.', 'Name', "ID"])
			counter = 1
			for diag in self.diag_with_no_dd:
				output.append([counter, diag.title, diag.ID])
				counter += 1
		
		return output


class SeventhBlock(BlockTemplate):
	"""
	7. Code review against SW requirements analysis.	
	"""

	analysis_name = 'code_review'

	description = '7. Code review against SW requirements analysis.	'
	stat = 'Does the code of the SW component has un-inteneded code versus SW requirements?'
	
	def __init__(self, first_block, fifth_block, sixth_block):
		self.first_block = first_block
		self.component = first_block.component
		self.variant = first_block.variant
		self.func_defs = fifth_block.func_defs  
		self.detailed_design = sixth_block.detailed_design

		self.repeated_functions = None

		self.code_reviews = self.get_code_reviews()

		self.stat = self.get_stat()

		# output tables
		self.checklist_table = self.get_checklist_table()
		self.analysis_table = self.get_analysis_table()  # initializes self.table_start_row_inds
		self.str_analysis_table = self.get_str_analysis_table()

	def get_code_reviews(self) -> List[CodeReview]:
		"""
		return list of CodeReview objects
		"""
		code_reviews = []
		repeated_functions = []
		
		for func in self.func_defs:
			found_flag = False
			for dd in self.component.detailed_designs:
				if func.name.lower() == dd.title.lower():
					# found same name, CAPTURE IT!
					captured_dd = dd
					found_flag = True

					# checking for any similar variant between the variants in dd and func
					if not not set(captured_dd.variant).intersection(set(func.variant)):
						# dd has same name and variant as func -> best match
						code_reviews.append(CodeReview(func, captured_dd, does_variant_match_dd=True))
						break  # found_flag logic will not run
					
			else:
				if found_flag:
					code_reviews.append(CodeReview(func, captured_dd, does_variant_match_dd=False))
				else:
					code_reviews.append(CodeReview(func, None))

			if [i.func.name for i in code_reviews].count(func.name) > 1:
				print(f"Found Repeated function with name: {func.name}")
				repeated_functions.append(func)

		self.repeated_functions = repeated_functions

		return code_reviews

	def get_stat(self) -> bool:
		"""
		False if it finds a problematic code review e.g-(one that has no DD), else None as script can't test descriptions
		"""
		# for code_review in self.code_reviews:
		# 	if not code_review.state:
		# 		return False
		# else:
		return None  # script can't (and will probably never) be able to do complete code review!

	def merges(self, starting_row_num: int, sheet_id: int) -> List[Dict]:
		'''
		For DD analysis table need to merge SN, DD ID and DD name columns
		as they do sometimes get repeated becaues one DD might have more 
		than one requirement or diagnostic

		:param starting_row_num: the row the table starts from
		:sheet_id: for google sheet api, must give sheet id

		:return: list of merge data (gridRange Json data) that will be put in .extend in the all_merges list 
		when creating it in GoogleSheet.get_all_analysis_sheet_merges()
		'''
		all_merge_data: List[Dict] = GoogleSheet.get_merges_list(self.str_analysis_table, [0, 2], starting_row_num, sheet_id)

		# getting the merges for local global column
		# we can't use the normal methods because two consecutive functions could be local
		# thus the merge function will merge all
		# The solution is to read the previous merges and assign new merges on the second col
		# depending on the previous merges (of first column)
		new_merge_data_list = []
		for merge_data in all_merge_data:
			
			# copy from the first column first, Don't want duplicate merge data!
			if merge_data['startColumnIndex'] != 0:
				break

			new_merge_data = deepcopy(merge_data)
			new_merge_data['startColumnIndex'] = 1
			new_merge_data['endColumnIndex'] = 2
			new_merge_data_list.append(new_merge_data)

		all_merge_data.extend(new_merge_data_list)

		return all_merge_data

	def get_checklist_table(self):
		output = []
		output.append([SeventhBlock.description])
		output.append([SeventhBlock.stat, "" if self.stat is None else "No" if self.stat else "Yes"])
		output.append([SeventhBlock.table, self.get_link_text()])
		return output

	def get_analysis_table(self):
		output = []
		output.append(["SN", "Function type", "Function", "Brief", "Covered SW Requirement", "SW Requirement ID", "Issues", "Requirement type", "Requirement brief", "Does the code covers the SW requirements only?"])
		
		self.table_start_row_inds = [0]

		counter = 1
		for code_review in self.code_reviews:

			### state ###
			state = ''
			# check if no dd
			if code_review.dd == None:
				state = 'No'

			### issues ###
			issues = ''
			# check if no dd
			if code_review.dd == None:
				issues += "Function has no DD.\n"
			else:
				# check if func variant matches dd
				if not code_review.does_variant_match_dd:
					issues += f"This function is implemented under code switches of variant {code_review.func.variant} which is different from its DD which is {code_review.dd.variant}.\n"

				# check if dd has req/diag
				if not code_review.dd.check_req_diag():
					issues += "DD has no requirement OR Diagnostics.\n"

			# check if func variant matches wanted
			if not set(code_review.func.variant).intersection(set([self.first_block.variant.capitalize()])):
				issues += f"This function is implemented under code switches of variant {code_review.func.variant} which is different from current component variant {self.first_block.variant.capitalize()}.\n"

			locality = 'Local' if code_review.func.is_local else 'Global'
			# brief = code_review.func.func_comment.brief if code_review.func.func_comment else "Function has no brief in code"


			if code_review.dd:

				description = code_review.dd.description
				desc_lines = description.split('\n')
				description = ""
				for line in desc_lines:
					if '\t' in line or line == "":
						continue
					else:
						description += line

				if code_review.dd.check_req_diag():  # function have dd, dd have req/diag
					for req in code_review.dd.requirements:
						output.append([counter, locality, code_review.func.name, description, req.title, req.ID, issues, "SW Requirement", req.description, state])
					
					for diag in code_review.dd.diagnostics:
						output.append([counter, locality, code_review.func.name, description, diag.title, diag.ID, issues, "SW Diagnostic", diag.description, state])
				
				else:  # dd of function doesn't req/diag
					output.append([counter, locality, code_review.func.name, description, "", "", issues, "", "", state])
			
			else:  # function doesn't have dd
				output.append([counter, locality, code_review.func.name, "", "", "", issues, "", "", state])

			counter += 1

		# for repeated functions
		if self.repeated_functions:

			output.append(['Functions initiated more than once in code'])
			
			self.table_start_row_inds.append(len(output))

			output.append(['SN', 'Name', 'Line number'])
			counter = 1
			for func in self.repeated_functions:
				output.append([counter, func.name, f"Line {func.start_line_num}"])
				counter += 1

		return output
########################################################################################################################################



########################################################################################################################################
#### Main Functions

# External and Internal (put in __all__) Functions
def set_wanted_directory(homedir_in):
	'''
	Meant to be called from a user script, e.g- a CLI
	sets the home directory the user will interact with
	This is done by calling an internal function in the main script itself
	e.g - put polarian csv files in, get output files, etc..
	'''
	set_wanted_directory_internal(homedir_in)

def read_assign_all_CSVs():
	'''
	reads and assigns all csvs to internal class variable cls.all_objects
	'''
	Component.get_all_from_csv(assign_class_variable=True, hash_key='ID')

	DetailedDesign.get_all_from_csv(assign_class_variable=True, hash_key='ID')

	Diagnostic.get_all_from_csv(assign_class_variable=True, hash_key='ID')

	Requirement.get_all_from_csv(assign_class_variable=True, hash_key='ID')

	Interface.get_all_from_csv(assign_class_variable=True, hash_key='ID')

def create_blocks(component, variant, branch, paths_to_code, path_to_reports, path_to_tcc, my_polarian_web_link):
	"""
	return list of blocks
	"""

	blocks = []
	if component.CAT_num == 1:	
		blocks.append(FirstBlock(component, variant, branch, paths_to_code, path_to_reports, path_to_tcc, my_polarian_web_link))
		blocks.append(SecondBlock(blocks[0]))
		blocks.append(ThirdBlock(blocks[0]))
		blocks.append(ForthBlock(blocks[0]))
		blocks.append(FifthBlock(blocks[0], blocks[3]))
		blocks.append(SixthBlock(blocks[0], blocks[4]))
		blocks.append(SeventhBlock(blocks[0], blocks[4], blocks[5]))

	elif component.CAT_num == 2:
		blocks.append(FirstBlock(component, variant, branch, paths_to_code, path_to_reports, path_to_tcc))
		blocks.append(SecondBlock(blocks[0]))
		blocks.append(ThirdBlock(blocks[0]))
		blocks.append(ForthBlock(blocks[0]))
		blocks.append(FifthBlock(blocks[0], blocks[3]))
		blocks.append(SixthBlock(blocks[0], blocks[4]))

	elif component.CAT_num == 3:
		blocks.append(FirstBlock(component, variant, branch, paths_to_code, path_to_reports, path_to_tcc))
		blocks.append(SecondBlock(blocks[0]))
		blocks.append(ThirdBlock(blocks[0]))
		blocks.append(ForthBlock(blocks[0]))
		blocks.append(FifthBlock(blocks[0], blocks[3]))

	# Updating first block analysis_stat attribute after running all blocks :)
	blocks[0].update_analysis_stat(blocks)

	return blocks

# Internal Only Functions
def main(homedir, component_name, CAT_num, branch, variant, paths_to_code_in, path_to_reports_in, path_to_tcc_in, my_polarian_web_link_in):
	'''
	Does all the steps necessary to start analyzing a component
	Meant to be used here in this file internally for rapid debugging
	'''
	### set the directory
	set_wanted_directory(homedir)

	### Read CSV files
	print("Reading polarian csv outputs and parsing data....")
	read_assign_all_CSVs()

	# get wanted component object and linking it to all linked workitems
	print(f"Finding Component: {component_name} in Polarian\n")
	wanted_component = Component.get_component(component_name, CAT_num, branch)
	if wanted_component.found_in_polarian:
		print(f"Found Component: {wanted_component.true_title} in Polarian!\n")

	### Commencing the Analysis
	# Running all bocks
	print(f"Starting analysis for {wanted_component.title} of variant {variant} of ID {wanted_component.ID}\nand Document name '{wanted_component.document}'\n\n")
	blocks = create_blocks(wanted_component, variant, branch, paths_to_code, path_to_reports, path_to_tcc, my_polarian_web_link)
	print('\nAnalysis is Completed Successfully!!!\n')

	# Export outputs as CSVs
	export_csv(blocks)

	# Export output in a Google Sheet
	WorkItem.assign_validate_polarian_link(my_polarian_web_link_in)
	google_sheet = GoogleSheet(blocks)
	google_sheet.copy_link_to_clipboard()
	google_sheet.save_link_in_txt_file()

def set_wanted_directory_internal(homedir_in):
	'''
	sets homedir for the main script itself
	'''
	global homedir
	homedir = homedir_in
	os.chdir(homedir)
########################################################################################################################################



########################################################################################################################################
#  Exports

def export_csv(blocks: List):
	"""
	export csv file for the list of blocks inputed
	"""
	#exporting the main template
	Path(f"output/csv/{blocks[0].component.true_title}").mkdir(parents=True, exist_ok=True)
	with open(f"output/csv/{blocks[0].component.true_title}/{blocks[0].name}_{blocks[0].variant}.csv", mode='w', encoding='utf-8') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
		
		print("Exporting Main Analysis Sheet")
		for block in blocks:
			for row in block.checklist_table:
				csv_writer.writerow(row)
			for _ in range(BlockTemplate.num_empty_rows_between_tables):
				csv_writer.writerow([])

	#exporting the analysis template
	Path(f"output/csv/{blocks[0].component.true_title}").mkdir(parents=True, exist_ok=True)
	with open(f"output/csv/{blocks[0].component.true_title}/{blocks[0].name}_{blocks[0].variant}_analysis_tables.csv", mode='w', encoding='utf-8') as csv_file:
		csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
		
		print("Exporting Analysis tables Sheet")
		for block in blocks[1:]:
			for row in block.analysis_table:
				csv_writer.writerow(row)
			for _ in range(BlockTemplate.num_empty_rows_between_tables):
				csv_writer.writerow([])

	# exporting the internal files for each block
	Path(f"output/csv/{blocks[0].component.true_title}/inner_tables").mkdir(parents=True, exist_ok=True)
	for block in blocks[1:]:
		with open(f"output/csv/{blocks[0].component.true_title}/inner_tables/{block.analysis_name}_{blocks[0].name}_{blocks[0].variant}.csv", mode='w', encoding='utf-8') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
			print(f"Exporting detail table for {block.analysis_name}")
			for row in block.analysis_table:
				csv_writer.writerow(row)


	print(f"Exported CSV files for {blocks[0].variant}\n######################################\n\n")

class GoogleSheet:  
	'''
	Class to manage the creation and modification of google sheet exports
	'''

	checklist_sheet_name = 'Checklist'
	checklist_sheet_id = 1670875314
	checklist_sheet_index = 0
	
	analysis_sheet_name = 'Analysis'
	analysis_sheet_id = 62458818
	analysis_sheet_index = 1

	# If modifying these scopes, delete the file token.json.
	SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

	path_to_json_files = 'input_files/json_files/'

	colors = {
		'yellow': {'blue': 0.6, 'green': 0.8980392, 'red': 1},

		# 'grey': {'blue': 0.6, 'green': 0.8980392, 'red': 1},  #TODO:

		'black': {'blue': 0, 'green': 0, 'red': 0},

		'white': {'blue': 1, 'green': 1, 'red': 1},

		'light_blue': {'blue': 0.8, 'green': 0.33333334, 'red': 0.06666667}
	}

	def __init__(self, blocks: List):
		'''
		creating the google sheet
		'''
		self.blocks = blocks

		# self.create_checklist_sheet()
		self.spreadsheetId = self.create()

	@property
	def link(self):
		'''
		return link to google sheet directly
		'''
		try:
			return f"https://docs.google.com/spreadsheets/d/{self.spreadsheetId}/edit#gid=0"
		except AttributeError:
			return ''

	def save_link_in_txt_file(self):
		'''
		creates a .txt file and saves the sheet link in it
		'''
		Path('output/GoogleSheets/').mkdir(parents=True, exist_ok=True)
		with open(f"output/GoogleSheets/{self.blocks[0].component.true_title}_{self.blocks[0].SW_release}_GoogleSheet_link.txt", 'w') as file:
			file.write(self.link)
			print(f"Saved GoogleSheet link in 'output/GoogleSheets/{self.blocks[0].component.true_title}_{self.blocks[0].SW_release}_GoogleSheet_link.txt' file!")

	def copy_link_to_clipboard(self):
		'''
		uses pyperclip to copy link to spreadsheet to clipboard
		'''
		if self.link != '':
			pyperclip.copy(self.link)
			print("\nCopied link to created sheet in clipboard!\n")

	@staticmethod
	def get_transpose(rows: List[List]) -> List[List]:
		'''
		gets the transpose of a table
		'''
		transpose = []
		for row_ind, row in enumerate(rows):
			for value_ind, value in enumerate(row):
				if len(transpose) < (value_ind+1):
					transpose.append([])
				transpose[value_ind].append(value)

		return transpose

	@staticmethod
	def convert_num_to_letters(num: int) -> str:
		'''
		converts number of column to letter notation
		e.g  24 -> X
			 27 -> AA
		'''
		
		alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		len_alphabets = len(alphabets)
		alphabet_mapping = {n+1: alphabets[n] for n in range(len_alphabets)}

		result = ""
		
		if num <= 0:
			raise ValueError("Column numbers start from 1 onwards only!")

		while num > len_alphabets:
			original_num = deepcopy(num)
			num = num // len_alphabets
			reminder = original_num % len_alphabets
			if reminder == 0:
				reminder = 26
				num = num - 1
			result += alphabet_mapping[reminder]

		original_num = deepcopy(num)
		result += alphabet_mapping[original_num]

		return result[::-1]

	@staticmethod
	def get_A1_notation(table: List[List], sheet_title=None, start_col=1, start_row=1) -> Tuple[str, int]:
		'''
		:param table: the values to be written inside a sheet, list of list, list of rows of values
		
		
		:returns: string of A1 notation of the range of the input table
					e.g - 2x2 table, [[1, 2], [3, 4]] 
							return "wanted_sheet_title!A1:B2"

							It also account for starting column and starting row,
							if the user inputed them
		'''

		# the max row value 
		max_row_value = len(table) + start_row

		# get the list with highest number of values -> get max column value
		max_col_value = 0
		for row in table:
			current_max_value = len(row)
			if current_max_value > max_col_value:
				max_col_value = current_max_value
		max_col_value += start_col

		start_col = GoogleSheet.convert_num_to_letters(start_col)
		start_row = start_row

		end_col = GoogleSheet.convert_num_to_letters(max_col_value-1)
		end_row = max_row_value-1

		if sheet_title:
			A1_notation = f"{sheet_title}!{start_col}{start_row}:{end_col}{end_row}"
		else:
			A1_notation = f"{start_col}{start_row}:{end_col}{end_row}"

		return A1_notation

	def read_json_file(self, file_name) -> Dict:
		'''
		reads json file and return json data (basically it's a dictionary)
		'''
		with open(f'{GoogleSheet.path_to_json_files}{file_name}', 'r') as json_file:
			return eval(json_file.read())

	@staticmethod
	def get_hyperlink_web_link(cell_value: str) -> str:
		'''
		Meant for cells under column with title ID of a table
		:return: polarian link to the this ID
		'''
		return f"{WorkItem.my_polarian_web_link}workitem?id={cell_value}"

	def create_cell(self, value: str, no_border = False, border: List[str] = [], alignment: str = 'c', background_color: str = 'white', 
																	bold: bool = False, attach_polarian_hyperlink: bool = False) -> Dict:
		'''
		return proper cellData in json data form (dictionary)

		{
			'effectiveFormat': 
			{
				object (CellFormat)
			}


			'effectiveValue':
			{
				object (ExtendedValue)
			}
		}

		This function assumes the cell is in a table
		:param value: the string value inside the cell
		:param border: list of one of values 'r', 'l', 'u', 'b' which will determine thick border line for up, left, right or bottom 
		:param alignment: defaulted to 'l' which is left, 'r' for right and 'c' for center
		:param background_color: input directly in the class variable color like this GoogleSheet.colors[background_color]
		:param bold: makes text bold (for title rows)
		:param hyperlink: defaulted to None, no hyperlink, else input is the tuple of name of sheet, row as integer and col as integer (both start from 1 !! )
		
		:return: cellData json data (dictionary) (exactly like the shown up)
		'''
		alignments = {'l': 'LEFT', 'r': 'RIGHT', 'c': 'CENTER'}

		cell = {
		    'userEnteredFormat': 
		    {     
		            'backgroundColorStyle': 
		            {
		                'rgbColor': GoogleSheet.colors[background_color]
		            },


		            'borders': 
		            {
		                  'bottom': 
		                  {
		                        'color': {},
		                        'colorStyle': {'rgbColor': {}},
		                        'style': 'SOLID_MEDIUM' if 'b' in border else "SOLID",
		                  },
		                  'left': 
		                  {
		                        'color': {},
		                        'colorStyle': {'rgbColor': {}},
		                        'style': 'SOLID_MEDIUM' if 'l' in border else "SOLID",
		                  },
		                  'right': 
		                  {
		                        'color': {},
		                        'colorStyle': {'rgbColor': {}},
		                        'style': 'SOLID_MEDIUM' if 'r' in border else "SOLID",
		                  },
		                  'top': 
		                  {
		                        'color': {},
		                        'colorStyle': {'rgbColor': {}},
		                        'style': 'SOLID_MEDIUM' if 't' in border else "SOLID",
		                  }
		            } if not no_border else {},


		            'horizontalAlignment': alignments[alignment],

		            'verticalAlignment': 'MIDDLE',

		            'hyperlinkDisplayType': "LINKED" if attach_polarian_hyperlink else 'PLAIN_TEXT',
		            

		            'padding': 
		            {
		                  'left': 3,
		                  'right': 3
		            },

		            'textFormat': 
		            {
		                  'bold': bold,
		                  'fontFamily': 'Arial',
		                  'fontSize': 10,
		                  'foregroundColor': {},
		                  'foregroundColorStyle': {'themeColor': 'TEXT'},
		                  'foregroundColorStyle': 
		                  {
		                        'rgbColor': GoogleSheet.colors['light_blue'] if attach_polarian_hyperlink else GoogleSheet.colors['black']
		                  },
		                  'italic': False,
		                  'strikethrough': False,
		                  'underline': True if attach_polarian_hyperlink else False
		            },


		            'verticalAlignment': 'BOTTOM',
		            
		            'wrapStrategy': 'CLIP'  # 'WRAP'
		    },

		}  


		# Assigning the value
		if attach_polarian_hyperlink:
			cell['userEnteredValue'] = {'formulaValue': f"=HYPERLINK(\"{GoogleSheet.get_hyperlink_web_link(value)}\", \"{value}\")"}
		else:
			cell['userEnteredValue'] = {'stringValue': value}           

		return cell
	
	def create_empty_table_rowData(self, row_count) -> List[Dict]:
		'''
		empty rows for Google sheet, meant to put spaces between different tables

		return list of rowData
		'''
		output = []
		for _ in range(row_count):
			output.append({'values': [self.create_cell('', no_border=True)]})

		return output

	def create_analysis_table_rowData(self, rows_of_tables: List[List[str]], table_start_row_inds: List[int]) -> List[Dict]:
		'''
		takes in any analysis table, e.g code coverage analysis table

		:param rows_of_tables: output of block.str_analysis_table, list of rows of string values
		:param table_start_row_inds: list of where every table starts of the block

		:returns: list of rowData json data (dictionary) AKA one checklist table as google sheet json data

		FOR MORE INFO LOOK AT THE DOCS OF self.create_checklist_table()

		How to do it:
		1-
		'''

		current_row = 0

		### create the first row, the title row -> list of cellData json data
		title_row = [self.create_cell(rows_of_tables[current_row][0], border = ['l', 't', 'b'], bold=True)]  # first cell, has borders from left and top
		for value in rows_of_tables[current_row][1:-1]:
			title_row.append(self.create_cell(value, border = ['t', 'b'], bold=True))
		title_row.append(self.create_cell(rows_of_tables[current_row][-1], border = ['r', 't', 'b'], bold=True))  # last cell for the top
		current_row += 1

		### finding ID columns
		ID_col_indexes = {}
		for ind_m in table_start_row_inds:
			ID_col_indexes[ind_m] = []
			for ind, value in enumerate(rows_of_tables[ind_m]):
				if 'id' in value.lower():
					ID_col_indexes[ind_m].append(ind)

		# the variables that will make sure the right list of ID_columns is choose for the right row
		table_end_row_inds = table_start_row_inds[1:]
		table_end_row_inds.append(len(rows_of_tables))
		current_key_col_index = 0
		current_col_list = ID_col_indexes[table_start_row_inds[current_key_col_index]]

		### create the rest of body rows except last row
		list_of_body_rows = []
		# creating list of list of cell celldata
		for row in rows_of_tables[1:-1]:

			# figuring out the current column ID list indexes
			if current_row >= table_end_row_inds[current_key_col_index]:
				current_key_col_index += 1
				current_col_list = ID_col_indexes[table_start_row_inds[current_key_col_index]]

			# creating a new list of cellData
			list_of_body_rows.append([])

			# first cell in the row
			list_of_body_rows[-1].append(self.create_cell(row[0], border=['l'], attach_polarian_hyperlink = True if 0 in current_col_list else False))  # first cell has left border
			
			# all body cells
			for ind_in, value in enumerate(row[1:-1]):
				list_of_body_rows[-1].append(self.create_cell(value, attach_polarian_hyperlink = True if ((ind_in+1) in current_col_list) else False))

			# last cell in the row
			list_of_body_rows[-1].append(self.create_cell(row[-1], border=['r'], attach_polarian_hyperlink = True if ind_in+2 in current_col_list else False))
		
			current_row += 1

		### create last row
		last_row = [self.create_cell(rows_of_tables[-1][0], border = ['l', 'b'], attach_polarian_hyperlink = True if 0 in current_col_list else False)]  # first cell, has borders from left and top
		for ind_in, value in enumerate(rows_of_tables[-1][1:-1]):
			last_row.append(self.create_cell(value, border = ['b'], attach_polarian_hyperlink = True if ((ind_in+1) in current_col_list) else False))
		last_row.append(self.create_cell(rows_of_tables[-1][-1], border = ['r', 'b'], attach_polarian_hyperlink = True if ind_in+2 in current_col_list else False))  # last cell for the top
		current_row += 1

		### converting list of cellData to proper rowData structure
		# title row
		rowData_title_row = {}
		rowData_title_row['values'] = title_row
		rowData_list_of_rowData = [rowData_title_row]  # list of dicts "values" = list_of_cellData
		
		# body rows
		for row in list_of_body_rows:
			rowData_list_of_rowData.append({"values": row})

		# last row
		rowData_last_row = {}
		rowData_last_row['values'] = last_row
		rowData_list_of_rowData.append(rowData_last_row)

		return rowData_list_of_rowData
		
	def create_all_analysis_table_rowData(self, blocks) -> List[dict]:
		'''
		loops through all analysis tables and creates all rowData

		puts two empty rows between each table
		'''
		all_rowData = []
		empty_cell = self.create_cell('')
		for block in blocks[1:]:
			all_rowData.extend(self.create_analysis_table_rowData(block.str_analysis_table, block.table_start_row_inds))
			all_rowData.append(self.create_empty_table_rowData(BlockTemplate.num_empty_rows_between_tables))

		return all_rowData

	def create_checklist_table_rowData(self, table: List[List[str]]) -> List[Dict]:
		'''
		takes in any checklist table, e.g code coverage checklist table

		and returns list of rowData json data (dictionary) AKA one checklist table as google sheet json data

		rowData json file represent one row in a google sheet, it is a list of cells
		A list of them is a table as it is (list of rows)

		rowData json file is represented like this

		{
			"values": 
			[  # this is start of the list, start of the row

				{  # first cell in the row
				object (CellData)  # a celldata is a json data that contains all information of a cell
				},

				{ # second cell in the row
				object (CellData)
				},

				{ # third cell in the row
				object (CellData)
				}
			
			]  # list finished, row ended
		}


		######################################################################################################
		The output of this function should help in inputing directly in 'data' key attribute in the 'Sheets' Google json file
		
		# A Sheet json data
		{
			"properties": 
			{
				object (SheetProperties)
			}


			"data":
			[
				{ # GridData json data
					"rowData": 
					[ 
						{ object (RowData) },
						{ object (RowData) },
						....
						{ object (RowData) }  
					]  <<----- This is the output of this function!!! (including the '[' and ']')
				}
			]

			....
		}

		The goodnews if i put this rowdata directly in this syntax like this it will immediately write it as it is from A1 cell
		THIS MEANS: I can loop through all checklist box and execute this function for each block and store all the outputs in a list
		THUS: I can pass this list directly after rowData like this

			"rowData":  <list of create_checklist_table() returns>

		How to do it:
		1- loop through str in a list of list and call self.create_cell() (with it's proper arguments specific to this cell only; the coordinates of this cell)
		2- keep appending to the list in 'values: []' of the json file to complete one row in the form of list of cell data 
		3- the whole thing inside {} and append the 'rowData: []' list to add new rows to the output table
		4- return the complete list of dictionary of which each dict has one key 'values' which has value list of cellData. That it! :)
		'''
		pass

	def create_checklist_sheet(self):
		'''
		:return: sheet Json file of checklist sheet
		'''
		
		### Load the complete sheet imported from the template Google Sheet
		sheet = self.read_json_file('checklist_sheet.json')


		### Modifying the Input Values AND assigning the hyperlinks to the 'Analysis of ...' cell of each block
		all_rows = BlockTemplate.get_checklist_tables(self.blocks)
		current_block_count = 1  # to know what is the block of the current row, we start from 1 because block[0] doesn't have analysis sheet
		start_row = 1  # in GoogleSheet, rows start at 1 not 0
		# looping through all userEnteredValue and changing them to the values I want
		for row_ind, row in enumerate(sheet['data'][0]['rowData']):
			for cell_ind, cell in enumerate(row.get('values', [{'None': None}])):

				# putting values I accounted for in the get_checklist_tables()
				if not row_ind+1 > len(all_rows):
					if not cell_ind+1 > len(all_rows[row_ind]):

						# put Hyperlink only in the cells which says 'Analysis of <block.name> for SW component <component.true_title>'
						cell_value = all_rows[row_ind][cell_ind]
						if 'Analysis of' and 'for the SW component' in cell_value:
							
							current_table = self.blocks[current_block_count].str_analysis_table
							A1_notation = GoogleSheet.get_A1_notation(current_table, start_row=start_row)
							start_row += len(current_table) + BlockTemplate.num_empty_rows_between_tables
							
							hyperlink_value = f"=HYPERLINK(\"#gid={GoogleSheet.analysis_sheet_id}&range={A1_notation}\", \"{cell_value}\")"
							cell['userEnteredValue'] = {'formulaValue': hyperlink_value}
							
							current_block_count += 1
						
						else:
							cell['userEnteredValue'] = {'stringValue': cell_value}

		return sheet

	def create_analysis_sheet(self):
		'''
		:return: sheet Json file of analysis sheet
		'''
		sheet = {
		            'properties': 
		            {
		                'sheetId': GoogleSheet.analysis_sheet_id, 
		                'title': GoogleSheet.analysis_sheet_name, 
		                'index': GoogleSheet.analysis_sheet_index, 
		                'sheetType': 'GRID', 
		                'gridProperties': 
		                {
		                    'rowCount': 1000, 
		                    'columnCount': 30
		                }
		            },

		            "merges": self.get_all_analysis_sheet_merges(self.blocks, GoogleSheet.analysis_sheet_id),

		            "data": [
		            	{
		            	"rowData": self.create_all_analysis_table_rowData(self.blocks)
		            	}
		            ]
		}

		return sheet

	################################ Merge Methods ################################
	@staticmethod
	def get_merge_data(sheet_id: int, start_row: int, end_row: int, start_col: int, end_col: int):
		'''
		:return: one gridRange Json data
		'''
		output =  {
		  "sheetId": sheet_id,
		  "startRowIndex": start_row,
		  "endRowIndex": end_row,
		  "startColumnIndex": start_col,
		  "endColumnIndex": end_col
		}
		return output

	@staticmethod
	def get_merges_list(rows: List[List[str]], col_num_to_be_merged: List[int], starting_row_num: int, sheet_id: int) -> List[Dict]:
		'''
		creates the list of GridRange json data input for vertical merges, 
		meant to be input of "merges" in Sheets Json data
		e.g of result when col_num_to_be_merged = [0, 1, 2] in the google sheet
		SN, 	ID, 	DD name, 	Req 		SN, 	ID, 	DD name, 	Req 
		1,  	432, 	DDname1, 	Req1					 			, 	Req1
		1, 		432, 	DDname1, 	Req2		1, 		432, 	DDname1 , 	Req2
		1, 		432, 	DDname1, 	Req3  --->	 			 			, 	Req3
		2, 		243, 	DDname2, 	Req8					 			, 	Req8
		2, 		243, 	DDname2, 	Req2		2, 		243, 	DDname2, 	Req2

		:param rows: output of BlockTemplate.get_str_analysis_table()
		:param col_num_to_be_merged: list of the index of the columns that has data that could be merged
		:param starting_row_num: the merge data is absolute, we need to know where does the table start
									ASSUME: all tables starts from first column
		:return: list of GridRange Json Data (meant to be input of "merges": in sheet Json data)
		'''
		merges = []

		# Get the transpose of the tables
		transpose = GoogleSheet.get_transpose(rows)

		# get merge value Algorithm
		for col_ind in col_num_to_be_merged:

			start_ind = starting_row_num
			current_value = transpose[col_ind][0]
			for ind, value in enumerate(transpose[col_ind][1:]):

				if current_value == value:
					continue  # keep continuing through all the col values that are the same
				
				else:
					current_value = value  # for next time, assigning the new different value

					end_ind = starting_row_num + ind + 1
					if end_ind - start_ind == 1:
						# no merge needed values are different in the next cell
						start_ind = end_ind  # for next time
						
					else:
						# more than one row with same value
						# getting the merge
						merges.append(GoogleSheet.get_merge_data(sheet_id, start_ind, end_ind, col_ind, col_ind+1))

						start_ind = end_ind


		return merges

	def get_all_analysis_sheet_merges(self, blocks, sheet_id):
		'''

		'''
		all_merges = []
		row_counter = 0
		for block in blocks[1:]:
			all_merges.extend(block.merges(row_counter, sheet_id))
			row_counter += len(block.str_analysis_table) + BlockTemplate.num_empty_rows_between_tables
			

		return all_merges
	################################################################################################

	def get_complete_spreadsheet(self) -> List[Dict]:
		'''
		:return: complete spreadsheet Json Data with EVERYTHING
		'''
		spreadsheet = {
			    ############### SpreadSheetProperties ###############
			    'properties': 
			    {
			        'title': self.blocks[0].component.true_title + '.c', 
			        'locale': 'en_US', 
			        'defaultFormat': 
			        {
			            'backgroundColor': 
			            {
			                'red': 1, 
			                'green': 1, 
			                'blue': 1
			            }, 
			            'padding': 
			            {
			                'right': 3, 
			                'left': 3
			            },
			            'verticalAlignment': 'MIDDLE', 
			            'wrapStrategy': 'CLIP', 
			            'textFormat': 
			            {
			                'foregroundColor': {}, 
			                'fontFamily': 'Arial', 
			                'fontSize': 10, 
			                'bold': False, 
			                'italic': False, 
			                'strikethrough': False, 
			                'underline': False, 
			                'foregroundColorStyle': 
			                {
			                    'rgbColor': {}
			                }
			            }, 
			            'backgroundColorStyle': 
			            {
			                'rgbColor': 
			                {
			                    'red': 1, 
			                    'green': 1, 
			                    'blue': 1
			                }
			            }
			        }, 
			        'spreadsheetTheme': 
			        {
			            'primaryFontFamily': 'Arial', 
			            'themeColors': 
			            [
			                {
			                    'colorType': 'TEXT', 
			                    'color': 
			                    {
			                        'rgbColor': {}
			                    }
			                }, 

			                {
			                    'colorType': 'BACKGROUND', 
			                    'color': 
			                    {
			                        'rgbColor': 
			                        {
			                            'red': 1, 
			                            'green': 1, 
			                            'blue': 1
			                        }
			                    }
			                }, 

			                {
			                    'colorType': 'ACCENT1', 
			                    'color': 
			                    {
			                        'rgbColor': 
			                        {
			                            'red': 0.25882354, 
			                            'green': 0.52156866, 
			                            'blue': 0.95686275
			                        }
			                    }
			                }, 

			                {
			                    'colorType': 'ACCENT2', 
			                    'color': 
			                    {
			                        'rgbColor': 
			                        {
			                            'red': 0.91764706, 
			                            'green': 0.2627451, 
			                            'blue': 0.20784314
			                        }
			                    }
			                }, 

			                {
			                    'colorType': 'ACCENT3', 
			                    'color': 
			                    {
			                        'rgbColor': 
			                        {
			                            'red': 0.9843137, 
			                            'green': 0.7372549, 
			                            'blue': 0.015686275
			                        }
			                    }
			                }, 

			                {
			                    'colorType': 'ACCENT4', 
			                    'color': 
			                    {
			                        'rgbColor': 
			                        {
			                            'red': 0.20392157, 
			                            'green': 0.65882355, 
			                            'blue': 0.3254902
			                        }
			                    }
			                }, 

			                {
			                    'colorType': 'ACCENT5', 
			                    'color': 
			                    {
			                        'rgbColor': 
			                        {
			                            'red': 1, 
			                            'green': 0.42745098, 
			                            'blue': 0.003921569
			                        }
			                    }
			                }, 

			                {
			                    'colorType': 'ACCENT6', 
			                    'color': 
			                    {
			                        'rgbColor': 
			                        {
			                            'red': 0.27450982, 
			                            'green': 0.7411765, 
			                            'blue': 0.7764706
			                            
			                        }
			                    }
			                }, 

			                {
			                    'colorType': 'LINK', 
			                    'color': 
			                    {
			                        'rgbColor': 
			                        {
			                            'red': 0.06666667, 
			                            'green': 0.33333334, 
			                            'blue': 0.8
			                        }
			                    }
			                }
			            ]
			        }
			    }, 

			    ############### Sheets ###############
			    'sheets': 
			    [
			    	############### Checklist sheet ###############
			        self.create_checklist_sheet(), 

			        ############### Analysis sheet ###############
			        self.create_analysis_sheet()
			    ]
			}

		return spreadsheet

	def create(self) -> str:
		"""
		Creates the Sheet the user has access to.
		
		PROVIDED: token.json is present in wanted path

		return spreadsheetId as str
	    """

	    ################### Creating the SpreadSheet ###################
		creds = None
		path_to_token_json = GoogleSheet.path_to_json_files + 'token.json'

		if os.path.exists(path_to_token_json):
			print("Reading Creds...")
			creds = Credentials.from_authorized_user_file(path_to_token_json, GoogleSheet.SCOPES)
			print("Done Reading Creds!")
			# If there are no (valid) credentials available, let the user log in.
		
		else:
			# token.json is not there
			raise FileNotFoundError("'token.json' is not found!\nPlease ask admin to make token.json for you.")
				
		# if token.json is there or not valid	
		if not creds or not creds.valid:

			# if token.json is not valid, refresh?!?
			if creds and creds.expired and creds.refresh_token:
				print("\n\nRefreshing token.json...")
				creds.refresh(Request())
				print("Done!")
				
		try:
			print("\nSending API create spreadsheet Request...")
			service = build('sheets', 'v4', credentials=creds)
			spreadsheet = self.get_complete_spreadsheet()  # :)

			spreadsheet = service.spreadsheets().create(body=spreadsheet, fields='spreadsheetId').execute()

			spreadsheet_id = spreadsheet.get('spreadsheetId')

			print(f"Done Creating Spreadsheet with ID: {(spreadsheet.get('spreadsheetId'))}")

		except HttpError as error:
			print(f"An error occurred: {error}")
			return error
		######################################################################################################


		# finally return spreadsheetID
		return spreadsheet_id
########################################################################################################################################



########################################################################################################################################
# running the script, only meant for debugging
if __name__ == '__main__':
	
	### Constants (for debugging)
	homedir = 'C:/Users/abadran/Dev_analysis/Beifang/script'
	DISABLE_REPORT_SEARCH = True
	DOCUMENT_CHOOSEN_NUMBER = 0  # REMEMBER TO PUT NONE and remember to include -1. for components that has multiple valid document and we must choose one
	MANUAL_CAT3_MODE_INPUT = None
	DEBUG_FUNC_DEFS = False


	### Inputs
	component_name = "idp"
	CAT_num = 1
	variant = 'Base+'
	branch = 'P330'

	paths_to_code = [r"C:\Users\abadran\Dev_analysis\Beifang\script\input_files\code\VW_MEB_Software\src\fw_cu\Components",
					 r"C:\Users\abadran\Dev_analysis\Beifang\script\input_files\code\VW_MEB_Software\src\fw_cu\workspace",
					 r"C:\Users\abadran\Dev_analysis\Beifang\script\input_files\code\VW_MEB_Software\src\fw_actvdcha\Components"]
	
	path_to_reports = r"W:\DE\ERL1\RnD\serv\JBUILD\VW_MEB"

	path_to_tcc = 'C:\\tcc'

	my_polarian_web_link = "https://vseapolarion.vnet.valeo.com/polarion/#/project/VW_MEB_Inverter/mypolarion"

	### Run the script
	main(homedir, component_name, CAT_num, branch, variant, paths_to_code, path_to_reports, path_to_tcc, my_polarian_web_link)
########################################################################################################################################

