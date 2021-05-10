from collections import OrderedDict, defaultdict
from typing import List, Set, Dict, Tuple, DefaultDict, Union
import itertools
import textwrap

from rfun_parser import *
from typed_rfun import *

import sys

from cs202_support.base_ast import AST, print_ast

import cs202_support.x86exp as x86
import cfun
import constants

# TODO Remove
import pyperclip as pc

gensym_num = 0


def test(*args):
    new_args = []
    for a in args:
        if isinstance(a, str):
            new_args.append(a.rstrip(':') + ':')
        else:
            new_args.append(a)
    print('test:', ' '.join([str(a) for a in new_args]).rstrip(':'))


def gensym(x):
    global gensym_num
    gensym_num = gensym_num + 1
    return f'{x}_{gensym_num}'


def unzip2(ls):
    """
    Unzip a list of 2-tuples.
    :param ls: A list of 2-tuples.
    :return: A single 2-tuple. The first element of the tuple is a list of the 
    first elements of the pairs in ls. The second element of the tuple is a list
    of the second elements of the pairs in ls.
    """

    if not ls:
        return [], []
    else:
        xs, ys = zip(*ls)
        return list(xs), list(ys)


##################################################
# typecheck
##################################################

TEnv = Dict[str, RfunType]


def typecheck(p: RfunProgram) -> RfunProgramT:
    """
    Typechecks the input program; throws an error if the program is not well-typed.
    :param e: The Rfun program to typecheck
    :return: The program, if it is well-typed
    """

    prim_arg_types = {
        '+': [IntT(), IntT()],
        'not': [BoolT()],
        '||': [BoolT(), BoolT()],
        '&&': [BoolT(), BoolT()],
        '>': [IntT(), IntT()],
        '>=': [IntT(), IntT()],
        '<': [IntT(), IntT()],
        '<=': [IntT(), IntT()],
    }

    prim_output_types = {
        '+': IntT(),
        'not': BoolT(),
        '||': BoolT(),
        '&&': BoolT(),
        '>': BoolT(),
        '>=': BoolT(),
        '<': BoolT(),
        '<=': BoolT(),
    }

    def tc_exp(e: RfunExp, env: TEnv) -> Tuple[RfunType, RfunExpT]:
        if isinstance(e, Var):
            t = env[e.var]
            return t, VarTE(e.var, t)
        elif isinstance(e, Int):
            return IntT(), IntTE(e.val)
        elif isinstance(e, Bool):
            return BoolT(), BoolTE(e.val)
        elif isinstance(e, Prim):
            if e.op == '==':
                e1, e2 = e.args
                t1, new_e1 = tc_exp(e1, env)
                t2, new_e2 = tc_exp(e2, env)
                assert t1 == t2
                return BoolT(), PrimTE('==', [new_e1, new_e2], BoolT())
            elif e.op == 'vector':
                results = [tc_exp(a, env) for a in e.args]
                types, new_es = zip(*results)
                t = VectorT(list(types))
                return t, PrimTE('vector', list(new_es), t)
            elif e.op == 'vectorRef':
                e1, e2 = e.args
                t1, new_e1 = tc_exp(e1, env)
                assert isinstance(e2, Int)
                assert isinstance(t1, VectorT)

                idx = e2.val
                t = t1.types[idx]
                return t, PrimTE('vectorRef', [new_e1, IntTE(e2.val)], t)
            elif e.op == 'vectorSet':
                e1, e2, e3 = e.args
                t1, new_e1 = tc_exp(e1, env)
                t3, new_e3 = tc_exp(e3, env)
                assert isinstance(e2, Int)
                assert isinstance(t1, VectorT)

                idx = e2.val
                t = t1.types[idx]
                assert t == t3

                return VoidT(), PrimTE('vectorSet', [new_e1, IntTE(e2.val), new_e3], VoidT())
            else:
                results = [tc_exp(a, env) for a in e.args]
                arg_types, new_es = zip(*results)
                assert list(arg_types) == prim_arg_types[e.op], e
                t = prim_output_types[e.op]
                return t, PrimTE(e.op, list(new_es), t)
        elif isinstance(e, Let):
            t1, new_e1 = tc_exp(e.e1, env)
            new_env = {**env, e.x: t1}
            t2, new_e2 = tc_exp(e.body, new_env)
            return t2, LetTE(e.x, new_e1, new_e2)
        elif isinstance(e, If):
            t1, new_e1 = tc_exp(e.e1, env)
            t2, new_e2 = tc_exp(e.e2, env)
            t3, new_e3 = tc_exp(e.e3, env)

            assert t1 == BoolT()
            assert t2 == t3
            return t2, IfTE(new_e1, new_e2, new_e3, t2)
        elif isinstance(e, Funcall):
            '''
            1. f should have the type (t1, t2, ..., tk) -> t
            2. check that a1 has type t2, a2 has type t2, ..., ak has type tk
            3. assign the function call expression the type t
            '''
            # 1. f should have the type (t1, t2, ..., tk) -> t
            assert isinstance(e.fun, Var)
            fun_name = e.fun.var
            typ = env[fun_name]
            assert isinstance(typ, FunT)
            param_types = typ.arg_types

            # 2. Check that a1 has type t1, a2 has type t2, ..., ak has type tk
            arg_types = [tc_exp(a, {})[0] for a in e.args]
            for t1, t2 in zip(param_types, arg_types):
                assert t1 == t2

            fun_typ, new_fun = tc_exp(e.fun, env)
            assert isinstance(fun_typ, FunT)

            # 3. Assign the function call expression the type t
            return typ.return_type, FuncallTE(new_fun, [tc_exp(a, {})[1] for a in e.args], fun_typ.return_type)
        else:
            raise Exception('tc_exp', e)

    def tc_def(defn: RfunDef, env: TEnv) -> RfunDefT:
        # Add this function's FunT type to the env
        env[defn.name] = FunT([a[1] for a in defn.args], defn.output_type)

        # Init env to map function parameter names to their claimed types
        param_typ_env = {name: typ for name, typ in defn.args}

        # Add all the functions' types
        param_typ_env.update(env)

        # Set new body and its output type
        body_type, new_body = tc_exp(defn.body, param_typ_env)

        assert body_type == defn.output_type
        return RfunDefT(defn.name,
                        defn.args,
                        defn.output_type,
                        new_body)

    # Construct a type environment mapping all of the defined functions to their types
    func_typs_env = {}
    new_defs = []
    env = {}
    for d in p.defs:
        t: RfunDefT = tc_def(d, env)
        new_defs.append(t)
        func_typs_env[d.name] = env[d.name]

    typ_body, new_body = tc_exp(p.body, func_typs_env)
    print(type(new_body))
    return RfunProgramT(new_defs, new_body)


##################################################
# shrink
##################################################

