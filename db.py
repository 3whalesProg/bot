import psycopg2
from config import host,user,password,db_name
from datetime import date
try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         "SELECT version()"
    #     )
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """CREATE TABLE users(
    #         id serial PRIMARY KEY,
    #         first_name varchar(50) NOT NULL,
    #         nick_name varchar(50) NOT NULL);"""
    #     )
    def addNewUser():
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO users (first_name, nick_name) VALUES
                ('oleg', 'foreman');"""
            )
            print("[INFO] Data was succefully inserted")
            return

    def regRequest(id, data):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO unwatched_regs (tg_id, firstName, secondName, role, phone, password, email) VALUES
                ({id}, '{data['first_name']}', '{data['second_name']}', '{data['role']}', '{data['phone']}', '{data['password']}', '{data['mail']}');"""
            )
            print("[INFO] New register request in base")
            return

    def register(data):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO users (id, first_name, second_name, role, phone, mail) VALUES
                ('{int(data['id'])}', '{data['first_name']}', '{data['second_name']}', '{data['role']}', '{data['phone']}', '{data['mail']}');"""
            )
            print("[INFO] New register request in base")

    def checkRegRequest():
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM unwatched_reg"""
            )
            return cursor.fetchall()

    def isAuth(id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT id FROM users WHERE tg_id = {id}"""
            )
            if(cursor.fetchone() == None):
                return False
            else: return True

    def checkRole(id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT role FROM users WHERE tg_id = {id}"""
            )
            return cursor.fetchone()[0]

    def userInfo(id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM users WHERE tg_id = {id}"""
            )
            return cursor.fetchall()

    def findRole(role):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT tgId FROM users WHERE role = '{role}'"""
            )
            return cursor.fetchall()
    def checkObj():
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM constructions"""
            )
            return cursor.fetchall()

    def checkObjForeman(id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM constructions WHERE foreman_id = {id}"""
            )
            return cursor.fetchall()

    def checkApplications(construction_id):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""SELECT * FROM applications WHERE construction_id = {construction_id} AND active"""
            )
            return cursor.fetchall()

    def checkApplicationsByForemanId(foreman_id):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""SELECT id FROM constructions WHERE foreman_id = {foreman_id}"""
            )
            return checkApplications(cursor.fetchone()[0])
    def constByForeman(foreman_id):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""SELECT id FROM constructions WHERE foreman_id = {foreman_id}"""
            )
            return cursor.fetchone()[0]

    def makeNewApp(foreman_id):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""INSERT INTO applications (construction_id) VALUES
                ({constByForeman(foreman_id)});"""

            )


    def checkItems(app_id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""SELECT * FROM application_items WHERE app_id = {app_id} AND active"""
            )
            return cursor.fetchall()
    def addItem(title, quantity, app_id):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""INSERT INTO application_items (title, quantity,app_id) VALUES
                ('{title}', '{quantity}',{app_id});"""
            )

    def updateLastItem(title, app_id):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""UPDATE applications SET last_item = '{title}' WHERE id = {app_id}"""
            )

    def updateTg(id, tg):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""UPDATE users SET tg_id = {tg} WHERE id = {id}"""
            )

    def itemStatusTreat(itemId):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""UPDATE application_items SET status = 'В обработке' WHERE id = {itemId}"""
            )
            return
    def itemStatusOrder(itemId):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""UPDATE application_items SET status = 'Заказано' WHERE id = {itemId}"""
            )
            return
    def itemStatusDone(itemId):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""UPDATE application_items SET status = 'Выполнено' WHERE id = {itemId}"""
            )
            return

    def findItem(itemId):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""SELECT * FROM application_items WHERE id = {itemId} AND active"""
            )
            return cursor.fetchone()
    def ItemDelete(itemId):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""UPDATE application_items SET active = false WHERE id = {itemId}"""
            )
            return
    def appDelete(appId):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""UPDATE applications SET active = false WHERE id = {appId}"""
            )
            return
    def findForeman(id):
        with connection.cursor()as cursor:
            cursor.execute(
                f"""SELECT firstName FROM users_info WHERE id = {id}"""
            )
            return cursor.fetchone()[0]

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
# finally:
#     if connection:
#         connection.close()
#         print("[INFO] PosgtgreSQL connection closed")