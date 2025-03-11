-- Eliminar las tablas si existen
DROP TABLE IF EXISTS cpu;
DROP TABLE IF EXISTS memoria;
DROP TABLE IF EXISTS disco;
DROP TABLE IF EXISTS entradasalida;
DROP TABLE IF EXISTS num_procesos;
DROP TABLE IF EXISTS procesos;
DROP TABLE IF EXISTS red;
DROP TABLE IF EXISTS hilos;
DROP TABLE IF EXISTS interfaces;
DROP TABLE IF EXISTS puertos_abiertos;
-- DROP TABLE IF EXISTS temperatura;


DROP PROCEDURE IF EXISTS AddDatos;

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

CREATE TABLE num_procesos(
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    numero INT NOT NULL,
    PRIMARY KEY(timestamp)
); --esta tabla se puede quitar se puede hacer un count de procesos

CREATE TABLE procesos (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    pid INT NOT NULL,
    cpu_percent FLOAT NOT NULL,
    memory_percent FLOAT NOT NULL,
    vsz FLOAT NOT NULL,
    rss FLOAT NOT NULL,
    usuario VARCHAR(255) NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    ruta VARCHAR(255) NOT NULL,
    hilos INT NOT NULL,
    estado VARCHAR(255) NOT NULL -- tinyint(1) = booleano
);

CREATE TABLE red (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    bytes_enviados INT NOT NULL,
    bytes_recibidos INT NOT NULL,
    conexiones_activas INT NOT NULL,
    paquetes_enviados INT NOT NULL,
    paquetes_recibidos INT NOT NULL,
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
    IN `num_proc` INT,
    IN `bytes_env` INT,
    IN `bytes_rec` INT,
    IN `conexiones` INT,
    IN `paq_env` INT,
    IN `paq_rec` INT
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

    DELETE FROM cpu;

    INSERT INTO cpu (timestamp, carga, frecuencia) VALUES (ts, carga_cpu, frecuencia_cpu);

    INSERT INTO memoria (timestamp, ram, swap) VALUES (ts, mem_ram, mem_swap);

    DELETE FROM disco;

    INSERT INTO disco (timestamp, espacio) VALUES (ts, espacio_disco);

    INSERT INTO entradasalida (timestamp, operaciones) VALUES (ts, io_operaciones);

    DELETE FROM num_procesos;

    INSERT INTO num_procesos (timestamp, numero) VALUES (ts, num_proc);

    -- Insertar información de red
    INSERT INTO red (timestamp, bytes_enviados, bytes_recibidos, conexiones_activas, paquetes_enviados, paquetes_recibidos) VALUES (ts, bytes_env, bytes_rec, conexiones, paq_env, paq_rec);

    COMMIT; -- Confirmar los cambios si todo va bien
END //

DELIMITER ;