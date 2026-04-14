def populate_dotenv_var_string(env_line:str, env_var:str):
    replace_prep = '="' + env_var + '"'
    env_line = env_line.replace("=\"\"", replace_prep)
    return env_line

def populate_dotenv_var_int(env_line:str, env_var:int):
    replace_prep = '=' + str(env_var)
    env_line = env_line.replace("=7443", replace_prep)
    return env_line

# Creates new .env file if it doesnt exist and adds new values to .env file
def modify_env(env_key, env_value, base_env=None):
    import os, shutil

    # Copies .env-template to .env before population if .env does not currently exist
    if os.path.isfile(base_env) == True and os.path.isfile(".env") == False:
        shutil.copy(base_env, ".env")
        with open(".env", "r") as file:
            data = file.readlines()
    
    # Loads .env to prep for population
    elif base_env != None:
        with open(".env", "r") as file:
            data = file.readlines()

    for i in range(len(data)):
        if env_key in data[i]:
            data[i] = populate_dotenv_var_string(data[i], env_value)
            break
            
        else:
            pass

    with open(".env", "w") as file:
        file.writelines(data)