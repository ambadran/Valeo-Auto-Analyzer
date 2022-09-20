'''
Unit Test file for auto_analysis.py script
'''

########################################################################################################################################
### Imports

# pytest
import pytest

# Database
from main_pkg.auto_analysis import WorkItem, Component, DetailedDesign, Requirement, Diagnostic, Interface

# Blocks
from main_pkg.auto_analysis import BlockTemplate, FirstBlock, SecondBlock, ThirdBlock, ForthBlock, FifthBlock, SixthBlock, SeventhBlock

# Main Functions
from main_pkg.auto_analysis import read_assign_all_CSVs, analyze_component, create_blocks

# Exports
from main_pkg.auto_analysis import export_csv, GoogleSheet
########################################################################################################################################




########################################################################################################################################
# Important Decorators

# skipping tests for a reason
# @pytest.mark.skip(reason='reason why you want to skip this test')

# tests based on a condition
# @pytest.mark.skipif

# for tests that you know will fail and don't want it to fail the build
# it will run normally, but if it fails, it will not tell you the whole build failed
# @pytest.mark.xfail

# for testing exceptions; whether an exception is raised or not for a specific input
# must implement in the test function
# def test_func_that_could_raises_ValuError():
# 	with pytest.raises(ValueError):
# 		func_that_could_raises_ValuError(argument_that_lets_the_function_raise_ValueError)

# fixtures :)
########################################################################################################################################




########################################################################################################################################
# Database Testing

class TestWorkItem:

	def test_CLASS_VARIABLES(self):
		pass

	def test_init(self):
		pass

	def test_getattr(self):
		pass

	def test_get_all_from_csv(self):
		pass

	def test_is_linked(self):
		pass

	def test_link(self):
		pass

	def test_link_all(self):
		pass

class TestComponent:

	def test_CLASS_VARIABLES(self):
		pass

	def test_init(self):
		pass

	def test_true_title(self):
		pass

	def test_filter_object_list(self):
		pass

	def test_get_component(self):
		pass

	def test_choose_component_manual(self):
		pass

	def test_do_one_dd_to_dd(self):
		pass

	def test_link(self):
		pass

	def link_dd_in_interface(self):
		pass

	def link_internals_all(self):
		pass

class TestRequirement:

	def test_CLASS_VARIABLES(self):
		pass

	def test_init(self):
		pass

	def test_filter_object_list(self):
		pass

class TestDiagnostic:

	def test_CLASS_VARIABLES(self):
		pass

	def test_init(self):
		pass

	def test_filter_object_list(self):
		pass

class TestDetailedDesign:

	def test_CLASS_VARIABLES(self):
		pass

	def test_init(self):
		pass

	def test_filter_object_list(self):
		pass

	def test_check_sw_component(self):
		pass

	def test_req_diag(self):
		pass

class TestInterface:

	def test_CLASS_VARIABLES(self):
		pass

	def test_init(self):
		pass

	def test_filter_object_list(self):
		pass
########################################################################################################################################



########################################################################################################################################
# Blocks Testing

class TestBlockTemplate:

	def test_init(self):
		pass

class TestFirstBlock:

	def test_init(self):
		pass

	def test_checklist_table(self):
		pass

	def test_analysis_table(self):
		pass

class TestSecondBlock:

	def test_init(self):
		pass

	def test_get_code_coverage_stat(self):
		pass

	def test_get_entries(self):
		pass

	def test_search_for_report(self):
		pass

	def test_find_report(self):
		pass

	def test_filter_backslash(self):
		pass

	def test_checklist_table(self):
		pass

	def test_analysis_table(self):
		pass

class TestThirdBlock:

	def test_init(self):
		pass

	def test_get_dead_code_stat(self):
		pass

	def test_get_entries(self):
		pass

	def test_filter_backslash(self):
		pass

	def test_checklist_table(self):
		pass

	def test_analysis_table(self):
		pass

class TestForthBlock:

	def test_init(self):
		pass

	def test_get_code_switch_necessity(self):
		pass

	def test_get_outside_function(self):
		pass

	def test_assign_enabled_stat(self):
		pass

	@pytest.mark.parametrize("test_input,expected", [
		('lskdfj /* lskjdfj */sdfdsfsd', 					'lskdfj sdfdsfsd'),  # testing comment in the middle
		('slkdjlkfjdskfj /* lskdfjdf\nldksjfkjdslkfj */', 	'slkdjlkfjdskfj '),  # testing multi-line comment
		('sldkfjldsjf // ljsdlfkjdsf lksjfd jsdlkfj ', 		'sldkfjldsjf '),  # testing // comment
		('// lskjdlfjdsfkj', 								''),  # testing comment at the begginging of the line
		('/* lskdjf */ lksjdlfkjdsf', 						' lksjdlfkjdsf')  # testing comment in the beggining with non-comment text after

		])
	def test_KILL_ALL_COMMENTS(self, test_input, expected):
		assert ForthBlock.KILL_ALL_COMMENTS(test_input) == expected

	def test_KILL_ALL_CODE_SWITCHES(self):
		pass

	def test_get_code_switches_all(self):
		pass

	def test_get_code_switches(self):
		pass

	def test_get_code_file(self):
		pass

	def test_filter_backslash(self):
		pass

	def test_manually_choose_c_file(self):
		pass

	def test_get_all_funcs(self):
		pass

	def test_checklist_table(self):
		pass

	def test_analysis_table(self):
		pass

class TestFifthBlock:

	def test_init(self):
		pass

	def test_get_code_comments_stat(self):
		pass

	def test_get_code_comments_all(self):
		pass

	def test_get_func_comments(self):
		pass

	def test_get_code_comments(self):
		pass

	def test_checklist_table(self):
		pass

	def test_analysis_table(self):
		pass

class TestSixthBlock:

	def test_init(self):
		pass

	def test_get_detailed_design_stat(self):
		pass

	def test_get_detailed_design(self):
		pass

	def test_checklist_table(self):
		pass

	def test_analysis_table(self):
		pass

class TestSeventhBlock:

	def test_init(self):
		pass

	def test_get_code_reviews(self):
		pass

	def test_get_code_reivew_stat(self):
		pass

	def test_checklist_table(self):
		pass

	def test_analysis_table(self):
		pass
########################################################################################################################################



########################################################################################################################################
#### Main Functions

def test_read_assign_all_CSVs():
	pass

def test_analyze_component():
	pass

def test_create_blocks():
	pass
########################################################################################################################################



########################################################################################################################################
#  Exports

def test_export_csv():
	pass

class TestGoogleSheet:
	
	def test_init(self):
		pass

	def test_creat(self):
		pass

########################################################################################################################################