def shrink(p: RfunProgramT) -> RfunProgramT:
    """
    Eliminates some operators from Rfun
    :param e: The Rfun program to shrink
    :return: A shrunken Rfun program
    """

    def shrink_def(defn: RfunDefT) -> RfunDefT:
        new_body = shrink_exp(defn.body)
        return RfunDefT(defn.name,
                        defn.args,
                        defn.output_type,
                        new_body)

    def shrink_exp(e: RfunExpT) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE, VarTE)):
            return e
        elif isinstance(e, LetTE):
            new_e1 = shrink_exp(e.e1)
            new_body = shrink_exp(e.body)
            return LetTE(e.x, new_e1, new_body)
        elif isinstance(e, PrimTE):
            new_args = [shrink_exp(arg) for arg in e.args]

            if e.op in ['+', 'not', '==', '<', 'vector', 'vectorRef', 'vectorSet']:
                return PrimTE(e.op, new_args, e.typ)
            elif e.op == '>':
                return PrimTE('<', [new_args[1], new_args[0]], BoolT())
            elif e.op == '<=':
                return PrimTE('not',
                              [PrimTE('<', [new_args[1], new_args[0]], BoolT())], BoolT())
            elif e.op == '>=':
                return PrimTE('not',
                              [PrimTE('<', new_args, BoolT())], BoolT())
            elif e.op == '&&':
                e1, e2 = new_args
                return IfTE(e1, e2, BoolTE(False), BoolT())
            elif e.op == '||':
                e1, e2 = new_args
                return IfTE(e1, BoolTE(True), e2, BoolT())
            else:
                raise Exception('shrink unknown prim:', e)
        elif isinstance(e, IfTE):
            return IfTE(shrink_exp(e.e1),
                        shrink_exp(e.e2),
                        shrink_exp(e.e3),
                        e.typ)
        elif isinstance(e, FuncallTE):
            return e
        elif isinstance(e, FunRefTE):
            return e
        else:
            raise Exception('shrink', e)

    new_defs = [shrink_def(d) for d in p.defs]
    new_body = shrink_exp(p.body)

    print(type(p))
    return RfunProgramT(new_defs, new_body)


##################################################
# uniquify
##################################################

def uniquify(p: RfunProgramT) -> RfunProgramT:
    """
    Makes the program's variable names unique
    :param e: The Rfun program to uniquify
    :return: An Rfun program with unique names
    """

    def uniquify_def(defn: RfunDefT) -> RfunDefT:
        # Need to uniquify the arguments to the function
        # So: gensym new names for the arguments
        # Create a new environment that maps arguments to their new names
        # and use it when we call uniquify_exp()

        # Must map the name of the arg variable to its gensymed name
        env = {arg_name: gensym(arg_name) for arg_name, _ in defn.args}

        new_body = uniquify_exp(defn.body, env)
        new_args = [(env[a_name], a_type) for a_name, a_type in defn.args]
        return RfunDefT(defn.name, new_args, defn.output_type, new_body)

    def uniquify_exp(e: RfunExpT, env: Dict[str, str]) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE)):
            return e
        elif isinstance(e, VarTE):
            return VarTE(env[e.var], e.typ)
        elif isinstance(e, LetTE):
            new_e1 = uniquify_exp(e.e1, env)
            new_x = gensym(e.x)
            new_env = {**env, e.x: new_x}
            new_body = uniquify_exp(e.body, new_env)
            return LetTE(new_x, new_e1, new_body)
        elif isinstance(e, PrimTE):
            new_args = [uniquify_exp(arg, env) for arg in e.args]
            return PrimTE(e.op, new_args, e.typ)
        elif isinstance(e, IfTE):
            return IfTE(uniquify_exp(e.e1, env),
                        uniquify_exp(e.e2, env),
                        uniquify_exp(e.e3, env),
                        e.typ)
        elif isinstance(e, FuncallTE):
            return e
        else:
            raise Exception('uniquify', e)

    new_defs = [uniquify_def(d) for d in p.defs]
    new_body = uniquify_exp(p.body, {})

    return RfunProgramT(new_defs, new_body)


##################################################
# reveal_functions
##################################################

def reveal_functions(p: RfunProgramT) -> RfunProgramT:
    """
    Transform references to top-level functions from variable references to
    function references.
    :param e: An Rfun program
    :return: An Rfun program in which all references to top-level functions
    are in the form of FunRef objects.
    """

    def reveal_functions_def(defn: RfunDefT, env: Set[str]) -> RfunDefT:
        new_body = reveal_functions_exp(defn.body, env)
        return RfunDefT(defn.name, defn.args, defn.output_type, new_body)

    def reveal_functions_exp(e: RfunExpT, env: Set[str]) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE)):
            return e
        elif isinstance(e, VarTE):
            if e.var in env:
                assert isinstance(e.typ, FunT)
                return FunRefTE(e.var, e.typ)
            else:
                return e
            # return VarTE(env[e.var], e.typ)
        elif isinstance(e, LetTE):
            new_e1 = reveal_functions_exp(e.e1, env)
            new_x = gensym(e.x)
            # Don't need to extend the environment here
            # new_env = {**env, e.x: new_x}
            new_body = reveal_functions_exp(e.body, env)
            return LetTE(new_x, new_e1, new_body)
        elif isinstance(e, PrimTE):
            new_args = [reveal_functions_exp(arg, env) for arg in e.args]
            return PrimTE(e.op, new_args, e.typ)
        elif isinstance(e, IfTE):
            return IfTE(reveal_functions_exp(e.e1, env),
                        reveal_functions_exp(e.e2, env),
                        reveal_functions_exp(e.e3, env),
                        e.typ)
        elif isinstance(e, FuncallTE):
            return FuncallTE(reveal_functions_exp(e.fun, env), e.args, e.typ)
        else:
            raise Exception('uniquify', e)

    # This should be a set of the names of top-level definitions
    env_top_level = set(d.name for d in p.defs)

    new_defs = [reveal_functions_def(d, env_top_level) for d in p.defs]
    new_body = reveal_functions_exp(p.body, env_top_level)

    return RfunProgramT(new_defs, new_body)


##################################################
# limit-functions
##################################################

# TODO if there is time
def limit_functions(p: RfunProgramT) -> RfunProgramT:
    """
    Limit functions to have at most 6 arguments.
    :param e: An Rfun program to reveal_functions
    :return: An Rfun program, in which each function has at most 6 arguments
    """

    return p


##################################################
# expose-alloc
##################################################

def mk_let(bindings: Dict[str, RfunExpT], body: RfunExpT):
    """
    Builds a Let expression from a list of bindings and a body.
    :param bindings: A list of bindings from variables (str) to their 
    expressions (RfunExp)
    :param body: The body of the innermost Let expression
    :return: A Let expression implementing the bindings in "bindings"
    """
    result = body
    for var, rhs in reversed(list(bindings.items())):
        result = LetTE(var, rhs, result)

    return result


