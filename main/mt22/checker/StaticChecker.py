from Visitor import Visitor
from abc import ABC

# from AST import *
from AST import ArrayType
from AST import IntegerType
from AST import FloatType
from AST import BooleanType
from AST import StringType
from AST import AutoType
from AST import VoidType
from AST import FuncDecl
from AST import WhileStmt
from AST import DoWhileStmt
from AST import ForStmt
from AST import VarDecl
from AST import Id

from StaticError import *

# parameter type
class ParamType:
    def __init__(self,name,returnType, inherit: bool = False):
        self.name = name
        self.returnType = returnType
        self.inherit = inherit

# luu tru var hoac function, isFunction nhan gia tri boolean 
# function: mtype.param la [Mtype(a, IntegerType())], .value luon la None
# variable: mtype.param luon la [], value co the khac None
class Symbol:
    def __init__(self, name, returnType, isFunction: bool = False, param = [],  inherit: str = None):
        self.name = name
        self.returnType = returnType
        self.isFunction = isFunction
        self.param = param
        self.inherit = inherit
        # self.value = value
        
    
class GetEnv(Visitor):
        # decls: List[Decl]
    def visitProgram(self, ast, param):
        
        o = []
        for decl in ast.decls:
            o.append(self.visit(decl, o))
            
        return o

        # name: str, typ: Type, init: Expr or None = None
        # param = [Symbol(ast.name, ast.typ, ast.init)] in global
    def visitVarDecl(self, ast, param):
        for var in param:
            if var.name == ast.name:
                raise Redeclared(Variable(), ast.name)
        return Symbol(ast.name, ast.typ)
        
    # _____________________________________________________________
    # name: str, return_type: Type, params: List[ParamDecl], inherit: str or None, body: BlockStmt
    # param [Symbol()] in global scope)
    # _____________________________________________________________
    def visitFuncDecl(self, ast, param):
        
        paramList = []
        for i in ast.params:
            paramList.append(self.visit(i, paramList))
        return Symbol(ast.name, ast.return_type, True, paramList, ast.inherit)
    # _________________________________________________________
    # name: str, typ: Type, inherit: str or None
    # param: [ParamDecl()]
    # _________________________________________________________
    def visitParamDecl(self, ast, param):
        for paramDecl in param:
            if paramDecl.name == ast.name:
                raise Redeclared(Parameter(), ast.name)
        return ParamType(ast.name, ast.typ, ast.inherit)

# _________________________________________________________
# infer typ for id
# _________________________________________________________
def infer(name, typ, o):
    for env in o:
        for symbol in env:
            if symbol.name == name:
                symbol.returnType = typ
                return typ
# _________________________________________________________
# infer typ for param_name in func_name
# _________________________________________________________
def inferParam(func_name, param_name , typ, o):
    for func in o:
        if func.name == func_name:
            for param in func.param:
                if param.name == param_name:
                    param.returnType = typ
                    return typ
        
def intersection(lst1, lst2): 
    lst3 = [value for value in lst1 if value in lst2] 
    return lst3   
    

