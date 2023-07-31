import sqlite3
import random as rnd

""" Klasa koja ima niz statičkih metoda koje se mogu pozvati bez instanciranja klase za rad s bazom"""


class SQLManager:
    def __init__(self):
        pass

    # Kako bi mogao pozvati metodu bez inicijalizacije klase u objekt
    @classmethod
    def login_check(self, database, login, password):
        """
        database - iz koje se vuku podaci \n
        return 0 -> rezultata nema u bazi empty rec \n
        return 1 -> sve je ok i login i pass i postoje u bazi \n
        """
        con = sqlite3.connect(database=database)
        crs = con.cursor()

        sql_expression = f"SELECT * FROM USERS WHERE LOGIN = '{login}'"

        result = crs.execute(sql_expression).fetchone()

        con.close()

        """test dali korisnik postoji u bazi odnosno dali je varijabla prazna"""
        if not result:
            return 0

        """Ako varijabla nije prazna"""
        if result:
            if password == str(result[4]) and login == str(result[3]):
                return 1

    @classmethod
    def get_user_info(self, database, login):
        """
        database - iz koje se vuku podaci \n
        login -> login za korisnika
        return 0 -> rezultata nema u bazi empty rec \n
        return Ime, Prezime
        """
        con = sqlite3.connect(database=database)
        crs = con.cursor()

        sql_expression = f"SELECT NAME, SURNAME FROM USERS WHERE LOGIN = '{login}'"

        result = crs.execute(sql_expression).fetchone()

        con.close()

        """test dali korisnik postoji u bazi odnosno dali je varijabla prazna"""
        if not result:
            return 0

        """Ako varijabla nije prazna vrati ime i prezime"""
        if result:
            return result[0], result[1]

    @classmethod
    def add_new_user(self, database, name, surname, login, password):
        """
        database -> str: baza podatakak
        name -> str: name novog korisnika
        surnamr -> str: prezime
        login -> str: login
        password -> str password
        return 0 -> korisnik postoji
        return 1 -> korisnik je dodan
        """
        con = sqlite3.connect(database=database)
        crs = con.cursor()
        sql_expression = f"SELECT COUNT(LOGIN) FROM USERS WHERE LOGIN = '{login}'"

        result = crs.execute(sql_expression).fetchone()

        # ako login vec postoji
        if result[0]:
            con.close()
            return 0

        if not result[0]:

            last_id = crs.execute(f"SELECT MAX(ID) FROM USERS").fetchall()

            # prvi korisnik u bazi
            if last_id[0][0] == None:
                sql_str = f"""
                            INSERT INTO USERS
                            VALUES(1, \'{name}\', \'{surname}\', \'{login}\', \'{password}\')
                            """
            else:
                sql_str = f"""
                            INSERT INTO USERS
                            VALUES({last_id[0][0] + 1}, \'{name}\', \'{surname}\', \'{login}\', \'{password}\')
                            """

            crs.execute(sql_str)
            con.commit()
            con.close()
            return 1

    @classmethod
    def del_at_ID_index(self, database, id_index, table_name):
        """
        Args:
            database (string): Ime Baze
            id_index (int): ID broj
            table_name (string): ime tablice u bazi "database"
        """
        self.conn = sqlite3.connect(database=database)

        sql_string = f""" DELETE FROM {table_name}
                        WHERE ID = \'{id_index}\' """

        self.cur = self.conn.cursor()

        self.cur.execute(sql_string)

        self.conn.commit()
        self.conn.close()

    @classmethod
    def get_user_items(self, login, database):
        """Vraća podatke za korisnika

        Args:
            login (str): Login korisnika
            database (str): Ime baze

        Returns:
            _type_: _description_
        """
        self.conn = sqlite3.connect(database=database)

        sql_string = f"""SELECT PLANT_NAME, DATE, IMAGE_NAME, THUMB_NAME, RND_TEMP, RND_HUM, RND_PH, RND_LUM, PLANTS.ID
                        FROM PLANTS
                        INNER JOIN USERS ON PLANTS.fk_USER_ID = USERS.ID
                        WHERE USERS.LOGIN = \'{login}\' """

        self.cur = self.conn.cursor()

        result = self.cur.execute(sql_string).fetchall()

        self.conn.close()

        return result

    @classmethod
    def execute_string(
        self, database, sql_str, headers=False, inserting=False, deleting=False
    ):
        """Izvršava poslani SQL upit u obliku stringa

        Args:
            database (str): baza
            sql_str (str): SQL upit
            headers (bool, optional): Dali želimo i Headere . Defaults to False.
            inserting (bool, optional): Dali čitamo iz baze ili dodajemo. Defaults to False.
            deleting (bool, optional): dali brišemo iz baze. Defaults to False.

        Returns:
            _type_: _description_
        """

        self.conn = sqlite3.connect(database=database)
        self.cur = self.conn.cursor()

        if inserting:
            self.cur.execute(sql_str)
            self.conn.commit()
            self.conn.close()
            return 0

        if deleting:
            self.cur.execute(sql_str)
            self.conn.commit()
            self.conn.close()
            return 0

        if headers:
            result = self.cur.execute(sql_str).fetchall()
            names = list(map(lambda x: x[0], self.cur.description))
        else:
            result = self.cur.execute(sql_str).fetchall()

        self.conn.commit()
        self.conn.close()

        if headers:
            return result, names
        else:
            return result

    @classmethod
    def delete_item(
        self,
        login,
        item_name,
        database,
    ) -> None:
        """
        login -> user login, vlasnik biljke, str
        item_name -> naziv biljke koja se briše, str
        database -> ime baze koja se briše, str
        """
        self.conn = sqlite3.connect(database=database)

        login_ID_Str = f"SELECT ID FROM USERS WHERE LOGIN = '{login}'"

        self.cur = self.conn.cursor()

        user_id = self.cur.execute(login_ID_Str).fetchone()

        sql_string = f"DELETE FROM PLANTS WHERE PLANT_NAME = '{item_name}' AND fk_USER_ID = {user_id[0]}"

        user_id = self.cur.execute(sql_string)

        self.conn.commit()
        self.conn.close()

    @classmethod
    def add_new_item(
        self, login, plant_name, date_of_planting, full_image, thumb_image, database
    ) -> None:
        """Dodaje novu biljku za korisnika u tabelu PLANTS

        Args:
            login (string): login korisnika
            plant_name (string): Ime biljke
            date_of_planting (string): Datum adnje "YYYY-MM-DD" format
            full_image (string): Cijela Slika
            thumb_image (string): Mala Slika
            database (string): Ime Baze
        """
        self.conn = sqlite3.connect(database=database)

        self.cur = self.conn.cursor()

        login_ID_sql = f"SELECT ID FROM USERS WHERE LOGIN = '{login}'"

        user_id = self.cur.execute(login_ID_sql).fetchone()

        last_plant_id_sql = f"""SELECT MAX(ID) FROM PLANTS"""

        plant_last_id = self.cur.execute(last_plant_id_sql).fetchone()

        # random za temperaturu
        temp_rnd = rnd.randrange(90, 110) / 100

        # random za vlažnost
        hum_rnd = rnd.randrange(80, 120) / 100

        # random za pH
        pH_rnd = rnd.randrange(95, 105) / 100

        # random za lux
        lux_rnd = rnd.randrange(95, 105) / 100

        if plant_last_id[0] == None:
            ret_val = 1
            insert_sql = f""" INSERT INTO PLANTS
                VALUES(1,{user_id[0]},\'{plant_name}\',\'{date_of_planting}\', \'{full_image}\',\'{thumb_image}\',{temp_rnd}, {hum_rnd}, {pH_rnd},{lux_rnd}, -35,35, 10,90,3,8)"""
        else:
            insert_sql = f""" INSERT INTO PLANTS
                VALUES({plant_last_id[0]+1},{user_id[0]},\'{plant_name}\',\'{date_of_planting}\', \'{full_image}\',\'{thumb_image}\',{temp_rnd}, {hum_rnd}, {pH_rnd},{lux_rnd},-35,35, 10,90,3,8)"""
            ret_val = plant_last_id[0] + 1

        self.conn.execute(insert_sql)

        self.conn.commit()

        self.conn.close()
        return ret_val

    @classmethod
    def get_sensors_now(self, database: str, date_time_now: str):
        """Dohvaćanje podataka senzora koristeći trenutno vrijeme

        Args:
            database (str): Ime baze
            date_time_now (str): Vrijeme u obliku Y-M-S HH:MM:SS

        Returns:
            list: rezultati SQL upita
        """

        self.conn = sqlite3.connect(database=database)

        self.cur = self.conn.cursor()

        sql_str = f"""SELECT DATE_TIME, SENSOR1_TEMP, SENSOR2_HUM, SENSOR3_PH, SENSOR4_LUM
        FROM SENSORS
        WHERE DATE_TIME >= \'{date_time_now}\'"""

        result = self.cur.execute(sql_str).fetchone()

        self.conn.close()
        return result

    @classmethod
    def execute_edit(self, database, sql_str):
        """Izvršavanje bilokojeg sql upita

        Args:
            database (string): baza
            sql_str (string): upit bazi
        """

        self.conn = sqlite3.connect(database=database)

        self.cur = self.conn.cursor()
        self.cur.execute(sql_str)

        self.conn.commit()
        self.conn.close()
