from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Đọc dữ liệu từ tệp CSV
data = pd.read_csv('C:/StockPrediction/datasets/prediction_target.csv')

@app.route('/api/v1/stock', methods=['POST'])
def get_profit_data():
    try:
        # Lấy tham số từ body yêu cầu
        page = request.json.get('page', 1)
        page_size = request.json.get('page_size', 5)

        # Tính toán các chỉ số cho phân trang
        start = (page - 1) * page_size
        end = start + page_size

        # Lấy dữ liệu phân trang
        paginated_data = data[start:end].to_dict(orient='records')

        # Trả về dữ liệu dưới dạng JSON với mã thành công
        return jsonify({
            'status': 1,  # Mã thành công
            'page': page,
            'page_size': page_size,
            'total': len(data),
            'data': paginated_data
        })
    except Exception as e:
        # Xử lý lỗi và trả về mã thất bại
        return jsonify({
            'status': 0,  # Mã thất bại
            'message': str(e)
        })

@app.after_request
def add_cors_headers(response):
    # Thêm headers CORS cho phản hồi
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

if __name__ == '__main__':
    # Chạy ứng dụng Flask
    from waitress import serve
    serve(app, host='0.0.0.0', port=80)
    # serve(app, host='0.0.0.0', port=80, threads=6, max_request_body_size=1073741824, max_request_header_size=262144, max_connections=2000)
    # app.run(host='0.0.0.0', port=80, debug=False)
