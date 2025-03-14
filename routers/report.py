from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas.report import Report as ReportSchema
from schemas.add_report import AddReport
from repositories.report_repository import ReportRepository

router = APIRouter(prefix="/report", tags=["Reports"])


@router.get("/", response_model=List[ReportSchema])
def get_all_reports(db: Session = Depends(get_db)):
    return ReportRepository.get_all(db)


@router.get("/{id}", response_model=ReportSchema)
def get_report_by_id(id: int, db: Session = Depends(get_db)):
    report = ReportRepository.get_by_id(db, id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/group/{group_id}", response_model=List[ReportSchema])
def get_reports_by_group_id(group_id: int, db: Session = Depends(get_db)):
    return ReportRepository.get_by_group_id(db, group_id)


@router.post("/", response_model=ReportSchema)
def add_report(group_id: int, report_data: AddReport, db: Session = Depends(get_db)):
    report = ReportRepository.add_report(db, group_id, report_data)
    if report is None:
        raise HTTPException(status_code=400, detail="Invalid Group ID")
    return report


@router.delete("/{id}")
def delete_report(id: int, db: Session = Depends(get_db)):
    success = ReportRepository.delete_report(db, id)
    if not success:
        raise HTTPException(status_code=400, detail="Report Not Valid")
    return {"message": "Report Deleted"}
