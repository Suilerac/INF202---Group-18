import pytest
from InputOutput.commandlineParser import CommandlineParser


@pytest.fixture
def clp_specific(tmp_path):
    """
    Returns a commandlineparser with findAll set to false
    """
    clp = CommandlineParser()
    f = open(f"{tmp_path}/input.toml", 'w')
    f.close()
    clp._folder = str(tmp_path)
    clp._findAll = False
    clp._config_file = "input.toml"
    clp.setConfigList()
    return clp


@pytest.fixture
def clp_findall(tmp_path):
    """
    Returns a commandlineparser with findAll set to true
    """
    clp = CommandlineParser()
    f = open(f"{tmp_path}/input.toml", 'w')
    pp = open(f"{tmp_path}/pyproject.toml", 'w')
    f.close()
    pp.close()
    clp._folder = str(tmp_path)
    clp._findAll = True
    clp._config_file = "input.toml"
    clp.setConfigList()
    return clp


def test_setConfigListSpecific(clp_specific, tmp_path):
    """
    Tests that it correctly adds input.toml to configs when findall is false
    """
    assert f"{tmp_path}/input.toml" in clp_specific.configs


def test_setConfigListFindall(clp_findall, tmp_path):
    """
    Tests that it correctly adds input.toml to configs when findall is true
    """
    assert f"{tmp_path}/input.toml" in clp_findall.configs


def test_folder(clp_specific, tmp_path):
    """
    Tests folder getter
    """
    assert clp_specific.folder == str(tmp_path)


def test_configs(clp_specific, tmp_path):
    """
    Tests configs getter
    """
    assert clp_specific.configs == [f"{tmp_path}/input.toml"]


def test_config_file(clp_specific):
    """
    Tests config file getter
    """
    assert clp_specific.config_file == "input.toml"


def test_findAll(clp_specific):
    """
    Tests findAll getter
    """
    assert not clp_specific.findAll


def test_pyproject_removal(clp_findall, tmp_path):
    """
    Checks that it doesn't add pyproject.toml to configs
    """
    assert f"{tmp_path}/pyproject.toml" not in clp_findall.configs
