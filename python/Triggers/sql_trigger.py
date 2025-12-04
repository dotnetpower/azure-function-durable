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
    logging.info("Python SQL trigger function processed changes.")
    
    for change in changes:
        logging.info(f"Change operation: {change['Operation']}")
        logging.info(f"Id: {change['Item']['Id']}")
        logging.info(f"Title: {change['Item']['title']}")
        logging.info(f"Url: {change['Item']['url']}")
        logging.info(f"Completed: {change['Item']['completed']}")
