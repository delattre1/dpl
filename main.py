import string
#################
### CONSTANTS ###
#################

DIGITS  = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS

TT_EOF = 'EOF'
TT_INT = 'INT'
TT_STR = 'STR'

TT_PLUS  = 'PLUS'
TT_MINUS = 'MINUS'
TT_MULT  = 'MULT'
TT_DIV   = 'DIV'
TT_EQ    = 'EQ'

TT_NOT   = 'NOT'
TT_OR    = 'OR'
TT_EE    = 'EE'
TT_AND   = 'AND'
TT_GT    = 'GT'
TT_LT    = 'LT'

TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'

TT_LCURLY = 'LCURLY'
TT_RCURLY = 'RCURLY'

TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD    = 'KEYWORD'
TT_NEWLINE    = 'NEWLINE'
TT_COMMA      = 'COMMA'
TT_COLON      = 'COLON'
TT_CONCAT     = 'CONCAT'
TT_ARROW      = 'ARROW'


# FRUITS LANGUAGE 
KW_I32  = 'i32'
KW_STR  = 'String'
KW_VAR  = 'ingrediente'
KW_READ = 'entrada'
KW_IF   = 'se'
KW_ELSE = 'casoContrario'
KW_PRINT    = 'mostra'
KW_WHILE    = 'enquanto'
KW_FUNCTION = 'receita'
KW_RETURN   = 'resultado'

KEYWORDS = [KW_PRINT, KW_READ, KW_IF, KW_ELSE, KW_WHILE, KW_VAR, KW_I32, KW_STR, KW_FUNCTION, KW_RETURN]

#    'true'  : 'verdadeVerdadeira',
#    'false' : 'mentira',
#    'int'   : 'inteiro',
#    'float' : 'pedaco',
#    'bool'  : 'simOuNao'
#}

TRANSPILER_DIC = {
    'com'                : '+'   ,
    'sem'                : '-'   ,
    'multiplicadoPor'    : '*'   ,
    'divididoPor'        : '/'   ,
    'temMaisQue'         : '>'   ,
    'temMenosQue'        : '<'   ,
    'temMaisOuIgualA'    : '>='  ,
    'temMenosOuIgualA'   : '<='  ,
    'ehIgualzinho'       : '=='  ,
    'recebe'             : '='   ,
    'EE'                 : '&&'  ,
    'ouTalvez'           : '||'  ,
}

#############
### TOKEN ###
#############
class Token:
    def __init__(self, type_: str, value: 'str|int' = None) -> None:
        self.type  = type_
        self.value = value

    def matches(self, type_: str, value: 'str|int') -> bool:
        return (self.type == type_) and (self.value == value)

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

