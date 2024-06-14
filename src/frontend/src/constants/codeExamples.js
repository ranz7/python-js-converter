export const codeExamples = [
    {
      exampleId: 1,
      exampleName: "+ Simple Hello World",
      codeContent: "print(\"Hello, world!\")",
    },
    {
      exampleId: 2,
      exampleName: "+ Variable Declaration and Usage",
      codeContent: "x = 10\ny = 5\nresult = x + y\nprint(\"The result is:\", result)",
    },
    {
      exampleId: 19,
      exampleName: "+ Sum of List Recursive Function",
      codeContent: "def sum_list(lst):\n    if not lst:\n        return 0\n    else:\n        return lst[0] + sum_list(lst[1:])\n\nprint(sum_list([1, 2, 3, 4, 5]))"
    },
    {
      exampleId: 3,
      exampleName: "+ For Loop",
      codeContent: "for i in range(5):\n    print(i)"
    },
    {
      exampleId: 6,
      exampleName: "+ While Loop",
      codeContent: "i = 0\nwhile i < 5:\n    print(i)\n    i += 1"
    },
    {
      exampleId: 9,
      exampleName: "+ 2D List Iteration",
      codeContent: "m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nfor row in m:\n    for e in row:\n        print(e)"
    },
    {
      exampleId: 13,
      exampleName: "+ Initialize 2D List",
      codeContent: "m = [[0] * 3 for _ in range(3)]\nprint(m)"
    },
    {
      exampleId: 15,
      exampleName: "+ Simple Recursive Function",
      codeContent: "def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n - 1)\n\nprint(factorial(5))"
    },
    {
      exampleId: 17,
      exampleName: "+ Fibonacci Recursive Function",
      codeContent: "def fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n        return fibonacci(n - 1) + fibonacci(n - 2)\n\nprint(fibonacci(6))"
    },
    {
      exampleId: 100,
      exampleName: "+ Mix",
      codeContent: "def sum_list(l):\n    sum = 0\n    for x in l:\n        sum += x\n\n    return sum\n\n\ndef factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n - 1)\n\n\ndef fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n        return fibonacci(n - 1) + fibonacci(n - 2)\nprint(\"Hello, world!\")\n\nx = 10\ny = 5\nresult = x + y\nprint(\"The result is:\", result)\n\n\n\nprint(sum_list([1, 2, 3, 4, 5]))\n\nfor i in range(5):\n    print(i)\n\ni = 0\nwhile i < 5:\n    print(i)\n    i += 1\n\nm = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nfor r in m:\n    for e in r:\n        print(e)\n\nprint(factorial(5))\n\n\nprint(fibonacci(6))\n"
    },
    {
      exampleId: 4,
      exampleName: "- For Loop; missing )",
      codeContent: "for i in range(5:\n    print(i)"
    },
    {
      exampleId: 5,
      exampleName: "- For Loop; variable mismatch",
      codeContent: "for i in range(5):\n    print(j)"
    },
    {
      exampleId: 7,
      exampleName: "- While Loop; missing declaration",
      codeContent: "while i < 5:\n    print(i)"
    },
    {
      exampleId: 8,
      exampleName: "- While Loop; missing argument block",
      codeContent: "i = 0\nwhile :\n    i -= 1\n    print(i)"
    },
    {
      exampleId: 10,
      exampleName: "- 2D List Iteration; missing inner loop",
      codeContent: "m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]\nfor row in m:\n    print(e)"
    },
    {
      exampleId: 14,
      exampleName: "- Initialize 2D List; syntax error",
      codeContent: "m = [[0] * 3 for _ in range(3)\nprint(m)"
    },
    {
      exampleId: 16,
      exampleName: "- Simple Recursive Function; missing base case",
      codeContent: "def factorial(n):\n    return n * factorial(n - 1)\n\nprint(factorial(5))"
    },
    {
      exampleId: 18,
      exampleName: "- Fibonacci Recursive Function; wrong base case",
      codeContent: "def fibonacci(n):\n    if n == 1:\n        return n\n    else:\n        return fibonacci(n - 1) + fibonacci(n - 2)\n\nprint(fibonacci(6))"
    },
    {
      exampleId: 20,
      exampleName: "- Sum of List Recursive Function; wrong slicing",
      codeContent: "def sum_list(lst):\n    if not lst:\n        return 0\n    else:\n        return lst[0] + sum_list(lst)\n\nprint(sum_list([1, 2, 3, 4, 5]))"
    }
  ];
  