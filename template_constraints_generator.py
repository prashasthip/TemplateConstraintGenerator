import ply.yacc as yacc
import ply.lex as lex
import re
from preprocessing import *

template_constraints={}

def sym_table_update(datatype, variable):
        sym_table[variable] = datatype
        temp_datatype_table[datatype].append(variable)
        
def lookup(variable):
        if(variable in sym_table):
                return sym_table[variable]

def register(m1,m2,m3=""):
        if(m3!=""):
                
                if(m1 not in template_constraints):
                        template_constraints[m1]=set()
                template_constraints[m1].add(m3)
        else:
                
                if(m1 not in template_constraints):
                        template_constraints[m1]=set()
                template_constraints[m1].add(m2)


filename=input("Enter file name\n")
input_expressions = preprocessing(filename)


datatype_pattern=r'int | double' 
for datatype in temp_datatype_table:
        datatype_pattern+=' | '+datatype
        
tokens = ('OB','CB','ID','DT','INT','DBL','COMMA','SC','EQ','COUT','CIN','RETURN',
'EXT','INS','ASSN_OP','OR','AND','S_AND','EQUAL','N_EQUAL','REL_OP',
'INCR','DECR','SO','MUL','DIV','PLUS','MINUS','NOT','MOD','OC','CONST')

@lex.TOKEN(datatype_pattern)
def t_DT(t):
        return t
def t_COMMA(t):
        r','
        return t
def t_CONST(t):
        r'const'
        return t

def t_OB(t):
        r'[(]'
        return t

def t_CB(t):
        r'[)]'
        return t

def t_DBL(t):
        r'\d*\.\d+'
        return t

def t_CIN(t):
        r'cin'
        return t

def t_COUT(t):
        r'cout'
        return t

def t_INT(t):
        r'\d+'
        return t
def t_RETURN(t):
        r'return'
        return t

def t_ID(t):
        r'\w+'
        return t

def t_INCR(t):
        r'\+\+'
        return t

def t_DECR(t):
        r'\-\-'
        return t

def t_OC(t):
        r'\"'
        return t

def t_EQUAL(t):
        r'=='
        return t
def t_N_EQUAL(t):
        r'!='
        return t
def t_EQ(t):
        r'='
        return t

def t_INS(t):
        r'<<'
        return t

def t_EXT(t):
        r'>>'
        return t

def t_ASSN_OP(t):
        r' \*= | /= | %= | \+= | –= | >= | <= | &= | ^= '
        return t

def t_PLUS(t):
        r'\+'
        return t

def t_MINUS(t):
        r'\-'
        return t

def t_DIV(t):
        r'[/]'
        return t

def t_MUL(t):
        r'[*]'
        return t

def t_MOD(t):
        r'[%]'
        return t

def t_OR(t):
        r'\|\|'
        return t
def t_AND(t):
        r'&&'
        return t
def t_S_AND(t):
        r'&'
        return t
def REL_OP(t):
        r'''<=
        | >=
        | <
        | >
        '''
        return t
def t_SC(t):
        r';'
        return t
def t_SO(t):
        r'sizeof'
        return t
def t_error(t):
	print("error")


#all the operators which can be overloaded      
t_ignore= '[ \t\n]'


def p_func_body(p):
        '''func_body : statement SC more_statements
        | empty
        '''


def p_more_statements(p):
        '''more_statements : statement SC more_statements
        | empty
        '''

def p_statement(p):
        '''statement : declaration
        | inout
        | expression
        | RETURN expression
        
        '''
        
def p_declaration(p):
        '''declaration : DT var_dec
        | CONST DT var_dec
        '''
        if(len(p)==3 and p[1] != "double" and p[1] != "int"):
                for var in p[2]:
                        sym_table_update(p[1], var)


def p_var_dec(p):
        '''
        var_dec : S_AND ID OB val CB var_dec
        | S_AND ID EQ val var_dec
        |  COMMA var_dec
        | MUL ID EQ S_AND ID
	| MUL ID
        | ID EQ expression
        | ID OB expression CB
        | ID var_dec
        | empty
        '''
        if(len(p)==2 and p[1]!=""):
                p[0]=[p[1]]
        elif(len(p)==6):
                p[0]=[p[2]]
                for var in p[5]:
                      p[0].append(var)  
        elif(len(p)==7):
                p[0]=[p[2]]
                for var in p[6]:
                        p[0].append(var)
        elif(len(p)==3):
                p[0]=[p[1]]
                for var in p[2]:
                        p[0].append(var)
        elif(len(p)==4):
                para_type = lookup(p[1])
                if(para_type):
                        register(para_type,p[2])  

        
def p_val(p):
        '''val : ID 
        | INT
        | DBL
        '''


def p_inout(p):
        '''inout : COUT INS to_print more_to_print
        | CIN EXT ID more_to_read
        '''
        l=len(p)
        m=3
        while(m<l):
                para_type = lookup(p[m])
                if(para_type):
                        register(para_type,p[2])
                m+=1


def p_more_to_print(p):
        ''' more_to_print : INS to_print  more_to_print
        | empty 
        '''
        if(len(p)==4):
                p[0] = p[2]


