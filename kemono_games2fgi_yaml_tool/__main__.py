import argparse
from argparse import RawTextHelpFormatter
from os.path import dirname
from loguru import logger
from pathlib import Path

from .converter import Converter
from .scanner import compare
from .utils.setting import config, default_config


parser = argparse.ArgumentParser(
    description="""
Noun Explanation:
FGI path: https://github.com/FurryGamesIndex/games The folder downloaded from this URL.
KEMONO path: https://github.com/kemono-games/fgi The folder downloaded from this URL.

Usage example:
   py -m kemono_games2fgi_yaml_tool -i c:\\downloads\\games c:\\downloads\\fgi -o OUTPUT_FOLDER --sm.ms YOUR_TOKEN
                                 """.strip(),
    formatter_class=RawTextHelpFormatter,
)
exclusive1 = parser.add_mutually_exclusive_group(required=True)
exclusive1.add_argument(
    "-i",
    "--input",
    type=str,
    nargs=2,
    metavar=("FGI_PATH", "KEMONO_PATH"),
    help="input folders.args is 2 (this option conflicts with --single)",
)
exclusive1.add_argument(
    "-s",
    "--single",
    type=str,
    metavar="SINGLE_FILE",
    help="Whether to convert only a single yaml file (this option conflicts with --input)",
)

parser.add_argument("-o", "--output", type=str, required=True)

exclusive2 = parser.add_mutually_exclusive_group(required=True)
exclusive2.add_argument(
    "-f",
    "--config",
    type=str,
    help="Location of the configuration file, see README for this project (this option conflicts "
    "with -sm.ms)",
)
exclusive2.add_argument(
    "--sm.ms",
    type=str,
    metavar="SM.MS_TOKEN_VALUE",
    help="Value of the Token, see the README for this project (this option conflicts with -f).",
)

args = parser.parse_args()
if args.config:
    if not args.single:
        config.load(args.config)
    else:
        config.base_path = Path(dirname(args.single)).parent
        config.load(args.config)
else:
    if not args.single:
        config.load(
            {
                **default_config,
                "sm_ms_token": getattr(args, "sm.ms"),
                "base_path": args.input[1],
            }
        )
    else:
        config.load(
            {
                **default_config,
                "sm_ms_token": getattr(args, "sm.ms"),
                "base_path": Path(dirname(args.single)).parent,
            }
        )
logger.info("\n" + str(config))
if not args.single:
    result = compare(Path(args.input[1]) / "games", Path(args.input[0]) / "games")
    for i in result:
        Converter(i, args.output).convert()
else:
    Converter(args.single, args.output).convert()
