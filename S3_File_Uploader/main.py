import os
import logging
from datetime import datetime

from UI.ProgramController import ProgramController


# Set up file based logger
current_datetime = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
log_path = os.getcwd() + f'/logs/{current_datetime}.log'

# Check if a logs directory is created, if not then it is created.
if not os.path.exists(os.getcwd() + '/logs'):
    os.makedirs(os.getcwd() + '/logs')

# Changed the setup of the logger from the basicConfig so that the file isn't logging the imported modules
logger = logging.getLogger('main_logger')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(log_path)
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(filename)s:%(funcName)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


logger.debug("Logger setup.")


def main():
    logger.debug("Starting program.")

    pc = ProgramController()
    pc.mainloop()

    logger.debug("Exiting program.")


if __name__ == "__main__":
    main()
