import enum
from datetime import datetime
from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum as SQLEnum,
    Identity,
    Index,
    String,
    func,
)
from sqlalchemy import Numeric, SmallInteger, Text, ForeignKey
from sqlalchemy.dialects.postgresql import TSVECTOR
from decimal import Decimal
from sqlalchemy import BigInteger, DateTime, Enum as SQLEnum, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ung_dung.co_so_du_lieu.ket_noi import CoSoMoHinh


class VaiTro(str, enum.Enum):
    ADMIN = "ADMIN"
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"


class TrangThaiNguoiDung(str, enum.Enum):
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    DELETED = "DELETED"


class NguoiDung(CoSoMoHinh):
    __tablename__ = "nguoi_dung"

    ma_nguoi_dung: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    ten_dang_nhap: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    mat_khau_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    ho_ten: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    so_dien_thoai: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    duong_dan_anh_dai_dien: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    cccd_ma_hoa: Mapped[str | None] = mapped_column(String(255), nullable=True)
    vai_tro: Mapped[VaiTro] = mapped_column(
        SQLEnum(VaiTro, name="vai_tro_enum"), nullable=False
    )
    trang_thai: Mapped[TrangThaiNguoiDung] = mapped_column(
        SQLEnum(TrangThaiNguoiDung, name="trang_thai_nguoi_dung_enum"),
        nullable=False,
        default=TrangThaiNguoiDung.ACTIVE,
    )
    ngay_tao: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    ngay_cap_nhat: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    __table_args__ = (
        Index("idx_nguoi_dung_vai_tro_trang_thai", "vai_tro", "trang_thai"),
    )


class TrangThaiPhong(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    RENTED = "RENTED"


class TrangThaiTinDang(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    HIDDEN = "HIDDEN"
    REMOVED = "REMOVED"


class Phong(CoSoMoHinh):
    __tablename__ = "phong"

    ma_phong: Mapped[int] = mapped_column(
        BigInteger, Identity(always=True), primary_key=True
    )
    ma_chu_tro: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("nguoi_dung.ma_nguoi_dung"), nullable=False
    )
    ma_loai_phong: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("danh_muc.ma_danh_muc"), nullable=False
    )
    ma_khu_vuc: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("danh_muc.ma_danh_muc"), nullable=False
    )

    tieu_de: Mapped[str] = mapped_column(String(200), nullable=False)
    mo_ta: Mapped[str | None] = mapped_column(Text, nullable=True)
    dia_chi: Mapped[str] = mapped_column(String(255), nullable=False)
    dien_tich_m2: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    gia_thue: Mapped[Decimal] = mapped_column(Numeric(12, 0), nullable=False)
    tien_coc: Mapped[Decimal] = mapped_column(Numeric(12, 0), nullable=False, default=0)
    don_gia_dien: Mapped[Decimal | None] = mapped_column(Numeric(10, 0), nullable=True)
    don_gia_nuoc: Mapped[Decimal | None] = mapped_column(Numeric(10, 0), nullable=True)
    so_nguoi_toi_da: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)

    trang_thai_phong: Mapped[TrangThaiPhong] = mapped_column(
        SQLEnum(TrangThaiPhong, name="trang_thai_phong_enum"),
        nullable=False,
        default=TrangThaiPhong.AVAILABLE,
    )
    trang_thai_tin_dang: Mapped[TrangThaiTinDang] = mapped_column(
        SQLEnum(TrangThaiTinDang, name="trang_thai_tin_dang_enum"),
        nullable=False,
        default=TrangThaiTinDang.PENDING,
    )

    ngay_tao: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
    ngay_cap_nhat: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )

    # Cột full-text search (đã có trong SQL của bạn)
    tieu_de_va_dia_chi_tsv: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)


class LoaiDanhMuc(str, enum.Enum):
    ROOM_TYPE = "ROOM_TYPE"
    AREA = "AREA"
    AMENITY = "AMENITY"
    REPORT_REASON = "REPORT_REASON"


class DanhMuc(CoSoMoHinh):
    __tablename__ = "danh_muc"

    ma_danh_muc: Mapped[int] = mapped_column(
        BigInteger, Identity(always=True), primary_key=True
    )
    ten: Mapped[str] = mapped_column(String(100), nullable=False)
    loai: Mapped[LoaiDanhMuc] = mapped_column(
        SQLEnum(LoaiDanhMuc, name="loai_danh_muc_enum"), nullable=False
    )
    ma_danh_muc_cha: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    mo_ta: Mapped[str | None] = mapped_column(Text, nullable=True)
    dang_su_dung: Mapped[bool] = mapped_column(default=True)