def expose_alloc(p: RfunProgramT) -> RfunProgramT:
    """
    Transforms 'vector' forms into explicit memory allocations, with conditional
    calls to the garbage collector.
    :param e: A typed Rfun expression
    :return: A typed Rfun expression, without 'vector' forms
    """

    def expose_alloc_def(defn: RfunDefT) -> RfunDefT:
        new_body = expose_alloc_exp(defn.body)
        return RfunDefT(defn.name, defn.args, defn.output_type, new_body)

    def expose_alloc_exp(e: RfunExpT) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE, VarTE)):
            return e
        elif isinstance(e, LetTE):
            new_e1 = expose_alloc_exp(e.e1)
            new_body = expose_alloc_exp(e.body)
            return LetTE(e.x, new_e1, new_body)
        elif isinstance(e, PrimTE):
            new_args = [expose_alloc_exp(arg) for arg in e.args]

            if e.op == 'vector':
                vec_type = e.typ
                assert isinstance(vec_type, VectorT)

                bindings = {}

                # Step 1.
                # make a name for each element of the vector
                # bind the name to the input expression
                var_names = [gensym('v') for _ in new_args]
                for var, a in zip(var_names, new_args):
                    bindings[var] = a

                # Step 2.
                # run the collector if we don't have enough space
                # to do the allocation
                total_bytes = 8 + 8 * len(new_args)
                bindings[gensym('_')] = \
                    IfTE(PrimTE('<', [PrimTE('+', [GlobalValTE('free_ptr'),
                                                   IntTE(total_bytes)], IntT()),
                                      GlobalValTE('fromspace_end')], BoolT()),
                         VoidTE(),
                         PrimTE('collect', [IntTE(total_bytes)], VoidT()),
                         VoidT())

                # Step 3.
                # allocate the bytes for the vector and give it a name
                vec_name = gensym('vec')
                bindings[vec_name] = PrimTE('allocate', [IntTE(len(new_args))], vec_type)

                # Step 4.
                # vectorSet each element of the allocated vector to its variable
                # from Step 1
                for idx in range(len(new_args)):
                    typ = vec_type.types[idx]
                    var = var_names[idx]

                    bindings[gensym('_')] = PrimTE('vectorSet',
                                                   [
                                                       VarTE(vec_name, vec_type),
                                                       IntTE(idx),
                                                       VarTE(var, typ)
                                                   ],
                                                   VoidT())

                # Step 5.
                # Make a big Let with all the bindings
                return mk_let(bindings, VarTE(vec_name, vec_type))
            else:
                return PrimTE(e.op, new_args, e.typ)

        elif isinstance(e, IfTE):
            return IfTE(expose_alloc_exp(e.e1),
                        expose_alloc_exp(e.e2),
                        expose_alloc_exp(e.e3),
                        e.typ)
        elif isinstance(e, FuncallTE):
            return e
        elif isinstance(e, FunRefTE):
            return e
        else:
            raise Exception('expose_alloc', e)

    new_defs = [expose_alloc_def(d) for d in p.defs]
    new_body = expose_alloc_exp(p.body)

    return RfunProgramT(new_defs, new_body)


##################################################
# remove-complex-opera*
##################################################

def rco(p: RfunProgramT) -> RfunProgramT:
    """
    Removes complex operands. After this pass, the program will be in A-Normal
    Form (the arguments to Prim operations will be atomic).
    :param e: An Rfun expression
    :return: An Rfun expression in A-Normal Form
    """

    '''
    1. Add a function to handle definitions (`rco_def`)
    2. Add cases in rco_exp and rco_atm to handle function refs and calls
       - Funtion refs are NOT atomic
         - Function ref case in rco_atm needs to create a temporary variable
       - Function calls should be handled like Primitives
         - The function itself needs to be atomic (call rco_atm on e.fun)
         - Arguments need to be atomic (call rco_atm on them)
    '''

    def rco_def(defn: RfunDefT) -> RfunDefT:
        return RfunDefT(defn.name, defn.args, defn.output_type, rco_exp(defn.body))

    def rco_atm(e: RfunExpT, bindings: Dict[str, RfunExpT]) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE, VarTE)):
            return e
        elif isinstance(e, GlobalValTE):
            new_v = gensym('tmp')
            bindings[new_v] = e
            return VarTE(new_v, IntT())  # all global vals are ints
        elif isinstance(e, LetTE):
            new_e1 = rco_exp(e.e1)
            bindings[e.x] = new_e1
            v = rco_atm(e.body, bindings)
            return v
        elif isinstance(e, PrimTE):
            new_args = [rco_atm(arg, bindings) for arg in e.args]

            new_v = gensym('tmp')
            bindings[new_v] = PrimTE(e.op, new_args, e.typ)
            return VarTE(new_v, e.typ)
        elif isinstance(e, IfTE):
            new_if = IfTE(rco_atm(e.e1, bindings),
                          rco_atm(e.e2, bindings),
                          rco_atm(e.e3, bindings),
                          e.typ)
            new_v = gensym('tmp')
            bindings[new_v] = new_if
            return VarTE(new_v, e.typ)
        elif isinstance(e, FuncallTE):
            return e
        elif isinstance(e, FunRefTE):
            return e
        else:
            raise Exception('rco_atm', e)

    def rco_exp(e: RfunExpT) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE, VoidTE, VarTE, GlobalValTE)):
            return e
        elif isinstance(e, LetTE):
            new_e1 = rco_exp(e.e1)
            new_body = rco_exp(e.body)
            return LetTE(e.x, new_e1, new_body)
        elif isinstance(e, PrimTE):
            bindings: Dict[str, RfunExpT] = {}
            new_args = [rco_atm(arg, bindings) for arg in e.args]

            return mk_let(bindings, PrimTE(e.op, new_args, e.typ))
        elif isinstance(e, IfTE):
            return IfTE(rco_exp(e.e1),
                        rco_exp(e.e2),
                        rco_exp(e.e3),
                        e.typ)
        elif isinstance(e, FuncallTE):
            new_name = gensym('tmp')
            assert isinstance(e.fun, FunRefTE)
            var = FunRefTE(e.fun.name, e.fun.typ)
            inner_funcall = FuncallTE(VarTE(new_name, e.fun.typ), e.args, e.typ)

            return LetTE(new_name, var, inner_funcall)
        elif isinstance(e, FunRefTE):
            return e
        else:
            raise Exception('rco_exp', e)

    new_defs = [rco_def(d) for d in p.defs]
    new_body = rco_exp(p.body)

    return RfunProgramT(new_defs, new_body)


##################################################
# explicate-control
##################################################

