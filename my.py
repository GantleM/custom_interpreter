class My:
    def __init__(self, code):
        self.code = code
        self.env = {}
        self.instructions = self.read_code(self.code)
        self.reserved_words = ["IF", "THEN", "DO", "print", "END", "LIST", "ADD"]
        self.execute_code(self.instructions)


    def resolve(self, condition):
        # Boolean value 
        if len(condition) == 1:
            return condition[0] == "True"
        
        left, operation, right = condition

        left = self.data(left)
        right = self.data(right)
        

        if operation == "==":
            return left == right
        if operation == "!=":
            return left != right
        if operation == ">":
            return left > right
        if operation == "<":
            return left < right
        if operation == "<=": 
            return left <= right
        if operation == ">=":
            return left >= right
        
        if operation == "+":
            return left + right
        if operation == "-":
            return left - right
        
        if operation == "*":
            return left * right
            
            
        raise ValueError(f"Unknown operator {operation}")
        

    def data(self, source):
        
        # print(source)
        if isinstance(source, int):
            return source
        
        elif "[" in source and source.endswith("]"):

            

            index_start = source.index("[")
            index_end = source.index("]")

            index = source[index_start+1:index_end]
            list_name = source[:index_start]

            if list_name in self.env:

                try:
                    index = self.data(index)
                    return self.env[list_name][index]
                
                except:
                    raise ValueError(f"Invalid index position {index}")

            else:
                raise ValueError(f"List does not exist with the name {list_name}")
        
        elif source.startswith("\"") and source.endswith("\""):
            return source[1:-1]
        
        elif source.isdigit():
            return int(source)
        
        elif source in self.env:
            return self.env[source]
        
        else:
            raise SyntaxError(f"Unknown data {source}")

    def read_code(self, code):
        lines = code.splitlines()

        #_ is the index returned, but it doesn't matter here
        instructions, _ = self.parse_block(lines, 0)
        return instructions

    # Lexer 
    def to_tokens(self, line):
        tokens = []
        characters = list(line)
        is_stringmode = False
        is_listmode = False
        token = ""

        # New line
        if len(characters) < 1:
            return []
        
        i = 0
        while i < len(characters):
            
            # print(token)
            if characters[i] == " " and not is_stringmode and not is_listmode:
                if token != "":
                    tokens.append(token)
                    token = ""

            

            elif characters[i] in "[]":
                if characters[i] == "]":
                    is_listmode = False
                    token += characters[i]
                    tokens.append(token)
                    token = ""

                else: 
                    is_listmode = True
                    token += characters[i]
                    
            elif characters[i] == "\"" and not is_listmode:
                if is_stringmode:
                    is_stringmode = False
                    
                    token += characters[i]
                    tokens.append(token)
                    token = ""
                else:
                    is_stringmode = True
                    token += characters[i]
                    
            else:   
                token += characters[i]
                
                
            i += 1

        if token != "":
            tokens.append(token)
        
        # print(tokens)
        return tokens
        
    def prarse_list_token(self, l):
        list_items = self.to_tokens(l[1:-1])
        result = []
        for item in list_items:
            result.append(self.data(item))
        return result

    def parse_block(self, lines, current_index):
        instructions_to_return = []
        
        while current_index < len(lines):
            line = lines[current_index].strip()
            tokens = self.to_tokens(line)

            if not tokens:
                # Empty line, so move to next
                current_index += 1 
                continue

            
            if tokens[0] == "END":
                # 7 - END
                # Returns previous + index of 8 to continue on 
                return instructions_to_return, current_index + 1

            if tokens[0] == "DO":

                
                iterator = tokens[1]
                
                body, current_index = self.parse_block(lines, current_index + 1)
                instructions_to_return.append({
                    "type"      : "for_loop",
                    "iterator" : iterator,
                    "body"      : body
                })

                continue

            if tokens[0] == "IF":
                # Store position of THEN
                then_pos = tokens.index("THEN")
                condition = tokens[1:then_pos]

                # Sets current index to end of if statement 
                body, current_index  = self.parse_block(lines, current_index + 1)

                instructions_to_return.append({
                    "type"      : "if",
                    "condition" : condition,
                    "body"      : body
                })

                continue
                    
            elif tokens[0] == "print":
    
                instructions_to_return.append({
                    "type"  : "print",
                    "data"  : tokens[1:]
                })
            
            elif tokens[0] == "VAR":
                instructions_to_return.append({
                    "type": "var",
                    "name": tokens[1],
                    "value": tokens[3:]
                })

            elif tokens[0] == "LIST":
                instructions_to_return.append({
                    "type": "list",
                    "name": tokens[1],
                    "value": tokens[3:]
                })

            elif tokens[0] == "ADD":
                instructions_to_return.append({
                    "type": "add",
                    "name": tokens[1],
                    "value": tokens[2]
                })

            current_index += 1

        return instructions_to_return, current_index


    def execute_code(self, instructions):
        
        for ins in instructions:

            if ins["type"] == "var":
                if ins["name"] in self.reserved_words:
                    raise SyntaxError("You cannot use reserved words as variable names")
                
                data = None
                if 1 < len(ins["value"]):
                    data = self.resolve(ins["value"])
                else:
                    data = ins["value"][0]

                self.env[ins["name"]] = self.data(data)

            if ins["type"] == "list":
                if ins["name"] in self.reserved_words:
                    raise SyntaxError("You cannot use reserved words as list names")
                
                self.env[ins["name"]] = self.prarse_list_token(ins["value"][0])

            if ins["type"] == "add":
                if ins["name"] not in self.env:
                    raise ValueError(f"List called {ins["name"]} does not exist")
                if isinstance(self.env[ins["name"]], list):
                    self.env[ins["name"]].append(self.data(ins["value"]))
                else:
                    raise SyntaxError(f"{ins["name"]} is not of type 'list'")

            if ins["type"] == "print":
                data = None
                if 1 < len(ins["data"]):
                    data = self.resolve(ins["data"])
                else:
                    data = ins["data"][0]

                print(self.data(data))
            
            if ins["type"] == "if":
                if self.resolve(ins["condition"]):

                    self.execute_code(ins["body"])

            if ins["type"] == "for_loop":

                iter = self.data(ins["iterator"])
                if not isinstance(iter, int):
                    raise SyntaxError("Iterator must be of type intiger!")
    
                for i in range (iter):
                    self.execute_code(ins["body"])

                    
'''
[IF, 1, ==, 1 THEN]
[print, sup]
[print, wsg]
[print, yolo]
[END]
'''

'''
{
    'type': 'if', 
    'condition': ['1', '==', '2'], 
    'body': [
        {'type': 'print', 'data': 'sup'}, 
        {'type': 'print', 'data': 'sup'}, 
        {'type': 'print', 'data': 'sup'}
    ]
}


'''