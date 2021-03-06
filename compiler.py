from collections import OrderedDict, defaultdict
from typing import List, Set, Dict, Tuple, DefaultDict, Union, ItemsView
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
from icecream import ic

gensym_num = 0


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
    :param p: The Rfun program to typecheck
    :return: The program, if it is well-typed
    """

    prim_arg_types = {
        '+':   [IntT(), IntT()],
        'not': [BoolT()],
        'neg': [IntT()],
        '||':  [BoolT(), BoolT()],
        '&&':  [BoolT(), BoolT()],
        '>':   [IntT(), IntT()],
        '>=':  [IntT(), IntT()],
        '<':   [IntT(), IntT()],
        '<=':  [IntT(), IntT()],
    }

    prim_output_types = {
        '+':   IntT(),
        'not': BoolT(),
        'neg': IntT(),
        '||':  BoolT(),
        '&&':  BoolT(),
        '>':   BoolT(),
        '>=':  BoolT(),
        '<':   BoolT(),
        '<=':  BoolT(),
    }

    def tc_def(defn: RfunDef, env: TEnv) -> RfunDefT:
        arg_env = {x: t for x, t in defn.args}
        new_env = {**env, **arg_env}

        t_body, new_body = tc_exp(defn.body, new_env)
        assert t_body == defn.output_type

        return RfunDefT(defn.name,
                        defn.args,
                        defn.output_type,
                        new_body)

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
                types, new_es = unzip2(results)
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
                arg_types, new_es = unzip2(results)
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
            t_fun, new_fun = tc_exp(e.fun, env)
            results = [tc_exp(a, env) for a in e.args]
            arg_types, new_es = unzip2(results)

            assert isinstance(t_fun, FunT)
            assert t_fun.arg_types == list(arg_types), (t_fun, list(arg_types))

            return t_fun.return_type, FuncallTE(new_fun, new_es, t_fun.return_type)

        else:
            raise Exception('tc_exp', e)

    init_env = {}

    for defn in p.defs:
        arg_types = [arg_type for arg_name, arg_type in defn.args]
        init_env[defn.name] = FunT(arg_types, defn.output_type)

    new_defs = [tc_def(d, init_env) for d in p.defs]
    typ, new_body = tc_exp(p.body, init_env)
    return RfunProgramT(new_defs, new_body)


##################################################
# shrink
##################################################

def shrink(p: RfunProgramT) -> RfunProgramT:
    """
    Eliminates some operators from Rfun
    :param p: The Rfun program to shrink
    :return: A shrunken Rfun program
    """

    def shrink_def(defn: RfunDefT) -> RfunDefT:
        return RfunDefT(defn.name,
                        defn.args,
                        defn.output_type,
                        shrink_exp(defn.body))

    def shrink_exp(e: RfunExpT) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE, VarTE)):
            return e
        elif isinstance(e, LetTE):
            new_e1 = shrink_exp(e.e1)
            new_body = shrink_exp(e.body)
            return LetTE(e.x, new_e1, new_body)
        elif isinstance(e, PrimTE):
            new_args = [shrink_exp(arg) for arg in e.args]

            if e.op in ['+', 'not', '==', '<', 'neg', 'vector', 'vectorRef', 'vectorSet']:
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
            new_args = [shrink_exp(a) for a in e.args]
            return FuncallTE(shrink_exp(e.fun), new_args, e.typ)
        else:
            raise Exception('shrink', e)

    new_defs = [shrink_def(d) for d in p.defs]
    new_body = shrink_exp(p.body)
    return RfunProgramT(new_defs, new_body)


##################################################
# uniquify
##################################################

def uniquify(p: RfunProgramT) -> RfunProgramT:
    """
    Makes the program's variable names unique
    :param p: The Rfun program to uniquify
    :return: An Rfun program with unique names
    """

    def uniquify_def(defn: RfunDefT, env: Dict[str, str]) -> RfunDefT:
        arg_names, arg_types = unzip2(defn.args)
        new_arg_names = [gensym(x) for x in arg_names]
        new_args = list(zip(new_arg_names, arg_types))

        arg_env = {a1: a2 for a1, a2 in zip(arg_names, new_arg_names)}
        new_env = {**env, **arg_env}

        return RfunDefT(defn.name,
                        new_args,
                        defn.output_type,
                        uniquify_exp(defn.body, new_env))

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
            new_args = [uniquify_exp(arg, env) for arg in e.args]
            return FuncallTE(uniquify_exp(e.fun, env), new_args, e.typ)
        else:
            raise Exception('uniquify', e)

    init_env = {d.name: d.name for d in p.defs}

    new_defs = [uniquify_def(d, init_env) for d in p.defs]
    new_body = uniquify_exp(p.body, init_env)
    return RfunProgramT(new_defs, new_body)


##################################################
# reveal_functions
##################################################

def reveal_functions(p: RfunProgramT) -> RfunProgramT:
    """
    Transform references to top-level functions from variable references to
    function references.
    :param p: An Rfun program
    :return: An Rfun program in which all references to top-level functions
    are in the form of FunRef objects.
    """

    def reveal_functions_def(defn: RfunDefT, env: Dict[str, FunT]) -> RfunDefT:
        return RfunDefT(defn.name,
                        defn.args,
                        defn.output_type,
                        reveal_functions_exp(defn.body, env))

    def reveal_functions_exp(e: RfunExpT, env: Dict[str, FunT]) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE)):
            return e
        elif isinstance(e, VarTE):
            if e.var in env:
                return FunRefTE(e.var, env[e.var])
            else:
                return e
        elif isinstance(e, LetTE):
            return LetTE(e.x,
                         reveal_functions_exp(e.e1, env),
                         reveal_functions_exp(e.body, env))
        elif isinstance(e, PrimTE):
            new_args = [reveal_functions_exp(arg, env) for arg in e.args]
            return PrimTE(e.op, new_args, e.typ)
        elif isinstance(e, IfTE):
            return IfTE(reveal_functions_exp(e.e1, env),
                        reveal_functions_exp(e.e2, env),
                        reveal_functions_exp(e.e3, env),
                        e.typ)
        elif isinstance(e, FuncallTE):
            new_args = [reveal_functions_exp(arg, env) for arg in e.args]
            return FuncallTE(reveal_functions_exp(e.fun, env), new_args, e.typ)
        else:
            raise Exception('reveal_functions', e)

    init_env = {}
    for d in p.defs:
        arg_names, arg_types = unzip2(d.args)
        t = FunT(list(arg_types), d.output_type)
        init_env[d.name] = t

    new_defs = [reveal_functions_def(d, init_env) for d in p.defs]
    new_body = reveal_functions_exp(p.body, init_env)
    return RfunProgramT(new_defs, new_body)

##################################################
# limit-functions
##################################################


def limit_functions(p: RfunProgramT) -> RfunProgramT:
    """
    Limit functions to have at most 6 arguments.
    :param p: An Rfun program to reveal_functions
    :return: An Rfun program, in which each function has at most 6 arguments
    """

    def limit_functions_def(defn: RfunDefT) -> RfunDefT:
        if len(defn.args) <= 6:
            return RfunDefT(defn.name,
                            defn.args,
                            defn.output_type,
                            limit_functions_exp(defn.body, {}))
        else:
            vec_name = gensym('args_vec')

            first_five_args = defn.args[:5]
            rest_args = defn.args[5:]
            rest_arg_types = [a[1] for a in rest_args]

            vec_type = VectorT(rest_arg_types)

            env = {}
            for idx, arg_pair in enumerate(rest_args):
                arg_name, arg_type = arg_pair
                env[arg_name] = PrimTE('vectorRef',
                                       [VarTE(vec_name, vec_type),
                                        IntTE(idx)],
                                       arg_type)

            new_fifth_arg = (vec_name, vec_type)
            new_args = first_five_args + [new_fifth_arg]

            return RfunDefT(defn.name,
                            new_args,
                            defn.output_type,
                            limit_functions_exp(defn.body, env))



    def limit_functions_exp(e: RfunExpT, env: Dict[str, RfunExpT]) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE, FunRefTE)):
            return e
        elif isinstance(e, VarTE):
            if e.var in env:
                return env[e.var]
            else:
                return e
        elif isinstance(e, LetTE):
            return LetTE(e.x,
                         limit_functions_exp(e.e1, env),
                         limit_functions_exp(e.body, env))
        elif isinstance(e, PrimTE):
            new_args = [limit_functions_exp(arg, env) for arg in e.args]
            return PrimTE(e.op, new_args, e.typ)
        elif isinstance(e, IfTE):
            return IfTE(limit_functions_exp(e.e1, env),
                        limit_functions_exp(e.e2, env),
                        limit_functions_exp(e.e3, env),
                        e.typ)
        elif isinstance(e, FuncallTE):
            new_args = [limit_functions_exp(arg, env) for arg in e.args]

            if len(new_args) > 6:
                first_five_args = new_args[:5]
                rest_args = new_args[5:]

                assert isinstance(e.fun, (VarTE, FunRefTE))

                fun_type = e.fun.typ
                assert isinstance(fun_type, FunT), e

                rest_args_types = fun_type.arg_types[5:]
                vec_type = VectorT(rest_args_types)
                vec_exp = PrimTE('vector', rest_args, vec_type)
                return FuncallTE(limit_functions_exp(e.fun, env),
                                 first_five_args + [vec_exp],
                                 e.typ)
            else:
                return FuncallTE(limit_functions_exp(e.fun, env), new_args, e.typ)
        else:
            raise Exception('limit_functions', e)

    new_defs = [limit_functions_def(d) for d in p.defs]
    new_body = limit_functions_exp(p.body, {})
    return RfunProgramT(new_defs, new_body)


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
    :param p: A typed Rfun program
    :return: A typed Rfun program, without 'vector' forms
    """

    def ea_def(defn: RfunDefT) -> RfunDefT:
        return RfunDefT(defn.name,
                        defn.args,
                        defn.output_type,
                        ea_exp(defn.body))

    def ea_exp(e: RfunExpT) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE, VarTE, FunRefTE)):
            return e
        elif isinstance(e, LetTE):
            new_e1 = ea_exp(e.e1)
            new_body = ea_exp(e.body)
            return LetTE(e.x, new_e1, new_body)
        elif isinstance(e, PrimTE):
            new_args = [ea_exp(arg) for arg in e.args]

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
                total_bytes = 8 + 8*len(new_args)
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
            return IfTE(ea_exp(e.e1),
                        ea_exp(e.e2),
                        ea_exp(e.e3),
                        e.typ)
        elif isinstance(e, FuncallTE):
            new_args = [ea_exp(arg) for arg in e.args]
            return FuncallTE(ea_exp(e.fun), new_args, e.typ)
        else:
            raise Exception('ea_exp', e)

    new_defs = [ea_def(d) for d in p.defs]
    new_body = ea_exp(p.body)
    return RfunProgramT(new_defs, new_body)