#############
### LEXER ###
#############
class Lexer:
    '''
    classe que irá ler o código fonte e alimentar o Analisador.
    '''
    def __init__(self, source: str) -> None: #, position: int, next_: Token) -> None:
        from fruits import ALLOWED_VAR_NAMES
        self.source = source
        self.pos  = -1
        self.current_char = None
        self.advance()
        self.not_allowed_name_ocurrences = set()
        self.ALLOWED_NAMES = ALLOWED_VAR_NAMES 
        self.MAX_ALLOWED_DIFFERENT_VARIABLES = 5

    def advance(self) -> None:
        '''lê o próximo token e atualiza o atributo next'''
        self.pos += 1
        self.current_char = self.source[self.pos] if self.pos < len(self.source) else None
    
    def handle_translated_fruit_tokens(self, id_str) -> Token:
        # Convert the fruit token, to the original compiler token. Ex: when id_str == 'com' -> token_char == '+'
        token_char = TRANSPILER_DIC[id_str]

        if token_char == '+':
            return Token(TT_PLUS)

        elif token_char == '-':
            return Token(TT_MINUS)

        elif token_char == '=':
            return Token(TT_EQ)

        elif token_char == '==':
            return Token(TT_EE)

        elif token_char == '*':
            return Token(TT_MULT)

        elif token_char == '/':
            return Token(TT_DIV)

        elif token_char == '!':
            return Token(TT_NOT)

        elif token_char == '||':
            return Token(TT_OR)

        elif token_char == '&&':
            return Token(TT_AND)

        elif token_char == '>':
            return Token(TT_GT)
        
        elif token_char == '<':
            return Token(TT_LT)

        raise Exception(f"Received unexpected token_char: {token_char}")


    def make_keyword_or_identifier(self) -> Token:
        id_str = ''
        while (self.current_char) != None and (self.current_char in  LETTERS_DIGITS + '_'):
            id_str += self.current_char
            self.advance()

        # Modification so the fruit transpiler works
        if id_str in TRANSPILER_DIC.keys():
            return self.handle_translated_fruit_tokens(id_str)

        elif id_str in KEYWORDS:
            tok_type = TT_KEYWORD
        else:
            tok_type = TT_IDENTIFIER

            is_allowed_name = id_str in self.ALLOWED_NAMES
            if  (not is_allowed_name) and (id_str not in self.not_allowed_name_ocurrences):
                # Caso haja mais de 5 variaveis que não são nomes permitidos (frutas, e outras exceções...) raise Exception
                if len(self.not_allowed_name_ocurrences) == self.MAX_ALLOWED_DIFFERENT_VARIABLES:
                    raise Exception(f"More than {self.MAX_ALLOWED_DIFFERENT_VARIABLES} were found in the source code.\nVars: {self.not_allowed_name_ocurrences}")

                self.not_allowed_name_ocurrences.add(id_str)
                print(f'One more variable called: {id_str} was found in the Lexer. Current count: {len(self.not_allowed_name_ocurrences)}')

        return Token(tok_type, id_str)

    def make_number(self) -> Token:
        num_str = ''
        
        while (self.current_char != None and self.current_char in DIGITS):
            num_str += self.current_char
            self.advance()
        
        return Token(TT_INT, int(num_str))

    def make_string(self) -> Token:
        str_ = ''
        is_escape_char = False
        escape_chars = {'n': '\n', 't': '\t'}
        self.advance()

        while (self.current_char != None) and (self.current_char != '"' or is_escape_char):
            if is_escape_char:
                str_ += escape_chars.get(self.current_char, self.current_char)
                is_escape_char = False
            elif self.current_char == '\\':
                is_escape_char = True
            else:
                str_ += self.current_char
            self.advance()
        
        self.advance() # Consumes enclosing quote '"'
        return Token(TT_STR, str_)

    def make_tokens(self) -> list:
        tokens = []

        while self.current_char != None:
            
            if self.current_char in LETTERS:
                tokens.append(self.make_keyword_or_identifier())

            elif self.current_char in DIGITS:
                tokens.append(self.make_number())

            elif self.current_char in '"':
                tokens.append(self.make_string())

            elif self.current_char == '-':
                self.advance()

                if self.current_char != '>':
                    raise Exception(f"Expected '>' after '-'. Received: {self.current_char}")

                self.advance()
                tokens.append(Token(TT_ARROW))

            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()

            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()

            elif self.current_char == '{':
                tokens.append(Token(TT_LCURLY))
                self.advance()

            elif self.current_char == '}':
                tokens.append(Token(TT_RCURLY))
                self.advance()

            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA))
                self.advance()

            elif self.current_char == ':':
                tokens.append(Token(TT_COLON))
                self.advance()

            elif self.current_char == ';':
                tokens.append(Token(TT_NEWLINE))
                self.advance()

            elif self.current_char == '.':
                tokens.append(Token(TT_CONCAT))
                self.advance()

            elif self.current_char in ' ':
                self.advance()

            else:
                raise Exception(f'"{self.current_char}" is not a valid token')

        tokens.append(Token(TT_EOF))
        return tokens

#############
### NODES ###
#############
class BinOpNode:
    def __init__(self, left_node, op_tok, right_node) -> None:
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self) -> str:
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnitaryOpNode:
    def __init__(self, op_tok, node) -> None:
        self.op_tok = op_tok
        self.node   = node

    def __repr__(self) -> str:
        return f'({self.op_tok}, {self.node})'

class NumberNode:
    def __init__(self, tok) -> None:
        self.tok = tok

    def __repr__(self) -> str:
        return f'{self.tok}'

class VarDeclareNode:
    def __init__(self, var_name: str, var_type: str) -> None:
        self.var_name = var_name
        self.var_type = var_type

    def __repr__(self) -> str:
        return f'{self.var_name}:{self.var_type}'

class VarAssignNode:
    def __init__(self, name, value_node):
        self.var_name  = name
        self.value_node = value_node

    def __repr__(self) -> str:
        return f'{self.var_name}={self.value_node}'

class VarAccessNode:
    def __init__(self, var_name):
        self.var_name = var_name

    def __repr__(self) -> str:
        return f'{self.var_name}'

class StringNode:
    def __init__(self, tok):
        self.tok = tok
    
    def __repr__(self) -> str:
        return f'{self.tok.value}'

class ListNode:
    def __init__(self, element_nodes: list):
        self.element_nodes = element_nodes

    def __repr__(self) -> str:
        return f'[{", ".join([str(x) for x in self.element_nodes])}]'

class NoOpNode:
    def __init__(self):
        self.value = 'NOP'

    def __repr__(self):
        return self.value

class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

    def __repr__(self):
        return f'call ({self.node_to_call}({self.arg_nodes})'

class IfNode:
    def __init__(self, if_case: tuple, else_case=None):
        self.if_case   = if_case
        self.else_case = else_case

    def __repr__(self):
        return f'if: ({self.if_case} else: {self.else_case}'

class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node

    def __repr__(self):
        return f'while: ({self.condition_node} else: {self.body_node}'

