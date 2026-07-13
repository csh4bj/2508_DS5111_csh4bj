"""Unit tests for clean_ids.py."""

import sys
import io
from bin.clean_ids import main, valid_id

def test_script_execution(monkeypatch, capsys):
    """Tests the complete clean_ids pipeline."""
    # 1. Simulate the standard input data
    # We use io.StringIO to make a string act like a readable stream/file
    fake_input = io.StringIO("kcFsuxaJ1es\nasd123\nN1k0laJ0k1c\n")
    monkeypatch.setattr(sys, "stdin", fake_input)

    # 2. Run the script's main logic
    main()

    # 3. Capture the printed output
    captured = capsys.readouterr()

    # 4. Assert that the data was modified correctly
    assert captured.out == "kcFsuxaJ1es\nN1k0laJ0k1c\n"

def test_valid_id():
    """ This tests a valid ID that follows all the Youtube ID rules."""
    assert valid_id("CaMer0n_H3r") is True

def test_short_id():
    """ This tests an invalid ID that is too short."""
    assert valid_id("JohnWall2") is False

def test_long_id():
    """ This tests an invalid ID that is too long."""
    assert valid_id("JaydenDanielsNumber5") is False
