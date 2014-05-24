from Classes.Compiler import Compiler

compiler = Compiler("./dist", "./nrtmp", "./Resources")

compiler.compileNightrainLinux()

# clean output folder
compiler.cleanDist()

# compile PHP

if compiler.isWindows():
    compiler.compilePHPWindows()

if compiler.isLinux():
    compiler.compilePHPLinux()

if compiler.isMac():
    compiler.compilePHPMac()

# compile nightrain

if compiler.isWindows():
    compiler.compileNightrainWindows()

if compiler.isLinux():
    compiler.compileNightrainLinux()

if compiler.isMac():
    compiler.compileNightrainMac()

# copy required files
compiler.copyResources()

if compiler.isWindows():
    compiler.copyPHPWindows()

if compiler.isLinux():
    compiler.copyPHPLinux()

if compiler.isMac():
    compiler.copyPHPMac()

