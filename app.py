import streamlit as st

# --- Configuration based on user requirements ---
# Tone: Xanh dương (Blue), Hồng (Pink), Be (Beige) pastel.
# Background: White/Beige. Text: Darker Blue/Pink for visibility.
# No icons. Elegant, easy-to-use interface.

# Pastel Color Palette
COLOR_BLUE = '#A9D6E5' # Light Blue
COLOR_PINK = '#FFB8C1' # Light Pink
COLOR_BEIGE = '#F5F5DC' # Beige / Cream background base
COLOR_DARK_BLUE = '#1B4965' # Darker Blue for text/accents
COLOR_DARK_PINK = '#C06C84' # Darker Pink for text/accents

# Custom CSS for the specified theme and layout
custom_css = f"""
<style>
    /* Set page background to a soft beige/cream */
    .stApp {{
        background-color: {COLOR_BEIGE};
    }}

    /* Title and Header Styling (using Dark Blue for emphasis) */
    h1, h2, h3 {{
        color: {COLOR_DARK_BLUE};
        font-family: 'Inter', sans-serif;
    }}
    
    /* Main container styling for a structured, elegant look */
    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }}

    /* Style for the main navigation tabs/radio buttons */
    .stRadio > label {{
        padding: 10px 15px;
        margin: 5px;
        border-radius: 8px;
        border: 1px solid {COLOR_PINK};
        color: {COLOR_DARK_BLUE};
        transition: all 0.2s ease-in-out;
    }}

    .stRadio > label:hover {{
        background-color: {COLOR_PINK}20; /* Light hover effect */
        border-color: {COLOR_DARK_PINK};
    }}

    /* Styling for the selected radio button (active tab) */
    .stRadio div[role="radiogroup"] > label:has(input:checked) {{
        background-color: {COLOR_BLUE};
        color: white; /* Contrast text on blue background */
        border-color: {COLOR_DARK_BLUE};
        font-weight: bold;
    }}

    /* Styling for the required 'Lưu' (Save) button */
    .stButton > button {{
        background-color: {COLOR_PINK};
        color: white;
        border-radius: 12px;
        padding: 10px 20px;
        font-weight: 600;
        border: 2px solid {COLOR_DARK_PINK};
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        transition: all 0.2s;
    }}
    .stButton > button:hover {{
        background-color: {COLOR_DARK_PINK};
        color: white;
        border-color: {COLOR_DARK_BLUE};
        box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.2);
    }}

    /* Style inputs and text areas */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        border: 1px solid {COLOR_BLUE};
        border-radius: 6px;
        padding: 10px;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Set up the main page config
st.set_page_config(
    page_title="Fetal ECG Monitoring App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- State Management (Simple Navigation) ---
if 'page' not in st.session_state:
    st.session_state.page = 'Trang chủ'

# --- Sidebar for User Info (Mock) ---
st.sidebar.title("🤰 Fetal Monitoring")
st.sidebar.markdown(f"**Chào mừng trở lại!**")
st.sidebar.markdown("---")

# Mock User/Login Info
st.sidebar.markdown(f"**User:** Nguyễn Thị A")
st.sidebar.markdown(f"**Email:** user@example.com")
st.sidebar.button("Đăng xuất", type="secondary")

st.sidebar.markdown("---")
st.sidebar.subheader("Navigation")
# Main navigation using st.radio, replacing the need for separate pages for this example
page = st.sidebar.radio(
    "Chọn mục:",
    ('Trang chủ', 'Sổ tay cá nhân', 'Cài đặt'),
    index=['Trang chủ', 'Sổ tay cá nhân', 'Cài đặt'].index(st.session_state.page),
    key='main_nav'
)
st.session_state.page = page

# --- Main Content Area ---

st.title("Ứng Dụng Theo Dõi Điện Tim Thai Nhi")

if st.session_state.page == 'Trang chủ':
    st.header("Trang Chủ")
    st.markdown("### Màn hình chính")
    
    # Use columns to lay out the three profile sections nicely
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Hồ sơ mẹ")
        with st.container(border=True):
            st.markdown(f"**Họ và tên:** *Chưa cập nhật*")
            st.markdown(f"**Tuổi:** *Chưa cập nhật*")
            st.markdown(f"**Chiều cao/Cân nặng:** *Chưa cập nhật*")
            st.markdown(f"**Tiền sử bệnh:** *Không*")
            st.markdown(f"**Thuốc đang sử dụng:** *Không*")
            if st.button("Cập nhật Hồ sơ mẹ", key="update_mother_btn"):
                st.info("Chức năng cập nhật sẽ được mở trong giao diện chi tiết.")
            st.button("Lưu (Mẹ)", key="save_mother") # Required Save button

    with col2:
        st.subheader("Hồ sơ bé")
        with st.container(border=True):
            st.markdown(f"**Lần sinh thứ:** *Lần 1*")
            st.markdown(f"**Tuần thai hiện tại:** **28 tuần**")
            st.markdown(f"**Ngày dự sinh:** *XX/YY/ZZZZ*")
            if st.button("Cập nhật Hồ sơ bé", key="update_baby_btn"):
                st.info("Chức năng cập nhật sẽ được mở trong giao diện chi tiết.")
            st.button("Lưu (Bé)", key="save_baby") # Required Save button

    with col3:
        st.subheader("Hồ sơ đo điện tim")
        with st.container(border=True):
            st.markdown(f"**Lần đo gần nhất:** 07/12/2025")
            st.markdown(f"**Kết quả sơ bộ:** **Bình thường**")
            st.markdown(f"**Nhịp tim thai (FHR):** 145 bpm")
            if st.button("Xem Chi tiết/Đo mới", key="view_ecg_btn"):
                st.info("Chức năng xem chi tiết kết quả điện tim.")
            st.button("Lưu (ECG)", key="save_ecg") # Required Save button

elif st.session_state.page == 'Sổ tay cá nhân':
    st.header("Sổ Tay Cá Nhân")

    st.subheader("Lịch sử theo dõi")
    st.markdown("Đây là nơi tự động lưu trữ các lần chẩn đoán và nhật ký thuốc.")

    tab_history, tab_medicine = st.tabs(["Lịch sử chẩn đoán", "Nhật kí thuốc"])

    with tab_history:
        st.markdown("#### Lịch sử Chẩn Đoán")
        st.info("Click vào một lần chẩn đoán để xem chi tiết các chỉ số và ghi chú.")
        st.dataframe({
            'Ngày - Giờ': ['07/12/2025 10:30', '30/11/2025 14:00'],
            'Kết quả sơ bộ': ['Bình thường', 'Nghi ngờ (Nhẹ)'],
            'Ghi chú': ['Không có', 'Uống đủ nước hơn'],
        }, use_container_width=True)

    with tab_medicine:
        st.markdown("#### Nhật Kí Thuốc")
        st.markdown("Danh sách thuốc đang sử dụng (nhập từ hồ sơ mẹ hoặc đã thêm).")
        st.text_area("Thuốc đã nhập:", value="Vitamin tổng hợp\nSắt/Folic Acid", height=100)
        new_medicine = st.text_input("Thêm thuốc mới:")
        if st.button("+ Thêm", key="add_medicine_btn"):
            if new_medicine:
                st.success(f"Đã thêm: {new_medicine}")
            else:
                st.warning("Vui lòng nhập tên thuốc.")
        st.button("Lưu (Thuốc)", key="save_medicine") # Required Save button

    st.subheader("Mẹo Chăm Sóc Thai Kì")
    
    st.markdown("#### Hướng dẫn mẹ theo dõi thai kì hiệu quả")
    st.info("Hãy luôn giữ tâm lý thoải mái, theo dõi cử động thai nhi đều đặn và thăm khám định kỳ. Việc theo dõi thai kì cần được thực hiện trong môi trường yên tĩnh.")

    st.markdown("#### Dinh dưỡng, bài tập")
    col_advice1, col_advice2 = st.columns(2)
    with col_advice1:
        st.markdown("**Dinh Dưỡng Đề Xuất**")
        st.markdown("1. Bổ sung Protein (trứng, thịt nạc).")
        st.markdown("2. Ăn nhiều rau xanh và trái cây.")
        st.markdown("3. Uống đủ $2 - 2.5$ lít nước mỗi ngày.")
    with col_advice2:
        st.markdown("**Bài Tập & Massage**")
        st.markdown("1. Yoga nhẹ nhàng cho bà bầu.")
        st.markdown("2. Đi bộ $30$ phút mỗi ngày.")
        st.markdown("3. Massage lưng và chân để giảm đau nhức.")
    st.button("Lưu (Mẹo)", key="save_tips") # Required Save button

elif st.session_state.page == 'Cài đặt':
    st.header("Cài Đặt")
    st.subheader("Thông tin tài khoản")

    col_info1, col_info2 = st.columns([1, 2])
    
    with col_info1:
        st.markdown("Ảnh đại diện (Mô phỏng)")
        # Placeholder for profile picture
        st.image("https://placehold.co/150x150/A9D6E5/1B4965?text=Ảnh+ĐD", width=150)
        st.button("Thay đổi ảnh", key="change_pic_btn")

    with col_info2:
        st.text_input("User Name", value="Nguyễn Thị A")
        st.text_input("Email", value="user@example.com", disabled=True)
        st.text_input("Số điện thoại", value="090-XXX-YYY")
        
        st.markdown("---")
        
        st.subheader("Bảo mật")
        st.text_input("Thay đổi mật khẩu", type="password", help="Nhập mật khẩu mới")
        st.text_input("Xác nhận mật khẩu", type="password")
        
    st.button("Lưu (Cài đặt)", key="save_settings") # Required Save button

    st.markdown("---")
    st.subheader("Chính sách & Pháp lý")
    st.markdown("Đọc **Điều khoản dịch vụ** và **Chính sách bảo mật**.")
