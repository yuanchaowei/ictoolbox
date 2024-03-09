#!/usr/bin/env python3
import os
import logging
import sys
from jinja2 import Environment, FileSystemLoader

#All changable parameters
proj_name = 'multig_base_t1'
agents_list    = ['agent_adc', 'agent_dfe']

base_path = os.getcwd()
template_path = f'{base_path}/templates'
generate_path = f'{base_path}/uvm/'         # Generated files are stored under same folder.
#NORMAL_UVM_TEST = True                     # Control parameter, output non-*_gen files or not
OVERWRITE_MODE  = True                      # Overwrite protection.                  

# print('Enable overwrite mode? [N/y]:')
# input_temp = input()
# if ((input_temp == 'y') | (input_temp == 'yes') | (input_temp == 'Yes') | (input_temp == 'YES')):
#     OVERWRITE_MODE  = True
# else:
#     OVERWRITE_MODE  = False

env = Environment(loader = FileSystemLoader(template_path))
env.trim_blocks = True
env.lstrip_blocks = True
env.rstrip_blocks = True

template_list = os.listdir(template_path)
template_base_list = []
template_test_list = []
for templ in template_list:
    if('test_' in templ):
        template_test_list.append(templ)
    elif('base_' in templ):
        template_base_list.append(templ)

#################################################################################################
# Main     #
#################################################################################################
if not os.path.exists(generate_path):       # If folder with name not exists, create folder
    os.makedirs(generate_path)
else: 
    if(OVERWRITE_MODE): 
        pass
    else:
        print(f'**********************************Error message:*******************************\n\
    Folder {generate_path} already exists. \n\
    Generator is not working in OVERWRITE mode since OVERWRITE_MODE = False. \n\
    Please assign OVERWRITE_MODE to \'True\' to enable overwrite. \n\
    Please make sure files under folder are backuped or custom changes are useless before enable overwrite!\n\
*************************************************************************************')
        sys.exit()

#################################################################################################
# Following code generates uvm code for each agent    #
#################################################################################################
for agent_name in agents_list:
    
    os.chdir(generate_path)

    if not os.path.exists(agent_name): 
        os.makedirs(agent_name)

    os.chdir(generate_path + agent_name)
    #if (NORMAL_UVM_TEST):                                       # If generate normal uvm test file is wanted, then create them
    for templ in template_base_list:
        filename = templ.replace('base_', f'{agent_name}_')
        template = env.get_template(templ)                      # get template
        output = template.render(name = agent_name)             # get output content from a chosen template
        if (os.path.exists(filename)):                          # if there were old files with same name, then delete the old file
            os.remove(filename)
        f = open(filename, "w")                                 # create file and write output content
        f.write(output)
        f.close()
        print(f'generation file {filename} is done')
    if not os.path.exists('seq'):                               # If folder with name seq not exists under folder proj_name, then create a folder for all generated files.
        os.makedirs('seq')
    os.rename(f'{agent_name}_seq.svh', f'seq/{agent_name}_seq.svh') # mv seq to individuell folder

#################################################################################################
# Following code generate top level files e.g. virtual sequencer and ...     #
#################################################################################################
os.chdir(generate_path)
for templ in template_test_list:
    filename = templ.replace('test_', f'{proj_name}_')
    template = env.get_template(templ)                  # get template
    output = template.render(projname = proj_name, agentlist = agents_list)        # get output content from a chosen template
    if (os.path.exists(filename)):                      # if there were old files with same name, then delete the old file
        os.remove(filename)
    f = open(filename, "w")                             # create file and write output content
    f.write(output)
    f.close()
    print(f'generation file {filename} is done')

if not os.path.exists('seq'):
    os.makedirs('seq')
if not os.path.exists('test'):
    os.makedirs('test')

os.rename(f'{proj_name}_test.svh', f'test/{proj_name}_test.svh')    # mv test and virtual seq to individuell folder
os.rename(f'{proj_name}_virtual_seq.svh', f'seq/{proj_name}_virtual_seq.svh')

