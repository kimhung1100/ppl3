import unittest
from TestUtils import TestChecker
from AST import *
from Visitor import Visitor
from StaticError import *
from abc import ABC

class CheckerSuite(unittest.TestCase):
    def test_400(self):
        input = Program([VarDecl("a", IntegerType(), IntegerLit(5)), VarDecl("c", AutoType())])
  
        # expect = """main: function void () {
        #     a: integer = 65; 
        #     a = a + b;
        # }"""
        expect = "Invalid Variable: c"
        self.assertTrue(TestChecker.test(input, expect, 400))
        
    def test_401(self):
        input = Program([FuncDecl("main", VoidType(), [], None, BlockStmt([VarDecl("a", IntegerType(), IntegerLit(65)), AssignStmt(Id("a"), BinExpr("+", Id("a"), Id("b")))]))])    
        # expect = """main: function void () {
        #     a: integer = 65; 
        #     a = a + b;
        # }"""
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input, expect, 401))
        
    def test_402(self):
        """Test basicUndeclared_Identifier_Param"""
        input = Program([FuncDecl("bds", IntegerType(), [], None, BlockStmt([ReturnStmt(Id("a"))])),FuncDecl("main", VoidType(), [], None, BlockStmt([]))])
        #  """
        #     bds: function integer () {
        #         return a; 
        #     }
        #     main: function void () {
        # }"""

        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 402))
    
    
    def test_403(self):
        """Test basicUndeclared_Function"""
        input = Program([FuncDecl("main", VoidType(), [], None, BlockStmt([CallStmt("helloWorld",[])]))])
        expect = "Undeclared Function: helloWorld"
