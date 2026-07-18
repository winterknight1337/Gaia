def update_env(env_key: str, env_value: str):
    import dotenv, os, shutil
    if os.path.isfile(".env-template") == True and os.path.isfile(".env") == False:
        shutil.copy(".env-template", ".env")
    
    # This will just override whatever is in that key value pair
    dotenv_file = dotenv.find_dotenv()
    dotenv.set_key(dotenv_path=dotenv_file, key_to_set=env_key, value_to_set=env_value)