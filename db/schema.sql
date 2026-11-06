--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA IF NOT EXISTS public;


--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- Name: generate_tracking_number(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.generate_tracking_number(country_code text) RETURNS text
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN country_code || 
           LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0') || '-' ||
           LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0') || '-' ||
           LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0');
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: addresses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.addresses (
    id integer NOT NULL,
    user_id integer,
    address_line character varying(300),
    city character varying(100),
    state character varying(100),
    country character varying(100),
    postal_code character varying(20),
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: addresses_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.addresses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: addresses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.addresses_id_seq OWNED BY public.addresses.id;


--
-- Name: shipments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.shipments (
    id integer NOT NULL,
    tracking_number character varying(50) NOT NULL,
    user_id integer,
    origin_address_id integer,
    destination_address_id integer,
    status character varying(50) NOT NULL,
    weight numeric(10,2),
    created_at timestamp with time zone DEFAULT now(),
    expected_delivery_date date
);


--
-- Name: shipments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.shipments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: shipments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.shipments_id_seq OWNED BY public.shipments.id;


--
-- Name: tracking_updates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tracking_updates (
    id integer NOT NULL,
    shipment_id integer,
    status character varying(100) NOT NULL,
    location_city character varying(100),
    location_details text,
    scanned_at timestamp with time zone DEFAULT now() NOT NULL,
    created_by character varying(100)
);


--
-- Name: tracking_updates_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.tracking_updates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: tracking_updates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.tracking_updates_id_seq OWNED BY public.tracking_updates.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(120) NOT NULL,
    full_name character varying(200),
    phone character varying(30),
    created_at timestamp with time zone DEFAULT now()
);


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: addresses id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.addresses ALTER COLUMN id SET DEFAULT nextval('public.addresses_id_seq'::regclass);


--
-- Name: shipments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shipments ALTER COLUMN id SET DEFAULT nextval('public.shipments_id_seq'::regclass);


--
-- Name: tracking_updates id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracking_updates ALTER COLUMN id SET DEFAULT nextval('public.tracking_updates_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: addresses addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_pkey PRIMARY KEY (id);


--
-- Name: shipments shipments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_pkey PRIMARY KEY (id);


--
-- Name: shipments shipments_tracking_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_tracking_number_key UNIQUE (tracking_number);


--
-- Name: tracking_updates tracking_updates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracking_updates
    ADD CONSTRAINT tracking_updates_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: idx_shipments_tracking; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_shipments_tracking ON public.shipments USING btree (tracking_number);


--
-- Name: idx_shipments_user; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_shipments_user ON public.shipments USING btree (user_id);


--
-- Name: idx_tracking_shipment_scanned; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_tracking_shipment_scanned ON public.tracking_updates USING btree (shipment_id, scanned_at DESC);


--
-- Name: addresses addresses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: shipments shipments_destination_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_destination_address_id_fkey FOREIGN KEY (destination_address_id) REFERENCES public.addresses(id) ON DELETE SET NULL;


--
-- Name: shipments shipments_origin_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_origin_address_id_fkey FOREIGN KEY (origin_address_id) REFERENCES public.addresses(id) ON DELETE SET NULL;


--
-- Name: shipments shipments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.shipments
    ADD CONSTRAINT shipments_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: tracking_updates tracking_updates_shipment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tracking_updates
    ADD CONSTRAINT tracking_updates_shipment_id_fkey FOREIGN KEY (shipment_id) REFERENCES public.shipments(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

