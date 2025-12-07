import streamlit as st
import pandas as pd
import time

# --- 1. CONFIGURATION AND AESTHETICS (Tông màu Pastel theo yêu cầu) ---

# Tông màu Pastel: Xanh dương, Hồng, Be
COLOR_BEIGE = '#F8F8F0'    # Nền chính (Gần như trắng/be nhạt)
COLOR_LIGHT_BLUE = '#A9D6E5' # Xanh pastel nhạt (cho nút/nền phụ)
COLOR_LIGHT_PINK = '#FFB8C1' # Hồng pastel nhạt (cho điểm nhấn/nền phụ)
COLOR_DARK_BLUE = '#1B4965'  # Xanh đậm (cho chữ/tiêu đề)
COLOR_DARK_PINK = '#C06C84'  # Hồng đậm (cho chữ/điểm nhấn chính)

# --- Custom CSS (Đảm bảo giao diện sang trọng, không icon, dễ nhìn) ---
custom_css = f"""
<style>
    /* Nền chung của ứng dụng */
    .stApp {{
        background-color: {COLOR_BEIGE};
        font-family: 'Inter', sans-serif;
    }}

    /* Tiêu đề chính và các thẻ Header */
    h1, h2, h3 {{
        color: {COLOR_DARK_BLUE};
        font-weight: 700;
    }}

    /* Container chính (Làm giao diện đăng nhập nổi bật) */
    .login-container {{
        max-width: 400px;
        margin: 50px auto;
        padding: 30px;
        background-color: white;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        text-align: center;
    }}

    /* Input Fields */
    .stTextInput input[type="text"], .stTextInput input[type="password"], .stTextInput input[type="number"], .stTextArea textarea {{
        border-radius: 10px;
        border: 1px solid {COLOR_LIGHT_BLUE};
        padding: 12px 15px;
        box-shadow: none;
    }}
    
    /* Nút Đăng nhập/Chính (Lấy màu Xanh pastel làm chủ đạo) */
    .stButton > button {{
        background-color: {COLOR_LIGHT_BLUE};
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 600;
        border: none;
        transition: all 0.2s;
    }}
    .stButton > button:hover {{
        background-color: {COLOR_DARK_BLUE};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }}

    /* Nút Lưu (Save) - Quan trọng, dùng màu Hồng/Hồng đậm */
    button[kind="primary"] {{
        background-color: {COLOR_DARK_PINK} !important;
        border: 1px solid {COLOR_DARK_PINK} !important;
        color: white !important;
    }}
    button[kind="primary"]:hover {{
        background-color: {COLOR_LIGHT_PINK} !important; /* Đã sửa lỗi: Dùng biến có sẵn */
        border: 1px solid {COLOR_DARK_PINK} !important;
        color: {COLOR_DARK_BLUE} !important;
    }}

    /* Nút Tạo Tài Khoản Mới (góc trên) */
    .new-account-btn {{
        color: {COLOR_DARK_PINK};
        font-weight: 600;
        text-decoration: none;
        padding: 5px;
        transition: color 0.2s;
    }}
    .new-account-btn:hover {{
        color: {COLOR_DARK_BLUE};
    }}

    /* Sidebar Navigation (Dùng màu xanh/hồng pastel cho các mục) */
    .stRadio > label {{
        padding: 8px 10px;
        margin: 3px 0;
        border-radius: 6px;
        color: {COLOR_DARK_BLUE};
        transition: all 0.2s;
    }}
    .stRadio div[role="radiogroup"] > label:has(input:checked) {{
        background-color: {COLOR_LIGHT_PINK};
        color: {COLOR_DARK_BLUE};
        font-weight: bold;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)
st.set_page_config(page_title="Fetal ECG App", layout="wide", initial_sidebar_state="auto")

# --- 2. STATE MANAGEMENT (Quản lý trạng thái đăng nhập và trang) ---

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Đăng nhập'
if 'username' not in st.session_state:
    st.session_state.username = "Mẹ"

# Dữ liệu mẫu (mock) cho 21 chỉ số CTG/FHR
CTG_FEATURES = [
    "BaseLine Value (bpm)", "Accel Time (msec)", "Movements", "Uterine Contractions",
    "Light Decels", "Severe Decels", "Prolong Decels", "Abnormal Short Term Var (%)",
    "Mean Short Term Var", "Abnormal Long Term Var (%)", "Mean Long Term Var", 
    "Width of Histogram", "Min of Histogram", "Max of Histogram", "Num of Peaks",
    "Num of Zeros", "Mode of Histogram", "Mean of Histogram", "Median of Histogram",
    "Variance of Histogram", "Tendency of Histogram"
]


# --- 3. PAGE FUNCTIONS (Các Hàm cho từng màn hình) ---

def login_page():
    """Màn hình Đăng nhập (Theo cấu trúc hình ảnh tham khảo)"""
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Góc trên bên phải: Tạo Tài Khoản Mới
    st.markdown(
        f'<div style="text-align: right; position: absolute; top: 15px; right: 15px;">'
        f'<a href="#" class="new-account-btn">Tạo tài khoản mới</a>'
        f'</div>', unsafe_allow_html=True
    )
    
    st.image("https://placehold.co/100x20/F5F5DC/F5F5DC", use_column_width=True) # Tạo khoảng trống
    st.markdown('<h2 style="text-align: center;">Chào mừng bạn quay trở lại!</h2>', unsafe_allow_html=True)
    
    # Form Đăng nhập
    with st.form("login_form"):
        email_sdt = st.text_input("Email hoặc số điện thoại", placeholder="Nhập email hoặc số điện thoại")
        
        # Mật khẩu (Có chi tiết mắt)
        # Streamlit không hỗ trợ icon mắt trực tiếp. Dùng text input type="password" là cách mô phỏng gần nhất.
        password = st.text_input("Mật khẩu", placeholder="Nhập mật khẩu", type="password")
        
        st.markdown(
            '<div style="text-align: right; margin-top: -10px; margin-bottom: 20px; font-size: 0.9em;">'
            '<a href="#" style="color: #6C757D;">Quên mật khẩu?</a>'
            '</div>', unsafe_allow_html=True
        )
        
        submitted = st.form_submit_button("Đăng nhập")

        if submitted:
            # Logic đăng nhập giả định (luôn thành công)
            if email_sdt and password:
                # Dùng time.sleep để mô phỏng độ trễ đăng nhập
                with st.spinner('Đang xác thực...'):
                    time.sleep(1)
                    
                st.session_state.logged_in = True
                st.session_state.current_page = 'Trang chủ'
                st.session_state.username = email_sdt.split('@')[0] if '@' in email_sdt else "Mẹ Bầu"
                st.rerun()
            else:
                st.error("Vui lòng nhập đầy đủ thông tin.")
    
    st.markdown('<div style="margin-top: 30px; text-align: center; color: #6C757D;">Hoặc tiếp tục với</div>', unsafe_allow_html=True)
    
    # Nút đăng nhập phụ
    col_social1, col_social2 = st.columns(2)
    with col_social1:
        st.button("Google", use_container_width=True, key="google_login")
    with col_social2:
        st.button("Apple ID", use_container_width=True, key="apple_login")

    st.markdown("---")
    
    # Chính sách
    st.markdown(
        '<div style="text-align: center; font-size: 0.8em; margin-top: 15px;">'
        '<a href="#" style="margin-right: 15px; color: #6C757D;">Hỗ trợ</a>'
        '<a href="#" style="margin-right: 15px; color: #6C757D;">Chính sách bảo mật</a>'
        '<a href="#" style="color: #6C757D;">Điều khoản sử dụng</a>'
        '</div>', unsafe_allow_html=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)


def sidebar_navigation():
    """Thanh Sidebar (chỉ hiện khi đã đăng nhập)"""
    st.sidebar.title("Theo Dõi Thai Nhi") # Đã bỏ icon theo yêu cầu
    st.sidebar.markdown(f"**Chào mừng, {st.session_state.username}!**")
    st.sidebar.markdown("---")

    # Navigation
    page_options = ('Trang chủ', 'Sổ tay cá nhân', 'Cài đặt')
    current_page = st.sidebar.radio(
        "Chọn mục:",
        page_options,
        index=page_options.index(st.session_state.current_page),
        key='app_nav_radio'
    )
    st.session_state.current_page = current_page
    
    st.sidebar.markdown("---")
    if st.sidebar.button("Đăng xuất", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.current_page = 'Đăng nhập'
        st.rerun()

def home_page():
    """Trang Chủ với 3 Hồ sơ chính"""
    st.title("Trang Chủ")

    col1, col2, col3 = st.columns(3)

    # --- 1. HỒ SƠ MẸ ---
    with col1:
        st.subheader("Hồ sơ mẹ")
        with st.container(border=True):
            st.text_input("Họ và tên", value="Nguyễn Thị A")
            st.number_input("Tuổi", min_value=15, max_value=50, value=28)
            st.number_input("Chiều cao (cm)", min_value=100.0, value=158.0, step=0.1)
            st.number_input("Cân nặng (kg)", min_value=30.0, value=55.0, step=0.1)
            st.text_area("Tiền sử bệnh", value="Tiểu đường thai kỳ (Kiểm soát tốt)")
            st.text_area("Thuốc đang sử dụng", value="Vitamin tổng hợp, Folic Acid", key="mother_meds")
            
            # Nút Lưu BẮT BUỘT (Dùng key khác để tránh xung đột)
            st.button("Lưu Hồ sơ mẹ", key="save_mother", type="primary", use_container_width=True)

    # --- 2. HỒ SƠ BÉ ---
    with col2:
        st.subheader("Hồ sơ bé")
        with st.container(border=True):
            st.selectbox("Lần sinh thứ", options=['Lần 1', 'Lần 2', 'Lần 3+'], index=0)
            
            # Tính Tuần thai tự động (Mock)
            due_date = st.date_input("Ngày dự sinh", value=pd.to_datetime('2026-03-01'), key="due_date")
            today = pd.to_datetime('2025-12-08')
            days_to_due = (due_date - today).days
            # Giả sử thai đủ tháng là 280 ngày (40 tuần)
            
            if days_to_due >= 0:
                days_since_start = 280 - days_to_due
                current_week = days_since_start / 7
            else:
                current_week = 40 # Thai đã quá ngày dự sinh
            
            st.markdown(f"**Tuần thai hiện tại:** **{int(current_week)} tuần**")
            
            st.number_input("Cân nặng ước tính (gram)", min_value=100.0, value=1500.0, step=10.0)
            
            # Nút Lưu BẮT BUỘC
            st.button("Lưu Hồ sơ bé", key="save_baby", type="primary", use_container_width=True)


    # --- 3. HỒ SƠ ĐO ĐIỆN TIM VÀ CHẨN ĐOÁN (Chức năng cốt lõi) ---
    with col3:
        st.subheader("Hồ sơ đo điện tim")
        with st.container(border=True):
            st.markdown("##### Tải Dữ Liệu")
            uploaded_file = st.file_uploader("Tải file CTG (.csv) từ máy cá nhân lên:", type=['csv'])

            st.markdown("##### Nhập Dữ Liệu Tùy Chỉnh")
            
            # Dùng st.expander để ẩn/hiện bảng nhập 21 chỉ số
            with st.expander("Nhập 21 Chỉ Số Điện Tim Thai (CTG)", expanded=False):
                col_i1, col_i2, col_i3 = st.columns(3)
                input_data = {}
                
                for i, feature in enumerate(CTG_FEATURES):
                    col = [col_i1, col_i2, col_i3][i % 3]
                    with col:
                        # Giao diện trực quan
                        # Dùng key khác nhau cho mỗi input
                        input_data[feature] = st.number_input(
                            f"{i+1}. {feature}", 
                            min_value=0.0, 
                            value=140.0 if i == 0 else (0.5 if i == 8 else 0.0), 
                            step=0.1,
                            key=f"input_ctg_{i}"
                        )

            # Nút Lưu BẮT BUỘC cho phần nhập liệu
            if st.button("Lưu và Chẩn Đoán", key="diagnose_save", type="primary", use_container_width=True):
                # Giả định chẩn đoán thành công (Dùng Random để mô phỏng)
                import random
                result_options = ["Bình thường", "Nghi ngờ", "Nguy hiểm"]
                diagnosis_result = random.choice(result_options)
                
                # Lưu vào session state để hiển thị
                st.session_state.diagnosis = diagnosis_result
                st.session_state.diagnosis_time = pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%S")

            if 'diagnosis' in st.session_state:
                display_diagnosis_result(st.session_state.diagnosis, st.session_state.diagnosis_time)


def display_diagnosis_result(result, diagnosis_time):
    """Hiển thị Khung Kết Quả Chẩn Đoán với lời nhận xét tùy chỉnh."""
    
    if result == "Bình thường":
        color_box = COLOR_LIGHT_BLUE
        color_text = COLOR_DARK_BLUE
        advice = "Đây là một tín hiệu rất tích cực. Mẹ hãy tiếp tục giữ tinh thần thoải mái, đảm bảo chế độ dinh dưỡng và nghỉ ngơi hợp lý. Vui lòng theo dõi các buổi khám thai định kỳ theo lịch hẹn của bác sĩ để kiểm tra các chỉ số tổng quát khác."
    elif result == "Nghi ngờ":
        color_box = COLOR_LIGHT_PINK
        color_text = COLOR_DARK_PINK
        advice = "**Điều này có nghĩa là có một số thay đổi nhỏ cần được chú ý, mặc dù chưa phải là tình trạng bệnh lý cấp bách.** KHUYẾN CÁO: Mẹ không cần quá lo lắng nhưng cần **tái khám hoặc làm thêm các xét nghiệm chuyên sâu** theo chỉ định của bác sĩ để xác nhận lại tình trạng sức khỏe của bé. Tiếp tục theo dõi cử động thai và giữ liên lạc với chuyên viên y tế."
    else: # Nguy hiểm
        color_box = '#F7B7C6' # Màu đỏ nhạt hơn, gần hồng pastel
        color_text = '#B8325C' # Màu đỏ đậm/hồng đậm hơn cho Nguy hiểm
        advice = "**Điều này đồng nghĩa với việc các chỉ số có dấu hiệu bất thường nghiêm trọng và cần được can thiệp y tế ngay lập tức.** HÀNH ĐỘNG KHẨN CẤP: Mẹ cần đến cơ sở y tế gần nhất **ngay lập tức** để được các bác sĩ chuyên khoa thăm khám trực tiếp, đánh giá lâm sàng và có phương án xử lý kịp thời, đảm bảo an toàn tối đa cho cả mẹ và bé."

    st.markdown("---")
    
    # Khung Kết quả Chẩn đoán (Màu pastel, chữ to rõ)
    st.markdown(
        f'<div style="background-color: {color_box}; border-radius: 10px; padding: 20px; border: 2px solid {color_text}; margin-top: 10px;">'
        f'<h4 style="color: {color_text}; margin-top: 0px;">Kết quả chẩn đoán</h4>'
        f'<p style="color: {color_text}; font-size: 1.1em;">Các chỉ số cho thấy: <strong>{result}</strong></p>'
        f'<p style="font-size: 0.9em; margin-bottom: 0px;">*Thời gian: {diagnosis_time}</p>'
        f'<hr style="border-top: 1px solid {color_text}40;">'
        f'<p style="color: {color_text}; font-size: 0.95em;">{advice}</p>'
        f'</div>', 
        unsafe_allow_html=True
    )


def personal_log_page():
    """Sổ Tay Cá Nhân (Lịch sử theo dõi và Mẹo chăm sóc)"""
    st.title("Sổ Tay Cá Nhân")
    st.markdown("Phần này giúp mẹ theo dõi lịch sử chẩn đoán và các lời khuyên chăm sóc thai kỳ.")

    # --- Lịch sử theo dõi ---
    st.subheader("Lịch sử theo dõi")
    
    tab_history, tab_medicine = st.tabs(["Lịch sử chẩn đoán", "Nhật kí thuốc"])

    with tab_history:
        st.markdown("##### Lịch sử Chẩn Đoán")
        
        # Dữ liệu Lịch sử Chẩn đoán giả định
        history_df = pd.DataFrame({
            'Ngày - Giờ Chẩn đoán': ['07/12/2025 10:30', '30/11/2025 14:00', '21/11/2025 09:00'],
            'Kết quả sơ bộ': ['Bình thường', 'Nghi ngờ', 'Bình thường'],
            'Ghi chú': ['Không có', 'Cần uống nhiều nước hơn', 'Không có'],
        })
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        
        st.info("Click vào một dòng để xem chi tiết 21 chỉ số cụ thể.")
        
        with st.expander("Xem chi tiết các chỉ số (21 chỉ số)"):
            st.markdown("Tạm thời ẩn, sẽ hiện ra khi click vào một lần chẩn đoán cụ thể.")
            st.dataframe(pd.DataFrame({'Chỉ số': CTG_FEATURES, 'Giá trị': [145, 0, 0, 0, 0, 0, 0, 75, 0.5, 10, 5.0, 50, 120, 160, 5, 0, 145, 140, 145, 10, 0]}), hide_index=True)
            
        st.button("Lưu Ghi chú", key="save_history_note", type="primary") # Nút Lưu BẮT BUỘC

    with tab_medicine:
        st.markdown("##### Nhật Kí Thuốc")
        
        # Đồng bộ từ hồ sơ mẹ (nếu có)
        initial_meds = st.session_state.get('mother_meds', "Vitamin tổng hợp\nSắt/Folic Acid")
        if 'meds' not in st.session_state:
            st.session_state.meds = initial_meds
            
        st.session_state.meds = st.text_area("Danh sách thuốc đang sử dụng:", value=st.session_state.meds, height=150, key="current_meds_area")
        
        col_med_input, col_med_btn = st.columns([3, 1])
        with col_med_input:
            new_medicine = st.text_input("Thêm thuốc mới vào sổ tay:", key="new_med_input")
        with col_med_btn:
            # Dùng khoảng trống để căn nút
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("+ Thêm", key="add_medicine_btn"):
                if new_medicine:
                    st.session_state.meds += f"\n{new_medicine}"
                    st.success(f"Đã thêm: {new_medicine}")
                    st.rerun() # Refresh để cập nhật text area
        
        st.button("Lưu Nhật kí thuốc", key="save_medicine_log", type="primary", use_container_width=True) # Nút Lưu BẮT BUỘC

    # --- Mẹo Chăm Sóc Thai Kì ---
    st.subheader("Mẹo Chăm Sóc Thai Kì")
    
    # Hướng dẫn chung
    st.markdown("##### Hướng dẫn mẹ theo dõi thai kì hiệu quả")
    st.info("Hãy luôn giữ tâm lý thoải mái, theo dõi cử động thai nhi đều đặn và thăm khám định kỳ. Việc theo dõi thai kì cần được thực hiện trong môi trường yên tĩnh.")

    # Dinh dưỡng, bài tập
    st.markdown("##### Dinh dưỡng, bài tập & massage")
    col_advice1, col_advice2 = st.columns(2)
    with col_advice1:
        st.markdown("**Dinh Dưỡng Đề Xuất**")
        st.markdown("* Bổ sung Protein (trứng, thịt nạc).")
        st.markdown("* Ăn nhiều rau xanh và trái cây.")
        st.markdown("* Uống đủ 2 - 2.5 lít nước mỗi ngày.")
    with col_advice2:
        st.markdown("**Bài Tập & Massage**")
        st.markdown("* Yoga nhẹ nhàng cho bà bầu.")
        st.markdown("* Đi bộ 30 phút mỗi ngày.")
        st.markdown("* Massage lưng và chân để giảm đau nhức.")
        
    st.button("Lưu Lời khuyên", key="save_tips", type="primary", use_container_width=True) # Nút Lưu BẮT BUỘC


def settings_page():
    """Màn hình Cài Đặt"""
    st.title("Cài Đặt")

    # --- Thông tin Tài khoản ---
    st.subheader("Thông tin tài khoản")

    col_info1, col_info2 = st.columns([1, 2])
    
    with col_info1:
        st.markdown("##### Ảnh đại diện")
        # Placeholder cho ảnh đại diện (không dùng icon)
        st.image("https://placehold.co/150x150/FFB8C1/1B4965?text=Ảnh+ĐD", width=150)
        st.button("Thay đổi ảnh", key="change_pic_btn", type="secondary")

    with col_info2:
        st.text_input("User Name", value=st.session_state.username)
        st.text_input("Email", value="user@example.com", disabled=True)
        st.text_input("Số điện thoại", value="090-XXX-YYY")
        st.text_input("Thay đổi mật khẩu", type="password", help="Nhập mật khẩu mới")
        st.text_input("Xác nhận mật khẩu", type="password")
        
        st.checkbox("Bật thông báo chuông báo/rung", value=True)

    st.button("Lưu Cài đặt tài khoản", key="save_settings_acc", type="primary", use_container_width=True) # Nút Lưu BẮT BUỘC

    st.markdown("---")
    
    # --- Dấu hiệu Cảnh Báo ---
    st.subheader("Dấu hiệu cảnh báo")
    st.markdown("Đây là danh sách các dấu hiệu bất thường mẹ cần theo dõi:")
    
    warning_list = [
        "Chảy máu âm đạo bất thường (Màu đỏ tươi, lượng nhiều).",
        "Đau bụng dữ dội, co thắt liên tục (đặc biệt trước 37 tuần).",
        "Thai nhi cử động ít hơn hẳn so với bình thường.",
        "Rò rỉ hoặc vỡ nước ối.",
        "Sốt cao, đau đầu kéo dài hoặc thị lực kém."
    ]
    
    for item in warning_list:
        st.markdown(f"- {item}")
        
    st.markdown(
        f'<div style="background-color: {COLOR_LIGHT_PINK}30; padding: 15px; border-left: 5px solid {COLOR_DARK_PINK}; border-radius: 5px; margin-top: 15px;">'
        f'<p style="color: {COLOR_DARK_PINK}; font-weight: 600; margin-bottom: 0px;">'
        f'🚨 HÀNH ĐỘNG KHẨN CẤP: Khi xuất hiện các dấu hiệu bất thường này, mẹ nên liên hệ người nhà và đưa đến cơ sở y tế gần nhất để được thăm khám kịp thời.'
        f'</p>'
        f'</div>', unsafe_allow_html=True
    )
        
    st.button("Lưu Thiết lập cảnh báo", key="save_settings_warning", type="primary", use_container_width=True) # Nút Lưu BẮT BUỘC
    
    st.markdown("---")
    st.markdown("##### Chính sách & Pháp lý")
    st.markdown("Đọc **Điều khoản dịch vụ** và **Chính sách bảo mật**.")


# --- 4. MAIN APPLICATION FLOW ---

if st.session_state.logged_in == False:
    login_page()
else:
    sidebar_navigation()
    if st.session_state.current_page == 'Trang chủ':
        home_page()
    elif st.session_state.current_page == 'Sổ tay cá nhân':
        personal_log_page()
    elif st.session_state.current_page == 'Cài đặt':
        settings_page()
