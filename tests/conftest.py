import pytest
from pathlib import Path
import os

pai = os.path.dirname(__file__ )
examples_path = pai +'/examples'


@pytest.fixture
def example():
    return lambda p: open(examples_path+ "/" + p).read()
