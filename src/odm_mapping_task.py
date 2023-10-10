''' 
    This script provides making task for ODM
    Made by Andrey Underoak(https://github.com/AndreyUnderoak) & Nancy Underoak(https://github.com/NancyUnderoak)
'''

import os
import sys
import time
from termcolor import colored

sys.path.append('..')

import pyodm 

# node = pyodm.Node("localhost", 3000)
fastMode = False
resolution = 2
skipPDF  = False
if(len(sys.argv) < 4):
    print(colored("Please write ip and port: python3 odm_mapping_task.py <path to images> <ip> <port> (optional)<?fast> (optional)<?skipPDF>",'red'))
    exit()
else:
    path_to_images   = sys.argv[1]
    adress           = sys.argv[2]
    port             = sys.argv[3]
    if(len(sys.argv) > 4):
        if(sys.argv[4]=="fast"):
            fastMode = True
            resolution = 0.1
            print(colored("FastMode Enabled", 'green'))
        if(len(sys.argv) > 5):
            if(sys.argv[5]=="skipPDF"):
                skipPDF = True
                print(colored("PDF Enabled", 'green'))
                
print(colored("adress = " + str(adress),'white','on_yellow',['bold']))
print(colored("port   = " + str(port),'white','on_yellow',['bold']))
    
node = pyodm.Node(adress, port)

try:
    # Start a task
    print(colored("Uploading images...",'yellow'))
    l = os.listdir(path_to_images)
    l = [path_to_images + s for s in l]
    print(l)
    
    task = node.create_task(l, {'orthophoto-resolution': resolution, 'dsm': True, 'skip-report':skipPDF, 'fast-orthophoto':fastMode})
    print(task.info())

    try:
        # This will block until the task is finished
        # or will raise an exception
        print("\nTask INFO:")
        i = ""
        while(task.info().status != pyodm.types.TaskStatus.COMPLETED and task.info().status != pyodm.types.TaskStatus.FAILED):
            print ("\033[A                             \033[A")
            
            i += "."
            if i == ".....":
                i = ""
                
            print(str(task.info().status) + " " + str(task.info().progress) + "% " + i)
            time.sleep(0.3)
        # task.wait_for_completion()

        print("Task completed, downloading results...")

        # Retrieve results
        task.download_assets("./odm_media/results")

        print("Assets saved in ./odm_media/results (%s)" % os.listdir("./odm_media/results"))

    except pyodm.exceptions.TaskFailedError as e:
        print("\n".join(task.output()))

except pyodm.exceptions.NodeConnectionError as e:
    print("Cannot connect: %s" % e)
except pyodm.exceptions.NodeResponseError as e:
    print("Error: %s" % e)
