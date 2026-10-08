import mysql.connector
import random
import string
import sys

# Globals
connection = None
cursor = None
admin_password = "Verstappen@1"
db_password=input("Enter your Database Password: ")

# ---------- Database connect / setup ----------
def connect_database():
    global connection, cursor
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=db_password,
            database="AutoSpec Database System"
        )
        cursor = connection.cursor(buffered=True)
        print("✓ Connected to database successfully!")
        return True
    except mysql.connector.Error as err:
        if getattr(err, "errno", None) == 1049:
            print("✓ Database doesn't exist. Creating database...")
            create_database()
            return connect_database()
        else:
            print("• Error connecting to database:", err)
            return False

def create_database():
    try:
        temp_conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Verstappen@1"
        )
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("CREATE DATABASE IF NOT EXISTS AutoSpec_Database_System")
        temp_cursor.execute("USE AutoSpec_Database_System")

        # ===================== Tables Insertion =====================
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS brands (
                brand_id INT AUTO_INCREMENT PRIMARY KEY,
                brand_name VARCHAR(50) UNIQUE NOT NULL,
                country_of_origin VARCHAR(50),
                year_founded INT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS models (
                model_id INT AUTO_INCREMENT PRIMARY KEY,
                brand_id INT,
                model_name VARCHAR(100) NOT NULL,
                body_type VARCHAR(50),
                category VARCHAR(50),
                FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE
            )
        """)
        
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS variants (
                variant_id INT AUTO_INCREMENT PRIMARY KEY,
                model_id INT,
                variant_name VARCHAR(150) NOT NULL,
                price_inr DECIMAL(15,2),
                engine VARCHAR(200),
                power_bhp INT,
                torque_nm INT,
                top_speed_kmh INT,
                acceleration_0_100 DECIMAL(4,2),
                transmission VARCHAR(100),
                drivetrain VARCHAR(50),
                fuel_type VARCHAR(50),
                mileage_range VARCHAR(50),
                seating_capacity INT,
                safety_rating VARCHAR(50),
                FOREIGN KEY (model_id) REFERENCES models(model_id) ON DELETE CASCADE
            )
        """)
        
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS features (
                feature_id INT AUTO_INCREMENT PRIMARY KEY,
                variant_id INT,
                feature_category VARCHAR(50),
                feature_description TEXT,
                FOREIGN KEY (variant_id) REFERENCES variants(variant_id) ON DELETE CASCADE
            )
        """)
        
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS colors (
                color_id INT AUTO_INCREMENT PRIMARY KEY,
                variant_id INT,
                color_name TEXT,
                color_type VARCHAR(50),
                FOREIGN KEY (variant_id) REFERENCES variants(variant_id) ON DELETE CASCADE
            )
        """)
        
        temp_cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id VARCHAR(20) PRIMARY KEY,
                variant_id INT,
                customer_name VARCHAR(100),
                customer_contact VARCHAR(20),
                customer_email TEXT,
                booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'Active',
                FOREIGN KEY (variant_id) REFERENCES variants(variant_id)
            )
        """)
        
        temp_conn.commit()
        print("✓ Database and tables created successfully!")

        insert_sample_data(temp_cursor, temp_conn)

        temp_cursor.close()
        temp_conn.close()
        
    except mysql.connector.Error as err:
        print("• Error creating database:", err)
        sys.exit(1)

def close_connection():
    try:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
        print("✓ Database connection closed.")
    except Exception as e:
        print("Error closing connection:", e)

# ===================== Data Insertion =====================
def insert_sample_data(cur, conn):
    print("✓ Inserting data (if not present)...")
    
# ===================== Brands =====================
    brands = [
          ('BMW', 'Germany', 1916),
          ('Audi', 'Germany', 1909),
          ('Mercedes-Benz', 'Germany', 1926),
          ('Jaguar', 'United Kingdom', 1922),
          ('Volvo', 'Sweden', 1927)
    ]
    for b in brands:
        try:
            cur.execute("INSERT INTO brands (brand_name, country_of_origin, year_founded) VALUES (%s, %s, %s)", b)
        except Exception:
            pass
    conn.commit()
    print("✓ All Brands inserted successfully!")

# ===================== Models =====================
    models = [
            ('BMW', 'X1', 'SUV', 'Compact Luxury'),
            ('BMW', 'X3', 'SUV', 'Mid-size Luxury'),
            ('BMW', 'X5', 'SUV', 'Full-size Luxury'),
            ('BMW', 'X7', 'Luxury SUV', 'Full-size Luxury'),
            ('BMW', 'XM', 'SUV', 'Full-size Luxury'),
            ('BMW', 'iX1 LWB', 'SUV','Electric SUV'),
            ('BMW', 'iX', 'SUV', 'Electric SUV'),
            ('BMW', '2 Series','Gran coupé', 'Luxury'),
            ('BMW', '3 Series LWB','Sedan', 'Luxury'),
            ('BMW', '3 Series','Sedan', 'Performance'),
            ('BMW', '5 Series','Sedan', 'Luxury'),
            ('BMW', '7 Series', 'Sedan', 'Luxury'),
            ('BMW', 'i4', 'Gran Coupé', 'Electric Luxury'),
            ('BMW', 'i5', 'Gran Coupé', 'Electric Luxury'),
            ('BMW', 'i7', 'Sedan', 'Electric Luxury'),
            ('BMW', 'M2', 'Gran coupé', 'Performance'),
            ('BMW', 'M4', 'coupé', 'Performance'),
            ('BMW', 'M5', 'coupé', 'Performance'),
            ('BMW', 'M8', 'coupé', 'Performance'),
            ('BMW', 'Z4', 'Roadster', 'Performance'),
            ('Audi', 'A4', 'Sedan', 'Premium'),
            ('Audi', 'A6', 'Sedan', 'Luxury'),
            ('Audi', 'S5', 'SportBack', 'Performance'),
            ('Audi', 'Q3', 'SUV', 'Compact Luxury'),
            ('Audi', 'Q5', 'SUV', 'Mid-size Luxury'),
            ('Audi', 'Q7', 'SUV', 'Full-size Luxury'),
            ('Audi', 'Q8', 'SUV', 'Ultra-Luxury'),
            ('Audi', 'Q8 e-tron', 'SUV', 'Electric Luxury'),
            ('Audi', 'Q8 Sportback e-tron', 'SUV-coupé', 'Electric Luxury'),
            ('Audi', 'RS e-tron GT', 'Sedan', 'Electric Sports'),
            ('Mercedes-Benz', 'A Class', 'Sedan', 'Luxury'),
            ('Mercedes-Benz', 'C Class', 'Sedan', 'Luxury'),
            ('Mercedes-Benz', 'C Class AMG', 'Sedan', 'Performance'),
            ('Mercedes-Benz', 'E Class', 'Sedan', 'Luxury'),
            ('Mercedes-Benz', 'E Class', 'Sedan', 'Luxury'),
            ('Mercedes-Benz', 'S Class', 'Sedan', 'Luxury'),
            ('Mercedes-Benz', 'S Class AMG', 'Sedan', 'Performance'),
            ('Mercedes-Benz', 'EQA', 'Sedan', 'Electric Luxury'),
            ('Mercedes-Benz', 'EQB', 'Sedan', 'Electric Luxury'),
            ('Mercedes-Benz', 'EQE', 'Sedan', 'Electric Luxury'),
            ('Mercedes-Benz', 'EQS', 'Sedan', 'Electric Luxury'),
            ('Mercedes-Benz', 'GLA', 'SUV', 'Mid-size Luxury'),
            ('Mercedes-Benz', 'GLA AMG', 'SUV', 'Mid-size Luxury, Performance'),
            ('Mercedes-Benz', 'GLC', 'SUV', 'Mid-size Luxury'),
            ('Mercedes-Benz', 'GLE', 'SUV', 'Mid-size Luxury'),
            ('Mercedes-Benz', 'GLE AMG', 'SUV', 'Mid-size Luxury, Performance'),
            ('Mercedes-Benz', 'GLS', 'SUV', 'Full-size Luxury'),
            ('Mercedes-Benz', 'GLS AMG', 'SUV', 'Mid-size Luxury, Performance'),
            ('Mercedes-Benz', 'G Class', 'SUV', 'Luxury Off-road'),
            ('Mercedes-Benz', 'G Class AMG', 'SUV', 'Performance Off-road'),
            ('Mercedes-Benz', 'CLE Cabriolet AMG', 'Convertible', 'Grand Tourer'),
            ('Jaguar', 'F-Pace', 'SUV', 'Mid-size Luxury'),
            ('Volvo', 'EX30', 'SUV', 'Electric Compact'),
            ('Volvo', 'EX40', 'SUV', 'Electric Mid-size'),
            ('Volvo', 'EC40', 'coupé SUV', 'Electric Luxury'),
            ('Volvo', 'XC60', 'SUV', 'Mid-size Luxury'),
            ('Volvo', 'XC90', 'SUV', 'Full-size Luxury')
    ]
    # Insert Models
    for m in models:
        try:
            cur.execute("""
                INSERT INTO models (brand_id, model_name, body_type, category)
                VALUES ((SELECT brand_id FROM brands WHERE brand_name = %s LIMIT 1), %s, %s, %s)
            """, m)
        except Exception:
            pass
    conn.commit()
    print("✓ All Models inserted successfully!")
    
    # ===================== Variants =====================
    variants = [
        (('Mercedes-Benz', 'A Class'), 'A200','5362000', '1.3L Turbo Petrol', 163, 270, 230, 8.3, 'Automatic (DCT) - 7 Gears, Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '15 km/L', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'C Class'), 'C200','7009000', '1.5L Turbo Petrol Mild Hybrid', 201, 300, 246, 7.3, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'Rear Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '15 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'C Class'), 'C220d','7141000', '2.0L Turbo Diesel', 197, 440, 245, 7.3, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'Rear Wheel Drive', 'Mild Hybrid (Electric + Diesel)', '23 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'C Class'), 'C300','7841000', '2.0L Turbo Petrol Mild Hybrid', 255, 400, 250, 6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'Rear Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '22 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'C Class AMG'), 'C 43 4MATIC','11600000', '2.0 L Turbo-Petrol + 48V e-turbo', 402, 500, 250, 4.6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '12 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'C Class AMG'), 'C 63 SE Performance','20500000', '2.0 L Turbo + PHEV 4.84 kWh battery', 469, 545, 280, 3.4, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Hybrid (Electric + Petrol)', '14.5 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'E Class'), 'E200','9515000', '2.0L Inline-4 Turbo Petrol', 201, 320, 240, 7.5, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'Rear Wheel Drive', 'Petrol', '15km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'E Class'), 'E200d','9805000', '2.0L Inline-4 Turbo Diesel', 194, 440, 238, 7.6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'Rear Wheel Drive', 'Diesel', '15 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'E Class'), 'E450 4Matic','11000000', '3.0L Inline-6 Turbo Petrol', 375, 500, 250, 4.5, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '13 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'S Class'), 'S450 4Matic','23000000', '3.0L Turbocharged Inline-6 (M256) with EQ Boost', 375, 500, 250, 5, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '12km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'S Class AMG'), 'S 63 E PERFORMANCE', '34600000', '4.0 L Twin-Turbo V8 + 13.1 kWh battery', 794, 1430, 250, 5, 'Automatic (DCT) - 9 Gears, Manual Override & Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '9.5 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'EQA'), '250 Plus','7092000', '70.5 kWh Battery', 188, 385, 160, 8.6, 'Automatic - 1 Gears, Sport Mode', 'Front Wheel Drive', 'Electric', '560 km', 5, 'Not Tested'),
        (('Mercedes-Benz', 'EQB'), '250 Plus','7615000', '70.5 kWh Battery', 188, 385, 160, 8.9, 'Automatic - 1 Gears, Sport Mode', 'Front Wheel Drive', 'Electric', '464 km', 7, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'EQB'), '350 4Matic','8317000', '66.5 kWh Battery', 288, 520, 160, 6.2, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '423 km', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'EQE'), '500 4Matic','14900000', '90.56 kWh, Battery', 402, 858, 210, 4.9, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '550 km', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'EQS'), '450 5 Seater','13800000', '122 kWh Battery', 265, 800, 210, 6.1, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '650 km', 5, 'Not Tested'),
        (('Mercedes-Benz', 'EQS'), '580 4Matic','15300000', '122 kWh Battery', 536, 858, 210, 4.7, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '809 km', 7, 'Not Tested'),
        (('Mercedes-Benz', 'EQS'), '580 4Matic Celebration Edition','13700000', '107.8 kWh Battery', 536, 858, 210, 4.3, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '857 km', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLA'), 'GLA200','5920000', '1.3L Turbo Petrol', 161, 270, 210, 8.9, 'Automatic (DCT) - 7 Gears, Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '15 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'GLA'), '220d 4Matic','6365000', '2.0L Turbocharged Diesel', 188, 400, 219, 7.5, 'Automatic (DCT) - 8 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '14 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'GLA AMG'), '220d AMG Line 4Matic','6597000', '2.0L Turbocharged Diesel', 188, 400, 219, 7.5, 'Automatic (DCT) - 8 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '14 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'GLC'), '200d 4Matic','9120000', '2.0L Turbo Diesel', 194 ,440, 219, 8, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '14.7 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLC'), '300 4Matic','9120000', '2.0L Turbo Petrol', 255, 400, 240, 6.2, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '19.5 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLE'), '450 4MATIC', '13300000', '3.0L Inline-6 (M256) with EQ Boost (mild-hybrid)', 375, 500, 250, 5.6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '11 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLE'), '450d 4MATIC', '13900000', '3.0L OM656 Turbo I6 (diesel)', 362, 750, 250, 5.6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '11 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLE AMG'), '300d 4MATIC AMG Line', '11800000', '2.0L OM654 Turbo I4 (mild-hybrid)', 265, 550, 230, 6.9, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '12 km/l', 5, '5 Star (Euro NCAP)'),
        (('Mercedes-Benz', 'GLS'), '450 4MATIC', '15900000', '3.0L Inline-6 Turbo Petrol', 375, 500, 250, 6.1, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '10.5 km/l', 7, 'Not Tested'),
        (('Mercedes-Benz', 'GLS'), '450d 4MATIC', '16500000', '3.0L Inline-6 Turbo Diesel', 362, 750, 250, 6.1, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '10.5 km/l', 7, 'Not Tested'),
        (('Mercedes-Benz', 'GLS AMG'), '450 4MATIC AMG Line', '16300000', '3.0L Inline-6 Turbo Petrol', 375, 500, 250, 6.1, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '10.5 km/l', 7, 'Not Tested'),
        (('Mercedes-Benz', 'GLS AMG'), '450d 4MATIC AMG Line', '16600000', '3.0L Inline-6 Turbo Diesel', 362, 750, 250, 6.1, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Diesel', '10.5 km/l', 7, 'Not Tested'),
        (('Mercedes-Benz', 'G Class'), 'G 580 with EQ Technology', '31000000', '4 × electric motors (1 per wheel), 116 kWh battery', 587, 1164, 180, 4.7, 'Automatic (TC) - 9 Gears, Manual Override & Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Electric', '473 km', 5, 'Not Tested'),
        (('Mercedes-Benz', 'G Class AMG'), 'G 63', '43500000', '4.0 L Twin-Turbo V8 + 48V mild-hybrid', 577, 850, 220, 4.4, 'Automatic (DCT) - 9 Gears, Manual Override & Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '6 km/l', 5, 'Not Tested'),
        (('Mercedes-Benz', 'CLE Cabriolet AMG'), 'CLE 300 CABRIOLET 4MATIC', '11700000', '2.0L Inline-4 Turbo Petrol', 255, 400, 250, 6.6, 'Automatic (TC) - 9 Gears, Paddle Shift, Sport Mode', 'All-Wheel Drive', 'Petrol', '11 km/l', 4, 'Not Tested'),
        (('Jaguar', 'F-Pace'), 'S R-Dynamic 2.0 Petrol', '9237000', '2.0L Ingenium Turbocharged I4', 247, 365, 217, 7.3, 'Automatic (TC) - 8 Gears, Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '12.9 km/l', 5, '5 Star (Euro NCAP)'),
        (('Jaguar', 'F-Pace'), 'S R-Dynamic 2.0 Diesel', '9237000', '2.0L Ingenium Turbocharged I4', 201, 430, 210, 8, 'Automatic (TC) - 8 Gears, Paddle Shift, Sport Mode', 'All Wheel Drive', 'Diesel', '19.3 km/l', 5, '5 Star (Euro NCAP)'),
        (('Volvo', 'EX30'), 'RWD Ultra', '4100000', '69 kWh Battery', 272, 343, 180, 5.3, 'Automatic - 1 Gears', 'Rear Wheel Drive', 'Electric', '480', 5, '5 Star (Euro NCAP)'),
        (('Volvo', 'EX40'), 'Plus', '5301000', '69 kWh Battery', 238, 420, 180, 7.3, 'Automatic - 1 Gears', 'Rear Wheel Drive', 'Electric', '475', 5, '5 Star (Euro NCAP)',),
        (('Volvo', 'EC40'), 'Ultra', '6233000', '78 kWh Battery', 408, 660, 180, 4.7, 'Automatic - 1 Gears', 'All-Wheel Drive', 'Electric', '530', 5, '5 Star (Euro NCAP)'),
        (('Volvo', 'XC60'), 'B5 Ultra', '8379000', '2.0L Turbo Petrol', 250, 350, 180, 7.1, 'Automatic (TC) - 8 Gears, Manual Override, Sport Mode', 'All-Wheel Drive', 'Petrol', '12 km/l', 5, '5 Star (Euro NCAP)'),
        (('Volvo', 'XC90'), 'B5 Ultra', '12000000', '2.0L Turbo Petrol + Supercharger + 48V Mild Hybrid', 247, 360, 180, 7.7, 'Automatic (TC) - 8 Gears, Manual Override, Sport Mode', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '12.38 km/l', 7, '5 Star (Euro NCAP)'),
        (('BMW', 'X1'), 'sDrive18i M Sport', '5992000', '1.5L 3-cylinder BMW TwinPower Turbo', 134, 230, 210, 9.2, '7-Speed Automatic (DCT), with Manual Override & Paddle Shifters, Sport Mode', 'sDrive', 'Petrol', '16.35 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'X1'), 'sDrive18d M Sport', '6423000', '2.0L 4-cylinder BMW TwinPower Turbo', 148, 360, 210, 8.9, '7-Speed Automatic (DCT), with Manual Override & Paddle Shifters, Sport Mode', 'sDrive', 'Diesel', '20.37 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'X3'), 'xDrive20i M Sport', '7120000', '2.0L 4-cylinder BMW TwinPower Turbo', 188, 310, 215, 7.8, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '13.38 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'X3'), 'xDrive20d M Sport', '7310000', '2.0L 4-cylinder BMW TwinPower Turbo', 197, 197, 215, 7.7, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Diesel', '16.55 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'X5'), 'xDrive40i', '9780000', '3.0L Inline-6 Cylinder BMW TwinPower Turbo', 375, 520, 250, 5.4, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '12 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'X5'), 'xDrive30d', '9980000', '3.0L 6-cylinder BMW TwinPower Turbo', 282, 650, 233, 6.1, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Diesel', '12 km/l', 5, 'Not Tested'),
        (('BMW', 'X7'), 'xDrive40i M Sport', '15000000', '3.0L 6-cylinder BMW TwinPower Turbo', 375, 520, 250, 5.8, '8-Speed Steptronic Sport Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '11.29 km/l', 6, 'Not Tested'),
        (('BMW', 'X7'), 'xDrive40d M Sport', '15600000', '3.0L 6-cylinder BMW TwinPower Turbo', 335, 700, 250, 5.9, '8-Speed Steptronic Sport Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Mild Hybrid(Electric + Diesel)', '14.31 km/l', 6, 'Not Tested'),
        (('BMW', 'X7'), 'xDrive40i M Sport Signature Edition', '15200000', '3.0 L inline-6 turbo-petrol + 48V mild-hybrid', 375, 520, 250, 5.9, '8-Speed Steptronic Sport Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Mild Hybrid(Electric + Petrol)', '11.29 km/l', 7, 'Not Tested'),
        (('BMW', 'XM'), 'Plug-in Hybrid', '29800000', '4.4L V8 Twin-Turbo + Electric Motor (Plug-in Hybrid)', 644, 800, 250, 4.3, 'Automatic - 8 Gears, Sport Mode', 'All-Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '61.9 km/l', 5, 'Not Tested'),
        (('BMW', 'iX1 LWB'), 'eDrive20L M Sport', '5185000', '66.4 kWh Battery', 204, 250, 175, 8.6, 'Automatic - 1 Gears, Sport Mode', 'sDrive', 'Electric', '531 km', 5, 'Not Tested'),
        (('BMW', 'iX'), 'xDrive 50', '12800000', '76.6 kWh Battery', 516, 765, 200, 4.6, 'Automatic - 1 Gears', 'All-Wheel Drive', 'Electric', '635 km', 5, 'Not Tested'),
        (('BMW', '2 Series'), '218 M Sport', '5460000', '1.5L 3-Cylinder Turbo Petrol', 154, 230, 230, 8.6, '7-speed Steptronic Dual-Clutch Automatic', 'sDrive', 'Petrol', '16.35 km/l', 4, 'Not Tested'),
        (('BMW', '2 Series'), '218 M Sport Pro', '5460000', '1.5L 3-Cylinder Turbo Petrol', 154, 230, 230, 8.6, '7-speed Steptronic Dual-Clutch Automatic', 'sDrive', 'Petrol', '16.35 km/l', 4, 'Not Tested'),
        (('BMW', 'M2'), '3.0 Petrol', '12000000', '3.0L Twin Turbo Inline-6', 473, 600, 250, 4, '6-Speed Automatic, with Manual Override & Paddle Shifters, Sport Mode', 'sDrive', 'Petrol', '10 km/l', 4, 'Not Tested'),
        (('BMW', '3 Series LWB'), '330 Li M Sport', '7184000', '2.0 L Twin-Turbo Inline-4 Petrol', 255, 400, 250, 6.2, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Petrol', '15.4 km/l', 5, 'Not Tested'),
        (('BMW', '3 Series LWB'), '320 Ld M Sport', '7116000', '2.0 L Twin-Turbo Inline-4 Diesel', 188, 400, 250, 7.6, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Petrol', '19.6 km/l', 5, 'Not Tested'),
        (('BMW', '3 Series'), 'M340i', '8703000', '3.0 L inline-6 Twin-Turbo (B58) Petrol', 369, 500, 250, 4.4, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '13.02 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'M4'), 'Competition', '18100000', '3.0 L Twin-Turbo Inline-6 (S58)', 523, 650, 250, 3.5, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '10 km/l', 4, '5★ (Euro NCAP)'),
        (('BMW', 'M4'), 'CS', '22000000', '3.0 L Twin-Turbo Inline-6 (S58)', 543, 650, 250, 3.4, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '10.24 km/l', 4, '5★ (Euro NCAP)'),
        (('BMW', 'i4'), 'eDrive40 M Sport', '8455000', '70.2 kWh Battery', 282, 430, 250, 6, 'Automatic - 1 Gears, Sport Mode', 'sDrive', 'Electric', '483 km', 5, 'Not Tested'),
        (('BMW', '5 Series'), '530Li M Sport', '8842000', '2.0L 4-cylinder TwinPower Turbo Petrol', 255, 400, 250, 6.5, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Petrol', '15.7 km/l', 5, '5★ (Euro NCAP)'),
        (('BMW', 'M5'), 'Competition', '20900000', '4.4L M TwinPower Turbo V8', 717, 1000, 250, 3.3, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Plug-in Hybrid (Electric + Petrol)', '14 km/l', 5, 'Not Tested'),
        (('BMW', 'i5'), 'M60 xDrive', '13600000', '83.9 kWh Battery', 601, 795, 230, 3.8, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '516 km', 4, 'Not Tested'),
        (('BMW', '7 Series'), '740i M Sport', '21100000', '3.0L Twin Turbo Inline-6', 375, 520, 250, 5.4, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Petrol', '12.61 km/l', 5, 'Not Tested'),
        (('BMW', '7 Series'), '740d M Sport', '21600000', '3.0L Twin Turbo Inline-6', 282, 650, 250, 6, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Diesel', '16.55 km/l', 5, 'Not Tested'),
        (('BMW', 'i7'), 'eDrive50 M Sport', '21600000', '101.7 kWh Battery', 449, 650, 250, 5.5, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '603 km', 5, 'Not Tested'),
        (('BMW', 'i7'), 'M70 xDrive', '26300000', '101.7 kWh Battery', 650, 1015, 250, 3.7, 'Automatic - 1 Gears, Sport Mode', 'All-Wheel Drive', 'Electric', '560 km', 5, 'Not Tested'),
        (('BMW', 'M8'), 'Competition Coupé', '28300000', '4.4L TwinPower Turbo V8 Petrol', 617, 750, 250, 3.2, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'All-Wheel Drive', 'Petrol', '8.77 km/l', 4, 'Not Tested'),
        (('BMW', 'Z4'), 'M40i', '10800000', '3.0L 6-cylinder TwinPower Turbo Petrol', 335, 500, 250, 4.5, '8-Speed Steptronic Automatic (Torque Converter), with Paddle Shifters', 'sDrive', 'Petrol', '12.09 km/l', 2, '5★ (Euro NCAP)'),
        (('Audi', 'A4'), 'Premium 40 TFSI','4699000', '2.0L TFSI Petrol', 201, 320,241, 7.1, 'Automatic (DCT) - 7 Gears, Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '17.4 km/l', 5,'5-Star (Euro NCAP)'),
        (('Audi', 'A4'), 'Premium Plus 40 TFSI','5199000', '2.0L TFSI Petrol', 201, 320, 241, 7.1, 'Automatic (DCT) - 7 Gears, Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '17.4 km/l', 5,'5-Star (Euro NCAP)'),
        (('Audi', 'A4'), 'Technology 40 TFSI','5584000', '2.0L TFSI Petrol', 201, 320, 241, 7.1, 'Automatic (DCT) - 7 Gears, Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '17.4 km/l', 5,'5-Star (Euro NCAP)'),
        (('Audi', 'A6'), 'Premium Plus 45 TFSI','8382000', '2.0L 4-cylinder TFSI Petrol', 261, 370, 250, 6.7, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '15 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'A6'), 'Technology 45 TFSI (Without Matrix)','8198000', '2.0L TFSI Petrol', 261, 370, 250, 6.7, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '14 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'A6'), 'Technology 45 TFSI','9185000', '2.0L Turbocharged Inline-4 (TFSI)', 261, 370, 250, 6.7, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'Front Wheel Drive', 'Petrol', '14 km/l', 5, '5-star (Euro NCAP)'),
        (('Audi', 'Q3'), 'Premium Plus 40 TFSI quattro S tronic','6294000', '2.0 L 4-cylinder TFSI', 188, 320, 222, 7.3, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '14.93 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'Q3'), 'Technology 40 TFSI quattro S tronic','6987000', '2.0 L 4-cylinder TFSI', 188, 320, 222, 7.3, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '14.93 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'Q5'), 'Premium Plus 45 TFSI','8543000', '2.0L TFSI Turbocharged I4', 261, 370, 240, 6.1, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '13.4 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q5'), 'Technology 45 TFSI','9214000', '2.0L TFSI Turbocharged I4', 261, 370, 240, 6.1, 'Automatic (DCT) - 7 Gears, Manual Override & Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '13.4 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q7'), 'Premium Plus TFSI quattro tiptronic','11300000', '3.0 TFSI V6 + 48V Mild-Hybrid System', 335, 500, 250, 5.6, 'Automatic (TC) - 8 Gears, Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '11.2 km/l', 7, '5-Star (Euro NCAP)'),
        (('Audi', 'Q7'), 'Technology TFSI quattro tiptronic','12500000', '3.0 TFSI V6 + 48V Mild-Hybrid System', 335, 500, 250, 5.6, 'Automatic (TC) - 8 Gears, Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '11.2 km/l', 7, '5-Star (Euro NCAP)'),
        (('Audi', 'Q8'), 'TFSI quattro tiptronic','15000000', '3.0 L V6 TFSI (Turbocharged)', 335, 500, 250, 5.6, 'Automatic (TC) - 8 Gears, Paddle Shift', 'All Wheel Drive', 'Petrol', '8 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'Q8'), 'quattro tiptronic','31700000', '4.0 L V8 Twin-Turbo (TFSI)', 648, 850, 305, 3.6, 'Automatic (TC) - 8 Gears, Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '9 km/l', 5, '5-Star (Euro NCAP)'),
        (('Audi', 'S5'), 'SportBack 3.0 TFSI Quattro','9943000', '3.0L V6 TFSI Turbocharged', 349, 500, 250, 4.8, 'Automatic (TC) - 8 Gears, Manual Override & Paddle Shift, Sport Mode', 'All Wheel Drive', 'Petrol', '10.6 km/l', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q8 e-tron'), '50 e-tron quattro','13600000', 'Battery (95 kWh Battery, 114 Volt)', 335, 664, 200, 6, 'Automatic - 1 Gears', 'All Wheel Drive', 'Electric', 'Range (491 km)', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q8 e-tron'), '55 e-tron quattro','15100000', 'Battery (114 kWh Battery, 114 Volt)', 402, 664, 200, 5.6, 'Automatic - 1 Gears', 'All Wheel Drive', 'Electric', 'Range (582 km)', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q8 Sportback e-tron'), '50 e-tron quattro','14200000', 'Battery (95 kWh)', 335, 664, 200, 6, 'Automatic - 1 Gears', 'All Wheel Drive', 'Electric', 'Range (491 km)', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'Q8 Sportback e-tron'), '55 e-tron quattro','15600000', 'Battery (114 kWh)', 402, 664, 200, 5.6, 'Automatic - 1 Gears', 'All Wheel Drive', 'Electric', 'Range (582 km)', 5, '5 Star (Euro NCAP)'),
        (('Audi', 'RS e-tron GT'), 'e-tron quattro','23100000', 'Battery (93.4 kWh)', 637, 830, 250, 3.3, 'Automatic - 1 Gears', 'All Wheel Drive', 'Electric', 'Range (401 km)', 5, '5-Star (Euro NCAP)')
        ]
    for v in variants:
        try:
            brand_name, model_name = v[0]

            cur.execute("""
                SELECT m.model_id FROM models m
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE b.brand_name = %s AND m.model_name = %s LIMIT 1
            """, (brand_name, model_name))
            model_row = cur.fetchone()

            if not model_row:
                print(f"Skipping variant, model not found: {brand_name} {model_name}")
                continue

            model_id = model_row[0]

            cur.execute("""
                INSERT INTO variants (model_id, variant_name, price_inr, engine, power_bhp, torque_nm,
                                      top_speed_kmh, acceleration_0_100, transmission, drivetrain, fuel_type,
                                      mileage_range, seating_capacity, safety_rating)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                model_id, v[1], v[2], v[3], v[4], v[5], v[6], v[7],
                v[8], v[9], v[10], v[11], v[12], v[13]
            ))

        except Exception as e:
            print(f"•Failed to insert variant {v}: {e}")

    conn.commit()
    print("✓ All variants inserted successfully!")

