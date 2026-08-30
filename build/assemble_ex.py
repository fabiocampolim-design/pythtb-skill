# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Fabio Campolim
"""Backward-compatible alias: assemble only the exercises notebook.

Equivalent to ``python build/assemble.py --which exercises`` (all of that
script's options are accepted here too).
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assemble import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main(["--which", "exercises", *sys.argv[1:]]))