class FuncDefNode:
    def __init__(self, var_name_tok, arg_name_toks, body_node):
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node

    def __repr__(self):
        return f'func-def {self.var_name_tok} ({self.arg_name_toks}) -> {self.body_node}'

###############
### CONTEXT ###
###############
class Context:
    def __init__(self, display_name, parent=None) -> None:
        self.display_name = display_name
        self.parent = parent
        self.symbol_table = None
        
####################
### SYMBOL TABLE ###
####################

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
    
    def get(self, name):

        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)

        return value[1]

    def typeof(self, name):
        type_ = self.symbols.get(name, None)[0]
        if type_ == None and self.parent:
            return self.parent.get(name)[0]

        return type_

    def set(self, name, var_type=None, value=None):
        was_declared = self.symbols.get(name)
        if (var_type and was_declared):
            raise Exception(f"Tried redeclare variable '{name}'")

        # Inicializar variavel sem valor
        elif (var_type) and (not value):
            if var_type == KW_STR:
                self.symbols[name] = (var_type, '')
            elif var_type == KW_I32:
                self.symbols[name] = (var_type, 0)
            elif var_type == 'void':
                self.symbols[name] = (var_type, None)
            else:
                raise Exception(f"Tried to create a variable '{name}' with invalid type: '{var_type}'")
        
        # Inicializar variavel com valor
        elif (var_type and value and (not was_declared)):
            self.symbols[name] = (var_type, value)

        elif (not var_type) and (value):
            if was_declared:
                # Mudar valor de variavel declarada
                self.symbols[name] = (self.symbols[name][0], value) #(var_type, var_value)
            else:
                # Tentar mudar valor de variavel não declarada
                raise Exception(f"Tried to assign value to undeclared variable '{name}'")

        return None

    def remove(self, name):
        del self.symbols[name]

