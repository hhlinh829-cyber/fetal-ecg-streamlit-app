import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os 

# CẤU HÌNH TRANG WEB
st.set_page_config(page_title="Chẩn đoán CTG AI", layout="wide")

# ==============================================================================
# PHẦN 1: TẢI MÔ HÌNH VÀ SCALER
# ==============================================================================

@st.cache_resource
def load_model_and_scaler():
    """Tải mô hình và scaler đã lưu."""
    # Đường dẫn tệp trên Streamlit Cloud
    model_path = 'fetal_health_model.pkl'
    scaler_path = 'fetal_health_scaler.pkl'
    
    # Kiểm tra sự tồn tại của tệp
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        st.error("Lỗi Tải File: Không tìm thấy file mô hình hoặc scaler. Vui lòng kiểm tra tên file trên GitHub.")
        return None, None
    
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        return model, scaler
    except Exception as e:
        # Xử lý lỗi khi đọc file (ví dụ: file bị hỏng)
        st.error(f"Lỗi: Không thể đọc file mô hình. Chi tiết lỗi: {e}")
        return None, None

# Gọi hàm tải mô hình và scaler
model, scaler = load_model_and_scaler()

if model is None or scaler is None:
    # Ngừng chạy ứng dụng nếu tải mô hình thất bại
    st.stop()
    
# ==============================================================================
# PHẦN 2: GIAO DIỆN VÀ XỬ LÝ DỮ LIỆU (ĐÃ SỬA LỖI TÊN CỘT DÙNG CHO SCALING)
# ==============================================================================

st.title("🩺 Ứng Dụng Phân Tích Điện Tim Thai (CTG) - Chẩn đoán Sơ bộ AI")
st.markdown("---")
st.subheader("Nhập 21 Chỉ Số Điện Tim Thai (CTG)")

# Đây là danh sách tên cột mà MÔ HÌNH YÊU CẦU. 
# Nó KHỚP CHÍNH XÁC với tên cột khi mô hình được huấn luyện để giải quyết lỗi ValueError.
MODEL_FEATURE_NAMES = [
    'baseline_value', 'accelerations', 'fetal_movement',
    'uterine_contractions', 'light_decelerations', 
    'severe_decelerations', 'prolongued_decelerations',
    'abnormal_short_term_variability', 'mean_value_of_short_term_variability',
    'percentage_of_time_with_abnormal_long_term_variability', 
    'mean_value_of_long_term_variability', 'histogram_width', 'histogram_min',
    'histogram_max', 'histogram_number_of_peaks', 'histogram_number_of_zeroes',
    'histogram_mode', 'histogram_mean', 'histogram_median', 'histogram_variance',
    'histogram_tendency'
]

# Tên thân thiện để HIỂN THỊ trên giao diện (Có đơn vị, dễ đọc)
DISPLAY_NAMES = [
    'Giá trị cơ sở (bpm)', 'Tăng tốc (mỗi giây)', 'Chuyển động thai (mỗi giây)',
    'Co thắt tử cung (mỗi giây)', 'Giảm tốc nhẹ (mỗi giây)', 
    'Giảm tốc nghiêm trọng (mỗi giây)', 'Giảm tốc kéo dài (mỗi giây)',
    'Biến thiên ngắn hạn bất thường (%)', 'Giá trị trung bình biến thiên ngắn hạn',
    'Phần trăm thời gian biến thiên dài hạn bất thường (%)', 
    'Giá trị trung bình biến thiên dài hạn', 'Chiều rộng Histogram', 'Histogram Min',
    'Histogram Max', 'Số đỉnh Histogram', 'Số điểm 0 Histogram',
    'Mode Histogram', 'Mean Histogram', 'Median Histogram', 'Variance Histogram',
    'Xu hướng Histogram'
]


# Giá trị mặc định (để người dùng dễ nhập liệu)
DEFAULT_VALUES = [
    120.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 73.0, 0.5, 43.0, 2.4, 64.0, 62.0, 
    126.0, 2.0, 0.0, 120.0, 137.0, 121.0, 73.0, 1.0
]


# Chia giao diện thành 3 cột để nhập liệu
input_data = {}
cols = st.columns(3)

# Tạo các ô nhập liệu
for i, (model_feature, display_name) in enumerate(zip(MODEL_FEATURE_NAMES, DISPLAY_NAMES)):
    col_index = i % 3
    with cols[col_index]:
        
        # Thiết lập format và step khác nhau cho các chỉ số nhỏ/lớn
        if i <= 6:
            # Tần suất (thường là số rất nhỏ, cần độ chính xác cao)
            value = st.number_input(f"Nhập **{display_name}**", 
                                                value=DEFAULT_VALUES[i], 
                                                step=0.0001, 
                                                format="%.4f",
                                                key=f"input_{i}")
        else:
            # Các giá trị khác (thường là số nguyên hoặc số thập phân đơn giản)
            value = st.number_input(f"Nhập **{display_name}**", 
                                                value=DEFAULT_VALUES[i], 
                                                step=0.1, 
                                                format="%.2f",
                                                key=f"input_{i}")
        
        # LƯU VỚI TÊN CỘT CỦA MÔ HÌNH
        input_data[model_feature] = value


# NÚT DỰ ĐOÁN
st.markdown("---")
st.subheader("Bấm vào để xem kết quả chẩn đoán sơ bộ")

if st.button('🔮 Chẩn Đoán Sơ Bộ', use_container_width=True):
    
    # 1. Chuẩn bị dữ liệu đầu vào (Tạo DataFrame từ dictionary)
    input_df = pd.DataFrame([input_data], index=[0])
    
    # 2. Đảm bảo thứ tự cột CHÍNH XÁC (Rất quan trọng cho scikit-learn/joblib)
    # Lỗi ValueError xảy ra vì tên cột không khớp và/hoặc thứ tự bị sai. Dòng này sửa lỗi đó.
    input_df = input_df[MODEL_FEATURE_NAMES]
    
    # 3. Chuẩn hóa dữ liệu (Scaling)
    scaled_data = scaler.transform(input_df)
    
    # 4. Dự đoán
    prediction = model.predict(scaled_data)
    
    # 5. Giải mã kết quả
    # Phân loại: 1: Normal, 2: Suspect, 3: Pathologic
    if prediction[0] == 1:
        result = "Bình thường (Normal) ✅"
        st.success(f"Kết Quả Phân Tích AI: {result}")
    elif prediction[0] == 2:
        result = "Nghi ngờ (Suspect) ⚠️"
        st.warning(f"Kết Quả Phân Tích AI: {result}")
    else:
        result = "Bệnh lý (Pathologic) 🔴"
        st.error(f"Kết Quả Phân Tích AI: {result}")
        
    st.balloons()
