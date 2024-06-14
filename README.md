# Compiler Python to JavaScript


## Description

**Objectives:**

This project aims to develop a compiler that automatically converts source code written in Python to its equivalent in JavaScript. This conversion process leverages ANTLR4, a powerful parser generator, along with a custom-designed grammar to facilitate the translation between these two programming languages.

**Technologies and Tools:**
- **ANTLR4:** A tool for generating parsers from formal grammars, used to create a Python parser and a JavaScript code generator.
- **Python:** The programming language from which the source code will be converted.
- **JavaScript:** The target programming language for the conversion.
- **Custom ANTLR Grammar:** A specialized grammar designed to recognize Python syntax and generate corresponding JavaScript code.

**Implementation Stages:**

1. **Analysis of Python Grammar:**
   - Identify and analyze the key syntactic structures in Python (e.g., control statements, expressions, functions, classes).
   - Determine the essential elements of Python grammar necessary for accurate conversion.

2. **Creating ANTLR Grammar for Python:**
   - Develop a grammar in ANTLR4 that precisely describes Python’s syntax.
   - Test the grammar against various Python code samples to ensure it correctly parses diverse language constructs.

3. **Implementation of the Python Parser:**
   - Use ANTLR4 to generate a parser from the developed grammar.
   - Implement mechanisms for error handling and exceptions during the parsing of Python code.

4. **Development of Output Grammar for JavaScript:**
   - Create a set of rules that define how each Python syntactic element should be transformed into JavaScript.
   - Account for differences in language paradigms, such as variable scoping, data types, and asynchronous programming between Python and JavaScript.

5. **Implementation of Code Generator:**
   - Extend the Python parser with a module to generate JavaScript code.
   - Implement conversion algorithms for transforming Python constructs into their JavaScript equivalents.

6. **Testing and Validation:**
   - Convert sample Python projects to JavaScript.
   - Validate the generated JavaScript code by running it in a JavaScript environment, ensuring functional equivalence with the original Python code.

7. **GUI:**
   - Create user interface, that consists of place for Python code and place for generated Javascript equivalent. User can also compile converted code and see results of his program.


## Get started
**Prerequisites**
- JDK
- ANTLR4
- Python and PIP
- JavaScript

**Installation**
- https://github.com/antlr/antlr4/blob/master/doc/getting-started.md


## Example
![Zrzut ekranu 2024-06-14 134646](https://github.com/ranz7/python-js-converter/assets/115559396/1373c11f-87db-4b80-ba1b-9834bdcd86b1)



