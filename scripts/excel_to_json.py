import pandas as pd
import json
import os

def export_csv_to_json_hierarchy(csv_file, output_dir):
    # 1. Đọc file CSV
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return

    # 2. Tạo cấu trúc thư mục nếu chưa có
    categories_dir = os.path.join(output_dir, "categories")
    if not os.path.exists(categories_dir):
        os.makedirs(categories_dir)

    # 3. Lấy danh sách các Category duy nhất để tạo index.json
    unique_categories = df['category'].unique()
    index_data = []

    print("Đang xử lý từng danh mục...")

    for cat in unique_categories:
        # Tạo ID cho category (viết thường, thay khoảng trắng bằng gạch dưới)
        cat_id = str(cat).lower().replace(" ", "_")
        file_name = f"{cat_id}.json"
        
        # Lấy các linh kiện thuộc category này
        cat_df = df[df['category'] == cat]
        
        # Chuyển đổi dataframe sang danh sách dictionary (JSON)
        cat_list = cat_df.to_dict(orient='records')
        
        # Lưu vào file JSON tương ứng trong thư mục /categories
        with open(os.path.join(categories_dir, file_name), 'w', encoding='utf-8') as f:
            json.dump(cat_list, f, indent=4, ensure_ascii=False)
        
        # Thêm vào thông tin cho file index.json
        index_data.append({
            "id": cat_id,
            "name": cat,
            "data_url": f"https://raw.githubusercontent.com/NhatNguyen0201/my-electronics-db/main/data/categories/{file_name}"
        })
        print(f" - Đã tạo: {file_name}")

    # 4. Tạo file index.json
    with open(os.path.join(output_dir, "index.json"), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4, ensure_ascii=False)
    
    print("\nHoàn tất! Cấu trúc database đã sẵn sàng để đẩy lên GitHub.")

# Chạy script
if __name__ == "__main__":
    # Tên file csv đầu vào của bạn
    INPUT_CSV = 'D:\Project\CircuitLab\RemoteDatabase\demodata.csv' 
    # Thư mục gốc để chứa kết quả
    OUTPUT_FOLDER = 'D:\Project\CircuitLab\RemoteDatabase\my-electronics-db\data' 
    
    export_csv_to_json_hierarchy(INPUT_CSV, OUTPUT_FOLDER)