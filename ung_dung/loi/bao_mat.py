from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.context import CryptContext
import bcrypt

from ung_dung.loi.cau_hinh import cau_hinh

# ---------- Băm mật khẩu ----------
bo_bam_mat_khau = CryptContext(schemes=["bcrypt"], deprecated="auto")


def bam_mat_khau(mat_khau: str) -> str:
    """Băm mật khẩu người dùng trước khi lưu DB."""
    # bcrypt yêu cầu đầu vào là bytes, nên cần encode
    mat_khau_bytes = mat_khau.encode("utf-8")
    # Tạo salt và băm
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(mat_khau_bytes, salt)
    # Lưu vào DB dưới dạng chuỗi (string)
    return hashed.decode("utf-8")


def kiem_tra_mat_khau(mat_khau: str, mat_khau_hash: str) -> bool:
    """So sánh mật khẩu nhập vào với hash trong DB."""
    try:
        return bcrypt.checkpw(mat_khau.encode("utf-8"), mat_khau_hash.encode("utf-8"))
    except ValueError:
        # Xử lý trường hợp hash không hợp lệ
        return False


# ---------- JWT ----------
def tao_token_truy_cap(ma_nguoi_dung: int) -> str:
    """Tạo JWT chứa mã người dùng (subject)."""
    thoi_diem_het_han = datetime.now(timezone.utc) + timedelta(
        minutes=cau_hinh.thoi_gian_het_han_token
    )
    du_lieu = {"sub": str(ma_nguoi_dung), "exp": thoi_diem_het_han}
    return jwt.encode(du_lieu, cau_hinh.khoa_bi_mat, algorithm=cau_hinh.thuat_toan_jwt)


def giai_ma_token(token: str) -> Optional[dict]:
    """Giải mã token; trả None nếu token không hợp lệ/hết hạn."""
    try:
        return jwt.decode(
            token, cau_hinh.khoa_bi_mat, algorithms=[cau_hinh.thuat_toan_jwt]
        )
    except JWTError:
        return None
