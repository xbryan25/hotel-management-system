

class PaidRoomQueries:
    def __init__(self, cursor):
        self.cursor = cursor

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
                (payment_id, payment_type, amount, transaction_date, guest_id, room_number) VALUES
                (%s, %s, %s, %s, %s, %s)"""

        latest_payment_id = self.get_latest_payment_id()

        new_payment_id = f"paid-{int(latest_payment_id[9:]) + 1:06}"

        values = (new_payment_id,
                  paid_room_information[0],
                  paid_room_information[1],
                  paid_room_information[2],
                  paid_room_information[3],
                  paid_room_information[4])

        self.cursor.execute(sql, values)
        self.db.commit()

    def update_paid_room(self, old_payment_id, paid_room_information):
        sql = """UPDATE paidrooms SET payment_id=%s, payment_type=%s, amount=%s, transaction_date=%s, guest_id=%s, room_number=%s
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
