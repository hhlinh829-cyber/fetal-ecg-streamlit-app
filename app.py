import streamlit as st
import datetime
import pandas as pd
import numpy as np
import time

# --- Cấu hình giao diện và Phong cách (Aesthetics) ---

# Tông màu chủ đạo (Pastel Blue, Pink, Beige)
COLOR_BEIGE = "#f8f7f3"
COLOR_BLUE = "#a8dadc"       # Xanh pastel
COLOR_DARK_BLUE = "#1d3557"  # Xanh đậm cho chữ
COLOR_PINK = "#fcc8c8"       # Hồng pastel
COLOR_DARK_PINK = "#e63946"  # Hồng đậm cho chữ
COLOR_LIGHT_GRAY = "#eeeeee"

# 21 chỉ số giả lập (Dùng cho phần chẩn đoán)
MODEL_FEATURE_NAMES = [
    "Baseline Value (bpm)", "Accel Time (msec)", "Movements", "Uterine Contractions",
    "Light Decels", "Severe Decels", "Long Decels", "Var Short Term (%)", 
    "Var Short Term Mean", "Var Long Term (%)", "Var Long Term Mean", "Histogram Width", 
    "Mode", "Mean", "Median", "Variance", "Tendency", "Hist Peaks", "Hist Zeros",
    "NSP (A, B, C)", "LBE (bpm)" 
]

def apply_custom_css():
    """Áp dụng CSS tùy chỉnh để thiết lập tông màu pastel và font chữ."""
    # Lưu ý: Font chữ được sử dụng là font hệ thống hiện đại.
    css = f"""
    <style>
        /* Thiết lập font và nền chung */
        .stApp {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: {COLOR_BEIGE};
        }}
        
        /* Tiêu đề chính */
        h1 {{ 
            color: {COLOR_DARK_BLUE};
            font-weight: 700;
        }}
        
        /* Màu chữ đậm theo yêu cầu */
        h2, h3, h4, h5, h6, label, .st-emotion-cache-1wivap2 {{
            color: {COLOR_DARK_BLUE} !important;
        }}

        /* Tùy chỉnh màu nút bấm */
        .stButton>button {{
            background-color: {COLOR_BLUE};
            color: {COLOR_DARK_BLUE};
            border-radius: 8px;
            border: 1px solid {COLOR_DARK_BLUE};
            padding: 8px 16px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        .stButton>button:hover {{
            background-color: {COLOR_PINK};
            border-color: {COLOR_DARK_PINK};
            color: {COLOR_DARK_PINK};
        }}
        
        /* Box chứa nội dung chính */
        .main-content-box {{
            padding: 20px;
            border-radius: 12px;
            background-color: white; /* Nền trắng cho nội dung */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            border-left: 5px solid {COLOR_PINK}; /* Điểm nhấn hồng */
        }}
        
        /* Thiết lập màu cho input */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stDateInput>div>div>input {{
            border-radius: 8px;
            border: 1px solid {COLOR_BLUE};
            background-color: {COLOR_LIGHT_GRAY};
            padding: 8px 10px;
        }}
        
        /* Màu nền cho các tab không được chọn */
        .st-emotion-cache-13l39w3 {{
            background-color: {COLOR_BEIGE};
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- Logic Chẩn đoán và Nhận xét ---

def get_diagnosis_result(prediction_value):
    """
    Trả về kết quả chẩn đoán và lời khuyên dựa trên giá trị giả lập.
    prediction_value là giá trị từ 0 đến 100.
    """
    if prediction_value <= 70:
        result = "Bình thường"
        color = "green"
        advice = """
            **Đây là một tín hiệu rất tích cực.** Mẹ hãy tiếp tục giữ tinh thần thoải mái, đảm bảo chế độ dinh dưỡng và nghỉ ngơi hợp lý. Vui lòng theo dõi các buổi khám thai định kỳ theo lịch hẹn của bác sĩ để kiểm tra các chỉ số tổng quát khác.
        """
    elif 70 < prediction_value <= 90:
        result = "Nghi ngờ"
        color = "orange"
        advice = f"""
            **Điều này có nghĩa là có một số thay đổi nhỏ cần được chú ý,** mặc dù chưa phải là tình trạng bệnh lý cấp bách. 
            **KHUYẾN CÁO:** Mẹ không cần quá lo lắng nhưng cần **tái khám hoặc làm thêm các xét nghiệm chuyên sâu** theo chỉ định của bác sĩ để xác nhận lại tình trạng sức khỏe của bé. Tiếp tục theo dõi cử động thai và giữ liên lạc với chuyên viên y tế.
        """
    else: # > 90
        result = "Nguy hiểm"
        color = "red"
        advice = f"""
            **Điều này đồng nghĩa với việc các chỉ số có dấu hiệu bất thường nghiêm trọng** và cần được can thiệp y tế ngay lập tức. 
            **HÀNH ĐỘNG KHẨN CẤP:** Mẹ cần đến cơ sở y tế gần nhất **ngay lập tức** để được các bác sĩ chuyên khoa thăm khám trực tiếp, đánh giá lâm sàng và có phương án xử lý kịp thời, đảm bảo an toàn tối đa cho cả mẹ và bé.
        """
    return result, color, advice

# --- Khởi tạo Trạng thái (Session State) ---

def init_session_state():
    """Khởi tạo các biến trạng thái cần thiết."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""
        
    # Dữ liệu hồ sơ
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = {
            'ho_ten': 'Người dùng',
            'email_sdt': 'chua_cap_nhat@app.com',
            'tuoi': 25,
            'chieu_cao': 160,
            'can_nang': 55.0,
            'tien_su_benh': 'Không',
            'thuoc_su_dung': ['Vitamin tổng hợp', 'Sắt/Axit Folic'],
            'lan_sinh_thu': 1,
            'ngay_du_sinh': datetime.date.today() + datetime.timedelta(days=120), # Giả lập còn 120 ngày
            'tuan_thai_hien_tai': 23,
        }

    # Lịch sử chẩn đoán
    if 'diagnosis_history' not in st.session_state:
        st.session_state.diagnosis_history = pd.DataFrame(columns=[
            'Ngày - Giờ', 'Kết quả sơ bộ', 'Mức độ', 'Chỉ số cụ thể (Ẩn)', 'Ghi chú'
        ])


