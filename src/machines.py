def get_machine_info(num):
    with open('config.txt', 'r') as file:
        lines = file.readlines()
    
    # Find the starting line of the machine configuration
    start_index = lines.index(f'MACHINE {num}\n')

    # Find the ending line of the machine configuration
    end_index = len(lines)
    for i in range(start_index + 1, len(lines)):
        if lines[i].startswith('MACHINE'):
            end_index = i
            break
    
    # Extract the relevant lines for the machine configuration
    config_lines = lines[start_index:end_index]

    # Parse the config lines and store the data in a dictionary
    config = {}
    config["NUMBER"] = num
    for line in config_lines:
        line = line.strip()
        if line.startswith(('ADDRESS', 'SEND_ADDRESS', 'CLASS')):
            key, value = line.split()
            config[key] = value
        elif line.startswith(('SEND_PORT', 'RECV_PORT')):
            key, value = line.split()
            config[key] = int(value)
    
    return config


def get_players_amout():
    with open('config.txt', 'r') as file:
        lines = file.readlines()
    return int(lines[0].strip().split()[1])