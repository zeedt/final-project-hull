
#### Execute the file with python3 sample-call.py --letters "A,B"


import argparse



def execute_crawl(letters):
    print(letters)
        


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--letters",
        default="",
        help="tLetters separated with comma"
    )
    args = parser.parse_args()

    execute_crawl(args.letters.split(','))