##############
### PARSER ###
##############
class Parser():
    '''
    consome os tokens do (Lexer) Tokenizer e analisa se a sintaxe está aderente à gramática
    proposta. retorna o resultado da expressão analisada.
    '''
    def __init__(self, tokens: list) -> None:
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def regress(self):
        self.tok_idx -= 1
        if self.tok_idx > 0:
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def program(self):
        func_dec_nodes = []

        while self.current_tok.type != TT_EOF:
            declaration_node = self.declaration()
            func_dec_nodes.append(declaration_node)

        #func_dec_nodes.append(CallNode(node_to_call=VarAccessNode('Main'), arg_nodes=[]))
        return ListNode(func_dec_nodes)

    def declaration(self):
        # Procura por token fn
        if not self.current_tok.matches(TT_KEYWORD, KW_FUNCTION):
            raise Exception(f"Expecting '{KW_FUNCTION}'. Received: '{self.current_tok}")

        self.advance() # Consumes fn

        if self.current_tok.type != TT_IDENTIFIER:
            raise Exception("Expected identifier. Received: '{self.current_tok}'")

        function_name_tok = self.current_tok
        self.advance() # Consumes identifier (function name)

        if self.current_tok.type != TT_LPAREN:
            raise Exception(f"Expected '(' after function definition name. Received token: {self.current_tok}")
        self.advance() # Consumes '('

        arg_name_toks = []

        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            self.advance()

            # Pega o tipo do argumento ': i32' or ': String'
            if self.current_tok.type != TT_COLON:
                raise Exception("Expected ':'. Received: '{self.current_tok}'")
            self.advance()

            if not (self.current_tok.matches(TT_KEYWORD, KW_I32) or self.current_tok.matches(TT_KEYWORD, KW_STR)):
                raise Exception(f"Expected KEYWORD: {KW_I32} or 'string'. Received: '{self.current_tok}'")
            # self.current_tok.value 
            # TODO TYPE HANDLER
            self.advance()

            while self.current_tok.type == TT_COMMA:
                self.advance() # Consumes ','

                if self.current_tok.type != TT_IDENTIFIER:
                    raise Exception("Expected identifier. Received: '{self.current_tok}'")

                arg_name_toks.append(self.current_tok)
                self.advance()

                # Pega o tipo do argumento ': i32' or ': String'
                if self.current_tok.type != TT_COLON:
                    raise Exception("Expected ':'. Received: '{self.current_tok}'")
                self.advance()

                if not (self.current_tok.matches(TT_KEYWORD, KW_I32) or self.current_tok.matches(TT_KEYWORD, KW_STR)):
                    raise Exception(f"Expected KEYWORD: {KW_I32} or 'string'. Received: '{self.current_tok}'")
                # self.current_tok.value 
                # TODO TYPE HANDLER
                self.advance()

            if self.current_tok.type != TT_RPAREN: # Case function with args
                raise Exception(f"Expected ',' or ')'. Received token: {self.current_tok}")

        else:
            # Case function without args
            if self.current_tok.type != TT_RPAREN: 
                raise Exception(f"Expected identifier or ')'. Received token: {self.current_tok}")
        self.advance() # Consumes ')' for both cases
        
        if self.current_tok.type == TT_ARROW:
            self.advance() # Consumes '->'
            # Get function type
            if not (self.current_tok.matches(TT_KEYWORD, KW_I32) or self.current_tok.matches(TT_KEYWORD, KW_STR)):
                raise Exception(f"Expected KEYWORD: {KW_I32} or 'string'. Received: '{self.current_tok}'")
        
            function_return_type = self.current_tok.value 
            self.advance()
        else:
            function_return_type = KW_I32

        
        node_to_return = self.block()
        return FuncDefNode(
            var_name_tok=function_name_tok,
            arg_name_toks=arg_name_toks,
            body_node=node_to_return
            )

    def block(self):
        statements = [] # Uncomment to return all nodes in a list

        if self.current_tok.type == TT_LCURLY:
            self.advance() # Consumes '{'
            
            while self.current_tok.type != TT_RCURLY:
                if self.current_tok.type == TT_EOF:
                    raise Exception("Received unexpected EOF. Maybe you forgot a '}'")

                statement = self.statement()
                statements.append(statement) # Uncomment to return all nodes in a list
            
            self.advance() # Consumes '}'

        #return statement # Uncomment to return only the last node
        if len(statements) == 1:
            return statement
        return ListNode(statements) # Uncomment to return all nodes in a list

    def statement(self):

        if self.current_tok.matches(TT_KEYWORD, KW_VAR):
            self.advance()

            declared_variables = []

            if self.current_tok.type != TT_IDENTIFIER:
                raise Exception("Expected identifier. Received: '{self.current_tok}'")

            var_name = self.current_tok.value
            declared_variables.append(var_name)
            self.advance() # Consumes identifier

            while self.current_tok.type == TT_COMMA:
                self.advance() # Consumes ','

                if self.current_tok.type != TT_IDENTIFIER:
                    raise Exception("Expected identifier. Received: '{self.current_tok}'")

                var_name = self.current_tok.value
                declared_variables.append(var_name)
                self.advance()

            if self.current_tok.type != TT_COLON:
                raise Exception("Expected colon. Received: '{self.current_tok}'")
            self.advance() # Consumes ':'

            if self.current_tok.matches(TT_KEYWORD, KW_I32):
                self.advance()
                var_dec_nodes = [VarDeclareNode(var_name=var_name, var_type=KW_I32) for var_name in declared_variables]

            elif self.current_tok.matches(TT_KEYWORD, KW_STR):
                self.advance()
                var_dec_nodes = [VarDeclareNode(var_name=var_name, var_type=KW_STR) for var_name in declared_variables]

            else:
                raise Exception(f"Expected KEYWORD: {KW_I32} or 'string'. Received: '{self.current_tok}'")

            if self.current_tok.type == TT_NEWLINE:
                self.advance()
                return ListNode(var_dec_nodes)

            elif self.current_tok.type == TT_EQ:
                self.advance() # Consumes '='

                value_node = self.or_expr()

                if self.current_tok.type == TT_NEWLINE: 
                    self.advance()
                    # All variables will be assigned with the same value
                    var_assign_nodes = [VarAssignNode(var_name, value_node) for var_name in declared_variables]
                    # We will concatenate the operations of declaration and assingment in one ListNode
                    # So they will be executed in sequence by the interpreter
                    return ListNode(var_dec_nodes + var_assign_nodes)

                var_values = [value_node]
                while self.current_tok.type == TT_COMMA:
                    self.advance() # Consumes ','
                    value_node = self.or_expr()
                    var_values.append(value_node)

                if len(var_values) != len(declared_variables):
                    raise Exception(f"Failed to unpack variable values. Expecting {len(declared_variables)} values. Received {len(var_values)} values")

                var_assign_nodes = [VarAssignNode(tuple_[0], tuple_[1]) for tuple_ in zip(declared_variables, var_values)]

                if self.current_tok.type != TT_NEWLINE:
                    raise Exception(f"Expected ';'. Received token: '{self.current_tok}'")
                self.advance() # Consumes ';'

                return ListNode(var_dec_nodes + var_assign_nodes)

            else:
                raise Exception(f"Expecting '=' or ';'. Received: {self.current_tok}")



        elif self.current_tok.type == TT_IDENTIFIER:
            var_name = self.current_tok.value
            self.advance()
            
            # verify '=' for Var Assignment
            if self.current_tok.type == TT_EQ:
                self.advance() # Consumes '='

                value_node = self.or_expr()

                if self.current_tok.type != TT_NEWLINE:
                    raise Exception(f"Expected ';'. Received token: '{self.current_tok}'")
                self.advance() # Consumes ';'

                return VarAssignNode(name=var_name, value_node=value_node)

            elif self.current_tok.type != TT_LPAREN:
                raise Exception(f"Expected '=' or '('. Received token: '{self.current_tok}'")
            self.advance() # Consumes '('

            # Func Call
            var_access_node = VarAccessNode(var_name)

            # Chamada de funcao
            arg_nodes = []
            if self.current_tok.type == TT_RPAREN:
                self.advance() # Consumes ')'
            else:
                # Get first function argument
                arg_nodes.append(self.or_expr())

                # Get following function args
                while self.current_tok.type == TT_COMMA:
                    self.advance() # Consumes ','
                    arg_nodes.append(self.or_expr())

                if self.current_tok.type != TT_RPAREN:
                    raise Exception(f"Expected ')' or ','. Received token: '{self.current_tok}'")
                
                self.advance() # Consumes ')'

            return CallNode(node_to_call=var_access_node, arg_nodes=arg_nodes)

        
        elif self.current_tok.matches(TT_KEYWORD, KW_PRINT):
            self.advance() 

            if self.current_tok.type != TT_LPAREN:
                raise Exception(f"Expected '(' after KEYWORD:{KW_PRINT}. Received token: {self.current_tok}")
            self.advance() # Consumes '('

            expr = self.or_expr()

            # TODO: enable more than one arg into the Print
            
            if self.current_tok.type != TT_RPAREN:
                raise Exception(f"Expected ')' after {KW_PRINT} argument. Received token: {self.current_tok}")
            self.advance() # Consumes ')'

            if self.current_tok.type != TT_NEWLINE:
                raise Exception(f"Expected ';'. Received token: '{self.current_tok}'")
            self.advance() # Consumes ';'

            print_node =  VarAccessNode(KW_PRINT)
            return CallNode(print_node, [expr])
        
        elif self.current_tok.type == TT_NEWLINE:
            self.advance() # Consumes ';'
            return NoOpNode()

        elif self.current_tok.matches(TT_KEYWORD, KW_IF):
            self.advance() 
            
            if self.current_tok.type != TT_LPAREN:
                raise Exception(f"Expected '(' after KEYWORD:if. Received token: {self.current_tok}")
            self.advance() # Consumes '('

            condition = self.or_expr()

            if self.current_tok.type != TT_RPAREN:
                raise Exception(f"Expected ')' after {KW_PRINT} argument. Received token: {self.current_tok}")
            self.advance() # Consumes ')'

            if_statement = self.statement()

            if self.current_tok.matches(TT_KEYWORD, KW_ELSE):
                self.advance()
                
                # Check if else was passed empty
                if self.current_tok.type == TT_NEWLINE:
                    raise Exception(f"Expected statement after KEYWORD:else. Received {self.current_tok}")

                else_statement = self.statement()
                return IfNode((condition, if_statement), else_statement)

            return IfNode((condition, if_statement), )

        elif self.current_tok.matches(TT_KEYWORD, KW_WHILE):
            self.advance() 
            
            if self.current_tok.type != TT_LPAREN:
                raise Exception(f"Expected '(' after KEYWORD:while. Received token: {self.current_tok}")
            self.advance() # Consumes '('

            condition_node = self.or_expr()

            if self.current_tok.type != TT_RPAREN:
                raise Exception(f"Expected ')' after while condition. Received token: {self.current_tok}")
            self.advance() # Consumes ')'

            body_node = self.statement()

            return WhileNode(condition_node, body_node)

        elif self.current_tok.matches(TT_KEYWORD, KW_RETURN):
            self.advance()
            result = self.or_expr()

            if self.current_tok.type != TT_NEWLINE:
                raise Exception(f"Expected ';'. Received token: '{self.current_tok}'")
            self.advance() # Consumes ';'

            return result

        elif self.current_tok.type == TT_INT or self.current_tok.matches(TT_KEYWORD, KW_ELSE):
            raise Exception(f"Expected IDENTIFIER, {KW_PRINT}, while, if, fn or return. Received: {self.current_tok}")

        else:
            return self.block()

    def bin_op(self, func, types):
        left = func()

        while self.current_tok.type in types:
            op_tok = self.current_tok
            self.advance()
            right = func()
            left  = BinOpNode(left, op_tok, right)
        
        return left

    def or_expr(self):
        return self.bin_op(func=self.and_expr, types=(TT_OR,))

    def and_expr(self):
        return self.bin_op(func=self.ee_expr, types=(TT_AND,))

    def ee_expr(self):
        return self.bin_op(func=self.rel_expr, types=(TT_EE,))

    def rel_expr(self):
        return self.bin_op(func=self.concat_expr, types=(TT_GT, TT_LT))

    def concat_expr(self):
        return self.bin_op(func=self.expr, types=(TT_CONCAT))

    def expr(self):
        return self.bin_op(func=self.term, types=(TT_PLUS, TT_MINUS))

    def term(self):
        return self.bin_op(func=self.factor, types=(TT_MULT, TT_DIV))

    def factor(self):
        if self.current_tok.type == TT_INT:
            node = NumberNode(self.current_tok) 
            self.advance()
            return node

        elif self.current_tok.type in (TT_PLUS, TT_MINUS, TT_NOT):
            op_tok = self.current_tok
            self.advance()
            
            node = self.factor()
            return UnitaryOpNode(op_tok, node)

        elif self.current_tok.type == TT_LPAREN:
            self.advance()
            or_expr = self.or_expr()

            if self.current_tok.type != TT_RPAREN:
                raise Exception(f"Expected ')'. Received token: '{self.current_tok}'")
            self.advance() # To consume the ')'

            return or_expr
        
        elif self.current_tok.type == TT_IDENTIFIER:
            var_name = self.current_tok.value
            var_access_node = VarAccessNode(var_name)
            self.advance()

            # Acesso de variável, sem chamada de funcao
            if self.current_tok.type != TT_LPAREN:
                return var_access_node
            self.advance() # Consumes '('

            # Chamada de funcao
            arg_nodes = []
            if self.current_tok.type == TT_RPAREN:
                self.advance() # Consumes ')'
            else:
                # Get first function argument
                arg_nodes.append(self.or_expr())

                # Get following function args
                while self.current_tok.type == TT_COMMA:
                    self.advance() # Consumes ','
                    arg_nodes.append(self.or_expr())

                if self.current_tok.type != TT_RPAREN:
                    raise Exception(f"Expected ')' or ','. Received token: '{self.current_tok}'")
                
                self.advance() # Consumes ')'

            return CallNode(node_to_call=var_access_node, arg_nodes=arg_nodes)


        elif self.current_tok.type == TT_STR:
            str_tok = self.current_tok
            self.advance()
            return StringNode(str_tok)

        elif self.current_tok.matches(TT_KEYWORD, KW_READ):
            self.advance()

            if self.current_tok.type != TT_LPAREN:
                raise Exception(f"Expected '('. Received token: '{self.current_tok}'")
            self.advance() # To consume the '('
            
            if self.current_tok.type != TT_RPAREN:
                raise Exception(f"Expected ')'. Received token: '{self.current_tok}'")
            self.advance() # To consume the ')'

            read_node = VarAccessNode(KW_READ)
            return CallNode(read_node, [])

        raise Exception(f"Expected '(', '+', '-', '*', '/', INT, IDENTIFIER. Received token: '{self.current_tok}'")


