#!/usr/bin/env python3

import sys
import re

def valid_id(youtube_id: str) -> bool:
    """
    This function checks if the string is a valid YouTub ID which contains
    exactly 11 characters consisting of the following 64 possibilities:
    A-Z, a-z, 0-9, -, _.
    Returns True if the ID follows the valid ID rules.
    Returns False, if the ID does not follow the valid ID rules.
    """
    return bool(
        re.match(r"^[A-Za-z0-9_-]{11}$", youtube_id )
    )
def main():
    try:
        with open("pipeline_autid.log", "a") as youtube_log:
            for row in sys.stdin:
                youtube_id = row.strip()

                if not youtube_id:
                    continue

                if valid_id(youtube_id):
                    print(youtube_id)
                else:
                    youtube_log.write(f"Invalid ID: {youtube_id}\n")

    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
