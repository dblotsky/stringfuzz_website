#!/usr/bin/env python3
import os
import sys
import glob
import subprocess
import signal
import datetime
import signal
import time

from collections import namedtuple
from operator import attrgetter

# arguments
TIMEOUT     = 30.0
PROBLEMS    = "../problems/**/*.smt25"
RESULTS_DIR = "../results"

# data
CSV_HEADER  = "Category,Instance,Result,Time\n"
Result = namedtuple('Result', ('category', 'problem', 'elapsed', 'result'))

# constants
SAT_RESULT = 'sat'
UNSAT_RESULT = 'unsat'
UNKNOWN_RESULT = 'unknown'
TIMEOUT_RESULT = 'timeout (%.1f s)' % TIMEOUT
ERROR_RESULT = 'error'

SOLVERS = {
    "Z3seq"  : "z3",
    "Z3str3" : "z3 smt.string_solver=z3str3",
    "CVC4"   : "cvc4 --lang smt --strings-exp --produce-models",
    "Norn"   : "norn +model",
    # "Sloth" : "sloth",
    # "S3"    : "S3"
}
DATA = {}
for solver in SOLVERS.keys():
    DATA[solver] = []


def output2result(problem, output):
    # it's important to check for unsat first, since sat
    # is a substring of unsat
    if 'UNSAT' in output or 'unsat' in output:
        return UNSAT_RESULT
    if 'SAT' in output or 'sat' in output:
        return SAT_RESULT
    if 'UNKNOWN' in output or 'unknown' in output:
        return UNKNOWN_RESULT

    # print(problem, ': Couldn\'t parse output', file=sys.stderr)
    return ERROR_RESULT

def run_problem(solver, invocation, problem):
    # pass the problem to the command
    command = "%s %s" %(invocation, problem)
    # get start time
    start = datetime.datetime.now().timestamp()
    # run command
    process = subprocess.Popen(
        command,
        shell      = True,
        stdout     = subprocess.PIPE,
        stderr     = subprocess.PIPE,
        preexec_fn = os.setsid
    )
    # wait for it to complete
    try:
        process.wait(timeout=TIMEOUT)
    # if it times out ...
    except subprocess.TimeoutExpired:
        # kill it
        print('TIMED OUT:', repr(command), '... killing', process.pid, file=sys.stderr)
        os.killpg(os.getpgid(process.pid), signal.SIGINT)
        # set timeout result
        elapsed = TIMEOUT
        result  = TIMEOUT_RESULT
    # if it completes in time ...
    else:
        # measure run time
        end     = datetime.datetime.now().timestamp()
        elapsed = end - start
        # get result
        stdout = process.stdout.read().decode("utf-8", "ignore")
        stderr = process.stderr.read().decode("utf-8", "ignore")
        result = output2result(problem, stdout + stderr)
    # make result
    result = Result(
        category = os.path.dirname(problem),
        problem  = os.path.basename(problem),
        result   = result,
        elapsed  = elapsed
    )
    return result

def signal_handler(signal, frame):
    print("KILLING!")
    sys.exit(0)

def main():
    global DATA
    signal.signal(signal.SIGTERM, signal_handler)
    problems = glob.glob(PROBLEMS)
    for solver, command in SOLVERS.items():
        for problem in problems:
            result = run_problem(solver, command, problem)
            DATA[solver].append(result)

    for solver, data in DATA.items():
        filename = "%s/%s.csv" %(RESULTS_DIR, solver)
        with open(filename, 'w') as fp:
            fp.write(CSV_HEADER)
            for point in data:
                # Same order as CSV_HEADER
                fp.write("%s,%s,%s,%s\n"%(point.category, point.problem, point.result, point.elapsed))

if __name__ == '__main__':
    main()
