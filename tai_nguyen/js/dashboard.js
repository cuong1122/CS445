document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem('access_token');
    
    // Nếu không có token -> đá về trang đăng nhập
    if (!token) {
        window.location.href = '/dang-nhap';
        return;
    }

    try {
        // Gọi API lấy thông tin cá nhân (đã viết ở bước trước)
        const response = await fetch('/xac-thuc/toi', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        
        if (!response.ok) {
            // Token hết hạn hoặc không hợp lệ
            localStorage.removeItem('access_token');
            window.location.href = '/dang-nhap';
            return;
        }

        const user = await response.json();
        
        // 1. Hiển thị tên và vai trò
        document.getElementById('user-name').innerText = "Xin chào, " + user.ho_ten;
        document.getElementById('user-role').innerText = "Vai trò: " + user.vai_tro;

        // 2. Hiển thị khu vực chức năng tương ứng với vai trò
        if (user.vai_tro === 'LANDLORD') {
            document.getElementById('khu-vuc-landlord').classList.remove('hidden');
        } else if (user.vai_tro === 'TENANT') {
            document.getElementById('khu-vuc-tenant').classList.remove('hidden');
        } else if (user.vai_tro === 'ADMIN') {
            document.getElementById('khu-vuc-admin').classList.remove('hidden');
        }

    } catch (error) {
        console.error("Lỗi:", error);
    }
});

// Hàm đăng xuất
function dangXuat() {
    localStorage.removeItem('access_token');
    window.location.href = '/dang-nhap';
}