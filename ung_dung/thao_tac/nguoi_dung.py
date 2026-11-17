from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ung_dung.co_so_du_lieu.mo_hinh import NguoiDung
from ung_dung.co_so_du_lieu.luoc_do import DangKyYeuCau
from ung_dung.loi.bao_mat import bam_mat_khau


async def lay_nguoi_dung_theo_ten_dang_nhap(
    phien: AsyncSession, ten_dang_nhap: str
) -> Optional[NguoiDung]:
    ket_qua = await phien.execute(
        select(NguoiDung).where(NguoiDung.ten_dang_nhap == ten_dang_nhap)
    )
    return ket_qua.scalar_one_or_none()


async def lay_nguoi_dung_theo_ma(
    phien: AsyncSession, ma_nguoi_dung: int
) -> Optional[NguoiDung]:
    ket_qua = await phien.execute(
        select(NguoiDung).where(NguoiDung.ma_nguoi_dung == ma_nguoi_dung)
    )
    return ket_qua.scalar_one_or_none()


async def kiem_tra_ton_tai(
    phien: AsyncSession, ten_dang_nhap: str, email: str, so_dien_thoai: str
) -> bool:
    """Trả True nếu đã có user trùng ten_dang_nhap / email / sđt."""
    ket_qua = await phien.execute(
        select(NguoiDung).where(
            (NguoiDung.ten_dang_nhap == ten_dang_nhap)
            | (NguoiDung.email == email)
            | (NguoiDung.so_dien_thoai == so_dien_thoai)
        )
    )
    return ket_qua.first() is not None


async def tao_nguoi_dung_moi(phien: AsyncSession, du_lieu: DangKyYeuCau) -> NguoiDung:
    nguoi_dung_moi = NguoiDung(
        ten_dang_nhap=du_lieu.ten_dang_nhap,
        mat_khau_hash=bam_mat_khau(du_lieu.mat_khau),  # ⚠️ băm ngay tại đây
        ho_ten=du_lieu.ho_ten,
        email=du_lieu.email,
        so_dien_thoai=du_lieu.so_dien_thoai,
        vai_tro=du_lieu.vai_tro,
    )
    phien.add(nguoi_dung_moi)
    await phien.commit()
    await phien.refresh(nguoi_dung_moi)
    return nguoi_dung_moi
