from typing import List
from Lib.Token import Token

class Node:
    def __init__(self, token :'Token', parameters : List['Node']):
        self.token = token
        self.parameters = parameters