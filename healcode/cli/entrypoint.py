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
from healcode.cli.commands.profile import ProfileCommand
from healcode.cli.commands.baseline import BaselineCommand
from healcode.cli.commands.watch import WatchCommand
from healcode.cli.commands.marketplace import MarketplaceCommand
from healcode.cli.splash import SplashManager
from healcode.config.manager import ConfigManager
from healcode.exceptions import HealCodeError
from healcode.utils.logger import HealCodeLogger
from healcode.constants import ExitCode
from healcode.utils.ui import print_error

def main(argv: Optional[List[str]] = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    else:
        argv = list(argv)

    # Detect and extract global flags from argv to support any position
    json_output = False
    if "--json" in argv:
        json_output = True
        argv = [x for x in argv if x != "--json"]

    no_banner = False
    if "--no-banner" in argv:
        no_banner = True
        argv = [x for x in argv if x != "--no-banner"]

    log_level = None
    if "--log-level" in argv:
        try:
            idx = argv.index("--log-level")
            if idx + 1 < len(argv):
                val = argv[idx + 1]
                if val.upper() not in ["TRACE", "DEBUG", "INFO", "WARN", "ERROR"]:
                    if json_output:
                        import json
                        print(json.dumps({
                            "status": "error",
                            "error": {
                                "type": "ValidationError",
                                "message": f"Invalid logging level: {val}. Choices are TRACE, DEBUG, INFO, WARN, ERROR."
                            },
                            "exit_code": ExitCode.INVALID_USAGE
                        }, indent=4))
                    else:
                        print_error(f"Error: Invalid logging level: {val}. Choices are TRACE, DEBUG, INFO, WARN, ERROR.")
                    return ExitCode.INVALID_USAGE
                log_level = val.upper()
                argv = argv[:idx] + argv[idx+2:]
            else:
                if json_output:
                    import json
                    print(json.dumps({
                        "status": "error",
                        "error": {
                            "type": "ValidationError",
                            "message": "Error: --log-level requires an argument."
                        },
                        "exit_code": ExitCode.INVALID_USAGE
                    }, indent=4))
                else:
                    print_error("Error: --log-level requires an argument.")
                return ExitCode.INVALID_USAGE
        except ValueError:
            pass

    # Register CLI commands
    commands_list: List[BaseCommand] = [
        ScanCommand(),
        ConfigCommand(),
        PluginsCommand(),
        VersionCommand(),
        AICommand(),
        ProfileCommand(),
        BaselineCommand(),
        WatchCommand(),
        MarketplaceCommand()
    ]
    commands = {cmd.name: cmd for cmd in commands_list}

    from healcode.cli.parser import HealCodeArgumentParser
    parser = create_parser(commands)
    if isinstance(parser, HealCodeArgumentParser):
        parser.show_full_help = any(x in argv for x in ["-h", "--help"])
        parser.json_output = json_output
    
    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        # argparse handles help print and exits
        return e.code if isinstance(e.code, int) else ExitCode.INVALID_USAGE

    # Override defaults with pre-processed global flags
    args.json = json_output
    args.no_banner = no_banner
    if log_level is not None:
        args.log_level = log_level

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

    # Render splash only once before the first command is executed
    SplashManager(config=config, no_banner=args.no_banner, json_mode=args.json or config.logging.json_format).display()

    # If no command was passed, show the top-level help screen.
    if args.command is None:
        parser.print_help()
        return ExitCode.SUCCESS

    # Execute matched command
    cmd_obj = commands.get(args.command)
    if not cmd_obj:
        print_error(f"Command not found: {args.command}")
        return ExitCode.INVALID_USAGE

    try:
        # Check for updates unless in json/quiet mode
        if not json_output:
            try:
                from healcode.utils.update import check_for_updates
                from healcode.constants import VERSION
                check_for_updates(VERSION, offline_mode=config.ai.offline_mode)
            except Exception:
                pass
        
        exit_code = cmd_obj.run(args, config)
        return exit_code
    except HealCodeError as e:
        logger.error(f"Execution failed: {e}")
        if json_output:
            import json
            print(json.dumps({
                "command": args.command,
                "status": "error",
                "error": {
                    "type": "HealCodeError",
                    "message": str(e)
                },
                "exit_code": ExitCode.ERROR
            }, indent=4))
        else:
            print_error(f"Error: {e}")
        return ExitCode.ERROR
    except Exception as e:
        logger.exception("An unhandled unexpected exception occurred.")
        if json_output:
            import json
            print(json.dumps({
                "command": args.command,
                "status": "error",
                "error": {
                    "type": type(e).__name__,
                    "message": str(e)
                },
                "exit_code": ExitCode.ERROR
            }, indent=4))
        else:
            print_error(f"Unexpected Error: {e}")
        return ExitCode.ERROR

if __name__ == "__main__":
    sys.exit(main())