def p_to_print(p):
        ''' to_print : OC OC 
        | expression
        '''
        p[0]=p[1]

def p_more_to_read(p):
        ''' more_to_read : EXT ID  more_to_read
        | empty
        '''
        if(len(p)==4):
                para_type = lookup(p[2])
                if(para_type):
                        register(para_type,p[1])

def p_expression(p):
        ''' expression : assignment_expression 
        | expression COMMA assignment_expression 
        | equality_expression
        | relational_expression
        | additive_expression
        | multiplicative_expression
        | unary_expression
        '''
        p[0]=p[1]
   

def p_assignment_expression(p):
        '''assignment_expression : unary_expression ASSN_OP equality_expression
        | unary_expression EQ equality_expression
        | unary_expression EQ assignment_expression
        '''
        if(re.search(r'^\*',p[1])):
                para_type=lookup(p[1].strip("*"))
                if(para_type):
                        register(para_type,"*","l-value dereferencing")
                        register(para_type,p[2])
        else:
                para_type=lookup(p[1])
                if(para_type):
                        register(para_type,p[2])
                
        

def p_equality_expression(p):
        '''equality_expression : relational_expression 
        | equality_expression EQUAL relational_expression
        | equality_expression N_EQUAL relational_expression
        '''
        p[0] = p[1]
        if(len(p)==4):
                para_type=lookup(p[1])
                if(para_type):
                        register(para_type,p[2])
                
                
                

def p_relational_expression(p): 
        '''relational_expression : additive_expression 
        | relational_expression REL_OP additive_expression 
        '''
        p[0]=p[1]
        if(len(p)==4):
                para_type=lookup(p[1])
                if(para_type):
                        register(para_type,p[2])
                
        

def p_additive_expression(p): 
        '''additive_expression : multiplicative_expression 
        | additive_expression PLUS additive_expression
        | additive_expression MINUS additive_expression 
        '''
        p[0] = p[1]
        if(len(p)==4):
                para_type=lookup(p[1])
                if(para_type):
                        register(para_type,p[2])
                

def p_multiplicative_expression(p): 
        '''multiplicative_expression : cast_expression
        | multiplicative_expression MUL multiplicative_expression 
        | multiplicative_expression DIV multiplicative_expression 
        | multiplicative_expression MOD multiplicative_expression 
        '''
        p[0] = p[1]
        if(len(p)==4):
                para_type=lookup(p[0])
                if(para_type):
                        register(para_type,p[2])

def p_cast_expression(p): 
        '''cast_expression : unary_expression 
        | OB DT CB cast_expression
        '''
        p[0] = p[1]
        if(len(p)==5):
                para_type=lookup(p[4])
                if(para_type):
                        register(para_type,p[2]+'()')


def p_unary_expression(p): 
        '''unary_expression : INCR unary_expression 
        | unary_expression INCR
        | DECR unary_expression
        | unary_expression DECR
        | MUL ID
        | S_AND ID
        | MINUS ID
        | PLUS ID
        | NOT ID
        | SO unary_expression 
        | SO OB DT CB 
        | ID
        | INT
        | DBL
        '''
        p[0] = p[1]
        if(len(p)==3 and (p[1]!="-") and (p[1]!="+")):
                if(p[1]=="*"):
                        para_type=lookup(p[2])
                        if(para_type):
                                register(para_type,p[1],"dereferencing operator r-value")
                        p[0]="*"+p[2]

                elif(p[1]=="++"):
                        para_type=lookup(p[2])
                        if(para_type):
                                register(para_type,p[1],"pre increment operator")
                elif(p[1]=="--"):
                        para_type=lookup(p[2])
                        if(para_type):
                                register(para_type,p[1],"pre decrement operator")
                elif(p[2]=="++"):
                        para_type=lookup(p[1])
                        if(para_type):
                                register(para_type,p[2],"post increment operator")
                elif(p[2]=="--"):
                        para_type=lookup(p[1])
                        if(para_type):
                                register(para_type,p[2],"post decrement operator")
                elif(p[1]=='!'):
                        para_type=lookup(p[2])
                        if(para_type):
                                register(para_type,p[1])
                elif(p[1]=='&'):
                        para_type=lookup(p[2])
                        if(para_type):
                                register(para_type,p[1])
                

def p_empty(p):
        ''' empty : '''
        pass

lexer = lex.lex()
parser = yacc.yacc()

for line_no in range(0,len(input_expressions)):
        parser.parse(input_expressions[line_no])

#print(template_constraints)


file1=open("output.txt","w")
file1.write("/* TEMPLATE CONSTRAINTS FOR THE GIVEN TEMPLATE FUNCTION ARE\n")
for parameter in template_constraints:
        file1.write(str(parameter)+" should support :\n")
        file1.write("\t"+"\n\t".join(str(operator) for operator in template_constraints[parameter]))
        file1.write("\n--------------------------------------------\n")
file1.write("*/\n\n")
file2=open(filename,"r")
lines = file2.read()
file1.write(lines)
file1.close()
file2.close()
