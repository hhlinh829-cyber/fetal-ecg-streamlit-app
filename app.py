import streamlit as st
import pandas as pd
import numpy as np
import joblib

import streamlit as st
import joblib

# ... (Giữ nguyên các lệnh import khác nếu có)
# import pandas as pd
# import numpy as np 

# BẮT ĐẦU PHẦN THAY THẾ
@st.cache_resource
def load_model_and_scaler():
    """Tải mô hình và scaler đã lưu."""
    try:
        # Tải Mô hình
        model = joblib.load('fetal_health_model.pkl')
        
        # Tải Scaler
        scaler = joblib.load('fetal_health_scaler.pkl')
        
        return model, scaler
    except FileNotFoundError:
        # st.error sẽ hiển thị lỗi trên web nếu không tìm thấy file
        st.error("Lỗi: Không tìm thấy file mô hình (.pkl). Vui lòng kiểm tra lại tên file trên GitHub.")
        return None, None

# Gọi hàm tải mô hình và scaler. Dữ liệu trả về sẽ thay thế biến 'model' và 'scaler' cũ của bạn.
model, scaler = load_model_and_scaler()

# KẾT THÚC PHẦN THAY THẾ
# ... (Phần code thiết lập giao diện web của bạn sẽ nằm ở dưới đây)

