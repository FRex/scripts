import subprocess
import sys
import os

#TODO: make it into a class?
#TODO: make it more robust
#TODO: use output to file or get rid of windows line endings in stdout

def try_run_cmd(args, cd, exe):
    if not all(os.path.exists(os.path.join(cd, x)) for x in args[1:]):
        return None
    #TODO: return None if cd/args dont exist
    args = list(args)
    args[0] = exe
    r = subprocess.run(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, cwd=cd)
    return r.stdout.decode('UTF-8').splitlines()

def get_till_end_of_code_block(item):
    ret = []
    line = item()
    while line != '```':
        ret.append(line)
        line = item()
    return ret

def handle_code_block(item, cd, exe):
    ret = ['```']
    cmd = item()
    ret.append(cmd)

    #ret.append('CMD = ' + cmd)

    cmd = cmd.split()
    rest = get_till_end_of_code_block(item)
    if cmd[0] == '$':
        cmd.pop(0)
        #ret.append(f"DEBUG: {cmd}")
        output = try_run_cmd(cmd, cd, exe)
        if output is not None:
            rest = output
    ret += rest
    ret.append('```')
    return ret

def process(lines, cd, exe):
    ret = []
    it = iter(lines)
    item = lambda: next(it)
    while True:
        try:
            line = item()
        except StopIteration:
            break
        if line == '```':
            ret += handle_code_block(item, cd, exe)
        else:
            ret.append(line)
    return ret


md, cd, exe = None, None, None
for x in sys.argv[1:]:
    if x.endswith('.md'):
        md = x
    elif os.path.isdir(x):
        cd = x
    else:
        exe = x



with open(md, 'r', encoding='UTF-8') as f:
    orig = f.read().splitlines()
    lines = process(orig, cd, exe)
    print('\n'.join(lines))


#TODO: make commands all run in parallel
#r = subprocess.run(['ls', 'x'], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
