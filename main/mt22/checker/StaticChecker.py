from Visitor import Visitor
from abc import ABC

from AST import *


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
def infer(id, typ, symbol_list):
    for sym in symbol_list:
        if sym.name == id.name:
            sym.returnType = typ
            return typ 
# _________________________________________________________
# infer typ for param_name in func_name
# _________________________________________________________
def inferParam(func_name, param_name , typ, global_env):
    for func in global_env:
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
            self.visit(decl, (True,[],env))
        
        # raise NoEntryPoint() in the end of 2nd check
        for func in env[0]:
            if func.name == "main" and func.returnType == VoidType() and func.isFunction == True:
                return
        raise NoEntryPoint()
    # _____________________________________________________________
    # name: str, typ: Type, init: Expr or None = None
    # param (isGlobal: Bool,[Symbol()] in current scope ,[Symbol()] in global scope)
    # param[0] = True if in global scope
    # _____________________________________________________________
    def visitVarDecl(self, ast, param):
        currentScope = param[1]
        globalScope = param[2]
        if ast.name in currentScope:
            raise Redeclared(Variable(), ast.name)
        
        if ast.init is None:
            if ast.typ is AutoType(): # declare auto type var but no init
                raise Invalid(Variable(),ast.name)
            return Symbol(ast.name, ast.typ)
        
        elif ast.init is not None:
            # if ast.typ is ArrayType:
            exprType = self.visit(ast.init, param)
            
            if ast.typ is AutoType():
                infer(ast, exprType, currentScope + globalScope)
            elif exprType is AutoType():
                infer(ast.init, ast.typ, currentScope + globalScope)
            elif ast.typ is IntegerType() and exprType is FloatType():
                raise TypeMismatchInStatement(ast)
            elif ast.typ is FloatType() and exprType is IntegerType():
                pass
            elif type(ast.typ) != type(exprType):
                raise TypeMismatchInStatement(ast)
            else:
                return Symbol(ast.name, ast.typ)
            
            
        
    # _____________________________________________________________
    # name: str, return_type: Type, params: List[ParamDecl], inherit: str or None, body: BlockStmt
    # param (isGlobal: Bool,[Symbol()] in current scope ,[Symbol()] in global scope)
    # _____________________________________________________________
    def visitFuncDecl(self, ast, param):        
        globalScope = param[2][0] # dung roi dung sua lai
        funcSymbol = Symbol(ast.name, ast.return_type, True, ast.params, ast.inherit)
        # them cac ten cua param vao local_scope
        listParam = ast.params 
        parent_function = None
        localEnv = []
        for i in listParam:
            localEnv += [self.visit(i, localEnv)]
        env = [[]] + [globalScope]
        env[0] = localEnv            
        # check if the function inherits from another function
        if ast.inherit is not None:
            # find the parent function in the global scope
            for symbol in globalScope:
                if symbol.name == ast.inherit:
                    # check if the parent function is a function
                    if symbol.isFunction == False:
                        raise TypeMismatchInExpression(ast)
                    parent_function = symbol
            # parent function is not found
            if parent_function is None:
                raise Undeclared(Function(), ast.inherit)
        # visit block statement
        # param (is_in_loop: Bool, env,  is_function_body: Bool, 
        # Symbol() of current function,
        # Symbol() of parent function)
        self.visit(ast.body, (False, env, True,funcSymbol ,parent_function))
        
        
    # _________________________________________________________
    # name: str, typ: Type, inherit: str or None
    # param: [ParamDecl()]
    # _________________________________________________________
    def visitParamDecl(self, ast, param):
        for paramDecl in param:
            if paramDecl.name == ast.name:
                raise Redeclared(Parameter(), ast.name)
    
        return Symbol(ast.name, ast.typ)
        
    # _________________________________________________________
    # lhs: LHS, rhs: Expr
    # param (is_in_loop: Bool, env, False, None, None, is_init_for: Bool)
    # _________________________________________________________
    def visitAssignStmt(self, ast, param):
        env = param[1]
        is_init_for = param[5]
        rightType = self.visit(ast.rhs, env)
        leftType = self.visit(ast.lhs, env)
        
        if is_init_for: 
            if leftType != integerType():
                raise TypeMismatchInStatement(ast)
            
        if type(leftType) == AutoType:
            infer(ast.lhs, rightType, env)
            return 
        elif rightType is AutoType():
            infer(ast.rhs, leftType, env)
            return 
        elif leftType is IntegerType() and rightType is FloatType():
            raise TypeMismatchInStatement(ast)
        elif leftType is FloatType() and rightType is IntegerType():
            pass
        elif leftType != rightType:
            raise TypeMismatchInStatement(ast)
        
    
    # _________________________________________________________
    # BlockStmt body: List[Stmt or VarDecl]
    # param (is_in_loop: Bool, env, is_function_body: Bool, 
    # Symbol() of current function,
    # Symbol() of parent function)
    # _________________________________________________________
    def visitBlockStmt(self, ast, param):
        is_in_loop = param[0]
        env = param[1]
        is_func_body = param[2]
        current_func = param[3]
        parent_func = param[4]
        currentEnv = []
        # check if the first statement in the function body is a call to the parent function (super(), or preventDefault())
        if is_func_body == True: # is_function_body
            if parent_func is not None: # parent function exists
                parent_params = parent_func.param
                if len(ast.body) > 0 and type(ast.body[0]) is CallStmt:
                    # name: str, args: List[Expr]
                    # expr la CallStmt 
                    expr = ast.body[0]
                    if expr.name == "super":
                        if len(expr.args) > len(parent_params):
                            raise TypeMismatchInExpression(expr.args[len(parent_params)]) # raise args du thua dau tien
                        elif len(expr.args) < len(parent_params):
                            raise TypeMismatchInExpression()
                        
                        
                            
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
                                raise TypeMismatchInExpression(expr.args[i]) # args dau tien khong khop kieu
                            else: # expr.args[i] is parent_params[i]
                                pass
                        # check if the name of params turn out 2 times
                        
                        
                        
                        # check if the name of params inherit in father function is the same as the name of params in function
                        # if not, add the param to the current environment
                        for param in parent_params:
                            if param.name in env[0] and param.inherit == True:
                                raise Invalid(Parameter(), param.name)
                            elif param.inherit == True:
                                env[0] += [Symbol(param.name, param.returnType)]
                            # else: # param.inherit == False
                        
                        
                    elif expr.name == "preventDefault":
                        # khong goi super()
                        pass
                    else: # goi ham super() khong tham so
                        if len(parent_params) != 0:
                            raise TypeMismatchInExpression()
                        
            
            else: # parent function does not exist, check if the first statement is preventDefault()
                if len(ast.body) > 0:
                    stmt = ast.body[0]
                    
                    if type(stmt) is CallStmt and (expr.name == "preventDefault" or expr.name == "super"):
                        raise TypeMismatchInExpression(expr)
                pass
                    
        
        
       
            
        for stmt in ast.body:
            if isinstance(stmt, VarDecl):
                env[0].append(self.visit(stmt, (False, env[0], env[1:])))
            else: # stmt is Stmt
                self.visit(stmt, (is_in_loop, env, False, None, None))
        
        
       # end of block, remove the current environment
        env = env[1:]
        
        return 
    # _________________________________________________________    
    # cond: Expr, tstmt: Stmt, fstmt: Stmt or None = None
    # param (is_in_loop: Bool, env, False, None, None)
    # _________________________________________________________
    def visitIfStmt(self, ast, param):
        is_in_loop = param[0]
        env = param[1]
        cond = self.visit(ast.cond, env)
        if cond is not BoolType():
            raise TypeMismatchInStatement(ast)
        tstmt = self.visit(ast.thenStmt, (is_in_loop, env, False, None, None))
        fstmt = None
        if ast.fstmt is not None:
            fstmt = self.visit(ast.fstmt, (is_in_loop, env, False, None, None))
            
    # _________________________________________________________    
    # init: AssignStmt, cond: Expr, upd: Expr, stmt: Stmt
    # param (is_in_loop: Bool, env)
    # _________________________________________________________  
    def visitForStmt(self, ast, param):
        is_in_loop = param[0]
        env = param[1]
        assignStmt = self.visit(ast.init, (is_in_loop, env, False, None, None, True)) # id for assignStmt duoc chuan bi ti truoc, khong khoi tao luc nay, id nay kieu int
        if ast.init.lhs is not Id() or ast.init.:
            raise TypeMismatchInStatement(ast)
        
        cond = self.visit(ast.cond, env)
        if cond is not BoolType():
            raise TypeMismatchInStatement(ast)
        upd = self.visit(ast.upd, env)
        if upd is not IntType():
            raise TypeMismatchInStatement(ast)
        
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
    # CallStmt(Stmt)
    # name: str, args: List[Expr]
    # param (is_in_loop: Bool, env 
    # _________________________________________________________
    def visitCallStmt(self, ast, param):
        env = param[1]
        if ast.name == "super" or ast.name == "preventDefault":
            return
        for localEnv in env[:-1]:
            for symbol in localEnv: # find id in the current environment
                if ast.name == symbol.name and symbol.isFuntion == False:
                    raise TypeMismatchInStatement(ast) # id is declared in current scope but is not a function
            
        for symbol in param[-1]: # param[-1] is the list of Symbol() in the global environment
            if ast.name == symbol.name:
                if len(ast.args) != len(symbol.param):
                    raise TypeMismatchInStatement(ast)
                for i in range(len(ast.args)):
                    if type(ast.args[i]) == AutoType():
                        infer(ast.args[i], symbol.param[i].typ, env)
                    elif type(symbol.param[i].typ) == AutoType():
                        infer(symbol.param[i].typ, ast.args[i], env)
                    elif type(ast.args[i]) == IntegerType() and type(symbol.param[i].typ) == FloatType():
                        # convert the param to float
                        pass
                    elif type(ast.args[i]) != type(symbol.param[i].typ):
                        raise TypeMismatchInStatement(ast)
                return # stmt chi check loi, khong tra ve kieu
        
        raise Undeclared(Function(), ast.name)
    
    # _________________________________________________________
    # FuncCall(Expr)
    # name: str, args: List[Expr]
    # param env 
    # _________________________________________________________
    def visitFuncCall(self, ast, param): 
        env = param
        for localEnv in env[:-1]:
            for symbol in localEnv: # find id in the current environment
                if ast.name == symbol.name and symbol.isFuntion == False:
                    raise TypeMismatchInExpression(ast) # id is declared in current scope but is not a function
                
        for symbol in param[-1]: # param[-1] is the list of Symbol() in the global environment
            if ast.name == symbol.name:
                if len(ast.args) != len(symbol.param):
                    raise TypeMismatchInExpression(ast)
                for i in range(len(ast.args)):
                    if type(ast.args[i]) == AutoType():
                        infer(ast.args[i], symbol.param[i].typ, env)
                    elif type(symbol.param[i].typ) == AutoType():
                        infer(symbol.param[i].typ, ast.args[i], env)
                    elif type(ast.args[i]) == IntegerType() and type(symbol.param[i].typ) == FloatType():
                        # convert the param to float
                        pass
                    elif type(ast.args[i]) != type(symbol.param[i].typ):
                        raise TypeMismatchInExpression(ast)
                return symbol.returnType # expr tra ve kieu
        
        raise Undeclared(Function(), ast.name)
    
    # _________________________________________________________
    # op: str, left: Expr, right: Expr
    # op is Multi: *, /, %
    #        Add: +, -
    #        Logical: &&, ||
    #        Relational: <, >, <=, >=, ==, !=
    #        String: ::
    # param is env
    # _________________________________________________________
    def visitBinExpr(self, ast, param): 
        op = ast.op
        
        leftType = self.visit(ast.left, param)
        rightType = self.visit(ast.right, param)
        if op in ['+', '-', '*', '/']: # operand type is int/float
            if intersection([leftType, rightType], [BooleanType(), StringType(), VoidType(), ArrayType()]):
                raise TypeMismatchInExpression(ast)
            elif leftType == AutoType() and rightType == AutoType():
                return FloatType() # testcase khong co 2 cai auto ko suy dien dc, tra ve float tang ti le dung
            elif leftType == AutoType():
                infer(ast.left, rightType, param)
                return rightType
            elif rightType == AutoType():
                infer(ast.right, leftType, param)
                return leftType
            elif leftType == IntegerType() and rightType == IntegerType():
                return IntegerType()
            else:
                return FloatType()
            
        elif op in ['%']: # operand type is int
            if intersection([leftType, rightType], [BooleanType(), StringType(), VoidType(), ArrayType(), FloatType()]):
                raise TypeMismatchInExpression(ast)
            elif leftType == AutoType() and rightType == AutoType():
                infer(ast.left, IntegerType(), param)
                infer(ast.right, IntegerType(), param)
                return IntegerType()
            elif leftType == AutoType():
                infer(ast.left, rightType, param)
                return IntegerType()
            elif rightType == AutoType():
                infer(ast.right, leftType, param)
                return IntegerType()
            elif leftType == IntegerType() and rightType == IntegerType():
                return IntegerType()
        elif op in ['&&', '||']: # operand type is bool
            if intersection([leftType, rightType], [IntegerType(), StringType(), VoidType(), ArrayType(), FloatType()]):
                raise TypeMismatchInExpression(ast)
            if leftType == AutoType() and rightType == AutoType():
                infer(ast.left, BooleanType(), param)
                infer(ast.right, BooleanType(), param)
                return BooleanType()
            elif leftType == AutoType():
                infer(ast.left, rightType, param)
                return BooleanType()
            elif rightType == AutoType():
                infer(ast.right, leftType, param)
                return BooleanType()
            else :
                return BooleanType()
        elif op in ['<', '>', '<=', '>=', '==', '!=']: # operand type is int/float
            if intersection([leftType, rightType], [BooleanType(), StringType(), VoidType(), ArrayType()]):
                raise TypeMismatchInExpression(ast)
            elif leftType == AutoType() and rightType == AutoType():
                return FloatType() # ti le dung cao hon
            elif leftType == AutoType():
                infer(ast.left, rightType, param)
                return rightType
            elif rightType == AutoType():
                infer(ast.right, leftType, param)
                return leftType
            elif leftType == IntegerType() and rightType == IntegerType():
                return IntegerType()
            else:
                return FloatType()
            
            
        elif op in ['::']: # operand type is string
            if intersection([leftType, rightType], [BooleanType(), IntegerType(), VoidType(), ArrayType(), FloatType()]):
                raise TypeMismatchInExpression(ast)
            elif leftType == AutoType() and rightType == AutoType():
                infer(ast.left, StringType(), param)
                infer(ast.right, StringType(), param)
                return StringType()
            elif leftType == AutoType():
                infer(ast.left, rightType, param)
                return StringType()
            elif rightType == AutoType():
                infer(ast.right, leftType, param)
                return StringType()
            else :
                return StringType()
    # _________________________________________________________
    # op: str, body: Expr
    # op is Unary: !, -
    # param is env
    # _________________________________________________________
    def visitUnExpr(self, ast, param): 
        op = ast.op
        bodyType = self.visit(ast.body, param)
        if op in ['!']: # operand type is bool
            if bodyType == AutoType():
                infer(ast.body, BooleanType(), param)
                return BooleanType()
            elif bodyType == BooleanType():
                return BooleanType()
            else:
                raise TypeMismatchInExpression(ast)
        elif op in ['-']: # operand type is int/float
            if bodyType == AutoType():
                infer(ast.body, IntegerType(), param)
                return IntegerType()
            elif bodyType == IntegerType():
                return IntegerType()
            elif bodyType == FloatType():
                return FloatType()
            else:
                raise TypeMismatchInExpression(ast)
    
    
    def visitId(self, ast, param):
        for env in param:
            for sym in env:
                if ast.name == sym.name:
                    return sym.returnType
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
    