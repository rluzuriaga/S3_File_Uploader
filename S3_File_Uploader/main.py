import os
import logging
from datetime import datetime

from UI.ProgramController import ProgramController


# Set up file based logger
current_datetime = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
log_path = os.getcwd() + f'/logs/{current_datetime}.log'

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s:%(funcName)s - %(message)s',
                    filename=log_path,
                    filemode='a')

logger = logging.getLogger('main_logger')

logger.debug("Logger setup.")


def main():
    logger.debug("Starting program.")

    pc = ProgramController()
    pc.mainloop()

    logger.debug("Exiting program.")


if __name__ == "__main__":
    main()
