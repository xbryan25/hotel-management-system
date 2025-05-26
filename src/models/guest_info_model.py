

class GuestInfoModel:
    def __init__(self, guest_id, name, gender, home_address, email_address, phone_number, birth_date, government_id,
                 last_visit_date, total_visit_count, total_amount_due):

        self.guest_id = guest_id
        self.name = name
        self.gender = gender
        self.home_address = home_address
        self.email_address = email_address
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.government_id = government_id
        self.last_visit_date = last_visit_date
        self.total_visit_count = total_visit_count
        self.total_amount_due = total_amount_due

        if not self.last_visit_date:
            self.last_visit_date = "-"

    def to_dict(self):
        return {
            "guest_id": self.guest_id,
            "name": self.name,
            "gender": self.gender,
            "home_address": self.home_address,
            "email_address": self.email_address,
            "phone_number": self.phone_number,
            "birth_date": self.birth_date,
            "government_id": self.government_id,
            "last_visit_date": self.last_visit_date,
            "total_visit_count": self.total_visit_count,
            "total_amount_due": self.total_amount_due
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            guest_id=data.get("guest_id"),
            name=data.get("name"),
            sex=data.get("sex"),
            home_address=data.get("home_address"),
            email_address=data.get("email_address"),
            phone_number=data.get("phone_number"),
            birth_date=data.get("birth_date"),
            government_id=data.get("government_id"),
            last_visit_date=data.get("last_visit_date"),
            total_visit_count=data.get("total_visit_count"),
            total_amount_due=data.get("total_amount_due")
        )

    @classmethod
    def from_list(cls, data):
        return cls(
            guest_id=data[0],
            name=data[1],
            gender=data[2],
            home_address=data[3],
            email_address=data[4],
            phone_number=data[5],
            birth_date=data[6],
            government_id=data[7],
            last_visit_date=data[8],
            total_visit_count=data[9],
            total_amount_due=data[10]
        )
