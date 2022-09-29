'''
Unit Test file for auto_analysis.py script
'''

########################################################################################################################################
### Imports

# pytest
import pytest

#Data Classes

from main_pkg.auto_analysis import QAC , CodeSwitch , CodeComment , FuncComment , Func , CodeReview , Memory

#html2text
from html2text import html2text

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


##For Detailed test cases result ================================> pytest -vv


########################################################################################################################################
# Test functions

#change component name 
def change_component_name(component_name,variant,branch):
	global dumy_component
	dumy_component = Component(ID='VW-MEB-2384', title=component_name, variant=['base+','base-'])
	dumy_component.CAT_num=1
	global dumy_first_block
	dumy_first_block = FirstBlock(dumy_component, variant, branch)
	global dumy_second_block
	dumy_second_block = SecondBlock(dumy_first_block)
	global dumy_third_block
	dumy_third_block = ThirdBlock(dumy_first_block)
	global dumy_forth_block
	dumy_forth_block = ForthBlock(dumy_first_block)
	global dumy_fifth_blocks
	dumy_fifth_block = FifthBlock(dumy_first_block,dumy_forth_block)


#Read File Function
def read_file(path: str) -> str:
	'''
	:input: path to .txt that we want to read
	:return: return content of the file as string
	'''
	path = ForthBlock.filter_backslash(path)
	with open(path, 'r') as file:
		return file.read()
		

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
    
dumy_component = Component(ID='VW-MEB-2384', title='Idp', variant=['base+','base-'])
dumy_component.CAT_num=1	

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

		
################################# methods of FirstBlock ########################
dumy_first_block = FirstBlock(dumy_component, 'base+', 'P330')


def test_checklist_table():
	pass

def test_analysis_table():
	pass

################################# methods of SecondBlock ########################
dumy_second_block = SecondBlock(dumy_first_block)



@pytest.mark.parametrize("test_input,expected",[

(({'Functions and exits': (2, 2) , 'statement blocks': (15, 15), 'implicit blocks': (12, 12) , 'Decisions' : (19,19)}), 1.0)               ,
(({'Functions and exits': (7, 2) , 'statement blocks': (20, 15), 'implicit blocks': (10, 12) , 'Decisions' : (15,19)}), 1.0833333333333333),
(({'Functions and exits': (25, 0), 'statement blocks': (0, 15) , 'implicit blocks': (10, 22) , 'Decisions' : (15,10)}), 1.0638297872340425),
(({'Functions and exits': (0, 30), 'statement blocks': (10, 15), 'implicit blocks': (8, 22)  , 'Decisions' : (4,10)}) , 0.2857142857142857),
(({'Functions and exits': (0, 30), 'statement blocks': (0, 15) , 'implicit blocks': (0, 22)  , 'Decisions' : (0,4)})  , 0.0)			   ,
#failed
#(({'Functions and exits': (20, 0), 'statement blocks': (20, 0),  'implicit blocks': (20, 0)  , 'Decisions' : (20,0)}) , 0.0),
 
])
def test_get_code_coverage_stat(test_input,expected):
	
	dumy_second_block.code_coverage = {'Summary': test_input}
	assert dumy_second_block.get_code_coverage_stat() == expected


	
#@pytest.mark.skip(reason = 'Not finished yet')
'''
@pytest.mark.parametrize("test_input, expected",[
	
	# input1
	(
	[html2text(read_file("C:/Dev/auto_analysis/Valeo-Auto-Analyzer/tests/test_snippets/test_get_entries_RTRT/test_input/Idp.html"))],
	
	#expected1
	eval(read_file("C:/Dev/auto_analysis/Valeo-Auto-Analyzer/tests/test_snippets/test_get_entries_RTRT/expected/dictionary_test1.txt"))
	),
	
	#input2
	(
	[html2text(read_file("C:/Dev/auto_analysis/Valeo-Auto-Analyzer/tests/test_snippets/test_get_entries_RTRT/test_input/Exc.html"))],
	
	#expected2
	eval(read_file("C:/Dev/auto_analysis/Valeo-Auto-Analyzer/tests/test_snippets/test_get_entries_RTRT/expected/dictionary_test2.txt"))
	),

	#A component with more one report :
	(
	#input3
	[html2text(read_file("C:/Dev/auto_analysis/Valeo-Auto-Analyzer/tests/test_snippets/test_get_entries_RTRT/test_input/SftyTqMon.html")),
	 html2text(read_file("C:/Dev/auto_analysis/Valeo-Auto-Analyzer/tests/test_snippets/test_get_entries_RTRT/test_input/SftyTqMon_1.html"))],
	  
	#expected3
	eval(read_file("C:/Dev/auto_analysis/Valeo-Auto-Analyzer/tests/test_snippets/test_get_entries_RTRT/expected/dictionary_test3.txt"))  
	  
	  
	),


])
'''
@pytest.mark.skip(reason = 'Test takes long time')
def test_get_entries_RTRT(test_input,expected):
	dumy_second_block.report = test_input
	assert dumy_second_block.get_entries() == expected
	


