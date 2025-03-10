# from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
# from sqlalchemy.orm import Session
# from database import get_db
# from schemas import BlogCreate, BlogResponse
# from repositories.blog_repository import BlogRepository
# from helpers.file_helper import FileHelper

# router = APIRouter(prefix="/blogs", tags=["Blogs"])

# @router.get("/", response_model=list[BlogResponse])
# def get_all_blogs(db: Session = Depends(get_db)):
#     return BlogRepository.get_all(db)

# @router.get("/{id}", response_model=BlogResponse)
# def get_blog_by_id(id: int, db: Session = Depends(get_db)):
#     blog = BlogRepository.get_by_id(db, id)
#     if not blog:
#         raise HTTPException(status_code=404, detail="Blog not found")
#     return blog

# @router.post("/", response_model=BlogResponse)
# async def add_blog(
#     title: str = Form(...),
#     content: str = Form(...),
#     image: UploadFile = None,
#     db: Session = Depends(get_db)
# ):
#     image_path = None
#     if image:
#         image_path = await FileHelper.save_image(image)
    
#     new_blog = BlogCreate(title=title, content=content, image=image_path)
#     return BlogRepository.add_blog(db, new_blog)

# @router.put("/{id}", response_model=BlogResponse)
# async def update_blog(
#     id: int,
#     title: str = Form(...),
#     content: str = Form(...),
#     image: UploadFile = None,
#     db: Session = Depends(get_db)
# ):
#     existing_blog = BlogRepository.get_by_id(db, id)
#     if not existing_blog:
#         raise HTTPException(status_code=404, detail="Blog not found")

#     image_path = existing_blog.image
#     if image:
#         await FileHelper.delete_image(image_path)
#         image_path = await FileHelper.save_image(image)

#     updated_blog = BlogCreate(title=title, content=content, image=image_path)
#     return BlogRepository.update_blog(db, id, updated_blog)

# @router.delete("/{id}")
# def delete_blog(id: int, db: Session = Depends(get_db)):
#     if not BlogRepository.delete_blog(db, id):
#         raise HTTPException(status_code=404, detail="Blog not found")
#     return {"message": "Blog deleted successfully"}