def explicate_control(p: RfunProgramT) -> cfun.Program:
    """
    Transforms an Rfun Program into a Cfun program.
    :param e: An Rfun Program
    :return: A Cfun Program
    """

    def explicate_control_help(name: str, e: RfunExpT) -> Dict[str, cfun.Tail]:
        cfg: Dict[str, cfun.Tail] = {}

        def ec_atm(e: RfunExpT) -> cfun.Atm:
            if isinstance(e, IntTE):
                return cfun.Int(e.val)
            elif isinstance(e, BoolTE):
                return cfun.Bool(e.val)
            elif isinstance(e, VoidTE):
                return cfun.Void()
            elif isinstance(e, VarTE):
                return cfun.Var(e.var, e.typ)
            elif isinstance(e, GlobalValTE):
                return cfun.GlobalVal(e.var)
            else:
                raise Exception('ec_atm', e)

        def ec_exp(e: RfunExpT) -> cfun.Exp:
            if isinstance(e, PrimTE):
                return cfun.Prim(e.op, [ec_atm(a) for a in e.args], e.typ)
            elif isinstance(e, FunRefTE):
                # Produce a cfun FunRef
                return cfun.FunRef(e.name)
            else:
                return cfun.AtmExp(ec_atm(e))

        def ec_assign(x: str, e: RfunExpT, k: cfun.Tail) -> cfun.Tail:
            if isinstance(e, (IntTE, BoolTE, VoidTE, GlobalValTE)):
                return cfun.Seq(cfun.Assign(x, ec_exp(e), False), k)
            elif isinstance(e, VarTE):
                return cfun.Seq(cfun.Assign(x, ec_exp(e), isinstance(e.typ, VectorT)), k)
            elif isinstance(e, PrimTE):
                if e.op == 'collect':
                    num_bytes = e.args[0]
                    assert isinstance(num_bytes, IntTE)
                    return cfun.Seq(cfun.Collect(num_bytes.val), k)
                else:
                    return cfun.Seq(cfun.Assign(x, ec_exp(e), isinstance(e.typ, VectorT)), k)
            elif isinstance(e, LetTE):
                return ec_assign(e.x, e.e1, ec_assign(x, e.body, k))
            elif isinstance(e, IfTE):
                finally_label = gensym('label')
                cfg[finally_label] = k
                b2 = ec_assign(x, e.e2, cfun.Goto(finally_label))
                b3 = ec_assign(x, e.e3, cfun.Goto(finally_label))
                return ec_pred(e.e1, b2, b3)
            elif isinstance(e, FuncallTE):
                # Produce a **TailCall**, not Call - error by Joe?
                return cfun.TailCall(ec_atm(e.fun), [ec_atm(a) for a in e.args], e.typ)
            elif isinstance(e, FunRefTE):
                return cfun.Seq(cfun.Assign(k.fun.var, cfun.FunRef(e.name), False), k)
            else:
                raise Exception('ec_assign', e)

        def ec_pred(test: RfunExpT, b1: cfun.Tail, b2: cfun.Tail) -> cfun.Tail:
            if isinstance(test, BoolTE):
                if test.val:
                    return b1
                else:
                    return b2
            elif isinstance(test, VarTE):
                then_label = gensym('label')
                else_label = gensym('label')

                cfg[then_label] = b1
                cfg[else_label] = b2

                return cfun.If(cfun.Prim('==',
                                         [cfun.Var(test.var, test.typ), cfun.Bool(True)],
                                         BoolT()),
                               then_label,
                               else_label)

            elif isinstance(test, PrimTE):
                if test.op == 'not':
                    return ec_pred(test.args[0], b2, b1)
                else:
                    then_label = gensym('label')
                    else_label = gensym('label')

                    cfg[then_label] = b1
                    cfg[else_label] = b2

                    return cfun.If(ec_exp(test), then_label, else_label)

            elif isinstance(test, LetTE):
                body_block = ec_pred(test.body, b1, b2)
                return ec_assign(test.x, test.e1, body_block)

            elif isinstance(test, IfTE):
                label1 = gensym('label')
                label2 = gensym('label')
                cfg[label1] = b1
                cfg[label2] = b2

                new_b2 = ec_pred(test.e2, cfun.Goto(label1), cfun.Goto(label2))
                new_b3 = ec_pred(test.e3, cfun.Goto(label1), cfun.Goto(label2))

                return ec_pred(test.e1, new_b2, new_b3)

            else:
                raise Exception('ec_pred', test)

        def ec_tail(e: RfunExpT) -> cfun.Tail:
            if isinstance(e, (IntTE, BoolTE, VarTE, PrimTE)):
                return cfun.Return(ec_exp(e))
            elif isinstance(e, LetTE):
                return ec_assign(e.x, e.e1, ec_tail(e.body))
            elif isinstance(e, IfTE):
                b1 = ec_tail(e.e2)
                b2 = ec_tail(e.e3)
                return ec_pred(e.e1, b1, b2)
            elif isinstance(e, FuncallTE):
                # Produce a TailCall
                return cfun.TailCall(ec_atm(e.fun), [ec_atm(a) for a in e.args], e.typ)
            else:
                raise Exception('ec_tail', e)

        cfg[name] = ec_tail(e)
        return cfg

    new_defs = []
    for d in p.defs:
        cfg = explicate_control_help(d.name, d.body)
        new_def = cfun.Def(d.name, d.args, d.output_type, cfg)
        new_defs.append(new_def)

    cfg = explicate_control_help('main', p.body)
    new_def = cfun.Def('main', [], IntT(), cfg)
    new_defs.append(new_def)

    output_program = cfun.Program(new_defs)
    return output_program


##################################################
# select-instructions
##################################################

