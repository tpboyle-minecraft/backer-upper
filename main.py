

##  IMPORTS

import time


##  LOCAL IMPORTS

import backup
import stopstart


##  CONSTANTS

stop_buffer = 20  # time in seconds to wait for server to fully stop


##  MAIN 

def main():
    stopstart.stop()
    time.sleep(stop_buffer)
    try:
        backup.backup()
    finally:
        stopstart.start()


##  EXE

if __name__ == "__main__":
    main()
