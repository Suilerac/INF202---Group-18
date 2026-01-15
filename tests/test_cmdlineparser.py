import pytest
from InputOutput.commandlineParser import CommandlineParser


@pytest.fixture
def clp(tmp_path):
    clp = CommandlineParser()
    clp._folder = str(tmp_path)
    return clp


def test_setConfigList(clp, tmp_path):
    assert f"{tmp_path}/input.toml" in clp.configs
