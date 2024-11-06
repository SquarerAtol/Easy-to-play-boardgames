import os

from src.app import create_app, socketio

if __name__ == "__main__":
    config_key = os.getenv("local")  # 환경에 맞게 기본 설정을 지정
    app = create_app(config_key)

    # socketio 서버 실행
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)