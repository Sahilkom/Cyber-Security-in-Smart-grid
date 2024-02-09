import sys

def main():
    if len(sys.argv) != 2:
        sys.stderr.write(f'Usage:\n{sys.argv[0]} start|stop\n')
        sys.exit(1)

    with open('flags.txt', 'w') as f:
        if sys.argv[1] == 'start':
            f.write('1')
        else:
            f.write('0')

if __name__ == '__main__':
    main()
