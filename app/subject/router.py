from fastapi import APIRouter
from typing import *
from .models import Subject
from .service import *
import traceback
from fastapi import HTTPException

router = APIRouter()

@router.get("/get-subjects")
def route_get_subjects(search_text:str="", page_size:int=10, page_index:int=1)->List[Subject]:
    try: 
        data = get_subjects(search_text, page_size, page_index)
        return data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail = str(e))

@router.get("/get-subject-by-id")
def route_get_subject_by_id(subject_id:str)->Subject:
    try: 
        data = get_subject(subject_id)
        return data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail = str(e))
    
@router.post("/insert-subject")
def route_insert_subject(subject:Subject)->str:
    try: 
        data = insert_subject(subject.dict())
        return data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail = str(e))

@router.post("/update-subject")
def route_update_subject(subject: Subject)->int:
    try: 
        data = update_subject(subject.sub_id, subject.dict())
        return data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail = str(e))

@router.post("/delete-subject")
def route_delete_subject(sub_ids:list[str])->int:
    try: 
        data = delete_subjects(sub_ids)
        return data
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail = str(e))