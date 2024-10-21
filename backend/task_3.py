from pathlib import Path
from enum import Enum
from datetime import date, time


class LogLevel(Enum):
    INFO = 'INFO'
    DEBUG = 'DEBUG'
    ERROR = 'ERROR'
    WARNING = 'WARNING'


def parse_log_line(line: str) -> dict[str, object]:
    try:
        line_split: list[str] = line.split(sep=' ')
        message_date: date = date.fromisoformat(line_split[0])
        message_time: time = time.fromisoformat(line_split[1])
        message_level: LogLevel = LogLevel(line_split[2])
        message_text: str = str(line_split[3])
    except:
        raise ValueError('Please, provide valid log file.')

    message: dict[str, object] = {
        'date': message_date,
        'time': message_time,
        'level': message_level,
        'text': message_text,
    }

    return message


def split_logfile(text: str) -> list[dict[str, object]]:
    return list(map(parse_log_line, [l for l in text.split(sep='\n') if len(l) > 0]))


def load_logs(file_path: str) -> list[dict[str, object]]:
    with open(Path(file_path), 'r') as file:
        return list(map(parse_log_line, file.readlines()))


def filter_logs_by_level(
    logs: list[dict[str, object]], level: LogLevel
) -> list[dict[str, object]]:
    return list(filter(lambda log: log if log['level'] is level else None, logs))


def count_logs_by_level(logs: list[dict[str, object]]) -> dict[str, int]:
    return {
        level.name: len(filter_logs_by_level(logs=logs, level=level))
        for level in LogLevel
    }


def count_messages_in_logfile(input_text: str, input_level: LogLevel) -> int:
    messages_all: list[dict[str, object]] = split_logfile(text=input_text)

    messages_filtered: list[dict[str, object]] = filter_logs_by_level(
        logs=messages_all, level=input_level
    )

    n_filtered_messages: int = len(messages_filtered)

    return n_filtered_messages
