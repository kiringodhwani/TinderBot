class Match:
    def __init__(self, chatid, name, age, work, study, home, gender, bio, looking_for, distance, passions):
        """
        A class to represent a Tinder match.
        
        Attributes
        ----------
            chatid : str
                An identifier for the match that Tinder stores (e.g., '666553a20486650100ce0e3966663c8280f72701007cd624')
            name : str
                The name of the match (e.g., 'Amy')
            age : int
                The age of the match (e.g, 20)
            work : str
                The type of work that the match does (e.g., 'Student')
            study : str
                The school that the match studies at (e.g., 'Boston University')
            home : str
                Location of home (e.g., 'Newton')
            gender : str
                The gender of the match (e.g., 'Woman')
            bio : str
                The bio of the match (e.g., 'if you like pineapple on your pizza disrespectfully swipe left')
            looking_for : str
                The relationship preference of the match (e.g., 'Looking for\nShort-term, open to long')
            distance : int
                The distance in miles between the user and the match (e.g, 3)
            passions : list
                The match's passions (e.g, ['Instagram', 'Language Exchange', 'Slam Poetry', 'Aquarium', 'Theater'])
        
        Methods
        -------
        Each attribute has a method to retrieve it (e.g., get_name()).
        
        get_dictionary():
            Returns the Tinder match and all of its attributes in dictionary form.
        """
        self.chatid = chatid
        
        self.name = name
        self.age = age
        self.work = work
        self.study = study
        self.home = home
        self.gender = gender
        self.bio = bio
        self.looking_for = looking_for
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
    
    def get_looking_for(self):
        return self.looking_for

    def get_distance(self):
        return self.distance
    
    def get_passions(self):
        return self.passions

    def get_dictionary(self):
        """Returns the Tinder match and all of its attributes in dictionary form.
        
        Returns
        -------
            data : dict
                A dictionary containing the Tinder match and all of its attributes.
        """
        data = {
            "chatid": self.get_chat_id(),
            "name": self.get_name(),
            "age": self.get_age(),
            "work": self.get_work(),
            "study": self.get_study(),
            "home": self.get_home(),
            "gender": self.get_gender(),
            "bio": self.get_bio(),
            "looking_for": self.get_looking_for(),
            "distance": self.get_distance(),
            "passions": self.get_passions(),
        }
        return data