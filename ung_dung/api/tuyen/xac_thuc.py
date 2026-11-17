from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ung_dung.api.phu_thuoc import lay_nguoi_dung_hien_tai
from ung_dung.co_so_du_lieu.ket_noi import lay_phien_csdl
from ung_dung.co_so_du_lieu.luoc_do import (
    DangKyYeuCau,
    NguoiDungPhanHoi,
    TokenPhanHoi,
)
from ung_dung.co_so_du_lieu.mo_hinh import NguoiDung, VaiTro
from ung_dung.loi.bao_mat import kiem_tra_mat_khau, tao_token_truy_cap
from ung_dung.thao_tac.nguoi_dung import (
    kiem_tra_ton_tai,
    lay_nguoi_dung_theo_ten_dang_nhap,
    tao_nguoi_dung_moi,
)

router = APIRouter(prefix="/xac-thuc", tags=["Xác thực"])


@router.post("/dang-ky", response_model=TokenPhanHoi, status_code=201)
async def dang_ky(
    du_lieu: DangKyYeuCau,
    phien: AsyncSession = Depends(lay_phien_csdl),
):
    # Không cho phép tự đăng ký ADMIN
    if du_lieu.vai_tro == VaiTro.ADMIN:
        raise HTTPException(
            status_code=403, detail="Không thể tự đăng ký vai trò ADMIN"
        )

    if await kiem_tra_ton_tai(
        phien, du_lieu.ten_dang_nhap, du_lieu.email, du_lieu.so_dien_thoai
    ):
        raise HTTPException(
            status_code=400,
            detail="Tên đăng nhập, email hoặc số điện thoại đã tồn tại",
        )

    nguoi_dung = await tao_nguoi_dung_moi(phien, du_lieu)
    token = tao_token_truy_cap(nguoi_dung.ma_nguoi_dung)
    return TokenPhanHoi(access_token=token)


@router.post("/dang-nhap", response_model=TokenPhanHoi)
async def dang_nhap(
    hinh_thuc: OAuth2PasswordRequestForm = Depends(),
    phien: AsyncSession = Depends(lay_phien_csdl),
):
    nguoi_dung = await lay_nguoi_dung_theo_ten_dang_nhap(phien, hinh_thuc.username)
    if not nguoi_dung or not kiem_tra_mat_khau(
        hinh_thuc.password, nguoi_dung.mat_khau_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = tao_token_truy_cap(nguoi_dung.ma_nguoi_dung)
    return TokenPhanHoi(access_token=token)


@router.get("/toi", response_model=NguoiDungPhanHoi)
async def thong_tin_ca_nhan(
    nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
):
    """Trả về thông tin người dùng đang đăng nhập."""
    return nguoi_dung
