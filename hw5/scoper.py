#!/usr/bin/env python3

# HW 5, problem 4
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
        return Program(r)

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
        raise
        print("Syntax error.  Rest of tokens:", toks[posn[0]:])
        sys.exit(1)

### recolic
globalSymTable = {}
#depre# [ ('class', 'classA'), ('def', 'defB'), ('local', 'ID'), ... ]
#depre# { 'classA' -> 'class', ... }
# {'classA' -> ('class', None, classA_id), 'aVar' -> ('local', classA_id, aVar_id), ...}

def pushStatementToSymTable(stmt, pSymTable):
    if type(stmt) == ClassDecl or type(stmt) == DefDecl:
        his_id = str(stmt.id)
        if his_id in pSymTable:
            raise SyntaxError('duplicate class or def decl.')
        his_kind = 'class' if type(stmt) == ClassDecl else 'def'
        pSymTable[his_id] = (his_kind, None, stmt.id)
    if type(stmt) == Assign:
        his_id = str(stmt.id)
        his_type = ('local', stmt.typ, stmt.id)
        if his_id in pSymTable:
            existing_type = pSymTable[his_id]
            if existing_type[0] != 'local':
                raise SyntaxError('multiple local assignment has type conflict: id {} is already {} but used as {}.'.format(his_id, existing_type, his_type))
            if existing_type[1] != None:
                if his_type[1] != None and str(his_type[1]) != str(existing_type[1]):
                    raise SyntaxError('multiple local assignment has type conflict: id {} is already {} but used as {}.'.format(his_id, existing_type, his_type))
                # don't touch the entry. it's ok.
                return
        pSymTable[his_id] = his_type
        
    return

###
# Abstract Syntax Tree
###

class AST(object):
    pass

class Program(AST):
    def __init__(self, stmts):
        self.stmts = stmts
        self.symTable = {} # Global sym table

        for stmt in stmts:
            pushStatementToSymTable(stmt, self.symTable)
    
    def write(self, indent):
        assert(indent == 0) # Global program always have zero indent
        for s in self.stmts:
            s.write(indent) # Do not plus 4. It starts at 0
        
    def numberDecls(self):
        for s in self.stmts:
            s.numberDecls()
       

# AST for class ID { stmts }
class ClassDecl(AST):     # FIXME?

    def __init__(self, id, stmts):
        self.id = id
        self.stmts = stmts
        self.symTable = {}
        
        for stmt in stmts:
            pushStatementToSymTable(stmt, self.symTable)


    def write(self, indent):
        print("class", self.id, "{")
        for s in self.stmts:
            s.write(indent+4)
        print("}")

    def numberDecls(self):
        self.id.numberDecls()
        for s in self.stmts:
            s.numberDecls()

# AST for def ID "{" stmts "}"
class DefDecl(AST):    # FIXME?

    def __init__(self, id, stmts):
        self.id = id
        self.stmts = stmts
        self.symTable = {}

        for stmt in stmts:
            pushStatementToSymTable(stmt, self.symTable)

    def write(self, indent):
        sys.stdout.write(" " * indent)
        print("def", self.id, "{")
        for s in self.stmts:
            s.write(indent+4)
        print(" " * indent + "}")
    
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
        print(";")
    
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

        self.id_pending_to_assign_decl = []
    
    def sync_pending_ids(self):
        for pending_id in self.id_pending_to_assign_decl:
            # the id is not decorated yet. If the silly language allows use-before-decl, this problem may happen.
            # let's fuck it...
            pending_id.decl = self.decl

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
        print("%d. %s %s" % \
              (self.index, self.kind, self.name), end=" ")
        if self.typ is not None:
            print("(type %s)" % (self.typ,))
        else:
            print()

    def number(self):
        if self.index is None:
            self.index = len(decls)
            decls.append(self)

###
# Semantic Analysis
###
_rlib_tmp_entry_counter = 0

