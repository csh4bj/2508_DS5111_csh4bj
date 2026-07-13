"""Tests for the project environment and required pytest markers."""

import platform
import sys
import pytest
from bin.clean_ids import valid_id

@pytest.mark.skipif(
    platform.system() != "Linux",
    reason="This test only applies to Linux environments.",
)

def test_is_ubuntu():
    '''Makes sure the operating system is running on Ubuntu.'''
    assert "ubuntu" in platform.version().lower()

def test_version_python():
    '''Checks to make sure that Python 3 is being used.'''
    assert sys.version_info.major == 3

@pytest.mark.xfail(reason="Demonstrates an expected failure.")
def test_expected_to_fail():
    '''A test that is expected to fail.'''
    assert False

@pytest.mark.skip(reason="Feature is not ready")
def test_expected_to_skip():
    """A test that is expected to be skipped."""
    assert True

@pytest.mark.parametrize(
    "youtube_id, expected_outcome",
    [("CaMer0n_H3r", True), ("JohnWall2", False), ("JaydenDanielsNumber5", False),],
    )

def test_parametrized(youtube_id, expected_outcome):
    '''Tests several Youtube IDs at once'''
    assert valid_id(youtube_id) is expected_outcome
