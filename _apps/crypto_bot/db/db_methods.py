import sqlite3
from _apps.crypto_bot.variables import db_path, user_table_name, user_table_create
from _apps.crypto_bot.variables import fields_user_table

def init_db():
    return sqlite3.connect(db_path)

def create_table_users() -> bool:
    return execute_query(user_table_create)

def execute_query(query, fetchall:bool=False) -> bool:
    con = init_db()
    with con:
        cur = con.cursor()
        try:
            cur.execute(query)
            return cur.fetchall() if fetchall else True
        except Exception as ex:
            print("EXECUTE_QUERY: ", ex)
            return False

def insert_db(data:dict, table:str=None) -> bool:
    table = table if table else user_table_name
    query = get_query(data, table)
    return True if execute_query(query) else False

def get_query(data:dict, table:str) -> str:
    fields = ", ".join(tuple(data.keys()))
    values = tuple(data.values()) if len(data.keys()) > 1 else tuple(data.values())[0]
    return f"INSERT INTO {table} ({fields}) VALUES {values};" if len(data.keys()) > 1 else f"INSERT INTO {table} ({fields}) VALUES ({tuple(data.values())[0]});"

def update_db(data:dict, table:str, **conditions) -> bool:
    query = f"UPDATE {table} SET {compose_update_data(data)}"
    if conditions:
        query += f" WHERE {compose_conditions_dict(conditions)}"
    if execute_query(query):
        # conditions = compose_conditions_dict(conditions)
        # return select_db(table=table, fields=None, condition=conditions)
        return True
    return False

def compose_update_data(data: dict) -> str:
    query = []
    for key in data:
        query.append(f"{key}={data[key]}") if type(data[key]) in [int, float] else query.append(f"{key}='{data[key]}'")
    return ", ".join(query)

def compose_conditions_dict(conditions:dict) -> str:
    queryList = []
    for key in conditions:
        queryList.append(f"{key}={conditions[key]}") if type(conditions[key]) in [int, tuple] else queryList.append(
            f"{key}='{conditions[key]}'")
    return " AND ".join(queryList)

def patch_db(id:int, data:dict):
    pass

def select_from(table, fields:list=None, condition:str=None):
    fields = ', '.join(fields) if fields else '*'
    query = f"SELECT {fields} FROM {table} WHERE {condition}" if condition else f"SELECT {fields} FROM {table}"
    responses = execute_query(query, fetchall=True)
    return get_dict(responses, fields)

def get_dict(responses, fields):
    responses_list = []
    if not fields or fields == "*":
        fields = fields_user_table

    for response in responses:
        response_dict = {}
        for i in range(0, len(fields)):
            response_dict[fields[i]] = response[i]
        responses_list.append(response_dict)
    return responses_list

