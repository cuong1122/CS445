from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from ung_dung.api.tuyen.phong import router as router_phong
from ung_dung.api.tuyen.danh_muc import router as router_danh_muc
from ung_dung.api.tuyen.xac_thuc import router as router_xac_thuc

ung_dung = FastAPI(
    title="Hệ thống quản lý phòng trọ",
    version="1.0.0",
)

# Cấu hình thư mục tài nguyên tĩnh
ung_dung.mount("/tai-nguyen", StaticFiles(directory="tai_nguyen"), name="tai_nguyen")
ung_dung.include_router(router_phong)
# Cấu hình thư mục giao diện
giao_dien = Jinja2Templates(directory="giao_dien")
ung_dung.include_router(router_danh_muc)
# Gắn các router API
ung_dung.include_router(router_xac_thuc)

# --- CÁC ROUTE GIAO DIỆN ---


@ung_dung.get("/quan-ly-phong", response_class=HTMLResponse)
async def giao_dien_quan_ly_phong(request: Request):
    return giao_dien.TemplateResponse(
        request=request, name="quan_ly_phong.html", context={}
    )


@ung_dung.get("/", response_class=HTMLResponse)
async def trang_chu(request: Request):
    """Tự động chuyển hướng về trang đăng nhập"""
    return RedirectResponse(url="/dang-nhap")


@ung_dung.get("/dang-nhap", response_class=HTMLResponse)
async def giao_dien_dang_nhap(request: Request):
    return giao_dien.TemplateResponse(
        request=request, name="dang_nhap.html", context={}
    )


@ung_dung.get("/dang-ky", response_class=HTMLResponse)
async def giao_dien_dang_ky(request: Request):
    return giao_dien.TemplateResponse(request=request, name="dang_ky.html", context={})


@ung_dung.get("/", response_class=HTMLResponse)
async def trang_chu(request: Request):
    """Tự động chuyển hướng về trang đăng nhập"""
    return RedirectResponse(url="/dang-nhap")


@ung_dung.get("/dang-nhap", response_class=HTMLResponse)
async def giao_dien_dang_nhap(request: Request):
    return giao_dien.TemplateResponse(
        request=request, name="dang_nhap.html", context={}
    )


@ung_dung.get("/dang-ky", response_class=HTMLResponse)
async def giao_dien_dang_ky(request: Request):
    return giao_dien.TemplateResponse(request=request, name="dang_ky.html", context={})


# THÊM ROUTE NÀY:
@ung_dung.get("/dashboard", response_class=HTMLResponse)
async def giao_dien_dashboard(request: Request):
    return giao_dien.TemplateResponse(
        request=request, name="dashboard.html", context={}
    )
