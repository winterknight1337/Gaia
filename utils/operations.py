from mythic import mythic

async def get_operations(mythic_instance:mythic):
    operations = await mythic.get_operations(mythic=mythic_instance)
    return operations

async def create_operation(mythic_instance: mythic, operation_name: str):
    results = await mythic.create_operation(mythic=mythic_instance, operation_name=operation_name)
    print(results)
    return results

async def add_operator_to_operation(mythic_instance: mythic, operation_name: str, username: str):
    results = await mythic.add_operator_to_operation(mythic=mythic_instance, operation_name=operation_name, operator_username=username)
    return results

async def remove_operator_to_operation(mythic_instance: mythic, operation_name: str, username: str):
    results = await mythic.remove_operator_from_operation(mythic=mythic_instance, operation_name=operation_name, operator_username=username)
    return results