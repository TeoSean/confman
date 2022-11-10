import sys, os

CONFIG_DIR = os.path.join(os.environ['HOME'], 'confs')
COMMAND = sys.argv[1]
TARGET = sys.argv[2]

#os.chdir(CONFIG_DIR)
def logsys(cmd):
    print(cmd)
    os.system(cmd)
match COMMAND:
    case 'load':
        if not os.path.exists(CONFIG_DIR): 
            print(f'Error: Necessary files not found. Run "{sys.argv[0]} init default" to get started.')
            exit(1)
        os.chdir(CONFIG_DIR)
        if not TARGET in os.listdir():
            print(f'Error: Necessary files not found. Run "{sys.argv[0]} init default" to get started.')
            exit(1)

        #if not TARGET+'.txt' in os.listdir(): 
        #    print(f'Error: Necessary files not found. Run "{sys.argv[0]} init default" to get started.')
        #    exit()
        
        if not 'current.txt'in os.listdir():
            print(f'Error: Necessary files not found. Run "{sys.argv[0]} init default" to get started.')
            exit(1)

        with open('current.txt', 'r') as file:
            for i in file.readlines():
                logsys(f'unlink {i.strip()}')
        with open('current.txt', 'w') as file:
            for r, d, f in os.walk(os.path.join(CONFIG_DIR, TARGET)):
                for dir_ in d: 
                    p = os.path.join(os.environ['HOME'], os.path.relpath(os.path.join(r, dir_), os.path.join(CONFIG_DIR, TARGET)))
                    logsys(f'mkdir -p {p}')
                for fi in f:
                    file.write(os.path.join(r, fi)+'\n')
                    p = os.path.join(os.environ['HOME'], os.path.relpath(os.path.join(r, fi), os.path.join(CONFIG_DIR, TARGET)))
                    logsys(f'ln -sf {os.path.join(r, fi)} {p}')
    
    case 'init':
        os.mkdir(CONFIG_DIR)
        os.chdir(CONFIG_DIR)
        os.mkdir(TARGET)
        logsys(f'cp -r ~/.config ~/confs/{TARGET}')
        with open('current.txt', 'w+') as file:
            for r, d, f in os.walk(os.path.join(CONFIG_DIR, TARGET)):
                for fi in f:
                    file.write(os.path.join(r, fi)+'\n')
                    p = os.path.join(os.environ['HOME'], os.path.relpath(os.path.join(r, fi), os.path.join(CONFIG_DIR, TARGET)))
                    logsys(f'ln -sf {os.path.join(r, fi)} {p}')

    case 'export':
        outfile = sys.argv[3]
        if not os.path.exists(CONFIG_DIR): 
            print(f'Error: Necessary files not found. Run "{sys.argv[0]} init default" to get started.')
            exit(1)
        # os.chdir(CONFIG_DIR)
        if not TARGET in os.listdir(CONFIG_DIR):
            print(f'Error: profile {TARGET} not found. Run "{sys.argv[0]} init {TARGET}" to copy your current config to profile {TARGET}')
            exit()
       
        logsys(f'zip -r {outfile} {os.path.join(CONFIG_DIR, TARGET)}')
        print('Profile "{TARGET}" has been exported to {outfile}.')


    case 'import':
        infile = sys.argv[3]
        if not os.path.exists(CONFIG_DIR): 
            print(f'Error: Necessary files not found. Run "{sys.argv[0]} init default" to get started.')
            exit(1)
        # os.chdir(CONFIG_DIR)
        if not TARGET in os.listdir(CONFIG_DIR):
            print(f'Error: profile {TARGET} not found. Run "{sys.argv[0]} init {TARGET}" to copy your current config to profile {TARGET}')
            exit()
        
        logsys(f'unzip {infile} -d {CONFIG_DIR}')
        print('Profile has been imported.')