# main: function void () {
#                 helloWorld(); 
#         }
        self.assertTrue(TestChecker.test(input, expect, 403))
        
    
    def test_inheritFunc(self):
        input = """
        foo: function integer (inherit a: integer, b: integer){
            a = a + b;
        }
        bar: function integer (c: integer) inherit foo {
            super(2, 3);
            c = a + b;
            }
        main: function void () {
        }"""
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input, expect, 404))
    
    def test_TypeMismatchInSTMT_for1(self):
        """test_TypeMismatchInBinExp_REMAINDER""" 
        # OPERAND TYPE: INT
        input = """
            foo: function integer (inherit a: integer) {
            }
            bar: function integer (c: integer) inherit foo {
                super(2);
            }
            """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 405))
    
    def test_406(self):
        """test_TypeMismatchInBinExp_REMAINDER""" 
        # OPERAND TYPE: INT
        input = """
            main: function void () {
                x, y, z: integer = 1, 2, 3;
                a, b: float;
                c = 1.0;
            }
            """
        expect = "Undeclared Identifier: c"
        self.assertTrue(TestChecker.test(input, expect, 406))
    
    def test_407(self):
        """test_TypeMismatchInBinExp_REMAINDER""" 
        # OPERAND TYPE: INT
        input = """
            a, b: integer;
            foo: function void () {
                x, y, z: integer = 1, 2, 3;
                a, b: float;
            }
            """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 407))
    
    def test_408(self):
        """test_TypeMismatchInBinExp_REMAINDER""" 
        # OPERAND TYPE: INT
        input = """
                    a: array[2] of integer = {1, 2}
            """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 408))
    
     
    def test_409(self):
        """test_TypeMismatchInBinExp_REMAINDER""" 
        # OPERAND TYPE: INT
        input = """
        bar: function integer (inherit a: integer) {
            a = a;
        }
        foo: function integer (a: integer) inherit bar {
            preventDefault();
        }
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 409))
    
    
    def test_410(self):
        """test loop""" 
        # OPERAND TYPE: INT
        input = """x: integer = 65;
        fact: function integer (n: integer) {
            if (n == 0) return 1;
            else return n * fact(n - 1);
        }
        inc: function void(out n: integer, delta: integer) {
            n = n + delta;
        }
        main: function void() {
            delta: integer = fact(3);
            inc(x, delta);
            printInteger(x);
            return 3;
        }"""
        expect = "Type mismatch in statement: ReturnStmt(IntegerLit(3))"
        self.assertTrue(TestChecker.test(input, expect, 410))
        
    def test_411(self):
        input = """
            goo: function float(a: float, b: boolean){}
            foo: function float(){
                i : integer;
                for (i = 2, i<10, i+1){
                    continue;
                }
                continue;
            }
            main: function void(){}
        """
       
        expect = "Must in loop: ContinueStmt()"

        self.assertTrue(TestChecker.test(input, expect, 411))

    def test_412(self):
        input = """
            goo: function float(a: float, b: boolean){}
            foo: function float(){
                i : integer;
                while (i<2) {break;}
                continue;
            }
            main: function void(){}
        """
        expect = "Must in loop: ContinueStmt()"

        self.assertTrue(TestChecker.test(input, expect, 412))
        
    def test_413(self):
        """nested loop break"""
        input = """
            main: function void() {
                i: integer;
                for (i = 1, i<10, i+3){
                    for (i = 1, i<10, i+3){
                        break;
                    }
                    break;
                }
                return 3;
            }
        """
        expect = "Type mismatch in statement: ReturnStmt(IntegerLit(3))"

        self.assertTrue(TestChecker.test(input, expect, 413))
        
    def test_414(self):
        """nested loop break"""
        input = """
            main: function void() {
                i: integer;
                for (i = 1, i<10, i+3){
                    for (i = 1, i<10, i+3){
                        break;
                    }
                    break;
                }
                break;
                return 3;
            }
        """
        expect = "Must in loop: BreakStmt()"

        self.assertTrue(TestChecker.test(input, expect, 414))
        
    def test_415(self):
        input = """
        main: function integer (inherit x: auto){
            y: float;
        }
        foo: function void(x:auto) inherit main{
            preventDefault();
            m: auto = main(1);
            {
                x: integer;
                z: integer;
            }
            if (1 > 2) m = 2; 
            else 
            {
                i: integer;
                for (i = 0, i < 5, i + 1)
                {
                    x: float;
                    return;
                }
            }
        }
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 415))
        
    def test_416(self):
        input = """
        main: function integer (inherit x: auto) inherit main2{
            preventDefault();
            y: float;
        }
        d: array[4] of float = {1,2,3,4};
        n: float = 1 + 2.1;
        foo1: auto = 5;
        foo: function void(x:auto) inherit main{
            preventDefault();
            m: auto = main(1);
            {
                x: integer;
                z: integer;
            }
            if (1 > 2) m = 2; 
            else 
            {
                i: integer;
                for (i = 0, i < 5, i + 1)
                {
                    x: float;
                    return;
                }
            }
        }
        """
        expect = "Undeclared Function: main2"
        self.assertTrue(TestChecker.test(input, expect, 416))
        
    
    def test_417(self):
        input = """
        d: array[4] of float = {1,2,3,4};
        n: float = 1 + 2.1;
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 417))
    
    def test_418(self):
        input = """
        d: array[4] of float = {1,2,3.2,4};
        n: float = 1 + 2.1;
        """
        expect = "Illegal array literal: ArrayLit([IntegerLit(1), IntegerLit(2), FloatLit(3.2), IntegerLit(4)])"
        self.assertTrue(TestChecker.test(input, expect, 418))
        
    def test_419(self):
        input = """
        d: array[5] of float = {1,2,3,4};
        n: float = 1 + 2.1;
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(d, ArrayType([5], FloatType), ArrayLit([IntegerLit(1), IntegerLit(2), IntegerLit(3), IntegerLit(4)]))"
        self.assertTrue(TestChecker.test(input, expect, 419))
        
    def test_420(self):
        input = """
        main: function void() {
            i: integer;
            for (i = 1, i<10, i+3){
                printInteger(i);
                break;
            }
        }
        a: array [2,2] of integer = {{1,2}};
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(a, ArrayType([2, 2], IntegerType), ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)])]))"
        self.assertTrue(TestChecker.test(input, expect, 420))
    
    def test_421(self):
        """boolean array cell"""
        input = """
        main: function void() {
            i: integer;
            for (i = 1, i<10, i+3){
                printInteger(i);
                break;
            }
            x: array[2] of integer = {1,2};
            y: auto = x[2<3];
        }
        
        """
        expect = "Type mismatch in expression: BinExpr(<, IntegerLit(2), IntegerLit(3))"
        self.assertTrue(TestChecker.test(input, expect, 421))
        
    def test_422(self):
        """ redundant array cell dimension"""
        input = """
        main: function void() {
            i: integer;
            for (i = 1, i<10, i+3){
                printInteger(i);
                break;
            }
            x: array[2] of integer = {1,2};
            y: auto = x[2,3];
        }
        
        """
        expect = "Type mismatch in expression: ArrayCell(x, [IntegerLit(2), IntegerLit(3)])"
        self.assertTrue(TestChecker.test(input, expect, 422))
    
    def test_423(self):
        """array cell of id not a array"""
        input = """
        main: function void() {
            i: integer;
            for (i = 1, i<10, i+3){
                printInteger(i);
                break;
            }
            x: array[2] of integer = {1,2};
            y: auto = i[2];
        }
        
        """
        expect = "Type mismatch in expression: ArrayCell(i, [IntegerLit(2)])"
        self.assertTrue(TestChecker.test(input, expect, 423))
    
    def test_424(self):
        """id array cell is not found"""
        input = """
        main: function void() {
            x: array[2] of integer = {1,2};
            y: auto = i[2];
        }
        
        """
        expect = "Undeclared Identifier: i"
        self.assertTrue(TestChecker.test(input, expect, 424))
    
    def test_425(self):
        """id array cell is not a arraytype"""
        input = """
        main: function void() {
            i: integer;
            for (i = 1, i<10, i+3){
                printInteger(i);
                break;
            }
            x: array[2] of integer = {1,2};
            y: auto = i[2];
        }
        
        """
        expect = "Type mismatch in expression: ArrayCell(i, [IntegerLit(2)])"
        self.assertTrue(TestChecker.test(input, expect, 425))
        
    def test_426(self):
        """id array cell is not a arraytype"""
        input = """
        main: function void() {
            i: integer;
            while (i < 10) {
                break;
                }
                break;
        }
        
        """
        expect = "Must in loop: BreakStmt()"
        self.assertTrue(TestChecker.test(input, expect, 426))
        
    def test_427(self):
        """id array cell is not a arraytype"""
        input = """
        main: function void() {
            i: integer;
            while (i < 10) {
                break;
                break;
                }
            i = 1&&1;
        }
        
        """
        expect = "Type mismatch in expression: BinExpr(&&, IntegerLit(1), IntegerLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 427))
        
    def test_428(self):
        """id array cell is not a arraytype"""
        input = """
        main: function void() {
            i: integer;
            while (i < 10) {
                break;
                break;
                }
            i = 1&&1;
        }
        
        """
        expect = "Type mismatch in expression: BinExpr(&&, IntegerLit(1), IntegerLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 428))
        
    def test_429(self):
        """id array cell is not a arraytype"""
        input = """
        main: function void() {
            i: integer;
            while (i == 10) {
                break;
                break;
                }
            i = 1&&1;
        }
        
        """
        expect = "Type mismatch in expression: BinExpr(&&, IntegerLit(1), IntegerLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 429))
        
    def test_430(self):
        input = """
        main: function void() {
            i: integer;
            i = i + foo();
            a: integer = foo();
            i = z;
        }
        foo: function auto() {
            }
        
        """
        expect = "Undeclared Identifier: z"
        self.assertTrue(TestChecker.test(input, expect, 430))
        
    def test_431(self):
        """infer parameter"""
        input = """
        main: function void() {
            i: integer;
            i = i + foo();
            a: integer = foo();
            fl: float = bar(foo());
            fl = bar("error here");
        }
        foo: function auto() {
            }
        bar: function float (z: auto){
            
        }
        
        """
        expect = "Type mismatch in expression: FuncCall(bar, [StringLit(error here)])"
        self.assertTrue(TestChecker.test(input, expect, 431))
    
    def test_432(self):
        input = """
        main: function void() {
            foo();
            a: integer = foo() + 1;
            z: string = foo();
        }
        foo: function auto() {
            }
        
        
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(z, StringType, FuncCall(foo, []))"
        self.assertTrue(TestChecker.test(input, expect, 432))
        
    def test_463(self):
        input = """
        x: array[2] of integer = {1,2};
        main: function integer () {
            a: integer;
            a = x/a;
        }
        a: auto = main();
        """
        expect = "Type mismatch in expression: BinExpr(/, Id(x), Id(a))"
        self.assertTrue(TestChecker.test(input, expect, 463))
    def test_464(self):
        input = """
        x: array[2] of integer = {1,2};
        main: function integer () {
            b: float;
            a: integer;
            a = x%b;
        }
        a: auto = main();
        """
        expect = "Type mismatch in expression: BinExpr(%, Id(x), Id(b))"
        self.assertTrue(TestChecker.test(input, expect, 464))
        
    def test_465(self):
        input = """
        main: function integer () {
            b: float;
            a: integer;
            a = a%b;
        }
        a: auto = main();
        """
        expect = "Type mismatch in expression: BinExpr(%, Id(a), Id(b))"
        self.assertTrue(TestChecker.test(input, expect, 465))
    def test_466(self):
        input = """
        
        main: function integer () {
            b: string;
            b = 1 :: "2asc";
        }
        a: auto = main();
        """
        expect = "Type mismatch in expression: BinExpr(::, IntegerLit(1), StringLit(2asc))"
        self.assertTrue(TestChecker.test(input, expect, 466))
        
    def test_467(self):
        input = """
        main: function integer () {
            
        }
        a: auto = main();
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 467))
        
    def test_468(self):
        input = """
        main: function void() {
            a: array [1,2] of integer = {{1,2,"3"}};

        }
        """
        expect = "Illegal array literal: ArrayLit([IntegerLit(1), IntegerLit(2), StringLit(3)])"
        self.assertTrue(TestChecker.test(input, expect, 468))
    def test_469(self):
        input = """
        main: function void() {
            
        }
        a: array [1,2] of integer = {{1,2}};
        b: array [1] of integer = a[1,2,3];
        """
        expect = "Type mismatch in expression: ArrayCell(a, [IntegerLit(1), IntegerLit(2), IntegerLit(3)])"
        self.assertTrue(TestChecker.test(input, expect, 469))
        
    def test_470(self):
        input = """
        main: function auto() {
            i: integer;
            for (i = 1, i<10, i+3){
                break;
            }
        }
        a: array [1,2] of integer = {{1,2}};
        b: array [1] of integer = {main()};
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 470))
        
    def test_471(self):
        input = """
        main: function void() {
            i: integer;
            for (i = 1, i<10, i+3){
                break;
            }
        }
        a: array [1,1] of integer = {{1}};
        b: array [1] of integer = a[0] + 1;
        """
        expect = "Type mismatch in expression: ArrayCell(a, [IntegerLit(0)])"
        self.assertTrue(TestChecker.test(input, expect, 471))
        
    def test_472(self):
        input = """
        main: function void() {
            i: integer;
            for (i = 1, i<10, i+3){
                break;
            }
        }
        a: array [1,1] of integer = {{1}};
        b: integer = a[0,0] + 2;
        main: integer = 1;
        """
        expect = "Redeclared Variable: main"
        self.assertTrue(TestChecker.test(input, expect, 472))
        
    def test_473(self):
        input = """
        main: function void() {
            i: integer;
            for (i = 1, i<10, i+3){
                printInteger(i);
                break;
            }
        }
        a: array [1,1] of integer = {{1}};
        b: array [1] of integer = { a[0, 0] + 3.5 };
        main: integer = 1;
        """
        expect = "Redeclared Variable: main"
        self.assertTrue(TestChecker.test(input, expect, 473))
    
    def test_474(self):
        input = """
        main: function void() {
            
        }
        a: array [1,2] of integer = {{1,2}};
        main: integer = 1;
        """
        expect = "Redeclared Variable: main"
        self.assertTrue(TestChecker.test(input, expect, 474))
        
    def test_475(self):
        input = """
                    x: array[4] of integer = foo(10);
                    foo: function array[4] of integer (n: float) {
                        return {n, n+1, n+2, n+3};
                    }
                        
                """
        expect = """Type mismatch in expression: FuncCall(foo, [IntegerLit(10)])"""
        self.assertTrue(TestChecker.test(input, expect, 475))
        
    def test_476(self):
        input = """
                    main: function void() {
                        b : float = 3.5;
                        x: array [2, 3, 2] of integer = {{{1, 2}, {1, 2}}, {{1, 2}, {1, "2"}, {1, 2}}};
                    }
                        
                """
        expect = """Illegal array literal: ArrayLit([IntegerLit(1), StringLit(2)])"""
        self.assertTrue(TestChecker.test(input, expect, 476))
    
    def test_477(self):
        input = """
                    x: array[4] of integer = foo(10);
                    foo: function array[2, 2] of integer (n: integer) {
                        return {n, n+1, n+2, n+3};
                    }
                        
                """
        expect = """Type mismatch in Variable Declaration: VarDecl(x, ArrayType([4], IntegerType), FuncCall(foo, [IntegerLit(10)]))"""
        self.assertTrue(TestChecker.test(input, expect, 477))
    
    def test_478(self):
        input = """
                    x: array[4] of integer = foo(10);
                    foo: function array[4] of integer (n: integer) {
                        return {n, n+1, n+2, n+3};
                    }
                        
                """
        expect = """No entry point"""
        self.assertTrue(TestChecker.test(input, expect, 478))
        
    def test_479(self):
        input = """
                    c: array[2,2] of integer = { {1,2.0}, {2,1} };
                """
        expect = """Illegal array literal: ArrayLit([IntegerLit(1), FloatLit(2.0)])"""
        self.assertTrue(TestChecker.test(input, expect, 479))
    
    def test_480(self):
        input = """
                    a: array[2,2] of integer = { {1,3}, {1,4} };
                    c: array[2,2] of integer = { {1,2}, {2,1} };
                    d: integer = 3;
                    b: integer = a[d];
                """
        expect = """Type mismatch in expression: ArrayCell(a, [Id(d)])"""
        self.assertTrue(TestChecker.test(input, expect, 480))
    
    def test_481(self):
        """khong suy dien khi duyet ham, goi ham lan dau moi suy dien"""
        input = """
        test1 : function string(y : auto) {
            y = 2; // line 2
            return "abc";
        }
        main: function void () {
            test1(true); // line 6
            test1(1);
        }
        """
        expect = "Type mismatch in statement: CallStmt(test1, IntegerLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 481))
    
    def test_482(self):
        input = """
        main: function void(){
            printInteger(a);
        }
        """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 482))
    
    def test_483(self):
        input = """
        main: function void(){
            printInteger(a);
        }
        a: integer = 1;
        """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input, expect, 483))

    def test_484(self):
        input = """
        foo: function integer(){
            
        }
        main: function void(){
            foo: integer = 3;
            a: integer;
            a = foo(); // line 5
        }
        """
        expect = "Type mismatch in expression: FuncCall(foo, [])"
        self.assertTrue(TestChecker.test(input, expect, 484))
        
    def test_485(self):
        input = """
        main: function void() {
            
        }
        foo: function auto (x: integer, y: float){
            writeFloat(main());
        }
        
        
        """
        expect = "Type mismatch in statement: CallStmt(writeFloat, FuncCall(main, []))"
        self.assertTrue(TestChecker.test(input, expect, 485))
        
    def test_486(self):
        input = """
        main: function void() {
            a: array[2,3] of integer = foo(1,2.0);
        }
        foo: function auto (x: integer, y: float){
            writeFloat(main());
        }
        
        
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(a, ArrayType([2, 3], IntegerType), FuncCall(foo, [IntegerLit(1), FloatLit(2.0)]))"
        self.assertTrue(TestChecker.test(input, expect, 486))
        
    def test_487(self):
        """test_TypeMismatchInBinExp_REMAINDER""" 
        # OPERAND TYPE: INT
        input = """
        foo: function integer (a: integer) inherit bar {
            super(1, 2);
            a = b;
        }
        bar: function integer (inherit a: integer, a: integer) {
            a = a;
        }
        """
        expect = "Invalid Parameter: a"
        self.assertTrue(TestChecker.test(input, expect, 487))
        
    def test_488(self):
        """test_TypeMismatchInBinExp_REMAINDER""" 
        # OPERAND TYPE: INT
        input = """
        foo: function integer (a: integer) inherit bar {
            super(1, 2);
            a = b;
        }
        bar: function integer (inherit b: integer, c: auto) {
            
            c = b + 100;
        }
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 488))
        
    def test_489(self):
        """test_TypeMismatchInBinExp_REMAINDER""" 
        # OPERAND TYPE: INT
        input = """
        foo: function integer (a: integer) inherit bar {
            preventDefault();
            a = b;
        }
        bar: function integer (inherit a: integer, a: integer) {
            a = a;
        }
        """
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input, expect, 489))
    
    def test_490(self):
        """test_TypeMismatchInBinExp_REMAINDER""" 
        # OPERAND TYPE: INT
        input = """
        foo: function integer (a: integer) inherit bar {
            preventDefault();
        }
        bar: function integer (inherit a: integer, a: integer) {
            a = a;
        }
        """
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input, expect, 490))
    
    def test_491(self):
        """break """ 
        # OPERAND TYPE: INT
        input = """
        fact: function integer () {
            i: integer;
            do{
                return 1;
            }
            while(i<10);
            return "error";
        }
        """
        expect = "Type mismatch in statement: ReturnStmt(StringLit(error))"
        self.assertTrue(TestChecker.test(input, expect, 491))
        
    def test_492(self):
        """break """ 
        # OPERAND TYPE: INT
        input = """
        fact: function integer () {
            i: integer;
            while(i<10) 
                return 1;
            return "error";
        }
        """
        expect = "Type mismatch in statement: ReturnStmt(StringLit(error))"
        self.assertTrue(TestChecker.test(input, expect, 492))
    
    def test_493(self):
        """break """ 
        # OPERAND TYPE: INT
        input = """
        fact: function integer () {
            if (1<2) {
                return 1;
                return "not error 1";
            } 
            return "error";
        }
        """
        expect = "Type mismatch in statement: ReturnStmt(StringLit(error))"
        self.assertTrue(TestChecker.test(input, expect, 493))
        
    def test_494(self):
        """break """ 
        # OPERAND TYPE: INT
        input = """
        fact: function auto (n: integer) {
            i: integer;
            for (i = 1, i<10, i+3){
                writeFloat(i);
                    for (i = 1, i<10, i+3){
                        writeFloat(i);
                        break;
                }
                break;
            }
        }
        """
        expect = "Type mismatch in statement: CallStmt(writeFloat, Id(i))"
        self.assertTrue(TestChecker.test(input, expect, 494))
        
    def test_495(self):
        """test call stmt, infer type""" 
        # OPERAND TYPE: INT
        input = """
        fact: function integer (n: integer) {
            if (n == 0) return 1;
            else return "hello";
        }
        """
        expect = "Type mismatch in statement: ReturnStmt(StringLit(hello))"
        self.assertTrue(TestChecker.test(input, expect, 495))
    
    def test_496(self):
        """test call stmt, infer type""" 
        # OPERAND TYPE: INT
        input = """
        foo: function integer (a: integer) {
            bar(1);
        }
        bar: function integer (a: auto) {
            b: integer = foo(1) + a;
        }
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 496))
        
    def test_497(self):
        """test call stmt, type not match""" 
        # OPERAND TYPE: INT
        input = """
        foo: function integer (a: integer) {
            bar(1);
        }
        bar: function integer (a: string) {
            a = a;
        }
        """
        expect = "Type mismatch in statement: CallStmt(bar, IntegerLit(1))"
        self.assertTrue(TestChecker.test(input, expect, 497))
    
    def test_498(self):
        """test call stmt""" 
        # OPERAND TYPE: INT
        input = """
        foo: function integer (a: integer) {
            bar(1);
        }
        bar: function integer (a: integer) {
            a = a;
        }
        """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input, expect, 498))
        
    def test_499(self):
        """test invalid parameter""" 
        # OPERAND TYPE: INT
        input = """
        foo: function integer (a: integer) inherit bar {
            super(1);
            a = a + 1;
        }
        bar: function integer (inherit a: integer) {
            a = a;
        }
        """
        expect = "Invalid Parameter: a"
        self.assertTrue(TestChecker.test(input, expect, 499))
        
    