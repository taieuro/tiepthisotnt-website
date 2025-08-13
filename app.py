from flask import Flask, render_template

# 1. Khởi tạo ứng dụng web Flask
#    - `__name__` là một biến đặc biệt trong Python, giúp Flask biết vị trí của ứng dụng
#      để tìm các tài nguyên như thư mục 'templates'.
app = Flask(__name__)

# 2. Định nghĩa một "route" (đường dẫn) cho trang chủ
#    - `@app.route("/")` giống như một biển chỉ dẫn. Nó nói rằng: "Khi có ai đó
#      truy cập vào đường dẫn gốc của website (ví dụ: http://127.0.0.1:8000/),
#      hãy thực thi hàm `home()` ngay bên dưới."
@app.route("/")
def home():
    # Hàm này chỉ có một nhiệm vụ: tìm file 'index.html' trong thư mục 'templates'
    # và trả về nội dung của nó cho trình duyệt.
    return render_template("index.html")

# --- THÊM ROUTE MỚI CHO TRANG "VỀ CHÚNG TÔI" ---
@app.route("/ve-chung-toi/")
def ve_chung_toi():
    return render_template("ve-chung-toi.html")
# -----------------------------------------------

# --- THÊM ROUTE MỚI CHO TRANG "DỊCH VỤ TIẾP THỊ SỐ ĐA KÊNH" ---
@app.route("/dich-vu-tiep-thi-so-da-kenh/")
def dich_vu_tiep_thi_so_da_kenh():
    return render_template("dich-vu-tiep-thi-so-da-kenh.html")
# -----------------------------------------------

# 3. Chạy ứng dụng
#    - `if __name__ == "__main__":` là một quy ước trong Python. Nó đảm bảo rằng
#      lệnh `app.run()` chỉ được thực thi khi bạn chạy trực tiếp file này 
#      (bằng lệnh `python3 app.py`), chứ không phải khi nó được import bởi một file khác.
#    - `debug=True` sẽ tự động tải lại server mỗi khi bạn thay đổi code, rất tiện lợi khi lập trình.
#    - `port=8000` chỉ định server sẽ chạy trên cổng 8000, tránh xung đột với các ứng dụng khác.
if __name__ == "__main__":
    app.run(debug=True, port=8000)