USE flight;

-- (1)插入用户账号和密码
INSERT INTO users(User_ID, User_Name, Creation_Date, Password, Email)
VALUES ('user123', 'John', CURRENT_TIMESTAMP, '12345678', 'john@example.com');

-- (2)通过用户ID重置密码
UPDATE Users
SET Password = 'new_hashed_password' 
WHERE User_ID = 'user123';

-- (3)插入用户购买机票的订单
INSERT INTO Orders (Flight_ID, Passenger_ID, Order_Date, Status)
VALUES (1, 1,  CURRENT_TIMESTAMP, 'Purchased'); -- Purchased /Reserved/Cancelled
-- 更新航班座位数减1
UPDATE Flights
SET Available_Seats = Available_Seats - 1
WHERE Flight_ID = 1; -- 使用实际的航班ID

-- (3)预订机票
INSERT INTO Orders (Flight_ID, Passenger_ID, Order_Date, Status)
VALUES (1, 1, CURRENT_TIMESTAMP, 'Reserved');
-- 更新航班座位数减1
UPDATE Flights
SET Available_Seats = Available_Seats - 1
WHERE Flight_ID = 1; -- 使用实际的航班ID

-- (4)将订单状态改为已退票
UPDATE Orders
SET Status = 'Refunded'
WHERE Order_ID = your_order_id; -- 使用实际的订单ID
-- 更新航班座位数加1
UPDATE Flights
SET Available_Seats = Available_Seats + 1
WHERE Flight_ID = 1; -- 使用实际的航班ID

-- （5）发送机票请求到客户支持，并关联航班信息
INSERT INTO CustomerSupport (Support_User_ID, Title, Description, Ticket_Date, Flight_ID)
VALUES ('customer123', 'Ticket Assistance', 'I need help with my flight booking.',CURRENT_TIMESTAMP, 1);

-- （6）检查可用航班
SELECT Flight_ID, Departure_City, Arrival_City, Departure_Date, Available_Seats,Flight_Company
FROM Flights
WHERE Available_Seats > 0;

-- 插入航班信息
INSERT INTO flights (Flight_ID, Departure_City, Arrival_City, Departure_Date, Available_Seats, Flight_Company)
VALUES (1, 'CityA', 'CityB', '2023-12-10 08:00:00', 100, 'AirlineX'),
       (2, 'CityC', 'CityD', '2023-12-12 10:30:00', 150, 'AirlineY');

-- 插入乘客信息
INSERT INTO passengers (Passenger_ID, First_Name, Last_Name, Email)
VALUES (1, 'Alice', 'Smith', 'alice@example.com'),
       (2, 'Bob', 'Johnson', 'bob@example.com');

-- 插入订单信息
INSERT INTO orders (Flight_ID, Passenger_ID, Order_Date, Status)
VALUES (1, 1, '2023-12-02 14:00:00', 'Purchased'),
       (2, 2, '2023-12-05 09:45:00', 'Reserved');

-- 插入客服信息
INSERT INTO customersupport (Support_User_ID, Title, Description, Ticket_Date, Flight_ID)
VALUES ('support123', 'Assistance', 'Need help with booking', '2023-12-04 11:30:00', 1);



