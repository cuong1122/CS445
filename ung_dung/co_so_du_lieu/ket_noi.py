from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from ung_dung.loi.cau_hinh import cau_hinh


engine = create_async_engine(
    cau_hinh.duong_dan_csdl,
    echo=False,  # Đổi thành True nếu muốn xem câu SQL thực thi
    pool_pre_ping=True,
)

PhienLamViec = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class CoSoMoHinh(DeclarativeBase):
    """Lớp cơ sở cho mọi model SQLAlchemy."""

    pass


async def lay_phien_csdl():
    """
    Dependency cấp một phiên làm việc (session) CSDL cho mỗi request.
    Session tự động đóng sau khi request kết thúc.
    """
    async with PhienLamViec() as phien:
        try:
            yield phien
        finally:
            await phien.close()
