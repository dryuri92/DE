--
-- PostgreSQL database dump
--
CREATE SCHEMA cd;



-- Dumped from database version 9.2.0
-- Dumped by pg_dump version 9.2.0
-- Started on 2013-05-19 16:05:10 BST

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 7 (class 2615 OID 32769)
-- Name: cd; Type: SCHEMA; Schema: -; Owner: -
--

SET search_path = cd, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

-- Table: cd.events

-- DROP TABLE IF EXISTS cd.events;

CREATE TABLE IF NOT EXISTS cd.events
(
    "id" bigint NOT NULL,
    "event_date" timestamp without time zone,
    "attribute1" bigint,
    "attribute2" bigint,
    "attribute3" bigint,
    "attribute4" varchar(80),
    "attribute5" varchar(80),
    "attribute6" boolean,
    "metric1" bigint,
    "metric2" numeric(10,5),
    CONSTRAINT events_pkey PRIMARY KEY ("id")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS cd.events
    OWNER to root;

INSERT INTO cd.events ("id", "attribute1", "attribute2","attribute3", "event_date", "metric1", "metric2", "attribute4", "attribute5","attribute6") VALUES
(0,0, 3, 1, '2012-07-03 11:21:00', 2, 0.1, 'test', 'raw', true ),
(1,1, 4, 1, '2012-07-03 08:00:05', 2, 0.1, 'test', 'raw', true ),
(2,2, 6, 0, '2012-07-03 18:32:00', 2, 0.1, 'test', 'raw', true ),
(3,3, 7, 1, '2012-07-03 19:54:00', 2, 0.1, 'test', 'raw', true ),
(4,4, 8, 1, '2012-07-03 10:21:00', 1, 0.1, 'test', 'raw', true ),
(5,5, 8, 1, '2012-07-03 15:11:00', 1, 0.1, 'test', 'raw', true ),
(6,6, 0, 2, '2012-07-04 09:40:00', 3, 0.1, 'test', 'raw', true ),
(7,7, 0, 2, '2012-07-04 15:00:00', 3, 0.1, 'test', 'raw', true ),
(8,8, 4, 3, '2012-07-04 13:30:00', 2, 0.1, 'test', 'raw', true ),
(9,9, 4, 0, '2012-07-04 15:50:00', 2, 0.1, 'test', 'raw', true ),
(10,10, 4, 0, '2012-07-04 17:30:00', 2, 0.1, 'test', 'raw', true );