'''
@pytest.mark.parametrize("test_input,variant,branch, expected", [
("Exc",'base-','Q330',['W:/DE/ERL1/RnD/serv/JBUILD/VW_MEB/Release/VW-MEB-Q330-0001-20220630_06/Base-/ForInternalUse/Reports/RTRT.zip/RTRT/BSW-ASM/Reporter/Exc.html']),
("Sba7o",'base-','Q330',[None]),
("SftyTqMon",'base+','P330',['W:/DE/ERL1/RnD/serv/JBUILD/VW_MEB/RollingBuild/VW-MEB-P330-0015-20220729/Reports/RTRT/SSW-PSM/Reporter/SftyTqMon.html',  
							 'W:/DE/ERL1/RnD/serv/JBUILD/VW_MEB/RollingBuild/VW-MEB-P330-0015-20220729/Reports/RTRT/SSW-PSM/Reporter/SftyTqMon_1.html'])

])
'''
@pytest.mark.skip(reason = 'Test takes long time')
def test_search_for_report_RTRT(test_input,expected,variant,branch):
	dumy_second_block.report_path = None
	dumy_second_block.sole_files = []
	dumy_second_block.search_for_report(test_input,variant,branch)
	if dumy_second_block.report_path == None:
		test_output = None
	else:
		test_outputs = []
		for value in dumy_second_block.sole_files:
			test_outputs.append(dumy_second_block.report_path + '/' + value)
			
		assert set(test_outputs) == set(expected)




@pytest.mark.parametrize("expected",[
html2text(read_file('C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\input_files\\reports\\base+\\RTRT\\Idp.html'))[:500],
])
def test_find_report_RTRT(expected):
	assert dumy_second_block.find_report()[0][:500] == expected


 
################################# methods of ThirdBlock ########################

dumy_third_block = ThirdBlock(dumy_first_block)

'''
@pytest.mark.parametrize("test_input,variant,branch, expected", [
("BswErrDeb",'base+','P330',['W:/DE/ERL1/RnD/serv/JBUILD/VW_MEB/RollingBuild/VW-MEB-P330-0015-20220729/Base+/Reports/QAC/VW_MEB/mcr_data/BswErrDeb.c.html']),
("Sba7o",'base-','Q330',[None]),
("SftyTqMon",'base+','P330',['W:/DE/ERL1/RnD/serv/JBUILD/VW_MEB/RollingBuild/VW-MEB-P330-0015-20220729/Base+/Reports/QAC/VW_MEB/mcr_data/SftyTqMon.c.html'])
])
def test_search_for_report_QAC(test_input,expected,variant,branch):
	dumy_third_block.report_path = None
	dumy_third_block.sole_files = []
	dumy_third_block.search_for_report(test_input,variant,branch)
	if dumy_third_block.report_path == None:
		test_output = None
	else:
		test_outputs = []
		for value in dumy_third_block.sole_files:
			test_outputs.append(dumy_third_block.report_path + '/' + value)
			
		assert set(test_outputs) == set(expected)

'''
@pytest.mark.parametrize("expected",[
html2text(read_file('W:\\DE\\ERL1\\RnD\\serv\\JBUILD\\VW_MEB\\RollingBuild\\VW-MEB-P330-0015-20220729\\Base+\\Reports\\QAC\\VW_MEB\\mcr_data\\Idp.c.html'))[:500],
])
def test_find_report_QAC(expected):
	assert dumy_third_block.find_report()[0][:500] == expected



