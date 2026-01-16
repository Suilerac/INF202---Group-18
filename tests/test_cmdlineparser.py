import pytest
from InputOutput.commandlineParser import CommandlineParser


@pytest.fixture
def clp(tmp_path):
    clp = CommandlineParser()
    f = open(f"{tmp_path}/input.toml", 'w')
    f.close()
    clp._folder = str(tmp_path)
    clp._findAll = False
    clp._config_file = "input.toml"
    clp.setConfigList()
    return clp


def test_setConfigList(clp, tmp_path):
    assert f"{tmp_path}/input.toml" in clp.configs