##################################################
# remove-complex-opera*
##################################################

def rco(p: RfunProgramT) -> RfunProgramT:
    """
    Removes complex operands. After this pass, the program will be in A-Normal
    Form (the arguments to Prim operations will be atomic).
    :param p: An Rfun program
    :return: An Rfun program in A-Normal Form
    """

    def rco_def(defn: RfunDefT) -> RfunDefT:
        return RfunDefT(defn.name,
                        defn.args,
                        defn.output_type,
                        rco_exp(defn.body))

    def rco_atm(e: RfunExpT, bindings: Dict[str, RfunExpT]) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE, VarTE)):
            return e
        elif isinstance(e, FunRefTE):
            new_v = gensym('tmp')
            bindings[new_v] = e
            return VarTE(new_v, e.typ)
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
            new_args = [rco_atm(arg, bindings) for arg in e.args]
            new_fun = rco_atm(e.fun, bindings)

            new_v = gensym('tmp')
            bindings[new_v] = FuncallTE(new_fun, new_args, e.typ)
            return VarTE(new_v, e.typ)
        else:
            raise Exception('rco_atm', e)

    def rco_exp(e: RfunExpT) -> RfunExpT:
        if isinstance(e, (IntTE, BoolTE, VoidTE, VarTE, GlobalValTE, FunRefTE)):
            return e
        elif isinstance(e, LetTE):
            new_e1 = rco_exp(e.e1)
            new_body = rco_exp(e.body)
            return LetTE(e.x, new_e1, new_body)
        elif isinstance(e, PrimTE):
            bindings: Dict[str, RfunExpT] = {}
            new_args = [rco_atm(arg, bindings) for arg in e.args]

            return mk_let(bindings, PrimTE(e.op, new_args, e.typ))
        elif isinstance(e, FuncallTE):
            bindings: Dict[str, RfunExpT] = {}
            new_fun = rco_atm(e.fun, bindings)
            new_args = [rco_atm(arg, bindings) for arg in e.args]

            return mk_let(bindings, FuncallTE(new_fun, new_args, e.typ))
        elif isinstance(e, IfTE):
            return IfTE(rco_exp(e.e1),
                        rco_exp(e.e2),
                        rco_exp(e.e3),
                        e.typ)
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
    :param p: An Rfun Program
    :return: A Cfun Program
    """

    defs = []
    for defn in p.defs:
        cfg = explicate_control_help(defn.body)
        defs.append(cfun.Def(defn.name,
                             defn.args,
                             defn.output_type,
                             cfg))

    cfg_main = explicate_control_help(p.body)
    def_main = cfun.Def('main',
                        [],
                        IntT(),
                        cfg_main)

    return cfun.Program(defs + [def_main])


def explicate_control_help(e: RfunExpT) -> Dict[str, cfun.Tail]:
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
            return cfun.FunRef(e.name)
        elif isinstance(e, FuncallTE):
            return cfun.Call(ec_atm(e.fun),
                             [ec_atm(a) for a in e.args],
                             e.typ)
        else:
            return cfun.AtmExp(ec_atm(e))

    def ec_assign(x: str, e: RfunExpT, k: cfun.Tail) -> cfun.Tail:
        if isinstance(e, (IntTE, BoolTE, VoidTE, GlobalValTE, FunRefTE)):
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
            return cfun.Seq(cfun.Assign(x, ec_exp(e), isinstance(e.typ, VectorT)), k)
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
        if isinstance(e, (IntTE, BoolTE, VarTE, PrimTE, FunRefTE)):
            return cfun.Return(ec_exp(e))
        elif isinstance(e, LetTE):
            return ec_assign(e.x, e.e1, ec_tail(e.body))
        elif isinstance(e, IfTE):
            b1 = ec_tail(e.e2)
            b2 = ec_tail(e.e3)
            return ec_pred(e.e1, b1, b2)
        elif isinstance(e, FuncallTE):
            f = ec_atm(e.fun)
            args = [ec_atm(a) for a in e.args]
            return cfun.TailCall(f, args, e.typ)
        else:
            raise Exception('ec_tail', e)

    cfg['start'] = ec_tail(e)
    return cfg


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

    def mk_var(x: str, is_vec: bool) -> x86.Arg:
        if is_vec:
            return x86.VecVar(x)
        else:
            return x86.Var(x)

    def si_atm(a: cfun.Atm) -> x86.Arg:
        if isinstance(a, cfun.Int):
            return x86.Int(a.val)
        if isinstance(a, cfun.Bool):
            if a.val:
                return x86.Int(1)
            elif not a.val:
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
            elif isinstance(e.exp, cfun.FunRef):
                f = x86.FunRef(e.exp.label)
                return [x86.Leaq(f, mk_var(e.var, e.is_vec))]
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
                elif e.exp.op == 'neg':
                    arg = si_atm(e.exp.args[0])

                    return [x86.Movq(arg, mk_var(e.var, e.is_vec)),
                            x86.Negq(mk_var(e.var, e.is_vec))]
                elif e.exp.op == 'allocate':
                    vec_type = e.exp.typ
                    assert isinstance(vec_type, VectorT)

                    tag = mk_tag(vec_type.types)
                    total_bytes = 8 + 8*len(vec_type.types)

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

            elif isinstance(e.exp, cfun.Call):
                param_instrs: List[x86.Instr] = \
                    [x86.Movq(si_atm(arg), x86.Reg(reg)) for arg, reg in
                     zip(e.exp.args, constants.parameter_passing_registers)]

                callq_instrs = [x86.IndirectCallq(si_atm(e.exp.fun), len(e.exp.args))]

                assign_instrs = [x86.Movq(x86.Reg('rax'), mk_var(e.var, e.is_vec))]

                return param_instrs + callq_instrs + assign_instrs

            raise Exception('si_stmt Assign', e)
        else:
            raise Exception('si_stmt', e)

    def si_tail(def_name: str, e: cfun.Tail) -> List[x86.Instr]:
        if isinstance(e, cfun.Return):
            new_var = gensym('retvar')
            instrs = si_stmt(cfun.Assign(new_var, e.exp, False))

            return instrs + \
                   [x86.Movq(mk_var(new_var, False), x86.Reg('rax')),
                    x86.Jmp(def_name + '_conclusion')]
        elif isinstance(e, cfun.Seq):
            return si_stmt(e.stmt) + si_tail(def_name, e.tail)
        elif isinstance(e, cfun.If):
            assert isinstance(e.test, cfun.Prim)
            e1, e2 = e.test.args
            return [ x86.Cmpq(si_atm(e2), si_atm(e1)),
                     x86.JmpIf(e.test.op, e.then_label),
                     x86.Jmp(e.else_label) ]
        elif isinstance(e, cfun.Goto):
            return [x86.Jmp(e.label)]
        elif isinstance(e, cfun.TailCall):
            param_instrs: List[x86.Instr] = \
                [x86.Movq(si_atm(arg), x86.Reg(reg)) for arg, reg in
                 zip(e.args, constants.parameter_passing_registers)]

            jmp_instrs = [x86.TailJmp(si_atm(e.fun), len(e.args))]

            return param_instrs + jmp_instrs
        else:
            raise Exception('si_tail', e)

    def si_def(defn: cfun.Def) -> Tuple[str, x86.Program]:
        x86_blocks = {}
        for label, block in defn.blocks.items():
            if label == 'start':
                args = [mk_var(name, isinstance(typ, VectorT)) for name, typ in defn.args]
                param_instrs: List[x86.Instr] = \
                    [x86.Movq(x86.Reg(reg), arg) for arg, reg in
                     zip(args, constants.parameter_passing_registers)]

                x86_blocks[defn.name + '_start'] = param_instrs + si_tail(defn.name, block)
            else:
                x86_blocks[label] = si_tail(defn.name, block)

        return defn.name, x86.Program(x86_blocks)

    x86_defs = dict([si_def(d) for d in p.defs])
    return x86_defs



##################################################
# uncover-live
##################################################

def uncover_live(program: Dict[str, x86.Program]) -> \
        Tuple[Dict[str, x86.Program],
              Dict[str, List[Set[x86.Var]]]]:
    """
    Performs liveness analysis. Returns the input program, plus live-after sets
    for its blocks.
    :param program: pseudo-x86 assembly program definitions
    :return: A tuple. The first element is the same as the input program. The
    second element is a dict of live-after sets. This dict maps each label in
    the program to a list of live-after sets for that label. The live-after
    sets are in the same order as the label's instructions.
    """

    label_live: Dict[str, Set[x86.Var]] = \
        {name + '_conclusion': set() for name in program.keys()}

    live_after_sets: Dict[str, List[Set[x86.Var]]] = {}

    # initialize a global dict of all the blocks
    blocks = {}
    for name, p in program.items():
        for label, block in p.blocks.items():
            blocks[label] = block

    def vars_arg(a: x86.Arg) -> Set[x86.Var]:
        if isinstance(a, (x86.Int, x86.Reg, x86.ByteReg, x86.Deref, x86.GlobalVal, x86.FunRef)):
            return set()
        elif isinstance(a, (x86.Var, x86.VecVar)):
            return {a}
        else:
            raise Exception('ul vars_arg', a)

    def ul_instr(e: x86.Instr, live_after: Set[x86.Var]) -> Set[x86.Var]:
        if isinstance(e, (x86.Movq, x86.Movzbq, x86.Leaq)):
            return live_after.difference(vars_arg(e.e2)).union(vars_arg(e.e1))
        elif isinstance(e, (x86.Addq, x86.Xorq)):
            return live_after.union(vars_arg(e.e1).union(vars_arg(e.e2)))
        elif isinstance(e, x86.Negq):
            return live_after.union(vars_arg(e.e1))
        elif isinstance(e, (x86.Callq, x86.Retq, x86.Set)):
            return live_after
        elif isinstance(e, x86.Cmpq):
            return live_after.union(vars_arg(e.e1).union(vars_arg(e.e2)))
        elif isinstance(e, (x86.Jmp, x86.JmpIf)):
            if e.label not in label_live:
                ul_block(e.label)

            return live_after.union(label_live[e.label])
        elif isinstance(e, (x86.TailJmp, x86.IndirectCallq)):
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

    # run the liveness analysis for each definition
    for name in program.keys():
        ul_block(name + '_start')

    return program, live_after_sets


##################################################
# select-allocation
##################################################

def select_allocation(inputs: Tuple[Dict[str, x86.Program], Dict[str, List[Set[x86.Var]]]]) -> \
        Tuple[Dict[str, x86.Program], Dict[str, List[Set[x86.Var]]], str]:
    """
    Performs machine learning analysis on what allocation type the compiler should use.
    Returns the input program plus the recommended allocation method.
    :param inputs: A tuple. The first element is the input program. The
        second element is a dict of live-after sets. This dict maps each label in
        the program to a list of live-after sets for that label. The live-after
        sets are in the same order as the label's instructions.
    :return: A tuple. The first element is the same as the input program.
        The second element is a string stating the recommended register allocation method.
    """
    if len(sys.argv) > 2:
        allocation_type = str(sys.argv[2])
    else:
        # Default to graph coloring
        # allocation_type = "graph_color"
        allocation_type = "linear_scan"

    return inputs[0], inputs[1], allocation_type


##################################################
# allocate-registers
##################################################
def allocate_registers(inputs: Tuple[Dict[str, x86.Program], Dict[str, List[Set[x86.Var]]], str]) -> \
        Dict[str, Tuple[x86.Program, int, int]]:
    """
    Assigns homes to variables in the input program. Allocates registers and
    stack locations as needed, uses one of the possible allocation methods as given
    by the third argument in the input.
    :param inputs: A Tuple. The first element is the pseudo-x86 program. The second
        element is a list of live-after sets. The third element is the allocation
        type for the program.
    :return: A dict mapping each function name to a Tuple. The first element
    of each tuple is an x86 program (with no variable references). The second
    element is the number of bytes needed in regular stack locations. The third
    element is the number of variables spilled to the root (shadow) stack.
    """

    p, live_after_sets, allocation_type = inputs
    # allocation_type = 'graph_color'
    if allocation_type == 'graph_color':
        return allocate_registers_graph_coloring(build_interference((p, live_after_sets)))
    elif allocation_type == 'linear_scan':
        p, defn_live_intervals = build_live_intervals(p)
        return allocate_registers_linear_scan(p, defn_live_intervals)
    else:
        raise Exception('allocate_registers')


##################################################
# allocate-registers
##################################################

Color = int
Coloring = Dict[x86.Var, Color]

''' =============== allocate-registers: Linear Scan =============== '''

class LiveInterval:
    """
    Helper class to represent live intervals
    """
    var: x86.Var
    startpoint: int
    endpoint: int
    location: x86.Arg

    def __init__(self, var: x86.Var, startpoint: int, endpoint: int, location: x86.Arg = None):
        assert isinstance(location, (x86.Reg, x86.Deref, type(None)))

        self.var = var
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.location = location

    def __str__(self):
        return f'`{self.var}`: ({self.startpoint}-{self.endpoint}), location={self.location}'

    def __repr__(self):
        return str(self)


def build_live_intervals(p: Dict[str, x86.Program]) -> Tuple[Dict[str, x86.Program], Dict[str, List[LiveInterval]]]:
    """
    Map block names to a list of live intervals for the variables in that block.
    :param p: A pseudo-x86 program
    :return: A tuple. The first element is the original program as a dict mapping block names
    to their program bodies. The second element is a dict mapping function/block names to a
    list of LiveIntervals whose names are the names of the variables in that function/block
    """

    def build_live_intervals_def(p: x86.Program) -> List[LiveInterval]:
        live_sets: List[Set[x86.Var]] = build_live_sets_def(p)
        live_intervals: List[LiveInterval] = []

        for line_num, live_set in enumerate(live_sets):
            if live_set is None:
                continue

            # For all vars in the live_set, update their endpoint in live_intervals
            # If they are not yet in live_intervals, add a new LiveIntervals for that var
            for var in live_set:
                for live_interval in live_intervals:
                    if live_interval.var == var:
                        live_interval.endpoint = line_num
                        break  # If this break is not reached, else \/ will execute
                else:
                    # This var is not yet in the live_set
                    # Make new LiveInterval with startpoint and endpoint as current line_num
                    live_intervals.append(LiveInterval(var, line_num, line_num))

        return live_intervals

    def build_live_sets_def(p: x86.Program) -> List[Set[x86.Var]]:
        assert len(p.blocks) == 1

        block: Tuple[str, List[x86.Instr]] = [(name, instrs) for name, instrs in p.blocks.items()][0]
        instrs: List[x86.Instr] = block[1]

        live_sets = []
        for instr in instrs:
            live_sets.append(build_live_sets_instr(instr))

        return live_sets

    def build_live_sets_instr(instr: x86.Instr) -> Set[x86.Var]:
        # TODO These types may need changing (?)
        if isinstance(instr, (x86.Movq, x86.Addq, x86.Cmpq, x86.Movzbq, x86.Xorq, x86.Leaq)):
            return build_live_sets_arg(instr.e1).union(build_live_sets_arg(instr.e2))
        elif isinstance(instr, (x86.Set, x86.Negq, x86.TailJmp, x86.IndirectCallq)):
            return build_live_sets_arg(instr.e1)

    def build_live_sets_arg(a: x86.Arg) -> Set[x86.Var]:
        if isinstance(a, (x86.Int, x86.Reg, x86.ByteReg, x86.GlobalVal, x86.Deref, x86.FunRef)):
            return set()
        elif isinstance(a, x86.Var):
            return {a}
        else:
            raise ValueError('live_sets_arg linear_scan_help', a)

    return p, {name: build_live_intervals_def(prog) for name, prog in p.items()}

def allocate_registers_linear_scan(defs: Dict[str, x86.Program], defs_live_intervals: Dict[str, List[LiveInterval]]) -> \
        Dict[str, Tuple[x86.Program, int, int]]:
    """
    Assigns homes to variables in the input program. Allocates registers and
    stack locations as needed, based on a linear scan register allocation
    algorithm.
    :param defs: A pseudo-x86 program.
    :param defs_live_intervals: A dict mapping function names to lists of LiveIntervals for
    the function's variables.

    :return: A dict mapping each function name to a Tuple. The first element
    of each tuple is an x86 program (with no variable references). The second
    element is the number of bytes needed in regular stack locations. The third
    element is the number of variables spilled to the root (shadow) stack.
    """

    def allocate_registers_ls_help(p: x86.Program, live_intervals: List[LiveInterval]) \
            -> Tuple[x86.Program, int, int]:

        ''' ============== Functions for listing the variables in the program ============== '''

        def vars_arg(a: x86.Arg) -> Set[x86.Var]:
            if isinstance(a, (x86.Int, x86.Reg, x86.ByteReg, x86.GlobalVal, x86.Deref,
                              x86.FunRef)):
                return set()
            elif isinstance(a, x86.Var):
                return {a}
            else:
                raise Exception('vars_arg allocate_registers', a)

        def vars_instr(e: x86.Instr) -> Set[x86.Var]:
            if isinstance(e, (x86.Movq, x86.Addq, x86.Cmpq, x86.Movzbq, x86.Xorq, x86.Leaq)):
                return vars_arg(e.e1).union(vars_arg(e.e2))
            elif isinstance(e, (x86.Set, x86.Negq, x86.TailJmp, x86.IndirectCallq)):
                return vars_arg(e.e1)
            elif isinstance(e, (x86.Callq, x86.Retq, x86.Jmp, x86.JmpIf)):
                return set()
            else:
                raise Exception('vars_instr allocate_registers', e)

        ''' ============== Functions for linear scan ============== '''

        # Defines the set of registers to use
        available_register_locations = [x86.Reg(r) for r in
                              constants.caller_saved_registers + constants.callee_saved_registers]
        num_available = len(available_register_locations)

        # `active` is the list, sorted in order of increasing end point,
        # of live intervals overlapping the current point and placed in registers
        active: List[LiveInterval] = []
        def linear_scan_color_regs(live_intervals: List[LiveInterval]) \
                -> Dict[str, x86.Arg]:
            # Init the live intervals
            # Loop through intervals by increasing startpoint
            live_intervals.sort(key=lambda int_: int_.startpoint)
            for interval in live_intervals:
                expire_old_intervals(interval)
                if len(active) == num_available:
                    spill_at_interval(interval)
                else:
                    # Take a register from the pool of free registers
                    interval.location = available_register_locations.pop(-1)
                    active.append(interval)

                    # TODO if there's time: Make active a queue.PriorityQueue
                    active.sort(key=lambda int_: int_.endpoint)

            ic(live_intervals)

            homes: Dict[str, x86.Arg] = {i.var.var: i.location for i in live_intervals}

            return homes

        def expire_old_intervals(i: LiveInterval) -> None:
            # Sort active by increasing end point
            active.sort(key=lambda interval: interval.endpoint)
            for j in active:
                if j.endpoint >= i.endpoint:
                    return
                active.remove(j)
                if isinstance(j.location, x86.Reg):
                    available_register_locations.append(j.location)

        stack_spills = 0
        root_stack_spills = 0
        def spill_at_interval(i: LiveInterval) -> None:
            nonlocal stack_spills
            nonlocal root_stack_spills

            # Sort active by increasing end point
            active.sort(key=lambda interval: interval.endpoint)
            spill = active[-1]

            if spill.endpoint > i.endpoint:
                i.location = spill.location
                if isinstance(i.var, x86.VecVar):
                    root_stack_spills += 1
                    offset = root_stack_spills
                    spill.location = x86.Deref(-(offset * 8), 'r15')

                elif isinstance(i.var, x86.Var):
                    stack_spills += 1
                    offset = stack_spills + 1
                    spill.location = x86.Deref(-(offset * 8), 'rbp')
                active.remove(spill)
                active.append(i)
            else:
                if isinstance(i.location, x86.VecVar):
                    offset = root_stack_spills
                    i.location = x86.Deref(-(offset * 8), 'r15')
                elif isinstance(i.location, x86.Var):
                    offset = stack_spills + 1
                    i.location = x86.Deref(-(offset * 8), 'rbp')


        ''' ============== Functions for allocating registers ============== '''

        def make_stack_loc(offset: int) -> x86.Deref:
            # TODO this might be a problem
            return x86.Deref(-(offset * 8), 'rbp')

        ''' ============== Functions for replacing variables with their homes ============== '''
        homes: Dict[str, x86.Arg] = {}

        def ah_arg(a: x86.Arg) -> x86.Arg:
            # ic(a)
            if isinstance(a, (x86.Int, x86.Reg, x86.ByteReg, x86.Deref,
                              x86.GlobalVal, x86.FunRef)):
                return a
            elif isinstance(a, x86.Var):
                # ic(homes)
                return homes[a.var]
            else:
                raise Exception('ah_arg', a)

        def ah_instr(e: x86.Instr) -> x86.Instr:
            if isinstance(e, x86.Movq):
                return x86.Movq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Addq):
                return x86.Addq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Cmpq):
                return x86.Cmpq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Movzbq):
                return x86.Movzbq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Xorq):
                return x86.Xorq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Negq):
                return x86.Negq(ah_arg(e.e1))
            elif isinstance(e, x86.Leaq):
                return x86.Leaq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Set):
                return x86.Set(e.cc, ah_arg(e.e1))
            elif isinstance(e, x86.TailJmp):
                return x86.TailJmp(ah_arg(e.e1), e.num_args)
            elif isinstance(e, x86.IndirectCallq):
                return x86.IndirectCallq(ah_arg(e.e1), e.num_args)
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

        ''' ============== Main body (help function) ============== '''

        blocks = p.blocks

        # Build "homes"
        homes: Dict[str, x86.Arg] = linear_scan_color_regs(live_intervals)
        ic(homes)
        vec_color_map = dict(enumerate(available_register_locations))


        new_blocks = {label: ah_block(block) for label, block in blocks.items()}
        return x86.Program(new_blocks), align(8 * stack_spills), root_stack_spills

    ''' ============== Main body ============== '''

    results = {}

    for label, prog in defs.items():
        results[label] = allocate_registers_ls_help(prog, defs_live_intervals[label])

    return results


''' =============== allocate-registers: Graph Coloring =============== '''

Saturation = Set[Color]

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

def build_interference(inputs: Tuple[Dict[str, x86.Program], Dict[str, List[Set[x86.Var]]]]) -> \
        Tuple[Dict[str, x86.Program], Dict[str, InterferenceGraph]]:
    """
    Build the interference graph.
    :param inputs: A Tuple. The first element is a pseudo-x86 program. The
    second element is the dict of live-after sets produced by the uncover-live
    pass.
    :return: A Tuple. The first element is the same as the input program.
    The second is a dict mapping each function name to its completed
    interference graph.
    """
    defs, live_after_sets = inputs

    caller_saved_registers = [x86.Reg(r) for r in constants.caller_saved_registers]
    callee_saved_registers = [x86.Reg(r) for r in constants.callee_saved_registers]

    def vars_arg(a: x86.Arg) -> Set[x86.Var]:
        if isinstance(a, (x86.Int, x86.Deref, x86.GlobalVal)):
            return set()
        elif isinstance(a, (x86.Var, x86.VecVar, x86.Reg)):
            return {a}
        else:
            raise Exception('bi_arg', a)

    def writes_of(e: x86.Instr) -> Set[x86.Var]:
        if isinstance(e, (x86.Movq, x86.Addq, x86.Movzbq, x86.Xorq, x86.Leaq)):
            return vars_arg(e.e2)
        elif isinstance(e, x86.Negq):
            return vars_arg(e.e1)
        elif isinstance(e, (x86.Callq, x86.Retq, x86.Jmp)):
            return set()
        else:
            raise Exception('writes_of', e)

    def bi_instr(e: x86.Instr, live_after: Set[x86.Var], graph: InterferenceGraph):
        if isinstance(e, (x86.Movq, x86.Addq, x86.Movzbq, x86.Xorq, x86.Negq, x86.Leaq)):
            for v1 in writes_of(e):
                for v2 in live_after:
                    graph.add_edge(v1, v2)
        elif isinstance(e, (x86.Callq, x86.TailJmp, x86.IndirectCallq)):
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

    def bi_def(p: x86.Program) -> InterferenceGraph:
        blocks = p.blocks

        interference_graph = InterferenceGraph()

        for label, instrs in blocks.items():
            bi_block(instrs, live_after_sets[label], interference_graph)

        return interference_graph

    interference_graphs = {name: bi_def(p) for name, p in defs.items()}

    return defs, interference_graphs

def allocate_registers_graph_coloring(inputs: Tuple[Dict[str, x86.Program],
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

    def allocate_registers_gc_help(inputs: Tuple[x86.Program, InterferenceGraph]) \
            -> Tuple[x86.Program, int, int]:

        ''' ============== Functions for listing the variables in the program ============== '''

        def vars_arg(a: x86.Arg) -> Set[x86.Var]:
            if isinstance(a, (x86.Int, x86.Reg, x86.ByteReg, x86.GlobalVal, x86.Deref,
                              x86.FunRef)):
                return set()
            elif isinstance(a, x86.Var):
                return {a}
            else:
                raise Exception('vars_arg allocate_registers', a)

        def vars_instr(e: x86.Instr) -> Set[x86.Var]:
            if isinstance(e, (x86.Movq, x86.Addq, x86.Cmpq, x86.Movzbq, x86.Xorq, x86.Leaq)):
                return vars_arg(e.e1).union(vars_arg(e.e2))
            elif isinstance(e, (x86.Set, x86.Negq, x86.TailJmp, x86.IndirectCallq)):
                return vars_arg(e.e1)
            elif isinstance(e, (x86.Callq, x86.Retq, x86.Jmp, x86.JmpIf)):
                return set()
            else:
                raise Exception('vars_instr allocate_registers', e)

        ''' ============== Functions for graph coloring ============== '''

        # Defines the set of registers to use
        register_locations = [x86.Reg(r) for r in
                              constants.caller_saved_registers + constants.callee_saved_registers]

        def color_graph(local_vars: Set[x86.Var], interference_graph: InterferenceGraph) \
                -> Coloring:
            coloring = {}

            to_color = local_vars.copy()
            saturation_sets = {x: set() for x in local_vars}

            # Init the saturation sets
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

            # temp_lst = list(coloring.items())
            # temp_lst.sort(key=lambda i: i[0].var)
            # temp = {var.var: color for var, color in temp_lst}
            # ic(temp)
            # ic(saturation_sets)

            return coloring

        ''' ============== Functions for allocating registers ============== '''
        def make_stack_loc(offset):
            return x86.Deref(-(offset * 8), 'rbp')

        ''' ============== Functions for replacing variables with their homes ============== '''
        homes: Dict[x86.Var, x86.Arg] = {}

        def ah_arg(a: x86.Arg) -> x86.Arg:
            if isinstance(a, (x86.Int, x86.Reg, x86.ByteReg, x86.Deref,
                              x86.GlobalVal, x86.FunRef)):
                return a
            elif isinstance(a, x86.Var):
                return homes[a]
            else:
                raise Exception('ah_arg', a)

        def ah_instr(e: x86.Instr) -> x86.Instr:
            if isinstance(e, x86.Movq):
                return x86.Movq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Addq):
                return x86.Addq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Cmpq):
                return x86.Cmpq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Movzbq):
                return x86.Movzbq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Xorq):
                return x86.Xorq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Negq):
                return x86.Negq(ah_arg(e.e1))
            elif isinstance(e, x86.Leaq):
                return x86.Leaq(ah_arg(e.e1), ah_arg(e.e2))
            elif isinstance(e, x86.Set):
                return x86.Set(e.cc, ah_arg(e.e1))
            elif isinstance(e, x86.TailJmp):
                return x86.TailJmp(ah_arg(e.e1), e.num_args)
            elif isinstance(e, x86.IndirectCallq):
                return x86.IndirectCallq(ah_arg(e.e1), e.num_args)
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

        ''' ============== Main body (help function) ============== '''
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

        # Fill in locations in the color map
        for v in local_vars:
            if isinstance(v, x86.VecVar):
                color = coloring[v]
                if color not in vec_color_map:
                    root_stack_spills += 1
                    offset = root_stack_spills
                    vec_color_map[color] = x86.Deref(-(offset * 8), 'r15')
            elif isinstance(v, x86.Var):
                color = coloring[v]
                if color not in color_map:
                    stack_spills += 1
                    offset = stack_spills + 1
                    color_map[color] = x86.Deref(-(offset * 8), 'rbp')

        # Build "homes"
        for v in local_vars:
            color = coloring[v]
            if isinstance(v, x86.VecVar):
                homes[v] = vec_color_map[color]
            elif isinstance(v, x86.Var):
                homes[v] = color_map[color]

        blocks = program.blocks
        new_blocks = {label: ah_block(block) for label, block in blocks.items()}
        return x86.Program(new_blocks), align(8 * stack_spills), root_stack_spills

    ''' ============== Main body ============== '''
    defs, interference_graphs = inputs
    results = {}

    for label, prog in defs.items():
        helper_inputs = (prog, interference_graphs[label])
        results[label] = allocate_registers_gc_help(helper_inputs)

    return results


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

    results = {name: patch_instructions_help(vals) for name, vals in inputs.items()}
    return results

def patch_instructions_help(inputs: Tuple[x86.Program, int, int]) -> Tuple[x86.Program, int, int]:

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
        elif isinstance(e, x86.Leaq) and \
                isinstance(e.e2, x86.Deref):
            return [x86.Leaq(e.e1, x86.Reg('rax')),
                    x86.Movq(x86.Reg('rax'), e.e2)]
        elif isinstance(e, x86.Cmpq) and \
                isinstance(e.e2, x86.Int):
            return [x86.Movq(e.e2, x86.Reg('rax')),
                    x86.Cmpq(e.e1, x86.Reg('rax'))]
        elif isinstance(e, x86.TailJmp):
            return [x86.Movq(e.e1, x86.Reg('rax')),
                    x86.TailJmp(x86.Reg('rax'), e.num_args)]
        elif isinstance(e, x86.IndirectCallq):
            return [x86.Movq(e.e1, x86.Reg('rax')),
                    x86.IndirectCallq(x86.Reg('rax'), e.num_args)]
        elif isinstance(e, (x86.Callq, x86.Retq, x86.Jmp, x86.JmpIf,
                            x86.Movq, x86.Addq, x86.Cmpq, x86.Set,
                            x86.Movzbq, x86.Xorq, x86.Negq, x86.Leaq)):
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
    return x86.Program(new_blocks), stack_size, root_stack_spills


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

    final_program = ""
    for name, vals in inputs.items():
        final_program = final_program + print_x86_help(name, vals)

    return final_program

def print_x86_help(name: str, inputs: Tuple[x86.Program, int, int]) -> str:
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
        elif isinstance(e, x86.Negq):
            return f'negq {print_arg(e.e1)}'
        elif isinstance(e, x86.Leaq):
            return f'leaq {print_arg(e.e1)}, {print_arg(e.e2)}'
        elif isinstance(e, x86.Callq):
            return f'callq {e.label}'
        elif isinstance(e, x86.Retq):
            return f'retq'
        elif isinstance(e, x86.Jmp):
            return f'jmp {e.label}'
        elif isinstance(e, x86.JmpIf):
            cc = ccs[e.cc]
            return f'j{cc} {e.label}'
        elif isinstance(e, x86.Set):
            return f'set{e.cc} {print_arg(e.e1)}'
        elif isinstance(e, x86.TailJmp):
            if name == 'main':
                return f'callq *{print_arg(e.e1)}\n  jmp main_conclusion'
            else:
                program, stack_size, root_stack_spills = inputs
                callee_saved_restore = \
                    '\n'.join([f'  popq %{r}'
                               for r in reversed(constants.callee_saved_registers)])

                code = f"""
  addq ${stack_size}, %rsp
  subq ${8 * root_stack_spills}, %r15
{callee_saved_restore}
  popq %rbp
  jmp *{print_arg(e.e1)}