def select_instructions(p: cfun.Program) -> Dict[str, x86.Program]:
    """
    Transforms a Cfun program into a pseudo-x86 assembly program.
    :param p: a Cfun program
    :return: a set of pseudo-x86 definitions, as a dictionary mapping function
    names to pseudo-x86 programs.
    """

    def select_instructions_help(p: cfun.Def) -> x86.Program:
        """
        Transforms a Cif program into a pseudo-x86 assembly program.
        :param p: a Cif program
        :return: a pseudo-x86 program
        """

        def mk_var(x: str, is_vec: bool) -> x86.Arg:
            if is_vec:
                return x86.VecVar(x)
            else:
                return x86.Var(x)

        def si_atm(a: cfun.Atm) -> x86.Arg:
            if isinstance(a, cfun.Int):
                return x86.Int(a.val)
            if isinstance(a, cfun.Bool):
                if a.val == True:
                    return x86.Int(1)
                elif a.val == False:
                    return x86.Int(0)
                else:
                    raise Exception('si_atm', a)
            elif isinstance(a, cfun.Var):
                return mk_var(a.var, isinstance(a.typ, VectorT))
            elif isinstance(a, cfun.GlobalVal):
                return x86.GlobalVal(a.val)
            elif isinstance(a, cfun.Void):
                return x86.Int(0)
            else:
                raise Exception('si_atm', a)

        op_cc = {
            '==': 'e',
            '>': 'g',
            '<': 'l',
        }

        def mk_tag(types: List[RfunType]) -> int:
            """
            Builds a vector tag. See section 5.2.2 in the textbook.
            :param types: A list of the types of the vector's elements.
            :return: A vector tag, as an integer.
            """
            pointer_mask = 0
            # for each type in the vector, encode it in the pointer mask
            for t in types:
                # shift the mask by 1 bit to make room for this type
                pointer_mask = pointer_mask << 1

                if isinstance(t, VectorT):
                    # if it's a vector type, the mask is 1
                    pointer_mask = pointer_mask + 1
                else:
                    # otherwise, the mask is 0 (do nothing)
                    pass

            # shift the pointer mask by 6 bits to make room for the length field
            mask_and_len = pointer_mask << 6
            mask_and_len = mask_and_len + len(types)  # add the length

            # shift the mask and length by 1 bit to make room for the forwarding bit
            tag = mask_and_len << 1
            tag = tag + 1

            return tag

        def si_stmt(e: cfun.Stmt) -> List[x86.Instr]:
            if isinstance(e, cfun.Collect):
                return [x86.Movq(x86.Reg('r15'), x86.Reg('rdi')),
                        x86.Movq(x86.Int(e.amount), x86.Reg('rsi')),
                        x86.Callq('collect')]

            elif isinstance(e, cfun.Assign):
                if isinstance(e.exp, cfun.AtmExp):
                    return [x86.Movq(si_atm(e.exp.atm), mk_var(e.var, e.is_vec))]
                elif isinstance(e.exp, cfun.Prim):
                    if e.exp.op == '+':
                        a1, a2 = e.exp.args
                        return [x86.Movq(si_atm(a1), mk_var(e.var, e.is_vec)),
                                x86.Addq(si_atm(a2), mk_var(e.var, e.is_vec))]
                    elif e.exp.op in ['==', '<']:
                        a1, a2 = e.exp.args
                        return [x86.Cmpq(si_atm(a2), si_atm(a1)),
                                x86.Set(op_cc[e.exp.op], x86.ByteReg('al')),
                                x86.Movzbq(x86.ByteReg('al'), mk_var(e.var, e.is_vec))]
                    elif e.exp.op == 'not':
                        arg = si_atm(e.exp.args[0])

                        return [x86.Movq(arg, mk_var(e.var, e.is_vec)),
                                x86.Xorq(x86.Int(1), mk_var(e.var, e.is_vec))]
                    elif e.exp.op == 'allocate':
                        vec_type = e.exp.typ
                        assert isinstance(vec_type, VectorT)

                        tag = mk_tag(vec_type.types)
                        total_bytes = 8 + 8 * len(vec_type.types)

                        return [x86.Movq(x86.GlobalVal('free_ptr'), mk_var(e.var, e.is_vec)),
                                x86.Addq(x86.Int(total_bytes), x86.GlobalVal('free_ptr')),
                                x86.Movq(mk_var(e.var, e.is_vec), x86.Reg('r11')),
                                x86.Movq(x86.Int(tag), x86.Deref(0, 'r11'))]
                    elif e.exp.op == 'vectorSet':
                        a1, idx, a2 = e.exp.args
                        assert isinstance(idx, cfun.Int)

                        offset = 8 * (idx.val + 1)

                        return [x86.Movq(si_atm(a1), x86.Reg('r11')),
                                x86.Movq(si_atm(a2), x86.Deref(offset, 'r11')),
                                x86.Movq(x86.Int(0), mk_var(e.var, e.is_vec))]

                    elif e.exp.op == 'vectorRef':
                        a1, idx = e.exp.args
                        assert isinstance(idx, cfun.Int)

                        offset = 8 * (idx.val + 1)

                        return [x86.Movq(si_atm(a1), x86.Reg('r11')),
                                x86.Movq(x86.Deref(offset, 'r11'), mk_var(e.var, e.is_vec))]
                elif isinstance(e.exp, cfun.FunRef):
                    return [x86.Leaq(x86.FunRef(e.exp.label), x86.Var(e.var))]
                elif isinstance(e.exp, cfun.Call):
                    pass
                raise Exception('si_stmt Assign', e)
            else:
                raise Exception('si_stmt', e)

        def si_tail(e: cfun.Tail) -> List[x86.Instr]:
            if isinstance(e, cfun.Return):
                new_var = gensym('retvar')
                instrs = si_stmt(cfun.Assign(new_var, e.exp, False))

                return instrs + \
                       [x86.Movq(mk_var(new_var, False), x86.Reg('rax')),
                        x86.Jmp(p.name + '_conclusion')]
            elif isinstance(e, cfun.Seq):
                return si_stmt(e.stmt) + si_tail(e.tail)
            elif isinstance(e, cfun.If):
                assert isinstance(e.test, cfun.Prim)
                e1, e2 = e.test.args
                return [x86.Cmpq(si_atm(e2), si_atm(e1)),
                        x86.JmpIf(e.test.op, e.then_label),
                        x86.Jmp(e.else_label)]
            elif isinstance(e, cfun.Goto):
                return [x86.Jmp(e.label)]
            elif isinstance(e, cfun.TailCall):
                instrs = []

                for i, a in enumerate(e.args):
                    instrs.append(
                        x86.Movq(si_atm(a), x86.Reg(constants.parameter_passing_registers[i])))
                assert isinstance(e.fun, cfun.Var)
                instrs.append(x86.TailJmp(x86.Var(e.fun.var), len(e.args)))
                return instrs
            else:
                raise Exception('si_tail', e)

        return x86.Program({label + '_start': si_tail(block) for (label, block) in p.blocks.items()})

    defs = p.defs
    results = {}

    for d in defs:
        progs = select_instructions_help(d)

        if d.args and d.name != 'main':
            instrs = []
            for i, a in enumerate(d.args):
                print(constants.parameter_passing_registers[i])
                instrs.append(x86.Movq(x86.Reg(constants.parameter_passing_registers[i]), x86.Var(a[0])))

            progs.blocks[d.name + '_start'] = instrs + progs.blocks[d.name + '_start']
        results[d.name] = progs

    return results


##################################################
# uncover-live
##################################################

def uncover_live(program: Dict[str, x86.Program]) -> Tuple[Dict[str, x86.Program], Dict[str, List[Set[x86.Var]]]]:
    """
    Performs liveness analysis. Returns the input program, plus live-after sets
    for its blocks.
    :param program: pseudo-x86 assembly program definitions
    :return: A tuple. The first element is the same as the input program. The
    second element is a dict of live-after sets. This dict maps each label in
    the program to a list of live-after sets for that label. The live-after
    sets are in the same order as the label's instructions.
    """

    def uncover_live_help(p: x86.Program) -> Tuple[x86.Program, Dict[str, List[Set[x86.Var]]]]:
        label_live: Dict[str, Set[x86.Var]] = {}

        live_after_sets: Dict[str, List[Set[x86.Var]]] = {}

        blocks = p.blocks

        def vars_arg(a: x86.Arg) -> Set[x86.Var]:
            if isinstance(a, (x86.Int, x86.Reg, x86.ByteReg, x86.Deref, x86.GlobalVal)):
                return set()
            elif isinstance(a, (x86.Var, x86.VecVar, x86.FunRef)):
                return {a}
            else:
                raise Exception('ul_arg', a)

        def ul_instr(e: x86.Instr, live_after: Set[x86.Var]) -> Set[x86.Var]:
            if isinstance(e, (x86.Movq, x86.Movzbq, x86.Leaq)):
                return live_after.difference(vars_arg(e.e2)).union(vars_arg(e.e1))
            elif isinstance(e, (x86.Addq, x86.Xorq)):
                return live_after.union(vars_arg(e.e1).union(vars_arg(e.e2)))
            elif isinstance(e, (x86.Callq, x86.Retq, x86.Set)):
                return live_after
            elif isinstance(e, x86.Cmpq):
                return live_after.union(vars_arg(e.e1).union(vars_arg(e.e2)))
            elif isinstance(e, (x86.Jmp, x86.JmpIf)):
                if e.label not in label_live:
                    # TODO This line causes KeyError on add_conclusion
                    ul_block(e.label)

                return live_after.union(label_live[e.label])
            elif isinstance(e, x86.TailJmp):
                return live_after.union(vars_arg(e.e1))
            else:
                raise Exception('ul_instr', e)

        def ul_block(label: str):
            instrs = blocks[label]

            current_live_after: Set[x86.Var] = set()

            local_live_after_sets = []
            for i in reversed(instrs):
                local_live_after_sets.append(current_live_after)
                current_live_after = ul_instr(i, current_live_after)

            live_after_sets[label] = list(reversed(local_live_after_sets))
            label_live[label] = current_live_after

        conclusion_name = list(blocks.keys())[0].replace('start', 'conclusion')
        label_live[conclusion_name] = set()
        ul_block(list(blocks.keys())[0])

        return p, live_after_sets

    block_live_after_sets = {}
    for label, prog in program.items():
        new_prog, live_after_sets = uncover_live_help(prog)
        new_label = label + '_start'
        block_live_after_sets[new_label] = live_after_sets[new_label]

    return program, block_live_after_sets