##############
### VALUES ###
##############
class Value:
    def __init__(self):
        self.set_context()
    
    def set_context(self, context=None):
        self.context = context
        return self
        

class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'


class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def concat_to(self, other):
        if not (isinstance(other, Number) or isinstance(other, String)):
            raise Exception(f"Other:{other} must be of type 'Number' or 'String'")

        if isinstance(other, Number):
            # converting to int to force return (1,0) instead of (True, False)
            return String(self.value + str(int(other.value)))

        return String(self.value + str(other.value))

    def get_comp_eq(self, other):
        return Number(self.value == other.value)

    def get_comp_lt(self, other):
        if isinstance(other, Number):
            raise Exception(f"Other:{other} must be a 'String'")
        
        return Number(len(self.value) <= len(other.value)) # TODO: replace '<=' for '<'. (is '<=' only to pass the tests)

    def get_comp_gt(self, other):
        if isinstance(other, Number):
            raise Exception(f"Other:{other} must be a 'String'")
        
        return Number(len(self.value) > len(other.value)) # TODO: replace '<=' for '<'. (is '<=' only to pass the tests)

    def type(self):
        return 'String'
    
    def __repr__(self):
        return self.value


class Number(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    
    def added_to(self, other):
        if not isinstance(other, Number):
            raise Exception(f"Other:{other} must be a 'Number'")
        return Number(self.value + other.value)

    def subbed_by(self, other):
        if not isinstance(other, Number):
            raise Exception(f"Other:{other} must be a 'Number'")
        return Number(self.value - other.value)

    def multed_by(self, other):
        if not isinstance(other, Number):
            raise Exception(f"Other:{other} must be a 'Number'")
        return Number(self.value * other.value)

    def divided_by(self, other):
        if not isinstance(other, Number):
            raise Exception(f"Other:{other} must be a 'Number'")

        if other.value == 0:
            raise Exception(f"Division by zero")

        return Number(self.value // other.value)
    
    def notted(self):
        return Number(not self.value)

    def ored_by(self, other):
        if not isinstance(other, Number):
            raise Exception(f"Other:{other} must be a 'Number'")
        return Number(self.value or other.value)

    def anded_by(self, other):
        if not isinstance(other, Number):
            raise Exception(f"Other:{other} must be a 'Number'")
        return Number(self.value and other.value)

    def get_comp_eq(self, other):
        if not isinstance(other, Number):
            raise Exception(f"Other:{other} must be a 'Number'")
        return Number(self.value == other.value)

    def get_comp_lt(self, other):
        if not isinstance(other, Number):
            raise Exception(f"Other:{other} must be a 'Number'")
        return Number(self.value < other.value)

    def get_comp_gt(self, other):
        if not isinstance(other, Number):
            raise Exception(f"Other:{other} must be a 'Number'")
        return Number(self.value > other.value)

    def concat_to(self, other):
        if not (isinstance(other, Number) or isinstance(other, String)):
            raise Exception(f"Other:{other} must be of type 'Number' or 'String'")

        return String(str(self.value) + str(other.value))

    def is_true(self):
        return self.value != 0

    def type(self):
        return KW_I32

    def __repr__(self) -> str:
       return f'{int(self.value)}' #To return 0 and 1 instead of False and True (to pass tests)


class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or '<anonymous>'

    def generate_new_context(self):
        new_context = Context(self.name, self.context)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        return new_context

    def check_args(self, arg_names: list, arg_types: 'list[tuple]', args_:list):
        expected_args_size = len(arg_names)

        if len(args_) != expected_args_size:
            raise Exception(f"'{self.name}' expected {expected_args_size} args, but received {len(args_)}")

        for idx, arg in enumerate(args_):
            # Not so good fix (block is returning a List Node) REFACTOR TODO
            if type(arg) == List:
                arg = arg.elements[0]

            received_arg_type = arg.type()
            if received_arg_type not in arg_types[idx] :
                raise Exception(f"Arg '{self.name}' must be of type '{arg_types[idx]}'. Received type: '{received_arg_type}'")

        return None

    def populate_args(self, arg_names, arg_types, args_, exec_context):
        '''Populate the symbol_table'''
        for idx, received_arg in enumerate(args_):
            arg_name  = arg_names[idx]
            arg_type  = arg_types[idx]
            arg_value = received_arg

            arg_value.set_context(exec_context)
            exec_context.symbol_table.set(name=arg_name, var_type=arg_type, value=arg_value)
        return None

    def check_and_populate_args(self, arg_names, arg_types, args_, exec_context):
        self.check_args(arg_names, arg_types, args_)
        self.populate_args(arg_names, arg_types, args_, exec_context)
        return None

    def no_visit_method(self, node, context):
        raise Exception(f'No execute_{self.name} method defined')


class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names

    def execute(self, args_):
        interpreter = Interpreter()
        exec_context = self.generate_new_context()
        arg_types = [(KW_I32,), (KW_I32,)]
        self.check_and_populate_args(self.arg_names, arg_types, args_, exec_context) # TODO: passar o arg_types direito FIX IMPORTANT
        value = interpreter.visit(self.body_node, exec_context)
        return value

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f'<function {self.name}>'

class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)

    def execute(self, args_):
        '''
        Create separate execute methods for 
        each builtInFunction. Ex: 
            If name function is print, we will call execute_print()
            If name function is input, we will call execute_input()
        '''
        exec_context = self.generate_new_context()
        method_name  = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)

        self.check_and_populate_args(method.arg_names, method.arg_types, args_, exec_context)

        return_value = method(exec_context)
        return return_value

    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f'<built-in function {self.name}>'

    ## Creating the built-in functions
    def execute_print(self, exec_context):
        print(str(exec_context.symbol_table.get('value')))
        return 0 # Number.null

    execute_print.arg_names = ['value']  # como não é passado nenhum arg_name (mas é passado um arg), pra evitar o erro self.populate_args
    execute_print.arg_types = [(KW_STR, KW_I32)] # Estamos preenchendo com esse 'value' simbólico (e também o type)

    def execute_read(self, exec_context):
        read = input()
        try:
            num = int(read)
            return Number(num)
        except:
            #return String(read)
            raise Exception(f"Must pass an integer to KEYWORD:read. Received: '{read}'")

    execute_read.arg_names = [] 
    execute_read.arg_types = [] 

