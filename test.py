def update_file_value(filename, variable_name, new_value):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    with open(filename, 'w') as file:
        for line in lines:
            if line.startswith(variable_name + '='):
                line = f"{variable_name}={new_value}\n"
            file.write(line)



def read_file_value(filename, variable_name):
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith(variable_name + '='):
                return line.split('=')[1].strip()
    return None



update_file_value('global_round.txt','round','23')