# ===================== Features =====================
    car_features = [
        (('Mercedes-Benz','A Class', 'A200'),'Features','10.25" Digital Instrument Cluster, 10.25" MBUX Touchscreen Infotainment, Dual-zone Automatic Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED High-Performance Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System'),
        (('Mercedes-Benz','A Class', 'A200'),'Interior','Dual Tone (Black with Carbon Fibre Trim, Macchiato Beige / Black with Walnut Wood Trim)'),
        (('Mercedes-Benz','A Class', 'A200'),'Alloy_Wheels','17" Multi-Spoke Alloy Wheels'),
        (('Mercedes-Benz','C Class', 'C200'),'Features','12.3" Digital Instrument Cluster, 11.9" MBUX Touchscreen Infotainment,Dual-zone Automatic Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED High-Performance Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System'),
        (('Mercedes-Benz','C Class', 'C200'),'Interior','Dual Tone (Customisable)'),
        (('Mercedes-Benz','C Class', 'C200'),'Alloy_Wheels','18" Multi-Spoke Alloy Wheels'),
        (('Mercedes-Benz','C Class', 'C200d'),'Features','12.3" Digital Instrument Cluster, 11.9" MBUX Touchscreen Infotainment, Dual-zone Automatic Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED High-Performance Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System, Diesel Optimised Engine Tuning'),
        (('Mercedes-Benz','C Class', 'C200d'),'Interior','Dual Tone (Customisable)'),
        (('Mercedes-Benz','C Class', 'C200d'),'Alloy_Wheels','18" Multi-Spoke Alloy Wheels'),
        (('Mercedes-Benz','C Class', 'C300'),'Features','12.3" Digital Cluster, 11.9" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor, AMG Performance Seats, Adaptive Suspension, Quad Exhausts, AMG Night Package, Sport Steering, 15-speaker Burmester Audio'),
        (('Mercedes-Benz','C Class', 'C300'),'Interior','Dual Tone (Customisable)'),
        (('Mercedes-Benz','C Class', 'C300'),'Alloy_Wheels','18" Multi-Spoke Alloy Wheels'),
        (('Mercedes-Benz','C Class AMG', 'C 43 4MATIC'),'Features','AMG-specific grille, 11.9-inch MBUX screen, sport seats, Burmester® 3D audio, adaptive suspension, track telemetry, and advanced driver aids.'),
        (('Mercedes-Benz','C Class AMG', 'C 43 4MATIC'),'Interior','Single Tone (Black with Yellow Contrast and Aluminium Trim)'),
        (('Mercedes-Benz','C Class AMG', 'C 43 4MATIC'),'Alloy_Wheels','20" AMG Light Alloy Wheels 4 fold 5-Double Spoke'),
        (('Mercedes-Benz','C Class AMG', 'C 63 S E Performance'),'Features','AMG hybrid powertrain with F1-derived tech, performance steering, 11.9-inch MBUX, AMG Track Pace, premium Burmester® audio, adaptive suspension, and driver assist suite.'),
        (('Mercedes-Benz','C Class AMG', 'C 63 S E Performance'),'Interior','Single Tone (Black)'),
        (('Mercedes-Benz','C Class AMG', 'C 63 S E Performance'),'Alloy_Wheels','20" AMG Light Alloy Wheels 4 fold 5-Double Spoke'),
        (('Mercedes-Benz','E Class', 'E200'),'Features','12.3" Digital Cluster, 11.9" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor. Premium interiors with 15-speaker Burmester audio, powered memory seats, adaptive cruise, AMG-style accents.'),
        (('Mercedes-Benz','E Class', 'E200'),'Interior','Dual Tone (Cinnamon Brown / Black/Anthracite / Beige)'),
        (('Mercedes-Benz','E Class', 'E200'),'Alloy_Wheels','18" 5-Spoke Light Alloy Wheel in Black with High Sheen'),
        (('Mercedes-Benz','E Class', 'E200d'),'Features','12.3" Digital Cluster, 11.9" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor. Premium interiors with 16-speaker Burmester audio, powered memory seats, adaptive cruise, AMG-style accents,Diesel Optimised Engine Tuning'),
        (('Mercedes-Benz','E Class', 'E200d'),'Interior','Dual Tone (Cinnamon Brown / Black/Anthracite / Beige)'),
        (('Mercedes-Benz','E Class', 'E200d'),'Alloy_Wheels','18" 5-Spoke Light Alloy Wheel in Black with High Sheen'),
        (('Mercedes-Benz','E Class', 'E450 4Matic'),'Features','12.3" Digital Cluster, 11.9" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor, enhanced engine, ventilated/heated seats, AMG-style accents, upgraded suspension, Petrol Optimised Enhanced Engine Tuning'),
        (('Mercedes-Benz','E Class', 'E450 4Matic'),'Interior','Dual Tone (Cinnamon Brown / Black/Anthracite / Beige)'),
        (('Mercedes-Benz','E Class', 'E450 4Matic'),'Alloy_Wheels','18" 5-Spoke Light Alloy Wheel in Tantalite Grey'),
        (('Mercedes-Benz','S Class', 'S450 4Matic'),'Features','AMG Night Package, Exterior Chrome Accents, Wheel Options, Sport Styling Package, 12.3" Digital Cluster, 12.8" OLED MBUX Touchscreen, 4-zone Climate, Ambient Lighting with 64 Colours, Reverse Camera, Keyless Go, LED Headlamps, 9 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor, Premium Burmester 3D Audio, Ventilated & Heated Seats, AMG-style Accents, Panoramic Sunroof, Executive Rear Seat Package, MBUX AR Navigation.'),
        (('Mercedes-Benz','S Class', 'S450 4Matic'),'Interior','Dual Tone (Sienna Black / Black with High-gloss Black Poplar Wood Trim, Beige / Black with High-gloss Black Poplar Wood Trim)'),
        (('Mercedes-Benz','S Class', 'S450 4Matic'),'Alloy_Wheels','20" AMG multi-spoke alloys'),
        (('Mercedes-Benz','S Class AMG', 'S 63 E PERFORMANCE'),'Features','AMG V8 hybrid with E-Performance boost, Executive rear package, 12.8-inch OLED MBUX, Burmester® 4D surround, AMG ride control+, and comprehensive luxury driver aids.'),
        (('Mercedes-Benz','S Class AMG', 'S 63 E PERFORMANCE'),'Interior','Dual Tone, High-gloss Black Poplar Wood Trim, High-gloss Brown Burr Walnut Wood Trim, MANUFAKTUR Black Piano Lacquer with Flowing Lines, MANUFAKTUR Brown Open-Pore Walnut with Aluminium Lines, AMG Carbon-Fibre/Black Piano Lacquer Trim'),
        (('Mercedes-Benz','S Class AMG', 'S 63 E PERFORMANCE'),'Alloy_Wheels','20-inch AMG 10-spoke light-alloy wheels, 21-inch AMG multi-spoke forged wheels (Silver), 21-inch AMG multi-spoke forged wheels (Black), 21-inch AMG cross-spoke forged wheels'),
        (('Mercedes-Benz','EQA', '250 Plus'),'Features','12.3" Digital Cluster, 10.25" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor; Burmester 3D Audio, Ventilated & Heated Seats,  Adaptive Cruise, MBUX Navigation, Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQA', '250 Plus'),'Interior','Dual Tone (Rose gold titanium grey), Star Pattern Trim'),
        (('Mercedes-Benz','EQA', '250 Plus'),'Alloy_Wheels','19" AMG 10-Spoke light-alloy wheels'),
        (('Mercedes-Benz','EQB', '250 Plus'),'Features','12.3" Digital Cluster, 10.25" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor; Burmester 3D Audio, Ventilated & Heated Seats, Adaptive Cruise, MBUX Navigation, Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQB', '250 Plus'),'Interior','Dual Tone (Rose Gold/Titanium Grey Pearl), Star Pattern Trim'),
        (('Mercedes-Benz','EQB', '250 Plus'),'Alloy_Wheels','19" AMG 10-Spoke light-alloy wheels'),
        (('Mercedes-Benz','EQB', '350 4Matic'),'Features','12.3" Digital Cluster, 10.25" MBUX Touchscreen, Dual-zone Climate, Ambient Lighting, Reverse Camera, Keyless Go, LED Headlamps, 7 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitor; Burmester 3D Audio, Ventilated & Heated Seats, Adaptive Cruise, MBUX Navigation, Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQB', '350 4Matic'),'Interior','Dual Tone (Rose Gold/Titanium Grey Pearl), Star Pattern Trim'),
        (('Mercedes-Benz','EQB', '350 4Matic'),'Alloy_Wheels','19" AMG 10-Spoke light-alloy wheels'),
        (('Mercedes-Benz','EQE', '500 4Matic'),'Features','12.8" MBUX Hyperscreen, 12.3" Digital Cluster, 4-zone Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED Headlamps, 9 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System; Burmester 3D Audio, Ventilated & Heated Seats,Adaptive Cruise, MBUX Navigation,  Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQE', '500 4Matic'),'Interior','Dual Tone (Black / Balao Brown/Neva Gray / Balao Brown), Brown Open-Pore Magnolia Wood Trim Elements With Mercedes-Benz Pattern In Aluminium'),
        (('Mercedes-Benz','EQE', '500 4Matic'),'Alloy_Wheels','20" 5-Spoke Light Alloy Wheels'),
        (('Mercedes-Benz','EQS', '450 5 Seater'),'Features','12.8" MBUX Hyperscreen, 12.3" Digital Cluster, 4-zone Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED Headlamps, 9 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System; Burmester 3D Audio, Ventilated & Heated Seats, Adaptive Cruise, MBUX Navigation,  Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQS', '450 5 Seater'),'Interior','Dual Tone (Neva Gray/Balao Brown/Macchiato Beige / Space Gray), Trim Elements-Wood Fineline Anthracite'),
        (('Mercedes-Benz','EQS', '450 5 Seater'),'Alloy_Wheels','21" 5-Spoke Light Alloy AllRound'),
        (('Mercedes-Benz','EQS', '580 4Matic'),'Features','12.8" MBUX Hyperscreen, 12.3" Digital Cluster, 4-zone Climate Control, Ambient Lighting with 64 Colours, Reverse Parking Camera, Keyless Go, LED Headlamps, 9 Airbags, Active Brake Assist, ATTENTION ASSIST, Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System; Burmester 3D Audio, Ventilated & Heated Seats, Adaptive Cruise, MBUX Navigation,  Auto Park Assist, Level 2 Autonomous Driving Features'),
        (('Mercedes-Benz','EQS', '580 4Matic'),'Interior','Dual Tone (Neva Gray/Balao Brown/Macchiato Beige / Space Gray)'),
        (('Mercedes-Benz','EQS', '580 4Matic'),'Alloy_Wheels','Data Missing'),
        (('Mercedes-Benz','EQS', '580 4Matic Celebration Edition'),'Features','12.3" Driver Display, 17.7" OLED Infotainment, 12.3" Passenger Display, Rear 11.6" Displays, 7" Rear Tablet, MBUX AR Navigation, Rear Seat Comfort Package with 38° Recline & Massage, 4-Zone Climate, Wireless Phone Charging, Panoramic Sunroof, Ambient Lighting, Premium Burmester Audio.'),
        (('Mercedes-Benz','EQS', '580 4Matic Celebration Edition'),'Interior','Dual Tone (Neva Grey/ Balao Brown, Macchiato Beige / Space Grey), Trim Elements-Wood Vinterio Walnut'),
        (('Mercedes-Benz','EQS', '580 4Matic Celebration Edition'),'Alloy_Wheels','LM-Wheel 5-Spoke 20" All Round'),
        (('Mercedes-Benz','GLA', 'GLA200'),'Features','10.25" Digital Display, Wireless Apple CarPlay & Android Auto, Dual-zone Climate Control, LED Headlamps, 7 Airbags, Active Brake Assist ATTENTION ASSIST Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System, Burmester Audio System, Panoramic Sunroof'),
        (('Mercedes-Benz','GLA', 'GLA200'),'Interior','Dual Tone (Black, Macchiato Beige / Black with optional Walnut Brown Wood Trim),Progressive/exterior chrome accent pack'),
        (('Mercedes-Benz','GLA', 'GLA200'),'Alloy_Wheels','18" 5-Spoke Light Alloy Wheel'),
        (('Mercedes-Benz','GLA', '220d 4Matic'),'Features','10.25" Digital Display, Dual-zone Climate Control, LED Headlamps, 7 Airbags, Active Brake Assist ATTENTION ASSIST Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System, Burmester Audio System, AMG Styling Package, AMG Performance Steering Wheel, AMG Sports Pedals, AMG Floor Mats, AMG Night Package'),
        (('Mercedes-Benz','GLA', '220d 4Matic'),'Interior','Single Tone (Black with Contrast Red Stitching, optional Light Aluminium Trim), AMG Line exterior'),
        (('Mercedes-Benz','GLA', '220d 4Matic'),'Alloy_Wheels','19" 5-Spoke Light Alloy Wheel'),
        (('Mercedes-Benz','GLA', '220d AMG Line 4Matic'),'Features','10.25" Digital Display, Dual-zone Climate Control, LED Headlamps, 7 Airbags, Active Brake Assist ATTENTION ASSIST Rain-Sensing Wipers, Hill Start Assist, Tyre Pressure Monitoring System, Burmester Audio System, AMG Styling Package, AMG Performance Steering Wheel, AMG Sports Pedals, AMG Floor Mats, AMG Night Package, AMG Performance Exhaust System, AMG Illuminated Door Sills, AMG Sports Seats, AMG Sport Suspension'),
        (('Mercedes-Benz','GLA', '220d AMG Line 4Matic'),'Interior','Single Tone (Black with Contrast Red Stitching, optional Light Aluminium Trim), Full AMG body kit'),
        (('Mercedes-Benz','GLA', '220d AMG Line 4Matic'),'Alloy_Wheels','19" 5-Spoke Light Alloy Wheel'),
        (('Mercedes-Benz','GLC', '200d 4Matic'),'Features','12.3" Digital Cluster, 10.25" MBUX touchscreen, Dual-zone climate, Ambient lighting; Reverse camera, Keyless Go, LED headlamps, 7 airbags, Active Brake Assist, Hill Start Assist.'),
        (('Mercedes-Benz','GLC', '200d 4Matic'),'Interior','Dual Tone (Black/ Macchiato Beige and Sienna brown), AMG Line exterior, Night Package, chrome surround options.'),
        (('Mercedes-Benz','GLC', '200d 4Matic'),'Alloy_Wheels','19" 5-Double Spoke Alloy Wheel'),
        (('Mercedes-Benz','GLC', '300 4Matic'),'Features','12.3" Digital Cluster, 11.9"/10.25" MBUX display, Dual-zone climate, Ambient lighting, Reverse camera, Keyless Go, LED headlamps; 9 airbags, Active Brake Assist, ATTENTION ASSIST.'),
        (('Mercedes-Benz','GLC', '300 4Matic'),'Interior','Dual Tone (Black/ Macchiato Beige and Sienna brown), Chrome/Gloss exterior packs, roof-rail finish options, AMG Line/Night Pack'),
        (('Mercedes-Benz','GLC', '300 4Matic'),'Alloy_Wheels','19" 5-Double Spoke Alloy Wheel'),
        (('Mercedes-Benz','GLE', '450 4MATIC'),'Features','12.3" digital cluster, 11-12" MBUX touchscreen, Dual-zone/4-zone climate (LWB), Ambient lighting, 360° camera, Keyless Go, LED headlamps, 9 airbags, Active Brake Assist.\nAdaptive cruise, Park Assist, panoramic sunroof, Burmester audio (pack)'),
        (('Mercedes-Benz','GLE', '450 4MATIC'),'Interior','Dual Tone (Macchiato Beige / Black, Black), Anthracite Open-Pore Oak Wood Trim Elements, Trim Element- Wood Socket Wrench Bit Tree'),
        (('Mercedes-Benz','GLE', '450 4MATIC'),'Alloy_Wheels','20" AMG 5-Twin Spoke Light Alloy Wheels'),
        (('Mercedes-Benz','GLE', '450d 4MATIC'),'Features','12.3" digital cluster, 10.25-11.9" MBUX, Dual-zone climate, Ambient lighting, Reverse cam, Keyless Go, LED headlamps, 9 airbags, Active Brake Assist.\nHigh torque diesel performance, 360° camera, adaptive cruise, Park Assist; panoramic roof optional.'),
        (('Mercedes-Benz','GLE', '450d 4MATIC'),'Interior','Dual Tone (Macchiato Beige / Black, Black), Anthracite Open-Pore Oak Wood Trim Elements, Trim Element- Wood Socket Wrench Bit Tree'),
        (('Mercedes-Benz','GLE', '450d 4MATIC'),'Alloy_Wheels','20" AMG 5-Twin Spoke Light Alloy Wheels'),
        (('Mercedes-Benz','GLE AMG', '300d 4MATIC AMG Line'),'Features','12.3" digital cluster, 10.25/11.9" MBUX, Dual-zone climate, Ambient lighting, Reverse cam, Keyless Go, LED headlamps, 9 airbags, Active Brake Assist, ATTENTION ASSIST, Rain-sensing wipers, Hill Start Assist, TPM, Panoramic sunroof, 360° camera, adaptive cruise & ADAS suite; optional Burmester audio'),
        (('Mercedes-Benz','GLE AMG', '300d 4MATIC AMG Line'),'Interior','Dual Tone (Macchiato Beige / Black, Black), High-Gloss Brown Linestructure Lime Wood Trim'),
        (('Mercedes-Benz','GLE AMG', '300d 4MATIC AMG Line'),'Alloy_Wheels','20" AMG 5-Twin Spoke Light Alloy Wheels'),
        (('Mercedes-Benz','GLS', '450 4MATIC'),'Features','12.3" digital cluster, 11.9" MBUX touchscreen with navigation & AI voice, Adaptive Cruise with Active Distance Assist, Blind Spot Assist, ATTENTION ASSIST, 360° surround-view camera, dual-zone climate, panoramic sunroof, Burmester audio, hands-free tailgate, AMG brakes & adaptive suspension, LED High-Performance headlamps.'),
        (('Mercedes-Benz','GLS', '450 4MATIC'),'Interior','Dual Tone (Macchiato Beige / Black, Espresso Brown / Black, Anthracite / Black), Manufaktur Piano Black Lacquer Trim Elements'),
        (('Mercedes-Benz','GLS', '450 4MATIC'),'Alloy_Wheels','21" AMG Twin 5-Spoke (Standard); Optional 22"/23" AMG Wheels'),
        (('Mercedes-Benz','GLS', '450d 4MATIC'),'Features','12.3" digital cluster, 11.9" MBUX touchscreen with navigation & AI voice, Adaptive Cruise with Active Distance Assist, Blind Spot Assist, ATTENTION ASSIST, 360° surround-view camera, dual-zone climate, panoramic sunroof, Burmester audio, hands-free tailgate, AMG brakes & adaptive suspension, LED High-Performance headlamps.'),
        (('Mercedes-Benz','GLS', '450d 4MATIC'),'Interior','Dual Tone (Macchiato Beige / Black, Espresso Brown / Black, Anthracite / Black), Manufaktur Piano Black Lacquer Trim Elements'),
        (('Mercedes-Benz','GLS', '450d 4MATIC'),'Alloy_Wheels','21" AMG Twin 5-Spoke (Standard); Optional 22"/23" AMG Wheels'),
        (('Mercedes-Benz','GLS AMG', '450 4MATIC AMG Line'),'Features','12.3" digital cluster, 11.9" MBUX touchscreen with navigation & AI voice, Adaptive Cruise with Active Distance Assist, Blind Spot Assist, ATTENTION ASSIST, 360° surround-view camera, dual-zone climate, panoramic sunroof, Burmester audio, hands-free tailgate, AMG brakes & adaptive suspension, AMG body kit & LED High-Performance headlamps.'),
        (('Mercedes-Benz','GLS AMG', '450 4MATIC AMG Line'),'Interior','Dual Tone (Macchiato Beige / Black, Espresso Brown / Black, Anthracite / Black), Manufaktur Piano Black Lacquer Trim Elements'),
        (('Mercedes-Benz','GLS AMG', '450 4MATIC AMG Line'),'Alloy_Wheels','21" AMG Twin 5-Spoke (Standard); Optional 22"/23" AMG Wheels'),
        (('Mercedes-Benz','GLS AMG', '450d 4MATIC AMG Line'),'Features','12.3" digital cluster, 11.9" MBUX touchscreen with navigation & AI voice, Adaptive Cruise with Active Distance Assist, Blind Spot Assist, ATTENTION ASSIST, 360° surround-view camera, dual-zone climate, panoramic sunroof, Burmester audio, hands-free tailgate, AMG brakes & adaptive suspension, AMG body kit & LED High-Performance headlamps.'),
        (('Mercedes-Benz','GLS AMG', '450d 4MATIC AMG Line'),'Interior','Dual Tone (Macchiato Beige / Black, Espresso Brown / Black, Anthracite / Black), Manufaktur Piano Black Lacquer Trim Elements'),
        (('Mercedes-Benz','GLS AMG', '450d 4MATIC AMG Line'),'Alloy_Wheels','21" AMG Twin 5-Spoke (Standard); Optional 22"/23" AMG Wheels'),
        (('Mercedes-Benz','G Class', 'G 580 with EQ Technology'),'Features','Dual 12.3" displays (instrument & MBUX), 360° camera, BURMESTER 18-speaker Dolbly Atmos sound; G-Turn (rotate on spot), G-Steering, G-Crawl, adaptive off-road modes, water-wading 850 mm'),
        (('Mercedes-Benz','G Class', 'G 580 with EQ Technology'),'Interior','Dual Tone (Nappa leather silver pearl/black), AMG carbon-fibre trim elements, MANUFAKTUR trim in black flamed open-pore ash wood, Metal structure trim element, MANUFAKTUR open-pore grey oak wood trim element, Black piano lacquer trim element, Open-pore natural walnut wood trim element, High-gloss light brown sen wood trim element'),
        (('Mercedes-Benz','G Class', 'G 580 with EQ Technology'),'Alloy_Wheels','20" AMG Silver/Black 10-Spoke Light Alloy Wheels'),
        (('Mercedes-Benz','G Class AMG', 'G63'),'Features','Off-road modes, G-turn, 360° cam, massaging seats, adaptive anti-roll suspension, dual displays, ADAS'),
        (('Mercedes-Benz','G Class AMG', 'G63'),'Interior','Dual Tone (Macchiato beige/black/Truffle brown/black), Boxy body, ladder frame, optional Collector\'s Edition, Night pack'),
        (('Mercedes-Benz','G Class AMG', 'G63'),'Alloy_Wheels','20" std, optional 21"/22" AMG'),
        (('Mercedes-Benz','CLE Cabriolet AMG', 'CLE 300 CABRIOLET 4MATIC'),'Features','Widescreen MBUX cockpit, double rear airbags, AIRCAP, AIRSCARF, 360° parking assist, ambient lighting, Burmester 3D audio, elegant open-air luxury'),
        (('Mercedes-Benz','CLE Cabriolet AMG', 'CLE 300 CABRIOLET 4MATIC'),'Interior','Dual Tone (Tonka brown / black/Power red / black), Metal Structure Trim Element'),
        (('Mercedes-Benz','CLE Cabriolet AMG', 'CLE 300 CABRIOLET 4MATIC'),'Alloy_Wheels','19" AMG Multi-Spoke Alloys'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Petrol'), 'Features', 'Gloss Black R-Dynamic exterior styling pack, Matrix LED headlights w/ DRL, 11.4-inch Pivi Pro infotainment, Meridian Sound System, powered tailgate, 12-way electric front seats w/ heating, adaptive cruise control, 3D surround camera, lane keep assist, dual-zone climate control, keyless entry, ambient lighting'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Petrol'), 'Interior', 'Single Tone (Black)'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Petrol'), 'Alloy_Wheels', '19-inch Diamond Turned Finish'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Diesel'), 'Features', 'Gloss Black R-Dynamic exterior styling pack, Matrix LED headlights w/ DRL, 11.4-inch Pivi Pro infotainment, Meridian Sound System, powered tailgate, 12-way electric front seats w/ heating, adaptive cruise control, 3D surround camera, lane keep assist, dual-zone climate control, keyless entry, ambient lighting'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Diesel'), 'Interior', 'Single Tone (Black)'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Diesel'), 'Alloy_Wheels', '19-inch Diamond Turned Finish'),
        (('Volvo', 'EX30', 'RWD Ultra'), 'Features', '12.3″ Touchscreen w/ Google Built-in, Wireless CarPlay, Harman Kardon Soundbar, 360° Camera, Pilot Assist ADAS, Adaptive Cruise, Panoramic Roof, OTA Updates, One-Pedal Drive'),
        (('Volvo', 'EX30', 'RWD Ultra'), 'Interior', 'Breeze interior,Pine interior,Mist interior'),
        (('Volvo', 'EX30', 'RWD Ultra'), 'Alloy_Wheels', '19″ 5-spoke glossy black diamond cut'),
        (('Volvo', 'EX40', 'Plus'), 'Features', '12.3" Touchscreen w/ Google Built-in, Harman Kardon Sound, 360° Camera, Pilot Assist ADAS, Adaptive Cruise, Panoramic Roof, OTA Updates, Wireless CarPlay'),
        (('Volvo', 'EX40', 'Plus'), 'Interior', 'Single Tone (Charcoal)'),
        (('Volvo', 'EX40', 'Plus'), 'Alloy_Wheels', '19"/20" Aero & Diamond Cut'), 
        (('Volvo', 'EC40', 'Ultra'), 'Features', 'Google Built-in 12.3" Display, Harman Kardon Audio, 360° Camera, Pilot Assist ADAS, Panoramic Roof, Ambient Lighting, Wireless CarPlay, OTA updates'),
        (('Volvo', 'EC40', 'Ultra'), 'Interior', 'Dual Tone (Charcoal Insert/Sky Blue Insert)'),
        (('Volvo', 'EC40', 'Ultra'), 'Alloy_Wheels', '19"/20" Aero & Diamond Cut'),
        (('Volvo', 'XC60', 'B5 Ultra'), 'Features', 'Google Built-in 9" Touchscreen, 15-speaker Bowers & Wilkins Audio, Panoramic Roof, Pilot Assist ADAS, 360° Camera, Adaptive Cruise, Wireless CarPlay, Ambient Lighting, 4-zone Climate'),
        (('Volvo', 'XC60', 'B5 Ultra'), 'Interior', 'Dual Tone (Amber / Charcoal, Maroon Brown / Charcoal)'),
        (('Volvo', 'XC60', 'B5 Ultra'), 'Alloy_Wheels', '19" Diamond Cut, optional 20"'),
        (('Volvo', 'XC90', 'B5 Ultra'), 'Features', '12.3" Digital Cockpit, 19-speaker Bowers & Wilkins Audio, Panoramic Roof, Pilot Assist ADAS, 360° Camera, Adaptive Cruise, Wireless CarPlay, Four-zone Climate, Soft-close Doors, Hands-free Tailgate'),
        (('Volvo', 'XC90', 'B5 Ultra'), 'Interior', 'Dual Tone (Grey Ash / Brown Ash/ Charcoal)'),
        (('Volvo', 'XC90', 'B5 Ultra'), 'Alloy_Wheels', '20" Diamond Cut, optional 21"'),
        (('BMW', 'X1', 'sDrive18i M Sport'),'Features', 'LED headlights w/ DRLs, Curved Display (10.25" + 10.7"), Wireless CarPlay & Android Auto, Wireless Charging, iDrive Controller w/ Voice Command, Navigation w/ Rear View Camera, Park Distance Control, 6 Airbags, Dynamic Stability Control, Crash Sensor, Dual-zone climate.'),
        (('BMW', 'X1', 'sDrive18i M Sport'), 'Interior', "Veganza Perforated Mocha/Veganza Perforated Oyster, Interior trim finishers Aluminium ‘Mesheffect’ with highlight trim finisher in Pearl Chrome"),
        (('BMW', 'X1', 'sDrive18i M Sport'), 'Alloy_Wheels', '18" M light alloy wheels Double-spoke style 838 M Bicolour'),
        (('BMW', 'X1', 'sDrive18d M Sport'),'Features', 'LED headlights w/ DRLs, Curved Display (10.25" + 10.7"), Wireless CarPlay & Android Auto, Wireless Charging, iDrive Controller w/ Voice Command, Navigation w/ Rear View Camera, Park Distance Control, 6 Airbags, Dynamic Stability Control, Crash Sensor, Dual-zone climate.'),
        (('BMW', 'X1', 'sDrive18d M Sport'), 'Interior', "Veganza Perforated Mocha/Veganza Perforated Oyster, Interior trim finishers Aluminium ‘Mesheffect’ with highlight trim finisher in Pearl Chrome"),
        (('BMW', 'X1', 'sDrive18d M Sport'), 'Alloy_Wheels', '18" M light alloy wheels Double-spoke style 838 M Bicolour'),
        (('BMW', 'X3', 'xDrive20i M Sport'),'Features', 'Parking Assistant, Reversing Assistant, 360° Camera, Wireless Apple CarPlay & Android Auto, Harman Kardon Surround Sound System, BMW Curved Display (12.3" Instrument + 14.9" Control Display), Panoramic Glass Sunroof, 6 Airbags, Tyre Pressure Indicator, Driving Assistant, Cruise Control with Braking Function'),
        (('BMW', 'X3', 'xDrive20i M Sport'), 'Interior', "Veganza Perforated Espresso Brown, Veganza Perforated Calm Beige, Interior trim finishers Aluminium ‘Rhombicle’ with highlight trim finisher in Pearl Chrome"),
        (('BMW', 'X3', 'xDrive20i M Sport'), 'Alloy_Wheels', '19" M Light Alloy Wheels Y-Spoke Bicolour'),
        (('BMW', 'X3', 'xDrive20d M Sport'),'Features', 'Parking Assistant, Reversing Assistant, 360° Camera, Wireless Apple CarPlay & Android Auto, Harman Kardon Surround Sound System, BMW Curved Display (12.3" Instrument + 14.9" Control Display), Panoramic Glass Sunroof, 6 Airbags, Tyre Pressure Indicator, Driving Assistant, Cruise Control with Braking Function'),
        (('BMW', 'X3', 'xDrive20d M Sport'), 'Interior', "Veganza Perforated Espresso Brown, Veganza Perforated Calm Beige, Interior trim finishers Aluminium ‘Rhombicle’ with highlight trim finisher in Pearl Chrome"),
        (('BMW', 'X3', 'xDrive20d M Sport'), 'Alloy_Wheels', '19" M Light Alloy Wheels Y-Spoke Bicolour'),
        (('BMW', 'X5', 'xDrive40i'),'Features', '360° Camera w/ Parking & Reversing Assist, Curved Display (12.3" + 14.9"), Wireless CarPlay & Android Auto, Harman Kardon Sound, Panoramic Sunroof, 6 Airbags, Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Adaptive Air Suspension, Gesture Control, BMW Laserlight, 4-Zone Climate, Electric Seats w/ Memory, Comfort Access, Welcome Light.'),
        (('BMW', 'X5', 'xDrive40i'), 'Interior', "Sensafin Decor Stitching / Cognac, Fine-Wood Trim 'Fineline Stripe' Brown High-Gloss"),
        (('BMW', 'X5', 'xDrive40i'), 'Alloy_Wheels', '21" Light Alloy Wheels Y-Spoke Style 744 Bicolour'),
        (('BMW', 'X5', 'xDrive30d'),'Features', '360° Camera w/ Parking & Reversing Assist, Curved Display (12.3" + 14.9"), Wireless CarPlay & Android Auto, Harman Kardon Sound, Panoramic Sunroof, 6 Airbags, Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Adaptive Air Suspension, Gesture Control, BMW Laserlight, 4-Zone Climate, Electric Seats w/ Memory, Comfort Access, Welcome Light.'),
        (('BMW', 'X5', 'xDrive30d'), 'Interior', "Sensafin Decor Stitching / Cognac, Fine-Wood Trim 'Fineline Stripe' Brown High-Gloss"),
        (('BMW', 'X5', 'xDrive30d'), 'Alloy_Wheels', '21" Light Alloy Wheels Y-Spoke Style 744 Bicolour'),
        (('BMW', 'X7', 'xDrive40i M Sport'),'Features', '360° Camera, Curved Display (12.3" + 14.9"), Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Air Suspension, Gesture Control, Laserlight, Comfort Seats w/ Memory, Welcome Light, Comfort Access, Rear Seat Entertainment, 5-Zone Climate, Soft-Close Doors, Sky Lounge Glass Roof, Heated & Ventilated Seats, Rear Comfort Package, Remote Functions via My BMW App.'),
        (('BMW', 'X7', 'xDrive40i M Sport'), 'Interior', "Individual Extended Leather Trim Merino | Tartufo, Fine-Wood Trim 'Fineline' Black With Metal Effect High-Gloss"),
        (('BMW', 'X7', 'xDrive40i M Sport'), 'Alloy_Wheels', '21" Inches M Light Alloy Wheels Double-Spoke Style 754 M Bicolour Orbit Grey, Gloss-Lathed'),
        (('BMW', 'X7', 'xDrive40d M Sport'),'Features', '360° Camera, Curved Display (12.3" + 14.9"), Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Air Suspension, Gesture Control, Laserlight, Comfort Seats w/ Memory, Welcome Light, Comfort Access, Rear Seat Entertainment, 5-Zone Climate, Soft-Close Doors, Sky Lounge Glass Roof, Heated & Ventilated Seats, Rear Comfort Package, Remote Functions via My BMW App.'),
        (('BMW', 'X7', 'xDrive40d M Sport'), 'Interior', "Individual Extended Leather Trim Merino | Tartufo, Fine-Wood Trim 'Fineline' Black With Metal Effect High-Gloss"),
        (('BMW', 'X7', 'xDrive40d M Sport'), 'Alloy_Wheels', '21" Inches M Light Alloy Wheels Double-Spoke Style 754 M Bicolour Orbit Grey, Gloss-Lathed'),
        (('BMW', 'X7', 'xDrive40i M Sport Signature Edition'),'Features', 'Crystal LED headlights, Curved Display (12.3" + 14.9"), Sky Lounge Panoramic Roof, Ambient Air Package, Rear Alcantara Cushions, Rear Captain Seats, Harman Kardon 16-Speaker Sound, Heads-Up Display, Ambient Light Bar, Comfort Access, Remote via My BMW App.'),
        (('BMW', 'X7', 'xDrive40i M Sport Signature Edition'), 'Interior', "BMW Individual Extended Leather Trim Merino | Tartufo', Fine-wood trim 'Fineline Stripe' brown high gloss"),
        (('BMW', 'X7', 'xDrive40i M Sport Signature Edition'), 'Alloy_Wheels', '53.4 cm (21") DPE light alloy wheels Y-spoke style 753 bicolour (9.5J x 21 with 285/45 R21 tyres)'),
        (('BMW', 'XM', 'Plug-in Hybrid'),'Features', '360° Camera, BMW Curved Display (12.3" + 14.9"), Bowers & Wilkins Diamond Surround Sound, Adaptive Cruise Control, M Adaptive Suspension, BMW Laserlight, Electric Comfort Seats w/ Massage & Memory, M Lounge Rear Seats, 4-Zone Climate Control, Soft-Close Doors, Heated & Ventilated Seats, Gesture Control, Ambient Lighting, Remote Functions via My BMW App'),
        (('BMW', 'XM', 'Plug-in Hybrid'), 'Interior', 'Dual Tone (Deep Lagoon / Walknappa Vintage Coffee , Silverstone / Walknappa Vintage Coffee, Sakhir Orange / Walknappa Vintage Coffee , Black / Walknappa Vintage Coffee), M-specific trims'),
        (('BMW', 'XM', 'Plug-in Hybrid'), 'Alloy_Wheels', '21" / 22" / 23" M Light-Alloy (optional)'),
        (('BMW', 'iX1 LWB', 'eDrive20L M Sport'),'Features', '360° Camera, BMW Curved Display (10.25" + 10.7"), Harman Kardon Sound, Driving Assistant Plus (Lane Keep, Blind Spot, Cross Traffic Alert), Adaptive Cruise Control, Electric Seats w/ Memory, 6 Airbags, Tyre Pressure Monitor, Ambient Lighting, Dual-Zone Climate, Comfort Access, Remote Functions via My BMW App.'),
        (('BMW', 'iX1 LWB', 'eDrive20L M Sport'), 'Interior', 'Veganza Perforated Mocha, Interior trim finishers Aluminium Hexacube'),
        (('BMW', 'iX1 LWB', 'eDrive20L M Sport'), 'Alloy_Wheels', 'M Sport 18-inch alloy wheels'),
        (('BMW', 'iX', 'xDrive 50'),'Features', 'Adaptive air suspension with Dynamic Handling, premium Harman Kardon surround sound, BMW Intelligent Personal Assistant, gesture control, optional 5G connectivity, extended ambient lighting with customizable themes'),
        (('BMW', 'iX', 'xDrive 50'), 'Interior', 'Dual Tone (Interior design Suite Leather Castanea), M-specific trims'),
        (('BMW', 'iX', 'xDrive 50'), 'Alloy_Wheels', '21" or 22" multi-spoke alloy wheels'),
        (('BMW', '2 Series', '218 M Sport'),'Features', '360° Camera with Parking & Reversing Assist, Curved Display (12.3" + 14.9"), Harman Kardon Sound, 6 Airbags, Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Adaptive Air Suspension, Gesture Control, BMW Laserlight, 4-Zone Climate Control, Electric Seats with Memory, Comfort Access, Welcome Light'),
        (('BMW', '2 Series', '218 M Sport'), 'Interior', 'Veganza Perforated Mocha, Veganza Perforated Oyster, Interior Decors Illuminated Aluminium Graphite'),
        (('BMW', '2 Series', '218 M Sport'), 'Alloy_Wheels', '18" M Law Y-Spoke 975M Bicolour'),
        (('BMW', '2 Series', '218 M Sport Pro'),'Features', '360° Camera with Parking & Reversing Assist, Curved Display (12.3" + 14.9"), Harman Kardon Sound, 6 Airbags, Tyre Pressure Monitor, Driving Assistant, Adaptive Cruise, Adaptive Air Suspension, Gesture Control, BMW Laserlight, 4-Zone Climate Control, Electric Seats with Memory, Comfort Access, Welcome Light'),
        (('BMW', '2 Series', '218 M Sport Pro'), 'Interior', 'Veganza Perforated Mocha, Veganza Perforated Oyster, M Illuminated Decor Hexacube Matte'),
        (('BMW', '2 Series', '218 M Sport Pro'), 'Alloy_Wheels', '18" M Law Y-Spoke 975M Bicolour'),
        (('BMW', 'M2', '3.0 Petrol'),'Features', 'BMW Curved Display (12.3-inch instrument cluster + 14.9-inch control display), iDrive 8.5, Harman Kardon Surround Sound System, M Sport Seats, Adaptive M Suspension, M Traction Control, Gear Shift Assistant, Matrix LED Headlights, 3-Zone Climate Control, Ambient Lighting, Lane Departure Warning, Blind Spot Monitoring, Rear Cross Traffic Alert, Parking Assistant, M Drift Analyzer'),
        (('BMW', 'M2', '3.0 Petrol'), 'Interior', "Leather 'Vernasca' Black/Exclusive Highlight, Leather 'Vernasca' Black/Contrast Stitching, Lthr Vernasca Black/Accent Red, Interior Trim Finishers 'Aluminum Rhombicle’, Interior Trim Finishers 'Carbon Fibre'"),
        (('BMW', 'M2', '3.0 Petrol'), 'Alloy_Wheels', '19"/ 20" M Light Alloy Wheels Double-Spoke Style 930 M Jet Black With Mixed Tyres, 19"/ 20" M Light Alloy Wheels Double-Spoke Style 930 M Bicolour With Mixed Tyres, 19"/20" M Law Do.Sp. 930M Silver'),
        (('BMW', '3 Series LWB', '330 Li M Sport'),'Features', 'Curved Display (14.9" + 12.3"), Panoramic Sunroof, 3-Zone Climate Control, Ambient Lighting, Driving Assistant (ADAS), Park Assistant Plus w/ Surround View, Comfort Access, Remote 3D View via My BMW App'),
        (('BMW', '3 Series LWB', '330 Li M Sport'), 'Interior', 'Leather Vernasca Cognac Decor Stitching, M Aerodynamics Package with satin aluminium accents, Pearl Chrome grille slats'),
        (('BMW', '3 Series LWB', '330 Li M Sport'), 'Alloy_Wheels', '18" Light Alloy Wheels 848 M Double Spoke'),
        (('BMW', '3 Series LWB', '320 Ld M Sport'),'Features', 'Curved Display (14.9" + 12.3"), Panoramic Sunroof, 3-Zone Climate Control, Ambient Lighting, Driving Assistant (ADAS), Park Assistant Plus w/ Surround View, Comfort Access, Remote 3D View via My BMW App'),
        (('BMW', '3 Series LWB', '320 Ld M Sport'), 'Interior', 'Leather Vernasca Cognac Decor Stitching, M Aerodynamics Package with satin aluminium accents, Pearl Chrome grille slats'),
        (('BMW', '3 Series LWB', '320 Ld M Sport'), 'Alloy_Wheels', '18" Light Alloy Wheels 848 M Double Spoke'),
        (('BMW', '3 Series', 'M340i'),'Features', 'BMW Curved Display (12.3" + 14.9"), M Sport Package, Adaptive LED Headlights with inverted L-DRL, BMW Digital Key Plus, Heads-Up Display, Driving Assistant, Adaptive Cruise Control, Park Assist Plus with 360° Camera, Harman Kardon Surround Sound, Ambient Lighting, 3-zone Climate Control, Sport Seats with Memory, M Sport Brakes & Exhaust, ConnectedDrive with Remote Functions via My BMW App.'),
        (('BMW', '3 Series', 'M340i'), 'Interior', 'Leather Vernasca Black/Contrast Stitching In Blue, Interior Trim Finishers Carbon Fibre'),
        (('BMW', '3 Series', 'M340i'), 'Alloy_Wheels', '19" M Do. Sp. 995M Jetblack Mt Rft'),
        (('BMW', 'M4', 'Competition'),'Features', 'M Drift Analyzer, M Laptimer, M Setup Menu (engine, steering, suspension, xDrive), 10-Stage M Traction Control, M Sport Differential, Carbon Roof & Carbon Interior Package, Optional Carbon Bucket Seats, M Compound Brakes w/ Carbon Ceramic option, M Exhaust w/ Flap Control, Launch Control'),
        (('BMW', 'M4', 'Competition'), 'Interior', "Bmw Individual Extended/Full Leather Trim 'Merino' | Fiona Red/Black, Bmw Individual Extended/Full Leather Trim 'Merino' | Tartufo, Bmw Individual Extended/Full Leather Trim 'Merino' | Fjord Blue/Black, Bmw Individual Extended/Full Leather Trim 'Merino' | Ivory White, Interior trim finishers 'Carbon Fibre'"),
        (('BMW', 'M4', 'Competition'), 'Alloy_Wheels', '19"/20" M forged wheels Double-spoke style 826 M Bicolour Black with mixed tyres, 19"/20" M forged wheels Double spoke 825 M Silver with mixed tyres, 19"/20" M forged wheels Double-spoke style 826 M Black with mixed tyres, 19"/20" M forged wheels Double-spoke style 825 M Bicolour Black with mixed tyres'),
        (('BMW', 'M4', 'CS'),'Features', 'Carbon fibre roof & bonnet, M Carbon bucket seats, Adaptive M suspension, M Carbon ceramic brakes (optional), M-specific Head-Up Display, Exclusive CS sound tuning, BMW Curved Display w/ M OS 8.5, Harman Kardon Surround, Track drive modes, Launch Control, M Drift Analyzer.'),
        (('BMW', 'M4', 'CS'), 'Interior', 'M Alcantara/Leather Combination Black w/ Red Contrast Stitching, M Carbon Bucket Seats (standard), Interior Trim Finishers ‘Carbon Fibre Matt’'),
        (('BMW', 'M4', 'CS'), 'Alloy_Wheels', '19"/20" M Forged Wheels V-Spoke Style 825M (Matte Gold Bronze or Black), Track-optimized mixed tyres'),
        (('BMW', 'i4', 'eDrive40 M Sport'),'Features', 'BMW Curved Display (12.3" + 14.9"), Harman Kardon Surround, Parking Assistant Plus w/ 360° Camera, Driving Assistant, Adaptive Cruise Control, Gesture Control, 3-Zone Climate Control, Heated & Powered Seats w/ Memory, Ambient Lighting, Comfort Access, My BMW App.'),
        (('BMW', 'i4', 'eDrive40 M Sport'), 'Interior', 'Sensatec Perforated Canberra Beige, Fi.Wood Trim Oak Grain Open-Pored'),
        (('BMW', 'i4', 'eDrive40 M Sport'), 'Alloy_Wheels', '18" M aerodynamic wheels 858 M Bicolour with mixed tyres'),
        (('BMW', '5 Series', '530Li M Sport'),'Features', 'Parking Assistant Plus, 360° Camera, BMW Curved Display (12.3" + 14.9"), Harman Kardon Surround Sound, 4-Zone Climate Control, Adaptive LED Headlamps, Gesture Control, Ambient Lighting, Electric Seats w/ Memory, Comfort Access, Reversing Assistant, Drive Recorder, Tyre Pressure Monitor,Adaptive Cruise Control.'),
        (('BMW', '5 Series', '530Li M Sport'), 'Interior', 'Perforated Sensatec | Cognac, Black, Dark Silver Accent Combined With Fine-Wood Trim Grey Blue Ash, Open-Pored'),
        (('BMW', '5 Series', '530Li M Sport'), 'Alloy_Wheels', '19" M Alloy Wheels 935 W/Dual-Spoke Bi-Colour Black Grey'),
        (('BMW', 'M5', 'Competition'),'Features', 'Adaptive LED/Laserlight, M Sport Exhaust, M Multifunction Seats, M Head-Up Display, 12.3" BMW Live Cockpit, Harman Kardon Audio (Bowers & Wilkins optional), M Setup w/ M1 & M2 modes, Parking Assistant Plus (360°), Driving Assistant, Soft-Close Doors, Ambient Lighting, 4-Zone Climate, Remote Functions via My BMW App.'),
        (('BMW', 'M5', 'Competition'), 'Interior', "Leather 'Merino' With Extended Contents Silverstone | Black, Leather ‘Merino’ With Extended Contents Black | Black, Leather 'Merino' With Extended Contents Kyalami Orange | Black, Leather Merino Red/Black, Acc. D. Silver/Fw Oak Dark Hi. Gl.,M Acc. D. Sil./Carb. F./Silv.Th. Hg, M Acc. D. Silver/Alu. Rhombicle Ds"),
        (('BMW', 'M5', 'Competition'), 'Alloy_Wheels', '20"/21" M Law D.Sp. 951M Bic Mg Mt, 20"/21" M Law D.Sp. 951M Black Mt, 20"/21" M Law D.Sp. 952M Bic Blk Mt'),
        (('BMW', 'i5', 'M60 xDrive'),'Features', 'BMW Curved Display (12.3" + 14.9"), M Head-Up Display, Bowers & Wilkins Audio, Parking Assistant Plus w/ 360° cam, Driving Assistant Pro, Adaptive Cruise, M Adaptive Air Suspension, Integral Active Steering, Heated & Ventilated Massage Seats, Ambient Lighting, Comfort Access, Remote Functions.'),
        (('BMW', 'i5', 'M60 xDrive'), 'Interior', 'Veganza Perf./Quilted Smoke White, Veganza Perf./Quilted Espresso Br., Veganza Perf./Quilted Burgundy, Veganza Perf./Quilted Black, Leather Merino Copper B./Atlas Grey, L. Merino Silverstone Ii/Atlas Grey, Leather Merino Black/Atlas Grey, Acc. D. Silver/Fw Ash Grey Blue Op, Acc. D. Silver/Fw Oak Dark Hi. Gl., M Acc. D. Sil./Carb. F./Silv.Th. Hg'),
        (('BMW', 'i5', 'M60 xDrive'), 'Alloy_Wheels', '20" M Star Sp. 938M Bic Jetblack Mt'),
        (('BMW', '7 Series', '740i M Sport'),'Features', 'BMW Curved Display (12.3" + 14.9"), Parking Assistant Plus w/ 360° Camera, Driving Assistant Professional, Adaptive Air Suspension, Soft-Close Doors, 4-Zone Climate Control, Heated/Ventilated Seats, Rear Seat Entertainment, Bowers & Wilkins Diamond Surround, Gesture Control, BMW Laserlight, Comfort Access, Remote Functions via My BMW App.'),
        (('BMW', '7 Series', '740i M Sport'), 'Interior', 'Leather Merino White Smoke, Leather Merino Tartufo, Leather Merino Amarone, Fine-Wood Trim Oak Mirror Finish Grey-Metallic High-Gloss''Leather Merino White Smoke, Leather Merino Tartufo, Leather Merino Amarone, Fine-Wood Trim Oak Mirror Finish Grey-Metallic High-Gloss'),
        (('BMW', '7 Series', '740i M Sport'), 'Alloy_Wheels', '20" M Aerodynamic Wheel 907 M Bicolour With Mixed Tyres'),
        (('BMW', '7 Series', '740d M Sport'),'Features', 'BMW Curved Display (12.3" + 14.9"), Parking Assistant Plus w/ 360° Camera, Driving Assistant Professional, Adaptive Air Suspension, Soft-Close Doors, 4-Zone Climate Control, Heated/Ventilated Seats, Rear Seat Entertainment, Bowers & Wilkins Diamond Surround, Gesture Control, BMW Laserlight, Comfort Access, Remote Functions via My BMW App.'),
        (('BMW', '7 Series', '740d M Sport'), 'Interior', 'Leather Merino White Smoke, Leather Merino Tartufo, Leather Merino Amarone, Fine-Wood Trim Oak Mirror Finish Grey-Metallic High-Gloss'),
        (('BMW', '7 Series', '740d M Sport'), 'Alloy_Wheels', '20" M Aerodynamic Wheel 907 M Bicolour With Mixed Tyres'),
        (('BMW', 'i7', 'eDrive50 M Sport'),'Features', 'BMW Curved Display (12.3" + 14.9"), Bowers & Wilkins Surround, Driving Assistant Pro, Parking Assistant Plus w/ 360° cam, Adaptive Air Suspension, 5-Zone Climate, Heated & Ventilated Seats w/ Massage, Ambient Lighting, Soft-Close Doors, Comfort Access, Remote Functions via My BMW App.'),
        (('BMW', 'i7', 'eDrive50 M Sport'), 'Interior', "Two-Tone Paint. Black Sapphire Metallic, Two-Tone Paint. Oxide Grey Metallic, Fine-Wood trim Oak Mirror Finish Grey-Metallic High-Gloss, Fine-wood trim Ash Flowing Grey, open-pored, Fine-wood trim 'Fineline' Black with metal effect high-gloss, M signature, Carbon Fibre M interior trim with silver stitching/Piano Finish Black"),
        (('BMW', 'i7', 'eDrive50 M Sport'), 'Alloy_Wheels', '21" M Light Alloy Wheels Star-Spoke Style 908 M With Mixed Tyres'),
        (('BMW', 'i7', 'M70 xDrive'),'Features', 'BMW Curved Display (12.3" + 14.9"), Bowers & Wilkins Surround, Driving Assistant Pro, Parking Assistant Plus w/ 360° cam, Adaptive Air Suspension, 5-Zone Climate, Heated & Ventilated Seats w/ Massage, Ambient Lighting, Soft-Close Doors, Comfort Access, Remote Functions via My BMW App.'),
        (('BMW', 'i7', 'M70 xDrive'), 'Interior', "Two-Tone Paint. Black Sapphire Metallic, Two-Tone Paint. Oxide Grey Metallic, Leather Merino', Fine-Wood trim Oak Mirror Finish Grey-Metallic High-Gloss, Fine-wood trim Ash Flowing Grey, open-pored, Fine-wood trim 'Fineline' Black with metal effect high-gloss, M signature, Carbon Fibre M interior trim with silver stitching/Piano Finish Black"),
        (('BMW', 'i7', 'M70 xDrive'), 'Alloy_Wheels','53.3 cm M Aerodynamic Wheels 909M Multicolour 3D Polished Buff with Mixed Tyres' ),
        (('BMW', 'M8', 'Competition Coupé'),'Features', 'BMW Live Cockpit Professional (12.3"), Bowers & Wilkins Diamond Surround, M multifunction seats w/ ventilation, M Sport Exhaust, Adaptive LED/Laserlight, Parking Assistant Plus w/ 360° Cam, Driving Assistant, Adaptive M Suspension, Integral Active Steering, Soft-Close Doors, Ambient Lighting, 4-Zone Climate, Remote Functions via My BMW App.'),
        (('BMW', 'M8', 'Competition Coupé'), 'Interior', "Full Leather 'Merino Interior, Fine-wood trim ash grain grey-metallic high-gloss"),
        (('BMW', 'M8', 'Competition Coupé'), 'Alloy_Wheels', '20" M light alloy wheels Double-spoke style 810 M Jet Black with mixed tyres, 20" M light alloy wheels Double-spoke style 813 M Bicolour Black Grey with mixed tyres, 20" M light alloy wheels Star-spoke style 811 M Bicolour with mixed tyres'),
        (('BMW', 'Z4', 'M40i'),'Features', 'Adaptive M Suspension, Variable Sport Steering, M Sport Differential, Adaptive LED Headlights, Harman Kardon Surround, Live Cockpit Professional (12.3"), 10.25" Control Display, Ambient Lighting, Electrically Adjustable Sports Seats with Memory, 2-zone Climate Control, Parking Assistant with Rear View Camera, Comfort Access with Keyless Entry.'),
        (('BMW', 'Z4', 'M40i'), 'Interior', "Leather 'Vernasca' Magma Red Decor Stitching | Black, Leather 'Vernasca' Cognac Decor Stitching | Black, Leather 'Vernasca' Black Decor Stitching | Black, Interior Trim Finishers Black High-Gloss, Interior Trim Finishers Aluminium 'Mesheffect'"),
        (('BMW', 'Z4', 'M40i'), 'Alloy_Wheels', '19" M Light Alloy Wheels Double-Spoke Style 800 M Bicolour With Mixed Tyres, 19" M Light Alloy Wheels Double-Spoke Style 799 M Bicolour With Mixed Tyres, 19" M Light Alloy Wheels Double-Spoke Style 799 M With Mixed Tyres Jet Black, 19" M Light Alloy Wheels V-Spoke Style 772 M With Mixed Tyres Jet Black, 19"/20" M Law Do. Sp. 800M Bic Mt'),
        (('Audi', 'A4', 'Premium 40 TFSI'), 'Features', 'Virtual Cockpit, MMI Navigation Plus, 10.1-inch infotainment screen, 3-zone climate control, LED headlamps, cruise control, wireless charger, panoramic sunroof, etc.'),
        (('Audi', 'A4', 'Premium 40 TFSI'), 'Interior', 'Multiple leather upholstery options (Atlas Beige, Black, Okapi Brown)'),
        (('Audi', 'A4', 'Premium 40 TFSI'), 'Alloy_Wheels', '17-inch 5-spoke alloy wheels'),
        (('Audi', 'A4', 'Premium Plus 40 TFSI'), 'Features', 'Virtual Cockpit, MMI Navigation Plus, 10.1-inch infotainment screen, 3-zone climate control, LED headlamps, cruise control, wireless charger, panoramic sunroof, etc.'),
        (('Audi', 'A4', 'Premium Plus 40 TFSI'), 'Interior', 'Multiple leather upholstery options (Atlas Beige, Black, Okapi Brown)'),
        (('Audi', 'A4', 'Premium Plus 40 TFSI'), 'Alloy_Wheels', '17-inch 5-spoke alloy wheels'),
        (('Audi', 'A4', 'Technology 40 TFSI'), 'Features', 'Virtual Cockpit, MMI Navigation Plus, 10.1-inch infotainment screen, 3-zone climate control, LED headlamps, cruise control, wireless charger, panoramic sunroof, etc.'),
        (('Audi', 'A4', 'Technology 40 TFSI'), 'Interior', 'Multiple leather upholstery options (Atlas Beige, Black, Okapi Brown)'),
        (('Audi', 'A4', 'Technology 40 TFSI'), 'Alloy_Wheels', '17-inch 5-spoke alloy wheels'),
        (('Audi', 'A6', 'Premium Plus 45 TFSI'), 'Features', 'High-gloss inlays, ambient lighting, Audi Virtual Cockpit Plus, 4-Zone Climate Control, Comfort Seats, MMI Navigation Plus, Bang & Olufsen 3D Sound System, 360° Camera, Park Assist, Panoramic Sunroof, Wireless Charging, Ambient Lighting, etc.'),
        (('Audi', 'A6', 'Premium Plus 45 TFSI'), 'Interior', 'Dual Tone (Mother-of-Pearl Beige / Black, Okapi Brown / Black)'),
        (('Audi', 'A6', 'Premium Plus 45 TFSI'), 'Alloy_Wheels', '18-inch 5-Twin-Spoke Design'),
        (('Audi', 'A6', 'Technology 45 TFSI (Without Matrix)'), 'Features', 'Technology trim without Matrix LED headlights, Audi Virtual Cockpit Plus, 4-Zone Climate Control, Comfort Seats, MMI Navigation Plus, Bang & Olufsen 3D Sound System, 360° Camera, Park Assist, Panoramic Sunroof, Wireless Charging, Ambient Lighting, etc.'),
        (('Audi', 'A6', 'Technology 45 TFSI (Without Matrix)'), 'Interior', 'Dual Tone (Mother-of-Pearl Beige / Black, Okapi Brown / Black)'),
        (('Audi', 'A6', 'Technology 45 TFSI (Without Matrix)'), 'Alloy_Wheels', '18-inch 5-Twin-Spoke Design'),
        (('Audi', 'A6', 'Technology 45 TFSI'), 'Features', 'Premium Plus trim with chrome highlights, wood inlays, ambient lighting, MMI Navigation Plus with MMI Touch, Audi Virtual Cockpit, Matrix LED headlights, 4-zone climate control, Bang & Olufsen 3D sound system, adaptive cruise control, wireless charging, park assist'),
        (('Audi', 'A6', 'Technology 45 TFSI'), 'Interior', 'Dual Tone (Mother-of-Pearl Beige / Black, Okapi Brown / Black)'),
        (('Audi', 'A6', 'Technology 45 TFSI'), 'Alloy_Wheels', '18-inch dual-tone alloys',),
        (('Audi', 'Q3', 'Premium Plus 40 TFSI quattro S tronic'), 'Features', 'Aluminium Satellite inlays, Audi Virtual Cockpit, 10.1-inch MMI touch display with wireless Apple CarPlay/Android Auto, powered front seats with lumbar support, 2-zone climate control, LED headlamps with DRLs, electric tailgate, and a premium 10-speaker sound system.'),
        (('Audi', 'Q3', 'Premium Plus 40 TFSI quattro S tronic'), 'Interior', 'Dual Tone (Okapi Brown and Pearl Beige)'),
        (('Audi', 'Q3', 'Premium Plus 40 TFSI quattro S tronic'), 'Alloy_Wheels', '18-inch alloy wheels'),
        (('Audi', 'Q3', 'Technology 40 TFSI quattro S tronic'), 'Features', 'Aluminium Satellite inlays, Audi Virtual Cockpit, 10.1-inch MMI touch display,powered front seats with lumbar support, 2-zone climate control, Matrix LED headlamps, gesture-controlled tailgate, 360° camera with park assist, Bang & Olufsen 3D sound system, adaptive cruise control, lane departure warning, and upgraded ambient lighting'),
        (('Audi', 'Q3', 'Technology 40 TFSI quattro S tronic'), 'Interior', 'Dual Tone (Okapi Brown and Pearl Beige)'),
        (('Audi', 'Q3', 'Technology 40 TFSI quattro S tronic'), 'Alloy_Wheels', '18-inch alloy wheels'),
        (('Audi', 'Q5', 'Premium Plus 45 TFSI'), 'Features', 'Leather upholstery, aluminium inlays, Panoramic sunroof, 3-zone climate control, 10.1-inch MMI touchscreen with wireless Apple CarPlay, Audi Virtual Cockpit Plus, 30-colour ambient lighting, powered front seats with memory, Audi sound system, powered tailgate'),
        (('Audi', 'Q5', 'Premium Plus 45 TFSI'), 'Interior', 'Dual Tone (Altas Beige / Black with Matte Black Accents and Aluminium Rhombus Inserts, Okapi Brown / Black with with Matte Black Accents and Aluminium Rhombus Inserts)'),
        (('Audi', 'Q5', 'Premium Plus 45 TFSI'), 'Alloy_Wheels', '19-inch 5-double-spoke star design alloys'),
        (('Audi', 'Q5', 'Technology 45 TFSI'), 'Features', 'Leather upholstery, aluminium inlays, 3-zone climate control, Audi Virtual Cockpit Plus, 30-colour ambient lighting, powered front seats with memory, powered tailgate, 19-speaker Bang & Olufsen premium audio, 360-degree camera, Park Assist, wireless phone charging, MMI Navigation Plus with MMI Touch, gesture-controlled tailgate.'),
        (('Audi', 'Q5', 'Technology 45 TFSI'), 'Interior', 'Dual Tone (Altas Beige / Black with Matte Black Accents and Black Piano Lacquer Inserts, Okapi Brown / Black with with Matte Black Accents and Black Piano Lacquer Inserts)'),
        (('Audi', 'Q5', 'Technology 45 TFSI'), 'Alloy_Wheels', '19-inch 5-double-spoke star design alloys',),
        (('Audi', 'Q7', 'Premium Plus TFSI quattro tiptronic'), 'Features', 'LED headlamps, panoramic sunroof, ambient lighting, Audi Virtual Cockpit Plus, dual-screen MMI Navigation Plus, Audi Drive Select (incl. off-road), 4-zone climate control, powered memory front seats, 30-colour ambient lighting, hands-free tailgate, adaptive air suspension, Audi Pre-Sense Basic & Rear.'),
        (('Audi', 'Q7', 'Premium Plus TFSI quattro tiptronic'), 'Interior', 'Dual Tone (Saiga Beige, Okapi Brown)'),
        (('Audi', 'Q7', 'Premium Plus TFSI quattro tiptronic'), 'Alloy_Wheels', '19-inch 5-arm turbine design alloys'),
        (('Audi', 'Q7', 'Technology TFSI quattro tiptronic'), 'Features', 'HD Matrix LED headlights with dynamic turn indicators, panoramic sunroof, Audi Virtual Cockpit Plus (3D nav), dual-screen MMI Navigation Plus with haptic feedback, Bang & Olufsen 3D sound, ventilated & heated massage front seats, Adaptive Cruise & Lane Assist, Park Assist Plus with 360° camera, Night Vision Assist, Head-Up Display, soft-close doors, adaptive air suspension, Audi Phone Box with wireless charging, 30-colour ambient lighting.'),
        (('Audi', 'Q7', 'Technology TFSI quattro tiptronic'), 'Interior', 'Dual Tone (Saiga Beige, Okapi Brown)'),
        (('Audi', 'Q7', 'Technology TFSI quattro tiptronic'), 'Alloy_Wheels', '19-inch 5-arm turbine design alloys'),
        (('Audi', 'Q8', 'TFSI quattro tiptronic'), 'Features', 'High-gloss trim, ambient lighting, Matrix LED headlights,adaptive air suspension,premium Bang & Olufsen 3D sound, Audi Virtual Cockpit, MMI Navigation Plus'),
        (('Audi', 'Q8', 'TFSI quattro tiptronic'), 'Interior', 'Dual Tone (Okapi Brown, Saiga Beige, Black, and Pando Grey)'),
        (('Audi', 'Q8', 'TFSI quattro tiptronic'), 'Alloy_Wheels', '21-inch multi-spoke alloys'),
        (('Audi', 'Q8', 'quattro tiptronic'), 'Features', 'RS sport styling, carbon/aluminum inlays, ambient lighting, Bang & Olufsen 3D sound, 360° camera, adaptive air suspension, dynamic steering, RS performance brakes, sport exhaust'),
        (('Audi', 'Q8', 'quattro tiptronic'), 'Interior', 'Single Tone (Black)'),
        (('Audi', 'Q8', 'quattro tiptronic'), 'Alloy_Wheels', '21-inch or optional 23-inch RS-spec alloys'),
        (('Audi', 'S5', 'SportBack 3.0 TFSI Quattro'), 'Features', 'Aluminium race inlays, S Sport seats, Matrix LED Headlights, Audi Virtual Cockpit Plus, Bang & Olufsen 3D Sound System, Sport Seats with Heating & Ventilation,Adaptive Cruise Control with Stop & Go, 3-Zone Climate Control, Ambient Lighting Package, Powered Tailgate, Keyless Entry & Start, MMI Navigation Plus with Touch, Rear View Camera with Parking Assist'),
        (('Audi', 'S5', 'SportBack 3.0 TFSI Quattro'), 'Interior', 'Alcantara/leather upholstery, contrast stitching'),
        (('Audi', 'S5', 'SportBack 3.0 TFSI Quattro'), 'Alloy_Wheels', '19-inch 5-double-spoke alloys'),
        (('Audi', 'Q8 e-tron', '50 e-tron quattro'), 'Features', 'Advanced Black Styling Package with gloss black grille, roof rails, Fast Charging (0–80% in 30 min [150 kW]), 2 Electric Motors Placed At One motor each on front and rear axle, Panoramic roof, LED headlamps, Adaptive Air Suspension, Audi Virtual Cockpit, MMI Navigation Plus'),
        (('Audi', 'Q8 e-tron', '50 e-tron quattro'), 'Interior', 'Dual Tone (Okapi Brown, Black, Pearl Beige)'),
        (('Audi', 'Q8 e-tron', '50 e-tron quattro'), 'Alloy_Wheels', '20-inch Aero wheels'),
        (('Audi', 'Q8 e-tron', '55 e-tron quattro'), 'Features', 'S line exterior with sport bumpers, chrome detailing, Fast Charging (0–80% in 30 min [150 kW]), 2 Electric Motors Placed At One motor each on front and rear axle, Panoramic roof, LED headlamps, Adaptive Air Suspension, Audi Virtual Cockpit, MMI Navigation Plus'),
        (('Audi', 'Q8 e-tron', '55 e-tron quattro'), 'Interior', 'Dual Tone (Okapi Brown, Black, Pearl Beige)'),
        (('Audi', 'Q8 e-tron', '55 e-tron quattro'), 'Alloy_Wheels', '21-inch dual-tone alloys'),
        (('Audi', 'Q8 Sportback e-tron', '50 e-tron quattro'), 'Features', 'S line exterior styling, Matrix LED headlights w/ dynamic indicators, Virtual Cockpit Plus (3D nav), dual-screen MMI w/ haptic, B&O 3D Sound, ventilated & heated massage seats, adaptive air suspension, adaptive cruise & lane assist, Park Assist Plus (360°), Night Vision, head-up display, soft-close doors, 30-colour ambient lighting.'),
        (('Audi', 'Q8 Sportback e-tron', '50 e-tron quattro'), 'Interior', 'Dual Tone (Black, Okapi Brown, Pearl Beige)'),
        (('Audi', 'Q8 Sportback e-tron', '50 e-tron quattro'), 'Alloy_Wheels', '20-inch Aero alloy wheels (optional 21-inch/22-inch)'),
        (('Audi', 'Q8 Sportback e-tron', '55 e-tron quattro'), 'Features', 'S line exterior with sport bumpers, chrome detailing, Matrix LED headlights w/ dynamic indicators, Virtual Cockpit Plus (3D nav), dual-screen MMI w/ haptic, B&O 3D Sound, ventilated & heated massage seats, adaptive air suspension, adaptive cruise & lane assist, Park Assist Plus (360°), Night Vision, head-up display, soft-close doors, 30-colour ambient lighting.'),
        (('Audi', 'Q8 Sportback e-tron', '55 e-tron quattro'), 'Interior', 'Dual Tone (Black, Okapi Brown, Pearl Beige)'),
        (('Audi', 'Q8 Sportback e-tron', '55 e-tron quattro'), 'Alloy_Wheels', '20-inch Aero alloy wheels (optional 21-inch/22-inch)'),
        (('Audi', 'RS e-tron GT', 'e-tron quattro'), 'Features', 'Gloss black accents with e-tron signature grille, Matrix LED headlights (dynamic), Virtual Cockpit Plus 12.3" (3D nav), 10.1" MMI+ (haptic), B&O 3D sound, ventilated/heated/massage sports seats, 3-zone climate, adaptive air suspension, Drive Select, Park Assist+ (360°), Lane Departure Warning, Adaptive Cruise, Phone Box (wireless+boost), 30-colour ambient lighting, HUD, soft-close doors, auto rear spoiler.'),
        (('Audi', 'RS e-tron GT', 'e-tron quattro'), 'Interior', 'Single Tone (Black)'),
        (('Audi', 'RS e-tron GT', 'e-tron quattro'), 'Alloy_Wheels', '21-inch or optional 22-inch forged alloys'),
    ]

    for feat in car_features:
        try:
            brand, model, variant_name = feat[0]
            category = feat[1]
            description = feat[2]

            cur.execute("""
                SELECT v.variant_id 
                FROM variants v
                JOIN models m ON v.model_id = m.model_id
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE b.brand_name = %s AND m.model_name = %s AND v.variant_name = %s
                LIMIT 1
            """, (brand, model, variant_name))
            row = cur.fetchone()
            if row:
                variant_id = row[0]
                cur.execute("""
                    INSERT INTO features (variant_id, feature_category, feature_description)
                    VALUES (%s, %s, %s)
                """, (variant_id, category, description))
        except Exception as e:
            print(f"Error inserting feature {category} for {variant_name}: {e}")

    conn.commit()
    print("✓ All Features inserted successfully!")

    # ===================== Colors =====================
    car_colors = [
        (('Mercedes-Benz','A Class', 'A200'), 'Cosmos Black, Mountain Grey,Polar White,Iridium Silver, Spectral Blue', 'Metallic'),
        (('Mercedes-Benz','C Class', 'C200'), 'Obsidian Black, Mojave Silver,Selenite Grey,Sodalite Blue, Opalith White, Hi-Tech Silver', 'Metallic'),
        (('Mercedes-Benz','C Class', 'C220d'), 'Obsidian Black, Mojave Silver,Selenite Grey,Sodalite Blue, Opalith White, Hi-Tech Silver', 'Metallic'),
        (('Mercedes-Benz','C Class', 'C300'), 'Obsidian Black,Sodalite Blue, Patagonia red bright, Opalith White', 'Metallic'),
        (('Mercedes-Benz','C Class AMG', 'C 43 4MATIC'), 'Polar White, Selenite Grey Metallic, Sodalite Blue Metallic, Hi Tech Silver, Spectral Blue,  Graphite Grey, Opalite White Bright, Patagonia Red Bright, Graphite Grey Magno', 'Metallic'),
        (('Mercedes-Benz','C Class AMG', 'C 63 S E Performance'), 'Polar White, Selenite Grey Metallic, Sodalite Blue Metallic, Hi Tech Silver, Spectral Blue,  Graphite Grey, Opalith white metallic, Patagonia red metallic bright, Graphite Grey Magno', 'Metallic'),
        (('Mercedes-Benz','E Class', 'E200'), 'High Tech Silver,Graphite Grey,Obsidian Black,Polar White, Nautic Blue', 'Metallic'),
        (('Mercedes-Benz','E Class', 'E200d'), 'High Tech Silver,Graphite Grey,Obsidian Black,Polar White, Nautic Blue', 'Metallic'),
        (('Mercedes-Benz','E Class', 'E450 4Matic'), 'High Tech Silver,Graphite Grey,Obsidian Black,Polar White, Nautic Blue', 'Metallic'),
        (('Mercedes-Benz','S Class', 'S450 4Matic'), 'Diamond White Bright,Onyx Black, Nautic Blue, High Tech Silver', 'Metallic'),
        (('Mercedes-Benz','S Class AMG', 'S 63 E PERFORMANCE'), 'Black, Nautic blue, Salenite Grey, High-Tech Silver, Emerald Green, Obsidian black, Graphite Grey, Verde Silver,Velvet Brown, Opalite White Bright, Rubellite Red Metallic, Kalahari Gold Metallic, Graphite Grey Magno, Opalite White Magno', 'Metallic'),
        (('Mercedes-Benz','EQA', '250 Plus'), 'Polar White,High Tech Silver, Patagonia red, Mountain Grey, Spectral Blue, Cosmos Black', 'Metallic'),
        (('Mercedes-Benz','EQB', '250 Plus'), 'Cosmos Black, Rose Gold, Digital White, Mountain Grey, Iridium Silver', 'Metallic'),
        (('Mercedes-Benz','EQB', '350 4Matic'), 'Cosmos Black, Rose Gold, Digital White, Mountain Grey, Iridium Silver', 'Metallic'),
        (('Mercedes-Benz','EQE', '500 4Matic'), 'Obsidian Black Metallic, Sodalite Blue Metallic, Emerald Green Metallic, Velvet Brown Metallic, High-Tech Silver Metallic, Selenite Grey Metallic, Polar White, Alpine Grey, Diamond White', 'Metallic'),
        (('Mercedes-Benz','EQS', '450 5 Seater'), 'Black Lacquer, Sodalite Blue, Velvet Brown, Polar White, Obsidian Black, Opalite White Bright Metallic, Alpine Grey, Emerald Green', 'Metallic'),
        (('Mercedes-Benz','EQS', '580 4Matic'), 'Black Lacquer, Sodalite Blue, Selenite Grey Metallic, Velvet Brown, Polar White, Obsidian Black, High-Tech Silver, Opalite White Bright Metallic, Alpine Grey, Emerald Green', 'Metallic'),
        (('Mercedes-Benz','EQS', '580 4Matic Celebration Edition'), 'Obsidian Black,Graphite Grey', 'Metallic'),
        (('Mercedes-Benz','GLA', 'GLA200'), 'Polar White, Mountain Grey, Cosmos Black, Iridium Silver, Spectral Blue', 'Metallic'),
        (('Mercedes-Benz','GLA', '220d 4Matic'), 'Polar White, Mountain Grey, Cosmos Black, Iridium Silver, Spectral Blue', 'Metallic'),
        (('Mercedes-Benz','GLA AMG', '220d AMG Line 4Matic'), 'Polar White, Mountain Grey, Cosmos Black, Iridium Silver, Spectral Blue', 'Metallic'),
        (('Mercedes-Benz','GLC', '200d 4Matic'), 'Nautic Blue, Mojave Silver, Graphite Grey, Polar White, Obsidian Black', 'Metallic'),
        (('Mercedes-Benz','GLC', '300 4Matic'), 'Nautic Blue, Mojave Silver, Graphite Grey, Polar White, Obsidian Black', 'Metallic'),
        (('Mercedes-Benz','GLE', '450 4MATIC'), 'Selenite Grey Metallic, Polar White, High-Tech Silver Metallic, Obsidian Black Metallic, Sodalite Blue Metallic', 'Metallic'),
        (('Mercedes-Benz','GLE', '450d 4MATIC'), 'Selenite Grey Metallic, Polar White, High-Tech Silver Metallic, Obsidian Black Metallic, Sodalite Blue Metallic', 'Metallic'),
        (('Mercedes-Benz','GLE AMG', '300d 4MATIC AMG Line'), 'Selenite Grey Metallic, Polar White, High-Tech Silver Metallic, Obsidian Black Metallic, Sodalite Blue Metallic', 'Metallic'),
        (('Mercedes-Benz','GLS', '450 4MATIC'), 'Polar White,Obsidian Black, High-tech Silver, Sodalite Blue,  Selenite Grey', 'Metallic'),
        (('Mercedes-Benz','GLS', '450d 4MATIC'), 'Polar White,Obsidian Black, High-tech Silver, Sodalite Blue,  Selenite Grey', 'Metallic'),
        (('Mercedes-Benz','GLS AMG', '450 4MATIC AMG Line'), 'Polar White,Obsidian Black, High-tech Silver, Sodalite Blue,  Selenite Grey', 'Metallic'),
        (('Mercedes-Benz','GLS AMG', '450d 4MATIC AMG Line'), 'Polar White,Obsidian Black, High-tech Silver, Sodalite Blue,  Selenite Grey', 'Metallic'),
        (('Mercedes-Benz','G Class', 'G 580 with EQ Technology'), 'Obsidian Black, Opalite White Bright, Classic Grey, Opalite White Magno, South Seas Blue Magno', 'Metallic'),
        (('Mercedes-Benz','G Class AMG', 'G 63'), 'Classic G shades + Manufaktur options', 'Metallic'),
        (('Mercedes-Benz','CLE Cabriolet', 'CLE 300 CABRIOLET 4MATIC'), 'Obsidian Black, Graphite Grey, Hi-Tech Silver, Spectral Blue', 'Metallic'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Petrol'), 'Fuji White, Santorini Black, Firenze Red, Eiger Grey, Portofino Blue', 'Solid'),
        (('Jaguar', 'F-Pace', 'S R-Dynamic 2.0 Diesel'), 'Fuji White, Santorini Black, Firenze Red, Eiger Grey, Portofino Blue', 'Solid'),
        (('Volvo', 'EX30', 'RWD Ultra'), 'Cloud Blue,Crystal White,Onyx Black,Vapour Grey,Sand Dune', 'Metallic'),
        (('Volvo', 'EX40', 'Plus'), 'Crystal White,Fjord Blue, Onyx Black, Sage Green, Cloud Blue', 'Metallic'),
        (('Volvo', 'EC40', 'Ultra'), 'Crystal White,Fjord Blue, Onyx Black, Sage Green, Cloud Blue,Fusion Red', 'Metallic'),
        (('Volvo', 'XC60', 'B5 Ultra'), 'Onyx Black, Crystal White, Denim Blue, Fusion Red, Bright Dusk', 'Metallic'),
        (('Volvo', 'XC90', 'B5 Ultra'), 'Onyx Black, Denim Blue, Crystal White, Bright Dusk, Mulberry Red, Vapour Grey', 'Metallic'),
        (('BMW', 'X1', 'sDrive18i M Sport'), 'Alpine White (Non-Metallic)/Black Sapphire (Metallic)/M Portimao Blue (Metallic)/Space Silver (Metallic)/Storm Bay (Metallic)', 'Metallic'),
        (('BMW', 'X1', 'sDrive18d M Sport'), 'Alpine White (Non-Metallic)/Black Sapphire (Metallic)/M Portimao Blue (Metallic)/Space Silver (Metallic)/Storm Bay (Metallic)', 'Metallic'),
        (('BMW', 'X3', 'xDrive20i M Sport'), 'Dune Grey Metallic, Alpine White, Individual Tanzanite Blue, Black Sapphire Metallic', 'Metallic'),
        (('BMW', 'X3', 'xDrive20d M Sport'), 'Dune Grey Metallic, Alpine White, Individual Tanzanite Blue, Black Sapphire Metallic', 'Metallic'),
        (('BMW', 'X5', 'xDrive40i'), 'Mineral White Metallic, SkyScraper Grey Metallic, Black, Sapphire Metallic', 'Metallic'),
        (('BMW', 'X5', 'xDrive30d'), 'Mineral White Metallic, SkyScraper Grey Metallic, Black, Sapphire Metallic', 'Metallic'),
        (('BMW', 'X7', 'xDrive40i M Sport'), 'Mineral White Metallic, Tanzanite Blue Metallic, Skyscraper Grey Metallic, Black Sapphire Metallic', 'Metallic'),
        (('BMW', 'X7', 'xDrive40d M Sport'), 'Mineral White Metallic, Tanzanite Blue Metallic, Skyscraper Grey Metallic, Black Sapphire Metallic', 'Metallic'),
        (('BMW', 'X7', 'xDrive40i M Sport Signature Edition'), 'Mineral White (Metallic),  Black Sapphire (Metallic), Sparkling Copper Grey (Metallic)', 'Metallic'),
        (('BMW', 'XM', 'Plug-in Hybrid'), 'Black Sapphire metallic,  Mineral White metallic,  Cape York Green metallic,  Dravit Grey metallic,  M Carbon Black metallic,  M Marina Bay Blue metallic,  M Toronto Red metallic', 'Metallic'),
        (('BMW', 'iX1 LWB', 'eDrive20L M Sport'), 'Portimao Blue Metallic,  Mineral White Metallic,  Skyscraper Grey Metallic,  Carbon Black Metallic,  Sparkling Cooper Grey Metallic', 'Metallic'),
        (('BMW', 'iX', 'xDrive 50'), 'Black Sapphire Metallic, Sophisto Grey (metallic), Mineral White Metallic,  Phytonic Blue Metallic,  Aventurin Red metallic,  Oxide Grey Metallic,  Storm Bay Metallic', 'Metallic'),
        (('BMW', '2 Series', '218 M Sport'), 'Black Sapphire Metallic, Alpine White, Portimao Blue Metallic, Brooklyn Grey', 'Metallic'),
        (('BMW', '2 Series', '218 M Sport Pro'), 'Black Sapphire Metallic, Alpine White, Portimao Blue Metallic, Brooklyn Grey', 'Metallic'),
        (('BMW', 'M2', '3.0 Petrol'), 'Brooklyn Grey Metallic, Skyscraper Grey Metallic, Dragon Fire Red Metallic, Black Sapphire, Portimao Blue Metallic, Sao Paulo Yellow, M Zandvoort Blue, Alpine White 3', 'Metallic'),
        (('BMW', '3 Series LWB', '330 Li M Sport'), 'Mineral White Metallic, Carbon Black Metallic, Skyscraper Grey Metallic, Arctic Race Blue Metallic', 'Metallic'),
        (('BMW', '3 Series LWB', '320 Ld M Sport'), 'Mineral White Metallic, Carbon Black Metallic, Skyscraper Grey Metallic, Arctic Race Blue Metallic', 'Metallic'),
        (('BMW', '3 Series', 'M340i'), 'Tanzanite Blue Metallic,  Dravit Grey Metallic,  Black Sapphire Metallic, Fire Red,  Arctic Race Blue', 'Metallic'),
        (('BMW', 'M4', 'Competition'), 'Black Sapphire Metallic, Toronto Red Metallic, Skyscraper Grey Metallic, Portimao Blue Metallic, Sao Paulo Yellow Metallic, Isle of Man Green Metallic, Dravit Gey Metallic, Tanzanite Blue Metallic, Aventurine Red Metallic, Brooklyn Grey Metallic', 'Metallic'),
        (('BMW', 'M4', 'CS'), 'Black Sapphire Metallic, Isle of Man Green Metallic, Brooklyn Grey Metallic', 'Metallic'),
        (('BMW', 'i4', 'eDrive40 M Sport'), 'Black Sapphire metallic, Skyscraper Grey metallic, Mineral White metallic', 'Metallic'),
        (('BMW', '5 Series', '530Li M Sport'), 'Carbon Black, Sparkling Cooper Grey', 'Metallic'),
        (('BMW', 'M5', 'Competition'), 'M Carbon Black metallic, Black Sapphire metallic, Sophisto Grey brilliant effect metallic, M Marina Bay Blue metallic, M Isle of Man Green metallic, M Brooklyn Grey metallic, Fire Red metallic', 'Metallic'),
        (('BMW', 'i5', 'M60 xDrive'), 'Alpine White Solid, M Carbon Black Metallic, Black Sapphire Metallic, Sophisto Grey brilliant effect metallic, Mineral White metallic, Phytonic Blue metallic, Oxide Grey metallic, M Brooklyn Grey metallic, Cape York Green metallic, Fire Red metallic, Tanzanite Blue, Frozen Deep Grey metallic, Frozen Pure Grey metallic, Frozen Portimao Blue metallic', 'Metallic'),
        (('BMW', '7 Series', '740i M Sport'), 'Black Sapphire Metallic, Individual Dravit Grey Metallic, Individual Tanzanite Blue Metallic, Brooklyn Grey Metallic, Carbon Black Metallic, Mineral White Metallic, Oxide Grey Metallic', 'Metallic'),
        (('BMW', '7 Series', '740d M Sport'), 'Black Sapphire Metallic, Individual Dravit Grey Metallic, Individual Tanzanite Blue Metallic, Brooklyn Grey Metallic, Carbon Black Metallic, Mineral White Metallic, Oxide Grey Metallic', 'Metallic'),
        (('BMW', 'i7', 'eDrive50 M Sport'), 'Black Sapphire Metallic, Dravit Grey Metallic, Tanzanite Blue Metallic, Brooklyn Grey Metallic, Carbon Black Metallic, Mineral White Metallic, Oxide Grey Metallic', 'Metallic'),
        (('BMW', 'i7', 'M70 xDrive'), 'Black Sapphire Metallic, Dravit Grey Metallic, Tanzanite Blue Metallic, Brooklyn Grey Metallic, Carbon Black Metallic, Mineral White Metallic, Oxide Grey Metallic', 'Metallic'),
        (('BMW', 'M8', 'Competition Coupé'), 'Black Sapphire metallic, Marina Bay Blue metallic, Isle of Man Green metallic, Brooklyn Grey metallic, Skyscraper Grey metallic, Aventurine Red metallic, Tanzanite Blue metallic, Daytona Beach Blue, Dravit Grey metallic', 'Metallic'),
        (('BMW', 'Z4', 'M40i'), 'Alpine White, Black Sapphire metallic, M Portimao Blau metallic, San francisco red metallic, Skyscraper grey metallic, Thundernight metallic', 'Metallic'),
        (('Audi', 'A4', 'Premium 40 TFSI'), 'Navarra Blue, Mythos Black, Glacier White', 'Solid'),
        (('Audi', 'A4', 'Premium Plus 40 TFSI'), 'Navarra Blue, Mythos Black, Glacier White', 'Solid'),
        (('Audi', 'A4', 'Technology 40 TFSI'), 'Mythos Black, Glacier White, Navarra Blue, Tango Red, Manhattan Grey', 'Solid'),
        (('Audi', 'A6', 'Premium Plus 45 TFSI'), 'Glacier White, Firmament Blue Metallic, Mythos Black Metallic, Madeira Brown Metallic, Manhattan Grey Metallic', 'Metallic'),
        (('Audi', 'A6', 'Technology 45 TFSI (Without Matrix)'), 'Glacier White, Firmament Blue Metallic, Mythos Black Metallic, Madeira Brown Metallic, Manhattan Grey Metallic', 'Metallic'),
        (('Audi', 'A6', 'Technology 45 TFSI'), 'Manhattan Grey, Mythos Black, Madeira Brown, Firmament Blue, Glacier White', 'Metallic'),
        (('Audi', 'Q3', 'Premium Plus 40 TFSI quattro S tronic'), 'Pulse Orange, Nano Grey Metallic, Glacier White Metallic, Mythos Black Metallic, Navarra Blue Metallic', 'Metallic'),
        (('Audi', 'Q3', 'Technology 40 TFSI quattro S tronic'), 'Pulse Orange, Nano Grey Metallic, Glacier White Metallic, Mythos Black Metallic, Navarra Blue Metallic', 'Metallic'),
        (('Audi', 'Q5', 'Premium Plus 45 TFSI'), 'Navarra Blue Metallic, Glacier White, Mythos Black Metallic, Manhattan Gray Metallic', 'Metallic'),
        (('Audi', 'Q5', 'Technology 45 TFSI'), 'Navarra Blue Metallic, Glacier White, Mythos Black Metallic, Manhattan Gray Metallic', 'Metallic'),
        (('Audi', 'Q7', 'Premium Plus TFSI quattro tiptronic'), 'Sakhir Gold, Waitomo Blue, Glacier White, Mythos Black, Samurai Grey', 'Metallic'),
        (('Audi', 'Q7', 'Technology TFSI quattro tiptronic'), 'Sakhir Gold, Waitomo Blue, Glacier White, Mythos Black, Samurai Grey', 'Metallic'),
        (('Audi', 'Q8', 'TFSI quattro tiptronic'), 'Glacier White Metallic, Mythos Black Metallic, Sakhir Gold Metallic, Samurai Gray Metallic, Satellite Silver Metallic, Tamarind Brown Metallic, Vicuna Beige Metallic, Waitomo Blue Metallic', 'Metallic'),
        (('Audi', 'Q8', 'quattro tiptronic'), 'Mythos Black Metallic, Glacier White Metallic, Chili Red Metallic, Sakhir Gold Metallic, Satellite Silver Metallic, Waitomo Blue Metallic, Ascari Blue Metallic', 'Metallic'),
        (('Audi', 'S5', 'SportBack 3.0 TFSI Quattro'), 'Tango Red Metallic, Mythos Black Metallic, Ibis White Solid, Navara Blue Metallic, District Green Metallic, Daytona Grey Pearl', 'Metallic'),
        (('Audi', 'Q8 e-tron', '50 e-tron quattro'), 'Magnet Gray, Chronos Gray Metallic, Glacier White Metallic, Madeira Brown Metallic, Manhattan Gray Metallic, Mythos Black Metallic, Plasma Blue Metallic, Siam Beige Metallic, Soneira Red Metallic', 'Metallic'),
        (('Audi', 'Q8 e-tron', '55 e-tron quattro'), 'Magnet Gray, Chronos Gray Metallic, Glacier White Metallic, Madeira Brown Metallic, Manhattan Gray Metallic, Mythos Black Metallic, Plasma Blue Metallic, Siam Beige Metallic, Soneira Red Metallic', 'Metallic'),
        (('Audi', 'Q8 Sportback e-tron', '50 e-tron quattro'), 'Magnet Gray, Chronos Gray Metallic, Glacier White Metallic, Madeira Brown Metallic, Manhattan Gray Metallic, Mythos Black Metallic, Plasma Blue Metallic, Siam Beige Metallic, Soneira Red Metallic', 'Metallic'),
        (('Audi', 'Q8 Sportback e-tron', '55 e-tron quattro'), 'Magnet Gray, Chronos Gray Metallic, Glacier White Metallic, Madeira Brown Metallic, Manhattan Gray Metallic, Mythos Black Metallic, Plasma Blue Metallic, Siam Beige Metallic, Soneira Red Metallic', 'Metallic'),
        (('Audi', 'RS e-tron GT', 'e-tron quattro'), 'Ibis White, Ascari Blue Metallic, Floret Silver Metallic, Kemora Grey Metallic, Mythos Black Metallic, Suzuka Grey Metallic, Tactics Green Metallic, Tango Red Metallic, Daytona Gray Pearl Effect', 'Metallic')
    ]

    for color in car_colors:
        try:
            brand, model, variant_name = color[0]
            color_name = color[1]
            color_type = color[2]

            cur.execute("""
                SELECT v.variant_id 
                FROM variants v
                JOIN models m ON v.model_id = m.model_id
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE b.brand_name = %s AND m.model_name = %s AND v.variant_name = %s
                LIMIT 1
            """, (brand, model, variant_name))
            row = cur.fetchone()
            if row:
                variant_id = row[0]
                cur.execute("""
                    INSERT INTO colors (variant_id, color_name, color_type)
                    VALUES (%s, %s, %s)
                """, (variant_id, color_name, color_type))
        except Exception as e:
            print(f"Error inserting color {color_name} for {variant_name}: {e}")

    conn.commit()
    print("✓ All Colors inserted successfully!")

# ---------- Utility ----------
def generate_booking_id():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=6))
    return "BK" + letters + numbers

