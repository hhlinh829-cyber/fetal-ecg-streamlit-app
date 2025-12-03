import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os 

# CẤU HÌNH TRANG WEB
st.set_page_config(page_title="Chẩn đoán CTG AI", layout="wide")

# ==============================================================================
# PHẦN 1: TẢI MÔ HÌNH VÀ SCALER (ĐÃ SỬA LỖI TẢI FILE)
# ==============================================================================

@st.cache_resource
def load_model_and_scaler():
    """Tải mô hình và scaler đã lưu."""
    model_path = 'fetal_health_model.pkl'
    scaler_path = 'fetal_health_scaler.pkl'
    
    # Kiểm tra sự tồn tại của tệp
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        st.error("Lỗi Tải File: Không tìm thấy file mô hình hoặc scaler. Vui lòng kiểm tra tên file trên GitHub.")
        return None, None
    
    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        # st.success("Tải mô hình thành công! Ứng dụng đã sẵn sàng.") 
        return model, scaler
    except Exception as e:
        st.error(f"Lỗi: Không thể đọc file mô hình. Chi tiết lỗi: {e}")
        return None, None

# Gọi hàm tải mô hình và scaler
model, scaler = load_model_and_scaler()

# Dừng ứng dụng nếu mô hình không tải được
if model is None or scaler is None:
    st.stop()
    
# ==============================================================================
# PHẦN 2: GIAO DIỆN VÀ XỬ LÝ DỮ LIỆU (PHẦN BỊ THIẾU)
# ==============================================================================

st.title("🩺 Ứng Dụng Phân Tích Điện Tim Thai (CTG) - Chẩn đoán Sơ bộ AI")
st.markdown("---")
st.subheader("Nhập 21 Chỉ Số Điện Tim Thai (CTG)")

# Tên các cột đầu vào (dùng để hiển thị)
FEATURE_NAMES = [
    'baseline value (bpm)', 'accelerations (per sec)', 'fetal_movement (per sec)',
    'uterine_contractions (per sec)', 'light_decelerations (per sec)', 
    'severe_decelerations (per sec)', 'prolongued_decelerations (per sec)',
    'abnormal_short_term_variability (%)', 'mean_value_of_short_term_variability',
    'percentage_of_time_with_abnormal_long_term_variability (%)', 
    'mean_value_of_long_term_variability', 'histogram_width', 'histogram_min',
    'histogram_max', 'histogram_number_of_peaks', 'histogram_number_of_zeroes',
    'histogram_mode', 'histogram_mean', 'histogram_median', 'histogram_variance',
    'histogram_tendency'
]

# Giá trị mặc định cho 21 chỉ số (ví dụ từ dữ liệu bình thường)
DEFAULT_VALUES = [
    120.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 73.0, 0.5, 43.0, 2.4, 64.0, 62.0, 
    126.0, 2.0, 0.0, 120.0, 137.0, 121.0, 73.0, 1.0
]


# Chia giao diện thành 3 cột để nhập liệu
input_data = {}
cols = st.columns(3)

for i, feature in enumerate(FEATURE_NAMES):
    col_index = i % 3
    with cols[col_index]:
        # Tạo ô nhập liệu cho từng tính năng
        # Sử dụng format="%.4f" cho các giá trị nhỏ, và format="%d" cho các giá trị lớn
        
        # Chỉ số 0-6 là các tần suất (dùng 4 chữ số thập phân)
        if i <= 6:
            input_data[feature] = st.number_input(f"Nhập **{feature}**", 
                                                value=DEFAULT_VALUES[i], 
                                                step=0.0001, 
                                                format="%.4f",
                                                key=f"input_{i}")
        # Chỉ số 7-20 là các giá trị lớn hơn (dùng 2 chữ số thập phân hoặc số nguyên)
        else:
            input_data[feature] = st.number_input(f"Nhập **{feature}**", 
                                                value=DEFAULT_VALUES[i], 
                                                step=0.1, 
                                                format="%.2f",
                                                key=f"input_{i}")


# NÚT DỰ ĐOÁN
st.markdown("---")
st.subheader("Bấm vào để xem kết quả chẩn đoán sơ bộ")

if st.button('🔮 Chẩn Đoán Sơ Bộ', use_container_width=True):
    
    # Chuẩn bị dữ liệu đầu vào
    input_df = pd.DataFrame([input_data])
    
    # Chuẩn hóa dữ liệu (Scaling)
    # Lưu ý: fit_transform chỉ dùng khi training. Ở đây ta dùng transform.
    scaled_data = scaler.transform(input_df)
    
    # Dự đoán
    prediction = model.predict(scaled_data)
    
    # Giải mã kết quả
    # 1: Normal (Bình thường), 2: Suspect (Nghi ngờ), 3: Pathologic (Bệnh lý)
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