def decorate(ast):
    """Annotate all Ids in AST with appropriate Decls."""
    # FIXME
    def _validate_type_usage(type_id, symTables):
        type_text = type_id.name
        entry = _find_entry_in_symTables(type_text, symTables)
        if entry is None:
            raise SyntaxError('Type {} is not found, but used to decl a variable.'.format(type_id))
        if entry[0] != 'class':
            raise SyntaxError('type of variable "{}" should be (class, *), rather than {}.'.format(type_text, entry))
        return entry

    def _find_entry_in_symTables(id_text, symTables, requirement=None):
        for tbl in symTables:
            if id_text in tbl:
                entry = tbl[id_text]
                if requirement is None or requirement(entry) is True:
                    return tbl[id_text]
        return None

    def _check_dup_entry_in_symTables(id_text, symTables, requirement=None):
        global _rlib_tmp_entry_counter
        _rlib_tmp_entry_counter = 0
        def new_req(entry):
            global _rlib_tmp_entry_counter
            if requirement is not None and not requirement(entry):
                return False
            _rlib_tmp_entry_counter += 1
            return _rlib_tmp_entry_counter % 2 == 0
        entry = _find_entry_in_symTables(id_text, symTables, new_req)
        
        if entry is not None:
            raise SyntaxError('Duplicate entry found but it\'s not allowed.')


    def do_decorate(ast, symTables):
        if type(ast) is Program:
            assert(symTables == [])
            for stmt in ast.stmts:
                do_decorate(stmt, [ast.symTable])
                # index_begin += 1
        elif type(ast) is ClassDecl:
            m_kind = 'class'
            _check_dup_entry_in_symTables(ast.id.name, symTables)
            ast.id.decl = Decl(ast.id.name, m_kind)
            ast.id.decl.number()
            ast.id.sync_pending_ids()
            for stmt in ast.stmts:
                if type(stmt) is DefDecl:
                    do_decorate(stmt, symTables) # class decl doesn't add the symTable into member function.
                else:
                    do_decorate(stmt, [ast.symTable] + symTables)
        elif type(ast) is DefDecl:
            m_kind = 'def'
            _check_dup_entry_in_symTables(ast.id.name, symTables)
            ast.id.decl = Decl(ast.id.name, m_kind)
            ast.id.decl.number()
            ast.id.sync_pending_ids()
            for stmt in ast.stmts:
                do_decorate(stmt, [ast.symTable] + symTables)
            ###################### types above has their own sym table.
        elif type(ast) is Assign:
            m_kind = 'local'
            entry = _find_entry_in_symTables(ast.id.name, symTables) # current symTable always contain this symbol... so entry is never None!
            if entry[2].decl is None:
                # Add new decl
                entry[2].decl = Decl(ast.id.name, m_kind, ast.typ)
                entry[2].decl.number()
            # Use existing decl
            ast.id.decl = entry[2].decl
            ast.id.sync_pending_ids()
            do_decorate(ast.expr, symTables)
            if ast.typ is not None:
                do_decorate(ast.typ, symTables)
        elif type(ast) is Expr:
            for _id in ast.ids:
                do_decorate(_id, symTables)
        elif type(ast) is Id:
            # Type Id is already processed in ClassDecl/DefDecl/Assign.
            m_name = ast.name
            #                                                   # This requirement don't allow 'use-before-decl'
            entry = _find_entry_in_symTables(m_name, symTables) # , requirement=lambda entry : entry[2].decl is not None)
            if entry == None:
                raise SyntaxError("Used a un-declared id " + m_name)
            type_to_validate = entry[1]
            #if type_to_validate is not None:
            #    _validate_type_usage(type_to_validate, symTables) # type should be in symTables NOW!
            if entry[2].decl is None:
                # the id is not decorated yet. If the silly language allows use-before-decl, this problem may happen.
                # let's fuck it...
                entry[2].id_pending_to_assign_decl.append(ast)
            ast.decl = entry[2].decl
        elif type(ast) is Type:
            # do nothing
            type_id = ast
            origin_type_decl = _validate_type_usage(type_id, symTables)[2].decl
            ast.decl = origin_type_decl
        else:
            raise RuntimeError('Unknown entry in ast...')

    do_decorate(ast, [])






###
# Main program
###

if len(sys.argv) > 1:
    inp = open(sys.argv[1])
else:
    inp = sys.stdin

ast = parse(inp.read())

decorate(ast)

# s is global "Program" ast. no need to iterate it manually.
ast.numberDecls()
ast.write(0)

print()
print("# Declarations:")
print()

for d in decls:
    d.write()

#print("recolic debug:")
#print(ast.symTable)
