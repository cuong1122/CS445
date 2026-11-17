from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ung_dung.co_so_du_lieu.mo_hinh import Phong
from ung_dung.co_so_du_lieu.luoc_do import TaoPhongYeuCau


async def tao_phong_moi(
    phien: AsyncSession, du_lieu: TaoPhongYeuCau, ma_chu_tro: int
) -> Phong:
    """Tạo phòng mới và gán cho chủ trọ đang đăng nhập."""
    phong_moi = Phong(
        ma_chu_tro=ma_chu_tro,
        **du_lieu.model_dump(),  # Tự động map các trường từ Pydantic sang Model
    )
    phien.add(phong_moi)
    await phien.commit()
    await phien.refresh(phong_moi)
    return phong_moi


async def lay_danh_sach_phong_cua_toi(
    phien: AsyncSession, ma_chu_tro: int
) -> list[Phong]:
    """Lấy tất cả phòng do chủ trọ này đăng."""
    ket_qua = await phien.execute(
        select(Phong)
        .where(Phong.ma_chu_tro == ma_chu_tro)
        .order_by(Phong.ngay_tao.desc())
    )
    return list(ket_qua.scalars().all())


async def lay_danh_sach_phong_da_duyet(phien: AsyncSession) -> list[Phong]:
    """Lấy tất cả phòng đã được duyệt (dành cho người thuê xem)."""
    # Lưu ý: Cần import TrangThaiTinDang từ mo_hinh
    from ung_dung.co_so_du_lieu.mo_hinh import TrangThaiTinDang

    ket_qua = await phien.execute(
        select(Phong).where(Phong.trang_thai_tin_dang == TrangThaiTinDang.APPROVED)
    )
    return list(ket_qua.scalars().all())
