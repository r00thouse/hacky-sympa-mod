
class HackyMod:
    def __init__(self, users=[], sympaEmail=None, moderatorEmail=None,
                moderatorPassword=None):
        self.users = users
        self.sympaEmail = sympaEmail
        self.moderatorEmail = moderatorEmail
        self.moderatorPassword = moderatorPassword

    def moderate(self):
        print 'moderating'

