# auto_analyzer

auto_analyzer is a Python package that automates component (c file) analysis according to Valeo analysis procedure.


## Installation

This package is not meant to be directly installed by the user. It's automatically installed and maintained through 
auto_analyzer_CLI.py script. This script silently git clone and git pull the package in a hidden folder in the same directory it
runs in.


## Usage

1- Download the 'auto_analyzer_CLI.py' from https://github.com/ambadran/auto_analyzer_CLI

2- Double click it and follow the instructions.



## Description

This program runs in three main steps. 
Firstly, It reads and process all needed data from polarian. The user must go to WorkItem tab, find components, Detailed Design, 
Interfaces, Software Requirements and Diagnostics workitems. Remove ANY filter applied and export CSV files including all the necessary
attributes.
For every workitem, these attributes must be selected when exporting the CSV file:
	- "ID"
	- "Title"
	- "Variant"
	- "Linked Work Items"
	- "Severity"
	- "Status"
	- "Space / Document"
	- "Description"

After running the auto_analyzer the first time, the program will ask the user to put the CSV files in their correct place which 
intuitively is in the created folder: 'input_files/polarian_csv_outputs'. 

The next step is to provide all the wanted paths to project code on your computer as will be asked by the CLI.
The code usually is in src/fw_cu/Components inside the project code folder

Then the user will be asked for the path to server folder where RTRT and QAC files are located. Please provide the folder has inside it
'Release' and 'Rolling Build' folders.

Then the user will be asked to provide path to tcc compiler which can be downloaded from https://bellard.org/tcc/ 

Finally, the user will be asked to provide the web link to mypolarian page openned in the wanted project.
It should look something like this https://vseapolarion.vnet.valeo.com/polarion/#/project/{project_name}/mypolarion

After finishing these first 5 inputs the program will make memory of them and will never ask for them again. (The program
will ask if the user wants to change any of the above data everytime though)

Next the user is supposed to enter the data of the component to be searched; name of component, variant, branch, etcc..

The user will be asked if more components need to be analyzed too.

The second stage of running this program is analysis step itself.
After all components are validated, the following analysis will commence. (depending on CAT number)
1- Code coverage (finds RTRT files, reads them and extract functions that don't have 100% covered stat or are failed)
2- Dead code (finds QAC files and reports if 'unreachable' code is found)
3- Code Switch (finds the C file, extracts all code switches, filters them and checks if it's enabled or disabled)
4- Code Comments (extracts all comments in the C file, filters them)
5- Detailed Design (checks if all DD in polarian have software requirements or diagnostics and is attached to a component)
6- Code Review (checks if functions implemented in C file matches Detailed Design workitems in polarian)


The last stage is generating the output itself.

CSV files containing all resulting data will be generated in 'output/csv'

Finally, the user will be asked if a Google Sheet needs to be created for each entered component.
This action needs approval from Google workspace owners. Please contact project leader to get access.


## How it Works

The code could be seperated into three distinct parts.

The database part, which is 5 class; Component, Interface, DetailedDesign, Requirement and Diagnostic all inheriting from the
same parent: WorkItem. Inside WorkItem is code that parses the data from the csv files, and the code to initialize the objects
successfully. Also it contains the generalized algorithm to link any WorkItem with any other.

The initial output of these class is a class variable called all_objects in each class which contain all the WorkItem object for each
class. However, the real output we want from this code is to call the Component.get_component function which will make a hash map of all
component which hash key of the name to match the input of the user. Then when wanted component is identified. The linking algorithm gets
executed and now we have a Component Object linked to all other workitem successfully.

The second part of the code is the 7 blocks class which all inherit form BlockTemplate class. Each block is responsible to do one type of
analysis. For example, the first block 'FirstBlock' is responsible for code coverage analysis. It contain the DFS (Depth-first-search) 
algorithm which searches for the RTRT files in the server folder for example. Each block has many methods. The most important are get_entries()
which is a method to get the analysis data the block is responsible for. For exmaple the 6th block 'SixthBlock' is responsible for
DetailedDesign analysis. So get_entries will output a list of wrong detailed design objects (DDs that doens't have requirements linked to them
for example). The second important method in each block is get_stat() which returns a boolean of whether the analysis of the corresponding
block has passed or not. There is also checklist_table() and analysis_table() methods in each block which output the data that should be put
in the csv/excel/google_sheet output as list of list (a table).

Finally, the last part of the code is the export_csv() function which reads the output of each block and writes to CSV files.
and there is ofcoarse the GoogleSheet class which handles communicating with the Google Sheet API and automatically creates the
Google sheet with all the merging, linking to polarian web page for IDs, highlights, conditional formatting and many more.
