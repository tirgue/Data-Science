import os
import glob

def pathCompletion(text, line, begidx, endidx):
    def _append_slash_if_dir(p):
        if p and os.path.isdir(p) and p[-1] != os.sep:
            return p + os.sep
        else:
            return p
            
    before_arg = line.rfind(" ", 0, begidx)
    if before_arg == -1:
        return

    fixed = line[before_arg+1:begidx]
    arg = line[before_arg+1:endidx]
    pattern = arg + '*'

    completions = []
    for path in glob.glob(pattern):
        path = _append_slash_if_dir(path)
        completions.append(path.replace(fixed, "", 1))
    return completions