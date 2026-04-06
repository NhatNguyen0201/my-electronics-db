import pandas as pd
import json
import os

def export_compact_json(csv_file, output_dir):
    # 1. Đọc file CSV
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return

    # 2. Bảng ánh xạ: Gom các loại nhỏ vào 10 nhóm lớn
    category_mapping = {
        'Passive': 'Passive', 'Resistor': 'Passive', 'Capacitor': 'Passive', 'Inductor': 'Passive',
        'Semiconductors': 'Semiconductors', 'Diode': 'Semiconductors', 'Transistor': 'Semiconductors', 'MOSFET': 'Semiconductors',
        'Power & Regulators': 'Power & Regulators', 'IC-Regulator': 'Power & Regulators', 'Power Module': 'Power & Regulators',
        'Analog ICs': 'Analog ICs', 'IC-OpAmp': 'Analog ICs', 'IC-Timer': 'Analog ICs',
        'Digital ICs': 'Digital ICs', 'IC-Digital': 'Digital ICs', 'Logic Gate': 'Digital ICs',
        'Microcontrollers': 'Microcontrollers', 'MCU': 'Microcontrollers', 'Development Board': 'Microcontrollers',
        'Sensors': 'Sensors', 'Sensor': 'Sensors',
        'Optoelectronics': 'Optoelectronics', 'Opto': 'Optoelectronics', 'Display': 'Optoelectronics', 'LED': 'Optoelectronics',
        'Electromechanical': 'Electromechanical', 'Relay': 'Electromechanical', 'Motor': 'Electromechanical',
        'Connectors & Tools': 'Connectors & Tools', 'Connector': 'Connectors & Tools', 'Tool': 'Connectors & Tools'
    }

    # Áp dụng gom nhóm
    # Nếu giá trị trong cột 'category' có trong mapping thì đổi, nếu không thì giữ nguyên
    df['category'] = df['category'].map(lambda x: category_mapping.get(x, 'Others'))

    # 3. Tạo cấu trúc thư mục
    categories_dir = os.path.join(output_dir, "categories")
    if not os.path.exists(categories_dir):
        os.makedirs(categories_dir)

    # 4. Lấy danh sách các Category sau khi đã gom nhóm
    unique_categories = df['category'].unique()
    index_data = []

    print(f"Đang xử lý dữ liệu vào {len(unique_categories)} danh mục chính...")

    for cat in unique_categories:
        # Tạo ID cho file (ví dụ: "Power & Regulators" -> "power_regulators.json")
        cat_id = str(cat).lower().replace(" & ", "_").replace(" ", "_")
        file_name = f"{cat_id}.json"
        
        # Lọc linh kiện thuộc nhóm này
        cat_df = df[df['category'] == cat]
        
        # Chuyển sang JSON
        cat_list = cat_df.to_dict(orient='records')
        
        # Lưu file chi tiết
        file_path = os.path.join(categories_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(cat_list, f, indent=4, ensure_ascii=False)
        
        # Thêm vào file index
        index_data.append({
            "id": cat_id,
            "name": cat,
            "data_url": f"https://raw.githubusercontent.com/NhatNguyen0201/my-electronics-db/main/data/categories/{file_name}",
        })
        print(f" - Đã gom nhóm và tạo: {file_name} ({len(cat_list)} linh kiện)")

    # 5. Lưu file index.json
    with open(os.path.join(output_dir, "index.json"), 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=4, ensure_ascii=False)
    
    print("\nHoàn tất! Cấu trúc database gọn nhẹ đã sẵn sàng tại thư mục: " + output_dir)

# Chạy script
if __name__ == "__main__":
    # Đảm bảo file components.csv nằm cùng thư mục với script này
    INPUT_CSV = 'D:\Project\CircuitLab\RemoteDatabase\demodata.csv' 
    OUTPUT_FOLDER = 'D:\Project\CircuitLab\RemoteDatabase\my-electronics-db\data' 
    
    export_compact_json(INPUT_CSV, OUTPUT_FOLDER)