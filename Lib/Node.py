from Lib.Token import Token


class Node:
    def __init__(self, token :'Token', parameters : 'Node'):
        self.token = token
        self.parameters = parameters