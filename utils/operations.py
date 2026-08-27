from mythic import mythic

async def create_operation(mythic_instance: mythic, operation_name: str):
    results = await mythic.create_operation(mythic=mythic_instance, operation_name=operation_name)
    return results

async def add_operator_to_operation(mythic_instance: mythic, operation_name: str, username: str):
    results = await mythic.add_operator_to_operation(mythic=mythic_instance, operation_name=operation_name, operator_username=username)
    return results

async def remove_operator_to_operation(mythic_instance: mythic, operation_name: str, username: str):
    results = await mythic.remove_operator_from_operation(mythic=mythic_instance, operation_name=operation_name, operator_username=username)
    return results

async def get_operations(mythic_instance: mythic):
    operation_names = []
    results = await mythic.get_operations(mythic=mythic_instance)
    for i in results:
        operation_names.append(i["name"])
    return operation_names

async def get_current_operation(mythic_instance: mythic):
    results = await mythic.get_me(mythic=mythic_instance)
    current_operation = results["meHook"]["current_operation"]
    return current_operation

async def add_discord_webhook(mythic_instance: mythic, operation_name:str, webhook_url: str):
    results = await mythic.update_operation(mythic=mythic_instance, operation_name=operation_name, webhook=webhook_url)

    return results