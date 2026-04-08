import pandas as pd
import json
import os

def export_compact_json(csv_file, output_dir):
    # 1. Đọc file CSV mới
    try:
        # Sử dụng encoding='utf-8-sig' để tránh lỗi BOM của Excel
        df_new = pd.read_csv(csv_file, encoding='utf-8-sig')
    except Exception as e:
        print(f"Lỗi khi đọc file CSV: {e}")
        return

    # 2. Tạo cấu trúc thư mục
    categories_dir = os.path.join(output_dir, "categories")
    if not os.path.exists(categories_dir):
        os.makedirs(categories_dir)

    # 3. Lấy danh sách các Category hiện có trong CSV
    unique_categories = df_new['category'].unique()
    index_data = []

    print(f"Đang xử lý dữ liệu cho {len(unique_categories)} danh mục...")

    for cat in unique_categories:
        cat_id = str(cat).lower().replace(" & ", "_").replace(" ", "_")
        file_name = f"{cat_id}.json"
        file_path = os.path.join(categories_dir, file_name)

        # Lấy list linh kiện mới từ CSV
        new_list = df_new[df_new['category'] == cat].to_dict(orient='records')

        # --- LOGIC GIỮ LẠI DỮ LIỆU CŨ ---
        final_list = []
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    old_data = json.load(f)
                    # Tạo set các ID đã có để check trùng
                    existing_ids = {str(item.get('id')) for item in new_list}
                    
                    # Giữ lại những item cũ mà ID không nằm trong file CSV mới
                    for old_item in old_data:
                        if str(old_item.get('id')) not in existing_ids:
                            final_list.append(old_item)
            except Exception as e:
                print(f"Lưu ý: Không thể đọc file cũ {file_name}, sẽ tạo mới. Lỗi: {e}")

        # Gộp dữ liệu cũ (không trùng) và dữ liệu mới
        final_list.extend(new_list)

        # 4. Lưu file chi tiết
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(final_list, f, indent=4, ensure_ascii=False)
        
        # 5. Cấu trúc lại URL cho index.json (trỏ đến thư mục data của bạn trên GitHub)
        # Bạn hãy thay 'user/repo' bằng thông tin thật của mình
        github_raw_base = "https://raw.githubusercontent.com/NhatNguyen0201/my-electronics-db/main/data/categories/"
        
        index_data.append({
            "id": cat_id,
            "name": cat,
            "data_url": f"{github_raw_base}{file_name}",
            "item_count": len(final_list)
        })
        print(f" - Cập nhật: {file_name} (Tổng cộng: {len(final_list)} linh kiện)")

    # 6. Cập nhật file index.json (Cũng giữ lại các category cũ nếu CSV không có)
    index_path = os.path.join(output_dir, "index.json")
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            old_index = json.load(f)
            new_cat_ids = {item['id'] for item in index_data}
            for old_cat in old_index:
                if old_cat['id'] not in new_cat_ids:
                    index_data.append(old_cat)

    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4, ensure_ascii=False)
    
    print("\nHoàn tất! Dữ liệu đã được merge thành công.")

if __name__ == "__main__":
    # Lưu ý: Thêm r trước chuỗi đường dẫn Windows để tránh lỗi Unicode
    INPUT_CSV = r'D:\Project\CircuitLab\RemoteDatabase\components_4.csv' 
    OUTPUT_FOLDER = r'D:\Project\CircuitLab\RemoteDatabase\my-electronics-db\data' 
    
    export_compact_json(INPUT_CSV, OUTPUT_FOLDER)