class Match:
    def __init__(self, chatid, name, age, work, study, home, gender, bio, distance, passions):
        self.chatid = chatid
        
        self.name = name
        self.age = age
        self.work = work
        self.study = study
        self.home = home
        self.gender = gender
        self.bio = bio
        self.distance = distance
        self.passions = passions

    def get_chat_id(self):
        return self.chatid
    
    def get_name(self):
        return self.name

    def get_age(self):
        return self.age

    def get_work(self):
        return self.work

    def get_study(self):
        return self.study

    def get_home(self):
        return self.home

    def get_gender(self):
        return self.gender

    def get_bio(self):
        return self.bio

    def get_distance(self):
        return self.distance
    
    def get_passions(self):
        return self.passions

    def get_dictionary(self):
        data = {
            "chatid": self.get_chat_id(),
            "name": self.get_name(),
            "age": self.get_age(),
            "work": self.get_work(),
            "study": self.get_study(),
            "home": self.get_home(),
            "gender": self.get_gender(),
            "bio": self.get_bio(),
            "distance": self.get_distance(),
            "passions": self.get_passions(),
        }
        return data