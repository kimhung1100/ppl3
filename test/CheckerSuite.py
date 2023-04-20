import unittest
from TestUtils import TestChecker
from AST import *
from Visitor import Visitor
from StaticError import *
from abc import ABC

class CheckerSuite(unittest.TestCase):
    # def test_basicUndeclared_Identifier(self):
    #     input = Program([FuncDecl("main", VoidType(), [], None, BlockStmt([VarDecl("a", IntegerType(), IntegerLit(65)), AssignStmt(Id("a"), BinExpr("+", Id("a"), Id("b")))]))])    
    #     # expect = """main: function void () {
    #     #     a: integer = 65; 
    #     #     a = a + b;
    #     # }"""
    #     expect = "Undeclared Identifier: b"
    #     self.assertTrue(TestChecker.test(input, expect, 401))
        
    # def test_basicUndeclared_Identifier_Param(self):
    #     """Test basicUndeclared_Identifier_Param"""
    #     input = Program([FuncDecl("bds", IntegerType(), [], None, BlockStmt([ReturnStmt(Id("a"))])),FuncDecl("main", VoidType(), [], None, BlockStmt([]))])
    #     #  """
    #     #     bds: function integer () {
    #     #         return a; 
    #     #     }
    #     #     main: function void () {
    #     # }"""

    #     expect = "Undeclared Identifier: a"
    #     self.assertTrue(TestChecker.test(input, expect, 402))
    
    
#     def test_basicCallStmt(self):
#         """Test basicUndeclared_Function"""
#         input = Program([FuncDecl("main", VoidType(), [], None, BlockStmt([CallStmt("helloWorld",[])]))])
#         expect = "Undeclared Function: helloWorld"
# # main: function void () {
# #                 helloWorld(); 
# #         }
#         self.assertTrue(TestChecker.test(input, expect, 403))
        
    
    # def test_inheritFunc(self):
    #     input = """
    #     foo: function integer (inherit a: integer, b: integer){
    #         a = a + b;
    #     }
    #     bar: function integer (c: integer) inherit foo {
    #         c = a + b;
    #         }
    #     main: function void () {
    #     }"""
    #     expect = "Undeclared Identifier: b"
    #     self.assertTrue(TestChecker.test(input, expect, 404))
    
    # def test_TypeMismatchInSTMT_for1(self):
    #     """test_TypeMismatchInBinExp_REMAINDER""" 
    #     # OPERAND TYPE: INT
    #     input = """
    #         foo: function integer (inherit a: integer) {
    #         }
    #         bar: function integer (c: integer) inherit foo {
    #             super(2);
    #         }
    #         """
    #     expect = "No entry point"
    #     self.assertTrue(TestChecker.test(input, expect, 405))
    # def test_TypeMismatchInSTMT_for1(self):
    #     """test_TypeMismatchInBinExp_REMAINDER""" 
    #     # OPERAND TYPE: INT
    #     input = """
    #         main: function void () {
    #             x, y, z: integer = 1, 2, 3;
    #             a, b: float;
    #             c = 1.0;
    #         }
    #         """
    #     expect = "Undeclared Identifier: c"
    #     self.assertTrue(TestChecker.test(input, expect, 406))
    
    def test_TypeMismatchInSTMT_for1(self):
        """test_TypeMismatchInBinExp_REMAINDER""" 
        # OPERAND TYPE: INT
        input = """
            a, b: integer;
            foo: function void () {
                x, y, z: integer = 1, 2, 3;
                a, b: float;
            }
            """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input, expect, 407))
    
    # def test_TypeMismatchInSTMT_for1(self):
    #     """test_TypeMismatchInBinExp_REMAINDER""" 
    #     # OPERAND TYPE: INT
    #     input = """
    #                 a: array[10, 2] of integer = {1, 2}
    #         """
    #     expect = "No entry point"
    #     self.assertTrue(TestChecker.test(input, expect, 408))
        