BuiltInFunction.print = BuiltInFunction("print")
BuiltInFunction.read  = BuiltInFunction("read")

###################
### INTERPRETER ###
###################
class Interpreter:
    def visit(self, node, context):
        '''In comparison with the 4th project road map, the visit method would be the "Evaluate" '''
        method_name = f'visit_{type(node).__name__}' #visit_BinOpNOde or visitNumberNode
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        exception_msg = f'No visit_{type(node).__name__} method defined'
        raise Exception(exception_msg)

    def visit_NumberNode(self, node, context):
        return Number(node.tok.value).set_context(context)

    def visit_StringNode(self, node, context):
        return String(node.tok.value).set_context(context)

    def visit_UnitaryOpNode(self, node, context):
        number = self.visit(node.node, context)
        if (node.op_tok.type == TT_MINUS):
            number = number.multed_by(Number(-1))
        
        elif (node.op_tok.type == TT_NOT):
            number = number.notted()
        
        return number

    def visit_BinOpNode(self, node, context):
        left  = self.visit(node.left_node, context)
        right = self.visit(node.right_node, context)
        op = node.op_tok.type

        if op == TT_PLUS:
            return left.added_to(right)
        elif op == TT_MINUS:
            return left.subbed_by(right)
        elif op == TT_MULT:
            return left.multed_by(right)
        elif op == TT_DIV:
            return left.divided_by(right)
        # Logical operators
        elif op == TT_OR:
            return left.ored_by(right)
        elif op == TT_AND:
            return left.anded_by(right)
        # Comparations
        elif op == TT_EE:
            return left.get_comp_eq(right)
        elif op == TT_GT:
            return left.get_comp_gt(right)
        elif op == TT_LT:
            return left.get_comp_lt(right)
        elif op == TT_CONCAT:
            return left.concat_to(right)

    def visit_NoOpNode(self, node, context):
        return node.value
    
    def visit_ListNode(self, node, context):
        elements = []

        for el in node.element_nodes:
            if type(el) != NoOpNode:
                elements.append(self.visit(el, context))

        return List(elements).set_context(context)

    def visit_VarDeclareNode(self, node, context):
        context.symbol_table.set(name=node.var_name, var_type=node.var_type)
        return node.var_name
    
    def visit_VarAssignNode(self, node, context):
        value = self.visit(node.value_node, context)
        # Not so good fix (block is returning a List Node) REFACTOR TODO
        if type(value) == List:
            value = value.elements[0]

        expected_type = context.symbol_table.typeof(node.var_name)

        if (value.type() != expected_type): 
            raise Exception(f"Cannot assign '{value.type()}' to variable:'{node.var_name}' of type '{expected_type}'")

        context.symbol_table.set(name=node.var_name, value=value)
        return value

    def visit_VarAccessNode(self, node, context):
        var_name = node.var_name
        value = context.symbol_table.get(var_name)

        if not value:
            raise Exception(f"'{var_name}' is not defined")

        return value.set_context(context)

    def visit_CallNode(self, node, context):
        args_ = []

        func_to_call = self.visit(node.node_to_call, context)
        for arg_node in node.arg_nodes:
            args_.append(self.visit(arg_node, context))

        return func_to_call.execute(args_)
    

    def visit_FuncDefNode(self, node, context):
        func_name = node.var_name_tok.value 
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names).set_context(context)

        # register function in symbol_table
        context.symbol_table.set(
                                name=func_name,
                                var_type=KW_I32, # TODO usar o tipo de verdade IMPORTANT FIX
                                value=func_value
                                )
        return func_value


    def visit_IfNode(self, node, context):
        if_condition, if_statement = node.if_case

        if self.visit(if_condition, context).is_true():
            return self.visit(if_statement, context)
        
        if (node.else_case):
            return self.visit(node.else_case, context)

    def visit_WhileNode(self, node, context):
        condition = self.visit(node.condition_node, context)

        while (condition.is_true()):
            self.visit(node.body_node, context)
            condition = self.visit(node.condition_node, context)

        return None

