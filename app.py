import streamlit as st
import datetime
import pandas as pd

# --- Cấu hình giao diện và Phong cách (Aesthetics) ---

# Tông màu chủ đạo (Pastel Blue, Pink, Beige)
COLOR_BEIGE = "#f8f7f3"
COLOR_BLUE = "#a8dadc"       # Xanh pastel
COLOR_DARK_BLUE = "#1d3557"  # Xanh đậm cho chữ
COLOR_PINK = "#fcc8c8"       # Hồng pastel
COLOR_DARK_PINK = "#e63946"  # Hồng đậm cho chữ

def apply_custom_css():
    """Áp dụng CSS tùy chỉnh để thiết lập tông màu pastel và font chữ."""
    # Sử dụng font hệ thống hiện đại, làm nền trắng/be, và các màu chủ đạo
    css = f"""
    <style>
        /* Thiết lập font và nền chung */
        .stApp {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: {COLOR_BEIGE};
        }}
        
        /* Tiêu đề chính */
        .st-emotion-cache-1wivap2 {{ 
            color: {COLOR_DARK_BLUE};
            font-weight: 700;
        }}

        /* Tiêu đề sidebar */
        .st-emotion-cache-1629p8f {{
            color: {COLOR_DARK_BLUE} !important;
            font-weight: 600;
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

        /* Màu nền cho các khung nội dung chính */
        .st-emotion-cache-1kyz2p8 {{ /* main content padding/margin */
            padding-top: 2rem;
        }}
        .main-content-box {{
            padding: 20px;
            border-radius: 12px;
            background-color: white; /* Nền trắng cho nội dung */
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            border-left: 5px solid {COLOR_PINK}; /* Điểm nhấn hồng */
        }}
        
        /* Màu cho các widget nhập liệu */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stDateInput>div>div>input {{
            border-radius: 8px;
            border: 1px solid #ccc;
            padding: 8px 10px;
        }}
        
        /* Tùy chỉnh màu chữ đậm theo yêu cầu */
        h1, h2, h3, h4, h5, h6, label {{
            color: {COLOR_DARK_BLUE};
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- Khởi tạo Trạng thái (Session State) ---
def init_session_state():
    """Khởi tạo các biến trạng thái cần thiết."""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "login"
    if 'user_id' not in st.session_state:
        st.session_state.user_id = ""
        
    # Dữ liệu hồ sơ (Thay thế cho database)
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = {
            'ho_ten': 'Chưa cập nhật',
            'tuoi': None,
            'chieu_cao': None,
            'can_nang': None,
            'tien_su_benh': 'Không',
            'thuoc_su_dung': 'Không',
            'lan_sinh_thu': None,
            'ngay_du_sinh': datetime.date.today(),
            'tuan_thai_hien_tai': 0,
        }

    # Lịch sử chẩn đoán
    if 'diagnosis_history' not in st.session_state:
        st.session_state.diagnosis_history = pd.DataFrame(columns=[
            'Ngày - Giờ', 'Kết quả sơ bộ', 'Chỉ số cụ thể (Ẩn)', 'Ghi chú'
        ])
    
    # Nhật ký thuốc
    if 'medication_diary' not in st.session_state:
        st.session_state.medication_diary = ["Vitamin tổng hợp", "Sắt/Axit Folic"]


# --- Hàm chuyển đổi trang ---
def navigate_to(page):
    """Chuyển đổi giữa các trang chính."""
    st.session_state.current_page = page
    st.experimental_rerun()

# --- Các trang chức năng ---

def login_page():
    """Màn hình chào mừng và đăng nhập."""
    st.title("Chào Mừng Quay Lại")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Đăng nhập")
        
        email = st.text_input("Email/Số điện thoại")
        password = st.text_input("Mật khẩu", type="password", key="password_input") # Có chi tiết mắt cạnh mật khẩu

        if st.button("Đăng Nhập", key="login_btn"):
            if email and password:
                # Giả lập đăng nhập thành công
                st.session_state.logged_in = True
                st.session_state.user_id = email # Lấy email làm user id tạm thời
                navigate_to("home")
            else:
                st.error("Vui lòng nhập đầy đủ Email/SĐT và Mật khẩu.")

        st.markdown(
            f"""
            <div style="font-size: 14px; margin-top: 10px;">
                <a href="#" style="color: {COLOR_DARK_BLUE};">Quên mật khẩu?</a>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with col2:
        st.subheader("Chính sách và Hỗ trợ")
        st.info("Chính sách bảo mật, điều khoản sử dụng và thông tin hỗ trợ được đặt tại đây.")
        st.markdown(
            f"""
            <div style="text-align: right; margin-top: 50px;">
                <p style="font-size: 14px; color: {COLOR_DARK_BLUE};">Chưa có tài khoản?</p>
                <a href="#" style="
                    color: {COLOR_DARK_PINK}; 
                    font-weight: 700; 
                    font-size: 18px; 
                    padding: 5px 10px; 
                    border: 2px solid {COLOR_DARK_PINK};
                    border-radius: 8px;
                    text-decoration: none;
                ">Tạo tài khoản mới</a>
            </div>
            """,
            unsafe_allow_html=True
        )

