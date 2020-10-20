
import subprocess
from subprocess import Popen, PIPE
import time
from time import sleep
from selenium import webdriver



def main(timerLinkedIn, timerScrape, timerGlassdoor):
    


    
    proc1 = Popen(['python3', '01_LinkedIn.py'])
    #proc1.communicate()
    start_time = time.time()
    while True:
        
        delta_t = time.time()-start_time
        if delta_t > timerLinkedIn:
            proc1.terminate()
            break
        time.sleep(1)
    #ret = proc1.wait()
    sleep(2)

    proc2 = Popen(['python3', '01B_LinkedIn.py'])

    while True:
        
        delta_t2 = time.time()-start_time
        if delta_t2 > timerLinkedIn + timerScrape + 2 :
            proc2.terminate()
            break
        time.sleep(1)

    sleep(5)


    proc3 = Popen(['python3', '02_Glassdoor.py'])

    while True:
        
        delta_t3 = time.time()-start_time
        if delta_t3 > timerLinkedIn + timerScrape + timerGlassdoor + 2 :
            proc3.terminate()
            break
        time.sleep(1)

    sleep(5)

    
    proc4 = Popen(['cmd.exe', '/C', 'start', 'http://localhost:8888/tree'])  
    sleep(2)
    proc4.terminate()
    
    sleep(2)
    #proc4 = Popen(['jupyter', '-notebook'])
    proc5 = Popen(['jupyter', 'notebook', '03_Alumni.ipynb'])
    #proc4.wait()        
    

    
  
if __name__ == '__main__':
    main(30, 200, 120)


