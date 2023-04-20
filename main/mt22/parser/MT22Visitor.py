# Generated from main/mt22/parser/MT22.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MT22Parser import MT22Parser
else:
    from MT22Parser import MT22Parser

# This class defines a complete generic visitor for a parse tree produced by MT22Parser.

class MT22Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by MT22Parser#program.
    def visitProgram(self, ctx:MT22Parser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#declare.
    def visitDeclare(self, ctx:MT22Parser.DeclareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#var_declare.
    def visitVar_declare(self, ctx:MT22Parser.Var_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#short_form.
    def visitShort_form(self, ctx:MT22Parser.Short_formContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#identifier_list.
    def visitIdentifier_list(self, ctx:MT22Parser.Identifier_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#init_var.
    def visitInit_var(self, ctx:MT22Parser.Init_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#pair.
    def visitPair(self, ctx:MT22Parser.PairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#type_decl_init.
    def visitType_decl_init(self, ctx:MT22Parser.Type_decl_initContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#parameter_list_declare_infunc.
    def visitParameter_list_declare_infunc(self, ctx:MT22Parser.Parameter_list_declare_infuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#parameter_list_declare.
    def visitParameter_list_declare(self, ctx:MT22Parser.Parameter_list_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#parameter_declare.
    def visitParameter_declare(self, ctx:MT22Parser.Parameter_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#type_parameter.
    def visitType_parameter(self, ctx:MT22Parser.Type_parameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#func_declare.
    def visitFunc_declare(self, ctx:MT22Parser.Func_declareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#type_return.
    def visitType_return(self, ctx:MT22Parser.Type_returnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#type_decl.
    def visitType_decl(self, ctx:MT22Parser.Type_declContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#atomic_type.
    def visitAtomic_type(self, ctx:MT22Parser.Atomic_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#array_type.
    def visitArray_type(self, ctx:MT22Parser.Array_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#dimension.
    def visitDimension(self, ctx:MT22Parser.DimensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#void_type.
    def visitVoid_type(self, ctx:MT22Parser.Void_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#auto_type.
    def visitAuto_type(self, ctx:MT22Parser.Auto_typeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp.
    def visitExp(self, ctx:MT22Parser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp1.
    def visitExp1(self, ctx:MT22Parser.Exp1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#relational.
    def visitRelational(self, ctx:MT22Parser.RelationalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp2.
    def visitExp2(self, ctx:MT22Parser.Exp2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#logical.
    def visitLogical(self, ctx:MT22Parser.LogicalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp3.
    def visitExp3(self, ctx:MT22Parser.Exp3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#adding.
    def visitAdding(self, ctx:MT22Parser.AddingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp4.
    def visitExp4(self, ctx:MT22Parser.Exp4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#multiplying.
    def visitMultiplying(self, ctx:MT22Parser.MultiplyingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp5.
    def visitExp5(self, ctx:MT22Parser.Exp5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp6.
    def visitExp6(self, ctx:MT22Parser.Exp6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp7.
    def visitExp7(self, ctx:MT22Parser.Exp7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#index_operator.
    def visitIndex_operator(self, ctx:MT22Parser.Index_operatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp_list_array.
    def visitExp_list_array(self, ctx:MT22Parser.Exp_list_arrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#operands.
    def visitOperands(self, ctx:MT22Parser.OperandsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#function_call.
    def visitFunction_call(self, ctx:MT22Parser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#statement.
    def visitStatement(self, ctx:MT22Parser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#assign_statement.
    def visitAssign_statement(self, ctx:MT22Parser.Assign_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#lhs.
    def visitLhs(self, ctx:MT22Parser.LhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#index_expression.
    def visitIndex_expression(self, ctx:MT22Parser.Index_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#match_statement.
    def visitMatch_statement(self, ctx:MT22Parser.Match_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#other_statement.
    def visitOther_statement(self, ctx:MT22Parser.Other_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#unmatch_statement.
    def visitUnmatch_statement(self, ctx:MT22Parser.Unmatch_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#for_statement.
    def visitFor_statement(self, ctx:MT22Parser.For_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#scalar_init_expr.
    def visitScalar_init_expr(self, ctx:MT22Parser.Scalar_init_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#scalar_var.
    def visitScalar_var(self, ctx:MT22Parser.Scalar_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#condition_expr.
    def visitCondition_expr(self, ctx:MT22Parser.Condition_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#update_expr.
    def visitUpdate_expr(self, ctx:MT22Parser.Update_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#while_statement.
    def visitWhile_statement(self, ctx:MT22Parser.While_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#do_while_statement.
    def visitDo_while_statement(self, ctx:MT22Parser.Do_while_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#break_statement.
    def visitBreak_statement(self, ctx:MT22Parser.Break_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#continue_statement.
    def visitContinue_statement(self, ctx:MT22Parser.Continue_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#return_statement.
    def visitReturn_statement(self, ctx:MT22Parser.Return_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#call_statement.
    def visitCall_statement(self, ctx:MT22Parser.Call_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp_list_call.
    def visitExp_list_call(self, ctx:MT22Parser.Exp_list_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#block_statement.
    def visitBlock_statement(self, ctx:MT22Parser.Block_statementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#statement_list.
    def visitStatement_list(self, ctx:MT22Parser.Statement_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#arraylit.
    def visitArraylit(self, ctx:MT22Parser.ArraylitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MT22Parser#exp_list_arraylit.
    def visitExp_list_arraylit(self, ctx:MT22Parser.Exp_list_arraylitContext):
        return self.visitChildren(ctx)



del MT22Parser