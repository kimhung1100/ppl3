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
                # raise Redeclared(Variable(), ast.name)
                pass
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
                # raise Redeclared(Parameter(), ast.name)
                pass
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
        
        # env[0] += globalEnv
        # second check, check all declare
        
        for decl in ast.decls:
            self.visit(decl, [True,env,globalEnv])
        
        # raise NoEntryPoint() in the end of 2nd check
        for func in env[0]:
            if func.name == "main" and func.returnType == VoidType() and func.isFunction == True:
                return
        raise NoEntryPoint()
    # _____________________________________________________________
    # name: str, typ: Type, init: Expr or None = None
    # param (isGlobal: Bool,env , globalEnvPrototype)
    # param[0] = True if in global scope
    # _____________________________________________________________
    def visitVarDecl(self, ast, param):
        env = param[1]
        globalEnvPrototype = param[2]
        # check redelare in current scope (can be local scope or global scope)
        for sym in env[0]:
            if sym.name == ast.name:
                raise Redeclared(Variable(), ast.name)
        if param[0] == True: # in global scope
            env[0].append(Symbol(ast.name, ast.typ))
        if ast.init is None:
            if ast.typ is AutoType(): # declare auto type var but no init
                raise Invalid(Variable(),ast.name)
            return Symbol(ast.name, ast.typ)
        
        elif ast.init is not None:
            # if ast.typ is ArrayType:
            exprType = self.visit(ast.init, env)
            
            if ast.typ == AutoType:
                infer(ast.name, exprType, env)
            elif ast.typ == IntegerType and exprType == FloatType:
                raise TypeMismatchInStatement(ast)
            elif ast.typ == FloatType and exprType == IntegerType:
                pass
            elif ast.typ != exprType:
                raise TypeMismatchInStatement(ast)
            else:
                return Symbol(ast.name, ast.typ)
            
            
        
    # _____________________________________________________________
    # name: str, return_type: Type, params: List[ParamDecl], inherit: str or None, body: BlockStmt
    # param (isGlobal: Bool, env ,[Symbol()] in global scope)
    # _____________________________________________________________
    def visitFuncDecl(self, ast, param):
        env = param[1]
        globalScopePrototype = param[2] # global duyet ban dau prototype
        
        # them cac ten cua param vao local_scope
        listParam = ast.params 
        parent_function = None
        localEnv = []
        # check redeclare function
        for sym in env[0]:
            if sym.name == ast.name:
                raise Redeclared(Function(), ast.name) # function is already declared
        # visit and check redeclare param
        paramList = []
        for i in ast.params:
            paramList.append(self.visit(i, paramList))
            
        # create function symbol
        funcSymbol = Symbol(ast.name, ast.return_type, True, paramList, ast.inherit)
        # add function symbol to local scope
        env[0] += [funcSymbol]
        # add param to local scope
        for i in listParam:
            localEnv += [self.visit(i, localEnv)]
        # create new scope
        env = [[]] + env
        env[0] = localEnv            
        # check if the function inherits from another function
        if ast.inherit is not None:
            # find the parent function in the global scope
            for symbol in globalScopePrototype:
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
        self.visit(ast.body, [False, env, True, funcSymbol ,parent_function])
        # end of scope block statement, remove local scope
        env = env[1:]
        
        
        
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
            if type(leftType) != IntegerType:
                raise TypeMismatchInStatement(ast)
            
        if type(leftType) == AutoType:
            infer(ast.lhs, rightType, env)
            return 
        elif rightType == AutoType:
            infer(ast.rhs, leftType, env)
            return 
        elif leftType == IntegerType and rightType == FloatType:
            raise TypeMismatchInStatement(ast)
        elif leftType == FloatType and rightType == IntegerType:
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
                    
                    if type(stmt) == CallStmt and (stmt.name == "preventDefault" or stmt.name == "super"):
                        raise TypeMismatchInExpression(expr)
                pass
                    
        
        
       
            
        for stmt in ast.body:
            if isinstance(stmt, VarDecl):
                env[0].append(self.visit(stmt, [is_in_loop, env, is_func_body, current_func, parent_func, False]))
            else: # stmt is Stmt
                self.visit(stmt, [is_in_loop, env, is_func_body, current_func, parent_func, False])
        
        # test env
        
        
       # end of block, remove the current environment
        
        
        
        return 
    # _________________________________________________________    
    # cond: Expr, tstmt: Stmt, fstmt: Stmt or None = None
    # param (is_in_loop: Bool, env, is_function_body: Bool, 
    # Symbol() of current function,
    # Symbol() of parent function)
    # _________________________________________________________
    def visitIfStmt(self, ast, param):
        is_in_loop = param[0]
        env = param[1]
        cond = self.visit(ast.cond, env)
        if type(cond) != BooleanType:
            raise TypeMismatchInStatement(ast) # tiep tuc truyen tham so cho visit stmt
        tstmt = self.visit(ast.tstmt, [is_in_loop, env, param[2], param[3], param[4]]) 
        fstmt = None
        if ast.fstmt is not None:
            fstmt = self.visit(ast.fstmt, [is_in_loop, env, param[2], param[3], param[4]])
            
    # _________________________________________________________    
    # init: AssignStmt, cond: Expr, upd: Expr, stmt: Stmt
    # param (is_in_loop: Bool, env)
    # _________________________________________________________  
    def visitForStmt(self, ast, param):
        is_in_loop = param[0]
        env = param[1]
        is_in_loop = True
        assignStmt = self.visit(ast.init, [is_in_loop, env, False, None, None, True]) # id for assignStmt duoc chuan bi ti truoc, khong khoi tao luc nay, id nay kieu int
        
        cond = self.visit(ast.cond, env)
        if type(cond) != BooleanType:
            raise TypeMismatchInStatement(ast)
        upd = self.visit(ast.upd, env)
        if type(upd) != IntegerType:
            raise TypeMismatchInStatement(ast)

        env = [[]] + env
        self.visit(ast.stmt, [is_in_loop, env, False, None, None])
        env = env[1:]
    
    # _________________________________________________________    
    # cond: Expr, stmt: Stmt
    # param (is_in_loop: Bool, env)
    # _________________________________________________________
    def visitWhileStmt(self, ast, param): 
        is_in_loop = param[0]
        env = param[1]
        is_in_loop = True
        cond = self.visit(ast.cond, env)
        if type(cond) != BooleanType:
            raise TypeMismatchInStatement(ast)
        
        env = [[]] + env
        self.visit(ast.stmt, [is_in_loop, env, False, None, None])
        env = env[1:]
        
    # _________________________________________________________    
    # cond: Expr, stmt: BlockStmt
    # param (is_in_loop: Bool, env)
    # _________________________________________________________
    def visitDoWhileStmt(self, ast, param): 
        is_in_loop = param[0]
        env = param[1]
        is_in_loop = True
        
        env = [[]] + env
        self.visit(ast.stmt, [is_in_loop, env, False, None, None])
        cond = self.visit(ast.cond, env)
        if type(cond) != BooleanType:
            raise TypeMismatchInStatement(ast)
        
        env = env[1:]
    
    # _________________________________________________________    
    # param (is_in_loop: Bool, env)
    # _________________________________________________________
    def visitBreakStmt(self, ast, param):
        is_in_loop = param[0]
        env = param[1]
        if is_in_loop == False:
            raise MustInLoop(ast)
        else:
            param[0] = False
            return 
            
    # _________________________________________________________    
    # param (is_in_loop: Bool, env)
    # _________________________________________________________
    def visitContinueStmt(self, ast, param): 
        is_in_loop = param[0]
        env = param[1]
        if is_in_loop == False:
            raise MustInLoop(ast)
        else:
            param[0] = False
            return 
    
    # _________________________________________________________
    # Rerturnstmt expr: Expr or None = None
    # # param (is_in_loop: Bool, env, is_function_body: Bool, 
    # Symbol() of current function,
    # Symbol() of parent function)
    # _________________________________________________________
    def visitReturnStmt(self, ast, param):
        env = param[1]
        currentFunc = param[3]
        return_type = None
        if ast.expr is None:
            return_type = VoidType()
        else :
            return_type = type(self.visit(ast.expr, env))
        if currentFunc.returnType == AutoType:
            for sym in env[-1]:
                if sym.name == currentFunc.name:
                    sym.returnType = return_type
        elif type(currentFunc.returnType) != return_type:
            raise TypeMismatchInStatement(ast)
        
        
    # _________________________________________________________
    # CallStmt(Stmt)
    # name: str, args: List[Expr]
    # param (is_in_loop: Bool, env 
    # _________________________________________________________
    def visitCallStmt(self, ast, param):
        env = param[1]
        
        if ast.name == "super" or ast.name == "preventDefault":
            return
        # check function name in local
        for localEnv in env[:-1]:
            for symbol in localEnv: # find id in the current environment
                if ast.name == symbol.name:
                    raise TypeMismatchInStatement(ast) # id is declared in current scope but is not a function
        # check function name in global
        for symbol in env[-1]: # param[-1] is the list of Symbol() in the global environment
            if ast.name == symbol.name:
                if len(ast.args) != len(symbol.param):
                    
                    raise TypeMismatchInStatement(ast)
                for i in range(len(ast.args)):
                    arg = self.visit(ast.args[i], env)
                    if symbol.param[i].returnType == AutoType:
                        inferParam(symbol.name,symbol.param[i].name, arg, env)
                    elif arg == IntegerType and symbol.param[i].returnType == FloatType:
                        # convert the param to float
                        pass
                    elif arg != symbol.param[i].returnType:
                        
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
        for symbol in env[-1]: # param[-1] is the list of Symbol() in the global environment
            if ast.name == symbol.name:
                if len(ast.args) != len(symbol.param):
                    
                    raise TypeMismatchInExpression(ast)
                for i in range(len(ast.args)):
                    
                    arg = self.visit(ast.args[i], env)
                    if symbol.param[i].returnType == AutoType:
                        inferParam(symbol.name,symbol.param[i].name, arg, env)
                    elif arg == IntegerType and symbol.param[i].returnType == FloatType:
                        # convert the param to float
                        pass
                    elif arg != symbol.param[i].returnType:
                        
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
            if intersection([type(leftType), type(rightType)], [BooleanType(), StringType(), VoidType()]):
                raise TypeMismatchInExpression(ast)
            elif type(leftType) == AutoType and type(rightType) == AutoType:
                return FloatType() # testcase khong co 2 cai auto ko suy dien dc, tra ve float tang ti le dung
            elif type(leftType) == AutoType:
                infer(ast.left, type(rightType), param)
                return rightType()
            elif type(rightType) == AutoType:
                infer(ast.right, type(leftType), param)
                return leftType()
            elif type(leftType) == IntegerType and type(rightType) == IntegerType:
                return IntegerType()
            elif type(leftType) == FloatType and type(rightType) == FloatType or type(leftType) == IntegerType and type(rightType) == FloatType or type(leftType) == FloatType and type(rightType) == IntegerType:
                return FloatType()
            else: # arrayType
                raise TypeMismatchInExpression(ast)
            
        elif op in ['%']: # operand type is int
            if intersection([type(leftType), type(rightType)], [BooleanType(), StringType(), VoidType(), FloatType()]):
                raise TypeMismatchInExpression(ast)
            elif type(leftType) == AutoType and type(rightType) == AutoType:
                infer(ast.left, IntegerType, param)
                infer(ast.right, IntegerType, param)
                return IntegerType()
            elif type(leftType) == AutoType:
                infer(ast.left, type(rightType), param)
                return IntegerType()
            elif type(rightType) == AutoType:
                infer(ast.right, type(leftType), param)
                return IntegerType()
            elif type(leftType) == IntegerType and type(rightType) == IntegerType:
                return IntegerType()
            else : # arrayType
                raise TypeMismatchInExpression(ast)
            
        elif op in ['&&', '||']: # operand type is bool
            if intersection([type(leftType), type(rightType)], [IntegerType(), StringType(), VoidType(), FloatType()]):
                raise TypeMismatchInExpression(ast)
            if type(leftType) == AutoType and type(rightType) == AutoType:
                infer(ast.left, BooleanType, param)
                infer(ast.right, BooleanType, param)
                return BooleanType()
            elif type(leftType) == AutoType:
                infer(ast.left, type(rightType), param)
                return BooleanType()
            elif type(rightType) == AutoType:
                infer(ast.right, type(leftType), param)
                return BooleanType()
            elif type(leftType) == BooleanType and type(rightType) == BooleanType:
                return BooleanType()
            else : # arrayType xuat hien
                raise TypeMismatchInExpression(ast)
        elif op in ['<', '>', '<=', '>=', '==', '!=']: # operand type is int/float, return booltype
            
            if intersection([type(leftType), type(rightType)], [BooleanType(), StringType(), VoidType()]):
                raise TypeMismatchInExpression(ast)
            elif type(leftType) == AutoType and type(rightType) == AutoType:
                return BooleanType() # ti le dung cao hon
            elif type(leftType) == AutoType:
                infer(ast.left, type(rightType), param)
                return BooleanType()
            elif type(rightType) == AutoType:
                infer(ast.right, type(leftType), param)
                return BooleanType()
            elif type(leftType) == IntegerType and type(rightType) == IntegerType:
                return BooleanType()
            elif type(leftType) == FloatType and type(rightType) == FloatType or type(leftType) == IntegerType and type(rightType) == FloatType or type(leftType) == FloatType and type(rightType) == IntegerType:
                return BooleanType()
            else :
                raise TypeMismatchInExpression(ast)
            
            
        elif op in ['::']: # operand type is string
            if intersection([type(leftType), type(rightType)], [BooleanType(), IntegerType(), VoidType(), FloatType()]):
                raise TypeMismatchInExpression(ast)
            elif type(leftType) == AutoType and type(rightType) == AutoType:
                infer(ast.left, StringType, param)
                infer(ast.right, StringType, param)
                return StringType()
            elif type(leftType) == AutoType:
                infer(ast.left, type(rightType), param)
                return StringType()
            elif type(rightType) == AutoType:
                infer(ast.right, type(leftType), param)
                return StringType()
            elif type(leftType) == StringType and type(rightType) == StringType:
                return StringType()
            else : # arrayType xuat hien
                raise TypeMismatchInExpression(ast)
    # _________________________________________________________
    # op: str, body: Expr
    # op is Unary: !, -
    # param is env
    # _________________________________________________________
    def visitUnExpr(self, ast, param): 
        op = ast.op
        bodyType = self.visit(ast.body, param)
        if op in ['!']: # operand type is bool
            if type(bodyType) == AutoType:
                infer(ast.body, BooleanType, param)
                return BooleanType()
            elif type(bodyType) == BooleanType:
                return BooleanType()
            else:
                raise TypeMismatchInExpression(ast)
        elif op in ['-']: # operand type is int/float
            if type(bodyType) == AutoType:
                infer(ast.body, IntegerType, param)
                return IntegerType()
            elif type(bodyType) == IntegerType:
                return IntegerType()
            elif type(bodyType) == FloatType:
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
    