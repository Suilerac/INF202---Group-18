import pytest
import os
from InputOutput.log import Log


@pytest.fixture
def log(tmp_path):
    return Log(f"{tmp_path}/log.log")


def test_existance(log, tmp_path):
    log.debug("Debug")
    assert "log.log" in os.listdir(tmp_path)


def test_debug(log, tmp_path):
    log.debug("Test")
    with open(f"{tmp_path}/log.log", 'r') as f:
        line = f.readline().strip().split(' ')
        assert line[-1] == "Test"


def test_info(log, tmp_path):
    log.info("Test")
    with open(f"{tmp_path}/log.log", 'r') as f:
        line = f.readline().strip().split(' ')
        assert line[-1] == "Test"


def test_error(log, tmp_path):
    log.error("Test")
    with open(f"{tmp_path}/log.log", 'r') as f:
        line = f.readline().strip().split(' ')
        assert line[-1] == "Test"


def test_critical(log, tmp_path):
    log.critical("Test")
    with open(f"{tmp_path}/log.log", 'r') as f:
        line = f.readline().strip().split(' ')
        assert line[-1] == "Test"