def close_connection():
    global cursor, connection
    try:
        if cursor:
            cursor.close()
    except:
        pass
    try:
        if connection:
            connection.close()
    except:
        pass
    print("Database connection closed.")

# ---------- Menus ----------
def main_menu():
    while True:
        print("\n===== AutoSpec Database System SYSTEM =====")
        print("1. User Mode")
        print("2. Admin Mode")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            user_mode()
        elif choice == '2':
            if admin_login():
                admin_mode()
        elif choice == '3':
            print("Thank you for using AutoSpec Database System!")
            break
        else:
            print("Invalid choice! Try again.")

def user_mode():
    while True:
        print("\n===== USER MODE =====")
        print("1. View All Brands")
        print("2. View Cars by Brand")
        print("3. Search & Filter Cars")
        print("4. View Car Details")
        print("5. Book a Car")
        print("6. Back to Main Menu")
        choice = input("Enter your choice (1-6): ").strip()
        if choice == '1':
            view_all_brands()
        elif choice == '2':
            view_cars_by_brand()
        elif choice == '3':
            search_filter_cars()
        elif choice == '4':
            view_car_details()
        elif choice == '5':
            book_car()
        elif choice == '6':
            break
        else:
            print("Invalid choice! Try again.")

def admin_mode():
    while True:
        print("\n===== ADMIN MODE =====")
        print("1. Add/Update Brand/Model/Variant")
        print("2. Delete Car/Model/Variant")
        print("3. View All Bookings")
        print("4. Reset Database")
        print("5. Back to Main Menu")
        choice = input("Enter your choice (1-5): ").strip()
        if choice == '1':
            add_or_update_Brand_Model_Variant()
        elif choice == '2':
            delete_car_data()
        elif choice == '3':
            view_all_bookings()
        elif choice == '4':
            reset_database()
        elif choice == '5':
            break
        else:
            print("Invalid choice! Try again.")

