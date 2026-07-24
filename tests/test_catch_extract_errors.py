"""Tests error handling in extract_transcripts.py."""

import sys
import io
from youtube_transcript_api import YouTubeTranscriptApi
from bin.extract_transcripts import main

def test_extract_transcripts_catch_errors(monkeypatch, capsys):
    """
    Verifies that my script catches an error when an
    unfetchable video ID hits the input processor stream.
    """

    # Creates a fake fetch that automatically raises an error.
    def failed_fetch(_, video_id):
        assert video_id == "notarealid99"
        raise RuntimeError("Not able to fetch transcript")

    monkeypatch.setattr(YouTubeTranscriptApi,"fetch",failed_fetch)

    # Mock Standard Input to feed a fake invalid video id into the script.
    mock_input_stream= io.StringIO("notarealid99\n")
    monkeypatch.setattr(sys, "stdin", mock_input_stream)

    # Triggers the script's main entry point execution loop directly
    main()

    # Intercept the standard console terminal print buffers using capsys
    captured_output = capsys.readouterr()

    # Makes sure there is no JSON transcript was printed for this failed video ID.
    assert captured_output.out == ""
