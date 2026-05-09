import sqlite3
import os

class ConnectDatabase:
    def __init__(self):
        self._database = os.path.join(os.path.dirname(__file__), "database.db")
        self.con = None
        self.cursor = None

    def connect_db(self):
        # Establish a database connection to SQLite
        self.con = sqlite3.connect(self._database)
        # To get rows as dictionaries similar to MySQL's dictionary=True
        self.con.row_factory = sqlite3.Row
        self.cursor = self.con.cursor()

    def add_info(self, Employe_id, first_name, last_name, state, city, email_address):
        self.connect_db()

        sql = """
            INSERT INTO service_requests (employe_id, first_name, last_name, state, city, email_address) 
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            self.cursor.execute(sql, (Employe_id, first_name, last_name, state, city, email_address))
            self.con.commit()
            return None # Success
        except Exception as E:
            self.con.rollback()
            return str(E)
        finally:
            self.con.close()

    def update_info(self, Employe_id, first_name, last_name, state, city, email_address):
        self.connect_db()

        sql = """
            UPDATE service_requests
            SET first_name=?, last_name=?, state=?, city=?, email_address=?
            WHERE employe_id=?
        """
        try:
            self.cursor.execute(sql, (first_name, last_name, state, city, email_address, Employe_id))
            self.con.commit()
            return None # Success
        except Exception as E:
            self.con.rollback()
            return str(E)
        finally:
            self.con.close()

    def delete_info(self, EmployeId):
        self.connect_db()

        sql = "DELETE FROM service_requests WHERE employe_id=?;"
        try:
            self.cursor.execute(sql, (EmployeId,))
            self.con.commit()
            return None
        except Exception as E:
            self.con.rollback()
            return str(E)
        finally:
            self.con.close()

    def search_info(self, Employe_id=None, first_name=None, last_name=None, state=None, city=None, email_address=None):
        self.connect_db()

        sql = "SELECT * FROM service_requests WHERE 1=1"
        params = []
        
        if Employe_id:
            sql += " AND employe_id LIKE ?"
            params.append(f"%{Employe_id}%")
        else:
            if first_name:
                sql += " AND first_name LIKE ?"
                params.append(f"%{first_name}%")
            if last_name:
                sql += " AND last_name LIKE ?"
                params.append(f"%{last_name}%")
            if state:
                sql += " AND state=?"
                params.append(state)
            if city:
                sql += " AND city=?"
                params.append(city)
            if email_address:
                sql += " AND email_address LIKE ?"
                params.append(f"%{email_address}%")

        try:
            self.cursor.execute(sql, params)
            # Fetch all rows and convert sqlite3.Row objects to dictionaries
            result = [dict(row) for row in self.cursor.fetchall()]
            return result
        except Exception as E:
            return str(E)
        finally:
            self.con.close()

    def get_all_states(self):
        self.connect_db()
        sql = "SELECT state FROM service_requests GROUP BY state;"
        try:
            self.cursor.execute(sql)
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as E:
            return []
        finally:
            self.con.close()

    def get_all_cities(self):
        self.connect_db()
        sql = "SELECT city FROM service_requests GROUP BY city;"
        try:
            self.cursor.execute(sql)
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as E:
            return []
        finally:
            self.con.close()