# ---------- Auth ----------
def admin_login():
        pw = input("Enter admin password: ").strip()
        if pw == admin_password:
            print("Admin login successful!")
            return True
        else:
            print("Incorrect password!")
            return False
        
# ---------- User features ----------
def view_all_brands():
    cursor.execute("SELECT brand_name, country_of_origin, year_founded FROM brands")
    brands = cursor.fetchall()
    if brands:
        print("\n===== Available Brands =====")
        for brand in brands:
            print("Brand:", brand[0])
            print("Country:", brand[1])
            print("Established:", brand[2])
            print("-" * 40)
    else:
        print("No brands found!")

def view_cars_by_brand():
    try:
        # Fetch all brands
        cursor.execute("SELECT brand_name FROM brands ORDER BY brand_name")
        brands = [b[0] for b in cursor.fetchall()]

        if not brands:
            print("No brands available.")
            return

        # Display brands with numbers
        print("\nAvailable Brands:")
        for i, brand in enumerate(brands, 1):
            print(f"{i}. {brand}")

        # Input: brand by name or number
        brand_input = input("\nEnter brand name or number: ").strip()

        if brand_input.isdigit():
            idx = int(brand_input) - 1
            if 0 <= idx < len(brands):
                selected_brand = brands[idx]
            else:
                print("Invalid brand number.")
                return
        else:
            match = [b for b in brands if b.lower() == brand_input.lower()]
            if not match:
                print("Brand not found.")
                return
            selected_brand = match[0]

        # Fetch models for selected brand
        cursor.execute("""
            SELECT model_name
            FROM models m
            JOIN brands b ON m.brand_id = b.brand_id
            WHERE b.brand_name = %s
            ORDER BY model_name
        """, (selected_brand,))
        models = [m[0] for m in cursor.fetchall()]

        if models:
            print(f"\nModels for {selected_brand}:")
            for i, model in enumerate(models, 1):
                print(f"{i}. {model}")
        else:
            print(f"No models found for brand: {selected_brand}")

    except Exception as e:
        print("Error fetching models:", e)
        
