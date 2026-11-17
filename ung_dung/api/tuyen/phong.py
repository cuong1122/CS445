from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from ung_dung.api.phu_thuoc import lay_nguoi_dung_hien_tai, yeu_cau_vai_tro
from ung_dung.co_so_du_lieu.ket_noi import lay_phien_csdl
from ung_dung.co_so_du_lieu.luoc_do import TaoPhongYeuCau, PhongPhanHoi
from ung_dung.co_so_du_lieu.mo_hinh import NguoiDung, VaiTro
from ung_dung.thao_tac.phong import (
    tao_phong_moi,
    lay_danh_sach_phong_cua_toi,
    lay_danh_sach_phong_da_duyet,
)

router = APIRouter(prefix="/phong", tags=["Quản lý Phòng"])


@router.post(
    "/dang-tin", response_model=PhongPhanHoi, status_code=status.HTTP_201_CREATED
)
async def dang_tin_phong(
    du_lieu: TaoPhongYeuCau,
    phien: AsyncSession = Depends(lay_phien_csdl),
    # Chỉ LANDLORD mới được gọi API này
    nguoi_dung: NguoiDung = Depends(yeu_cau_vai_tro([VaiTro.LANDLORD])),
):
    """Dành cho Chủ trọ đăng tin phòng mới."""
    phong_moi = await tao_phong_moi(phien, du_lieu, nguoi_dung.ma_nguoi_dung)
    return phong_moi


@router.get("/cua-toi", response_model=list[PhongPhanHoi])
async def danh_sach_phong_cua_toi(
    phien: AsyncSession = Depends(lay_phien_csdl),
    nguoi_dung: NguoiDung = Depends(yeu_cau_vai_tro([VaiTro.LANDLORD])),
):
    """Lấy danh sách phòng do chính chủ trọ này đăng."""
    return await lay_danh_sach_phong_cua_toi(phien, nguoi_dung.ma_nguoi_dung)


@router.get("/", response_model=list[PhongPhanHoi])
async def danh_sach_phong_cong_khai(phien: AsyncSession = Depends(lay_phien_csdl)):
    """Ai cũng xem được danh sách các phòng đã được duyệt."""
    return await lay_danh_sach_phong_da_duyet(phien)
