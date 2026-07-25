def update_env(env_key: str, env_value: str):
    import dotenv
    
    # This will just override whatever is in that key value pair
    dotenv_file = dotenv.find_dotenv()
    dotenv.set_key(dotenv_path=dotenv_file, key_to_set=env_key, value_to_set=str(env_value))