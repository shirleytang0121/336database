Database:
    The database can be recreated by copy and pasting the content in Medico_DB.sql file to
    MySQL server;

Software Verification:
    Functions:
        - Only admin can manage/add/remove doctors and staffs
        - Login
            -> login with the username and password
            -> based on the permission level, different functions are shown after login
        - Sign up
            -> fill in the form to sign up 
            -> the username and password will be insert into users table with a permission
               level of 4
            -> the other information will be insert into patient profile

        -Patient:
            1. show profile
                -> profiles of the current patient is shown
            2. edit profile
                -> edit profile of the patient after fill in all the blank
                -> the patientprofile and users table are updated with new information
                -> changed profile will be shown in 'show profile'
            3. see doctor profiles
                -> check the available doctors
            4. make appointment
                -> make appointment after select a !date! and a doctor
                -> if you used an admin account to add a doctor, the lastname of doctor
                   will not immediately shown in make appointment select field.
                   You have to save the code to run it again and refresh the page
                   to show it.
            5. check appointment status
                -> the status of appointment including date, start time, end time,
                   and doctor id are shown

        -Doctor:
            1. show profile
                -> show the profile of the doctor logged in currently
            2. edit profile
                -> edit profile by filling in all the blanks
                -> changed profile will be shown in 'show profile'

        -Staff:
            1. approve/reject appointment
                -> if the appointment is approved, the status in appointment table is 
                   changed to approved. Same thing happens to reject.

        -Admin:
            1. add Staff
                -> add staff to the system after fill in the form
            2. add doctor
                -> add doctor to the system after fill in the form
            3. list all users
                -> list all users with their permission level and username
            4. remove any users from the system
                -> after delete button is clicked, that user is removed from the system
        
Schemas: 
    users(id, username, password, permission_level)
    receptionist(id, firstname, lastname)
    Administrator(id, firstname, lastname)
    doctorProfile(id, firstname, lastname, specialization, startTime, endTime, descriptions)
    appointment(id, date, startTime, endTime, status, doctor_id, patient_id)
    patientProfile(id, firstname, lastname, email, phone_number, address, DOB, gender)
    insurance(patient_id, insurance_company, insurance_id, group_name)
