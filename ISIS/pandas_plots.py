import pandas as pd
import os

def main(filename, workspace=os.getcwd()):
    os.chdir(workspace)
    f = open(filename)
    lines = f.readlines()
    f.close()

    print(lines)


if __name__ == '__main__':
    main('isis_tweets.csv')