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
    def __init__(self, ast):
        self.ast = ast
    def check(self):
        return self.visitProgram(self.ast, [])
    def visitProgram(self, ast, param):
        
        o = param
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
# infer string
# _________________________________________________________
def infer(name, typ, env):
    for symbolList in env:
        for sym in symbolList:
            if sym.name == name:
                sym.returnType = typ
                return typ 
# _________________________________________________________
# infer typ for param_name in func_name
# global_env can be env or prototype
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
        globalScopePrototype = GetEnv(ast).visitProgram(ast, [])
        
        # env[0] += globalEnv
        # second check, check all declare
        
        for decl in ast.decls:
            self.visit(decl, [True,env,globalScopePrototype])
        
        # raise NoEntryPoint() in the end of 2nd check
            
        for func in env[0]:
            if func.name == "main" and func.returnType == VoidType and func.isFunction == True:
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
        if param[0] == True: # in global scope, env = [globalEnv]
            env[0].append(Symbol(ast.name, ast.typ))
        if ast.init is None:
            
            if type(ast.typ) is AutoType: # declare auto type var but no init
                raise Invalid(Variable(),ast.name)
            return Symbol(ast.name, ast.typ)
        
        elif ast.init is not None:
            # if ast.typ is ArrayType:
            exprType = self.visit(ast.init, env)
            if type(ast.typ) is AutoType:
                return Symbol(ast.name, exprType)
            elif type(ast.typ) is IntegerType and type(exprType) is FloatType:
                raise TypeMismatchInVarDecl(ast)
            elif type(ast.typ) is FloatType and type(exprType) is IntegerType:
                return Symbol(ast.name, ast.typ)
            elif type(ast.typ) is not type(exprType): # khong dung type de so sanh truc tiep dimension and type of array
                raise TypeMismatchInVarDecl(ast)
            else:
                if ast.typ != exprType: # check array type
                    raise TypeMismatchInVarDecl(ast)
                return Symbol(ast.name, ast.typ)
            
            
        
    # _____________________________________________________________
    # name: str, return_type: Type, params: List[ParamDecl], inherit: str or None, body: BlockStmt
    # param (isGlobal: Bool, env ,[Symbol()] in global scope)
    # _____________________________________________________________
    def visitFuncDecl(self, ast, param):
        env = param[1]
        # global duyet ban dau prototype, 
        # chi dung de check ham cha viet sau ham con, chua dc khai bao
        globalScopePrototype = param[2] 
        
        # them cac ten cua param vao local_scope
        listParam = ast.params 
        localEnv = []
        # check redeclare function
        for sym in env[0]:
            if sym.name == ast.name:
                raise Redeclared(Function(), ast.name) # function is already declared
        symInfered = False
        for sym in globalScopePrototype:
            if sym.name == ast.name:
                symInfered = sym
                break
        # infer return type for function, and type of param 
        # ast.return_type = type(symInfered.returnType)
        # visit and check redeclare param
        paramList = []
        for i in ast.params:
            paramList.append(self.visit(i, paramList))
            
        # create function symbol
        # funcSymbol = Symbol(ast.name, ast.return_type, True, paramList, ast.inherit)
        # add function symbol to local scope
        # env[0] += [funcSymbol]
        # symbol been infered to scope
        env[0] += [symInfered]
        # add param to local scope, which is inferd
        listParam = symInfered.param
        for i in listParam:
            localEnv += [Symbol(i.name, i.returnType)]
        # create new scope
        env = [[]] + env
        env[0] = localEnv            
        # check if the function inherits from another function
        parent_function = None
        
            
            
            
        # visit block statement
        # stmt param (is_in_loop: Bool, env,  is_function_body: Bool, Symbol() of current function,Symbol() of parent function, is_init_for: Bool, globalScopePrototype)
        self.visit(ast.body, [False, env, True, symInfered ,parent_function, False, globalScopePrototype])
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
    # stmt param (is_in_loop: Bool, env, False, None, None, is_init_for: Bool)
    # _________________________________________________________
    def visitAssignStmt(self, ast, param):
        env = param[1]
        is_init_for = param[5]
        rightType = self.visit(ast.rhs, env)
        leftType = self.visit(ast.lhs, env)

        if is_init_for: 
            if type(leftType) is not IntegerType:
                raise TypeMismatchInStatement(ast)
            
        if type(leftType) is AutoType:            
            infer(ast.lhs, rightType, env)
            return 
        elif type(rightType) is AutoType:
            infer(ast.rhs, leftType, env)
            return 
        elif type(leftType) is IntegerType and type(rightType) is FloatType:
            raise TypeMismatchInStatement(ast)
        elif type(leftType) is FloatType and type(rightType) is IntegerType:
            pass
        elif type(leftType) is not type(rightType):
            raise TypeMismatchInStatement(ast)
        else: # leftType == rightType
            return
    
    # *********************************************************
    # blockstmt is using by function or other stmt
    # if blockstmt is call from function, env is created in visitFuncDecl (1)
    # if blockstmt is call from other stmt, env is created in here (2)
    #       in case (1): if inherit, parentfunc is Symbol of parent function, 
    #                     has been checked in visitFuncDecl
    # _________________________________________________________
    # BlockStmt body: List[Stmt or VarDecl]
    # stmt param (is_in_loop: Bool, env, is_function_body: Bool, 
    # Symbol() of current function,
    # Symbol() of parent function) # not used
    # is_init_for: Bool, 
    # globalScopePrototype
    # [7] is_init_if: Bool 
    # _________________________________________________________
    def visitBlockStmt(self, ast, param):
        is_in_loop = param[0]
        env = param[1]
        is_func_body = param[2]
        current_func = param[3]
        # parent_func = param[4]
        localEnv = []
        prototypeEnv = param[6]
        # ____________________
        # case block statement is function body, 
        # be called from visitFuncDecl,
        # local env has been created in visitFuncDecl
        
        if current_func.inherit is not None:
            # check function name in env, if not found, check in prototype, and infer param and return type
            parentFuncName = current_func.inherit 
            beFound = 0 # 0: not found, 1: found in env, 2: found in prototype
            parent_function = None
            for symbol in env[-1]:
                if symbol.name == parentFuncName:
                    beFound = 1
                    parent_function = symbol
                    break
            
            if beFound == 0:
                for symbol in prototypeEnv:
                    if symbol.name == parentFuncName:
                        beFound = 2
                        parent_function = symbol
                        break
            # parent function is not found
            if beFound == 0:
                raise Undeclared(Function(), parentFuncName)
            # check parent is a function when call super
            if parent_function.isFunction == False:
                raise Undeclared(Function(), parentFuncName)
            
            # case call super or preventdefault
            if len(ast.body) > 0 and type(ast.body[0]) is CallStmt:
                # name: str, args: List[Expr]
                # expr la CallStmt 
                expr = ast.body[0]
                if expr.name == "super":
                    # check parent is a function
                    
                    # visit father function, env[-1] is global scope
                    # get name and type of params of parent function
                    parent_params = parent_function.param
                    if len(expr.args) > len(parent_params):
                        raise TypeMismatchInExpression(expr.args[len(parent_params)]) # raise args du thua dau tien
                    elif len(expr.args) < len(parent_params):
                        raise TypeMismatchInExpression()
                    
                    # check type of each param of super function and the parent function
                    for i in range(len(expr.args)):
                        typArgs = self.visit(expr.args[i], env)
                        if type(typArgs) is AutoType and type(parent_function[i].returnType) is AutoType:
                            pass # not error type cannot be inferred
                        elif type(typArgs) is AutoType: # infer the type of param in father function for id in super function
                            infer(expr.args[i].name, parent_params[i].returnType, globalEnv)
                            pass 
                        elif type(parent_params[i].returnType) is AutoType: # infer the type of param in super function for father function
                            inferParam(parent_function.name,parent_function.param[i].name, typArgs, env[-1] if beFound == 1 else prototypeEnv)
                        elif type(typArgs) is IntegerType and type(parent_params[i].returnType) is FloatType:
                            # convert the integer type param to float
                            pass
                        elif type(typArgs) is not type(parent_params[i].returnType):
                            raise TypeMismatchInExpression(expr.args[i]) # args dau tien khong khop kieu
                        else: # expr.args[i] is parent_params[i]                            
                            pass
                    # check if the name of params turn out 2 times
                    
                    
                    
                    # check if the name of params inherit in father function is the same as the name of params in function
                    # if not, add the param to the current environment                    
                    for param in parent_params:
                        for symbol in env[0]:
                            if param.name == symbol.name and param.inherit == True:
                                raise Invalid(Parameter(), param.name)
                        if param.inherit == True:
                            env[0] += [Symbol(param.name, param.returnType)]
                        # else: # param.inherit == False
                        
                    
                    
                    
                elif expr.name == "preventDefault":
                    # khong goi super()
                    pass
                else: # firststmt is another callfunc, -> goi ham super() khong tham so
                    if len(parent_params) != 0:
                        raise TypeMismatchInStatement()
                    else: # ham cha khong co tham so nen ko thua huong
                        pass
            
                        
        else: # non inherit case, special func for inherit cannot be called
            if len(ast.body) > 0:
                stmt = ast.body[0]
                if type(stmt) is CallStmt and (stmt.name == "preventDefault" or stmt.name == "super"):
                    raise TypeMismatchInStatement(ast.body[0])
            pass
        
        # --------------------------------------------------------
        # case block is_block_body, be called from other statement
        # local env create here          
        if is_func_body == False: 
            # create new scope
            env = [[]] + env
            env[0] = localEnv  
        
        # xu ly chung cho ca 2 truong hop funcbody va blockbody
        
        for stmt in ast.body:
            
            if isinstance(stmt, VarDecl):
                env[0].append(self.visit(stmt, [is_in_loop, env, False, current_func, None, False, prototypeEnv, False]))
            else: # stmt is Stmt
                self.visit(stmt, [is_in_loop, env, False, current_func, None, False, prototypeEnv, False])
        # if block is blockbody, local env is removed here
        # if block is function body, local env is removed in visitFuncDecl
        if is_func_body == False: 
            env = env[1:]
        return 
    # _________________________________________________________    
    # cond: Expr, tstmt: Stmt, fstmt: Stmt or None = None
    # stmt param (is_in_loop: Bool, env, is_function_body: Bool, 
    # Symbol() of current function,
    # Symbol() of parent function) # not used
    # is_init_for: Bool, 
    # globalScopePrototype
    # 7 in_if_stmt: Bool
    # _________________________________________________________
    def visitIfStmt(self, ast, param):
        is_in_loop = param[0]
        env = param[1]
        cond = self.visit(ast.cond, env)
            
        if type(cond) is not BooleanType:
            raise TypeMismatchInStatement(ast) # tiep tuc truyen tham so cho visit stmt
        tstmt = self.visit(ast.tstmt, [is_in_loop, env, param[2], param[3], param[4], False, param[6], True]) 
        fstmt = None
        if ast.fstmt is not None:
            fstmt = self.visit(ast.fstmt, [is_in_loop, env, param[2], param[3], param[4], False, param[6], True])
            
    # _________________________________________________________    
    # init: AssignStmt, cond: Expr, upd: Expr, stmt: Stmt
    # stmt param (is_in_loop: Bool, env)
    # _________________________________________________________  
    def visitForStmt(self, ast, param):
        is_in_loop = param[0]
        env = param[1]
        is_in_loop = True
        assignStmt = self.visit(ast.init, [is_in_loop, env, param[2], param[3], None, True, param[6], param[7]]) # id for assignStmt duoc chuan bi ti truoc, khong khoi tao luc nay, id nay kieu int
        
        cond = self.visit(ast.cond, env)
        if type(cond) != BooleanType:
            raise TypeMismatchInStatement(ast)
        upd = self.visit(ast.upd, env)
        if type(upd) != IntegerType:
            raise TypeMismatchInStatement(ast)

        env = [[]] + env
        self.visit(ast.stmt, [is_in_loop, env, param[2], param[3], None, False, param[6]])
        env = env[1:]
    
    # _________________________________________________________    
    # cond: Expr, stmt: Stmt
    # stmt param (is_in_loop: Bool, env)
    # _________________________________________________________
    def visitWhileStmt(self, ast, param): 
        is_in_loop = param[0]
        env = param[1]
        is_in_loop = True
        funcSym = param[3]
        cond = self.visit(ast.cond, env)
        if type(cond) != BooleanType:
            raise TypeMismatchInStatement(ast)
        
        env = [[]] + env
        self.visit(ast.stmt, [is_in_loop, env, False, funcSym, None, False, param[6]])
        env = env[1:]
        
    # _________________________________________________________    
    # cond: Expr, stmt: BlockStmt
    # stmt param (is_in_loop: Bool, env)
    # _________________________________________________________
    def visitDoWhileStmt(self, ast, param): 
        is_in_loop = param[0]
        env = param[1]
        is_in_loop = True
        
        env = [[]] + env
        self.visit(ast.stmt, [is_in_loop, env, False, None, None, param[6]])
        cond = self.visit(ast.cond, env)
        if type(cond) != BooleanType:
            raise TypeMismatchInStatement(ast)
        
        env = env[1:]
    
    # _________________________________________________________    
    # stmt param (is_in_loop: Bool, env)
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
    # stmt param (is_in_loop: Bool, env)
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
    # # stmt param (is_in_loop: Bool, env, is_function_body: Bool, 
    # Symbol() of current function,
    # Symbol() of parent function)
    # _________________________________________________________
    def visitReturnStmt(self, ast, param):
        env = param[1]
        currentFunc = param[3]
        return_type = None
        
        if ast.expr is None: # dung == la error luon
            return_type = VoidType()
        else :
            return_type = self.visit(ast.expr, env)
        
        for sym in env[-1]:
            if sym.name == currentFunc.name:
                currentFunc = sym
        if currentFunc.returnType is AutoType():
            for sym in env[-1]:
                if sym.name == currentFunc.name:
                    sym.returnType = return_type
        if type(currentFunc.returnType) is type(return_type):
            return
        else:
            raise TypeMismatchInStatement(ast)
        
    # _________________________________________________________
    # CallStmt(Stmt)
    # name: str, args: List[Expr]
    # stmt param (is_in_loop: Bool, env 
    # _________________________________________________________
    def visitCallStmt(self, ast, param):
        env = param[1]
        prototype = param[6]
        if ast.name == "super" or ast.name == "preventDefault":
            return
        # check function name in local
        for localEnv in env[:-1]:
            for symbol in localEnv: # find id in the current environment
                if ast.name == symbol.name:
                    raise TypeMismatchInStatement(ast) # id is declared in current scope but is not a function
        # check function name in env, if not found, check in prototype, and infer param and return type
        beFound = 0 # 0: not found, 1: found in env, 2: found in prototype
        funcSym = None
        for symbol in env[-1]:
            if symbol.name == ast.name:
                beFound = 1
                funcSym = symbol
                break
        
        if beFound == 0:
            for symbol in prototype:
                if symbol.name == ast.name:
                    beFound = 2
                    funcSym = symbol
                    break
        if beFound == 0:
            raise Undeclared(Function(), ast.name)
            

        if funcSym.isFunction == False:
            raise TypeMismatchInStatement(ast) 
        if len(ast.args) > len(funcSym.param):
            raise TypeMismatchInExpression(ast.args[len(funcSym.param)])
        elif len(ast.args) < len(funcSym.param):
            raise TypeMismatchInExpression()
        for i in range(len(ast.args)):
            arg = self.visit(ast.args[i], env)
            if type(funcSym.param[i].returnType) is AutoType:
                inferParam(funcSym.name,funcSym.param[i].name, arg, env[-1] if beFound == 1 else prototype)
            elif type(arg) is IntegerType and type(funcSym.param[i].returnType) is FloatType:
                # convert the param to float
                pass
            elif type(arg) is not type(funcSym.param[i].returnType):
                
                raise TypeMismatchInStatement(ast)
        return # stmt chi check loi, khong tra ve kieu
        
    
    # _________________________________________________________
    # FuncCall(Expr)
    # name: str, args: List[Expr]
    # param env 
    # _________________________________________________________
    def visitFuncCall(self, ast, param):
        env = param
        for localEnv in env[:-1]: # find lan luot tu local ra global
            for symbol in localEnv: # find id in the current environment
                if ast.name == symbol.name and symbol.isFuntion == False:
                    
                    raise TypeMismatchInExpression(ast) # id is declared in current scope but is not a function
        for symbol in env[-1]: # param[-1] is the list of Symbol() in the global environment
            if ast.name == symbol.name:
                if len(ast.args) > len(symbol.param):
                    raise TypeMismatchInExpression(ast.args[len(symbol.param)])
                elif len(ast.args) < len(symbol.param):
                    raise TypeMismatchInExpression()
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
            elif type(leftType) is AutoType and type(rightType) is AutoType:
                return FloatType() # testcase khong co 2 cai auto ko suy dien dc, tra ve float tang ti le dung
            elif type(leftType) is AutoType:
                infer(ast.left, type(rightType), param)
                return rightType()
            elif type(rightType) is AutoType:
                infer(ast.right, type(leftType), param)
                return leftType()
            elif type(leftType) is IntegerType and type(rightType) is IntegerType:
                return IntegerType()
            elif type(leftType) is FloatType and type(rightType) is FloatType or type(leftType) is IntegerType and type(rightType) is FloatType or type(leftType) is FloatType and type(rightType) is IntegerType:
                return FloatType()
            else: # arrayType
                raise TypeMismatchInExpression(ast)
            
        elif op in ['%']: # operand type is int
            if intersection([type(leftType), type(rightType)], [BooleanType(), StringType(), VoidType(), FloatType()]):
                raise TypeMismatchInExpression(ast)
            elif type(leftType) is AutoType and type(rightType) is AutoType:
                infer(ast.left, IntegerType, param)
                infer(ast.right, IntegerType, param)
                return IntegerType()
            elif type(leftType) is AutoType:
                infer(ast.left, type(rightType), param)
                return IntegerType()
            elif type(rightType) is AutoType:
                infer(ast.right, type(leftType), param)
                return IntegerType()
            elif type(leftType) is IntegerType and type(rightType) is IntegerType:
                return IntegerType()
            else : # arrayType
                raise TypeMismatchInExpression(ast)
            
        elif op in ['&&', '||']: # operand type is bool
            if intersection([type(leftType), type(rightType)], [IntegerType(), StringType(), VoidType(), FloatType()]):
                raise TypeMismatchInExpression(ast)
            if type(leftType) is AutoType and type(rightType) is AutoType:
                infer(ast.left, BooleanType, param)
                infer(ast.right, BooleanType, param)
                return BooleanType()
            elif type(leftType) is AutoType:
                infer(ast.left, type(rightType), param)
                return BooleanType()
            elif type(rightType) is AutoType:
                infer(ast.right, type(leftType), param)
                return BooleanType()
            elif type(leftType) is BooleanType and type(rightType) is BooleanType:
                return BooleanType()
            else : # arrayType xuat hien
                raise TypeMismatchInExpression(ast)
        elif op in ['<', '>', '<=', '>=', '==', '!=']: # operand type is int/float, return booltype    
            if intersection([type(leftType), type(rightType)], [BooleanType(), StringType(), VoidType()]):
                raise TypeMismatchInExpression(ast)
            elif type(leftType) is AutoType and type(rightType) is AutoType:
                return BooleanType() # ti le dung cao hon
            elif type(leftType) is AutoType:
                infer(ast.left, type(rightType), param)
                return BooleanType()
            elif type(rightType) is AutoType:
                infer(ast.right, type(leftType), param)
                return BooleanType()
            elif type(leftType) is IntegerType and type(rightType) is IntegerType:
                return BooleanType()
            elif type(leftType) is FloatType and type(rightType) is FloatType or type(leftType) is IntegerType and type(rightType) is FloatType or type(leftType) is FloatType and type(rightType) is IntegerType:
                return BooleanType()
            else :
                raise TypeMismatchInExpression(ast)
            
            
        elif op in ['::']: # operand type is string
            if intersection([type(leftType), type(rightType)], [BooleanType(), IntegerType(), VoidType(), FloatType()]):
                raise TypeMismatchInExpression(ast)
            elif type(leftType) is AutoType and type(rightType) is AutoType:
                infer(ast.left, StringType, param)
                infer(ast.right, StringType, param)
                return StringType()
            elif type(leftType) is AutoType:
                infer(ast.left, type(rightType), param)
                return StringType()
            elif type(rightType) is AutoType:
                infer(ast.right, type(leftType), param)
                return StringType()
            elif type(leftType) is StringType and type(rightType) is StringType:
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
            if type(bodyType) is AutoType:
                infer(ast.body, BooleanType, param)
                return BooleanType()
            elif type(bodyType) is BooleanType:
                return BooleanType()
            else:
                raise TypeMismatchInExpression(ast)
        elif op in ['-']: # operand type is int/float
            if type(bodyType) is AutoType:
                infer(ast.body, IntegerType, param)
                return IntegerType()
            elif type(bodyType) is IntegerType:
                return IntegerType()
            elif type(bodyType) is FloatType:
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
        # thu tu check tu ngoai vao trong, check id, check length, check type exp
        env = param
        # find array in env
        arr = None
        for i in env:
            for sym in i:
                if ast.name == sym.name:
                    arr = sym.returnType
        if arr is None:
            raise Undeclared(Identifier(), ast.name)
        # check cell
        if arr not in [IntegerType(), FloatType(), BooleanType(), StringType(), VoidType(), AutoType()]:
            # check length
            if len(ast.cell) > len(arr.dimensions):
                raise TypeMismatchInExpression(ast.cell[len(arr.dimensions)]) # exp du thua dau tien
            elif len(ast.cell) < len(arr.dimensions):
                raise TypeMismatchInExpression() # voi dau vao rong, tuong tu giai thich super
            # check type
            for i in range(len(ast.cell)):
                typCell = self.visit(ast.cell[i], param)
                if typCell is not IntegerType():
                    raise TypeMismatchInExpression(ast.cell[i])
            return arr.typ
        else: # id khong phai la array
            raise TypeMismatchInExpression(ast.name)
        
    
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
    