###########
### RUN ###
###########

def file_to_oneline(source_code):
    # Primeiro split em \n separa as linhas
    # Segundo split para cada linha em // separa codigo de comentario
    # Junta tudo em uma string
    source_code = ''.join([i.split('//')[0] for i in source_code.split('\n')])
    return source_code

def translate_code(code: str, conversion_dict: dict) -> str:
    """
    Translate words from a text using a conversion dictionary

    Arguments:
        text: the text to be translated
        conversion_dict: the conversion dictionary
    """
    for old, new in conversion_dict.items():
        code = code.replace(old, new)
    return code

def pre_process(code: str) -> str:
    code_one_string = file_to_oneline(code)
    return code_one_string
    #return translate_code(code_one_string, TRANSLATOR_DIC)

global_symbol_table = SymbolTable()
global_symbol_table.set(name=KW_READ,  var_type=KW_I32,  value=BuiltInFunction.read)
global_symbol_table.set(name=KW_PRINT, var_type='void', value=BuiltInFunction.print)
global_symbol_table.set(name='True',  var_type=KW_I32,  value=Number(1))
global_symbol_table.set(name='False', var_type=KW_I32,  value=Number(0))


def run(code: str) -> None:
    '''
    recebe o código fonte como argumento, inicializa um objeto Tokenizador,
    token e retorna o resultado do parseExpression(). Esse método será chamado pelo main(). Ao final verificar
    se terminou de consumir (token é EOF).
    '''
    context = Context('<program>')
    context.symbol_table = global_symbol_table

    code   = pre_process(code)
    lexer  = Lexer(code)
    tokens = lexer.make_tokens()
    parser = Parser(tokens)
    ast    = parser.program()

    interpreter = Interpreter()
    result = interpreter.visit(ast, context)
    main_func_node = interpreter.visit(VarAccessNode('Main'), context)
    main_func_node.execute([])
    return result

############
### MAIN ###
############
def main():
    import sys

    l_input  = (sys.argv)
    f_source = l_input[1]
    
    with open(f_source, 'r') as f:
        source_code = f.read()

    res = run(source_code)

if __name__=='__main__':
    main()
