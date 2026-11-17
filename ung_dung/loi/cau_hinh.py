from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class CauHinh(BaseSettings):
    """
    Lớp cấu hình - đọc biến môi trường từ file .env
    """

    # Kết nối cơ sở dữ liệu
    duong_dan_csdl: str

    # Cấu hình JWT
    khoa_bi_mat: str
    thuat_toan_jwt: str = "HS256"
    thoi_gian_het_han_token: int = 30  # phút

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def lay_cau_hinh() -> CauHinh:
    """Trả về instance cấu hình (cache để không đọc .env nhiều lần)."""
    return CauHinh()


# Singleton dùng chung cho toàn bộ ứng dụng
cau_hinh = lay_cau_hinh()
