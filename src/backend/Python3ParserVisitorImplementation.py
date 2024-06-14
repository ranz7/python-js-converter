from collections import deque
import re

import utils

from antlr4 import *
if __name__ is not None and "." in __name__:
    from .Python3Parser import Python3Parser
else:
    from Python3Parser import Python3Parser

class Python3ParserVisitor(ParseTreeVisitor):
    class Scopes:
        scopes = deque()
        
        GLOBAL_SCOPE_FUNCTIONS = {"print", "range", "abs", "round"}

        def __init__(self):
            self.enterScope()
            for func in self.GLOBAL_SCOPE_FUNCTIONS:
                self.getCurrentScope()["functions"].add(func)
        
        def enterScope(self):
            self.scopes.append({"variables": set(), "functions": set(), "classes": set()})
            
        def exitScope(self):
            self.scopes.pop()
                        
        def getCurrentScope(self):
            return self.scopes[-1]
        
        def inScope(self, name, return_subscope: bool = False) -> bool:
            for scope in self.scopes:
                for subscope in scope.values():
                    if name in subscope:
                        if return_subscope:
                            return True, subscope
                        return True
                    
            return False
        
        def addToCurrentScope(self, name, subscope):
            if self.inScope(name):
                self.removeFromCurrentScope(name)
            
            self.getCurrentScope()[subscope].add(name)
            
        def removeFromCurrentScope(self, name):
            self.errorIfNotInScope(name)
            
            for scope in self.scopes:
                for subscope in scope.keys():
                    if name in scope[subscope]:
                        scope[subscope].remove(name)
                        break
        
        subscope_names = {
                "variables": "Variable",
                "functions": "Function",
                "classes": "Class"
            }

        def errorIfNotInScope(self, name):
            is_scope = self.inScope(name)
            if not is_scope:
                raise NameError(f"{name} does not exist in the current scope")
            
    
    param_type_map = {
        'int': 'Number',
        'float': 'Number',
        'str': 'String',
        'bool': 'Boolean',
        'None': 'void'
    }
    
    comparison_operator_map = {
        '>': '>',
        '<': '<',
        '==': '===',
        '!=': '!==',
        '>=': '>=',
        '<=': '<=',
        'is': '===',
        'isnot': '!=='
    }
    
    arithmetic_operator_map = {
        '+': '+',
        '-': '-',
        '*': '*',
        '/': '/',
        '%': '%',
        '<<': '<<',
        '>>': '>>',
        '&': '&',
        '^': '^',
        '|': '|',
        '//': '/'
    }
    
    exception_type_map = {
        'Exception': 'Error',
        'ValueError': 'Error',
        'TypeError': 'TypeError',
        'NameError': 'ReferenceError',
        'ZeroDivisionError': 'Error',
        'IndexError': 'RangeError',
        'KeyError': 'Error',
        'FileNotFoundError': 'Error',
        'OSError': 'Error',
        'NotImplementedError': 'Error',
        'AttributeError': 'Error',
        'ImportError': 'Error',
        'SyntaxError': 'SyntaxError',
        'IndentationError': 'Error',
        'OverflowError': 'Error',
        'RuntimeError': 'Error',
        'StopIteration': 'Error',
        'UnboundLocalError': 'ReferenceError',
        'UnicodeDecodeError': 'Error',
        'UnicodeEncodeError': 'Error',
        'UnicodeTranslateError': 'Error',
        'AssertionError': 'Error',
        'BufferError': 'Error',
        'EOFError': 'Error',
        'ImportError': 'Error',
        'LookupError': 'Error',
        'MemoryError': 'Error',
        'ReferenceError': 'ReferenceError',
        'SystemExit': 'Error',
        'TypeError': 'TypeError',
        'ValueError': 'Error',
        'Warning': 'Error',
    }

    scopes = Scopes()
    
    def map_exception_type(self, except_clause):
        python_exception_type = except_clause.getChild(1).getText()
        js_exception_type = self.exception_type_map.get(python_exception_type, 'Error')
        
        return js_exception_type

    def get_exception_alias(self, except_clause: Python3Parser.Except_clauseContext):
        if except_clause.getChildCount() == 3:
            return except_clause.alias().getText()
        else:
            return 'e'
        
    def is_nth_child(self, ctx, n):
        parent = ctx.parentCtx
        if not parent:
            return False
        
        return parent.getChild(n) == ctx

    def aggregateResult(self, aggregate, nextResult):
        result = ""
        if aggregate is not None:
            result += aggregate
        if nextResult is not None:
            result += nextResult
        
        return result
    
    def visitTerminal(self, node):
        if node.getSymbol().text == "<EOF>":
            return "<EOF>"
        
        return self.defaultResult()

    def visitFile_input(self, ctx:Python3Parser.File_inputContext):
        result = self.visitChildren(ctx)

        class_definitions = ""
        function_definitions = ""
        main_code = ""
        eof_code = ""

        lines = result.split("\n")
        in_class = False
        in_function = False
        brace_count = 0

        for line in lines:
            stripped_line = line.strip()
            if "class " in stripped_line:
                in_class = True
            elif re.match(r"^\s*[\w\[\]]+\s+\w+\s*\([^)]*\)\s*", line) is not None:
                in_function = True

            if in_class:
                class_definitions += line + "\n"
                brace_count += stripped_line.count('{')
                brace_count -= stripped_line.count('}')
                
                if brace_count == 0:
                    in_class = False
            elif in_function:
                function_definitions += line + "\n"
                brace_count += stripped_line.count('{')
                brace_count -= stripped_line.count('}')
                
                if brace_count == 0:
                    in_function = False
            elif "<EOF>" in stripped_line:
                eof_code += "<EOF>\n"
            else:
                main_code += line + "\n"

        program_result = ""
        program_result += class_definitions
        program_result += function_definitions
        program_result += main_code

        return program_result

    def visitFuncdef(self, ctx:Python3Parser.FuncdefContext):    
        func_name = self.visit(ctx.name())
        
        return_type = ''
        if ctx.getChild(3).getText() == '->':
            return_type = self.visit(ctx.getChild(4))           

        self.scopes.addToCurrentScope(func_name, "functions")
        
        self.scopes.enterScope()
        
        params = self.visit(ctx.parameters())
        body = self.visit(ctx.block())
        
        self.scopes.exitScope()

        return f"function {func_name}{params} {body}"

    def visitParameters(self, ctx:Python3Parser.ParametersContext):
        parameters = self.visit(ctx.typedargslist()) if ctx.typedargslist() else ''
        return f'({parameters})'

    def visitTypedargslist(self, ctx:Python3Parser.TypedargslistContext):
        from Python3Parser import Python3Parser
        params = []
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            if isinstance(child, Python3Parser.TfpdefContext):
                param = self.visit(child)
                if i + 1 < ctx.getChildCount() and ctx.getChild(i + 1).getText() == '=':
                    default_value = self.visit(ctx.getChild(i + 2))
                    param += f' = {default_value}'
                params.append(param)
            elif child.getText() == ',':
                continue
            elif child.getText() in ('*', '**'):
                params.append(child.getText())
            else:
                param = self.visit(child)
                if param:
                    params.append(param)
        return ', '.join(params)

    def visitTfpdef(self, ctx:Python3Parser.TfpdefContext):
        param_name = self.visit(ctx.name())
        self.scopes.addToCurrentScope(param_name, "variables")
        result = f"{param_name}"
        return result

    def visitStmt(self, ctx:Python3Parser.StmtContext):    
        result = self.visitChildren(ctx)
        return result

    def visitSimple_stmt(self, ctx:Python3Parser.Simple_stmtContext):
        if ctx.getText() == "pass":
            return ""
        
        result = self.visitChildren(ctx) + ";\n"
        
        return result

    def visitExpr_stmt(self, ctx:Python3Parser.Expr_stmtContext):
        from Python3Parser import Python3Parser
        
        if ctx.getChildCount() == 3 and ctx.getChild(1).getText() == '=':
                _type, value = utils.get_type_of(ctx.getChild(2).getText())
                name = self.visit(ctx.getChild(0))

                self.scopes.addToCurrentScope(name, "variables")
                if _type == 'bad_type' or _type == 'None':
                    _type = ''
                
                result = f"let {name} = {value}"
                
                return result
            
        elif isinstance(ctx.getChild(1), Python3Parser.AnnassignContext):
            name = self.visit(ctx.testlist_star_expr(0))
            _type = self.visit(ctx.annassign().test(0))
            value = self.visit(ctx.annassign().test(1))
            
            value_type, _ = utils.get_type_of(value)
            if value_type != _type:
                raise TypeError(f"Type mismatch: {value_type} and {_type}")
            
            self.scopes.addToCurrentScope(name, "variables")
            
            return f"let {name} = {value}"
        return self.visitChildren(ctx)   

    def visitReturn_stmt(self, ctx:Python3Parser.Return_stmtContext):
        expr = self.visit(ctx.testlist())
        return f"return {expr}"

    def visitIf_stmt(self, ctx:Python3Parser.If_stmtContext):
        condition = self.visit(ctx.test(0))
        block = self.visit(ctx.block(0))
        result = f"if ({condition}) {block}"

        for i in range(1, ctx.getChildCount()//4):
            condition = self.visit(ctx.test(i)) 
            block = self.visit(ctx.block(i))
            result += f"else if ({condition}) {block}"
        
        if ctx.getChildCount() % 4 == 3:
            block = self.visit(ctx.block(ctx.getChildCount()//4))
            result += f"else {block}"

        return result

    def visitWhile_stmt(self, ctx:Python3Parser.While_stmtContext):
        condition = self.visit(ctx.test())  
        block = self.visit(ctx.block(0))  
        result = f"while ({condition}) {block}"

        return result

    def visitFor_stmt(self, ctx:Python3Parser.For_stmtContext):

        test = self.visit(ctx.testlist())
        param = self.visit(ctx.exprlist())[0] #TODO: Works only for one param
        
        self.scopes.addToCurrentScope(param, "variables")
        
        block = self.visit(ctx.block(0))

        if test.startswith("range"):
            test = test[6:-1].split(',')
            if len(test) == 1:
                test = [0, test[0], 1]
            elif len(test) == 2:
                test = [test[0], test[1], 1]

            sign = '<' if int(test[0]) < int(test[1]) else '>'
            result = f"for(let {param} = {test[0]}; {param} {sign} {test[1]}; {param} += {test[2]}) {block}"
        else:
            result = f"for(let {param} of {test[0]}) {block}"

        return result

    def visitTry_stmt(self, ctx:Python3Parser.Try_stmtContext):
        result = self.visitChildren(ctx)
        result = f"try {result}"
        
        return result

    def visitExcept_clause(self, ctx:Python3Parser.Except_clauseContext):
        exception_type = self.map_exception_type(ctx)
        exception_alias = self.get_exception_alias(ctx)

        self.scopes.addToCurrentScope(exception_alias, "variables")

        result = f"catch ({exception_alias}) "
        
        return result

    def visitBlock(self, ctx:Python3Parser.BlockContext):
        result =  self.visitChildren(ctx)
        result = f"{{\n{result}}}\n"
        
        return result

    def visitComparison(self, ctx:Python3Parser.ComparisonContext):
        left = self.visit(ctx.expr(0))

        if ctx.comp_op():
            operator = ctx.comp_op(0).getText()
        else:
            operator = ''

        right = self.visit(ctx.expr(1)) if ctx.expr(1) else ''  # Visit the right operand if it exists

        js_operator = self.comparison_operator_map.get(operator, operator)

        return f"{left} {js_operator} {right}" if operator else left

    def visitExpr(self, ctx:Python3Parser.ExprContext):
        if ctx.getChildCount() == 3:
            left = self.visit(ctx.expr(0))
            operator = ctx.getChild(1).getText()
            right = self.visit(ctx.expr(1))

            if operator == '**':
                return f"Math.pow({left}, {right})"

            if operator in self.arithmetic_operator_map:
                operator = self.arithmetic_operator_map[operator]

                return f"{left} {operator} {right}"
        
        return self.visitChildren(ctx)


    def visitAtom_expr(self, ctx:Python3Parser.Atom_exprContext):
        name = self.visit(ctx.atom())
        
        if name == 'print':
            trailer = ctx.trailer(0)
            
            if trailer.getChild(1).getText() == ')':
                return "console.log()"
            
            log_args = self.visit(trailer)
            
            if log_args.startswith('(') and log_args.endswith(')'):
                log_args = log_args[1:-1]
    
            return f"console.log({log_args})"
        
        if name == 'abs':
            return f"Math.abs{self.visit(ctx.trailer(0))}"
        
        if name == 'round':
            return f"Math.round{self.visit(ctx.trailer(0))}"
        
        return self.visitChildren(ctx)

    def get_nth_parent(self, ctx, n):
        parent = ctx
        for _ in range(n):
            parent = parent.parentCtx
            if not parent:
                break
            
        return parent

    def visitAtom(self, ctx:Python3Parser.AtomContext):
        from Python3Parser import Python3Parser
        text = ctx.getText()
        
        if text in self.param_type_map:
            return self.param_type_map.get(text, 'var')
        
        if text.startswith("'") and text.endswith("'"):
            return f'"{text[1:-1]}"'
        
        if ctx.name():
            name = self.visit(ctx.name())
            
            parent_argument = self.get_nth_parent(ctx, 8)
            parent_expr_stmt = self.get_nth_parent(ctx, 9)
            
            is_lhs_of_keyword_argument = None
            if isinstance(parent_argument, Python3Parser.ArgumentContext):
                is_keyword_argument = parent_argument.getChildCount() == 3 
                is_lhs_of_assignment = parent_argument.getChild(0) == self.get_nth_parent(ctx, 7)
                
                is_lhs_of_keyword_argument = (is_keyword_argument and is_lhs_of_assignment)
            
            is_being_assigned_to = None
            if isinstance(parent_expr_stmt, Python3Parser.Expr_stmtContext):
                is_being_assigned_to = isinstance(parent_expr_stmt.getChild(1), Python3Parser.AnnassignContext) or parent_expr_stmt.getChildCount() == 3
            
            if is_being_assigned_to or is_lhs_of_keyword_argument:
                return self.visitChildren(ctx)

            if not self.scopes.inScope(name):
                raise NameError(f"{name} does not exist in any scope")
            else:
                return self.visitChildren(ctx)
        
        return text

    def visitTrailer(self, ctx:Python3Parser.TrailerContext):
        
        if ctx.getChildCount() == 2:
            return ctx.getText()
        
        if ctx.getChildCount() == 3:
            if ctx.getChild(0).getText() == '(' and ctx.getChild(2).getText() == ')':
                return '(' + self.visit(ctx.getChild(1)) + ')'
        
        return self.visitChildren(ctx)

    def visitExprlist(self, ctx:Python3Parser.ExprlistContext):
        result = []
        for i in range(ctx.getChildCount()):
            result.append(ctx.getChild(i).getText())

        if result.count(','):
            result.remove(',')

        return result

    def visitArglist(self, ctx:Python3Parser.ArglistContext):
        result = ""
        
        num_of_args = ctx.getChildCount() - ctx.getChildCount() // 2 # Subtract commas
        for i in range(num_of_args):
            result += self.visit(ctx.argument(i))
            if i < num_of_args - 1:
                result += ", "
        
        return result


    def visitArgument(self, ctx:Python3Parser.ArgumentContext):
        if ctx.getChildCount() == 1:
            if ctx.getChild(0).getChildCount() == 1:
                arg_name = self.visit(ctx.getChild(0))
                return arg_name
        if ctx.getChildCount() == 3:
            arg_name = self.visit(ctx.getChild(0))
            arg_value = self.visit(ctx.getChild(2))
            
            return f"{arg_name}: {arg_value}"
        
        return self.visitChildren(ctx)
