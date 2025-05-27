

class PaidRoomQueries:
    def __init__(self, db, cursor):
        self.db = db
        self.cursor = cursor

    def get_count_of_revenue(self, view_type='Past 7 Days'):

        if view_type == 'Past 7 Days':
            sql = """SELECT DATE(transaction_date) AS payment_day, SUM(amount) AS total_amount FROM paidrooms
                        WHERE transaction_date >= CURDATE() - INTERVAL 6 DAY
                        GROUP BY DATE(transaction_date)
                        ORDER BY payment_day ASC;"""

        elif view_type == 'Past 4 Weeks':
            sql = """SELECT YEARWEEK(transaction_date, 1) AS year_week, SUM(amount) AS total_amount 
                        FROM paidrooms
                        WHERE transaction_date >= CURDATE() - INTERVAL 4 WEEK
                        GROUP BY year_week
                        ORDER BY year_week ASC;"""

        else:
            sql = """SELECT DATE_FORMAT(transaction_date, '%Y-%m') AS transaction_month, SUM(amount) AS total_amount
                        FROM paidrooms
                        WHERE transaction_date >= CURDATE() - INTERVAL 6 MONTH 
                        GROUP BY transaction_month
                        ORDER BY transaction_month;"""

        self.cursor.execute(sql)
        result = self.cursor.fetchall()

        return result


    def get_latest_payment_id(self):

        self.cursor.execute("""SELECT payment_id FROM paidrooms
            ORDER BY CAST(SUBSTRING(payment_id, 6) AS UNSIGNED) DESC LIMIT 1;
        """)

        result = self.cursor.fetchone()

        if not result:
            return "paid-000000"
        else:
            return result[0]

    def add_paid_room(self, paid_room_information):
        sql = """INSERT INTO paidrooms
                (payment_id, payment_type, amount, transaction_date, guest_id, room_id) VALUES
                (%s, %s, %s, %s, %s, %s)"""

        latest_payment_id = self.get_latest_payment_id()

        new_payment_id = f"paid-{int(latest_payment_id[9:]) + 1:06}"

        values = (new_payment_id,
                  paid_room_information['payment_type'],
                  paid_room_information['amount'],
                  paid_room_information['transaction_date'],
                  paid_room_information['guest_id'],
                  paid_room_information['room_id'])

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_paid_room(self, old_payment_id, paid_room_information):
        sql = """UPDATE paidrooms SET payment_id=%s, payment_type=%s, amount=%s, transaction_date=%s, guest_id=%s, room_id=%s
        WHERE payment_id=%s;"""

        values = (paid_room_information[0],
                  paid_room_information[1],
                  paid_room_information[2],
                  paid_room_information[3],
                  paid_room_information[4],
                  paid_room_information[5],
                  old_payment_id)

        self.cursor.execute(sql, values)
        self.db.commit()

    def delete_paid_room(self, identifier):

        sql = "DELETE FROM paidrooms WHERE payment_id=%s"
        values = (identifier.strip(),)

        self.cursor.execute(sql, values)
        self.db.commit()