@pytest.mark.parametrize("test_input, expected" , [

(True , True),
(False , False),
])
def test_get_dead_code_stat(test_input,expected):
	dumy_third_block.dead_code = test_input
	assert dumy_third_block.get_dead_code_stat() == expected

@pytest.mark.parametrize("test_input, expected",[

([html2text(read_file('C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_entries_QAC\\test_input\\BswErrDeb.c.html'))] , False),
([html2text(read_file('C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_entries_QAC\\test_input\\Idp.c.html'))]       , False),
([html2text(read_file('C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_entries_QAC\\test_input\\SftyTqMon.c.html'))] , False),
([html2text(read_file('C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_entries_QAC\\test_input\\Test_input_4.txt'))] , True),

])
def test_get_entries_QAC(test_input,expected):
	dumy_third_block.report = test_input
	assert dumy_third_block.get_entries() == expected
	

@pytest.mark.parametrize("test_input, expected",[
(r"C:\Dev\auto_analysis\Valeo-Auto-Analyzer\tests","C:/Dev/auto_analysis/Valeo-Auto-Analyzer/tests"),
(r"C:\Beifang_Script\output",r"C:/Beifang_Script/output"),
(r"C:\\Beifang_Script\\\\output",r"C://Beifang_Script////output"),
(r"\C:\Beifang_Script\output\\", r"/C:/Beifang_Script/output//"),
])
def test_filter_backslash(test_input,expected):
	assert dumy_second_block.filter_backslash(test_input) == expected
	assert dumy_third_block.filter_backslash(test_input) == expected
	assert ForthBlock.filter_backslash(test_input) == expected




########################### methods of ForthBlock ###########################

dumy_forth_block = ForthBlock(dumy_first_block)




@pytest.mark.parametrize("test_input,expected",[

#expected to pass no faliure
(None,None),
("Trw",None),
(23,None),

])
def test_get_code_switch_necessity(test_input,expected):
	assert dumy_forth_block.get_code_switch_necessity() == expected




@pytest.mark.parametrize("test_input,expected",[
(309,					"Idp_ValidateAdminTable"),
(359,					"Idp_ReadDIDFromInfoTable"),
(209384093284, 			None),
(293,					None),
(305,					"Idp_ValidateAdminTable"),
(563,					"Idp_F189_VWApplicationSoftwareVersionNumber_ReadData"),
(5,						None)

])
def test_get_outside_function(test_input, expected):
	assert dumy_forth_block.get_outside_function(dumy_forth_block.func_defs, test_input) == expected



def test_assign_enabled_stat():
	pass



@pytest.mark.parametrize("test_input,expected", [
	('lskdfj /* lskjdfj */sdfdsfsd', 					'lskdfj sdfdsfsd'),  # testing comment in the middle
	('slkdjlkfjdskfj /* lskdfjdf\nldksjfkjdslkfj */', 	'slkdjlkfjdskfj '),  # testing multi-line comment
	('sldkfjldsjf // ljsdlfkjdsf lksjfd jsdlkfj ', 		'sldkfjldsjf '),  # testing // comment
	('// lskjdlfjdsfkj', 								''),  # testing comment at the begginging of the line
	('/* lskdjf */ lksjdlfkjdsf', 						' lksjdlfkjdsf')  # testing comment in the beggining with non-comment text after

	])
def test_KILL_ALL_COMMENTS(test_input, expected):
	assert dumy_forth_block.KILL_ALL_COMMENTS(test_input) == expected

@pytest.mark.parametrize("test_input, expected",[

	(read_file(r'tests\test_snippets\test_KILL_ALL_CODE_SWITCHES\test_cases\test_case1.txt'), 	read_file(r'tests/test_snippets/test_KILL_ALL_CODE_SWITCHES/expected/expected1.txt')),
	#(read_file(r'tests\test_snippets\test_KILL_ALL_CODE_SWITCHES\test_cases\test_case2.txt'), 	read_file(r'tests/test_snippets/test_KILL_ALL_CODE_SWITCHES/expected/expected2.txt')),
	
])
def test_KILL_ALL_CODE_SWITCHES(test_input,expected):
	assert dumy_forth_block.KILL_ALL_CODE_SWITCHES(test_input,dumy_forth_block.code_switches_all) == expected


def test_get_code_switches_all():
	pass

