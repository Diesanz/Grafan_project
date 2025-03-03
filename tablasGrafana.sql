create database grafana
create user 'grafanareader'@'localhost' identified by 'Grupo6esi';
grant all privileges on grafana.* TO 'grafanareader'@'localhost';

CREATE TABLE cpu (
    timestamp TIMESTAMP default current_timeStamp,
    carga float NOT NULL,
    frecuencia float NOT NULL,
    PRIMARY KEY(timestamp)
);

CREATE TABLE memoria (
    timestamp TIMESTAMP default current_timeStamp,
    ram float NOT NULL,
    swap float NOT NULL,
    PRIMARY KEY(timestamp)
);

CREATE TABLE disco (
    timestamp TIMESTAMP default current_timeStamp,
    espacio float NOT NULL,
    PRIMARY KEY(timestamp)
);

CREATE TABLE entradasalida (
    timestamp TIMESTAMP default current_timeStamp,
    operaciones int NOT NULL,
    PRIMARY KEY(timestamp)
);

CREATE TABLE procesos (
    timestamp TIMESTAMP default current_timeStamp,
    id int NOT NULL,
    activo tinyint(1) NOT NULL,  --tinyint(1) = booleano
    PRIMARY KEY(timestamp)
);

CREATE TABLE red (
    timestamp TIMESTAMP default current_timeStamp,
    bytes_enviados int NOT NULL,
    bytes_recibidos int NOT NULL,
    conexiones_activas int NOT NULL,
    PRIMARY KEY(timestamp)
);