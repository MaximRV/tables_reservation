import json
import logging
from datetime import datetime

from pythonjsonlogger import jsonlogger

from app.config import settings

logger = logging.getLogger()

logHandler = logging.StreamHandler()


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict
        )
        if not log_record.get("timestamp"):
            now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            log_record["timestamp"] = now
        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

        if 'message' in log_record:
            log_record['message'] = self.process_message(log_record['message'])

    def process_message(self, message):
        # Преобразование объектов в строку
        if isinstance(message, dict):
            # Обработка объектов datetime
            for key, value in message.items():
                if isinstance(value, datetime):
                    message[key] = value.isoformat()  # Преобразуем datetime в строку
            return json.dumps(message, ensure_ascii=False)
        return str(message)





formatter = CustomJsonFormatter(
    "%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s"
)

logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LEVEL)

