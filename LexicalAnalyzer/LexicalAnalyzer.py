from Lib.Token import *
from typing import List
from Lib.ErrorHandler import *

list_tokens = []
char_count = 1
total_char_count = 1
line_count = 1
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
        
        cur_f = open(fileName)
        cur_ch = cur_f.read(1) 

        while True:
            token = self.next()
            if token != None:
                obj = Token(cur_token_type, token, line_count,char_count)
                list_tokens.append(obj)
            else:
                break  
        cur_f.close()
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
        while True:
            buffer.clear()
        
            while cur_ch and cur_ch.isspace():
                if cur_ch=="\n":
                    line_count+=1 
                    char_count=0
                    total_char_count=0
                cur_ch = cur_f.read(1)
                total_char_count+=1 

            if not cur_ch:
                cur_token_type = TokenType.END_OF_FILE
                cur_token = None
                return cur_token        

            if cur_ch.isalpha():
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
                    cur_token_type = TokenType.IDENTIFIER
                return cur_token
            
            elif cur_ch.isnumeric(): 
                char_count=total_char_count
                buffer.append(cur_ch)
                cur_ch = cur_f.read(1)
                total_char_count+=1
                while cur_ch and cur_ch.isnumeric():
                    buffer.append(cur_ch)
                    cur_ch = cur_f.read(1)
                    total_char_count+=1
                cur_token_type = TokenType.INT_LITERAL
                cur_token = self.buffer_to_string(buffer)
                return cur_token

            elif cur_ch and cur_ch == '\"':
                char_count=total_char_count
                buffer.append(cur_ch)
                cur_ch = cur_f.read(1)
                total_char_count +=1
                while cur_ch and cur_ch != '\"':
                    buffer.append(cur_ch)
                    if cur_ch == '\\':                      
                        buffer.append(cur_f.read(1))        
                    cur_ch = cur_f.read(1)
                    total_char_count +=1
                buffer.append(cur_ch)
                cur_ch = cur_f.read(1)
                total_char_count +=1
                cur_token_type = TokenType.STRING_LITERAL
                cur_token = self.buffer_to_string(buffer)
                return cur_token
            
            elif cur_ch == '/': 
                char_count = total_char_count
                buffer.append(cur_ch)
                cur_ch = cur_f.read(1)
                total_char_count+=1
                if cur_ch =='/': 
                    while cur_ch and cur_ch!="\n":
                        buffer.append(cur_ch)
                        cur_ch = cur_f.read(1)
                        total_char_count+=1
                    cur_token = self.buffer_to_string(buffer)
                    continue
                elif cur_ch =='*':
                    while True:
                        buffer.append(cur_ch)
                        cur_ch = cur_f.read(1)
                        total_char_count+=1
                        if cur_ch=="\n":
                            line_count+=1
                        if cur_ch =="*":
                            buffer.append(cur_ch)
                            cur_ch = cur_f.read(1)
                            total_char_count+=1
                            if cur_ch =="/":
                                buffer.append(cur_ch)
                                cur_ch = cur_f.read(1)
                                total_char_count+=1
                                break
                    continue
                else:
                    cur_token = self.buffer_to_string(buffer)
                    cur_token_type = TokenType.SLASH
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
                    cur_token_type = TokenType.DOUBLE_EQUAL
                    cur_token = self.buffer_to_string(buffer)
                    return cur_token
                else:
                    cur_token = self.buffer_to_string(buffer)
                    cur_token_type = TokenType.EQUAL
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
                    cur_token_type = TokenType.NOT_EQUAL
                    cur_token = self.buffer_to_string(buffer)
                    return cur_token
                else:
                    raise_token_error(line_count,char_count)
                
            elif cur_ch == '>' or cur_ch == '<':
                token = cur_ch
                char_count=total_char_count
                buffer.append(cur_ch)
                cur_ch = cur_f.read(1)
                total_char_count+=1
                if cur_ch =='=':
                    token+=cur_ch
                    buffer.append(cur_ch)
                    cur_ch = cur_f.read(1)
                    total_char_count+=1
                    if token == ">=":
                        cur_token_type = TokenType.MORE_EQUAL
                    else:
                        cur_token_type = TokenType.LESS_EQUAL            
                    cur_token = self.buffer_to_string(buffer)
                    return cur_token
                cur_token = self.buffer_to_string(buffer)
                if token == ">":
                    cur_token_type = TokenType.MORE
                else:
                    cur_token_type = TokenType.LESS
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
                raise_token_error(line_count,char_count)