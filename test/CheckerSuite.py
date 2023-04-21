import unittest
from TestUtils import TestChecker
from AST import *
from Visitor import Visitor
from StaticError import *
from abc import ABC

class CheckerSuite(unittest.TestCase):
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
        
    # ----------------------------------------------------------------------
    # test array 
    # ----------------------------------------------------------------------
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
                writeFloat(i);
                break;
            }
        }
        a: array [1,2] of integer = {{1,2}};
        """
        expect = "Type mismatch in Variable Declaration: VarDecl(a, ArrayType([1, 2], IntegerType), ArrayLit([ArrayLit([IntegerLit(1), IntegerLit(2)])]))"
        self.assertTrue(TestChecker.test(input, expect, 420))
        
    