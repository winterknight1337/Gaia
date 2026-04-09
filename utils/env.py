def populate_dotenv_var_string(env_line:str, env_var:str):
    replace_prep = '="' + env_var + '"'
    env_line = env_line.replace("=\"\"", replace_prep)
    return env_line

def populate_dotenv_var_int(env_line:str, env_var:int):
    replace_prep = '=' + str(env_var)
    env_line = env_line.replace("=7443", replace_prep)
    return env_line