def test_get_code_switches():
	pass



@pytest.mark.parametrize("test_input, expected",[
("IdP",(read_file("C:/VW/VW_MEB_Software/src/fw_cu/Components/Cmn/Diagc/Diagc/src/idp.c"),"C:/VW/VW_MEB_Software/src/fw_cu/Components/Cmn/Diagc/Diagc/src/Idp.c")),
("obd",(read_file("C:/VW/VW_MEB_Software/src/fw_cu/Components/Cmn/Diagc/Diagc/src/obd.c"),"C:/VW/VW_MEB_Software/src/fw_cu/Components/Cmn/Diagc/Diagc/src/Obd.c")),
("dcmext",(read_file("C:/VW/VW_MEB_Software/src/fw_cu/Components/Cmn/Diagc/Diagc/src/dcmext.c"),"C:/VW/VW_MEB_Software/src/fw_cu/Components/Cmn/Diagc/Diagc/src/DcmExt.c")),
("demext",(read_file("C:/VW/VW_MEB_Software/src/fw_cu/Components/Cmn/Diagc/Diagc/src/demext.c"),"C:/VW/VW_MEB_Software/src/fw_cu/Components/Cmn/Diagc/Diagc/src/DemExt.c")),

])
def test_get_code_file(test_input,expected):
	assert dumy_forth_block.get_code_file(test_input) == expected

def test_manually_choose_c_file():
	pass

def test_get_all_funcs():
	pass



################################################Methods of fifth block#############################################################


dumy_fifth_block = FifthBlock(dumy_first_block,dumy_forth_block)

@pytest.mark.parametrize("component_name,variant,branch,expected1,code_comment_input_list,expected2",[
("Idp","base+","P330",True,eval(read_file("C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_code_comments_stat\\expected_1.txt")),True),
("Obd","base+","P330",True,eval(read_file("C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_code_comments_stat\\expected_2.txt")),False),
("emm","base+","P330",True,eval(read_file("C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_code_comments_stat\\expected_3.txt")),False),
("ecum_callouts","base+","P330",True,eval(read_file("C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_code_comments_stat\\expected_4.txt")),False),

])
def test_get_code_comments_stat(component_name,variant,branch,expected1,code_comment_input_list,expected2):
	change_component_name(component_name,variant,branch)
	#dumy_fifth_block.code_file = dumy_forth_block.code_file_both
	#assert dumy_fifth_block.get_code_comments_stat() == expected1
	
	
	
	dumy_fifth_block.code_comments = code_comment_input_list
	#assert dumy_fifth_block.get_code_comments_stat() == expected2
	#assert dumy_fifth_block.get_code_comments_stat() == eval(read_file("C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_code_comments_stat\\expected_2.txt"))
	#assert dumy_fifth_block.get_code_comments_stat() == eval(read_file("C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_code_comments_stat\\expected_3.txt"))
	pass

@pytest.mark.parametrize("component_name,variant,branch,input,",[

("Idp","base+","P330",eval(read_file('C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_code_comments_all\\expected_1.txt'))),
("Obd","base+","P330",eval(read_file('C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_code_comments_all\\expected_2.txt'))),
("emm","base+","P330",eval(read_file('C:\\Dev\\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_code_comments_all\\expected_3.txt'))),


])
def test_get_code_comments_all(component_name,variant,branch,input):
	change_component_name(component_name,variant,branch)
	
	#dumy_fifth_block.code_file = read_file('C:\\Dev\auto_analysis\\Valeo-Auto-Analyzer\\tests\\test_snippets\\test_get_code_comments_all\\code_1.c')
	dumy_fifth_block.code_comments = input
	assert dumy_fifth_block.get_code_comments_all() == input
	

def test_get_func_comments():
	pass

def test_get_code_comments():
	pass

################################################Methods of sixth block#############################################################



def test_get_detailed_design_stat():
	pass

def test_get_detailed_design():
	pass

################################################Methods of Seventh block#############################################################

def test_get_code_reviews():
	pass

def test_get_code_reivew_stat():
	pass


########################################################################################################################################



########################################################################################################################################



########################################################################################################################################
#  Exports


class TestGoogleSheet:
	
	def test_init(self):
		pass

	def test_creat(self):
		pass

########################################################################################################################################
