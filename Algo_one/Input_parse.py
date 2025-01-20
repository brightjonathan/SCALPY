import argparse #argparse module in Python's standard library for creating command-line interfaces


#defining a function to parse the arguments
def parse_arguments():

    #creating an ArgumentParser object with a description
    parser = argparse.ArgumentParser(description=" Scapy an AI-Powered Port and Service Scanning Tool")  

    # Target host input
    parser.add_argument(
        "-t", "--target",
        type=str,
        required=True,
        help="Target host (IP address or domain)"
    )

    # Port range input
    parser.add_argument(
        "-p", "--port-range",
        type=str,
        required=True,
        help="Port range to scan (e.g., 20-80)"
    )

    # AI mode toggle
    parser.add_argument(
        "--ai-mode",
        action="store_true",
        help="Enable AI mode for intelligent scanning"
    )


    return parser.parse_args(); #parse the arguments and return the result
