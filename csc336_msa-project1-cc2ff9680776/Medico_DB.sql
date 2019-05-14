CREATE DATABASE medico;
USE medico;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS receptionist;
DROP TABLE IF EXISTS administrator;
DROP TABLE IF EXISTS patientprofile;
DROP TABLE IF EXISTS doctorprofile;
DROP TABLE IF EXISTS insurance;
DROP TABLE IF EXISTS appointment;

CREATE TABLE users(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(128),
    password VARCHAR(128),
    permission_level INT
);

CREATE TABLE receptionist(
    id INT NOT NULL PRIMARY KEY,
    firstname VARCHAR(128),
    lastname VARCHAR(128),
    FOREIGN KEY (id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE administrator(
    id INT NOT NULL PRIMARY KEY,
    firstname VARCHAR(128),
    lastname VARCHAR(128),
    FOREIGN KEY (id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
); 

CREATE TABLE patientprofile(
    id INT NOT NULL PRIMARY KEY,
    firstname VARCHAR(128),
    lastname VARCHAR(128),
    email VARCHAR(128),
    phone_number VARCHAR(128),
    address VARCHAR(128),
    gender VARCHAR(128),
    date_of_birth VARCHAR(128),
    register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE doctorprofile(
    id INT NOT NULL PRIMARY KEY,
    firstname VARCHAR(128),
    lastname VARCHAR(128),
    specialization VARCHAR(128),
    startTime VARCHAR(128),
    endTime VARCHAR(128),
    descriptions VARCHAR(128),
    FOREIGN KEY (id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE insurance(
    patient_id INT NOT NULL PRIMARY KEY,
    insurance_company VARCHAR(128),
    insurance_id INT,
    group_name VARCHAR(128),
    FOREIGN KEY (patient_id) REFERENCES patientprofile(id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE appointment(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    date VARCHAR(128),
    startTime VARCHAR(128),
    endTime VARCHAR(128),
    status VARCHAR(128),
    doctor_id INT,
    patient_id INT,
    register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (doctor_id) REFERENCES doctorprofile(id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (patient_id) REFERENCES patientprofile(id) ON UPDATE CASCADE ON DELETE CASCADE
);

INSERT INTO users (username, password, permission_level) VALUES ('admin', 'admin', 1);
INSERT INTO administrator(id, firstname, lastname) VALUES (1, 'admin', 'admin');


DELIMITER $$ 
CREATE PROCEDURE SelectDoctorLastname() 
    BEGIN 
    SELECT lastname FROM doctorprofile;
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE SelectDoctors(IN lastname_t VARCHAR(128)) 
    BEGIN SELECT id FROM doctorprofile WHERE lastname = lastname_t; 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE SelectDoctorProfile(IN id_t INT) 
    BEGIN SELECT * FROM doctorprofile WHERE id = id_t; 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE SelectAllDoctors() 
    BEGIN SELECT * FROM doctorprofile; 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE SelectLastInsertID() 
    BEGIN SELECT LAST_INSERT_ID(); 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE SelectUsers(IN username_t VARCHAR(128)) 
    BEGIN SELECT * FROM users WHERE username = username_t; 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE SelectAppointmentInfo() 
    BEGIN SELECT * FROM appointment; 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE SelectAllUsers() 
    BEGIN SELECT * FROM users; 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE SelectInsuranceInfo(IN patient_id_t INT) 
    BEGIN SELECT * FROM insurance WHERE patient_id = patient_id_t; 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE SelectUsersID(IN id_t INT) 
    BEGIN SELECT * FROM users WHERE id = id_t; 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE SelectPatientProfile(IN id_t INT) 
    BEGIN SELECT * FROM patientprofile WHERE id = id_t; 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE SelectAppointmentStatus(IN id_t INT) 
    BEGIN SELECT * FROM ShowAppointment WHERE patient_id = id_t; 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE InsertUser(IN username_t VARCHAR(128), IN password_t VARCHAR(128), 
    IN permission INT) 
    BEGIN 
    INSERT INTO users(username, password, permission_level) VALUES(username_t, password_t, permission); 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE InsertPatientProfile(IN id_t INT, IN firstname_t VARCHAR(128), 
    IN lastname_t VARCHAR(128), IN email_t VARCHAR(128), IN phone_number_t VARCHAR(128),
    IN address_t VARCHAR(128), IN gender_t VARCHAR(128), IN date_of_birth_t VARCHAR(128)) 
    BEGIN 
    INSERT INTO patientProfile(id, firstname, lastname, email, 
                phone_number, address, gender, date_of_birth) 
                VALUES(id_t, firstname_t, lastname_t, email_t, 
                phone_number_t, address_t, gender_t, date_of_birth_t);
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE InsertInsurancePatientID(IN id_t INT) 
    BEGIN 
    INSERT INTO insurance(patient_id) VALUES(id_t); 
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE InsertStaff(IN id_t INT, IN firstname_t VARCHAR(128), IN lastname_t VARCHAR(128)) 
    BEGIN 
    INSERT INTO receptionist(id, firstname, lastname) VALUES(id_t, firstname_t, lastname_t);
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE InsertDoctorProfile(IN id_t INT, IN firstname_t VARCHAR(128), 
    IN lastname_t VARCHAR(128), IN specialization_t VARCHAR(128), IN startTime_t VARCHAR(128),
    IN endTime_t VARCHAR(128), IN description_t VARCHAR(128)) 
    BEGIN 
    INSERT INTO doctorprofile(id, firstname, lastname, specialization, startTime, 
                endTime, descriptions) VALUES(id_t, firstname_t, lastname_t, 
                specialization_t, startTime_t, endTime_t, descriptions_t);
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE InsertAppointment(IN date_t VARCHAR(128), IN startTime_t VARCHAR(128), 
    IN endTime_t VARCHAR(128), IN status_t VARCHAR(128), IN doctor_id_t INT, IN patient_id_t INT) 
    BEGIN 
    INSERT INTO appointment(date, startTime, endTime, status, doctor_id, patient_id) 
                VALUES(date_t, startTime_t, endTime_t, status_t, doctor_id_t, patient_id_t);
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE InsertInsuranceInfo(IN patient_id_t INT, IN insurance_company_t VARCHAR(128), 
    IN insurance_id_t INT, IN group_name_t VARCHAR(128)) 
    BEGIN 
    INSERT INTO insurance(patient_id, insurance_company, insurance_id, group_name) 
                VALUES(patient_id_t, insurance_company_t, insurance_id_t, group_name_t);
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE DeleteUser(IN user_id INT) 
    BEGIN DELETE FROM users WHERE id = user_id;
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE UpdateAppointment(IN status_t VARCHAR(128), IN id_t INT) 
    BEGIN UPDATE appointment SET status = status_t WHERE id = id_t;
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE UpdateDoctorProfile(IN firstname_t VARCHAR(128), IN lastname_t VARCHAR(128), 
    IN specialization_t VARCHAR(128), IN startTime_t VARCHAR(128), IN endTime_t VARCHAR(128), 
    IN description_t VARCHAR(128), IN id_t INT) 
    BEGIN 
    UPDATE doctorprofile SET firstname = firstname_t, lastname = lastname_t,
        specialization = specialization_t, startTime = startTime_t, endTime = endTime_t, 
        descriptions = description_t WHERE id = id_t;
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE UpdateUser(IN username_t VARCHAR(128), IN password_t VARCHAR(128), IN id_t INT) 
    BEGIN UPDATE users SET username = username_t, password = password_t WHERE id = id_t;
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE UpdatePatientProfile(IN firstname_t VARCHAR(128), 
    IN lastname_t VARCHAR(128), IN email_t VARCHAR(128), IN phone_number_t VARCHAR(128),
    IN address_t VARCHAR(128), IN id_t INT) 
    BEGIN 
    UPDATE patientprofile SET firstname = firstname_t, lastname = lastname_t, email = email_t, 
        phone_number = phone_number_t, address = address_t WHERE id = id_t;
    END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE UpdateInsurance(IN insurance_company_t VARCHAR(128), 
    IN insurance_id_t INT, IN group_name_t VARCHAR(128), IN patient_id_t INT)
    BEGIN 
    UPDATE insurance SET insurance_company = insurance_company_t, insurance_id = insurance_id_t, 
        group_name = group_name_t WHERE patient_id = patient_id_t;
    END $$
DELIMITER ;

CREATE VIEW ShowAppointment AS
    SELECT appointment.id, appointment.patient_id, appointment.date, appointment.startTime, appointment.endTime,
    doctorprofile.firstname, doctorprofile.lastname, appointment.status FROM appointment 
    INNER JOIN doctorprofile ON appointment.doctor_id = doctorprofile.id GROUP BY appointment.id;


DELIMITER $$
CREATE TRIGGER patientDOBTrigger
BEFORE INSERT ON patientprofile
FOR EACH ROW
IF NEW.date_of_birth>CURRENT_TIMESTAMP
    THEN SET NEW.date_of_birth=CURRENT_TIMESTAMP;
END IF; $$
DELIMITER ;


DELIMITER $$
CREATE FUNCTION givePermission (userIndentity VARCHAR(128))
    RETURNS INT
IF(userIndentity='admin') THEN
    RETURN 1;
ELSEIF(userIndentity='staff') THEN
    RETURN 2;
ELSEIF(userIndentity='doctor') THEN
    RETURN 3;
ELSEIF(userIndentity='patient') THEN
    RETURN 4;
END IF;$$
DELIMITER ;

DELIMITER $$
CREATE FUNCTION giveIndentity (permission_level INT)
    RETURNS VARCHAR(128)
IF(permission_level=1) THEN
    RETURN 'admin';
ELSEIF(permission_level=2) THEN
    RETURN 'staff';
ELSEIF(permission_level=3) THEN
    RETURN 'doctor';
ELSEIF(permission_level=4) THEN
    RETURN 'patient';
END IF;$$
DELIMITER ;

DELIMITER $$ 
CREATE PROCEDURE GetUserIdentity(
    IN  the_id INT,
    OUT userIndentity  varchar(128)
)
BEGIN
    DECLARE the_pl DOUBLE;
 
    SELECT permission_level INTO the_pl
    FROM users
    WHERE id=the_id;
 
    SELECT GetUserIdentity(the_pl) 
    INTO userIndentity;
 
END
