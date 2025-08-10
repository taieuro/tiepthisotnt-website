import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# --- Cấu hình ---
LIVE_URL = 'https://gobranding.com.vn/' # URL của trang web cần lấy dữ liệu
HTML_OUTPUT_FILE = 'templates/index.html' # Nơi lưu file HTML sạch
STATIC_FOLDER = 'static'
IMAGE_FOLDER = os.path.join(STATIC_FOLDER, 'images')
VALID_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']

# --- Bước 1: Tạo các thư mục cần thiết ---
os.makedirs(os.path.dirname(HTML_OUTPUT_FILE), exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)
print(f"Các thư mục '{os.path.dirname(HTML_OUTPUT_FILE)}' và '{IMAGE_FOLDER}' đã sẵn sàng.")

def download_asset(asset_url):
    """Tải một tài sản (ảnh) từ URL và trả về đường dẫn cục bộ mới."""
    # Đảm bảo URL là đầy đủ (ví dụ: biến /wp-content/... thành https://...)
    full_url = urljoin(LIVE_URL, asset_url)
    
    try:
        path = urlparse(full_url).path
        filename = os.path.basename(path)

        # Kiểm tra đuôi file hợp lệ
        if not any(path.lower().endswith(ext) for ext in VALID_EXTENSIONS):
            print(f"⚠️  Bỏ qua: '{asset_url}' (Không phải file ảnh hợp lệ)")
            return None

        # Tải file
        response = requests.get(full_url, timeout=15)
        response.raise_for_status()

        save_path = os.path.join(IMAGE_FOLDER, filename)
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Tải thành công: {filename}")
        
        # Trả về đường dẫn mới để sử dụng trong file HTML
        return f"/{STATIC_FOLDER}/images/{filename}"

    except requests.exceptions.RequestException as e:
        print(f"❌ Lỗi khi tải {full_url}: {e}")
        return None

# --- Bước 2: Lấy nội dung HTML trực tiếp từ trang web ---
print(f"\nĐang tải nội dung từ {LIVE_URL}...")
try:
    response = requests.get(LIVE_URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    print("Tải nội dung HTML thành công!")
except requests.exceptions.RequestException as e:
    print(f"Không thể tải trang web. Lỗi: {e}")
    exit() # Thoát chương trình nếu không lấy được HTML

# --- Bước 3: Tìm, tải và cập nhật đường dẫn ảnh ---
print("\nBắt đầu quét và tải hình ảnh...")
for img_tag in soup.find_all('img'):
    # Ưu tiên lấy 'data-src' hoặc 'data-lazy-src' cho các ảnh tải trễ
    original_src = img_tag.get('data-src') or img_tag.get('src')
    
    if original_src:
        new_src = download_asset(original_src)
        if new_src:
            img_tag['src'] = new_src # Cập nhật lại đường dẫn
            # Xóa các thuộc tính tải trễ không cần thiết nữa
            if 'data-src' in img_tag.attrs:
                del img_tag['data-src']
            if 'srcset' in img_tag.attrs:
                del img_tag['srcset']

# --- Bước 4: Lưu lại file HTML hoàn chỉnh ---
print(f"\nĐang lưu file HTML đã xử lý vào '{HTML_OUTPUT_FILE}'...")
with open(HTML_OUTPUT_FILE, 'w', encoding='utf-8') as f:
    # Dùng prettify() để file HTML mới có cấu trúc đẹp, dễ đọc
    f.write(str(soup.prettify()))

print("\n🎉🎉🎉 Hoàn tất! Mọi thứ đã sẵn sàng cho Giai đoạn 2 (chạy với Flask).")