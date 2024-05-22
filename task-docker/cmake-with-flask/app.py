from argparse import ArgumentParser
from flask import Flask



def parse_args():
    parser = ArgumentParser('Test web app')
    parser.add_argument('--port', type=int, help='Port to use')
    parser.add_argument('--host', type=str, help='Host to use')
    return parser.parse_args()



app = Flask('Test app')


@app.route('/app')
def main():
    return 'ok'


if __name__ == '__main__':
    args = parse_args()
    app.run(port=args.port, host=args.host)
