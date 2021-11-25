#  application/run.py
# 만들어진 서버 객체를 실행한다.
from create import create_app
import argparse

parser = argparse.ArgumentParser(description='서버 실행 환경 선택')
parser.add_argument('--env', required=False, default='dev', help='dev, prod, test 가 있습니다.')

args = parser.parse_args()

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=80)