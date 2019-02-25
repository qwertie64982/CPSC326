# Author: Maxwell Sherman
# Course: CPSC 326, Spring 2019
# Assignment: 5
# Description:
#   Type Checker visitor class, to be used in hw5.py
#-----------------------------------------------------

import mypl_token as token
import mypl_ast as ast
import mypl_error as error
import mypl_symbol_table as symbol_table

# TODO: var decls and assigns
# TODO: if stmts and while loops
# TODO: struct decls and creations
# TODO: function decls and calls
# TODO: nil values and types

# a MyPL type checker visitor implementation where struct types
# take the form: type_id -> {v1:t1, ..., vn:tn} and function types
# take the form: fun_id -> [[t1, t2, ..., tn], return_type]
class TypeChecker(ast.Visitor):
    # init method
    def __init__(self):
        # initialize the symbol table (for ids -> types)
        self.sym_table = symbol_table.SymbolTable()
        
        # current_type holds the type of the last expression type
        self.current_type = None
        
        # global env (for return)
        self.sym_table.push_environment()
        
        # set global return type to int
        self.sym_table.add_id('return')
        self.sym_table.set_info('return', token.INTTYPE)
        
        # load in built-in function types
        self.sym_table.add_id('print')
        self.sym_table.set_info('print', [[token.STRINGTYPE], token.NIL])
        
        '''
        print(str(self.sym_table.scopes))
        print(self.sym_table.get_info('return'))
        '''
        
        # TODO: remaining function types
    
    # raises a descriptive MyPLError given a simple error_msg
    def __error(self, error_msg, error_token):
        s = error_msg + ', found "' + error_token.lexeme + '" in type checker'
        l = error_token.line
        c = error_token.column
        raise error.MyPLError(s, l, c)
    
    # beginning of type checking visitor methods
    
    def visit_stmt_list(self, stmt_list):
        # add new block (scope)
        self.sym_table.push_environment()
        
        for stmt in stmt_list.stmts:
            stmt.accept(self)
        
        # remove new block
        self.sym_table.pop_environment
    
    def visit_expr_stmt(self, expr_stmt):
        expr_stmt.expr.accept(self)
    
    def visit_var_decl_stmt(self, var_decl): pass
        # TODO
    
    def visit_assign_stmt(self, assign_stmt):
        assign_stmt.rhs.accept(self)
        rhs_type = self.current_type
        assign_stmt.lhs.accept(self)
        lhs_type = self.current_type
        if rhs_type != token.NIL and rhs_type != lhs_type:
            msg = 'mismatched type in assignment'
            self.__error(msg, assign_stmt.lhs.path[0])
    
    def visit_simple_expr(self, simple_expr):
        simple_expr.term.accept(self)
    
    def visit_simple_rvalue(self, simple_rvalue):
        if simple_rvalue.val.tokentype == token.INTVAL:
            self.current_type = token.INTTYPE
        elif simple_rvalue.val.tokentype == token.FLOATVAL:
            self.current_type = token.FLOATTYPE
        elif simple_rvalue.val.tokentype == token.BOOLVAL:
            self.current_type = token.BOOLTYPE
        elif simple_rvalue.val.tokentype == token.STRINGVAL:
            self.current_type = token.STRINGTYPE
        elif simple_rvalue.val.tokentype == token.NIL:
            self.current_type = token.NIL
        else:
            msg = 'this should not happen'
            self.__error(msg, simple_rvalue.val)
    
    def visit_new_rvalue(self, new_rvalue): pass
        # TODO - get the ID token?
        # self.current_type = new_rvalue.struct_type
    
    def visit_call_rvalue(self, call_rvalue): pass
        # TODO - get the function's return type
    
    def visit_id_rvalue(self, id_rvalue):
        # TODO: paths.of.struct.vars
        if self.sym_table.id_exists(id_rvalue.path[0]):
            self.current_type = self.sym_table.get_info(id_rvalue.path[0].lexeme)
            # print(str(self.sym_table.get_info(id_rvalue.path[0])))
        else:
            msg = 'id use before declaration'
            self.__error(msg, id_rvalue.path[0])
    
    def visit_complex_expr(self, complex_expr):
        complex_expr.first_operand.accept(self)
        left_type = self.current_type
        complex_expr.rest.accept(self)
        right_type = self.current_type
        if left_type == token.NIL or right_type == token.NIL:
            msg = 'nil type in expression'
            self.__error(msg, complex_expr.math_rel) # math rel b/c token needed
        elif left_type == token.INTTYPE and left_type == right_type:
            self.current_type = left_type
        elif (left_type == token.FLOATTYPE and left_type == right_type and
                (complex_expr.math_rel.tokentype == token.PLUS or
                complex_expr.math_rel.tokentype == token.MINUS or
                complex_expr.math_rel.tokentype == token.MULTIPLY or
                complex_expr.math_rel.tokentype == token.DIVIDE)):
            self.current_type = left_type
        elif (left_type == token.STRINGTYPE and left_type == right_type and
                complex_expr.math_rel.tokentype == token.PLUS):
            self.current_type = left_type
        elif left_type == token.BOOLTYPE or right_type == token.BOOLTYPE:
            msg = 'boolean in complex expression' # bools should be in boolexpr
            self.__error(msg, complex_expr.math_rel)
        else:
            msg = 'mismatched type in complex expression'
            self.__error(msg, complex_expr.math_rel)
    
    def visit_bool_expr(self, bool_expr):
        bool_expr.first_expr.accept(self)
        if bool_expr.bool_rel != None and bool_expr.second_expr != None:
            first_type = self.current_type
            bool_expr.second_expr.accept(self)
            second_type = self.current_type
            if (bool_expr.bool_rel.tokentype == token.EQUAL or
                    bool_expr.bool_rel.tokentype == token.NOT_EQUAL):
                if (first_type == token.NIL or second_type == token.NIL or
                        first_type == second_type):
                    self.current_type = token.BOOLTYPE
                else:
                    msg = 'mismatched type in boolean expression'
                    self.__error(msg, bool_expr.bool_rel) # bool rel b/c token needed
            elif (bool_expr.bool_rel.tokentype == token.GREATER_THAN or
                    bool_expr.bool_rel.tokentype == token.LESS_THAN or
                    bool_expr.bool_rel.tokentype == token.GREATER_THAN_EQUAL or
                    bool_expr.bool_rel.tokentype == token.LESS_THAN_EQUAL):
                if ((left_type == token.INTTYPE or
                        left_type == token.FLOATTYPE or
                        left_type == token.BOOLTYPE or
                        left_type == token.STRINGTYPE) and
                        (right_type == token.INTTYPE or
                        right_type == token.FLOATTYPE or
                        right_type == token.BOOLTYPE or
                        right_type == STRINGTYPE)):
                    if left_type == right_type:
                        self.current_type = token.BOOLTYPE
                    else:
                        msg = 'mismatched type in boolean expression'
                        self.__error(msg, bool_expr.bool_rel)
                else:
                    msg = 'invalid comparison type'
                    self.__error(msg, bool_expr.bool_rel)
        else:
            self.current_type = token.BOOLTYPE
        
        if bool_expr.bool_connector != None and bool_expr.rest != None:
            left_type = self.current_type
            bool_expr.rest.accept(self)
            right_type = self.current_type
            if (bool_expr.bool_connector.tokentype == token.AND or
                    bool_expr.bool_connector.tokentype == token.OR):
                if left_type == token.BOOLTYPE and left_type == right_type:
                    self.current_type = left_type
                else:
                    msg = 'mismatched type in boolean expression'
                    self.__error(msg, bool_expr.bool_connector)
            else:
                msg = 'this should not happen'
                self.__error(msg, bool_expr.bool_connector)
        else:
            self.current_type = token.BOOLTYPE
        
        if bool_expr.negated:
            if self.current_type != token.BOOLTYPE:
                msg = 'mismatched type in negation'
                # just need some nearby token I know exists for the error message
                if type(bool_expr.first_expr) is ast.SimpleExpr:
                    if type(bool_expr.first_expr.term) is ast.SimpleRValue:
                        self.__error(msg, bool_expr.first_expr.term.val)
                    elif type(bool_expr.first_expr.term) is ast.NewRValue:
                        self.__error(msg, bool_expr.first_expr.term.struct_type)
                    elif type(bool_expr.first_expr.term) is ast.CallRValue:
                        self.__error(msg, bool_expr.first_expr.term.fun)
                    else: # ast.IDRValue
                        self.__error(msg, bool_expr.first_expr.term.path[0])
                else: # ast.ComplexExpr
                    self.__error(msg, bool_expr.first_expr.math_rel)