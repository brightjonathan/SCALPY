#importing all modules
from Algo_one import Input_parse, Input_Validation
from Algo_two.Port_Scanning import scan_ports
from Algo_three.Service_detection import detect_service

# Function to display ASCII art banner
def display_banner():
    print('''
      \033[31mSSSS\033[0m   \033[32mCCCC\033[0m   \033[33mAAAA\033[0m   \033[34mLLLL\033[0m   \033[35mPPPP\033[0m   \033[36mYYYY\033[0m   
     \033[31mS\033[0m     \033[31mS\033[0m \033[32mC\033[0m      \033[33mA\033[0m    \033[33mA\033[0m \033[34mL\033[0m      \033[35mP\033[0m   \033[35mP\033[0m   \033[36mY\033[0m     
     \033[31mS\033[0m       \033[32mC\033[0m      \033[33mA\033[0m    \033[33mA\033[0m \033[34mL\033[0m      \033[35mP\033[0m   \033[35mP\033[0m   \033[36mY\033[0m     
      \033[31mSSSS\033[0m  \033[32mC\033[0m      \033[33mAAAAAA\033[0m \033[34mL\033[0m      \033[35mPPPP\033[0m    \033[36mY\033[0m     
           \033[31mS\033[0m \033[32mC\033[0m      \033[33mA\033[0m    \033[33mA\033[0m \033[34mL\033[0m      \033[35mP\033[0m     \033[36mY\033[0m     
     \033[31mS\033[0m     \033[31mS\033[0m \033[32mC\033[0m      \033[33mA\033[0m    \033[33mA\033[0m \033[34mL\033[0m      \033[35mP\033[0m     \033[36mY\033[0m     
      \033[31mSSSS\033[0m   \033[32mCCCC\033[0m   \033[33mA\033[0m    \033[33mA\033[0m \033[34mLLLL\033[0m   \033[35mP\033[0m     \033[36mY\033[0m     
    ''')

# Main function
def main():
    display_banner()
    args = Input_parse.parse_arguments()

    # Validate inputs
    if not Input_Validation.validate_target(args.target):
        print("Invalid target host. Exiting...")
        exit(1)

    if not Input_Validation.validate_port_range(args.port_range):
        print("Invalid port range. Exiting...")
        exit(1)

    try:
        # Parse port range
        if '-' in args.port_range:
            start, end = map(int, args.port_range.split('-'))
            port_range = list(range(start, end + 1))
        else:
            port_range = list(map(int, args.port_range.split(',')))

        # Port scanning
        open_ports = scan_ports(args.target, port_range, timeout=1, verbose=True)
        if open_ports:
            service_info = detect_service(args.target, open_ports)

        # AI integration
        if args.ai_mode:
            print("\nPreparing data for AI analysis...")
          

        # Debug information
        print("Target Host:", args.target)
        print("Port Range:", args.port_range)
        print("AI Mode Enabled:", args.ai_mode)

    except Exception as e:
        print(f"Error occurred: {e}")
        exit(1)

if __name__ == "__main__":
    main()


#FORMAT OF THE COMMAND TO RUN THE SCRIPT
#python Index.py -t tailwindcss.com -p 20-80 --ai-mode  