def home_page():
    """Trang chủ bao gồm các hồ sơ mẹ, bé và điện tim."""
    st.title("Trang Chủ")
    st.markdown("---")

    st.header(f"Xin chào, {st.session_state.profile_data['ho_ten']}!")
    
    tab1, tab2, tab3 = st.tabs(["Hồ sơ Mẹ", "Hồ sơ Bé", "Hồ sơ Đo Điện Tim"])

    # 1. Hồ sơ Mẹ
    with tab1:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("Cập nhật Hồ sơ Mẹ")
        
        with st.form("mother_profile_form"):
            col_a, col_b = st.columns(2)
            
            # Khai báo biến tạm thời để giữ giá trị hiện tại
            temp_data = st.session_state.profile_data

            with col_a:
                ho_ten = st.text_input("Họ và Tên", value=temp_data['ho_ten'])
                chieu_cao = st.number_input("Chiều cao (cm)", min_value=100, max_value=250, value=temp_data['chieu_cao'] if temp_data['chieu_cao'] else 160)
                tien_su_benh = st.text_area("Tiền sử bệnh", value=temp_data['tien_su_benh'], height=100)

            with col_b:
                tuoi = st.number_input("Tuổi", min_value=15, max_value=60, value=temp_data['tuoi'] if temp_data['tuoi'] else 25)
                can_nang = st.number_input("Cân nặng hiện tại (kg)", min_value=30.0, max_value=200.0, value=temp_data['can_nang'] if temp_data['can_nang'] else 55.0, step=0.1)
                thuoc_su_dung = st.text_area("Thuốc đang sử dụng (nếu có)", value=temp_data['thuoc_su_dung'], height=100)
            
            submitted_mother = st.form_submit_button("Lưu Hồ Sơ Mẹ", type="primary")

            if submitted_mother:
                st.session_state.profile_data.update({
                    'ho_ten': ho_ten,
                    'tuoi': tuoi,
                    'chieu_cao': chieu_cao,
                    'can_nang': can_nang,
                    'tien_su_benh': tien_su_benh,
                    'thuoc_su_dung': thuoc_su_dung,
                })
                st.success("Đã lưu Hồ sơ Mẹ thành công!")
        st.markdown('</div>', unsafe_allow_html=True)


    # 2. Hồ sơ Bé
    with tab2:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("Thông tin Thai kỳ và Hồ sơ Bé")

        with st.form("baby_profile_form"):
            col_c, col_d = st.columns(2)
            
            temp_data = st.session_state.profile_data

            with col_c:
                lan_sinh_thu = st.number_input("Lần sinh thứ", min_value=1, max_value=10, value=temp_data['lan_sinh_thu'] if temp_data['lan_sinh_thu'] else 1)
                ngay_du_sinh = st.date_input("Ngày dự sinh (Dự kiến)", value=temp_data['ngay_du_sinh'])

            with col_d:
                # Giả lập tính Tuần thai hiện tại dựa trên Ngày dự sinh
                today = datetime.date.today()
                
                # Tính tuần thai (giả định thai kỳ 40 tuần)
                if ngay_du_sinh:
                    days_remaining = (ngay_du_sinh - today).days
                    total_days = 40 * 7
                    days_passed = total_days - days_remaining
                    tuan_thai_hien_tai = max(0, min(40, days_passed // 7))
                else:
                    tuan_thai_hien_tai = 0
                
                st.markdown(f"**Tuần thai hiện tại:** <span style='color: {COLOR_DARK_PINK}; font-size: 20px; font-weight: 700;'>Tuần {tuan_thai_hien_tai}</span>", unsafe_allow_html=True)
                st.session_state.profile_data['tuan_thai_hien_tai'] = tuan_thai_hien_tai


            submitted_baby = st.form_submit_button("Lưu Hồ Sơ Bé", type="primary")

            if submitted_baby:
                st.session_state.profile_data.update({
                    'lan_sinh_thu': lan_sinh_thu,
                    'ngay_du_sinh': ngay_du_sinh,
                })
                st.success("Đã lưu Hồ sơ Bé thành công!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    # 3. Hồ sơ Đo Điện Tim
    with tab3:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("Kết quả Đo Điện Tim/Chẩn đoán (Mockup)")
        st.warning("Tính năng này cần kết nối với thiết bị y tế. Hiện tại chỉ là giao diện giả lập.")
        
        with st.form("ecg_form"):
            ecg_data = st.file_uploader("Tải lên file dữ liệu điện tim (ECG/EPH)", type=['txt', 'csv'])
            ghi_chu_ecg = st.text_area("Ghi chú về lần đo này", "Không có")
            
            if st.form_submit_button("Gửi Dữ Liệu Chẩn Đoán", type="primary"):
                if ecg_data is not None:
                    st.info(f"Đã gửi file **{ecg_data.name}** để xử lý. Kết quả sẽ được cập nhật vào Lịch sử theo dõi.")
                else:
                    # Giả lập thêm một chẩn đoán không có file
                    new_diagnosis = {
                        'Ngày - Giờ': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'Kết quả sơ bộ': 'Nghi ngờ',
                        'Chỉ số cụ thể (Ẩn)': 'Chỉ số giả định: Huyết áp (130/85), Nhịp tim (95)',
                        'Ghi chú': ghi_chu_ecg
                    }
                    st.session_state.diagnosis_history.loc[len(st.session_state.diagnosis_history)] = new_diagnosis
                    st.success("Đã lưu kết quả chẩn đoán sơ bộ vào Lịch sử.")

        st.markdown('</div>', unsafe_allow_html=True)


def handbook_page():
    """Sổ tay cá nhân: Lịch sử theo dõi, Nhật kí thuốc, Mẹo thai kì."""
    st.title("Sổ Tay Cá Nhân")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Lịch sử - Theo dõi", "Nhật ký Thuốc", "Mẹo Chăm sóc Thai kì"])

    # 1. Lịch sử - Theo dõi
    with tab1:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("Lịch sử Chẩn đoán & Theo dõi")
        
        history_df = st.session_state.diagnosis_history.sort_values(by='Ngày - Giờ', ascending=False).reset_index(drop=True)
        
        if history_df.empty:
            st.info("Chưa có lịch sử chẩn đoán nào được lưu.")
        else:
            for index, row in history_df.iterrows():
                with st.expander(f"Lần chẩn đoán: {row['Ngày - Giờ']} - Kết quả: **{row['Kết quả sơ bộ']}**", expanded=False):
                    st.write(f"**Ngày - Giờ chẩn đoán:** {row['Ngày - Giờ']}")
                    
                    # Kết quả chẩn đoán sơ bộ
                    color = COLOR_DARK_BLUE
                    if 'Bình thường' in row['Kết quả sơ bộ']:
                        color = 'green'
                    elif 'Nghi ngờ' in row['Kết quả sơ bộ']:
                        color = 'orange'
                    elif 'Bất thường' in row['Kết quả sơ bộ']:
                        color = 'red'

                    st.markdown(f"**Kết quả chẩn đoán sơ bộ:** <span style='color: {color}; font-weight: 600;'>{row['Kết quả sơ bộ']}</span>", unsafe_allow_html=True)
                    
                    # Chỉ số cụ thể (tạm thời ẩn, khi click sẽ hiện ra)
                    with st.expander("Xem Chỉ số Cụ thể (21 chỉ số)"):
                        st.text_area("Chỉ số chi tiết:", value=row['Chỉ số cụ thể (Ẩn)'], height=150, disabled=True)
                        
                    st.write(f"**Ghi chú:** {row['Ghi chú']}")

        st.markdown('</div>', unsafe_allow_html=True)

    # 2. Nhật ký Thuốc
    with tab2:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("Thuốc Đang Sử Dụng/Nhật ký")
        
        current_meds = st.session_state.medication_diary

        st.markdown("##### 💊 Danh sách thuốc đã nhập:")
        for med in current_meds:
            st.markdown(f"- <span style='color: {COLOR_DARK_BLUE}; font-weight: 500;'>{med}</span>", unsafe_allow_html=True)
            
        st.markdown("---")
        
        st.markdown("##### Thêm thuốc/thực phẩm chức năng mới")
        new_med = st.text_input("Tên thuốc hoặc thực phẩm chức năng mới")
        
        if st.button("+ Thêm", key="add_med_btn"):
            if new_med and new_med not in current_meds:
                st.session_state.medication_diary.append(new_med)
                st.success(f"Đã thêm '{new_med}' vào nhật ký.")
                st.experimental_rerun()
            elif new_med in current_meds:
                 st.warning("Thuốc này đã có trong danh sách.")
            else:
                st.error("Vui lòng nhập tên thuốc.")
        
        # Nút lưu, mặc dù dữ liệu đã được lưu vào session state khi thêm
        if st.button("Lưu Nhật Ký Thuốc", key="save_med_btn"):
            st.success("Đã cập nhật nhật ký thuốc.")

        st.markdown('</div>', unsafe_allow_html=True)


    # 3. Mẹo Chăm sóc Thai kì (Thông tin tĩnh)
    with tab3:
        st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
        st.subheader("💡 Mẹo Chăm sóc Thai kì")
        
        st.markdown(f"#### 1. Hướng dẫn mẹ theo dõi thai kì hiệu quả", unsafe_allow_html=True)
        st.info(
            "Việc theo dõi thai kỳ cần được thực hiện đều đặn. Mẹ nên ghi chép lại mọi thay đổi của cơ thể, các chỉ số đo được và lịch sử tiêm chủng/khám thai. Hãy chuẩn bị tâm lý thoải mái, tham gia các lớp học tiền sản và luôn sẵn sàng trao đổi với bác sĩ về mọi lo lắng của mình. Đừng quên theo dõi cử động của bé mỗi ngày."
        )

        st.markdown(f"#### 2. Dinh dưỡng và Bài tập", unsafe_allow_html=True)
        col_e, col_f = st.columns(2)
        
        with col_e:
            st.markdown("**🍲 Dinh Dưỡng Đề Xuất:**", unsafe_allow_html=True)
            st.markdown(f"""
                - Cá hồi (Omega-3)
                - Các loại đậu (Protein và chất xơ)
                - Rau xanh đậm (Axit Folic)
                - Trứng (Choline)
                - Trái cây và sữa chua.
            """)
            
        with col_f:
            st.markdown("**🤸 Bài Tập Sức Khỏe:**", unsafe_allow_html=True)
            st.markdown(f"""
                - Yoga hoặc Pilates nhẹ nhàng
                - Đi bộ 30 phút mỗi ngày
                - Bơi lội (giúp giảm áp lực khớp)
                - Các bài tập Kegel.
            """)
        
        st.markdown(f"#### 3. Massage Cơ Thể", unsafe_allow_html=True)
        st.caption("Massage giúp giảm sưng phù và thư giãn tinh thần.")
        st.markdown(f"""
            - **Chân và Bàn chân:** Massage nhẹ nhàng giúp lưu thông máu, giảm sưng.
            - **Vùng lưng dưới:** Giúp giảm đau lưng do thai nhi lớn dần.
            - **Vai và Cổ:** Tập trung thư giãn các cơ bị căng.
        """)
        
        if st.button("Lưu Các Mẹo Yêu Thích", key="save_tips_btn"):
            st.success("Đã lưu các mẹo chăm sóc thai kỳ!") # Giả lập lưu

        st.markdown('</div>', unsafe_allow_html=True)


def settings_page():
    """Cài đặt: Thông tin tài khoản, thay đổi mật khẩu."""
    st.title("Cài Đặt")
    st.markdown("---")

    st.markdown(f'<div class="main-content-box">', unsafe_allow_html=True)
    st.subheader("Thông tin Tài khoản")
    
    current_user_name = st.session_state.profile_data.get('ho_ten', 'Người dùng')
    
    st.markdown(f"**👤 Tên tài khoản:** <span style='color: {COLOR_DARK_BLUE};'>{current_user_name}</span>", unsafe_allow_html=True)
    st.markdown(f"**📧 Email/Số điện thoại:** <span style='color: {COLOR_DARK_BLUE};'>{st.session_state.user_id}</span>", unsafe_allow_html=True)
    
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
                    st.success("Đã thay đổi mật khẩu thành công!")
                else:
                    st.error("Mật khẩu mới không khớp hoặc quá ngắn.")
        
        with col_h:
            if st.button("Đăng Xuất", key="logout_btn"):
                st.session_state.logged_in = False
                st.session_state.current_page = "login"
                st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# --- Chạy ứng dụng chính ---
def main():
    """Hàm chính điều khiển luồng ứng dụng."""
    
    # 1. Khởi tạo
    init_session_state()
    st.set_page_config(page_title="App Theo Dõi Thai Kỳ", layout="wide")
    apply_custom_css()

    # 2. Xử lý logic đăng nhập
    if not st.session_state.logged_in:
        login_page()
        return

    # 3. Thanh điều hướng (Sidebar)
    st.sidebar.title("🤰 Ứng Dụng")
    st.sidebar.markdown(f"**Xin chào:** *{st.session_state.user_id}*")
    st.sidebar.markdown("---")
    
    nav_options = {
        "home": "Trang Chủ",
        "handbook": "Sổ Tay Cá Nhân",
        "settings": "Cài Đặt"
    }
    
    for key, name in nav_options.items():
        if st.sidebar.button(name, key=f"nav_{key}", use_container_width=True):
            navigate_to(key)
    
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
    
    # Đảm bảo trang hiện tại hợp lệ
    if st.session_state.current_page in page_functions:
        page_functions[st.session_state.current_page]()
    else:
        # Mặc định về trang chủ nếu có lỗi
        home_page()

if __name__ == '__main__':
    main()
