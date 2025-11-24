import os
import tempfile
import subprocess
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/add-emoji")
async def add_emoji(file: UploadFile = File(...)):
    # принимаем только mp4
    if file.content_type != "video/mp4":
        raise HTTPException(status_code=400, detail="Only .mp4 files are allowed")

    # создаём временную директорию, всё в ней удалится автоматически
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.mp4")
        output_path = os.path.join(tmpdir, "output.mp4")

        # сохраняем входной файл
        with open(input_path, "wb") as f:
            f.write(await file.read())

        # команда ffmpeg как список аргументов
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-vf",
            (
                "drawtext=text='😀':"
                "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                "fontsize=72:"
                "x=(w-text_w)/2:y=(h-text_h)/2:"
                "fontcolor=white"
            ),
            "-codec:a",
            "copy",
            output_path,
        ]

        try:
            subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError:
            raise HTTPException(status_code=500, detail="ffmpeg processing error")

        # отдаём файл клиенту
        return FileResponse(
            output_path,
            media_type="video/mp4",
            filename="output.mp4",
        )
