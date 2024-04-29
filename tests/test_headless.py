import pytest
from main import *

def test_headless():
    with pytest.raises(SystemExit) as e:
        main("headless")
    assert e.value.code == 0
