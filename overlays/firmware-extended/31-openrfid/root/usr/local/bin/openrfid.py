#!/usr/bin/env python3

import configparser
import logging
import logging.handlers
import os
import re
import runpy
import sys


_FM175XX_READER = "/home/lava/klipper/klippy/extras/fm175xx_reader.py"


def _snapmaker_key():
    try:
        with open(_FM175XX_READER, "r") as f:
            content = f.read()
    except OSError as e:
        print(f"Error: cannot read Klipper RFID driver at {_FM175XX_READER}: {e}", file=sys.stderr)
        sys.exit(1)
    m = re.search(r'FM175XX_M1_CARD_HKDF_SALT_KEY_B\s*=\s*b"([^"]+)"', content)
    if m is None:
        print(
            f"Error: Snapmaker HKDF key not found in {_FM175XX_READER}. "
            "The firmware driver may have changed.",
            file=sys.stderr,
        )
        sys.exit(1)
    return m.group(1).encode().hex()


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <target.cfg> [source.cfg ...]")
        sys.exit(1)

    target = sys.argv[1]
    sources = sys.argv[2:]

    config = configparser.RawConfigParser()
    config.optionxform = str
    config.read(sources)

    if not config.has_section("snapmaker_tag_processor"):
        config.add_section("snapmaker_tag_processor")
    config.set("snapmaker_tag_processor", "key", _snapmaker_key())

    with open(target, "w") as f:
        config.write(f)

    handler = logging.handlers.SysLogHandler(address="/dev/log")
    logging.root.handlers = [handler]
    logging.root.setLevel(logging.DEBUG)

    sys.argv = [sys.argv[0], target]
    sys.path.insert(0, "/usr/local/share/openrfid")
    os.chdir("/usr/local/share/openrfid")
    runpy.run_path("main.py", run_name="__main__")


if __name__ == "__main__":
    main()
