-- Trace360: Stored procedure and trigger setup
-- IMPORTANT:
-- 1. Select the SAME database that database.py connects to before running this script.
-- 2. In the current repository, database.py uses trace360_db1, while trace360.sql creates trace360_db.
--    Confirm which database contains your live Trace360 tables before executing.
-- 3. Run this script in MySQL Workbench (or another SQL client that supports DELIMITER).

CREATE TABLE IF NOT EXISTS ServiceHistoryAudit (
    AuditID INT AUTO_INCREMENT PRIMARY KEY,
    ServiceID INT NOT NULL,
    ProductID VARCHAR(30) NOT NULL,
    ActionType VARCHAR(10) NOT NULL,
    ChangedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP PROCEDURE IF EXISTS GetProductLifecycle;

DELIMITER //

CREATE PROCEDURE GetProductLifecycle(
    IN p_ProductID VARCHAR(30)
)
BEGIN
    SELECT
        sh.ServiceID,
        sh.ProductID,
        sh.ServiceType,
        sh.ProblemReported,
        sh.Diagnosis,
        sh.ActionTaken,
        sh.Remarks,
        sh.ServiceDate,
        sh.Cost,
        sc.CenterName
    FROM ServiceHistory AS sh
    INNER JOIN ServiceCenter AS sc
        ON sh.ServiceCenterID = sc.ServiceCenterID
    WHERE sh.ProductID = p_ProductID
    ORDER BY sh.ServiceDate ASC, sh.ServiceID ASC;
END //

DELIMITER ;

DROP TRIGGER IF EXISTS AfterServiceInsert;

DELIMITER //

CREATE TRIGGER AfterServiceInsert
AFTER INSERT ON ServiceHistory
FOR EACH ROW
BEGIN
    INSERT INTO ServiceHistoryAudit (
        ServiceID,
        ProductID,
        ActionType
    )
    VALUES (
        NEW.ServiceID,
        NEW.ProductID,
        'INSERT'
    );
END //

DELIMITER ;

-- Verify the database objects after running this script:
-- SHOW PROCEDURE STATUS WHERE Db = DATABASE();
-- SHOW TRIGGERS;
-- SELECT * FROM ServiceHistoryAudit ORDER BY AuditID DESC;
