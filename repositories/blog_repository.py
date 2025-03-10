from sqlalchemy.orm import Session
from models import Blog
from schemas import BlogDto
from typing import List, Optional
import os

class BlogRepository:
    def __init__(self, db: Session, image_folder_path: str):
        self.db = db
        self.image_folder_path = image_folder_path

    def get_all_blogs(self) -> List[Blog]:
        blogs = self.db.query(Blog).all()
        for blog in blogs:
            blog.image_con = self.get_image(blog.image)
        return blogs

    def get_blog_by_id(self, id: int) -> Optional[Blog]:
        blog = self.db.query(Blog).filter(Blog.id == id).first()
        if blog:
            blog.image_con = self.get_image(blog.image)
        return blog

    def add_blog(self, blog_dto: BlogDto) -> Blog:
        new_blog = Blog(**blog_dto.model_dump())
        self.db.add(new_blog)
        self.db.commit()
        self.db.refresh(new_blog)
        return new_blog

    def update_blog(self, id: int, blog_dto: BlogDto) -> Optional[Blog]:
        blog = self.db.query(Blog).filter(Blog.id == id).first()
        if blog:
            for key, value in blog_dto.model_dump().items():
                if value:
                    setattr(blog, key, value)
            self.db.commit()
            self.db.refresh(blog)
        return blog

    def delete_blog(self, id: int) -> bool:
        blog = self.db.query(Blog).filter(Blog.id == id).first()
        if blog:
            self.db.delete(blog)
            self.db.commit()
            return True
        return False

    def get_image(self, image_name: str) -> Optional[bytes]:
        file_path = os.path.join(self.image_folder_path, image_name)
        return open(file_path, 'rb').read() if os.path.exists(file_path) else None
