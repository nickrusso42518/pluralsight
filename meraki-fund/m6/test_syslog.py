import logging
import logging.handlers

logger = logging.getLogger("globo_test")
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address = ("19.0.2.1", 514))
logger.addHandler(handler)
logger.info("GLOBOMANTICS TEST")
