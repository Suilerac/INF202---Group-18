from InputOutput.tomlParser import TomlParser
import pytest


@pytest.fixture
def tp(tmp_path):
    tfile = f"{tmp_path}/test.toml"
    config = [
        "[settings]\n",
        "nSteps = 500\n",
        "tEnd = 0.5\n",
        "[geometry]\n",
        "meshName = \"meshes/bay.msh\"\n",
        "borders = [[0.0, 0.45], [0.0, 0.2]]\n",
        "[IO]\n",
        "logName = \"log\"\n",
        "writeFrequency = 20"
    ]
    with open(tfile, 'w') as f:
        f.writelines(config)
    return TomlParser(tfile)


def test_nSteps(tp):
    assert tp.nSteps == 500


def test_tEnd(tp):
    assert tp.tEnd == pytest.approx(0.5)


def test_meshName(tp):
    assert tp.meshName == "meshes/bay.msh"


def test_borders(tp):
    assert tp.borders == [[0.0, 0.45], [0.0, 0.2]]


def test_logName(tp):
    assert tp.logName == "log"


def test_writeFrequency(tp):
    assert tp.writeFrequency == 20
