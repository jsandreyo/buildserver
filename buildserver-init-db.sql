-- ----------------------------------------------------
-- Author: John Andreyo
-- Copyright: Copyright (c) 2024. All rights reserved.
-- License: Please see LICENSE file in program's root.
-- Version: 2.0
-- ----------------------------------------------------

-- DB INIT SCRIPT --

-- -- INTERNAL TO CONTAINER 
-- CREATE USER '<user>'@'localhost' IDENTIFIED BY '<password>';
-- GRANT ALL ON *.* TO '<user>'@'localhost';
-- FLUSH PRIVILEGES;
-- -- EXTERNAL TO CONTAINER
-- CREATE USER '<user>'@'%' IDENTIFIED BY '<password>';
-- GRANT ALL ON *.* TO '<user>'@'%';
-- FLUSH PRIVILEGES;
                              
SET GLOBAL max_allowed_packet=1280000000;
SET GLOBAL net_buffer_length=1280000;

SET GLOBAL connect_timeout=25600000;
SET GLOBAL interactive_timeout=25600000;
SET GLOBAL wait_timeout=25600000;

SET GLOBAL innodb_io_capacity = 100;
SET GLOBAL innodb_buffer_pool_size = 512000000;
                         
SET GLOBAL host_cache_size = 0;
SET GLOBAL log_output = 'file'; 

CREATE DATABASE db;
use db;

CREATE TABLE Programs(
    BuildReqID int not null AUTO_INCREMENT,
    CommitID varchar(100) NOT NULL,
    ProgramName varchar(100) NOT NULL,
    Status varchar(100) NOT NULL,
    RegistrationID char (36) NULL,
    BinaryObject BLOB DEFAULT NULL,
    PRIMARY KEY (BuildReqID)
);

create TABLE Params(
    ParamName varchar(100) not null,
    ParamValue tinyint(1)
);

INSERT INTO Params VALUES ("is_o_mode_in_use", 0);
INSERT INTO Params VALUES ("is_a_mode_in_use", 0);  
INSERT INTO Params VALUES ("is_a_cycle_in_prog", 0);