def search_filter_cars():
    print("\nSearch Filters:")
    print("1. By Price Range")
    print("2. By Fuel Type")
    print("3. By Body Type")
    choice = input("Select filter (1-3): ").strip()
    
    try:
        if choice == '1':
            min_price = input("Enter minimum price (INR): ").strip()
            max_price = input("Enter maximum price (INR): ").strip()
            try:
                min_val = float(min_price)
                max_val = float(max_price)
            except:
                print("Please enter numeric values.")
                return
            query = """
                SELECT b.brand_name, m.model_name, v.variant_name, v.price_inr
                FROM variants v
                JOIN models m ON v.model_id = m.model_id
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE v.price_inr BETWEEN %s AND %s
            """
            cursor.execute(query, (min_val, max_val))
            
        elif choice == '2':
            fuel = input("Enter fuel type (Petrol/Diesel/Electric/Hybrid): ").strip().lower()
            cursor.execute("""
                SELECT b.brand_name, m.model_name, v.variant_name, v.price_inr
                FROM variants v
                JOIN models m ON v.model_id = m.model_id
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE LOWER(v.fuel_type) LIKE %s
            """, ('%'+fuel+'%',))
            
        elif choice == '3':
            body = input("Enter body type (Sedan/SUV/Coupé/Roadster): ").strip().lower()
            cursor.execute("""
                SELECT b.brand_name, m.model_name, v.variant_name, v.price_inr
                FROM variants v
                JOIN models m ON v.model_id = m.model_id
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE LOWER(m.body_type) LIKE %s
            """, ('%'+body+'%',))
        else:
            print("Invalid choice.")
            return
            
        res = cursor.fetchall()
        if res:
            print("\nSearch Results:")
            for c in res:
                if c[3]:
                    price = "₹" + str(format(c[3], ",.2f"))
                else:
                    price = "Price TBD"
                print("- " + str(c[0]) + " " + str(c[1]) + " " + str(c[2]) + " - " + price)
        else:
            print("No cars found matching criteria.")
            
    except Exception as e:
        print("Error searching cars:", e)

