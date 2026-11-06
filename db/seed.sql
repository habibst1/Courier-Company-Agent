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
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.users (id, username, email, full_name, phone, created_at) VALUES (2, 'marie_dupont', 'marie.dupont@email.fr', 'Marie Dupont', '+33123456789', '2025-08-22 23:33:38.067136+01');
INSERT INTO public.users (id, username, email, full_name, phone, created_at) VALUES (3, 'carlos_garcia', 'carlos.garcia@email.es', 'Carlos Garcia', '+34123456789', '2025-08-27 23:33:38.067136+01');
INSERT INTO public.users (id, username, email, full_name, phone, created_at) VALUES (4, 'anna_muller', 'anna.muller@email.de', 'Anna Müller', '+49123456789', '2025-09-01 23:33:38.067136+01');
INSERT INTO public.users (id, username, email, full_name, phone, created_at) VALUES (5, 'mohamed_ali', 'mohamed.ali@email.tn', 'Mohamed Ali', '+21698765432', '2025-09-06 23:33:38.067136+01');
INSERT INTO public.users (id, username, email, full_name, phone, created_at) VALUES (6, 'sophie_martin', 'sophie.martin@email.fr', 'Sophie Martin', '+33198765432', '2025-09-08 23:33:38.067136+01');
INSERT INTO public.users (id, username, email, full_name, phone, created_at) VALUES (7, 'juan_rodriguez', 'juan.rodriguez@email.es', 'Juan Rodriguez', '+34987654321', '2025-09-10 23:33:38.067136+01');
INSERT INTO public.users (id, username, email, full_name, phone, created_at) VALUES (8, 'klaus_schmidt', 'klaus.schmidt@email.de', 'Klaus Schmidt', '+49987654321', '2025-09-12 23:33:38.067136+01');
INSERT INTO public.users (id, username, email, full_name, phone, created_at) VALUES (1, 'habib_bencheikhali', 'habib.bencheikh@email.com', 'Habib BEN CHEIKH ALI', '+21624123456', '2025-08-17 23:33:38.067136+01');


--
-- Data for Name: addresses; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.addresses (id, user_id, address_line, city, state, country, postal_code, created_at) VALUES (1, 1, '123 Avenue Habib Bourguiba', 'Tunis', 'Tunis', 'Tunisia', '1000', '2025-08-19 23:33:38.067136+01');
INSERT INTO public.addresses (id, user_id, address_line, city, state, country, postal_code, created_at) VALUES (2, 5, '45 Rue de la Kasbah', 'Sfax', 'Sfax', 'Tunisia', '3000', '2025-09-07 23:33:38.067136+01');
INSERT INTO public.addresses (id, user_id, address_line, city, state, country, postal_code, created_at) VALUES (3, 2, '78 Rue de Rivoli', 'Paris', 'Île-de-France', 'France', '75001', '2025-08-23 23:33:38.067136+01');
INSERT INTO public.addresses (id, user_id, address_line, city, state, country, postal_code, created_at) VALUES (4, 6, '15 Avenue des Champs-Élysées', 'Lyon', 'Auvergne-Rhône-Alpes', 'France', '69001', '2025-09-09 23:33:38.067136+01');
INSERT INTO public.addresses (id, user_id, address_line, city, state, country, postal_code, created_at) VALUES (5, 3, '32 Calle Gran Vía', 'Madrid', 'Madrid', 'Spain', '28013', '2025-08-28 23:33:38.067136+01');
INSERT INTO public.addresses (id, user_id, address_line, city, state, country, postal_code, created_at) VALUES (6, 7, '67 Rambla de Catalunya', 'Barcelona', 'Catalonia', 'Spain', '08007', '2025-09-11 23:33:38.067136+01');
INSERT INTO public.addresses (id, user_id, address_line, city, state, country, postal_code, created_at) VALUES (7, 4, '89 Friedrichstraße', 'Berlin', 'Berlin', 'Germany', '10117', '2025-09-02 23:33:38.067136+01');
INSERT INTO public.addresses (id, user_id, address_line, city, state, country, postal_code, created_at) VALUES (8, 8, '23 Maximilianstraße', 'Munich', 'Bavaria', 'Germany', '80539', '2025-09-13 23:33:38.067136+01');
INSERT INTO public.addresses (id, user_id, address_line, city, state, country, postal_code, created_at) VALUES (15, 1, '89 Avenue Mohamed V', 'Tunis', 'Tunis', 'Tunisia', '1002', '2025-09-02 02:10:40.202751+01');
INSERT INTO public.addresses (id, user_id, address_line, city, state, country, postal_code, created_at) VALUES (16, 1, '156 Rue du Commerce', 'Sousse', 'Sousse', 'Tunisia', '4000', '2025-09-07 02:10:40.202751+01');