##################################################
# build-interference
##################################################

class InterferenceGraph:
    """
    A class to represent an interference graph: an undirected graph where nodes 
    are x86.Arg objects and an edge between two nodes indicates that the two
    nodes cannot share the same locations.
    """
    graph: DefaultDict[x86.Arg, Set[x86.Arg]]

    def __init__(self):
        self.graph = defaultdict(lambda: set())

    def add_edge(self, a: x86.Arg, b: x86.Arg):
        if a != b:
            self.graph[a].add(b)
            self.graph[b].add(a)

    def neighbors(self, a: x86.Arg) -> Set[x86.Arg]:
        if a in self.graph:
            return self.graph[a]
        else:
            return set()

    def __str__(self):
        strings = []
        for k, v in dict(self.graph).items():
            if isinstance(k, (x86.Var, x86.VecVar)):
                t = ', '.join([print_ast(i) for i in v])
                tt = '\n      '.join(textwrap.wrap(t))
                strings.append(f'{print_ast(k)}: {tt}')
        lines = '\n  '.join(strings)
        return f'InterferenceGraph (\n  {lines}\n )\n'


def build_interference(inputs: Tuple[Dict[str, x86.Program],
                                     Dict[str, List[Set[x86.Var]]]]) -> \
        Tuple[Dict[str, x86.Program],
              Dict[str, InterferenceGraph]]:
    """
    Build the interference graph.
    :param inputs: A Tuple. The first element is a pseudo-x86 program. The 
    second element is the dict of live-after sets produced by the uncover-live 
    pass.
    :return: A Tuple. The first element is the same as the input program. 
    The second is a dict mapping each function name to its completed 
    interference graph.
    """

    def build_interference_help(inputs: Tuple[x86.Program, Dict[str, List[Set[x86.Var]]]]) -> \
            Tuple[x86.Program, InterferenceGraph]:
        """
        Build the interference graph.
        :param inputs: A Tuple. The first element is a pseudo-x86 program. The second element is the dict of live-after
        sets produced by the uncover-live pass.
        :return: A Tuple. The first element is the same as the input program. The second is a completed interference graph.
        """

        caller_saved_registers = [x86.Reg(r) for r in constants.caller_saved_registers]
        callee_saved_registers = [x86.Reg(r) for r in constants.callee_saved_registers]

        def vars_arg(a: x86.Arg) -> Set[x86.Var]:
            if isinstance(a, (x86.Int, x86.Deref, x86.GlobalVal)):
                return set()
            elif isinstance(a, (x86.Reg, x86.Var, x86.VecVar)):
                return {a}
            else:
                raise Exception('bi_arg', a)

        def writes_of(e: x86.Instr) -> Set[x86.Var]:
            if isinstance(e, (x86.Movq, x86.Addq, x86.Movzbq, x86.Xorq, x86.Leaq)):
                return vars_arg(e.e2)
            elif isinstance(e, (x86.Callq, x86.Retq, x86.Jmp)):
                return set()
            else:
                raise Exception('writes_of', e)

        def bi_instr(e: x86.Instr, live_after: Set[x86.Var], graph: InterferenceGraph):
            if isinstance(e, (x86.Movq, x86.Addq, x86.Movzbq, x86.Xorq, x86.Leaq)):
                for v1 in writes_of(e):
                    for v2 in live_after:
                        graph.add_edge(v1, v2)
            elif isinstance(e, (x86.Callq, x86.IndirectCallq, x86.TailJmp)):
                for v in live_after:
                    for r in caller_saved_registers:
                        graph.add_edge(v, r)
                    if isinstance(v, x86.VecVar):
                        for r in callee_saved_registers:
                            graph.add_edge(v, r)
            elif isinstance(e, (x86.Retq, x86.Jmp, x86.Cmpq, x86.Jmp, x86.JmpIf, x86.Set)):
                pass
            else:
                raise Exception('bi_instr', e)

        def bi_block(instrs: List[x86.Instr], live_afters: List[Set[x86.Var]], graph: InterferenceGraph):
            for instr, live_after in zip(instrs, live_afters):
                bi_instr(instr, live_after, graph)

        program, live_after_sets = inputs
        blocks = program.blocks

        interference_graph = InterferenceGraph()

        for label in blocks.keys():
            bi_block(blocks[label], live_after_sets[label], interference_graph)

        return program, interference_graph

    prog, live_after_sets = inputs

    progs = {}
    interference_graph = {}
    for p, s in prog.items():
        progs[p] = s
        interference_graph[p] = build_interference_help((s, live_after_sets))[1]

    return progs, interference_graph


##################################################
# allocate-registers
##################################################


Color = int
Coloring = Dict[x86.Var, Color]
Saturation = Set[Color]


