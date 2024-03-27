import sqlite3
from _apps.crypto_bot.variables import db_path, user_table_name, user_table_create

def init_db():
    return sqlite3.connect(db_path)

def create_table_users() -> bool:
    return execute_query(user_table_create)

def execute_query(query) -> bool:
    con = init_db()
    with con:
        cur = con.cursor()
        try:
            cur.execute(query)
            return True
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

def update_db(id:int, data:dict, table:str, **conditions):
    query = f"UPDATE {table} SET {compose_update_data(data)}"
    if conditions:
        query += f" WHERE {compose_conditions_dict(conditions)}"
    if execute_query(query):
        conditions = compose_conditions_dict(conditions)
        return select_db(table=table, fields=None, condition=conditions)
    return False

def compose_update_data(data: dict):
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

def select_db():
    def select_from(self, table, fields, condition:str):
        fields = ', '.join(fields) if fields else '*'
        query = f"SELECT {fields} FROM {table} WHERE {condition}"
        responses = self.execute_query(query, select=True)
        return self.get_dict(responses, fields)


