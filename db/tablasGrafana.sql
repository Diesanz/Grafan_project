create database grafana
create user 'grafanareader'@'localhost' identified by 'Grupo6esi';
grant all privileges on grafana.* TO 'grafanareader'@'localhost';

-- Crear las tablas con correcciones
CREATE TABLE cpu (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    carga FLOAT NOT NULL,
    frecuencia FLOAT NOT NULL,
    PRIMARY KEY(timestamp)
);

CREATE TABLE memoria (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ram FLOAT NOT NULL,
    swap FLOAT NOT NULL,
    PRIMARY KEY(timestamp)
);

CREATE TABLE disco (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    espacio FLOAT NOT NULL,
    PRIMARY KEY(timestamp)
);

CREATE TABLE entradasalida (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operaciones INT NOT NULL,
    PRIMARY KEY(timestamp)
);

CREATE TABLE procesos (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id INT NOT NULL,
    activo TINYINT(1) NOT NULL,  -- tinyint(1) = booleano
    PRIMARY KEY(timestamp)
);

CREATE TABLE red (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bytes_enviados INT NOT NULL,
    bytes_recibidos INT NOT NULL,
    conexiones_activas INT NOT NULL,
    PRIMARY KEY(timestamp)
);

DELIMITER //

CREATE PROCEDURE `AddDatos` (
    IN `carga_cpu` FLOAT, 
    IN `frecuencia_cpu` FLOAT, 
    IN `mem_ram` FLOAT, 
    IN `mem_swap` FLOAT,
    IN `espacio_disco` FLOAT,
    IN `io_operaciones` INT,
    IN `proc_id` INT,
    IN `proc_activo` TINYINT(1),
    IN `bytes_env` INT,
    IN `bytes_rec` INT,
    IN `conexiones` INT
)
BEGIN
    DECLARE ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

    -- Manejo de errores con ROLLBACK si hay fallo
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK; -- Revertir cambios si hay error
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ERROR al insertar datos';
    END;

    START TRANSACTION; -- Empezar una transacción

    INSERT INTO cpu (timestamp, carga, frecuencia) VALUES (ts, carga_cpu, frecuencia_cpu);

    INSERT INTO memoria (timestamp, ram, swap) VALUES (ts, mem_ram, mem_swap);

    INSERT INTO disco (timestamp, espacio) VALUES (ts, espacio_disco);

    INSERT INTO entradasalida (timestamp, operaciones) VALUES (ts, io_operaciones);

    INSERT INTO procesos (timestamp, id, activo) VALUES (ts, proc_id, proc_activo);
    
    INSERT INTO red (timestamp, bytes_enviados, bytes_recibidos, conexiones_activas) VALUES (ts, bytes_env, bytes_rec, conexiones);

    COMMIT; -- Confirmar los cambios si todo va bien
END //

DELIMITER ;
