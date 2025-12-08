import streamlit as st
import pandas as pd
import time
# Các thư viện phân tích/mô hình: 
# import joblib
# from sklearn.ensemble import RandomForestClassifier

# --- 1. CONFIGURATION AND AESTHETICS (Tông màu Mint & Rose Pastel) ---

# Tông màu Mint & Rose Pastel:
COLOR_MINT = '#C7EBEB'       # Xanh bạc hà nhạt (Nền phụ, Nút chính) - Tông Lạnh
COLOR_PINK = '#F5C7D9'       # Hồng Pastel nhạt (Điểm nhấn, Nền phụ) - Tông Ấm
COLOR_OFF_WHITE = '#F8F8F8'  # Trắng ngà/Nền chính rất nhạt
COLOR_DARK_TEXT = '#4A4E69'  # Xanh xám đậm (Cho chữ, Tiêu đề)
COLOR_DEEP_ROSE = '#C93756'  # Hồng Đậm/Đỏ Rose (Điểm nhấn quan trọng, Nút Lưu)

# --- Custom CSS (Đảm bảo giao diện sang trọng, không icon, dễ nhìn) ---
custom_css = f"""
<style>
    /* Nền chung của ứng dụng */
    .stApp {{
        background-color: {COLOR_OFF_WHITE};
        font-family: 'Inter', sans-serif;
    }}

    /* Tiêu đề chính và các thẻ Header (Nhấn mạnh font) */
    h1, h2, h3 {{
        color: {COLOR_DARK_TEXT};
        font-weight: 800; /* Nhấn mạnh hơn */
        letter-spacing: -0.5px;
    }}
    
    /* Giao diện Đăng nhập nổi bật */
    .login-container {{
        max-width: 450px; /* To hơn một chút */
        margin: 50px auto;
        padding: 40px;
        background-color: white;
        border-radius: 25px; /* Góc bo tròn hơn */
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        text-align: center;
    }}

    /* Input Fields */
    .stTextInput input[type="text"], .stTextInput input[type="password"], .stTextInput input[type="number"], .stTextArea textarea, .stSelectbox > div:first-child {{
        border-radius: 12px;
        border: 1px solid {COLOR_MINT}; /* Viền nhạt */
        padding: 10px 15px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); /* Shadow nhẹ */
    }}
    
    /* Nút Đăng nhập/Chính (Màu Xanh bạc hà) */
    .stButton > button {{
        background-color: {COLOR_MINT};
        color: {COLOR_DARK_TEXT};
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 700;
        border: none;
        transition: all 0.3s;
    }}
    .stButton > button:hover {{
        background-color: {COLOR_PINK}; /* Hover sang màu hồng */
        color: {COLOR_DARK_TEXT};
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    }}

    /* Nút Lưu (Save) - Quan trọng, dùng màu Hồng Đậm Accent */
    button[kind="primary"] {{
        background-color: {COLOR_DEEP_ROSE} !important;
        border: 1px solid {COLOR_DEEP_ROSE} !important;
        color: white !important;
    }}
    button[kind="primary"]:hover {{
        background-color: {COLOR_DEEP_ROSE}AA !important; /* Độ mờ nhẹ khi hover */
        border: 1px solid {COLOR_DEEP_ROSE} !important;
        color: white !important;
    }}

    /* Sidebar Navigation (Đổi màu sidebar) */
    [data-testid="stSidebarContent"] {{
        background-color: {COLOR_MINT}50; /* Xanh bạc hà nhạt */
    }}
    
    .stRadio div[role="radiogroup"] > label:has(input:checked) {{
        background-color: {COLOR_PINK}; /* Màu Hồng nhạt khi chọn */
        color: {COLOR_DARK_TEXT};
        font-weight: bold;
    }}
    
    /* Box chẩn đoán */
    .diagnosis-box {{
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        margin-top: 10px;
        padding: 20px;
    }}

    /* Tab Layout (Tạo giao diện Tab mềm mại hơn) */
    .stTabs [data-testid="stTab"] {{
        background-color: {COLOR_OFF_WHITE};
        color: {COLOR_DARK_TEXT};
        border-radius: 10px 10px 0 0;
        padding: 10px 15px;
        margin-right: 5px;
        border: 1px solid {COLOR_MINT};
        font-weight: 600;
    }}
    .stTabs [data-testid="stTab"].st-h:nth-child(1) {{ 
        border-bottom-color: {COLOR_OFF_WHITE} !important; /* Ẩn viền dưới của tab đang chọn */
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
if 'diagnosis' not in st.session_state:
    st.session_state.diagnosis = None
if 'diagnosis_time' not in st.session_state:
    st.session_state.diagnosis_time = None
if 'due_date' not in st.session_state:
    st.session_state.due_date = pd.to_datetime('2026-03-01').date() # Dùng .date() cho st.date_input

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
    """Màn hình Đăng nhập"""
    
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.markdown(f'<h2 style="text-align: center; color: {COLOR_DEEP_ROSE};">Theo Dõi Sức Khỏe Thai Nhi</h2>', unsafe_allow_html=True)
    st.markdown(f'<h3 style="text-align: center; color: {COLOR_DARK_TEXT};">Chào mừng bạn quay trở lại!</h3>', unsafe_allow_html=True)
    
    # Form Đăng nhập
    with st.form("login_form"):
        email_sdt = st.text_input("Email hoặc số điện thoại", placeholder="Nhập email hoặc số điện thoại")
        password = st.text_input("Mật khẩu", placeholder="Nhập mật khẩu", type="password")
        
        col_login_1, col_login_2 = st.columns([1, 1])
        with col_login_1:
            st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)
            st.markdown(f'<a href="#" style="color: {COLOR_DARK_TEXT}; font-size: 0.9em;">Quên mật khẩu?</a>', unsafe_allow_html=True)
        
        with col_login_2:
            st.markdown('<div style="text-align: right;">', unsafe_allow_html=True)
            # Nút Đăng nhập vẫn dùng màu Mint (secondary style, nhưng CSS custom đã đổi màu)
            submitted = st.form_submit_button("Đăng nhập", use_container_width=False) 
            st.markdown('</div>', unsafe_allow_html=True)

        if submitted:
            # Logic đăng nhập giả định (luôn thành công)
            if email_sdt and password:
                with st.spinner('Đang xác thực...'):
                    time.sleep(1)
                    
                st.session_state.logged_in = True
                st.session_state.current_page = 'Trang chủ'
                st.session_state.username = email_sdt.split('@')[0] if '@' in email_sdt else "Mẹ Bầu"
                st.rerun()
            else:
                st.error("Vui lòng nhập đầy đủ thông tin.")
    
    st.markdown(f'<div style="margin-top: 30px; text-align: center; color: {COLOR_DARK_TEXT};">Hoặc tiếp tục với</div>', unsafe_allow_html=True)
    
    # Chế độ Demo
    if st.button("Sử dụng Chế độ Demo (Không cần tài khoản)", use_container_width=True, key="demo_login", type="primary"):
        st.session_state.logged_in = True
        st.session_state.current_page = 'Trang chủ'
        st.session_state.username = "Khách (Demo)"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


def sidebar_navigation():
    """Thanh Sidebar (chỉ hiện khi đã đăng nhập) - Đã bỏ icon theo yêu cầu"""
    st.sidebar.title("Theo Dõi Thai Nhi") 
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
        st.session_state.diagnosis = None 
        st.session_state.diagnosis_time = None
        st.rerun()

def home_page():
    """Trang Chủ với Bố cục Tab Ngang"""
    st.title("Trang Chủ - Quản Lý Hồ Sơ")

    # --- 1. BỐ CỤC TAB NGANG ---
    tab_mother, tab_baby, tab_ecg = st.tabs(["🩺 Hồ sơ mẹ", "👶 Hồ sơ bé", "💖 Đo điện tim & Chẩn đoán"])

    # --- TAB 1: HỒ SƠ MẸ ---
    with tab_mother:
        st.subheader("Thông tin chi tiết của mẹ")
        
        # Dùng container để tạo khung bo góc nhẹ
        with st.container(border=True):
            st.text_input("Họ và tên", value="Nguyễn Thị A", key="mother_name")
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.number_input("Tuổi", min_value=15, max_value=50, value=28, key="mother_age")
            with col_m2:
                st.number_input("Chiều cao (cm)", min_value=100.0, value=158.0, step=0.1, key="mother_height")
            with col_m3:
                st.number_input("Cân nặng (kg)", min_value=30.0, value=55.0, step=0.1, key="mother_weight")
                
            st.text_area("Tiền sử bệnh", value="Tiểu đường thai kỳ (Kiểm soát tốt)", key="mother_history")
            st.text_area("Thuốc đang sử dụng", value="Vitamin tổng hợp, Folic Acid", key="mother_meds_home")
            
            st.markdown("---")
            st.button("Lưu Hồ sơ mẹ", key="save_mother", type="primary", use_container_width=True)

    # --- TAB 2: HỒ SƠ BÉ ---
    with tab_baby:
        st.subheader("Thông tin thai nhi")
        with st.container(border=True):
            st.selectbox("Lần sinh thứ", options=['Lần 1', 'Lần 2', 'Lần 3+'], index=0, key="baby_order")
            
            due_date = st.date_input("Ngày dự sinh", value=st.session_state.due_date, key="due_date_input")
            st.session_state.due_date = due_date
            
            # Tính Tuần thai tự động
            today = pd.to_datetime('today').date()
            if isinstance(due_date, pd.Timestamp):
                 due_date = due_date.date()

            days_to_due = (pd.to_datetime(due_date) - pd.to_datetime(today)).days
            
            current_week_display = 0
            if days_to_due >= 0:
                days_since_start = 280 - days_to_due
                current_week = days_since_start / 7
                current_week_display = max(0, int(current_week))
            
            st.markdown(f"**Tuần thai hiện tại:** **<span style='color:{COLOR_DEEP_ROSE}; font-size: 1.1em;'>{current_week_display} tuần</span>**", unsafe_allow_html=True)
            
            st.number_input("Cân nặng ước tính (gram)", min_value=100.0, value=1500.0, step=10.0, key="baby_weight")
            
            st.markdown("---")
            st.button("Lưu Hồ sơ bé", key="save_baby", type="primary", use_container_width=True)


    # --- TAB 3: ĐO ĐIỆN TIM VÀ CHẨN ĐOÁN (Chức năng cốt lõi) ---
    with tab_ecg:
        st.subheader("Phân tích chỉ số CTG/FHR")
        col_ecg_upload, col_ecg_manual = st.columns(2)
        
        with col_ecg_upload:
            st.markdown("##### Tải Dữ Liệu")
            st.info("Tải file CTG (.csv) để phân tích chuyên sâu.")
            uploaded_file = st.file_uploader("Chọn file CTG (.csv) từ máy cá nhân lên:", type=['csv'])

        with col_ecg_manual:
            st.markdown("##### Nhập Dữ Liệu Tùy Chỉnh")
            st.info("Nhập thủ công 21 chỉ số nếu có dữ liệu từ phòng khám.")
            
            with st.expander("Nhập 21 Chỉ Số Điện Tim Thai (CTG)", expanded=False):
                col_i1, col_i2, col_i3 = st.columns(3)
                input_data = {}
                
                # Logic nhập liệu giữ nguyên
                for i, feature in enumerate(CTG_FEATURES):
                    col = [col_i1, col_i2, col_i3][i % 3]
                    with col:
                        default_value = 140.0 if i == 0 else (0.5 if i == 8 else 0.0)
                        input_data[feature] = st.number_input(
                            f"{i+1}. {feature}", 
                            min_value=0.0, 
                            value=st.session_state.get(f"input_ctg_{i}", default_value), 
                            step=0.1,
                            key=f"input_ctg_{i}"
                        )
            
            if st.button("Lưu và Chẩn Đoán", key="diagnose_save", type="primary", use_container_width=True):
                # Giả định chẩn đoán thành công (Dùng Random để mô phỏng)
                import random
                result_options = ["Bình thường"] * 5 + ["Nghi ngờ"] * 3 + ["Nguy hiểm"] * 1
                diagnosis_result = random.choice(result_options)
                
                st.session_state.diagnosis = diagnosis_result
                st.session_state.diagnosis_time = pd.Timestamp.now().strftime("%d/%m/%Y %H:%M:%S")

            if st.session_state.diagnosis:
                display_diagnosis_result(st.session_state.diagnosis, st.session_state.diagnosis_time)


def display_diagnosis_result(result, diagnosis_time):
    """Hiển thị Khung Kết Quả Chẩn Đoán với lời nhận xét tùy chỉnh."""
    
    if result == "Bình thường":
        color_box = COLOR_MINT # Bạc Hà cho Bình thường
        color_text = COLOR_DARK_TEXT
        advice = "Đây là một tín hiệu rất tích cực. Mẹ hãy tiếp tục giữ tinh thần thoải mái, đảm bảo chế độ dinh dưỡng và nghỉ ngơi hợp lý. Vui lòng theo dõi các buổi khám thai định kỳ theo lịch hẹn của bác sĩ để kiểm tra các chỉ số tổng quát khác."
    elif result == "Nghi ngờ":
        color_box = COLOR_PINK # Hồng Pastel cho Nghi ngờ
        color_text = COLOR_DEEP_ROSE
        advice = "**Điều này có nghĩa là có một số thay đổi nhỏ cần được chú ý, mặc dù chưa phải là tình trạng bệnh lý cấp bách.** KHUYẾN CÁO: Mẹ không cần quá lo lắng nhưng cần **tái khám hoặc làm thêm các xét nghiệm chuyên sâu** theo chỉ định của bác sĩ để xác nhận lại tình trạng sức khỏe của bé. Tiếp tục theo dõi cử động thai và giữ liên lạc với chuyên viên y tế."
    else: # Nguy hiểm
        color_box = '#FFDDE6' # Màu đỏ nhạt, phù hợp với pastel
        color_text = '#C70039' # Màu đỏ đậm/hồng đậm hơn cho Nguy hiểm
        advice = "**Điều này đồng nghĩa với việc các chỉ số có dấu hiệu bất thường nghiêm trọng và cần được can thiệp y tế ngay lập tức.** HÀNH ĐỘNG KHẨN CẤP: Mẹ cần đến cơ sở y tế gần nhất **ngay lập tức** để được các bác sĩ chuyên khoa thăm khám trực tiếp, đánh giá lâm sàng và có phương án xử lý kịp thời, đảm bảo an toàn tối đa cho cả mẹ và bé."

    st.markdown("---")
    
    # Khung Kết quả Chẩn đoán (Dùng CSS Class mới)
    st.markdown(
        f'<div class="diagnosis-box" style="background-color: {color_box}; border: 2px solid {color_text}40;">'
        f'<h4 style="color: {color_text}; margin-top: 0px;">Kết quả chẩn đoán</h4>'
        f'<p style="color: {color_text}; font-size: 1.1em;">Các chỉ số cho thấy: <strong>{result}</strong></p>'
        f'<p style="font-size: 0.9em; margin-bottom: 0px;">*Thời gian: {diagnosis_time}</p>'
        f'<hr style="border-top: 1px solid {color_text}40;">'
        f'<p style="color: {color_text}; font-size: 0.95em; font-weight: 500;">{advice}</p>'
        f'</div>', 
        unsafe_allow_html=True
    )


def personal_log_page():
    """Sổ Tay Cá Nhân (Lịch sử theo dõi, Nhật kí thuốc và Sổ tay Chăm sóc & Cảnh báo)"""
    st.title("Sổ Tay Cá Nhân")
    st.markdown("Phần này giúp mẹ theo dõi lịch sử chẩn đoán, các lời khuyên chăm sóc thai kỳ và nắm rõ các dấu hiệu cần cảnh báo.")

    # --- CẤU TRÚC TAB MỚI: Lịch sử, Thuốc, Chăm sóc & Cảnh báo ---
    tab_history, tab_medication, tab_care = st.tabs(["Lịch sử Chẩn đoán", "💊 Nhật Kí Thuốc", "✨ Sổ Tay Chăm Sóc & Cảnh Báo"])

    # --- TAB 1: Lịch sử Chẩn đoán ---
    with tab_history:
        st.subheader("Lịch sử Chẩn Đoán")
        
        history_df = pd.DataFrame({
            'Ngày - Giờ Chẩn đoán': ['07/12/2025 10:30', '30/11/2025 14:00', '21/11/2025 09:00'],
            'Kết quả sơ bộ': ['Bình thường', 'Nghi ngờ', 'Bình thường'],
            'Ghi chú': ['Không có', 'Cần uống nhiều nước hơn', 'Không có'],
        })
        st.dataframe(history_df, use_container_width=True, hide_index=True)
        
        st.info("Click vào một dòng để xem chi tiết 21 chỉ số cụ thể.")
        
        with st.expander("Xem chi tiết các chỉ số (21 chỉ số)"):
            st.dataframe(pd.DataFrame({'Chỉ số': CTG_FEATURES, 'Giá trị': [145, 0, 0, 0, 0, 0, 0, 75, 0.5, 10, 5.0, 50, 120, 160, 5, 0, 145, 140, 145, 10, 0]}), hide_index=True)
            
        st.button("Lưu Ghi chú Lịch sử", key="save_history_note", type="primary") 

    # --- TAB 2: Nhật Kí Thuốc (Tách biệt) ---
    with tab_medication:
        st.subheader("Nhật Kí Thuốc")
        
        initial_meds = st.session_state.get('mother_meds_home', "Vitamin tổng hợp\nSắt/Folic Acid")
        if 'meds' not in st.session_state:
            st.session_state.meds = initial_meds
            
        st.session_state.meds = st.text_area("Danh sách thuốc đang sử dụng:", value=st.session_state.meds, height=150, key="current_meds_area")
        
        col_med_input, col_med_btn = st.columns([3, 1])
        with col_med_input:
            new_medicine = st.text_input("Thêm thuốc mới vào sổ tay:", key="new_med_input")
        with col_med_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("+ Thêm", key="add_medicine_btn"):
                if new_medicine:
                    st.session_state.meds += f"\n{new_medicine}"
                    st.success(f"Đã thêm: {new_medicine}")
                    st.session_state.current_meds_area = st.session_state.meds
                    st.rerun() 
        
        st.button("Lưu Nhật kí thuốc", key="save_medicine_log", type="primary", use_container_width=True) 

    # --- TAB 3: Sổ tay Chăm sóc & Cảnh báo (Gộp Mẹo & Cảnh báo) ---
    with tab_care:
        st.subheader("Hướng Dẫn Chăm Sóc & Dấu Hiệu Khẩn Cấp")
        
        # Mẹo Chăm Sóc (Nội dung dài hơn)
        st.markdown(f"##### 🌿 Mẹo Chăm Sóc Sức Khỏe Toàn Diện ({st.session_state.current_week_display} tuần)")
        st.info("Thai kỳ là một hành trình tuyệt vời. Hãy áp dụng những lời khuyên sau để giữ sức khỏe tốt nhất cho cả mẹ và bé.")
        
        st.markdown("**1. Dinh Dưỡng Cân Bằng (Đặc biệt 3 tháng cuối):**")
        st.markdown("""
        * **Protein:** Cần thiết cho sự phát triển não và mô của thai nhi (thịt nạc, trứng, sữa, đậu).
        * **Sắt:** Ngăn ngừa thiếu máu cho mẹ (thịt bò, cải bó xôi). Kết hợp với Vitamin C để tăng khả năng hấp thụ.
        * **Canxi:** Giúp hình thành xương cho bé và bảo vệ mật độ xương cho mẹ (sữa chua, phô mai, cá mòi).
        * **Omega-3 (DHA/EPA):** Hỗ trợ phát triển thị lực và thần kinh. Nên ăn cá béo (cá hồi) hoặc dùng thực phẩm chức năng.
        """)
        
        st.markdown("**2. Hoạt Động Thể Chất Hợp Lý:**")
        st.markdown("""
        * **Đi bộ:** Ít nhất 30 phút mỗi ngày.
        * **Yoga:** Tập trung vào các bài tập thở và giãn cơ nhẹ nhàng giúp cải thiện tâm trạng và chuẩn bị cho quá trình sinh nở.
        * **Nghỉ ngơi:** Ngủ đủ 7-9 tiếng mỗi đêm. Nên nằm nghiêng sang trái để cải thiện lưu thông máu.
        """)

        st.markdown("---")

        # Dấu hiệu Cảnh Báo
        st.markdown(f"##### ⚠️ Dấu hiệu cảnh báo KHẨN CẤP")
        st.markdown("Mẹ cần ghi nhớ và đến bệnh viện ngay nếu thấy bất kỳ dấu hiệu nào sau đây:")
        
        warning_list = [
            "Chảy máu âm đạo bất thường (Màu đỏ tươi, lượng nhiều).",
            "Đau bụng dữ dội, co thắt liên tục (đặc biệt trước 37 tuần).",
            "Thai nhi cử động ít hơn hẳn so với bình thường (Đếm cử động, nếu < 10 lần/2 giờ).",
            "Rò rỉ hoặc vỡ nước ối (chất lỏng chảy ra không kiểm soát).",
            "Sốt cao (>38.5 độ C), đau đầu kéo dài hoặc thị lực kém đột ngột."
        ]
        
        for item in warning_list:
            st.markdown(f"- **{item}**") 
            
        st.markdown(
            f'<div style="background-color: {COLOR_PINK}50; padding: 20px; border-left: 5px solid {COLOR_DEEP_ROSE}; border-radius: 8px; margin-top: 20px;">'
            f'<p style="color: {COLOR_DEEP_ROSE}; font-weight: 700; margin-bottom: 0px; font-size: 1.1em;">'
            f'🚨 HÀNH ĐỘNG KHẨN CẤP: Khi xuất hiện các dấu hiệu bất thường này, mẹ nên đến **cơ sở y tế gần nhất ngay lập tức** để được thăm khám kịp thời.'
            f'</p>'
            f'</div>', unsafe_allow_html=True
        )
            
        st.button("Đã Đọc và Hiểu Rõ Sổ Tay", key="confirm_warning", type="primary", use_container_width=True)


def settings_page():
    """Màn hình Cài Đặt ⚙️ (Đã loại bỏ phần Cảnh báo)"""
    # Đã giữ lại icon bánh răng theo yêu cầu của bạn
    st.title("Cài Đặt ⚙️") 
    st.markdown("Quản lý thông tin cá nhân và thiết lập ứng dụng.")

    # --- Thông tin Tài khoản ---
    st.subheader("Thông tin tài khoản")

    col_info1, col_info2 = st.columns([1, 2])
    
    with col_info1:
        st.markdown("##### Ảnh đại diện")
        st.image("https://placehold.co/150x150/F5C7D9/C93756?text=Ảnh+ĐD", width=150)
        st.button("Thay đổi ảnh", key="change_pic_btn", type="secondary")

    with col_info2:
        st.text_input("User Name", value=st.session_state.username)
        st.text_input("Email", value="user@example.com", disabled=True)
        st.text_input("Số điện thoại", value="090-XXX-YYY")
        st.text_input("Thay đổi mật khẩu", type="password", help="Nhập mật khẩu mới")
        st.text_input("Xác nhận mật khẩu", type="password")
        
        st.checkbox("Bật thông báo chuông báo/rung", value=True)

    st.button("Lưu Cài đặt tài khoản", key="save_settings_acc", type="primary", use_container_width=True)

    st.markdown("---")
    
    st.subheader("Thiết lập Chung")
    st.checkbox("Chế độ Tiết kiệm pin (Tắt animation)", value=False)
    
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