--
-- Data for Name: shipments; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (1, 'TN8988-5589-3700', 1, 1, 3, 'delivered', 12.80, '2025-08-20 23:33:38.067136+01', '2025-08-27');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (2, 'TN8125-5390-1487', 1, 1, 4, 'in_transit', 10.45, '2025-08-21 23:33:38.067136+01', '2025-08-28');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (3, 'TN3064-8780-3022', 5, 2, 7, 'delivered', 4.02, '2025-09-08 23:33:38.067136+01', '2025-09-15');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (4, 'TN8079-3568-2125', 5, 2, 8, 'in_transit', 1.88, '2025-09-09 23:33:38.067136+01', '2025-09-16');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (5, 'FR5134-6280-2360', 2, 3, 1, 'in_transit', 19.78, '2025-08-24 23:33:38.067136+01', '2025-08-31');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (6, 'FR7583-4893-1121', 2, 3, 5, 'delivered', 8.59, '2025-08-25 23:33:38.067136+01', '2025-09-01');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (7, 'FR6971-4755-4724', 6, 4, 2, 'delivered', 20.20, '2025-09-10 23:33:38.067136+01', '2025-09-17');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (8, 'FR4324-4726-7412', 6, 4, 6, 'delivered', 14.25, '2025-09-11 23:33:38.067136+01', '2025-09-18');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (9, 'SP4650-3552-6491', 3, 5, 1, 'delivered', 8.76, '2025-08-29 23:33:38.067136+01', '2025-09-05');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (10, 'SP1199-7761-0247', 3, 5, 4, 'delivered', 4.02, '2025-08-30 23:33:38.067136+01', '2025-09-06');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (11, 'SP7269-6934-8956', 7, 6, 3, 'delivered', 16.28, '2025-09-12 23:33:38.067136+01', '2025-09-19');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (12, 'SP9295-2584-2225', 7, 6, 8, 'delivered', 18.32, '2025-09-13 23:33:38.067136+01', '2025-09-20');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (13, 'GR6771-3330-0270', 4, 7, 2, 'delivered', 4.84, '2025-09-03 23:33:38.067136+01', '2025-09-10');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (14, 'GR4639-8437-8151', 4, 7, 5, 'delivered', 13.00, '2025-09-04 23:33:38.067136+01', '2025-09-11');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (15, 'GR7567-5104-8617', 8, 8, 1, 'delivered', 2.72, '2025-09-14 23:33:38.067136+01', '2025-09-21');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (16, 'GR3788-8049-6936', 8, 8, 6, 'delivered', 16.59, '2025-09-15 23:33:38.067136+01', '2025-09-22');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (17, 'TN1921-8225-4511', 1, 1, 7, 'in_transit', 18.45, '2025-08-22 23:33:38.067136+01', '2025-08-29');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (18, 'FR5657-1034-8818', 2, 3, 8, 'out_for_delivery', 8.93, '2025-08-26 23:33:38.067136+01', '2025-09-02');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (19, 'SP0679-8215-5271', 3, 5, 3, 'in_transit', 20.12, '2025-08-31 23:33:38.067136+01', '2025-09-07');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (20, 'GR2368-3017-9191', 4, 7, 6, 'delivered', 1.15, '2025-09-05 23:33:38.067136+01', '2025-09-12');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (66, 'TN4271-9726-9162', 1, 1, 3, 'in_transit', 9.69, '2025-09-03 02:12:30.017595+01', '2025-09-12');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (67, 'TN4208-4747-5634', 1, 1, 4, 'in_transit', 7.56, '2025-09-04 02:12:30.017595+01', '2025-09-11');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (68, 'TN3284-7840-5474', 1, 1, 5, 'delivered', 9.72, '2025-09-05 02:12:30.017595+01', '2025-09-11');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (69, 'TN1991-4500-0442', 1, 1, 6, 'delivered', 11.93, '2025-09-06 02:12:30.017595+01', '2025-09-15');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (70, 'TN7691-1614-6127', 1, 16, 3, 'delivered', 12.91, '2025-09-08 02:12:30.017595+01', '2025-09-16');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (71, 'TN5692-5816-2494', 1, 16, 4, 'delivered', 14.89, '2025-09-09 02:12:30.017595+01', '2025-09-15');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (72, 'TN3991-9128-3002', 1, 16, 5, 'delivered', 3.73, '2025-09-10 02:12:30.017595+01', '2025-09-18');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (73, 'TN7938-8205-0137', 1, 16, 8, 'in_transit', 7.90, '2025-09-11 02:12:30.017595+01', '2025-09-17');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (74, 'TN0790-6076-9024', 1, 1, 3, 'delivered', 1.07, '2025-09-13 02:12:30.017595+01', '2025-09-21');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (75, 'TN4255-8215-9617', 1, 1, 4, 'in_transit', 10.77, '2025-09-14 02:12:30.017595+01', '2025-09-23');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (76, 'TN2663-3034-6284', 1, 16, 5, 'delivered', 1.69, '2025-09-15 02:12:30.017595+01', '2025-09-21');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (77, 'TN6947-4045-3076', 1, 16, 6, 'delivered', 3.21, '2025-09-16 02:12:30.017595+01', '2025-09-21');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (78, 'TN4257-7735-4349', 1, 1, 8, 'delivered', 1.30, '2025-09-16 14:12:30.017595+01', '2025-09-21');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (79, 'TN3140-0290-1314', 1, 16, 7, 'delivered', 12.14, '2025-09-16 20:12:30.017595+01', '2025-09-26');
INSERT INTO public.shipments (id, tracking_number, user_id, origin_address_id, destination_address_id, status, weight, created_at, expected_delivery_date) VALUES (80, 'TN7295-5795-1821', 1, 1, 3, 'delivered', 1.24, '2025-09-17 00:12:30.017595+01', '2025-09-26');


