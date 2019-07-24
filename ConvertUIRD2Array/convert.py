# coding:utf-8
import re

# lineThreshold = 100

lineNum = 1
rfile = open("work_script/ConvertUIRD2Array/input.txt", "r")
wfile = open("work_script/ConvertUIRD2Array/output.txt", "w")
# lines = rfile.readlines()
lines = [ll for ll in rfile.readlines() if ll != '\n']
p = re.compile(r'.{2}')
print("read %d line" % len(lines))
for line in lines:
    b = p.findall(line)
    print(b)
    if lineNum == 1:
        c = "{\n// " + str(lineNum) + "\n{0x" + ",0x".join(b) + "},\n"
    # elif lineNum == lineThreshold:
    elif lineNum == len(lines):
        c = "// " + str(lineNum) + "\n{0x" + ",0x".join(b) + "}\n};\n\n"
        lineNum = 0
    else:
        c = "// " + str(lineNum) + "\n{0x" + ",0x".join(b) + "},\n"
    lineNum += 1

    wfile.writelines(c)

if c.endswith(';\n\n') == False:
    pos = wfile.tell()
    wfile.seek(pos - 3, 0)
    wfile.writelines("\n};")

rfile.close()
wfile.close()
