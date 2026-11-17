// tai_nguyen/js/xac_thuc.js

// Hàm hiển thị thông báo
function hienThiKetQua(message, isSuccess) {
    const el = document.getElementById('ket-qua');
    if (!el) return; // Nếu trang không có id này thì bỏ qua
    el.innerText = message;
    el.className = isSuccess ? 'success' : 'error';
}

// Xử lý Đăng Nhập
async function xuLyDangNhap(event) {
    event.preventDefault(); // Ngăn form load lại trang
    const ten = document.getElementById('login-ten').value;
    const matKhau = document.getElementById('login-mat-khau').value;

    // Đăng nhập dùng OAuth2 nên gửi dạng form-urlencoded
    const formData = new URLSearchParams();
    formData.append('username', ten);
    formData.append('password', matKhau);

    try {
        const response = await fetch('/xac-thuc/dang-nhap', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData
        });
        const data = await response.json();

        if (response.ok) {
            hienThiKetQua('Đăng nhập thành công! Đang chuyển hướng...', true);
            localStorage.setItem('access_token', data.access_token);
            
            // Đợi 1 giây rồi chuyển về trang chủ (hoặc dashboard)
            setTimeout(() => {
                window.location.href = '/dashboard'; 
            }, 1000);
        } else {
            hienThiKetQua('Lỗi: ' + data.detail, false);
        }
    } catch (error) {
        hienThiKetQua('Lỗi kết nối Server!', false);
    }
}

// Xử lý Đăng Ký
async function xuLyDangKy(event) {
    event.preventDefault();
    const duLieu = {
        ten_dang_nhap: document.getElementById('reg-ten').value,
        mat_khau: document.getElementById('reg-mat-khau').value,
        ho_ten: document.getElementById('reg-ho-ten').value,
        email: document.getElementById('reg-email').value,
        so_dien_thoai: document.getElementById('reg-sdt').value,
        vai_tro: document.getElementById('reg-vai-tro').value
    };

    try {
        const response = await fetch('/xac-thuc/dang-ky', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(duLieu)
        });
        const data = await response.json();

        if (response.ok) {
            hienThiKetQua('Đăng ký thành công! Đang chuyển sang trang đăng nhập...', true);
            setTimeout(() => {
                window.location.href = '/dang-nhap';
            }, 1500);
        } else {
            let loi = data.detail;
            if (Array.isArray(loi)) loi = loi[0].msg; // Lấy lỗi Pydantic đầu tiên
            hienThiKetQua('Lỗi: ' + loi, false);
        }
    } catch (error) {
        hienThiKetQua('Lỗi kết nối Server!', false);
    }
}