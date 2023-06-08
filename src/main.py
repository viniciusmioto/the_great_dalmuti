import sys
import network as net

CONFIG_FILE = 'config.txt'

# Check if the current machine number is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide the current machine number as a command-line argument.")
    sys.exit(1)

# Get the current machine number from the command-line argument
try:
    curr_machine_number = int(sys.argv[1])
except ValueError:
    print("Invalid machine number. Please provide an integer.")
    sys.exit(1)

# Extract current machine information from config.txt
curr_machine = net.get_current_machine(CONFIG_FILE, curr_machine_number)

# Extract next machine information from config.txt
next_machine = net.get_next_machine(CONFIG_FILE, curr_machine_number)

if next_machine is None:
    print(f"Machine {curr_machine_number} is not defined in the configuration.")
    sys.exit(1)


print(f"Current machine: {curr_machine}")
print(f"Next machine: {next_machine}")