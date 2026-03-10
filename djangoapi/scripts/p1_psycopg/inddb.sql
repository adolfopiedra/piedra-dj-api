CREATE DATABASE infraverde;
CREATE EXTENSION postgis;
CREATE SCHEMA apm;

CREATE TABLE apm.trees (
    id integer SERIAL PRIMARY KEY,
    description character varying,
    geom public.geometry(Point,25830),
    species character varying,
    height real,
    condition character varying,
    is_protected boolean
);

CREATE TABLE apm.corridors (
    id integer SERIAL PRIMARY KEY,
    description character varying,
    dist double precision,
    geom public.geometry(LineString,25830),
    type character varying,
    width real,
    lighting boolean
);

CREATE TABLE apm.parks (
    id integer SERIAL PRIMARY KEY,
    description character varying,
    area double precision,
    geom public.geometry(Polygon,25830),
    type character varying,
    management character varying,
    equipment boolean
);