class StaticChecker(Visitor):
    
    def __init__(self, ast):
        self.ast = ast
    def check(self):
        return self.visitProgram(self.ast, [])
    
        # decls: List[Decl]
    def visitProgram(self, ast, param): 
        # special functions
        env = [[]]
        # special functions
        env[0] = [Symbol("readInteger", IntegerType(), True),
            Symbol("printInteger", VoidType(), True, [ParamType("anArg", IntegerType())]),
            Symbol("readFloat", FloatType(), True),
            Symbol("writeFloat", VoidType(), True, [ParamType("anArg", FloatType())]),
            Symbol("readBoolean", BooleanType(), True),
            Symbol("printBoolean", VoidType(), True, [ParamType("anArg", BooleanType())]),
            Symbol("readString", True, None, StringType()),
            Symbol("printString", VoidType(), True, [ParamType("anArg", StringType())])
        ]
        
        # first check, get all function and variable of global scope
        globalEnv = GetEnv().visitProgram(ast, [])
            
        env[0] += globalEnv
        # second check, check all declare
        
        for decl in ast.decls:
            self.visit(decl, (env, True))
        
        # raise NoEntryPoint() in the end of 2nd check
        for func in env[0]:
            if func.name == "main" and func.returnType == VoidType() and func.isFunction == True:
                return
        raise NoEntryPoint()
    # _____________________________________________________________
    # name: str, typ: Type, init: Expr or None = None
    # param[0] = [Symbol(ast.name, ast.typ, ast.init)] in current scope
    # param[1] = flag global
    # _____________________________________________________________
    def visitVarDecl(self, ast, param):
        env = param[0]
        flag_global = param[1]
        if flag_global == False: # if local scope thi added vao env[0]
            for Symbol in env[0]:
                if Symbol.name == ast.name:
                    raise Redeclared(Variable(), ast.name)
        
            if ast.init is None:
                return Symbol(ast.name, ast.typ)
        
        
        # kieu tu init
        elif ast.init is not None:
            # if ast.typ is ArrayType:
            exprType = self.visit(ast.init, env)
            
            if ast.typ is AutoType():
                infer(ast, exprType, env)
            elif exprType is AutoType():
                infer(ast.init, ast.typ, env)
            elif ast.typ is IntegerType() and exprType is FloatType():
                raise TypeMismatchInStatement(ast)
            elif ast.typ is FloatType() and exprType is IntegerType():
                pass
            elif type(ast.typ) is not type(exprType):
                raise TypeMismatchInStatement(ast)
            else:
                env[0].append(Symbol(ast.name, ast.typ))
            
            
        
    # _____________________________________________________________
    # name: str, return_type: Type, params: List[ParamDecl], inherit: str or None, body: BlockStmt
    # param[0] = [Symbol(ast.name, ast.typ, ast.init)] in global scope
    # _____________________________________________________________
    def visitFuncDecl(self, ast, param):        
        funcSymbol = Symbol(ast.name, ast.return_type, True, ast.params, ast.inherit)
        # them cac ten cua param vao local_scope
        listParam = ast.params 
        parent_function = None
        
        newEnv = [[]] + param[0]
        for i in listParam:
            self.visit(i, newEnv)
        
        
        # check if the function inherits from another function
        if ast.inherit is not None:
            # find the parent function in the global scope
            for symbol in newEnv[1]: # search in global scope
                if symbol.name == ast.inherit:
                    # check if the parent function is a function
                    if symbol.isFunction == False:
                        raise TypeMismatchInExpression(ast) # not tested
                    parent_function = symbol
            # parent function is not found
            if parent_function is None:
                raise Undeclared(Function(), ast.inherit)
        
        # visit block statement
        # param (newEnv,
        # is_in_loop: Bool, is_function_body: Bool, 
        # Symbol() of current function,
        # Symbol() of parent function)
        self.visit(ast.body, (newEnv, False, True,funcSymbol ,parent_function))
        
        
        
        
    # _________________________________________________________
    # name: str, typ: Type, inherit: str or None
    # param: param[0] = [Symbol(ast.name, ast.typ, ast.init)] current scope
    # _________________________________________________________
    def visitParamDecl(self, ast, param):
        for symbol in param:
            if symbol.name == ast.name:
                raise Redeclared(Parameter(), ast.name)
    
        param[0].append(Symbol(ast.name, ast.typ))
        
    # _________________________________________________________
    # lhs: LHS, rhs: Expr
    # param (is_in_loop: Bool, [Symbol()] in current scope)
    # _________________________________________________________
    def visitAssignStmt(self, ast, param):
        localScope = param[1]
        leftType = self.visit(ast.lhs, localScope)
        rightType = self.visit(ast.rhs, localScope)
        
        if leftType is AutoType():
            infer(ast.lhs, rightType, localScope)
            return 
        elif rightType is AutoType():
            infer(ast.rhs, leftType, localScope)
            return 
        elif leftType is IntegerType() and rightType is FloatType():
            raise TypeMismatchInStatement(ast)
        elif leftType is FloatType() and rightType is IntegerType():
            pass
        elif leftType is not rightType:
            raise TypeMismatchInStatement(ast)
        
    
    # _________________________________________________________
    # BlockStmt body: List[Stmt or VarDecl]
    #param (newEnv,
    # is_in_loop: Bool, is_function_body: Bool, 
    # Symbol() of current function,
    # Symbol() of parent function)
    # _________________________________________________________
    def visitBlockStmt(self, ast, param):
        env = param[0]
        is_in_loop = param[1]
        is_func_body = param[2]
        current_func = param[3]
        parent_func = param[4]
        # check if the first statement in the function body is a call to the parent function (super(), or preventDefault())
        if is_func_body == True: # is_function_body
            if parent_func is not None: # parent function exists
                parent_params = parent_func.param
                if len(ast.body) > 0:
                    # name: str, args: List[Expr]
                    # expr la CallStmt 
                    expr = ast.body[0]
                    if expr.name == "super":
                        if len(expr.args) != len(parent_params):
                            raise TypeMismatchInExpression(ast)
                        
                            
                        # check type of each param of super function and the parent function
                        for i in range(len(expr.args)):
                            typArgs = self.visit(expr.args[i], env)
                            if typArgs is AutoType() and parent_params[i].returnType is AutoType():
                                pass # not error type cannot be inferred
                            elif typArgs is AutoType(): # infer the type of param in father function for id in super function
                                # infer(expr.args[i].name, parent_params[i].returnType, globalEnv)
                                pass # test case var decl with auto type always init
                            elif parent_params[i] is AutoType(): # infer the type of param in super function for father function
                                inferParam(parent_func.name, parent_params[i].name, expr.args[i].returnType, globalEnv)
                            elif typArgs is IntegerType() and parent_params[i].returnType is FloatType():
                                # convert the integer type param to float
                                pass
                            elif typArgs != parent_params[i].returnType:
        
                                raise TypeMismatchInExpression(expr.args[i])
                            else: # expr.args[i] is parent_params[i]
                                pass
                        # check if the name of params turn out 2 times
                        
                        
                        
                        # check if the name of params inherit in father function is the same as the name of params in function
                        # if not, add the param to the current environment
                        for param in parent_params:
                            if param.name in currentEnv and param.inherit == True:
                                raise Redeclared(Parameter(), param.name)
                            else:
                                currentEnv += [param]
                        
                    elif expr.name == "preventDefault":
                        # khong goi super()
                        pass
                    else: # goi ham super() khong tham so
                        if len(parent_params) != 0:
                            raise TypeMismatchInExpression()
            
            else: # parent function does not exist, check if the first statement is preventDefault()
                if len(ast.body) > 0 and not isinstance(ast.body[0], VarDecl):
                    stmt = self.visit(ast.body[0], env)
                    if type(stmt) is CallStmt() and stmt.name == "preventDefault":
                        raise TypeMismatchInExpression(expr)
                pass
                    
            
                
        for stmt in ast.body:
            if isinstance(stmt, VarDecl):
                self.visit(stmt, (env, False))
            else: # stmt is Stmt
                self.visit(stmt, (env, is_in_loop))
        print("test:_______")
        for o in env:
            print("_______")
            for symbol in o:
                print(symbol.name, symbol.returnType)
        
        
        return 
        
        
    def visitIfStmt(self, ast, param): pass
    def visitForStmt(self, ast, param): pass
    def visitWhileStmt(self, ast, param): pass
    def visitDoWhileStmt(self, ast, param): pass
    def visitBreakStmt(self, ast, param): pass
    def visitContinueStmt(self, ast, param): pass
    
    # _________________________________________________________
    # Rerturnstmt expr: Expr or None = None
    # param (is_in_loop: Bool, [Symbol()] in current scope)
    # _________________________________________________________
    def visitReturnStmt(self, ast, param): 
        if ast.expr is None:
            return VoidType()
        else :
            return self.visit(ast.expr, param[1])
        
    # _________________________________________________________
    # name: str, args: List[Expr]
    # param (is_in_loop: Bool, [Symbol()] in current scope)
    # _________________________________________________________
    def visitCallStmt(self, ast, param): 
        for symbol in param[1]:
            if ast.name == symbol.name:
                if len(ast.args) != len(symbol.param):
                    raise TypeMismatchInStatement(ast)
                for i in range(len(ast.args)):
                    if type(ast.args[i]) is AutoType():
                        infer(ast.args[i], symbol.param[i].typ, param[1])
                    elif type(symbol.param[i].typ) is AutoType():
                        infer(symbol.param[i].typ, ast.args[i], param[1])
                    elif type(ast.args[i]) == IntegerType() and type(symbol.param[i].typ) == FloatType():
                        # convert the param to float
                        pass
                    elif type(ast.args[i]) != type(symbol.param[i].typ):
                        raise TypeMismatchInStatement(ast)
                return
        if ast.name == "super" or ast.name == "preventDefault":
            return
        raise Undeclared(Function(), ast.name)
    # _________________________________________________________
    # op: str, left: Expr, right: Expr
    # op is Multi: *, /, %
    #        Add: +, -
    #        Logical: &&, ||
    #        Relational: <, >, <=, >=, ==, !=
    #        String: ::
    def visitBinExpr(self, ast, param): 
        op = ast.op
        
        leftType = self.visit(ast.left, param)
        rightType = self.visit(ast.right, param)
        
        if op in ['+', '-', '*', '/']: # operand type is int/float
            if intersection([type(leftType), type(rightType)], [BooleanType, StringType, VoidType, ArrayType]):
                raise TypeMismatchInExpression(ast)
            elif type(leftType) is AutoType() and type(rightType) is AutoType():
                return AutoType()
            elif type(leftType) is AutoType():
                infer(ast.left, rightType, param)
                return rightType
            elif type(rightType) is AutoType():
                infer(ast.right, leftType, param)
                return leftType
            elif type(leftType) is IntegerType() and type(rightType) is IntegerType():
                return IntegerType()
            else:
                return FloatType()
            
        elif op in ['%']: # operand type is int
            pass
        elif op in ['&&', '||']: # operand type is bool
            pass
        elif op in ['<', '>', '<=', '>=', '==', '!=']: # operand type is int/float
            pass
        elif op in ['::']: # operand type is string
            pass
    def visitUnExpr(self, ast, param): pass
    
    def visitFuncCall(self, ast, param): pass
    
    def visitId(self, ast, param):
        for symbol in param:
            if ast.name == symbol.name:
                return symbol.returnType
        raise Undeclared(Identifier(), ast.name)

    

    def visitIntegerType(self, ast, param): return IntegerType()
    def visitFloatType(self, ast, param): return FloatType()
    def visitBooleanType(self, ast, param): return BooleanType()
    def visitStringType(self, ast, param): return StringType()
    
    def visitAutoType(self, ast, param): return AutoType()
    def visitVoidType(self, ast, param): return VoidType()
    
    # (self, dimensions: List[int], typ: AtomicType):
    def visitArrayType(self, ast, param): return ArrayType(ast.dimensions, ast.typ) 
    
    # name: str, cell: List[Expr]
    def visitArrayCell(self, ast, param): 
        arr = self.visit(ast.name, param)
        elements = []
        for ele in ast.cell:
            elements += [self.visit(ele, param)]
        if type(arr) is ArrayType:
            if len(arr.dimensions) != len(elements):
                raise TypeMismatchInExpression(ast)
            for i in range(len(elements)):
                if type(elements[i]) != IntegerType():
                    raise TypeMismatchInExpression(ast)
            return arr.typ
        else :
            raise TypeMismatchInExpression(ast)
        
    
    # explist: List[Expr]
    def visitArrayLit(self, ast, param):
        elements = []
        for ele in ast.explist:
            elements += [self.visit(ele, param)]
        typEle = self.visit(ast.explist[0], param)
        for ele in elements:
            if type(ele) != type(typEle):
                raise IllegalArrayLiteral(ast)
        return ArrayType([len(ast.explist)], typEle)
    
    def visitIntegerLit(self, ast, param): return IntegerType()
    def visitFloatLit(self, ast, param): return FloatType()
    def visitStringLit(self, ast, param): return StringType()
    def visitBooleanLit(self, ast, param): return BooleanType()
    