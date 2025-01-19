import sys, os
import subprocess

def main() -> int:
    '''
    Main entry point
    '''
    argCount = len(sys.argv)
    if sys.argv[1] == '-h' or sys.argv[1] == '--help':
        print('Usage: materialxjson <command> [options] where command is j2m or m2j')

    # Check if the command is valid
    cmdArgs = sys.argv[1:]
    if cmdArgs[0] == 'm2j':
        cmdArgs[0] = 'mtlx2json.py'
    elif cmdArgs[0] == 'j2m':
        cmdArgs[0] = 'json2mtlx.py'
    else:
        print('Unknown command specified:', cmdArgs[0])
        return 1
    
    # Build the command
    cmd = ' '.join(cmdArgs)
    packageLocation = os.path.dirname(__file__)
    cmd = 'python ' + packageLocation + '/' + cmd

    # Run the command
    return subprocess.call(cmd, shell=True)

if __name__ == '__main__':
    sys.exit(main())