# --- Hàm chuyển đổi trang ---
def navigate_to(page):
    """Chuyển đổi giữa các trang chính."""
    st.session_state.current_page = page
    # st.experimental_rerun() # Không cần dùng rerun nếu dùng sidebar button

# --- Các trang chức năng ---

def login_page():
    """Màn hình chào mừng và đăng nhập."""
    
    st.markdown(f'<div class="main-content-box" style="width: 350px; margin: auto; padding: 40px; text-align: center;">', unsafe_allow_html=True)
    st.markdown(f"## Chào mừng bạn quay trở lại!", unsafe_allow_html=True)
    st.markdown("---")
    
    # Sử dụng form để tạo nhóm input và button
    with st.form("login_form", clear_on_submit=False):
        # Email/SĐT
        email = st.text_input("Email hoặc số điện thoại", key="email_input", placeholder="Nhập email hoặc số điện thoại")
        
        # Mật khẩu (Không có chi tiết mắt cạnh mật khẩu trong Streamlit cơ bản, dùng type="password")
        password = st.text_input("Mật khẩu", type="password", key="password_input", placeholder="Nhập mật khẩu") 

        st.markdown(
            f"""
            <div style="font-size: 14px; text-align: right; margin-bottom: 20px;">
                <a href="#" style="color: {COLOR_DARK_BLUE};">Quên mật khẩu?</a>
            </div>
            """, 
            unsafe_allow_html=True
        )

        login_button = st.form_submit_button("Đăng nhập", type="primary", use_container_width=True)

    if login_button:
        if email and password:
            # Giả lập đăng nhập thành công
            st.session_state.logged_in = True
            st.session_state.user_id = email
            st.session_state.profile_data['email_sdt'] = email
            navigate_to("home")
            st.experimental_rerun()
        else:
            st.error("Vui lòng nhập đầy đủ Email/SĐT và Mật khẩu.")

    st.markdown("<hr style='border: 1px solid #ccc; margin-top: 20px;'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 14px;'>Hoặc tiếp tục với</p>", unsafe_allow_html=True)
    
    # Giả lập các nút đăng nhập khác (không dùng icon theo yêu cầu)
    col_x, col_y = st.columns([1, 1])
    with col_x:
         st.button("Tạm thời bỏ qua", key="skip_login", use_container_width=True)
    with col_y:
        # Nút tạo tài khoản mới (làm rõ lên)
        if st.button("Tạo Tài Khoản Mới", key="create_account_btn", use_container_width=True):
            st.info("Chức năng tạo tài khoản mới đang được phát triển.")

    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 30px; font-size: 14px;">
            <span style="margin-right: 15px;"><a href="#" style="color: {COLOR_DARK_BLUE};">Hỗ trợ</a></span>
            <span style="margin-right: 15px;"><a href="#" style="color: {COLOR_DARK_BLUE};">Chính sách bảo mật</a></span>
            <span><a href="#" style="color: {COLOR_DARK_BLUE};">Điều khoản sử dụng</a></span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)


