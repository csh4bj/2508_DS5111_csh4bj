# File location: tests/test_load_snowflake.py
"""Tests for the Snowflake JSONL loading pipeline."""
import io
import json
import sys
from unittest.mock import MagicMock

import pytest
import snowflake.connector

from bin.load_snowflake import main

def test_load_snowflake_pipeline_ingestion_loop(monkeypatch):
    """
    Verifies that main() correctly processes stringified JSON lines from stdin,
    triggers table structural validation DDL, and executes safe parameter-bound insertions.
    """
    # 1. Setup mock database connector dependencies
    mock_cursor = MagicMock()
    mock_context = MagicMock()
    mock_context.cursor.return_value = mock_cursor

    # 2. Prevent the script from attempting real external network calls
    monkeypatch.setattr(snowflake.connector, "connect", lambda **kwargs: mock_context)

    # 3. Intercept and isolate execution shell environment state
    monkeypatch.setenv("SF_USER", "test_user")
    monkeypatch.setenv("SF_PASSWORD", "test_password")

    # 4. Fabricate structured incoming JSON Lines streaming content
    mock_input_stream = io.StringIO(
        '{"video_id": "test_id_001", "source": "youtube", "raw_text": "Sample content text A."}\n'
        '{"video_id": "test_id_002", "source": "podcast", "raw_text": "Sample content text B."}\n'
    )
    monkeypatch.setattr(sys, "stdin", mock_input_stream)

    # 5. Execute the target script
    try:
        main()
    except UnboundLocalError:
        pytest.fail(
            "Resource variables were referenced before definition. "
            "Verify cursor initialization logic."
        )

    # 6. Verify that table creation and insertion statements occurred
    assert mock_cursor.execute.call_count >= 3, (
        "The cursor should create the table and insert both input rows."
    )

    executed_queries = [
        call[0][0]
        for call in mock_cursor.execute.call_args_list
    ]
    executed_bindings = [
        call[0][1]
        for call in mock_cursor.execute.call_args_list
        if len(call[0]) > 1
    ]

    assert any(
        "CREATE TABLE IF NOT EXISTS RAW_TRANSCRIPTS" in query
        for query in executed_queries
    ), (
        "The script must verify that the target table exists."
    )

    insert_queries = [
        query
        for query in executed_queries
        if "INSERT INTO RAW_TRANSCRIPTS" in query
    ]
    assert len(insert_queries) == 2, (
        "Exactly two SQL insert calls should occur."
    )

    for query in insert_queries:
        assert "PARSE_JSON(%s)" in query, (
            "Payloads must be wrapped in PARSE_JSON."
        )
        assert "%s" in query and "f" not in query, (
            "Use parameter placeholders instead of hard-coded formatting."
        )
    # Ensure parameter payloads are passed safely within matching positional argument tuples
    assert len(executed_bindings) == 2
    parsed_payload = json.loads(executed_bindings[0][0])
    assert parsed_payload["video_id"] == "test_id_001"
