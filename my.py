class My:
    def __init__(self, code):
        self.code = code
        self.env = {}
        self.instructions = self.read_code(self.code)
        self.reserved_words = ["IF", "THEN", "DO", "print", "END"]
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
        
        if source.startswith("\"") and source.endswith("\""):
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


    def to_tokens(self, line):
        tokens = []
        characters = list(line)
        is_stringmode = False
        token = ""

        # New line
        if len(characters) < 1:
            return []
        
        i = 0
        while i < len(characters):
    
            # print(token)
            if characters[i] == " " and not is_stringmode:
                if token != "":
                    tokens.append(token)
                    token = ""

            elif characters[i] == "\"":
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
        
        return tokens
        


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

                try:
                    iterator = int(tokens[1])
                except:
                    raise SyntaxError("Iterator must be of type intiger!")
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
                for i in range (ins["iterator"]):
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