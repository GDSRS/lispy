import pytest
from pathlib import Path
import os


examples_path = os.getcwd() +'/tests/examples'


@pytest.fixture
def example():
    return lambda p: open(examples_path+ "/" + p).read()
