#importing all modules 
from Algo_one import Input_parse; 
from Algo_one import Input_Validation; 
from Algo_two.Port_Scanning import main as perform_port_scanning;


#added a custom ASCII art banner and color codes
print('''
  \033[31mSSSS\033[0m   \033[32mCCCC\033[0m   \033[33mAAAA\033[0m   \033[34mLLLL\033[0m   \033[35mPPPP\033[0m   \033[36mYYYY\033[0m   
 \033[31mS\033[0m     \033[31mS\033[0m \033[32mC\033[0m      \033[33mA\033[0m    \033[33mA\033[0m \033[34mL\033[0m      \033[35mP\033[0m   \033[35mP\033[0m   \033[36mY\033[0m     
 \033[31mS\033[0m       \033[32mC\033[0m      \033[33mA\033[0m    \033[33mA\033[0m \033[34mL\033[0m      \033[35mP\033[0m   \033[35mP\033[0m   \033[36mY\033[0m     
  \033[31mSSSS\033[0m  \033[32mC\033[0m      \033[33mAAAAAA\033[0m \033[34mL\033[0m      \033[35mPPPP\033[0m    \033[36mY\033[0m     
       \033[31mS\033[0m \033[32mC\033[0m      \033[33mA\033[0m    \033[33mA\033[0m \033[34mL\033[0m      \033[35mP\033[0m     \033[36mY\033[0m     
 \033[31mS\033[0m     \033[31mS\033[0m \033[32mC\033[0m      \033[33mA\033[0m    \033[33mA\033[0m \033[34mL\033[0m      \033[35mP\033[0m     \033[36mY\033[0m     
  \033[31mSSSS\033[0m   \033[32mCCCC\033[0m   \033[33mA\033[0m    \033[33mA\033[0m \033[34mLLLL\033[0m   \033[35mP\033[0m     \033[36mY\033[0m     
''')

#calling the main function
if __name__ == "__main__":
    args = Input_parse.parse_arguments() #parse the arguments and store them in the args variable


    # Validate inputs
    if not Input_Validation.validate_target(args.target):
        exit(1)

    if not Input_Validation.validate_port_range(args.port_range):
        exit(1)

    
 # Convert port_range to a list of integers
    if '-' in args.port_range:
        start, end = map(int, args.port_range.split('-'))
        port_range = list(range(start, end + 1))
    else:
        port_range = list(map(int, args.port_range.split(',')))
    
     # Perform port scanning
    open_ports = perform_port_scanning(args.target, port_range, timeout=1, verbose=True)

     # If AI mode is enabled, prepare data for analysis
    if args.ai_mode:
        print("\nPreparing data for AI analysis...")




    #Display parsed arguments for debugging
    print("Target Host:", args.target)
    print("Port Range:", args.port_range)
    print("AI Mode Enabled:", args.ai_mode)



#FORMAT OF THE COMMAND TO RUN THE SCRIPT
#python Index.py -t tailwindcss.com -p 20-80 --ai-mode  