def view_car_details():
    try:
        cursor.execute("SELECT brand_name FROM brands ORDER BY brand_name")
        brands = [b[0] for b in cursor.fetchall()]
        if not brands:
            print("No brands available.")
            return

        print("\nAvailable Brands:")
        for i, b in enumerate(brands, 1):
            print(str(i) + ". " + b)

        brand_choice = input("\nChoose a brand (number or name): ").strip()
        if brand_choice.isdigit():
            idx = int(brand_choice) - 1
            if 0 <= idx < len(brands):
                selected_brand = brands[idx]
            else:
                print("Invalid selection.")
                return
        else:
            match = [b for b in brands if b.lower() == brand_choice.lower()]
            if match:
                selected_brand = match[0]
            else:
                print("Brand not found.")
                return

        cursor.execute("""
            SELECT m.model_name
            FROM models m
            JOIN brands b ON m.brand_id = b.brand_id
            WHERE b.brand_name = %s
            ORDER BY m.model_name
        """, (selected_brand,))
        models = [m[0] for m in cursor.fetchall()]
        if not models:
            print("No models available for this brand.")
            return

        print("\nModels under " + selected_brand + ":")
        for i, m in enumerate(models, 1):
            print(str(i) + ". " + m)

        model_choice = input("\nChoose a model (number or name): ").strip()
        if model_choice.isdigit():
            idx = int(model_choice) - 1
            if 0 <= idx < len(models):
                selected_model = models[idx]
            else:
                print("Invalid selection.")
                return
        else:
            match = [m for m in models if m.lower() == model_choice.lower()]
            if match:
                selected_model = match[0]
            else:
                print("Model not found.")
                return

        cursor.execute("""
            SELECT v.variant_id, v.variant_name, v.price_inr, v.engine, v.power_bhp, v.torque_nm,
                   v.top_speed_kmh, v.acceleration_0_100, v.transmission, v.drivetrain, v.fuel_type,
                   v.mileage_range, v.seating_capacity, v.safety_rating
            FROM variants v
            JOIN models m ON v.model_id = m.model_id
            JOIN brands b ON m.brand_id = b.brand_id
            WHERE b.brand_name = %s AND m.model_name = %s
            ORDER BY v.variant_name
        """, (selected_brand, selected_model))
        variants = cursor.fetchall()
        if not variants:
            print("No variants available for this model.")
            return

        print("\nVariants for " + selected_model + ":")
        for i, v in enumerate(variants, 1):
            if v[2]:
                price = "₹" + str(format(v[2], ",.2f"))
            else:
                price = "Price TBD"
            print(str(i) + ". " + v[1] + " - " + price)

        variant_choice = input("\nChoose a variant (number or name): ").strip()
        if variant_choice.isdigit():
            idx = int(variant_choice) - 1
            if 0 <= idx < len(variants):
                selected = variants[idx]
            else:
                print("Invalid selection.")
                return
        else:
            match = [v for v in variants if v[1].lower() == variant_choice.lower()]
            if match:
                selected = match[0]
            else:
                print("Variant not found.")
                return

        selected_variant_id = selected[0]
        selected_variant_name = selected[1]

        print("\nMain specs for " + selected_variant_name + ":")
        if selected[2]:
            print("Price: ₹" + str(format(selected[2], ",")))
        else:
            print("Price: Price TBD")
        print("- " + "Engine: " + str(selected[3]))
        print("- " + "Power: " + str(selected[4]) + " BHP")
        print("- " + "Torque: " + str(selected[5]) + " Nm")
        print("- " + "Top Speed: " + str(selected[6]) + " km/h")
        print("- " + "0-100 km/h: " + str(selected[7]) + " s")
        print("- " + "Transmission: " + str(selected[8]))
        print("- " + "Drivetrain: " + str(selected[9]))
        print("- " + "Fuel Type: " + str(selected[10]))
        print("- " + "Mileage: " + str(selected[11]))
        print("- " + "Seating Capacity: " + str(selected[12]))
        print("- " + "Safety Rating: " + str(selected[13]))

        cursor.execute("""
            SELECT feature_category, feature_description
            FROM features
            WHERE variant_id = %s
        """, (selected_variant_id,))
        features = cursor.fetchall()
        if features:
            print("\nFeatures for " + selected_variant_name + ":")
            for f in features:
                print("- " + f[0]+": ",f[1],sep='\n')
        else:
            print("No features available for this variant.")

        cursor.execute("""
            SELECT color_name, color_type
            FROM colors
            WHERE variant_id = %s
        """, (selected_variant_id,))
        colors = cursor.fetchall()
        if colors:
            print("\nAvailable colors for " + selected_variant_name + ":")
            for c in colors:
                print("- " + c[0] + " (" + c[1] + ")")
        else:
            print("No colors available for this variant.")

    except Exception as e:
        print("Error viewing car details:", e)

