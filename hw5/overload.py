# HW 5, problem 5.

# Fill in the resolve... methods in class Call below.  To play around with this
# module, start python and enter the command
#
#  from overload import *
#
# You can print programs (like prog1) with
#     print prog1


class Signature(object):
    """A function signature."""

    def __init__(self, argTypes, retnType):
        """A new Signature representing the function type
               argTypes[0] x argTypes[1] x ... --> retnType.
           retnType is a string, and argTypes is a tuple or list of
           strings."""
        self._retnType = retnType
        self._argTypes = tuple(argTypes)

    def retnType(self):
        return self._retnType

    def argType(self, k):
        """Type of the Kth argument"""
        return self._argTypes[k]

    def arity(self):
        """Number of arguments"""
        return len(self._argTypes)

    def __str__(self):
        return str(self._argTypes) + " --> " + self._retnType

    # Other methods might go here.

class AST(object):
    """An abstract syntax tree node"""
    
    def typeof(self):
        return self._type

    def resolve1(self, Env):
        pass

    def resolve2(self, Env):
        pass

    def unresolve(self):
        pass

    # Other methods might go here.

class Leaf(AST):
    """Represents a primitive expression's type."""

    def __init__(self, typ):
        self._type = typ

    def __str__(self):
        return self._type

class Call(AST):
    """Represents a call."""

    def __init__(self, func, actuals):
        self._func = func
        self._actuals = tuple(actuals)
        self._type = None

    def __str__(self):
        return self._func + (":" + self._type if self._type else "") \
               + "(" + ','.join(map(str, self._actuals)) + ")"

    def unresolve(self):
        """Undo all type determinations."""
        self._type = None
        for kid in self._actuals:
            kid.unresolve()

    def resolve1(self, Env):
        """Set my type and (recursively) those of my actual parameters, given
        that the dictionary Env maps function names (_func) to lists of
        Signatures.  Uses the style of Java and C++, where we are oblivious
        to the context in which the call is used.  Raise TypeError if resolution
        is impossible (or ambiguous)"""
        # FILL THIS IN
        pass


    def resolve2(self, Env):
        """Set my type and (recursively) those of my actual parameters, given
        that the dictionary Env maps function names (_func) to lists of
        Signatures.  Uses the style of Ada, where we take into account which
        return types are legal for this call.  The type of the whole AST
        (the outermost call) is unconstrained. Raise TypeError if resolution
        is impossible (or ambiguous)"""
        # FILL THIS IN 
        pass

    # HINTS for resolve2:

    def _resolve2Up(self, Env):
        """Return the set of possible types this call might have in the
        environment Env, considering only the types of the children (not the
        context in which the call is used)."""
        # FILL THIS IN
        pass

    def _resolve2Down(self, returnType):
        """Set my type and (recursively) those of my actual parameters, given
        that the dictionary Env maps function names (_func) to lists of
        Signatures, and that the return type must be returnType."""
        # FILL THIS IN
        pass

    # Other methods might go here.

def toAST(src):
    """Given a source program, src, return the corresponding AST.  src is either
    a type name (a single string), or else a list or tuple (f, a1, a2, ..., an),
    where f is a function name and the ai are lists or strings in the same
    form as src.  Thus f(Int, Bool) is represents ["f", "Int", "Bool"] and
    f(g(Int)) as ["f", ["g", "Int"]]."""
    if type(src) is str:
        return Leaf(src)
    else:
        return Call (src[0], map(toAST, src[1:]))


# Example:

# f can take Ints and produce Floats or Bools, or take Floats and produce Ints.
# g takes no arguments and can return Bool or Int.
# r can take Int or Float, returning Void.
funcEnv = { 'f': [ Signature(["Int"], "Float"), Signature(["Float"], "Int"),
                   Signature(["Int"], "Bool"),
                   Signature(["Int", "Int"], "Int") ],
            'g': [ Signature([], "Int"), Signature([], "Bool") ],
            'r': [ Signature(["Int"], "Void"), Signature(["Float"], "Void") ]
            }

# The program r(f(g()))
prog1 = toAST( ('r', ('f', ('g',))) )

# After prog1.resolve2(funcEnv), prog1 should print as
#    r:Void(f:Float(g:Int()))
#                                                          

# The program r(f(Int,Int))
prog2 = toAST( ('r', ('f', 'Int', 'Int')) )

# Then after prog1.unresolve(), prog1.resolve1(funcEnv) should raise an
# exception.  After prog2.resolve1(), prog2 should print as

#    r:Void(f:Int(Int,Int))
