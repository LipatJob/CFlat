from Lib.Token import *
from typing import List

list_tokens = []
char_count = 1
total_char_count = 1
line_count = 0
cur_token = None
cur_ch = None
buffer = []
cur_token_type = -1
cur_f = None

class LexicalAnalyzer:
    def run(self, fileName: str) -> List[Token]:
        global list_tokens
        global char_count
        global total_char_count
        global line_count
        global cur_token
        global cur_ch
        global buffer
        global cur_token_type
        global cur_f
        
        cur_f = open("kk.txt") #cur_f = open(fileName)
        cur_ch = cur_f.read(1) 

        while True:
            token = self.next()
            if token != None:
                obj = Token(cur_token_type, token, line_count,char_count)
                list_tokens.append(obj)
            else:
                break  
        return list_tokens
        
    def buffer_to_string(self, buffer):
        return ''.join(buffer)

    def next(self):
        global list_tokens
        global char_count
        global total_char_count
        global line_count
        global cur_token
        global cur_ch
        global buffer
        global cur_token_type
        global cur_f

        buffer.clear()
        
        while cur_ch and cur_ch.isspace():
            if cur_ch=="\n":
                line_count+=1 
                char_count=0
                total_char_count=0
            cur_ch = cur_f.read(1)
            total_char_count+=1 #counted pati space

        if not cur_ch:# EOF
            cur_token_type = "TOKEN_EOF"
            cur_token = None
            return cur_token        

        if cur_ch.isalpha(): # identifiers & keywords
            char_count = total_char_count
            buffer.append(cur_ch)
            cur_ch = cur_f.read(1)
            total_char_count+=1
            while cur_ch and (cur_ch.isalnum()): 
                buffer.append(cur_ch)
                cur_ch = cur_f.read(1)
                total_char_count+=1
            cur_token = self.buffer_to_string(buffer)
            if cur_token in Reserved.reserved:
                cur_token_type= Reserved.reserved.get(cur_token)
            else:
                cur_token_type = "TOKEN_IDENTIFIER"
            return cur_token
        
        elif cur_ch.isnumeric(): # int literal note: WALA NEGATIVE
            char_count=total_char_count
            buffer.append(cur_ch)
            cur_ch = cur_f.read(1)
            total_char_count+=1
            while cur_ch and cur_ch.isnumeric():
                buffer.append(cur_ch)
                cur_ch = cur_f.read(1)
                total_char_count+=1
            cur_token_type = "TOKEN_NUM int literal"
            cur_token = self.buffer_to_string(buffer)
            return cur_token

        elif cur_ch and cur_ch == '\"': # string literal
            char_count=total_char_count
            buffer.append(cur_ch)
            cur_ch = cur_f.read(1)
            total_char_count +=1
            while cur_ch and cur_ch != '\"':
                buffer.append(cur_ch)
                if cur_ch == '\\':                      ##### idk this if-part
                    buffer.append(cur_f.read(1))        ##### secretly eat next \t then act as if nothing happened
                cur_ch = cur_f.read(1)
                total_char_count +=1
            buffer.append(cur_ch)
            cur_ch = cur_f.read(1)
            total_char_count +=1
            cur_token_type = "TOKEN_STRING string literal"
            cur_token = self.buffer_to_string(buffer)
            return cur_token
        
        elif cur_ch == '/': ##comments
            char_count = total_char_count
            buffer.append(cur_ch)
            cur_ch = cur_f.read(1)
            total_char_count+=1
            if cur_ch =='/': #single line comment
                while cur_ch and cur_ch!="\n":
                    buffer.append(cur_ch)
                    cur_ch = cur_f.read(1)
                    total_char_count+=1
                cur_token = self.buffer_to_string(buffer)
                cur_token_type = "single line comment"
                return cur_token
            elif cur_ch =='*':##multiline coment
                while True:
                    buffer.append(cur_ch)
                    cur_ch = cur_f.read(1)
                    total_char_count+=1
                    if cur_ch =="*":
                        buffer.append(cur_ch)
                        cur_ch = cur_f.read(1)
                        total_char_count+=1
                        if cur_ch =="/":
                            buffer.append(cur_ch)
                            cur_ch = cur_f.read(1)
                            total_char_count+=1
                            cur_token_type = "multi line comment"
                            cur_token = self.buffer_to_string(buffer)
                            return cur_token
            else:
                cur_token = self.buffer_to_string(buffer)
                cur_token_type = "symbols_arithmetic_operator"
                return cur_token
                    
        elif cur_ch == "=":
            char_count=total_char_count
            buffer.append(cur_ch)
            cur_ch = cur_f.read(1)
            total_char_count+=1
            if cur_ch =='=':
                buffer.append(cur_ch)
                cur_ch = cur_f.read(1)
                total_char_count+=1
                cur_token_type = "symbols_relational_operator"
                cur_token = self.buffer_to_string(buffer)
                return cur_token
            else:
                cur_token = self.buffer_to_string(buffer)
                cur_token_type = "symbols_assignment_operator"
                return cur_token
            
        elif cur_ch =="!":
            char_count=total_char_count
            buffer.append(cur_ch)
            cur_ch = cur_f.read(1)
            total_char_count+=1
            if cur_ch =='=':
                buffer.append(cur_ch)
                cur_ch = cur_f.read(1)
                total_char_count+=1
                cur_token_type = "symbols_relational_operator"
                cur_token = self.buffer_to_string(buffer)
                return cur_token
            ##################??????????????????
            else:
                cur_token_type = "TOKEN_OTHER...ERROR"
                cur_token = self.buffer_to_string(buffer)
                return cur_token
            
        elif cur_ch == '>' or cur_ch == '<':
            char_count=total_char_count
            buffer.append(cur_ch)
            cur_ch = cur_f.read(1)
            total_char_count+=1
            if cur_ch =='=':
                buffer.append(cur_ch)
                cur_ch = cur_f.read(1)
                total_char_count+=1
                cur_token_type = "symbols_relational_operator"
                cur_token = self.buffer_to_string(buffer)
                return cur_token
            cur_token = self.buffer_to_string(buffer)
            cur_token_type = "symbols_relational_operator"
            return cur_token

        elif cur_ch in Reserved.reserved:
            char_count=total_char_count
            cur_token=cur_ch
            cur_ch = cur_f.read(1)
            total_char_count +=1
            cur_token_type= Reserved.reserved.get(cur_token)
            return cur_token

        else:
            char_count=total_char_count
            buffer.append(cur_ch)
            cur_ch = cur_f.read(1)
            total_char_count+=1
            cur_token_type = "TOKEN_OTHER...ERROR"
            cur_token = self.buffer_to_string(buffer)
            return cur_token
