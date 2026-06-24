import argparse
import sys
from . import analyzer, dom_utils

def main():
    parser = argparse.ArgumentParser(description="Gitee Cleanup CLI Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Subcommand: report
    subparsers.add_parser("report", help="Analyze HAR file and generate GraphQL requests report")

    # Subcommand: find-parents
    parents_parser = subparsers.add_parser("find-parents", help="Find ancestors of a DOM element in the HTML file")
    parents_parser.add_argument("-t", "--type", choices=["alt", "text", "class", "tag"], default="text",
                               help="Type of selector to search for (default: text)")
    parents_parser.add_argument("value", help="Value of the selector to search for")
    parents_parser.add_argument("-l", "--levels", type=int, default=8, help="Max levels of ancestors to print")

    # Subcommand: find-text
    text_parser = subparsers.add_parser("find-text", help="Search for text context in the HTML file (excluding scripts/styles)")
    text_parser.add_argument("keyword", help="Text to search for")
    text_parser.add_argument("-w", "--window", type=int, default=200, help="Number of surrounding characters to print")

    args = parser.parse_args()

    if args.command == "report":
        analyzer.generate_report()
    elif args.command == "find-parents":
        dom_utils.find_element_ancestors(args.type, args.value, args.levels)
    elif args.command == "find-text":
        dom_utils.print_text_context(args.keyword, args.window)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
