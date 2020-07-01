

##  IMPORTS

import time


##  LOCAL IMPORTS

import backup
import stopstart


##  MAIN 

def main():
    stopstart.stop()
    time.sleep(10)  # wait for server to fully stop
    backup.backup()
    stopstart.start()


##  EXE

if __name__ == "__main__":
    main()
