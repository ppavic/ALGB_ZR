from SqlLiteUtils import SQLManager



# str = """
#     DELETE FROM USERS
# """

str = """
    INSERT INTO USERS 
    VALUES(1, "admin", "admin", "admin", "123")
"""


SQLManager.execute_string("DB.sqlite", str, headers=False, deleting=True)