def home_page():
    """Trang chủ bao gồm các hồ sơ mẹ, bé và điện tim."""
    st.title("Trang Chủ")
    st.markdown("---")

    st.header(f"Tuần Thai Hiện Tại: <span style='color: {COLOR_DARK_PINK}; font-weight: 700;'>Tuần {st.session_state.profile_data.get('tuan_thai_hien_tai', 0)}</span>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Hồ sơ Mẹ", "Hồ sơ Bé", "Chẩn đoán Điện Tim"])

    # 1. Hồ sơ Mẹ
    with tab1:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("Cập nhật Hồ sơ Mẹ")
        
        with st.form("mother_profile_form"):
            col_a, col_b = st.columns(2)
            temp_data = st.session_state.profile_data

            with col_a:
                ho_ten = st.text_input("Họ và Tên", value=temp_data['ho_ten'])
                chieu_cao = st.number_input("Chiều cao (cm)", min_value=100, max_value=250, value=temp_data['chieu_cao'], step=1)
                tien_su_benh = st.text_area("Tiền sử bệnh", value=temp_data['tien_su_benh'], height=100)

            with col_b:
                tuoi = st.number_input("Tuổi", min_value=15, max_value=60, value=temp_data['tuoi'], step=1)
                can_nang = st.number_input("Cân nặng hiện tại (kg)", min_value=30.0, max_value=200.0, value=temp_data['can_nang'], step=0.1)
                
                # Hiển thị nhật ký thuốc dưới dạng text area (nhưng cho phép chỉnh sửa bằng form)
                meds_text = st.text_area(
                    "Thuốc đang sử dụng (nhập cách nhau bằng dấu phẩy)", 
                    value=", ".join(temp_data['thuoc_su_dung']), 
                    height=100
                )
            
            submitted_mother = st.form_submit_button("Lưu Hồ Sơ Mẹ", type="primary")

            if submitted_mother:
                # Cập nhật dữ liệu vào session state
                st.session_state.profile_data.update({
                    'ho_ten': ho_ten,
                    'tuoi': tuoi,
                    'chieu_cao': chieu_cao,
                    'can_nang': can_nang,
                    'tien_su_benh': tien_su_benh,
                    'thuoc_su_dung': [m.strip() for m in meds_text.split(',')]
                })
                st.success("Đã lưu Hồ sơ Mẹ thành công!")
                st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)


    # 2. Hồ sơ Bé
    with tab2:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("Thông tin Thai kỳ và Hồ sơ Bé")

        with st.form("baby_profile_form"):
            col_c, col_d = st.columns(2)
            temp_data = st.session_state.profile_data

            with col_c:
                lan_sinh_thu = st.number_input("Lần sinh thứ", min_value=1, max_value=10, value=temp_data['lan_sinh_thu'], step=1)
                
                # Tính tuần thai tự động
                today = datetime.date.today()
                ngay_du_sinh_hien_tai = temp_data['ngay_du_sinh']
                
                # Lấy ngày dự sinh từ input
                ngay_du_sinh_moi = st.date_input("Ngày dự sinh (Dự kiến)", value=ngay_du_sinh_hien_tai)

                # Tính toán lại tuần thai
                if ngay_du_sinh_moi:
                    days_remaining = (ngay_du_sinh_moi - today).days
                    total_days = 40 * 7 # Giả định thai kỳ 40 tuần
                    days_passed = total_days - days_remaining
                    tuan_thai_hien_tai = max(0, min(40, days_passed // 7))
                    
                    st.session_state.profile_data['tuan_thai_hien_tai'] = tuan_thai_hien_tai
                    st.markdown(f"**Tuần thai hiện tại (Tự tính):** <span style='color: {COLOR_DARK_PINK}; font-size: 20px; font-weight: 700;'>Tuần {tuan_thai_hien_tai}</span>", unsafe_allow_html=True)
                
            with col_d:
                # Cân nặng ước tính theo tuần thai (Giả lập theo công thức đơn giản)
                weight_estimate = tuan_thai_hien_tai * 100 + 500 # Tăng 100g mỗi tuần + 500g ban đầu
                st.markdown(f"**Cân nặng ước tính:** <span style='color: {COLOR_DARK_BLUE}; font-size: 20px; font-weight: 700;'>{weight_estimate/1000:.2f} kg</span>", unsafe_allow_html=True)
                
                # Mục này chỉ hiển thị, không cho chỉnh sửa trực tiếp
                st.markdown("**Các mốc phát triển quan trọng:** (Tự động theo Tuần)")
                if tuan_thai_hien_tai < 12:
                    st.info("Giai đoạn hình thành cơ quan.")
                elif tuan_thai_hien_tai < 28:
                    st.info("Giai đoạn phát triển chiều dài và cân nặng.")
                else:
                    st.info("Giai đoạn hoàn thiện phổi và tăng tốc cân nặng.")


            submitted_baby = st.form_submit_button("Lưu Hồ Sơ Bé", type="primary")

            if submitted_baby:
                st.session_state.profile_data.update({
                    'lan_sinh_thu': lan_sinh_thu,
                    'ngay_du_sinh': ngay_du_sinh_moi,
                })
                st.success("Đã lưu Hồ sơ Bé thành công!")
                st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # 3. Chẩn đoán Điện Tim
    with tab3:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("B. Chẩn đoán sơ bộ bằng AI")
        st.info("Đây là công cụ hỗ trợ. Kết quả cuối cùng phải dựa trên đánh giá của bác sĩ.")
        
        # --- Mục Tải Dữ liệu ---
        st.markdown("#### 1. Tải Dữ liệu (File ECG/CTG)")
        ecg_data = st.file_uploader("Tải lên file dữ liệu (Ví dụ: .csv, .txt)", type=['txt', 'csv'])
        
        # --- Mục Nhập Dữ liệu tùy chỉnh ---
        st.markdown("#### 2. Nhập Dữ liệu Tùy chỉnh (21 Chỉ số CTG)")
        
        # Tạo nút để hiện/ẩn form nhập dữ liệu
        if 'show_input_form' not in st.session_state:
            st.session_state.show_input_form = False
            
        if st.button("Nhấp vào đây để Nhập 21 Chỉ Số", key="toggle_input"):
            st.session_state.show_input_form = not st.session_state.show_input_form

        input_data = {}

        if st.session_state.show_input_form:
            with st.form("manual_input_form"):
                cols = st.columns(3)
                for i, feature in enumerate(MODEL_FEATURE_NAMES):
                    with cols[i % 3]:
                        # Giả lập nhập liệu với giá trị mặc định để dễ test
                        default_val = 120.0 if "Baseline" in feature else (0.5 if "%" in feature else 0.0)
                        input_data[feature] = st.number_input(feature, value=default_val, step=0.1, key=f"input_{i}")

                ghi_chu = st.text_area("Ghi chú của mẹ về lần đo/kiểm tra này", value="")
                
                submitted_diagnosis = st.form_submit_button("Gửi Dữ Liệu & Chẩn Đoán", type="primary")
                
                if submitted_diagnosis:
                    # Giả lập kết quả AI (random 50-100 để có cả 3 trường hợp)
                    # Giả sử: giá trị càng cao, nguy cơ càng lớn
                    mock_prediction = np.random.randint(50, 101) 
                    
                    # 1. Lấy kết quả chẩn đoán và lời khuyên
                    result, color, advice = get_diagnosis_result(mock_prediction)
                    
                    # 2. Chuẩn bị dữ liệu để lưu
                    diagnosis_details = "\n".join([f"{k}: {v}" for k, v in input_data.items()])
                    
                    new_diagnosis = {
                        'Ngày - Giờ': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'Kết quả sơ bộ': result,
                        'Mức độ': mock_prediction,
                        'Chỉ số cụ thể (Ẩn)': diagnosis_details,
                        'Ghi chú': ghi_chu if ghi_chu else 'Không có'
                    }
                    
                    # Lưu vào Lịch sử (Session State)
                    new_df = pd.DataFrame([new_diagnosis])
                    st.session_state.diagnosis_history = pd.concat([st.session_state.diagnosis_history, new_df], ignore_index=True)
                    
                    st.success("Đã gửi dữ liệu và nhận kết quả chẩn đoán!")
                    st.session_state.last_diagnosis_result = {'result': result, 'color': color, 'advice': advice, 'time': new_diagnosis['Ngày - Giờ']}
                    
                    # Tắt form nhập liệu
                    st.session_state.show_input_form = False
                    st.experimental_rerun()
        
        # --- Mục Hiển thị Kết quả Chẩn đoán ---
        if 'last_diagnosis_result' in st.session_state:
            res = st.session_state.last_diagnosis_result
            
            st.markdown(f"#### 3. Kết Quả Chẩn Đoán Sơ Bộ ({res['time']})")
            
            # Khung kết quả chẩn đoán to rõ ràng
            st.markdown(f'<div style="background-color: {COLOR_LIGHT_GRAY}; padding: 25px; border-radius: 12px; border: 2px solid {res["color"]};">', unsafe_allow_html=True)
            
            st.markdown(f"**<span style='color: {COLOR_DARK_BLUE}; font-size: 24px;'>Kết quả chẩn đoán:</span>**", unsafe_allow_html=True)
            st.markdown(f"### <span style='color: {res['color']}; font-weight: 800;'>{res['result'].upper()}</span>", unsafe_allow_html=True)
            
            st.markdown(f"<p style='color: {COLOR_DARK_BLUE};'>Các chỉ số cho thấy:</p>", unsafe_allow_html=True)
            
            st.markdown(f"<p style='color: {COLOR_DARK_BLUE}; font-weight: 500;'>{res['advice']}</p>", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)


        st.markdown('</div>', unsafe_allow_html=True)


def handbook_page():
    """Sổ tay cá nhân: Lịch sử theo dõi, Nhật kí thuốc, Mẹo thai kì."""
    st.title("Sổ Tay Cá Nhân")
    st.markdown("---")

    tab1, tab2 = st.tabs(["Lịch sử - Theo dõi", "Mẹo Chăm sóc Thai kì"])

    # 1. Lịch sử - Theo dõi
    with tab1:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("1. Lịch sử Chẩn đoán & Theo dõi")
        
        history_df = st.session_state.diagnosis_history.sort_values(by='Ngày - Giờ', ascending=False).reset_index(drop=True)
        
        if history_df.empty:
            st.info("Chưa có lịch sử chẩn đoán nào được lưu.")
        else:
            for index, row in history_df.iterrows():
                result, color, _ = get_diagnosis_result(row['Mức độ'])
                
                with st.expander(f"Lần chẩn đoán: {row['Ngày - Giờ']} - Kết quả: **{result}**"):
                    st.write(f"**Ngày - Giờ chẩn đoán:** {row['Ngày - Giờ']}")
                    
                    st.markdown(f"**Kết quả sơ bộ:** <span style='color: {color}; font-weight: 600;'>{result}</span>", unsafe_allow_html=True)
                    
                    # Chỉ số cụ thể (tạm thời ẩn, khi click sẽ hiện ra)
                    with st.expander("Xem Chỉ số Cụ thể (21 chỉ số)"):
                        st.text_area("Chỉ số chi tiết:", value=row['Chỉ số cụ thể (Ẩn)'], height=150, disabled=True)
                        
                    st.write(f"**Ghi chú:** {row['Ghi chú']}")

        st.markdown("---")
        
        st.subheader("2. Nhật ký Thuốc")
        
        current_meds = st.session_state.profile_data['thuoc_su_dung']

        st.markdown("#####Danh sách thuốc đã nhập:")
        
        # Chỉ hiển thị các mục không rỗng
        display_meds = [m for m in current_meds if m]
        
        if display_meds:
            for med in display_meds:
                st.markdown(f"- <span style='color: {COLOR_DARK_BLUE}; font-weight: 500;'>{med}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"*Chưa có thuốc nào được nhập.*", unsafe_allow_html=True)
            
        st.markdown("---")
        
        st.markdown("##### Thêm thuốc/thực phẩm chức năng mới")
        with st.form("add_med_form", clear_on_submit=True):
            new_med = st.text_input("Tên thuốc/TPCN mới", key="new_med_input")
            if st.form_submit_button("+ Thêm", type="primary", key="add_med_btn"):
                if new_med and new_med.strip() not in current_meds:
                    st.session_state.profile_data['thuoc_su_dung'].append(new_med.strip())
                    st.success(f"Đã thêm '{new_med.strip()}' vào nhật ký.")
                    st.experimental_rerun()
                elif new_med.strip() in current_meds:
                     st.warning("Thuốc này đã có trong danh sách.")
                else:
                    st.error("Vui lòng nhập tên thuốc.")

        st.markdown('</div>', unsafe_allow_html=True)


    # 2. Mẹo Chăm sóc Thai kì (Thông tin tĩnh)
    with tab2:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("💡 Mẹo Chăm sóc Thai kì")
        
        st.markdown(f"#### 1. Hướng dẫn mẹ theo dõi thai kì hiệu quả", unsafe_allow_html=True)
        st.info(
            "Việc theo dõi thai kỳ cần được thực hiện đều đặn. Mẹ nên ghi chép lại mọi thay đổi của cơ thể, các chỉ số đo được và lịch sử tiêm chủng/khám thai. Hãy chuẩn bị tâm lý thoải mái, tham gia các lớp học tiền sản và luôn sẵn sàng trao đổi với bác sĩ về mọi lo lắng của mình. **Đừng quên theo dõi cử động của bé mỗi ngày.**"
        )

        st.markdown(f"#### 2. Dinh dưỡng và Bài tập", unsafe_allow_html=True)
        col_e, col_f = st.columns(2)
        
        with col_e:
            st.markdown("**Dinh Dưỡng Đề Xuất:**", unsafe_allow_html=True)
            st.markdown(f"""
                - **Sắt và Axit Folic:** Rất quan trọng trong 3 tháng đầu.
                - **Canxi:** Sữa, sữa chua, phô mai.
                - **Protein và Chất Xơ:** Thịt nạc, cá, trứng và các loại hạt.
            """)
            
        with col_f:
            st.markdown("**Bài Tập Sức Khỏe:**", unsafe_allow_html=True)
            st.markdown(f"""
                - **Đi bộ:** 30 phút mỗi ngày.
                - **Bơi lội:** Giảm áp lực lên khớp.
                - **Yoga/Pilates:** Các bài tập nhẹ nhàng, chuyên biệt cho bà bầu.
            """)
        
        st.markdown(f"#### 3. Massage Cơ Thể", unsafe_allow_html=True)
        st.caption("Massage giúp giảm sưng phù và thư giãn tinh thần.")
        st.markdown(f"""
            - **Chân và Bàn chân:** Giúp lưu thông máu.
            - **Vùng lưng dưới:** Giảm đau lưng.
            - **Vai và Cổ:** Thư giãn cơ.
        """)
        
        st.markdown('</div>', unsafe_allow_html=True)


def settings_page():
    """Cài đặt: Thông tin tài khoản, thay đổi mật khẩu, Dấu hiệu cảnh báo."""
    st.title("Cài Đặt")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Thông tin Tài khoản", "Dấu hiệu Cảnh báo"])

    with tab1:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("Thông tin Tài khoản")
        
        st.markdown(f"**Tên tài khoản:** <span style='color: {COLOR_DARK_BLUE};'>{st.session_state.profile_data.get('ho_ten', 'Người dùng')}</span>", unsafe_allow_html=True)
        st.markdown(f"**Email/Số điện thoại:** <span style='color: {COLOR_DARK_BLUE};'>{st.session_state.user_id}</span>", unsafe_allow_html=True)
        
        st.markdown("---")

        with st.form("settings_form"):
            st.markdown("##### Thay đổi Mật khẩu")
            mk_cu = st.text_input("Mật khẩu cũ", type="password")
            mk_moi = st.text_input("Mật khẩu mới", type="password")
            xac_nhan_mk_moi = st.text_input("Xác nhận Mật khẩu mới", type="password")
            
            col_g, col_h = st.columns([1, 2])
            
            with col_g:
                if st.form_submit_button("Lưu Thay Đổi", type="primary"):
                    if mk_moi == xac_nhan_mk_moi and len(mk_moi) > 5:
                        st.success("Đã thay đổi mật khẩu thành công (Giả lập).")
                    else:
                        st.error("Mật khẩu mới không khớp hoặc quá ngắn.")
            
            with col_h:
                if st.button("Đăng Xuất", key="logout_btn"):
                    st.session_state.logged_in = False
                    st.session_state.current_page = "login"
                    st.experimental_rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("Dấu hiệu Cảnh báo nguy hiểm")
        st.warning("Đây là các dấu hiệu cần được quan tâm đặc biệt.")
        
        st.markdown(f"""
        <ul style="color: {COLOR_DARK_BLUE}; font-weight: 500; padding-left: 20px;">
            <li>Chảy máu âm đạo bất thường (nhiều hoặc đỏ tươi).</li>
            <li>Đau bụng dưới dữ dội, co thắt liên tục.</li>
            <li>Sốt cao (trên 38.5°C) không rõ nguyên nhân.</li>
            <li>Phù nề nghiêm trọng ở mặt, tay chân kèm theo tăng huyết áp.</li>
            <li>Giảm hoặc mất hoàn toàn cử động thai (sau tuần thứ 28).</li>
            <li>Nôn mửa kéo dài không kiểm soát được.</li>
        </ul>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"<p style='color: {COLOR_DARK_PINK}; font-weight: 700;'>Khi xuất hiện các dấu hiệu bất thường này, mẹ nên liên hệ người nhà và đưa đến cơ sở y tế gần nhất NGAY LẬP TỨC để được các bác sĩ chuyên khoa thăm khám trực tiếp.</p>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)


# --- Chạy ứng dụng chính ---
def main():
    """Hàm chính điều khiển luồng ứng dụng."""
    
    # 1. Khởi tạo
    init_session_state()
    st.set_page_config(page_title="App Theo Dõi Thai Kỳ (Mẹ & Bé)", layout="wide")
    apply_custom_css()

    # 2. Xử lý logic đăng nhập
    if not st.session_state.logged_in:
        login_page()
        return

    # 3. Thanh điều hướng (Sidebar)
    st.sidebar.title("Menu Ứng Dụng")
    st.sidebar.markdown(f"**Tài khoản:** *{st.session_state.profile_data['ho_ten']}*")
    st.sidebar.markdown("---")
    
    nav_options = {
        "home": "Trang Chủ",
        "handbook": "Sổ Tay Cá Nhân",
        "settings": "Cài Đặt"
    }
    
    # Sử dụng radio/select box để tạo hiệu ứng chọn trang tốt hơn trong Streamlit
    selected_page = st.sidebar.radio(
        "Chọn Trang", 
        options=list(nav_options.keys()), 
        format_func=lambda x: nav_options[x],
        index=list(nav_options.keys()).index(st.session_state.current_page)
    )
    
    # Cập nhật trang khi chọn
    st.session_state.current_page = selected_page
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Đăng Xuất", key="sidebar_logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.current_page = "login"
        st.experimental_rerun()

    # 4. Hiển thị trang hiện tại
    page_functions = {
        "home": home_page,
        "handbook": handbook_page,
        "settings": settings_page,
    }
    
    page_functions[st.session_state.current_page]()

if __name__ == '__main__':
    main()
