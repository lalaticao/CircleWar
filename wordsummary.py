import os

exception = ["graphics.py", "wordsummary.py"]
exceptionDir = [".git"]

def summary(dirname=os.curdir, stage=0):
    if stage:
        try:
            if dirname in exceptionDir:
                raise Exception()
            os.chdir(dirname)
        except:
            return "",0,0

    file_name_list = os.listdir(os.curdir)
    global exception
    lines_total = 0
    chars_total = 0
    
    r=""
    for file_name in file_name_list:
        rr, ll, cc = summary(file_name, stage+1)
        #print os.listdir(os.curdir)
        if rr == "":
            if file_name[-3:]==".py" or file_name[-4:]==".pyw":
                if not(file_name in exception):
                    f = file(file_name)
                    line_list = f.readlines()
                    f.close()
                    
                    lines = len(line_list)
                    chars = 0
                    for line in line_list:
                        chars += len(line)
                        
                    r+='  '*stage + "%-*s"%(40-2*stage,file_name)+ \
                        "%-15s %-15s\n"%\
                        ("%-d lines"%lines,"%-d characters"%chars)
                    
                    lines_total += lines
                    chars_total += chars
        else:
            r='  '*stage+""+file_name+" <dir> " + rr+r
            lines_total += ll
            chars_total += cc

    if stage:
        os.chdir("..")
    
    r = "(total: %s, %s)\n"%\
            ("%-d lines"%lines_total,"%-d characters"%chars_total) + r
    return r, lines_total, chars_total

print summary()[0]
