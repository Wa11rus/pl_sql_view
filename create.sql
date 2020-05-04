CREATE TABLE locations (
    location_id   INTEGER NOT NULL PRIMARY KEY,
    latitude      FLOAT NOT NULL,
    longitude     FLOAT NOT NULL
);

CREATE TABLE params (
    params_id    INTEGER NOT NULL PRIMARY KEY,
    brightness   FLOAT NOT NULL,
    frp          FLOAT NOT NULL
);

CREATE TABLE confidence (
    confidence INTEGER NOT NULL PRIMARY KEY
);

CREATE TABLE fire_info (
    fire_id       INTEGER NOT NULL PRIMARY KEY,
    location_id   INTEGER NOT NULL,
    params_id     INTEGER NOT NULL,
    confidence    INTEGER NOT NULL
);

ALTER TABLE fire_info
    ADD CONSTRAINT fk_location_id FOREIGN KEY ( location_id )
        REFERENCES locations ( location_id );

ALTER TABLE fire_info
    ADD CONSTRAINT fk_params_id FOREIGN KEY ( params_id )
        REFERENCES params ( params_id );

ALTER TABLE fire_info
    ADD CONSTRAINT fk_confidence FOREIGN KEY ( confidence )
        REFERENCES confidence ( confidence );
