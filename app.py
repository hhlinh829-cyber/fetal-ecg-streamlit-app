import streamlit as st
import pandas as pd
import numpy as np
import joblib

import streamlit as st
import joblib
import os # Thêm thư viện os để kiểm tra tệp

# Thêm decorator @st.cache_resource
@st.cache_resource
def load_model_and_scaler():
    """Tải mô hình và scaler đã lưu."""
    
    # ĐƯỜNG DẪN ĐẾN CÁC TỆP TRÊN STREAMLIT CLOUD
    model_path = 'fetal_health_model.pkl'
    scaler_path = 'fetal_health_scaler.pkl'
    
    # BƯỚC 1: KIỂM TRA SỰ TỒN TẠI CỦA TỆP
    if not os.path.exists(model_path):
        st.error(f"Lỗi Tải File: Không tìm thấy '{model_path}'. Vui lòng kiểm tra tên file trên GitHub.")
        return None, None
    if not os.path.exists(scaler_path):
        st.error(f"Lỗi Tải File: Không tìm thấy '{scaler_path}'. Vui lòng kiểm tra tên file trên GitHub.")
        return None, None
    
    try:
        # BƯỚC 2: TẢI TỆP
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        st.success("Tải mô hình thành công! Ứng dụng đã sẵn sàng.") # Thêm thông báo thành công
        return model, scaler
    except Exception as e:
        # Lỗi xảy ra khi đọc tệp (dù tệp tồn tại)
        st.error(f"Lỗi: Không thể đọc file mô hình. Chi tiết lỗi: {e}")
        return None, None

# Gọi hàm tải mô hình và scaler
model, scaler = load_model_and_scaler()

# Thêm dòng kiểm tra nếu mô hình tải không thành công thì dừng chương trình
if model is None or scaler is None:
    st.stop()
