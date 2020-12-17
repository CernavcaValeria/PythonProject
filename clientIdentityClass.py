
class ClientIdentity:
    def __init__(self,sockCl,nameCl,preferenceCl):
        self.sockCl = sockCl
        self.name = nameCl.upper()
        self.preference = preferenceCl
        self.score = []