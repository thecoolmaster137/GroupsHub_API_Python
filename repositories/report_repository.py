from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Report, Group  # Assuming these models are defined in models.py
from schemas import ReportDTO, AddReportDTO  # Assuming these schemas are defined in schemas.py

def get_all_reports(db: Session):
    reports = db.query(Report).all()
    return [ReportDTO(report_id=r.id, report_reason=r.report_reason, report_desc=r.report_desc) for r in reports]

def get_report_by_id(db: Session, report_id: int):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportDTO(report_id=report.id, report_reason=report.report_reason, report_desc=report.report_desc)

def get_reports_by_group_id(db: Session, group_id: int):
    reports = db.query(Report).filter(Report.group_id == group_id).all()
    return [ReportDTO(report_id=r.id, report_reason=r.report_reason, report_desc=r.report_desc) for r in reports]

def add_report(db: Session, group_id: int, report_data: AddReportDTO):
    group_exists = db.query(Group).filter(Group.id == group_id).first()
    if not group_exists:
        raise HTTPException(status_code=404, detail="Group not found")
    
    new_report = Report(
        group_id=group_id,
        report_reason=report_data.report_reason,
        report_desc=report_data.report_desc
    )
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report

def delete_report(db: Session, report_id: int):
    report = db.query(Report).filter(Report.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    db.delete(report)
    db.commit()
    return {"message": "Report deleted successfully"}
