from fastapi import APIRouter, File, UploadFile

router = APIRouter()

@router.post("/")
async def upload(file: UploadFile = File(...)):
    try:
        content = await file.read()
        with open(f'static/{file.filename}', 'wb') as f:
            f.write(content)
    except Exception as error:
        return {
            "message": "There was an error when uploading the file"
        }
    finally:
        await file.close()
    return {"file_url": f'static/{file.filename}' }, 200
    # return "0.0.0.0:8085/static/" + file.filename
        