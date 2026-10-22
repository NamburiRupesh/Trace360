-- Trace360: Stored procedure and trigger setup
-- This script is specifically for the live Trace360 database: trace360_db1.
-- Run the entire script in MySQL Workbench (supports DELIMITER).

USE trace360_db1;

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

-- Verify the database objects:
-- SHOW PROCEDURE STATUS WHERE Db = DATABASE();
-- SHOW TRIGGERS;
-- SELECT * FROM ServiceHistoryAudit ORDER BY AuditID DESC;