--
-- Data for Name: tracking_updates; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (1, 1, 'processing', 'Tunis', 'Package received at origin facility', '2025-08-21 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (2, 1, 'in_transit', 'Tunis', 'Departed origin facility', '2025-08-21 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (3, 1, 'in_transit', 'Tunis', 'In transit to destination', '2025-08-21 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (4, 1, 'out_for_delivery', 'Paris', 'Arrived at destination facility', '2025-08-23 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (5, 1, 'delivered', 'Paris', 'Package delivered successfully', '2025-08-25 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (6, 2, 'processing', 'Tunis', 'Package received at origin facility', '2025-08-22 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (7, 2, 'in_transit', 'Tunis', 'Departed origin facility', '2025-08-22 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (8, 2, 'in_transit', 'Tunis', 'In transit to destination', '2025-08-22 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (9, 2, 'in_transit', 'Lyon', 'Arrived at destination facility', '2025-08-24 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (10, 2, 'in_transit', 'Lyon', 'Processing at destination facility', '2025-08-25 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (11, 3, 'processing', 'Sfax', 'Package received at origin facility', '2025-09-09 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (12, 3, 'in_transit', 'Sfax', 'Departed origin facility', '2025-09-09 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (13, 3, 'in_transit', 'Berlin', 'In transit to destination', '2025-09-09 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (14, 3, 'out_for_delivery', 'Berlin', 'Arrived at destination facility', '2025-09-11 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (15, 3, 'delivered', 'Berlin', 'Package delivered successfully', '2025-09-13 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (16, 4, 'processing', 'Sfax', 'Package received at origin facility', '2025-09-10 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (17, 4, 'in_transit', 'Sfax', 'Departed origin facility', '2025-09-10 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (18, 4, 'in_transit', 'Sfax', 'In transit to destination', '2025-09-10 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (19, 4, 'in_transit', 'Munich', 'Arrived at destination facility', '2025-09-12 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (20, 4, 'in_transit', 'Munich', 'Processing at destination facility', '2025-09-13 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (21, 5, 'processing', 'Paris', 'Package received at origin facility', '2025-08-25 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (22, 5, 'in_transit', 'Paris', 'Departed origin facility', '2025-08-25 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (23, 5, 'in_transit', 'Tunis', 'In transit to destination', '2025-08-25 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (24, 5, 'in_transit', 'Tunis', 'Arrived at destination facility', '2025-08-27 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (25, 5, 'in_transit', 'Tunis', 'Processing at destination facility', '2025-08-28 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (26, 6, 'processing', 'Paris', 'Package received at origin facility', '2025-08-26 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (27, 6, 'in_transit', 'Paris', 'Departed origin facility', '2025-08-26 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (28, 6, 'in_transit', 'Paris', 'In transit to destination', '2025-08-26 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (29, 6, 'out_for_delivery', 'Madrid', 'Arrived at destination facility', '2025-08-28 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (30, 6, 'delivered', 'Madrid', 'Package delivered successfully', '2025-08-30 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (31, 7, 'processing', 'Lyon', 'Package received at origin facility', '2025-09-11 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (32, 7, 'in_transit', 'Lyon', 'Departed origin facility', '2025-09-11 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (33, 7, 'in_transit', 'Lyon', 'In transit to destination', '2025-09-11 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (34, 7, 'out_for_delivery', 'Sfax', 'Arrived at destination facility', '2025-09-13 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (35, 7, 'delivered', 'Sfax', 'Package delivered successfully', '2025-09-15 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (36, 8, 'processing', 'Lyon', 'Package received at origin facility', '2025-09-12 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (37, 8, 'in_transit', 'Lyon', 'Departed origin facility', '2025-09-12 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (38, 8, 'in_transit', 'Barcelona', 'In transit to destination', '2025-09-12 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (39, 8, 'out_for_delivery', 'Barcelona', 'Arrived at destination facility', '2025-09-14 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (40, 8, 'delivered', 'Barcelona', 'Package delivered successfully', '2025-09-16 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (41, 9, 'processing', 'Madrid', 'Package received at origin facility', '2025-08-30 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (42, 9, 'in_transit', 'Madrid', 'Departed origin facility', '2025-08-30 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (43, 9, 'in_transit', 'Madrid', 'In transit to destination', '2025-08-30 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (44, 9, 'out_for_delivery', 'Tunis', 'Arrived at destination facility', '2025-09-01 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (45, 9, 'delivered', 'Tunis', 'Package delivered successfully', '2025-09-03 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (46, 10, 'processing', 'Madrid', 'Package received at origin facility', '2025-08-31 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (47, 10, 'in_transit', 'Madrid', 'Departed origin facility', '2025-08-31 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (48, 10, 'in_transit', 'Madrid', 'In transit to destination', '2025-08-31 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (49, 10, 'out_for_delivery', 'Lyon', 'Arrived at destination facility', '2025-09-02 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (50, 10, 'delivered', 'Lyon', 'Package delivered successfully', '2025-09-04 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (51, 11, 'processing', 'Barcelona', 'Package received at origin facility', '2025-09-13 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (52, 11, 'in_transit', 'Barcelona', 'Departed origin facility', '2025-09-13 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (53, 11, 'in_transit', 'Paris', 'In transit to destination', '2025-09-13 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (54, 11, 'out_for_delivery', 'Paris', 'Arrived at destination facility', '2025-09-15 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (55, 11, 'delivered', 'Paris', 'Package delivered successfully', '2025-09-17 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (56, 12, 'processing', 'Barcelona', 'Package received at origin facility', '2025-09-14 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (57, 12, 'in_transit', 'Barcelona', 'Departed origin facility', '2025-09-14 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (58, 12, 'in_transit', 'Munich', 'In transit to destination', '2025-09-14 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (59, 12, 'out_for_delivery', 'Munich', 'Arrived at destination facility', '2025-09-16 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (60, 12, 'delivered', 'Munich', 'Package delivered successfully', '2025-09-18 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (61, 13, 'processing', 'Berlin', 'Package received at origin facility', '2025-09-04 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (62, 13, 'in_transit', 'Berlin', 'Departed origin facility', '2025-09-04 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (63, 13, 'in_transit', 'Berlin', 'In transit to destination', '2025-09-04 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (64, 13, 'out_for_delivery', 'Sfax', 'Arrived at destination facility', '2025-09-06 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (65, 13, 'delivered', 'Sfax', 'Package delivered successfully', '2025-09-08 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (66, 14, 'processing', 'Berlin', 'Package received at origin facility', '2025-09-05 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (67, 14, 'in_transit', 'Berlin', 'Departed origin facility', '2025-09-05 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (68, 14, 'in_transit', 'Madrid', 'In transit to destination', '2025-09-05 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (69, 14, 'out_for_delivery', 'Madrid', 'Arrived at destination facility', '2025-09-07 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (70, 14, 'delivered', 'Madrid', 'Package delivered successfully', '2025-09-09 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (71, 15, 'processing', 'Munich', 'Package received at origin facility', '2025-09-15 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (72, 15, 'in_transit', 'Munich', 'Departed origin facility', '2025-09-15 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (73, 15, 'in_transit', 'Munich', 'In transit to destination', '2025-09-15 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (74, 15, 'out_for_delivery', 'Tunis', 'Arrived at destination facility', '2025-09-17 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (75, 15, 'delivered', 'Tunis', 'Package delivered successfully', '2025-09-19 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (76, 16, 'processing', 'Munich', 'Package received at origin facility', '2025-09-16 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (77, 16, 'in_transit', 'Munich', 'Departed origin facility', '2025-09-16 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (78, 16, 'in_transit', 'Munich', 'In transit to destination', '2025-09-16 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (79, 16, 'out_for_delivery', 'Barcelona', 'Arrived at destination facility', '2025-09-18 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (80, 16, 'delivered', 'Barcelona', 'Package delivered successfully', '2025-09-20 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (81, 17, 'processing', 'Tunis', 'Package received at origin facility', '2025-08-23 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (82, 17, 'in_transit', 'Tunis', 'Departed origin facility', '2025-08-23 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (83, 17, 'in_transit', 'Berlin', 'In transit to destination', '2025-08-23 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (84, 17, 'in_transit', 'Berlin', 'Arrived at destination facility', '2025-08-25 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (85, 17, 'in_transit', 'Berlin', 'Processing at destination facility', '2025-08-26 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (86, 18, 'processing', 'Paris', 'Package received at origin facility', '2025-08-27 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (87, 18, 'in_transit', 'Paris', 'Departed origin facility', '2025-08-27 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (88, 18, 'in_transit', 'Munich', 'In transit to destination', '2025-08-27 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (89, 18, 'in_transit', 'Munich', 'Arrived at destination facility', '2025-08-29 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (90, 18, 'out_for_delivery', 'Munich', 'Out for delivery', '2025-08-30 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (91, 19, 'processing', 'Madrid', 'Package received at origin facility', '2025-09-01 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (92, 19, 'in_transit', 'Madrid', 'Departed origin facility', '2025-09-01 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (93, 19, 'in_transit', 'Paris', 'In transit to destination', '2025-09-01 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (94, 19, 'in_transit', 'Paris', 'Arrived at destination facility', '2025-09-03 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (95, 19, 'in_transit', 'Paris', 'Processing at destination facility', '2025-09-04 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (96, 20, 'processing', 'Berlin', 'Package received at origin facility', '2025-09-06 00:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (97, 20, 'in_transit', 'Berlin', 'Departed origin facility', '2025-09-06 05:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (98, 20, 'in_transit', 'Berlin', 'In transit to destination', '2025-09-06 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (99, 20, 'out_for_delivery', 'Barcelona', 'Arrived at destination facility', '2025-09-08 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (100, 20, 'delivered', 'Barcelona', 'Package delivered successfully', '2025-09-10 23:33:38.067136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (101, 2, 'in_transit', 'Madrid', 'Package in transit through regional hub', '2025-08-24 20:43:39.527696+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (102, 4, 'in_transit', 'Paris', 'Package in transit through regional hub', '2025-09-12 18:43:33.908559+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (103, 5, 'in_transit', 'Paris', 'Package in transit through regional hub', '2025-08-27 15:15:58.542169+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (104, 8, 'in_transit', 'Berlin', 'Package in transit through regional hub', '2025-09-14 20:34:01.753985+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (105, 9, 'in_transit', 'Paris', 'Package in transit through regional hub', '2025-08-31 23:51:11.431757+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (106, 11, 'in_transit', 'Berlin', 'Package in transit through regional hub', '2025-09-15 09:02:45.840482+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (107, 12, 'in_transit', 'Paris', 'Package in transit through regional hub', '2025-09-16 07:38:36.099151+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (108, 13, 'in_transit', 'Paris', 'Package in transit through regional hub', '2025-09-06 04:50:00.070661+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (109, 14, 'in_transit', 'Madrid', 'Package in transit through regional hub', '2025-09-07 20:57:31.523046+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (110, 15, 'in_transit', 'Berlin', 'Package in transit through regional hub', '2025-09-17 06:44:50.391742+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (111, 17, 'in_transit', 'Madrid', 'Package in transit through regional hub', '2025-08-25 05:13:55.299152+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (112, 18, 'in_transit', 'Madrid', 'Package in transit through regional hub', '2025-08-29 21:12:45.248136+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (113, 20, 'in_transit', 'Paris', 'Package in transit through regional hub', '2025-09-08 21:20:59.359287+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (114, 80, 'processing', 'Tunis', 'Package received at origin facility', '2025-09-17 00:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (115, 80, 'processing', 'Tunis', 'Package sorted at origin sorting center', '2025-09-17 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (116, 80, 'in_transit', 'Tunis', 'Departed origin facility en route to destination', '2025-09-17 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (117, 80, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-18 00:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (118, 80, 'in_transit', 'Paris', 'Arrived at destination country - clearing customs', '2025-09-19 00:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (119, 80, 'delivered', 'Paris', 'Package delivered successfully to recipient', '2025-09-23 08:51:20.043932+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (120, 79, 'processing', 'Sousse', 'Package received at origin facility', '2025-09-16 20:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (121, 79, 'processing', 'Sousse', 'Package sorted at origin sorting center', '2025-09-16 22:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (122, 79, 'in_transit', 'Sousse', 'Departed origin facility en route to destination', '2025-09-17 00:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (123, 79, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-17 20:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (124, 79, 'in_transit', 'Berlin', 'Arrived at destination country - clearing customs', '2025-09-18 20:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (125, 79, 'delivered', 'Berlin', 'Package delivered successfully to recipient', '2025-09-22 22:18:02.121833+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (126, 78, 'processing', 'Tunis', 'Package received at origin facility', '2025-09-16 14:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (127, 78, 'processing', 'Tunis', 'Package sorted at origin sorting center', '2025-09-16 16:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (128, 78, 'in_transit', 'Tunis', 'Departed origin facility en route to destination', '2025-09-16 18:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (129, 78, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-17 14:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (130, 78, 'in_transit', 'Munich', 'Arrived at destination country - clearing customs', '2025-09-18 14:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (131, 78, 'delivered', 'Munich', 'Package delivered successfully to recipient', '2025-09-20 03:46:21.762217+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (132, 77, 'processing', 'Sousse', 'Package received at origin facility', '2025-09-16 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (133, 77, 'processing', 'Sousse', 'Package sorted at origin sorting center', '2025-09-16 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (134, 77, 'in_transit', 'Sousse', 'Departed origin facility en route to destination', '2025-09-16 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (135, 77, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-17 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (136, 77, 'in_transit', 'Barcelona', 'Arrived at destination country - clearing customs', '2025-09-18 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (137, 77, 'delivered', 'Barcelona', 'Package delivered successfully to recipient', '2025-09-20 06:56:44.606569+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (138, 76, 'processing', 'Sousse', 'Package received at origin facility', '2025-09-15 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (139, 76, 'processing', 'Sousse', 'Package sorted at origin sorting center', '2025-09-15 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (140, 76, 'in_transit', 'Sousse', 'Departed origin facility en route to destination', '2025-09-15 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (141, 76, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-16 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (142, 76, 'in_transit', 'Madrid', 'Arrived at destination country - clearing customs', '2025-09-17 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (143, 76, 'delivered', 'Madrid', 'Package delivered successfully to recipient', '2025-09-19 21:18:18.898278+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (144, 75, 'processing', 'Tunis', 'Package received at origin facility', '2025-09-14 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (145, 75, 'processing', 'Tunis', 'Package sorted at origin sorting center', '2025-09-14 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (146, 75, 'in_transit', 'Tunis', 'Departed origin facility en route to destination', '2025-09-14 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (147, 75, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-15 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (148, 75, 'in_transit', 'Lyon', 'Arrived at destination country - clearing customs', '2025-09-16 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (149, 75, 'in_transit', 'Lyon', 'In transit to final destination facility', '2025-09-15 22:54:57.413595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (150, 74, 'processing', 'Tunis', 'Package received at origin facility', '2025-09-13 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (151, 74, 'processing', 'Tunis', 'Package sorted at origin sorting center', '2025-09-13 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (152, 74, 'in_transit', 'Tunis', 'Departed origin facility en route to destination', '2025-09-13 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (153, 74, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-14 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (154, 74, 'in_transit', 'Paris', 'Arrived at destination country - clearing customs', '2025-09-15 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (155, 74, 'delivered', 'Paris', 'Package delivered successfully to recipient', '2025-09-16 11:50:37.078069+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (156, 73, 'processing', 'Sousse', 'Package received at origin facility', '2025-09-11 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (157, 73, 'processing', 'Sousse', 'Package sorted at origin sorting center', '2025-09-11 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (158, 73, 'in_transit', 'Sousse', 'Departed origin facility en route to destination', '2025-09-11 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (159, 73, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-12 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (160, 73, 'in_transit', 'Munich', 'Arrived at destination country - clearing customs', '2025-09-13 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (161, 73, 'in_transit', 'Munich', 'In transit to final destination facility', '2025-09-12 05:26:32.128991+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (162, 72, 'processing', 'Sousse', 'Package received at origin facility', '2025-09-10 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (163, 72, 'processing', 'Sousse', 'Package sorted at origin sorting center', '2025-09-10 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (164, 72, 'in_transit', 'Sousse', 'Departed origin facility en route to destination', '2025-09-10 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (165, 72, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-11 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (166, 72, 'in_transit', 'Madrid', 'Arrived at destination country - clearing customs', '2025-09-12 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (167, 72, 'delivered', 'Madrid', 'Package delivered successfully to recipient', '2025-09-13 23:45:07.510359+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (168, 71, 'processing', 'Sousse', 'Package received at origin facility', '2025-09-09 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (169, 71, 'processing', 'Sousse', 'Package sorted at origin sorting center', '2025-09-09 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (170, 71, 'in_transit', 'Sousse', 'Departed origin facility en route to destination', '2025-09-09 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (171, 71, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-10 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (172, 71, 'in_transit', 'Lyon', 'Arrived at destination country - clearing customs', '2025-09-11 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (173, 71, 'delivered', 'Lyon', 'Package delivered successfully to recipient', '2025-09-15 23:28:51.370713+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (174, 70, 'processing', 'Sousse', 'Package received at origin facility', '2025-09-08 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (175, 70, 'processing', 'Sousse', 'Package sorted at origin sorting center', '2025-09-08 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (176, 70, 'in_transit', 'Sousse', 'Departed origin facility en route to destination', '2025-09-08 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (177, 70, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-09 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (178, 70, 'in_transit', 'Paris', 'Arrived at destination country - clearing customs', '2025-09-10 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (179, 70, 'delivered', 'Paris', 'Package delivered successfully to recipient', '2025-09-11 12:05:58.158811+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (180, 69, 'processing', 'Tunis', 'Package received at origin facility', '2025-09-06 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (181, 69, 'processing', 'Tunis', 'Package sorted at origin sorting center', '2025-09-06 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (182, 69, 'in_transit', 'Tunis', 'Departed origin facility en route to destination', '2025-09-06 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (183, 69, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-07 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (184, 69, 'in_transit', 'Barcelona', 'Arrived at destination country - clearing customs', '2025-09-08 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (185, 69, 'delivered', 'Barcelona', 'Package delivered successfully to recipient', '2025-09-11 00:17:49.535854+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (186, 68, 'processing', 'Tunis', 'Package received at origin facility', '2025-09-05 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (187, 68, 'processing', 'Tunis', 'Package sorted at origin sorting center', '2025-09-05 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (188, 68, 'in_transit', 'Tunis', 'Departed origin facility en route to destination', '2025-09-05 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (189, 68, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-06 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (190, 68, 'in_transit', 'Madrid', 'Arrived at destination country - clearing customs', '2025-09-07 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (191, 68, 'delivered', 'Madrid', 'Package delivered successfully to recipient', '2025-09-08 02:59:22.312589+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (192, 67, 'processing', 'Tunis', 'Package received at origin facility', '2025-09-04 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (193, 67, 'processing', 'Tunis', 'Package sorted at origin sorting center', '2025-09-04 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (194, 67, 'in_transit', 'Tunis', 'Departed origin facility en route to destination', '2025-09-04 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (195, 67, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-05 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (196, 67, 'in_transit', 'Lyon', 'Arrived at destination country - clearing customs', '2025-09-06 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (197, 67, 'in_transit', 'Lyon', 'In transit to final destination facility', '2025-09-06 08:28:46.721454+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (198, 66, 'processing', 'Tunis', 'Package received at origin facility', '2025-09-03 02:42:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (199, 66, 'processing', 'Tunis', 'Package sorted at origin sorting center', '2025-09-03 04:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (200, 66, 'in_transit', 'Tunis', 'Departed origin facility en route to destination', '2025-09-03 06:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (201, 66, 'in_transit', 'Tunis', 'Processing at international shipping hub', '2025-09-04 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (202, 66, 'in_transit', 'Paris', 'Arrived at destination country - clearing customs', '2025-09-05 02:12:30.017595+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (203, 66, 'in_transit', 'Paris', 'In transit to final destination facility', '2025-09-05 11:45:18.581153+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (204, 66, 'in_transit', 'Sousse', 'Package scanned at regional sorting facility', '2025-09-03 04:02:34.408884+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (205, 67, 'in_transit', 'Sousse', 'In transit through distribution network', '2025-09-06 03:04:47.600184+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (206, 68, 'in_transit', 'Paris', 'Package scanned at regional sorting facility', '2025-09-05 21:09:54.096092+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (207, 69, 'in_transit', 'Paris', 'In transit through distribution network', '2025-09-07 11:43:55.212225+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (208, 70, 'in_transit', 'Tunis', 'In transit through distribution network', '2025-09-10 07:15:56.985783+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (209, 71, 'in_transit', 'Sousse', 'In transit through distribution network', '2025-09-11 20:20:46.776474+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (210, 74, 'in_transit', 'Sousse', 'Package scanned at regional sorting facility', '2025-09-15 21:52:52.54657+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (211, 76, 'in_transit', 'Sousse', 'In transit through distribution network', '2025-09-15 05:25:15.379888+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (212, 77, 'in_transit', 'Sousse', 'In transit through distribution network', '2025-09-16 06:14:22.414276+01', 'system');
INSERT INTO public.tracking_updates (id, shipment_id, status, location_city, location_details, scanned_at, created_by) VALUES (213, 79, 'in_transit', 'Paris', 'Temporarily held at transfer station', '2025-09-18 00:16:19.513536+01', 'system');


--
-- Name: addresses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.addresses_id_seq', 16, true);


--
-- Name: shipments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.shipments_id_seq', 80, true);


--
-- Name: tracking_updates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.tracking_updates_id_seq', 213, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_id_seq', 8, true);


--
-- PostgreSQL database dump complete
--

