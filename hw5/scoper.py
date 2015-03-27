#!/usr/bin/env python

# HW 5, problem 6
# Replace (at least) the parts marked FIXME.

import sys, re

###
#  Parsing
###

TOKENS = re.compile(r'::|def|class|[a-zA-Z_][a-zA-Z_0-9]*|\S')

class BackTrack(BaseException):
    pass

def parse(prog):
    EOF = ""
    prog = re.sub(r'#.*', '', prog)
    toks = TOKENS.findall(prog)
    posn = [0]

    def check(f):
        try:
            return f()
        except BackTrack:
            return None

    def next():
        if posn[0] >= len(toks):
            return EOF
        else:
            return toks[posn[0]]

    def scan(patn = None, recoverable=False):
        if patn is not None:
            if not re.match(patn, next()):
                if recoverable:
                    raise BackTrack
                else:
                    raise SyntaxError
        posn[0] += 1

    def scanId(recoverable=False):
        tok = next()
        if tok in ("def", "class") or tok == "" \
           or not re.match('[A-Za-z]', tok):
            if recoverable: 
                raise BackTrack
            else:
                raise SyntaxError
        posn[0] += 1
        return tok

    def prog():
        r = [outer_stmt()]
        while True:
            s = check(outer_stmt)
            if s is None:
                break
            r.append(s)
        scan("$")
        return r

    def outer_stmt():
        return check(stmt) or check(defn) or clazz()

    def stmt():
        name = Id(scanId(True))
        if next() == "::":
            scan()
            typ = Type(scanId())
        else:
            typ = None
        scan("=")
        e = expr()
        scan(";")
        return Assign(name, typ, e)

    def defn():
        scan("def$", True)
        name = Id(scanId())
        scan("{")
        st = stmts()
        scan("}")
        return DefDecl(name, st)

    def clazz():
        scan("class$", True)
        name = Type(scanId())
        scan("{")
        st = stmts()
        scan("}")
        return ClassDecl(name, st)

    def stmts():
        r = []
        while True:
            s = check(stmt) or check(defn)
            if s is None:
                return r
            r.append(s)

    def expr():
        r = []
        while next() != ";":
            r.append(Id(scanId()))
        return Expr(r)

    # Main body:
    try: 
        return prog()
    except:
        print "Syntax error.  Rest of tokens:", toks[posn[0]:]
        sys.exit(1)

###
# Abstract Syntax Tree
###

class AST(object):
    pass

# AST for class ID { stmts }
class ClassDecl(AST):     # FIXME?

    def __init__(self, id, stmts):
        self.id = id
        self.stmts = stmts

    def write(self, indent):
        print "class", self.id, "{"
        for s in self.stmts:
            s.write(indent+4)
        print "}"

    def numberDecls(self):
        self.id.numberDecls()
        for s in self.stmts:
            s.numberDecls()

# AST for def ID "{" stmts "}"
class DefDecl(AST):    # FIXME?

    def __init__(self, id, stmts):
        self.id = id
        self.stmts = stmts

    def write(self, indent):
        sys.stdout.write(" " * indent)
        print "def", self.id, "{"
        for s in self.stmts:
            s.write(indent+4)
        print " " * indent + "}"
    
    def numberDecls(self):
        self.id.numberDecls()
        for s in self.stmts:
            s.numberDecls()

# AST for assignment
class Assign(AST):    # FIXME?

    def __init__(self, id, typ, expr):
        self.id = id
        self.typ = typ
        self.expr = expr

    def write(self, indent):
        sys.stdout.write(" " * indent)
        sys.stdout.write(repr(self.id))
        if self.typ:
            sys.stdout.write("::")
            sys.stdout.write(repr(self.typ))
        sys.stdout.write(" = ")
        self.expr.write(indent)
        print ";"
    
    def numberDecls(self):
        self.id.numberDecls()
        if self.typ:
            self.typ.numberDecls()
        self.expr.numberDecls()

# An expression
class Expr(AST):    # FIXME?

    def __init__(self, ids):
        self.ids = ids
        
    def write(self, indent):
        for id in self.ids:
            id.write(indent)
            sys.stdout.write(" ")

    def numberDecls(self):
        for id in self.ids:
            id.numberDecls()


# An identifier
class Id(AST):    # FIXME?

    def __init__(self, name):
        self.name = name
        self.decl = None

    def __repr__(self):
        if self.decl:
            return "%s@%d" % (self.name, self.decl.index)
        else:
            return self.name

    def write(self, indent):
        sys.stdout.write(repr(self))

    def setDecl(self, decl):
        self.decl = decl

    def numberDecls(self):
        if self.decl:
            self.decl.number()

# An identifier used as a type
class Type(Id):    # FIXME?
    pass

###
# Declarations
###

decls = []

class Decl(object):    # FIXME?

    def __init__(self, name, kind, typ = None):
        """A Decl of an entity whose category is KIND (one of the strings
        'def', 'class', or 'local'), whose name is NAME (a string), and whose
        type (if supplied) is TYP (either None or of type Id).  Each declaration
        has a unique index number accessed by its .index attribute and the
        list decls contains all declarations, in order by index.  Decls must
        be created in the order their identifiers are first defined in a
        preorder traversal of the AST."""

        self.name = name
        self.kind = kind
        self.typ = typ
        self.index = None

    def write(self):
        print "%d. %s %s" % \
              (self.index, self.kind, self.name),
        if self.typ is not None:
            print "(type %s)" % (self.typ,)
        else:
            print

    def number(self):
        if self.index is None:
            self.index = len(decls)
            decls.append(self)

###
# Semantic Analysis
###

def decorate(ast):
    """Annotate all Ids in AST with appropriate Decls."""
    # FIXME

###
# Main program
###

if len(sys.argv) > 1:
    inp = open(sys.argv[1])
else:
    inp = sys.stdin

ast = parse(inp.read())

decorate(ast)

for s in ast:
    s.numberDecls()

for s in ast:
    s.write(0)

print
print "# Declarations:"
print

for d in decls:
    d.write()
