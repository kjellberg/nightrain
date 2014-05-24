from Classes.Compiler import Compiler

compiler = Compiler("./dist", "./nrtmp", "./Resources")

# clean output folder
compiler.cleanDist()

# compile nightrain

if compiler.isWindows():
    compiler.compileNightrainWindows()

if compiler.isLinux():
    compiler.compileNightrainLinux()

if compiler.isMac():
    compiler.compileNightrainMac()

# compile PHP

if compiler.isWindows():
    compiler.compilePHPWindows()

if compiler.isLinux():
    compiler.compilePHPLinux()

if compiler.isMac():
    compiler.compilePHPMac()

# copy required files
compiler.copyResources()

if compiler.isWindows():
    compiler.copyPHPWindows()

if compiler.isLinux():
    compiler.copyPHPLinux()
    compiler.copyPHPINILinux()

if compiler.isMac():
    compiler.copyPHPMac()

