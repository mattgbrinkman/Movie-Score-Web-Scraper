import logging

class SingletonLogger:
    _instance = None

    @staticmethod
    def get_instance():
        if SingletonLogger._instance is None:
            SingletonLogger()
        return SingletonLogger._instance

    def __init__(self):
        if SingletonLogger._instance is not None:
            raise Exception("Only one instance of this class is allowed")
        else:
            SingletonLogger._instance = self
            self._setup_logging()

    def _setup_logging(self):
        """
        Set up logging configuration.
        """
        self.logger = logging.getLogger("mylog")
        self.logger.setLevel(logging.DEBUG)

        # Create handlers
        console_handler = logging.StreamHandler()  # Console handler
        file_handler = logging.FileHandler("debug.log")  # File handler

        # Set level for handlers
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.DEBUG)

        # Create a formatter and set it for handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger