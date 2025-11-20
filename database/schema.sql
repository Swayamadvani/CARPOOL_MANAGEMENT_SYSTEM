--  Drivers Table
CREATE TABLE Drivers (
    driver_id INT AUTO_INCREMENT PRIMARY KEY,
    driver_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15),
    license_number VARCHAR(50)
);
-- Rides Table
CREATE TABLE Rides (
    ride_id INT AUTO_INCREMENT PRIMARY KEY,
    pickup_location VARCHAR(100) NOT NULL,
    drop_location VARCHAR(100) NOT NULL,
    driver_id INT,
    no_of_seats INT NOT NULL,
    persons INT DEFAULT 0,
    FOREIGN KEY (driver_id) REFERENCES Drivers(driver_id) ON DELETE CASCADE
);

--  Users Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    pickup VARCHAR(100),
    drop_location VARCHAR(100),
    ride_id INT,
    FOREIGN KEY (ride_id) REFERENCES Rides(ride_id) ON DELETE SET NULL
);

--  Payments Table (optional)
CREATE TABLE Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10,2),
    status VARCHAR(20),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- ---------------------------------------------------------------
-- ✅ STORED PROCEDURES
-- ---------------------------------------------------------------

-- Add user to an existing ride automatically
DROP PROCEDURE IF EXISTS AddUserAutoRide;
DELIMITER //
CREATE PROCEDURE AddUserAutoRide(
    IN p_name VARCHAR(100),
    IN p_age INT,
    IN p_pickup VARCHAR(100),
    IN p_drop VARCHAR(100)
)
BEGIN
    DECLARE r_id INT DEFAULT NULL;

    -- Find available ride
    SELECT ride_id
    INTO r_id
    FROM Rides
    WHERE pickup_location = p_pickup
      AND drop_location = p_drop
      AND persons < no_of_seats
    ORDER BY ride_id
    LIMIT 1;

    -- If no ride is found or rides are full, throw an error
    IF r_id IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No available rides for this route or all rides are full.';
    ELSE
        -- Assign user to existing ride
        INSERT INTO Users (name, age, pickup, drop_location, ride_id)
        VALUES (p_name, p_age, p_pickup, p_drop, r_id);

        -- Update person count
        UPDATE Rides
        SET persons = persons + 1
        WHERE ride_id = r_id;
    END IF;
END //
DELIMITER ;

-- ---------------------------------------------------------------
-- Add a new ride manually
DROP PROCEDURE IF EXISTS AddRide;
DELIMITER //
CREATE PROCEDURE AddRide(
    IN p_pickup VARCHAR(100),
    IN p_drop VARCHAR(100),
    IN p_driver_name VARCHAR(100),
    IN p_driver_phone VARCHAR(15),
    IN p_license VARCHAR(50),
    IN p_no_of_seats INT
)
BEGIN
    DECLARE d_id INT;

    -- Add or find driver
    SELECT driver_id INTO d_id FROM Drivers
    WHERE driver_name = p_driver_name
    LIMIT 1;

    IF d_id IS NULL THEN
        INSERT INTO Drivers (driver_name, phone_number, license_number)
        VALUES (p_driver_name, p_driver_phone, p_license);
        SET d_id = LAST_INSERT_ID();
    END IF;

    -- Create ride
    INSERT INTO Rides (pickup_location, drop_location, driver_id, no_of_seats, persons)
    VALUES (p_pickup, p_drop, d_id, p_no_of_seats, 0);
END //
DELIMITER ;

-- ---------------------------------------------------------------
-- Remove a user by ID
DROP PROCEDURE IF EXISTS RemoveUser;
DELIMITER //
CREATE PROCEDURE RemoveUser(IN p_user_id INT)
BEGIN
    DECLARE ride_ref INT;
    SELECT ride_id INTO ride_ref FROM Users WHERE user_id = p_user_id;

    IF ride_ref IS NOT NULL THEN
        UPDATE Rides
        SET persons = persons - 1
        WHERE ride_id = ride_ref AND persons > 0;
    END IF;

    DELETE FROM Users WHERE user_id = p_user_id;
END //
DELIMITER ;

-- ---------------------------------------------------------------
-- Remove a ride by ID
DROP PROCEDURE IF EXISTS RemoveRide;
DELIMITER //
CREATE PROCEDURE RemoveRide(IN p_ride_id INT)
BEGIN
    DELETE FROM Rides WHERE ride_id = p_ride_id;
END //
DELIMITER ;

-- --------------------b-------------------------------------------
-- VIEW QUERIES (for GUI)
-- ---------------------------------------------------------------

-- View all users
SELECT * FROM Users;

-- View all rides with driver info
SELECT Rides.ride_id, pickup_location, drop_location, no_of_seats, persons,
       Drivers.driver_name, Drivers.phone_number
FROM Rides
JOIN Drivers ON Rides.driver_id = Drivers.driver_id;

