CREATE TABLE IF NOT EXISTS race_program (
    id SERIAL PRIMARY KEY,
    yaris_gunu DATE,
    hipodrom VARCHAR(100),
    kosu_no INT,
    saat TIME,
    mesafe INT,
    pist VARCHAR(20),
    at_sayisi INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
