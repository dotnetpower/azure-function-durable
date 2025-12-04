import logging
import json
import azure.functions as func


def main(changes: func.SqlRowList) -> None:
    """
    SQL Trigger - SQL Database의 변경사항을 감지하여 트리거
    
    중요: DB 변경 추적을 위해 다음 명령 필수
    
    ALTER DATABASE [your database name]
    SET CHANGE_TRACKING = ON
    (CHANGE_RETENTION = 2 DAYS, AUTO_CLEANUP = ON);
    
    ALTER TABLE [dbo].[your table name]
    ENABLE CHANGE_TRACKING;
    
    Args:
        changes: SQL 변경 목록
    """
    # 보안: 변경된 데이터의 개수만 로그에 기록 (민감한 데이터 보호)
    change_count = sum(1 for _ in changes)
    logging.info(f"Python SQL trigger function processed {change_count} change(s).")
