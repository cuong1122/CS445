from pydantic import BaseModel, ConfigDict, EmailStr, Field
from ung_dung.co_so_du_lieu.mo_hinh import TrangThaiNguoiDung, VaiTro
from decimal import Decimal
from ung_dung.co_so_du_lieu.mo_hinh import Phong, TrangThaiPhong, TrangThaiTinDang
from datetime import datetime


# ---------- Đăng ký ----------
class DangKyYeuCau(BaseModel):
    ten_dang_nhap: str = Field(min_length=3, max_length=50)
    mat_khau: str = Field(min_length=6, max_length=128)
    ho_ten: str = Field(min_length=1, max_length=100)
    email: EmailStr
    so_dien_thoai: str = Field(min_length=10, max_length=15)
    vai_tro: VaiTro  # chỉ chấp nhận TENANT hoặc LANDLORD


# ---------- Đăng nhập ----------
class DangNhapYeuCau(BaseModel):
    ten_dang_nhap: str
    mat_khau: str


# ---------- Token trả về ----------
class TokenPhanHoi(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Thông tin người dùng trả về ----------
class NguoiDungPhanHoi(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # cho phép đọc từ ORM

    ma_nguoi_dung: int
    ten_dang_nhap: str
    ho_ten: str
    email: EmailStr
    so_dien_thoai: str
    vai_tro: VaiTro
    trang_thai: TrangThaiNguoiDung


class TaoPhongYeuCau(BaseModel):
    ma_loai_phong: int
    ma_khu_vuc: int
    tieu_de: str = Field(min_length=10, max_length=200)
    mo_ta: str | None = None
    dia_chi: str
    dien_tich_m2: Decimal
    gia_thue: Decimal
    tien_coc: Decimal = Decimal(0)
    don_gia_dien: Decimal | None = None
    don_gia_nuoc: Decimal | None = None
    so_nguoi_toi_da: int | None = None


class PhongPhanHoi(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ma_phong: int
    ma_chu_tro: int
    tieu_de: str
    dia_chi: str
    gia_thue: Decimal
    dien_tich_m2: Decimal
    trang_thai_phong: TrangThaiPhong
    trang_thai_tin_dang: TrangThaiTinDang
    ngay_tao: datetime