def allocate_registers(inputs: Tuple[Dict[str, x86.Program],
                                     Dict[str, InterferenceGraph]]) -> \
        Dict[str, Tuple[x86.Program, int, int]]:
    """
    Assigns homes to variables in the input program. Allocates registers and 
    stack locations as needed, based on a graph-coloring register allocation 
    algorithm.
    :param inputs: A Tuple. The first element is the pseudo-x86 program. The
    second element is a dict mapping function names to interference graphs.

    :return: A dict mapping each function name to a Tuple. The first element
    of each tuple is an x86 program (with no variable references). The second
    element is the number of bytes needed in regular stack locations. The third
    element is the number of variables spilled to the root (shadow) stack.
    """

    def allocate_registers_help(inputs: Tuple[x86.Program, InterferenceGraph]) -> \
            Tuple[x86.Program, int, int]:
        """
        Assigns homes to variables in the input program. Allocates registers and
        stack locations as needed, based on a graph-coloring register allocation
        algorithm.
        :param inputs: A Tuple. The first element is the pseudo-x86 program. The
        second element is the completed interference graph.
        :return: A Tuple. The first element is an x86 program (with no variable
        references). The second element is the number of bytes needed in regular
        stack locations. The third element is the number of bytes needed in root
        (shadow) stack locations.
        """

        # Functions for listing the variables in the program
        def vars_arg(a: x86.Arg) -> Set[x86.Var]:
            if isinstance(a, (x86.Int, x86.Reg, x86.ByteReg, x86.GlobalVal, x86.FunRef, x86.Deref)):
                return set()
            elif isinstance(a, x86.Var):
                return {a}
            else:
                raise Exception('vars_arg allocate_registers', a)

        def vars_instr(e: x86.Instr) -> Set[x86.Var]:
            if isinstance(e, (x86.Movq, x86.Addq, x86.Cmpq, x86.Movzbq, x86.Xorq, x86.Leaq)):
                return vars_arg(e.e1).union(vars_arg(e.e2))
            elif isinstance(e, x86.Set):
                return vars_arg(e.e1)
            elif isinstance(e, (x86.Callq, x86.Retq, x86.Jmp, x86.JmpIf, x86.TailJmp, x86.IndirectCallq)):
                return set()
            else:
                raise Exception('vars_instr allocate_registers', e)

        # Defines the set of registers to use
        register_locations = [x86.Reg(r) for r in
                              constants.caller_saved_registers + constants.callee_saved_registers]

        # Functions for graph coloring
        def color_graph(local_vars: Set[x86.Var], interference_graph: InterferenceGraph) -> Coloring:
            coloring = {}

            to_color = local_vars.copy()
            saturation_sets = {x: set() for x in local_vars}

            # init the saturation sets
            for color, register in enumerate(register_locations):
                for neighbor in interference_graph.neighbors(register):
                    if isinstance(neighbor, x86.Var):
                        saturation_sets[neighbor].add(color)

            while to_color:
                x = max(to_color, key=lambda x: len(saturation_sets[x]))
                to_color.remove(x)

                x_color = next(i for i in itertools.count() if i not in saturation_sets[x])
                coloring[x] = x_color

                for y in interference_graph.neighbors(x):
                    if isinstance(y, x86.Var):
                        saturation_sets[y].add(x_color)

            return coloring

        # Functions for replacing variables with their homes
        homes: Dict[str, x86.Arg] = {}

        def ah_arg(a: x86.Arg) -> x86.Arg:
            if isinstance(a, (x86.Int, x86.Reg, x86.ByteReg, x86.GlobalVal, x86.FunRef, x86.Deref)):
                return a
            elif isinstance(a, x86.Var):
                return homes[a]
            else:
                raise Exception('ah_arg', a)

        def ah_instr(e: x86.Instr) -> x86.Instr:
            if isinstance(e, x86.Addq):
                return x86.Addq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Movq):
                return x86.Movq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Cmpq):
                return x86.Cmpq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Xorq):
                return x86.Xorq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Movzbq):
                return x86.Movzbq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Leaq):
                return x86.Leaq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.IndirectCallq):
                # TODO not sure of this case
                # return e
                return x86.IndirectCallq(ah_arg(e.e1), e.num_args)
            elif isinstance(e, x86.TailJmp):
                return x86.TailJmp(ah_arg(e.e1), e.num_args)
            elif isinstance(e, x86.Set):
                return x86.Set(e.cc, ah_arg(e.e1))
            elif isinstance(e, (x86.Callq, x86.Retq, x86.Jmp, x86.JmpIf)):
                return e
            else:
                raise Exception('ah_instr', e)

        def ah_block(instrs: List[x86.Instr]) -> List[x86.Instr]:
            return [ah_instr(i) for i in instrs]

        def align(num_bytes: int) -> int:
            if num_bytes % 16 == 0:
                return num_bytes
            else:
                return num_bytes + (16 - (num_bytes % 16))

        # Main body of the pass
        program, interference_graph = inputs
        blocks = program.blocks

        local_vars = set()
        for block in blocks.values():
            for instr in block:
                local_vars = local_vars.union(vars_instr(instr))

        coloring = color_graph(local_vars, interference_graph)
        color_map = dict(enumerate(register_locations))
        vec_color_map = dict(enumerate(register_locations))

        stack_spills = 0
        root_stack_spills = 0

        # fill in locations in the color map
        for v in local_vars:
            if isinstance(v, x86.VecVar):
                color = coloring[v]
                if color in vec_color_map:
                    pass
                else:
                    root_stack_spills = root_stack_spills + 1
                    offset = root_stack_spills + 1
                    vec_color_map[color] = x86.Deref(-(offset * 8), 'r15')
            elif isinstance(v, x86.Var):
                color = coloring[v]
                if color in color_map:
                    pass
                else:
                    stack_spills = stack_spills + 1
                    offset = stack_spills + 1
                    color_map[color] = x86.Deref(-(offset * 8), 'rbp')

        # build "homes"
        for v in local_vars:
            color = coloring[v]
            if isinstance(v, x86.VecVar):
                homes[v] = vec_color_map[color]
            elif isinstance(v, x86.Var):
                homes[v] = color_map[color]

        blocks = program.blocks
        new_blocks = {label: ah_block(block) for label, block in blocks.items()}
        return x86.Program(new_blocks), align(8 * stack_spills), root_stack_spills

    prog, igs = inputs

    progs = {}
    for p, s in prog.items():
        progs[p] = allocate_registers_help((s, igs[p]))

    return progs


##################################################
# patch-instructions
##################################################

def patch_instructions(inputs: Dict[str, Tuple[x86.Program, int, int]]) -> \
        Dict[str, Tuple[x86.Program, int, int]]:
    """
    Patches instructions with two memory location inputs, using %rax as a 
    temporary location.
    :param inputs: A dict mapping each function name to a Tuple. The first
    element of each tuple is an x86 program. The second element is the stack
    space in bytes. The third is the number of variables spilled to the root
    stack.
    :return: A Tuple. The first element is the patched x86 program. The second
    and third elements stay the same.
    """

    def patch_instructions_help(inputs: Tuple[x86.Program, int, int]) -> Tuple[x86.Program, int, int]:
        """
        Patches instructions with two memory location inputs, using %rax as a
        temporary location.
        :param inputs: A Tuple. The first element is an x86 program. The second
        element is the stack space in bytes.
        :return: A Tuple. The first element is the patched x86 program. The second
        element is the stack space in bytes.
        """

        def pi_instr(e: x86.Instr) -> List[x86.Instr]:
            if isinstance(e, x86.Movq) and \
                    isinstance(e.e1, x86.Deref) and \
                    isinstance(e.e2, x86.Deref):
                return [x86.Movq(e.e1, x86.Reg('rax')),
                        x86.Movq(x86.Reg('rax'), e.e2)]
            elif isinstance(e, x86.Addq) and \
                    isinstance(e.e1, x86.Deref) and \
                    isinstance(e.e2, x86.Deref):
                return [x86.Movq(e.e1, x86.Reg('rax')),
                        x86.Addq(x86.Reg('rax'), e.e2)]
            elif isinstance(e, x86.Cmpq) and \
                    isinstance(e.e2, x86.Int):
                return [x86.Movq(e.e2, x86.Reg('rax')),
                        x86.Cmpq(e.e1, x86.Reg('rax'))]
            elif isinstance(e, x86.Leaq) and \
                    isinstance(e.e2, x86.Deref):
                return [x86.Movq(e.e1, x86.Reg('rax')),
                        x86.Leaq(x86.Reg('rax'), e.e2)]
            elif isinstance(e, x86.TailJmp):
                return [x86.Movq(e.e1, x86.Reg('rax')),
                        x86.TailJmp(x86.Reg('rax'), e.num_args)]
            elif isinstance(e, (x86.Callq, x86.Retq, x86.Jmp, x86.JmpIf,
                                x86.Movq, x86.Addq, x86.Cmpq, x86.Set,
                                x86.Movzbq, x86.Xorq, x86.Leaq)):
                return [e]
            else:
                raise Exception('pi_instr', e)

        def pi_block(instrs: List[x86.Instr]) -> List[x86.Instr]:
            new_instrs = [pi_instr(i) for i in instrs]
            flattened = [val for sublist in new_instrs for val in sublist]
            return flattened

        program, stack_size, root_stack_spills = inputs
        blocks = program.blocks
        new_blocks = {label: pi_block(block) for label, block in blocks.items()}
        return (x86.Program(new_blocks), stack_size, root_stack_spills)

    programs = {}
    for block_name, prog in inputs.items():
        programs[block_name] = patch_instructions_help(prog)

    return programs