"""
                return code
        elif isinstance(e, x86.IndirectCallq):
            return f'callq *{print_arg(e.e1)}'

        else:
            raise Exception('print_instr', e)

    def print_block(label: str, instrs: List[x86.Instr]) -> str:
        name = f'{label}:\n'
        instr_strs = '\n'.join(['  ' + print_instr(i) for i in instrs])
        return name + instr_strs

    program, stack_size, root_stack_spills = inputs
    blocks = program.blocks
    block_instrs = '\n'.join([print_block(label, block) for label, block in blocks.items()])

    root_stack_inits = ""
    for i in range(root_stack_spills):
        root_stack_inits = root_stack_inits + "  movq $0, (%r15)\n  addq $8, %r15\n"

    root_stack_init_code = ""
    print_code = ""

    if name == 'main':
        root_stack_init_code = f"""
  movq ${constants.root_stack_size}, %rdi
  movq ${constants.heap_size}, %rsi
  callq initialize
  movq rootstack_begin(%rip), %r15"""

        print_code = f"""
  movq %rax, %rdi
  callq print_int
  movq $0, %rax
"""

    callee_saved_save    = '\n'.join([f'  pushq %{r}' for r in constants.callee_saved_registers])
    callee_saved_restore = '\n'.join([f'  popq %{r}'
                                      for r in reversed(constants.callee_saved_registers)])

    final_program = f"""
  .globl {name}
{name}:
  pushq %rbp
  movq %rsp, %rbp
  subq ${stack_size}, %rsp
{callee_saved_save}
{root_stack_init_code}
{root_stack_inits}
  jmp {name}_start
{block_instrs}
{name}_conclusion:
{print_code}
  addq ${stack_size}, %rsp
  subq ${8 * root_stack_spills}, %r15
{callee_saved_restore}
  popq %rbp
  retq
"""

    return final_program


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
    'select allocation': select_allocation,
    'allocate registers': allocate_registers,
    # 'build interference': build_interference,
    # 'allocate registers': allocate_registers_gc,
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

    if logging:
        print()
        print('==================================================')
        print(' Input program')
        print('==================================================')
        print()
        print(print_ast(current_program))

    for pass_name, pass_fn in compiler_passes.items():
        current_program = pass_fn(current_program)

        if logging:
            print()
            print('==================================================')
            print(f' Output of pass: {pass_name}')
            print('==================================================')
            print()
            print(print_ast(current_program))

    assert isinstance(current_program, str)
    return current_program


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python compiler.py <source filename>')
    else:
        file_name = sys.argv[1]
        with open(file_name) as f:
            print(f'Compiling program {file_name}...')

            program = f.read()
            x86_program = run_compiler(program, logging=True)

            with open(file_name + '.s', 'w') as output_file:
                output_file.write(x86_program)
