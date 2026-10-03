from config.logger import RUN_ID, get_logger


def test_run_id_format():
    date_part, suffix = RUN_ID.split("_")
    assert len(date_part) == 15 and len(suffix) == 6


def test_logger_not_duplicated():
    assert get_logger("x") is get_logger("x")
    assert len(get_logger("x").handlers) == 2