##################################################
# print-x86
##################################################

def print_x86(inputs: Dict[str, Tuple[x86.Program, int, int]]) -> str:
    """
    Prints an x86 program to a string.
    :param inputs: A dict mapping each function name to a Tuple. The first
    element of the Tuple is an x86 program. The second element is the stack
    space in bytes. The third is the number of variables spilled to the
    root stack.
    :return: A string, ready for gcc.
    """

    def print_x86_help(function_name: str, inputs: Tuple[x86.Program, int, int]) -> str:
        """
        Prints an x86 program to a string.
        :param inputs: A Tuple. The first element is the x86 program. The second
        element is the stack space in bytes.
        :return: A string, ready for gcc.
        """

        def print_arg(a: x86.Arg) -> str:
            if isinstance(a, x86.Int):
                return f'${a.val}'
            elif isinstance(a, (x86.Reg, x86.ByteReg)):
                return f'%{a.val}'
            elif isinstance(a, x86.Var):
                return f'#{a.var}'
            elif isinstance(a, x86.VecVar):
                return f'##{a.var}'
            elif isinstance(a, x86.Deref):
                return f'{a.offset}(%{a.val})'
            elif isinstance(a, x86.GlobalVal):
                return f'{a.val}(%rip)'
            elif isinstance(a, x86.FunRef):
                return f'{a.label}(%rip)'
            else:
                raise Exception('print_arg', a)

        ccs = {
            '==': 'e',
            '<': 'l',
            '<=': 'le',
            '>': 'g',
            '>=': 'ge'
        }

        def print_instr(e: x86.Instr) -> str:
            if isinstance(e, x86.Movq):
                return f'movq {print_arg(e.e1)}, {print_arg(e.e2)}'
            elif isinstance(e, x86.Addq):
                return f'addq {print_arg(e.e1)}, {print_arg(e.e2)}'
            elif isinstance(e, x86.Cmpq):
                return f'cmpq {print_arg(e.e1)}, {print_arg(e.e2)}'
            elif isinstance(e, x86.Movzbq):
                return f'movzbq {print_arg(e.e1)}, {print_arg(e.e2)}'
            elif isinstance(e, x86.Xorq):
                return f'xorq {print_arg(e.e1)}, {print_arg(e.e2)}'
            elif isinstance(e, x86.Leaq):
                return f'leaq {print_arg(e.e1)}, {print_arg(e.e2)}'
            elif isinstance(e, x86.Callq):
                return f'callq {e.label}'
            elif isinstance(e, x86.TailJmp):
                if function_name == 'main':
                    return '\n  '.join([f'callq *{print_arg(e.e1)}',
                                        f'jmp main_conclusion'])
                else:
                    return '\n  '.join(['addq $0, %rsp',
                                        'subq $0, %r15',
                                        'popq %r14',
                                        'popq %r13',
                                        'popq %r12',
                                        'popq %rbx',
                                        'popq %rbp',
                                        f'jmp *{print_arg(e.e1)}'])
            elif isinstance(e, x86.Retq):
                return f'retq'
            elif isinstance(e, x86.Jmp):
                return f'jmp {e.label}'
            elif isinstance(e, x86.JmpIf):
                cc = ccs[e.cc]
                return f'j{cc} {e.label}'
            elif isinstance(e, x86.Set):
                return f'set{e.cc} {print_arg(e.e1)}'
            else:
                raise Exception('print_instr', e)

        def print_block(label: str, instrs: List[x86.Instr]) -> str:
            name = f'{label}:\n'
            instr_strs = '\n'.join(['  ' + print_instr(i) for i in instrs])
            return name + instr_strs

        program, stack_size, root_stack_spills = inputs
        blocks = program.blocks
        block_instrs = '\n'.join([print_block(label, block) for label, block in blocks.items()])

        root_stack_inits = ''
        for i in range(root_stack_spills):
            root_stack_inits = root_stack_inits + '  movq $0, (%r15)\n  addq $8, %r15\n'

        # TODO Change
        initialize = ''
        main_stack = ''
        conclusion = ''
        if function_name == 'main':
            initialize = '\n  movq $16384, %rdi\n  movq $16, %rsi\n  callq initialize\n  movq rootstack_begin(%rip), %r15'
            conclusion = '\n  movq %rax, %rdi\n  callq print_int\n  movq $0, %rax\n'

        final_program = f"""
  .globl {function_name}
{function_name}:
  pushq %rbp
  movq %rsp, %rbp
  subq ${stack_size}, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14
{initialize}
{root_stack_inits}
  jmp {function_name}_start
{block_instrs}
{function_name}_conclusion:
{conclusion}
  addq ${stack_size}, %rsp
  subq ${stack_size}, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
"""
        return final_program

    return ''.join(print_x86_help(block_name, prog) for block_name, prog in inputs.items())

##################################################
# Compiler definition
##################################################

compiler_passes = {
    'typecheck': typecheck,
    'shrink': shrink,
    'uniquify': uniquify,
    'reveal functions': reveal_functions,
    'limit functions': limit_functions,
    'expose allocation': expose_alloc,
    'remove complex opera*': rco,
    'explicate control': explicate_control,
    'select instructions': select_instructions,
    'uncover live': uncover_live,
    'build interference': build_interference,
    'allocate registers': allocate_registers,
    'patch instructions': patch_instructions,
    'print x86': print_x86
}


def run_compiler(s: str, logging=False) -> str:
    """
    Run the compiler on an input program.
    :param s: An Rfun program, as a string.
    :param logging: Whether or not to print out debugging information.
    :return: An x86 program, as a string
    """
    current_program = parse_rfun(s)

    # TODO Remove
    print('::::::::::input program::::::::::')
    input_program = '' + s
    print(input_program)
    print(':::::::::::::::::::::::::::::::::')

    if logging == True:
        print()
        print('==================================================')
        print(' Input program')
        print('==================================================')
        print()
        print(print_ast(current_program))

    for pass_name, pass_fn in compiler_passes.items():
        # TODO Remove
        try:
            current_program = pass_fn(current_program)
        except Exception as e:
            print('=====================')
            print('exception was raised:', e)
            pc.copy(s)
            print('Pass result copied. [Enter] to copy the input program: ', end='')
            input()
            pc.copy(input_program)
            print('done!')
            raise e

        if logging:
            print()
            print('==================================================')
            print(f' Output of pass: {pass_name}')
            print('==================================================')
            print()
            # TODO Remove pyperclip call
            s = print_ast(current_program)
            pc.copy(s)
            print(s)
            # TODO Uncomment
            # print(print_ast(current_program))

    assert isinstance(current_program, str)
    return current_program


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python compiler.py <source filename>')
    else:
        file_name = sys.argv[1]
        with open(file_name) as f:
            print(f'Compiling program {file_name}...')

            program = f.read()
            x86_program = run_compiler(program, logging=True)

            with open(file_name + '.s', 'w') as output_file:
                output_file.write(x86_program)
