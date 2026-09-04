import getpass
from argparse import Namespace

# Update env file
def update_env(env_key: str, env_value: str):
    import dotenv
    
    # This will just override whatever is in that key value pair
    dotenv_file = dotenv.find_dotenv()
    dotenv.set_key(dotenv_path=dotenv_file, key_to_set=env_key, value_to_set=str(env_value))

# Logic here is to take the input from the CLI as preference, if not, then fall back to .env value.
def resolve_env_inputs(arg_parameter:Namespace, env_key:str, env):
    param = None
    if env[env_key] != "":
        param = env[env_key]

    if arg_parameter != None or param != None:
        if type(arg_parameter) == str:
            if arg_parameter != "":
                param = arg_parameter
                update_env(env_key=env_key, env_value=param)
            
        elif type(arg_parameter) == bool:
            if arg_parameter != False:
                param = arg_parameter
                update_env(env_key=env_key, env_value=param)

        elif type(arg_parameter) == int:
            param = arg_parameter
            update_env(env_key=env_key, env_value=param)

        elif param != None:
            pass
        
        else:
            param = None
        
    else:
        param = None

    return param

# Since API keys are all bools, either we update it, pull it from env, or pass back none to error out
def resolve_env_api_key(arg_parameter:Namespace, env_key:str, getpass_text:str, env):
    if arg_parameter == True:
        api_key = getpass.getpass(getpass_text)
        update_env(env_key=env_key, env_value=api_key)

    elif env[env_key] != '':
        api_key = env[env_key]
    
    else:
        api_key = None

    return api_key