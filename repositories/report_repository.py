from sqlalchemy.orm import Session
from models.report import Report
from schemas.report import Report as ReportSchema
from schemas.add_report import AddReport
from models.group import Group  # Assuming the Group model exists

class ReportRepository:

    @staticmethod
    def get_all(db: Session):
        reports = db.query(Report).all()
        return [ReportSchema(
            report_id=r.report_id,
            report_reason=r.report_reason,
            report_desc=r.report_desc
        ) for r in reports]

    @staticmethod
    def get_by_id(db: Session, report_id: int):
        report = db.query(Report).filter(Report.report_id == report_id).first()
        if report:
            return ReportSchema(
                report_id=report.report_id,
                report_reason=report.report_reason,
                report_desc=report.report_desc
            )
        return None

    @staticmethod
    def get_by_group_id(db: Session, group_id: int):
        reports = db.query(Report).filter(Report.group_id == group_id).all()
        return [ReportSchema(
            report_id=r.report_id,
            report_reason=r.report_reason,
            report_desc=r.report_desc
        ) for r in reports]

    @staticmethod
    def add_report(db: Session, group_id: int, report_data: AddReport):
        # Check if the group exists
        group_exists = db.query(Group).filter(Group.group_id == group_id).first()
        if not group_exists:
            return None

        new_report = Report(
            group_id=group_id,
            report_reason=report_data.report_reason,
            report_desc=report_data.report_desc
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
        return new_report

    @staticmethod
    def delete_report(db: Session, report_id: int):
        report = db.query(Report).filter(Report.report_id == report_id).first()
        if not report:
            return False
        db.delete(report)
        db.commit()
        return True
