const token = localStorage.getItem('access_token');
if (!token) window.location.href = '/dang-nhap';

// 1. Tải danh mục và danh sách phòng khi mở trang
document.addEventListener("DOMContentLoaded", async () => {
    await taiDanhMuc();
    await taiDanhSachPhong();
});

async function taiDanhMuc() {
    try {
        // Lấy loại phòng
        const resLoai = await fetch('/danh-muc/loai-phong');
        const loaiPhong = await resLoai.json();
        const selectLoai = document.getElementById('loai-phong');
        loaiPhong.forEach(item => {
            selectLoai.innerHTML += `<option value="${item.ma_danh_muc}">${item.ten}</option>`;
        });

        // Lấy khu vực
        const resKhuVuc = await fetch('/danh-muc/khu-vuc');
        const khuVuc = await resKhuVuc.json();
        const selectKhuVuc = document.getElementById('khu-vuc');
        khuVuc.forEach(item => {
            selectKhuVuc.innerHTML += `<option value="${item.ma_danh_muc}">${item.ten}</option>`;
        });
    } catch (error) { console.error("Lỗi tải danh mục", error); }
}

async function taiDanhSachPhong() {
    try {
        const response = await fetch('/phong/cua-toi', {
            headers: { 'Authorization': 'Bearer ' + token }
        });
        const data = await response.json();
        
        const tbody = document.getElementById('danh-sach-phong');
        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">Bạn chưa có phòng nào. Hãy đăng tin!</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        data.forEach(phong => {
            // Format giá tiền
            const gia = new Intl.NumberFormat('vi-VN').format(phong.gia_thue);
            // Đổi màu trạng thái
            let color = phong.trang_thai_tin_dang === 'APPROVED' ? 'green' : (phong.trang_thai_tin_dang === 'PENDING' ? 'orange' : 'red');
            
            tbody.innerHTML += `
                <tr>
                    <td>#${phong.ma_phong}</td>
                    <td><b>${phong.tieu_de}</b><br><small>${phong.dia_chi}</small></td>
                    <td>${gia} đ</td>
                    <td>${phong.dien_tich_m2} m2</td>
                    <td style="color: ${color}; font-weight: bold;">${phong.trang_thai_tin_dang}</td>
                </tr>
            `;
        });
    } catch (error) { console.error("Lỗi tải danh sách", error); }
}

function toggleForm() {
    const form = document.getElementById('form-dang-tin');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

async function xuLyDangTin(event) {
    event.preventDefault();
    
    const duLieu = {
        ma_loai_phong: parseInt(document.getElementById('loai-phong').value),
        ma_khu_vuc: parseInt(document.getElementById('khu-vuc').value),
        tieu_de: document.getElementById('tieu-de').value,
        dia_chi: document.getElementById('dia-chi').value,
        gia_thue: parseFloat(document.getElementById('gia-thue').value),
        tien_coc: parseFloat(document.getElementById('tien-coc').value || 0),
        dien_tich_m2: parseFloat(document.getElementById('dien-tich').value),
        so_nguoi_toi_da: document.getElementById('so-nguoi').value ? parseInt(document.getElementById('so-nguoi').value) : null,
        mo_ta: document.getElementById('mo-ta').value
    };

    try {
        const response = await fetch('/phong/dang-tin', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify(duLieu)
        });

        if (response.ok) {
            alert("Đăng tin thành công! Vui lòng chờ Admin duyệt.");
            toggleForm(); // Ẩn form
            document.getElementById('form-phong').reset();
            taiDanhSachPhong(); // Tải lại danh sách
        } else {
            const err = await response.json();
            alert("Lỗi: " + (err.detail || "Không thể đăng tin"));
        }
    } catch (error) { alert("Lỗi kết nối server!"); }
}