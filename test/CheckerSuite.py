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
        
        
    