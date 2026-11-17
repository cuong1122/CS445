import uvicorn

if __name__ == "__main__":
    uvicorn.run("ung_dung.main:ung_dung", host="127.0.0.1", port=1836, reload=True)
