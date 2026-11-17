from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from ung_dung.co_so_du_lieu.ket_noi import lay_phien_csdl
from ung_dung.co_so_du_lieu.mo_hinh import NguoiDung, VaiTro
from ung_dung.loi.bao_mat import giai_ma_token
from ung_dung.thao_tac.nguoi_dung import lay_nguoi_dung_theo_ma

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/xac-thuc/dang-nhap")


async def lay_nguoi_dung_hien_tai(
    token: str = Depends(oauth2_scheme),
    phien: AsyncSession = Depends(lay_phien_csdl),
) -> NguoiDung:
    """Xác thực token và trả về user hiện tại."""
    loi_xac_thuc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn",
        headers={"WWW-Authenticate": "Bearer"},
    )
    du_lieu = giai_ma_token(token)
    if du_lieu is None or du_lieu.get("sub") is None:
        raise loi_xac_thuc

    nguoi_dung = await lay_nguoi_dung_theo_ma(phien, int(du_lieu["sub"]))
    if nguoi_dung is None:
        raise loi_xac_thuc
    return nguoi_dung


# Hàm tạo Dependency kiểm tra quyền
def yeu_cau_vai_tro(danh_sach_vai_tro: list[VaiTro]):
    def kiem_tra_quyen(
        nguoi_dung: NguoiDung = Depends(lay_nguoi_dung_hien_tai),
    ) -> NguoiDung:
        if nguoi_dung.vai_tro not in danh_sach_vai_tro:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền thực hiện hành động này",
            )
        return nguoi_dung

    return kiem_tra_quyen
