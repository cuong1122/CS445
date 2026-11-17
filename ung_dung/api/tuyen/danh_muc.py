from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ung_dung.co_so_du_lieu.ket_noi import lay_phien_csdl
from ung_dung.co_so_du_lieu.mo_hinh import DanhMuc, LoaiDanhMuc

router = APIRouter(prefix="/danh-muc", tags=["Danh mục"])


@router.get("/loai-phong")
async def lay_danh_sach_loai_phong(phien: AsyncSession = Depends(lay_phien_csdl)):
    """Lấy danh sách loại phòng (ROOM_TYPE)"""
    ket_qua = await phien.execute(
        select(DanhMuc).where(
            DanhMuc.loai == LoaiDanhMuc.ROOM_TYPE, DanhMuc.dang_su_dung == True
        )
    )
    return ket_qua.scalars().all()


@router.get("/khu-vuc")
async def lay_danh_sach_khu_vuc(phien: AsyncSession = Depends(lay_phien_csdl)):
    """Lấy danh sách khu vực (AREA)"""
    ket_qua = await phien.execute(
        select(DanhMuc).where(
            DanhMuc.loai == LoaiDanhMuc.AREA, DanhMuc.dang_su_dung == True
        )
    )
    return ket_qua.scalars().all()
