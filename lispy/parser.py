from lark import Lark, InlineTransformer
from pathlib import Path
import os

from .runtime import Symbol


class LispTransformer(InlineTransformer):
    number = float
    name   = str

    def bool(self, term):
        print(term)
        return True if term == '#t' else False

    def symbol_list(self,args):
        print("bb",args)
        print("aa",[self.symbol(args)])
        return [self.symbol(args)]

    def binop(self, op, left, right):
        print("binop")
        return [(Symbol(op), left, right)]

    def string(self, string):
        string = string.replace('\\t', '\t').replace('\\"','\"').replace('\\n','\n')[1:-1]
        print(string)
        return string

    def word(self,word):
        print("AAAAAAAAAAAAAAAAA:",word)
        return word

    def list(self, *args):
        return list(args)

    def symbol(self, symbol):
        return Symbol(symbol)

    def quote(self,quote):
        return [Symbol.QUOTE,quote]

    def let(self, declarations, expr):
        return [(Symbol('let'),declarations,expr)]

    def func_lambda(self,params, expr):
        return [Symbol('lambda'),(params,expr)]

    def ext1(self,left,op,right):
        if isinstance(left,list):
            result = [op,left,right]
        else:
            result = [Symbol(op),left,right]
        return result

    def attr(self,name,value):
        return [name,value]

    def ext2(self,*attr):
        *attr1,attr2 = attr
        attr2 = list(attr2[0])
        result = [Symbol('let'),attr1,attr2]
        return result

    def ext3(self,cond,verd,fal,*args):
        print("EXT3")
        result = [Symbol("if"),cond,verd,fal]
        if args != ():
            result = [Symbol("if"),cond,verd,self.ext3(fal,*args)]
            print("result: ",result)
        return result

    def ext4(self,*params):
        *params,expr = params
        print("expr: ",expr)
        print("param: ",params)
        result = [Symbol('lambda'),(params,expr)]
        print("result: ",result)
        return result

    def ext5(self,*params):
        print("Olá",*params)
        name, *parameters, expr = params
        print("name",name)
        print("parameters",parameters)
        print("exp",expr)
        result = [Symbol.DEFINE,name,[Symbol('lambda'),(parameters,expr)]]
        return result

def parse(src: str):
    """
    Compila string de entrada e retorna a S-expression equivalente.
    """
    return parser.parse(src)


def _make_grammar():
    """
    Retorna uma gramática do Lark inicializada.
    """
    path =os.getcwd()+'/lispy/grammar.lark'# / 'grammar.lark'
    with open(path) as fd:
        grammar = Lark(fd, parser='lalr', transformer=LispTransformer())
    return grammar

parser = _make_grammar()
