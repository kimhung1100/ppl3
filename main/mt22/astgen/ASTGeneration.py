from MT22Visitor import MT22Visitor
from MT22Parser import MT22Parser
from AST import *

from functools import reduce
class ASTGeneration(MT22Visitor):
    # program: declare+ EOF ;
    def visitProgram(self, ctx:MT22Parser.ProgramContext):
        declares = reduce(lambda x, y: x + y, [self.visit(x) for x in ctx.declare()])
        return Program(declares)


    # var_declare | func_declare ;
    def visitDeclare(self, ctx:MT22Parser.DeclareContext):
        if ctx.var_declare():
            return self.visit(ctx.var_declare())
        elif ctx.func_declare():
            return self.visit(ctx.func_declare())


    # var_declare: short_form | init_var;
    def visitVar_declare(self, ctx:MT22Parser.Var_declareContext):
        if ctx.short_form():
            return self.visit(ctx.short_form())
        else :
            return self.visit(ctx.init_var())


    # short_form: identifier_list CL type_decl SM; 
    def visitShort_form(self, ctx:MT22Parser.Short_formContext):
        ids = self.visit(ctx.identifier_list())
        typ = self.visit(ctx.type_decl())
        return [VarDecl(x, typ, None) for x in ids]


    # identifier_list: ID CM identifier_list | ID;
    def visitIdentifier_list(self, ctx:MT22Parser.Identifier_listContext):
        if ctx.identifier_list():
            return [ctx.ID().getText()] + self.visit(ctx.identifier_list())
        else:
            return [ctx.ID().getText()]


    # init_var: ID pair exp SM;
    def visitInit_var(self, ctx:MT22Parser.Init_varContext):
        idsTypExp = [ctx.ID().getText()] + self.visit(ctx.pair()) + [self.visit(ctx.exp())]
        n = len(idsTypExp)
        if n >= 3:
            ids = idsTypExp[0:n//2]
            typ = idsTypExp[n//2]
            exp = idsTypExp[n//2+1:]
            return list (map(lambda x: VarDecl(x[0], typ, x[1]), zip(ids, exp)))
        else:
            return list(VarDecl(self.visit(ctx.ID()), idsTypExp[0], self.visit(ctx.exp())))
        


    # pair: CM ID pair exp CM | CL type_decl_init  EQ;
    def visitPair(self, ctx:MT22Parser.PairContext):
        if ctx.pair():
            return [ctx.ID().getText()] + self.visit(ctx.pair()) + [self.visit(ctx.exp())]

        else :
            return [self.visit(ctx.type_decl_init())]


    # type_decl_init: atomic_type | auto_type | array_type;
    def visitType_decl_init(self, ctx:MT22Parser.Type_decl_initContext):
        if ctx.atomic_type():
            return self.visit(ctx.atomic_type())
        elif ctx.auto_type():
            return self.visit(ctx.auto_type())
        else :
            return self.visit(ctx.array_type())


    # parameter_list_declare_infunc: LB parameter_list_declare RB;
    def visitParameter_list_declare_infunc(self, ctx:MT22Parser.Parameter_list_declare_infuncContext):
        return self.visit(ctx.parameter_list_declare())


    # parameter_list_declare: parameter_declare CM parameter_list_declare | parameter_declare | ;
    def visitParameter_list_declare(self, ctx:MT22Parser.Parameter_list_declareContext):
        if ctx.parameter_list_declare():
            return [self.visit(ctx.parameter_declare())] + self.visit(ctx.parameter_list_declare())
        elif ctx.parameter_declare():
            return [self.visit(ctx.parameter_declare())]
        else:
            return []

    # # parameter_declare: ID CL type_parameter                         // parameter type not be void
	# 				| INHERIT ID CL type_parameter
	# 				| OUT ID CL type_parameter
	# 				| INHERIT OUT ID CL type_parameter;
    def visitParameter_declare(self, ctx:MT22Parser.Parameter_declareContext):
        if ctx.INHERIT() and ctx.OUT():
            return ParamDecl(ctx.ID().getText(), self.visit(ctx.type_parameter()), True, True)
        elif ctx.INHERIT():
            return ParamDecl(ctx.ID().getText(), self.visit(ctx.type_parameter()), False, True)
        elif ctx.OUT():
            return ParamDecl(ctx.ID().getText(), self.visit(ctx.type_parameter()), True, False)
        else:
            return ParamDecl(ctx.ID().getText(), self.visit(ctx.type_parameter()), False, False)

    # type_parameter: atomic_type | array_type | auto_type;
    def visitType_parameter(self, ctx:MT22Parser.Type_parameterContext):
        if ctx.atomic_type():
            return self.visit(ctx.atomic_type())
        elif ctx.array_type():
            return self.visit(ctx.array_type())
        else:
            return self.visit(ctx.auto_type())


    # # func_declare: ID CL FUNCTION type_return                           // return type can be array, auto, void 
	# 		parameter_list_declare_infunc 
	# 		(LSB INHERIT ID RSB)
	# 		block_statement
	# 		| ID CL FUNCTION type_return 
	# 		parameter_list_declare_infunc 
	# 		block_statement;
 
    # self.name = name
    #     self.return_type = return_type
    #     self.params = params
    #     self.inherit = inherit
    #     self.body = body
    def visitFunc_declare(self, ctx:MT22Parser.Func_declareContext):
        return [FuncDecl(ctx.ID(0).getText(), 
                    self.visit(ctx.type_return()), 
                    self.visit(ctx.parameter_list_declare_infunc()),
                    ctx.ID(1).getText() if ctx.ID(1) else None,
                    self.visit(ctx.block_statement()))]


    # type_return: atomic_type | array_type | void_type | auto_type;
    def visitType_return(self, ctx:MT22Parser.Type_returnContext):
        if ctx.atomic_type():
            return self.visit(ctx.atomic_type())
        elif ctx.array_type():
            return self.visit(ctx.array_type())
        elif ctx.auto_type():
            return self.visit(ctx.auto_type())
        else:
            return self.visit(ctx.void_type())


    # type_decl: atomic_type | array_type | auto_type;
    def visitType_decl(self, ctx:MT22Parser.Type_declContext):
        if ctx.atomic_type():
            return self.visit(ctx.atomic_type())
        elif ctx.array_type():
            return self.visit(ctx.array_type())
        elif ctx.auto_type():
            return self.visit(ctx.auto_type())
        


    # atomic_type: BOOLEAN | INTEGER | FLOAT | STRING;
    def visitAtomic_type(self, ctx:MT22Parser.Atomic_typeContext):
        if ctx.BOOLEAN():
            return BooleanType()
        elif ctx.INTEGER():
            return IntegerType()
        elif ctx.FLOAT():
            return FloatType()
        else:
            return StringType()


    # array_type: ARRAY LSB dimension RSB OF atomic_type;
    def visitArray_type(self, ctx:MT22Parser.Array_typeContext):
        return ArrayType(self.visit(ctx.dimension()), self.visit(ctx.atomic_type()))


    # dimension: INTLIT CM dimension | INTLIT;
    def visitDimension(self, ctx:MT22Parser.DimensionContext):
        if ctx.dimension():
            return [int(ctx.INTLIT().getText())] + self.visit(ctx.dimension())
        else :
            return [int(ctx.INTLIT().getText())]


    # void_type: VOID;
    def visitVoid_type(self, ctx:MT22Parser.Void_typeContext):
        return VoidType()


    # auto_type: AUTO;
    def visitAuto_type(self, ctx:MT22Parser.Auto_typeContext):
        return AutoType()


    # exp: exp1 DC exp1 | exp1; 
    def visitExp(self, ctx:MT22Parser.ExpContext):
        if ctx.DC():
            return BinExpr(ctx.DC().getText(), self.visit(ctx.exp1(0)), self.visit(ctx.exp1(1)))
        else :
            return self.visit(ctx.exp1(0))


    # exp1: exp2 (relational) exp2 | exp2;  
    def visitExp1(self, ctx:MT22Parser.Exp1Context):
        if ctx.relational():
            return BinExpr(ctx.relational().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
        else:
            return self.visit(ctx.exp2(0))


    # relational: DEQ | NEQ | LT | LE | GT | GE;
    def visitRelational(self, ctx:MT22Parser.RelationalContext):
        return self.visitChildren(ctx).getText()


    # exp2: exp2 (logical) exp3 | exp3;
    def visitExp2(self, ctx:MT22Parser.Exp2Context):
        if ctx.logical():
            return BinExpr(ctx.logical().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
        else:
            return self.visit(ctx.exp3())

    # logical: AND | OR;
    def visitLogical(self, ctx:MT22Parser.LogicalContext):
        return self.visitChildren(ctx).getText()


    # exp3 (adding) exp4 | exp4; 
    def visitExp3(self, ctx:MT22Parser.Exp3Context):
        if ctx.adding():
            return BinExpr(ctx.adding().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
        else:
            return self.visit(ctx.exp4())


    # adding: ADD | SUB;
    def visitAdding(self, ctx:MT22Parser.AddingContext):
        return self.visitChildren(ctx)


    # exp4 (multiplying) exp5 | exp5;  
    def visitExp4(self, ctx:MT22Parser.Exp4Context):
        if ctx.multiplying():
            return BinExpr(ctx.multiplying().getText(), self.visit(ctx.exp4()), self.visit(ctx.exp5()))
        else:
            return self.visit(ctx.exp5())


    # multiplying: MUL | DIV | MOD;
    def visitMultiplying(self, ctx:MT22Parser.MultiplyingContext):
        return self.visitChildren(ctx)


    # exp5: NOT exp5 | exp6;
    def visitExp5(self, ctx:MT22Parser.Exp5Context):
        if ctx.NOT():
            return UnExpr(ctx.NOT().getText(), self.visit(ctx.exp5()))
        else:
            return self.visit(ctx.exp6())


    # SUB exp6 | exp7;
    def visitExp6(self, ctx:MT22Parser.Exp6Context):
        if ctx.SUB():
            return UnExpr(ctx.SUB().getText(), self.visit(ctx.exp6()))
        return self.visit(ctx.exp7())
        


    # exp7: index_operator | operands;
    def visitExp7(self, ctx:MT22Parser.Exp7Context):
        if(ctx.index_operator()):
            return self.visit(ctx.index_operator())
        else:
            return self.visit(ctx.operands())


    # index_operator: ID LSB exp_list_array RSB;
    def visitIndex_operator(self, ctx:MT22Parser.Index_operatorContext):
        return ArrayCell(ctx.ID().getText(), self.visit(ctx.exp_list_array()))


    # exp_list_array: exp CM exp_list_array | exp | ;
    def visitExp_list_array(self, ctx:MT22Parser.Exp_list_arrayContext):
        if ctx.CM():
            return [self.visit(ctx.exp())] + self.visit(ctx.exp_list_array())
        elif ctx.exp():
            return [self.visit(ctx.exp())]
        else:
            return []


    # ID | INTLIT | FLOATLIT | (TRUE | FALSE) | STRINGLIT | arraylit | LB exp RB | function_call;
    def visitOperands(self, ctx:MT22Parser.OperandsContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.INTLIT():
            return IntegerLit(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLit(float(ctx.FLOATLIT().getText()))
        elif ctx.TRUE():
            return BooleanLit(True)
        elif ctx.FALSE():
            return BooleanLit(False)
        elif ctx.STRINGLIT():
            return StringLit(ctx.STRINGLIT().getText())
        elif ctx.arraylit():
            return self.visit(ctx.arraylit())
        elif ctx.LB():
            return self.visit(ctx.exp())
        elif ctx.function_call():
            return self.visit(ctx.function_call())
        


    # ID LB exp_list_call RB;
    def visitFunction_call(self, ctx:MT22Parser.Function_callContext):
        return FuncCall(ctx.ID().getText(), self.visit(ctx.exp_list_call()))


    # statement: assign_statement | if_statement | for_statement 
    # | while_statement | do_while_statement | return_statement 
    # | call_statement | block_statement | continue | break | match_statement | unmatch_statement;
    def visitStatement(self, ctx:MT22Parser.StatementContext):
        if ctx.assign_statement():
            return self.visit(ctx.assign_statement())
        elif ctx.for_statement():
            return self.visit(ctx.for_statement())
        elif ctx.while_statement():
            return self.visit(ctx.while_statement())
        elif ctx.do_while_statement():
            return self.visit(ctx.do_while_statement())
        elif ctx.return_statement():
            return self.visit(ctx.return_statement())
        elif ctx.call_statement():
            return self.visit(ctx.call_statement())
        elif ctx.block_statement():
            return self.visit(ctx.block_statement())
        elif ctx.continue_statement():
            return self.visit(ctx.continue_statement())
        elif ctx.break_statement():
            return self.visit(ctx.break_statement())
        elif ctx.match_statement():
            return self.visit(ctx.match_statement())
        elif ctx.unmatch_statement():
            return self.visit(ctx.unmatch_statement())
            


    # lhs EQ exp SM;
    def visitAssign_statement(self, ctx:MT22Parser.Assign_statementContext):
        return AssignStmt(self.visit(ctx.lhs()), self.visit(ctx.exp()))


    # lhs: ID | index_expression;
    def visitLhs(self, ctx:MT22Parser.LhsContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.index_expression():
            return self.visit(ctx.index_expression())


    # index_expression: ID LSB exp_list_array RSB;
    def visitIndex_expression(self, ctx:MT22Parser.Index_expressionContext):
        return ArrayCell(ctx.ID().getText(), self.visit(ctx.exp_list_array()))


    # IF LB exp RB match_statement ELSE match_statement | other_statement;
    def visitMatch_statement(self, ctx:MT22Parser.Match_statementContext):
        if ctx.ELSE():
            return IfStmt(self.visit(ctx.exp()), self.visit(ctx.match_statement(0)), self.visit(ctx.match_statement(1)))
        else :
            return self.visit(ctx.other_statement())


    # assign_statement | for_statement | while_statement | do_while_statement 
	#	| return_statement | call_statement | block_statement| continue_statement| break_statement;
    def visitOther_statement(self, ctx:MT22Parser.Other_statementContext):
        # same as statement but without match_statement and unmatch_statement
        if ctx.assign_statement():
            return self.visit(ctx.assign_statement())
        elif ctx.for_statement():
            return self.visit(ctx.for_statement())
        elif ctx.while_statement():
            return self.visit(ctx.while_statement())
        elif ctx.do_while_statement():
            return self.visit(ctx.do_while_statement())
        elif ctx.return_statement():
            return self.visit(ctx.return_statement())
        elif ctx.call_statement():
            return self.visit(ctx.call_statement())
        elif ctx.block_statement():
            return self.visit(ctx.block_statement())
        elif ctx.continue_statement():
            return self.visit(ctx.continue_statement())
        elif ctx.break_statement():
            return self.visit(ctx.break_statement())


    # IF LB exp RB statement 
	#| IF LB exp RB match_statement ELSE unmatch_statement;
				
    def visitUnmatch_statement(self, ctx:MT22Parser.Unmatch_statementContext):
        if ctx.ELSE():
            return IfStmt(self.visit(ctx.exp()), self.visit(ctx.match_statement()), self.visit(ctx.unmatch_statement()))
        else:
            return IfStmt(self.visit(ctx.exp()), self.visit(ctx.statement()), None)


    # for_statement: FOR LB scalar_init_expr CM condition_expr CM update_expr RB statement;
    def visitFor_statement(self, ctx:MT22Parser.For_statementContext):
        return ForStmt(self.visit(ctx.scalar_init_expr()), self.visit(ctx.condition_expr()), self.visit(ctx.update_expr()), self.visit(ctx.statement()))


    # scalar_init_expr: scalar_var EQ exp;
    def visitScalar_init_expr(self, ctx:MT22Parser.Scalar_init_exprContext):
        return AssignStmt(self.visit(ctx.scalar_var()), self.visit(ctx.exp()))
    
    # scalar_var: ID | index_operator;
    def visitScalar_var(self, ctx:MT22Parser.Scalar_varContext):
        if (ctx.ID()):
            return Id(ctx.ID().getText())
        else :
            return self.visit(ctx.index_operator())
        
    # condition_expr: exp;
    def visitCondition_expr(self, ctx:MT22Parser.Condition_exprContext):
        return self.visit(ctx.exp())


    # update_expr: exp;
    def visitUpdate_expr(self, ctx:MT22Parser.Update_exprContext):
        return self.visit(ctx.exp())


    # while_statement: WHILE LB exp RB statement
    def visitWhile_statement(self, ctx:MT22Parser.While_statementContext):
        return WhileStmt(self.visit(ctx.exp()), self.visit(ctx.statement()))


    # do_while_statement: DO block_statement WHILE LB exp RB SM;
        # self.cond = cond
        #     self.stmt = stmt
    def visitDo_while_statement(self, ctx:MT22Parser.Do_while_statementContext):
        return DoWhileStmt(self.visit(ctx.exp()), self.visit(ctx.block_statement()))


    # BREAK SM;
    def visitBreak_statement(self, ctx:MT22Parser.Break_statementContext):
        return BreakStmt()


    # continue_statement: CONTINUE SM;
    def visitContinue_statement(self, ctx:MT22Parser.Continue_statementContext):
        return ContinueStmt()


    # return_statement: RETURN exp SM | RETURN SM;
    def visitReturn_statement(self, ctx:MT22Parser.Return_statementContext):
        if ctx.exp():
            return ReturnStmt(self.visit(ctx.exp()))
        else:
            return ReturnStmt(None)


    # ID LB exp_list_call RB SM;
    def visitCall_statement(self, ctx:MT22Parser.Call_statementContext):
        return CallStmt(ctx.ID().getText(), self.visit(ctx.exp_list_call()))


    # exp_list_call: exp CM exp_list_call | exp |;
    def visitExp_list_call(self, ctx:MT22Parser.Exp_list_callContext):
        if ctx.exp_list_call():
            return [self.visit(ctx.exp())] + self.visit(ctx.exp_list_call())
        elif ctx.exp():
            return [self.visit(ctx.exp())]
        else:
            return []


    # block_statement: LP statement_list RP;
    def visitBlock_statement(self, ctx:MT22Parser.Block_statementContext):
        return BlockStmt(self.visit(ctx.statement_list()))


    # statement_list: statement statement_list | statement | var_declare statement_list| var_declare| ;
    def visitStatement_list(self, ctx:MT22Parser.Statement_listContext):
        if ctx.statement_list() and ctx.statement():
            return [self.visit(ctx.statement())] + self.visit(ctx.statement_list())
        elif ctx.statement_list() and ctx.var_declare():
            return self.visit(ctx.var_declare()) + self.visit(ctx.statement_list())
        elif ctx.statement():
            return [self.visit(ctx.statement())]
        elif ctx.var_declare():
            return [self.visit(ctx.var_declare())]
        else:
            return []
            

    # arraylit: LP exp_list_arraylit RP;  
    def visitArraylit(self, ctx:MT22Parser.ArraylitContext):
        
        return ArrayLit(self.visit(ctx.exp_list_arraylit()))

    # exp_list_arraylit: exp CM exp_list_arraylit | exp | ;
    def visitExp_list_arraylit(self, ctx:MT22Parser.Exp_list_arraylitContext):
        if ctx.CM():
            return [self.visit(ctx.exp())] + self.visit(ctx.exp_list_arraylit())
        elif ctx.exp():
            return [self.visit(ctx.exp())]
        else:
            return []
    