def book_car():
    try:
        cursor.execute("SELECT brand_name FROM brands ORDER BY brand_name")
        brands = [b[0] for b in cursor.fetchall()]
        if not brands:
            print("No brands available.")
            return

        print("\nAvailable Brands:")
        for i, b in enumerate(brands, 1):
            print(str(i) + ". " + b)

        brand_choice = input("Enter brand name or number: ").strip()
        if brand_choice.isdigit():
            idx = int(brand_choice) - 1
            if 0 <= idx < len(brands):
                brand_input = brands[idx]
            else:
                print("Invalid selection.")
                return
        else:
            brand_input = brand_choice
            if brand_input not in brands:
                print("Brand not found.")
                return

        cursor.execute("""
            SELECT model_name
            FROM models m
            JOIN brands b ON m.brand_id = b.brand_id
            WHERE b.brand_name = %s
            ORDER BY model_name
        """, (brand_input,))
        models = [m[0] for m in cursor.fetchall()]
        if not models:
            print("No models found for brand:", brand_input)
            return

        print("\nAvailable Models:")
        for i, m in enumerate(models, 1):
            print(str(i) + ". " + m)

        model_input = input("Enter model name or number: ").strip()
        if model_input.isdigit():
            idx = int(model_input) - 1
            if 0 <= idx < len(models):
                model_input = models[idx]
            else:
                print("Invalid selection.")
                return
        else:
            if model_input not in models:
                print("Model not found.")
                return

        cursor.execute("""
            SELECT variant_name, price_inr
            FROM variants v
            JOIN models m ON v.model_id = m.model_id
            JOIN brands b ON m.brand_id = b.brand_id
            WHERE b.brand_name = %s AND m.model_name = %s
            ORDER BY variant_name
        """, (brand_input, model_input))
        variants = cursor.fetchall()
        if not variants:
            print("No variants found for model:", model_input)
            return

        print("\nAvailable Variants:")
        for i, v in enumerate(variants, 1):
            if v[1]:
                price = "₹" + str(format(v[1], ",.2f"))
            else:
                price = "Price TBD"
            print(str(i) + ". " + v[0] + " - " + price)

        variant_choice = input("Enter variant name or number: ").strip()
        if variant_choice.isdigit():
            idx = int(variant_choice) - 1
            if 0 <= idx < len(variants):
                variant_input = variants[idx][0]
                variant_price = variants[idx][1]
            else:
                print("Invalid selection.")
                return
        else:
            found = False
            for v in variants:
                if v[0] == variant_choice:
                    variant_input = v[0]
                    variant_price = v[1]
                    found = True
                    break
            if not found:
                print("Variant not found.")
                return

        customer_name = input("Enter your name: ")
        customer_contact = input("Enter your contact number: ").strip()
        customer_email = input("Enter your email address: ").strip()

        booking_id = generate_booking_id()
        cursor.execute("""
            INSERT INTO bookings (booking_id, variant_id, customer_name, customer_contact, customer_email, status)
            SELECT %s, v.variant_id, %s, %s, %s,'Active'
            FROM variants v
            JOIN models m ON v.model_id = m.model_id
            JOIN brands b ON m.brand_id = b.brand_id
            WHERE b.brand_name = %s AND m.model_name = %s AND v.variant_name = %s
            LIMIT 1
        """, (booking_id, customer_name, customer_contact, customer_email, brand_input, model_input, variant_input))
        connection.commit()

        print("\nBooking Successful!")
        print("Booking ID:", booking_id)
        print("Car:", brand_input, model_input, variant_input)
        print("Customer:", customer_name)

    except Exception as e:
        print("Error booking car:", e)

