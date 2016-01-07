
class HackyMod:
    def __init__(self, users=[], simpaEmail=None, moderatorEmail=None,
                moderatorPassword=None):
        self.users = users
        self.simpaEmail = simpaEmail
        self.moderatorEmail = moderatorEmail
        self.moderatorPassword = moderatorPassword

    def moderate(self):
        print 'moderating'

