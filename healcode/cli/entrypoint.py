"""
HealCode CLI Main Entry Point
"""

import sys
import argparse
from typing import List, Optional
from healcode.cli.parser import create_parser
from healcode.cli.commands.base import BaseCommand
from healcode.cli.commands.scan import ScanCommand
from healcode.cli.commands.config import ConfigCommand
from healcode.cli.commands.plugins import PluginsCommand
from healcode.cli.commands.version import VersionCommand
from healcode.cli.commands.ai_cmd import AICommand
from healcode.config.manager import ConfigManager
from healcode.exceptions import HealCodeError
from healcode.utils.logger import HealCodeLogger
from healcode.constants import ExitCode
from healcode.utils.ui import print_error

def main(argv: Optional[List[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    # Register CLI commands
    commands_list: List[BaseCommand] = [
        ScanCommand(),
        ConfigCommand(),
        PluginsCommand(),
        VersionCommand(),
        AICommand(),
    ]
    commands = {cmd.name: cmd for cmd in commands_list}

    parser = create_parser(commands)
    
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        # argparse handles help print and exits
        return e.code if isinstance(e.code, int) else ExitCode.INVALID_USAGE

    # Load configuration
    try:
        config_manager = ConfigManager()
        config = config_manager.load()
    except HealCodeError as e:
        print_error(f"Configuration Error: {e}")
        return ExitCode.CONFIG_ERROR

    # Override logging level if specified via CLI
    log_level = args.log_level or config.logging.level
    json_output = args.json or config.logging.json_format
    
    # Setup global logger
    HealCodeLogger.setup(level=log_level, json_output=json_output)
    logger = HealCodeLogger.get_logger()
    logger.debug("Logging initialized.")

    # Execute matched command
    cmd_obj = commands.get(args.command)
    if not cmd_obj:
        print_error(f"Command not found: {args.command}")
        return ExitCode.INVALID_USAGE

    try:
        exit_code = cmd_obj.run(args, config)
        return exit_code
    except HealCodeError as e:
        logger.error(f"Execution failed: {e}")
        if not json_output:
            print_error(f"Error: {e}")
        return ExitCode.ERROR
    except Exception as e:
        logger.exception("An unhandled unexpected exception occurred.")
        if not json_output:
            print_error(f"Unexpected Error: {e}")
        return ExitCode.ERROR

if __name__ == "__main__":
    sys.exit(main())
