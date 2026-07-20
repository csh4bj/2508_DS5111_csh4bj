#!/usr/bin/env python3
"""Enrich transcript records with structured data from the Gemini API."""

import sys
import os
import json
import logging
from abc import ABC, abstractmethod

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environmental configurations from local workspace files
load_dotenv()

# Audit logging framework tracking pipeline telemetry
logging.basicConfig(
    filename='logs/pipeline_audit.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class LLMStrategy(ABC):
    """Abstract contract for transcript enrichment strategies."""
    @abstractmethod
    def enrich(self, video_id: str, raw_text: str) -> dict:
        """
        Takes in transcript data and returns a dictionary matching
        the enrichment response schema.
        """
        pass

def main():
    """Read transcript JSONL records, enrich them, and emit structured JSONL."""
    logging.info("Pipeline Step 2B (Gemini Enrichment) started.")

    # -------------------------------------------------------------------------
    # API Environment Validation and Client Initialization
    # Extract the necessary credential key token from the local environment.
    # If the token is missing, log a critical failure and terminate the system.
    # Otherwise, instantiate the official Google GenAI Client utility.
    # -------------------------------------------------------------------------
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        logging.critical("GEMINI_API_KEY is not configured.")
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    # -------------------------------------------------------------------------
    # Structured Output Response Schema Definition
    # To prevent the LLM from returning unpredictable formats that would crash
    # downstream applications, define a strict "Data Contract" using a JSON
    # Schema layout.
    #
    # Enforce a response type of "OBJECT" that guarantees the presence of:
    #   - video_id: (STRING, Required)
    #   - cleaned_text: (STRING, Required)
    #   - tech_terms: (ARRAY of STRINGS)
    #   - book_names: (ARRAY of STRINGS)
    # -------------------------------------------------------------------------
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "video_id": {
                "type": "STRING"
            },
            "cleaned_text": {
                "type": "STRING"
            },
            "tech_terms": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            },
            "book_names": {
                "type": "ARRAY",
                "items": {
                    "type": "STRING"
                }
            }
       },
       "required": [
           "video_id",
           "cleaned_text",
           "tech_terms",
           "book_names"
       ]
    }

    # Stream processing framework reading line-by-line text inputs from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        # ---------------------------------------------------------------------
        # Inbound String Stream Deserialization
        # Safely wrap your stream ingestion inside an isolated try-except block.
        # Parse the raw line string object into a key-value dictionary and
        # extract the target 'video_id' and 'raw_text' properties.
        # Log any malformed line tracks and continue processing the stream.
        # ---------------------------------------------------------------------
        try:
            payload = json.loads(line)
            video_id = payload["video_id"]
            raw_text = payload["raw_text"]
        except (json.JSONDecodeError, KeyError, TypeError) as exc:
            logging.error(
                "Failed to parse incoming JSON payload row: %s",
                exc,
            )
            continue

        logging.info(
            "Orchestrating Gemini enrichment for video: %s",
            video_id,
        )

        prompt = f"""
        You are an elite data engineer. Clean this transcript text for video_id '{video_id}'.
        1. Strip all timestamps and duration codes.
        2. Extract technical architecture terms and books.
        """

        # ---------------------------------------------------------------------
        # Structured Model Invocation and Instant Stream Flushing
        # Call the 'gemini-2.5-flash' model via the unified SDK interface.
        # Inject the constructed prompt along with the raw text sequence payload.
        # Map the configuration block to use the structured JSON mime-type
        # and enforce your defined response schema parameters.
        # Write the resulting text explicitly to sys.stdout and flush immediately.
        # ---------------------------------------------------------------------
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt + "\n\nTranscript:\n" + raw_text,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=response_schema,
                ),
            )
            enriched_payload = json.loads(response.text)
            sys.stdout.write(json.dumps(enriched_payload) + "\n")
            sys.stdout.flush()

        except Exception as exc:  # pylint: disable=broad-exception-caught
            logging.error(
                "Failed processing video %s during LLM generation: %s",
                video_id,
                exc,
            )

    logging.info("Pipeline Step 2B finished.")

if __name__ == '__main__':
    main()