# ---------- Admin features ----------
def add_or_update_Brand_Model_Variant():
    try:
        # ---------- BRAND ----------
        cursor.execute("SELECT brand_name, country_of_origin, year_founded FROM brands ORDER BY brand_name")
        brands = cursor.fetchall()
        if brands:
            print("\nExisting Brands:")
            for i, (name, country, year) in enumerate(brands, 1):
                print(i, ".", name, "-", country, "-", year)

        bname = input("Enter brand name: ").strip()
        cursor.execute("SELECT brand_id FROM brands WHERE brand_name = %s", (bname,))
        brand = cursor.fetchone()

        if brand:
            brand_id = brand[0]
            print("Brand exists, continuing…")
        else:
            print("Brand does not exist, Creating brand…")
            country = input("Enter country of origin: ").strip()
            year = input("Enter year founded: ").strip()
            cursor.execute(
                "INSERT INTO brands (brand_name, country_of_origin, year_founded) VALUES (%s, %s, %s)",
                (bname, country, int(year))
            )
            connection.commit()
            brand_id = cursor.lastrowid
            print("Brand created.")

        # ---------- MODEL ----------
        cursor.execute("SELECT model_name FROM models WHERE brand_id = %s ORDER BY model_name", (brand_id,))
        models = [m[0] for m in cursor.fetchall()]
        if models:
            print("\nExisting Models for this brand:")
            for i, m in enumerate(models, 1):
                print(i, ".", m)

        mname = input("Enter model name: ").strip()
        cursor.execute("SELECT model_id FROM models WHERE brand_id = %s AND model_name = %s", (brand_id, mname))
        model = cursor.fetchone()

        if model:
            model_id = model[0]
            print("Model exists, continuing…")
        else:
            print("Model does not exist, Creating Model")
            body = input("Enter body type: ").strip()
            category = input("Enter category: ").strip()
            cursor.execute(
                "INSERT INTO models (brand_id, model_name, body_type, category) VALUES (%s, %s, %s, %s)",
                (brand_id, mname, body, category)
            )
            connection.commit()
            model_id = cursor.lastrowid
            print("Model created.")

        # ---------- VARIANT ----------
        # Fetch and display all variants for the given model
        cursor.execute("SELECT variant_id, variant_name FROM variants WHERE model_id = %s", (model_id,))
        variants = cursor.fetchall()

        if variants:
            print("Existing variants for this model:")
            for index, v in enumerate(variants, start=1):
                print(str(index) + ". " + v[1])
        else:
            print("No variants exist for this model yet.")

        # Ask the user for the variant name
        vname = input("Enter variant name: ").strip()

        # Check if the entered variant exists
        cursor.execute(
            "SELECT variant_id FROM variants WHERE model_id = %s AND variant_name = %s",
            (model_id, vname)
        )
        variant = cursor.fetchone()

        if variant:
            vid = variant[0]
            print("Variant exists, you can update details.")
        else:
            vid = None
            print("Variant does not exist, creating new.")


        # ---------- VARIANT DETAILS ----------
        price = input("Enter price (INR, press Enter to skip): ").strip()
        engine = input("Enter engine: ").strip()
        power = input("Enter power (BHP): ").strip()
        torque = input("Enter torque (Nm): ").strip()
        tops = input("Enter top speed (km/h): ").strip()
        accel = input("Enter 0-100 (s): ").strip()
        trans = input("Enter transmission: ").strip()
        drive = input("Enter drivetrain: ").strip()
        fuel = input("Enter fuel type: ").strip()
        mileage = input("Enter mileage/range: ").strip()
        seats = input("Enter seating capacity: ").strip()
        safety = input("Enter safety rating: ").strip()

        params = [
            float(price) if price else None,
            engine or None,
            int(power) if power else None,
            int(torque) if torque else None,
            int(tops) if tops else None,
            float(accel) if accel else None,
            trans or None,
            drive or None,
            fuel or None,
            mileage or None,
            int(seats) if seats else None,
            safety or None
        ]

        if vid:
            # Update existing variant
            cursor.execute("""
                UPDATE variants SET price_inr=%s, engine=%s, power_bhp=%s, torque_nm=%s,
                                    top_speed_kmh=%s, acceleration_0_100=%s, transmission=%s,
                                    drivetrain=%s, fuel_type=%s, mileage_range=%s,
                                    seating_capacity=%s, safety_rating=%s
                WHERE variant_id=%s
            """, params + [vid])
            connection.commit()
            print("Variant updated.")
        else:
            # Add new variant
            cursor.execute("""
                INSERT INTO variants (model_id, variant_name, price_inr, engine, power_bhp, torque_nm,
                                      top_speed_kmh, acceleration_0_100, transmission, drivetrain,
                                      fuel_type, mileage_range, seating_capacity, safety_rating)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, [model_id, vname] + params)
            connection.commit()
            print("Variant added.")

    except Exception as e:
        print("Error in Add/Update flow:", e)
        
def delete_car_data():
    try:
        print("1. Delete Brand")
        print("2. Delete Model")
        print("3. Delete Variant")
        choice = input("Select (1-3): ").strip()

        # Get brand list (common for all choices)
        cursor.execute("SELECT brand_name FROM brands ORDER BY brand_name")
        brands = [b[0] for b in cursor.fetchall()]
        if not brands:
            print("No brands found.")
            return

        print("\nAvailable Brands:")
        for i, b in enumerate(brands, 1):
            print(i, ".", b)

        # Get brand selection
        binput = input("\nEnter brand number or name: ").strip()
        if binput.isdigit():
            bnum = int(binput)
            if bnum < 1 or bnum > len(brands):
                print("Invalid number.")
                return
            bname = brands[bnum - 1]
        else:
            bname = binput
            if bname not in brands:
                print("Brand not found.")
                return

        if choice == '1':
            # Delete Brand
            cursor.execute("DELETE FROM brands WHERE brand_name = %s", (bname,))
            if cursor.rowcount > 0:
                connection.commit()
                print("Brand deleted successfully.")
            else:
                print("Brand not found.")

        elif choice == '2' or choice == '3':
            # Get models for this brand
            cursor.execute("""
                SELECT m.model_name FROM models m
                JOIN brands b ON m.brand_id = b.brand_id
                WHERE b.brand_name = %s ORDER BY m.model_name
            """, (bname,))
            models = [m[0] for m in cursor.fetchall()]
            if not models:
                print("No models found for this brand.")
                return

            print("\nAvailable Models:")
            for i, m in enumerate(models, 1):
                print(i, ".", m)

            # Get model selection
            minput = input("\nEnter model number or name: ").strip()
            if minput.isdigit():
                mnum = int(minput)
                if mnum < 1 or mnum > len(models):
                    print("Invalid number.")
                    return
                mname = models[mnum - 1]
            else:
                mname = minput
                if mname not in models:
                    print("Model not found.")
                    return

            if choice == '2':
                # Delete Model
                cursor.execute("""
                    DELETE FROM models
                    WHERE model_name = %s AND brand_id = (SELECT brand_id FROM brands WHERE brand_name = %s)
                """, (mname, bname))

                if cursor.rowcount > 0:
                    connection.commit()
                    print("Model deleted successfully.")
                else:
                    print("Model not found.")

            elif choice == '3':
                # Get variants for this model
                cursor.execute("""
                    SELECT v.variant_name FROM variants v
                    JOIN models m ON v.model_id = m.model_id
                    JOIN brands b ON m.brand_id = b.brand_id
                    WHERE b.brand_name = %s AND m.model_name = %s ORDER BY v.variant_name
                """, (bname, mname))
                variants = [v[0] for v in cursor.fetchall()]
                if not variants:
                    print("No variants found for this model.")
                    return

                print("\nAvailable Variants:")
                for i, v in enumerate(variants, 1):
                    print(i, ".", v)

                # Get variant selection
                vinput = input("\nEnter variant number or name to delete: ").strip()
                if vinput.isdigit():
                    vnum = int(vinput)
                    if vnum < 1 or vnum > len(variants):
                        print("Invalid number.")
                        return
                    vname = variants[vnum - 1]
                else:
                    vname = vinput
                    if vname not in variants:
                        print("Variant not found.")
                        return

                # Delete Variant
                cursor.execute("""
                    DELETE FROM variants
                    WHERE model_id = (SELECT model_id FROM models m
                                      JOIN brands b ON m.brand_id = b.brand_id
                                      WHERE b.brand_name = %s AND m.model_name = %s LIMIT 1)
                      AND variant_name = %s
                """, (bname, mname, vname))

                if cursor.rowcount > 0:
                    connection.commit()
                    print("Variant deleted successfully.")
                else:
                    print("Variant not found.")

        else:
            print("Invalid option.")

    except Exception as e:
        print("Error deleting:", e)

def view_all_bookings():
    try:
        cursor.execute("""
            SELECT bk.booking_id, b.brand_name, m.model_name, v.variant_name,
                   bk.customer_name, bk.customer_contact, bk.customer_email, bk.booking_date, bk.status
            FROM bookings bk
            JOIN variants v ON bk.variant_id = v.variant_id
            JOIN models m ON v.model_id = m.model_id
            JOIN brands b ON m.brand_id = b.brand_id
            ORDER BY bk.booking_date DESC
        """)
        rows = cursor.fetchall()
        
        if rows:
            print("\nAll Bookings:")
            for i, r in enumerate(rows, 1):
                print(str(i) + ". Booking ID: " + str(r[0]))
                print("   Car: " + str(r[1]) + " " + str(r[2]) + " - " + str(r[3]))
                print("   Customer: " + str(r[4]) + " (" + str(r[5]) + ") (" + str(r[6]) + ")")
                print("   Date: " + str(r[7]) + " | Status: " + str(r[8]))
                print("-" * 40)
        else:
            print("No bookings found.")
            
    except Exception as e:
        print("Error fetching bookings:", e)

def reset_database():
    confirm = input("⚠️ Are you sure you want to CLEAR ALL DATA and reload? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Cancelled database reset.")
        return

    try:
        cursor.execute("DELETE FROM bookings")
        cursor.execute("DELETE FROM features")
        cursor.execute("DELETE FROM colors")
        cursor.execute("DELETE FROM variants")
        cursor.execute("DELETE FROM models")
        cursor.execute("DELETE FROM brands")
        connection.commit()
        print("✓ All data cleared successfully!")

        insert_sample_data(cursor, connection)
        print("✓ Database reset and reloaded with fresh data!")

    except Exception as e:
        print("Error resetting database:", e)

# ---------- Main ----------
def main():
    print("Starting AutoSpec Database System System...")
    if not connect_database():
        print("Failed to setup database. Exiting.")
        return

    try:
        cursor.execute("SELECT COUNT(*) FROM brands")
        c = cursor.fetchone()
        if c and c[0] == 0:
            print("No data found — inserting data...")
            insert_sample_data(cursor, connection)
    except Exception:
        pass

    try:
        main_menu()
    except Exception as e:
        print("Unexpected error:", e)
    finally:
        close_connection()

main()
