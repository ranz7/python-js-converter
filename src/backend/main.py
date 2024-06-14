import sys
from antlr4 import *
from Python3Lexer import Python3Lexer
from Python3Parser import Python3Parser
from Python3ParserVisitor import Python3ParserVisitor

def main(input: int) -> int:
    if input.endswith('.py'):
        input_code = ''''''
        with open(input, 'r') as f:
            input_code = f.read()
            
    else:
        input_code = input

    input_stream = InputStream(input_code)
    lexer = Python3Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Python3Parser(stream)
    
    tree = parser.file_input()

    visitor = Python3ParserVisitor()
    output_code = visitor.visit(tree)

    with open('output.js', 'w') as f:
        f.write(output_code)

    return output_code

if __name__ == "__main__":
    main(sys.argv[1])