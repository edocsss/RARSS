import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
web_logger = logging.getLogger('webapp')
classifier_logger = logging.getLogger('classifier')
data_processor_logger = logging.getLogger('data_processor')