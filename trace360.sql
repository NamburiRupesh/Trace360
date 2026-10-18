CREATE DATABASE trace360_db;
USE trace360_db;
show databases;
Show tables;

create table Role(
RoleID INT auto_increment primary key,
RoleName Varchar(50) NOT NULL UNIQUE
);

INSERT INTO Role(RoleName)
VALUES
('ADMIN'),
('MANUFACTURER'),
('SUPPLIER'),
('SERVICE_CENTER'),
('CUSTOMER');

Select *from Role
ORDER BY RoleID;
USE trace360_db;

CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(50) NOT NULL UNIQUE,
    Email VARCHAR(100) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    RoleID INT NOT NULL,
    Status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_role
        FOREIGN KEY (RoleID)
        REFERENCES Role(RoleID)
);

describe user;
USE trace360_db;

CREATE TABLE Manufacturer (
    ManufacturerID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL UNIQUE,
    CompanyName VARCHAR(100) NOT NULL,
    RegistrationNumber VARCHAR(100),
    GSTIN VARCHAR(20),

    CONSTRAINT fk_manufacturer_user
        FOREIGN KEY (UserID)
        REFERENCES User(UserID)
);

CREATE TABLE ServiceCenter (
    ServiceCenterID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL UNIQUE,
    CenterName VARCHAR(100) NOT NULL,
    LicenseNumber VARCHAR(100),
    Phone VARCHAR(20),

    CONSTRAINT fk_servicecenter_user
        FOREIGN KEY (UserID)
        REFERENCES User(UserID)
);


CREATE TABLE Product (
    ProductID VARCHAR(30) PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    Model VARCHAR(100) NOT NULL,
    SerialNumber VARCHAR(100) NOT NULL UNIQUE,
    ManufacturingDate DATE NOT NULL,
    BatchNumber VARCHAR(50),
    Category VARCHAR(50),

    ManufacturerID INT NOT NULL,

    Status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',

    DeactivationReason VARCHAR(255),
    DeactivatedAt TIMESTAMP NULL,
    DeactivatedBy INT NULL,

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_product_manufacturer
        FOREIGN KEY (ManufacturerID)
        REFERENCES Manufacturer(ManufacturerID),

    CONSTRAINT fk_product_deactivated_by
        FOREIGN KEY (DeactivatedBy)
        REFERENCES User(UserID)
);


CREATE TABLE ServiceHistory (
    ServiceID INT AUTO_INCREMENT PRIMARY KEY,

    ProductID VARCHAR(30) NOT NULL,
    ServiceCenterID INT NOT NULL,

    ServiceType VARCHAR(50) NOT NULL,
    ProblemReported TEXT,
    Diagnosis TEXT,
    ActionTaken TEXT,
    Remarks TEXT,

    ServiceDate DATE NOT NULL,
    Cost DECIMAL(10,2),

    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_service_product
        FOREIGN KEY (ProductID)
        REFERENCES Product(ProductID),

    CONSTRAINT fk_service_center
        FOREIGN KEY (ServiceCenterID)
        REFERENCES ServiceCenter(ServiceCenterID)
);

SHOW TABLES;

select *from  Manufacturer;
select *from Product;

INSERT INTO User
(
    Username,
    Email,
    PasswordHash,
    RoleID,
    Status
)
VALUES
(
    'dell_admin',
    'dell@example.com',
    'TEST_HASH',	
    2,
    'APPROVED'
);

SELECT UserID, Username, RoleID, Status
FROM User
WHERE Username = 'dell_admin';

INSERT INTO Manufacturer
(
    UserID,
    CompanyName,
    RegistrationNumber,
    GSTIN
)
VALUES
(
    1,
    'Dell Technologies',
    'REG-DELL-001',
    'GSTIN-DELL-001'
);

INSERT INTO Product
(
    ProductID,
    ProductName,
    Model,
    SerialNumber,
    ManufacturingDate,
    BatchNumber,
    Category,
    ManufacturerID
)
VALUES
(
    'TRC-2026-0001',
    'Dell Laptop',
    'Inspiron 15',
    'DELL-SN-10001',
    '2026-07-15',
    'BATCH-2026-07',
    'Laptop',
    1
);

SELECT * FROM Product;
show tables;

Select *from servicecenter




