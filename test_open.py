from solution import interpret_spartytalk

def test_test001(capsys):
    inp = """
    gogreen;
        nvar i = 1;
        while i <= 10 gogreen;
            spartysays i;
            i = i + 1;
        gowhite;
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""1
2
3
4
5
6
7
8
9
10
"""

def test_test002(capsys):
    inp = """
    gogreen;
        nvar i = 0;
        while i < 3 gogreen;
            nvar j = 0;
            while j < 3 gogreen;
                spartysays "i, j: " + i + ", " + j;
                j = j + 1;
            gowhite;
            i = i + 1;
        gowhite;
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""i, j: 0, 0
i, j: 0, 1
i, j: 0, 2
i, j: 1, 0
i, j: 1, 1
i, j: 1, 2
i, j: 2, 0
i, j: 2, 1
i, j: 2, 2
"""


def test_test003(capsys):
    inp = """
    gogreen;
        function foo(a) gogreen;
            spartysays a;
        gowhite;

        call foo(10);
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""10
"""


def test_test004(capsys):
    inp = """
    gogreen;
        function foo(a) gogreen;
            spartysays a;
        gowhite;

        nvar a = 3.14;
        call foo(a);
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""3.14
"""

def test_test005(capsys):
    inp = """
    gogreen;
        function foo(a) gogreen;
            nvar i = 0;
            while i < 3 gogreen;
                spartysays a;
                i = i + 1;
            gowhite;
        gowhite;

        nvar a = 7;
        call foo(a);
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""7
7
7
"""

def test_test006(capsys):
    inp = """
    gogreen;
        function foo(a, b) gogreen;
            spartysays a;
            spartysays b;
        gowhite;

        nvar a = 7;
        call foo(5, a);
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""5
7
"""

def test_test007(capsys):
    inp = """
    gogreen;
        function foo(a) gogreen;
            nvar b = a;
            b = b + 1;
            return b;
        gowhite;

        spartysays call foo(8);
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""9
"""

def test_test008(capsys):
    inp = """
    gogreen;
        function foo() gogreen;
            return "hi";
        gowhite;

        spartysays call foo();
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""hi
"""

def test_test009(capsys):
    inp = """
    gogreen;
        function foo() gogreen;
            spartysays "I am here.";
        gowhite;

        function bar() gogreen;
            spartysays "Where am I?";
            call foo();
        gowhite;

        call bar();
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""Where am I?
I am here.
"""

def test_test010(capsys):
    inp = """
    gogreen;
        function foo() gogreen;
            spartysays "I am here.";
        gowhite;

        nvar i = 0;
        while i < 5 gogreen;
            call foo();
            i = i + 1;
        gowhite;
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""I am here.
I am here.
I am here.
I am here.
I am here.
"""


def test_test011(capsys):
    inp = """
    gogreen;
        function foo() gogreen;
            return "hello";
        gowhite;

        svar s = call foo();
        spartysays s;
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""hello
"""

def test_test012(capsys):
    inp = """
    gogreen;
        function foo() gogreen;
            return "hello";
        gowhite;

        function bar() gogreen;
            return "world";
        gowhite;

        svar s = call foo() + " " + call bar();
        spartysays s;
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""hello world
"""


def test_test013(capsys):
    inp = """
    gogreen;
        function foo(a, b) gogreen;
            return a + " " + b;
        gowhite;

        spartysays call foo("hello", "world");
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""hello world
"""


def test_test014(capsys):
    inp = """
    gogreen;
        function bar(c) gogreen;
            return c;
        gowhite;
        
        function foo(a, b) gogreen;
            return a + " " + call bar(b);
        gowhite;

        spartysays call foo("hello", "world");
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""hello world
"""

def test_test015(capsys):
    inp = """
    gogreen;    
        function foo(a) gogreen;
            spartysays a;
        gowhite;

        call foo("a"+"b");
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""ab
"""


def test_test016(capsys):
    inp = """
    gogreen;    
        function foo(a) gogreen;
            return a;
        gowhite;

        nvar v1 = 1;
        nvar v2 = 2;
        nvar v3 = v1 + v2;
        nvar v4 = call foo(v3);
        v4 = v4 + 1;
        spartysays v4;
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""4
"""


def test_test017(capsys):
    inp = """
    gogreen;    
        function foo(a, b) gogreen;
            nvar n1 = a;
            nvar n2 = b;
            nvar sum = n1 + n2;
            return sum;
        gowhite;

        spartysays call foo(7, 5);
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""12
"""


def test_test018(capsys):
    inp = """
    gogreen;
        function bar() gogreen;
            return "hello";
        gowhite;

        function foo(a, b) gogreen;
            return a + b;
        gowhite;

        spartysays call foo(call bar(), call bar());
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""hellohello
"""

def test_test019(capsys):
    inp = """
    gogreen;
        function bar() gogreen;
            return "hello";
        gowhite;

        function foo() gogreen;
            nvar count = 5;
            svar sbuilder = "";
            while count != 0 gogreen;
                sbuilder = sbuilder + call bar();
                count = count - 1;
            gowhite;

            return sbuilder;
        gowhite;

        spartysays call foo();
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""hellohellohellohellohello
"""

def test_test020(capsys):
    inp = """
    gogreen;
        function bar() gogreen; return "hello"; gowhite;
        function foo() gogreen;
            nvar count = 5;
            svar sbuilder = "";
            while count != 0 gogreen; sbuilder = sbuilder + call bar();
                count = count - 1; gowhite;
            return sbuilder; gowhite;
        spartysays call foo();
    gowhite;
    """

    interpret_spartytalk(inp)

    captured = capsys.readouterr()

    assert captured.out == r"""hellohellohellohellohello
"""