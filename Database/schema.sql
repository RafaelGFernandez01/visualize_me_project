-- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
-- Link to schema: https://app.quickdatabasediagrams.com/#/d/ykOc4O
-- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

-- Modify this code to update the DB schema diagram.
-- To reset the sample schema, replace everything with
-- two dots ('..' - without quotes).

CREATE TABLE "transaction" (
    "dua" text   NOT NULL,
    "date" date   NOT NULL,
    "bl" int   NOT NULL,
    "country_of_origin" text   NOT NULL,
    "acquisition_country" text   NOT NULL,
    "loading_port" text   NOT NULL,
    "via" text   NOT NULL,
    "transport_agent" text   NOT NULL,
    "custom_agent" text   NOT NULL,
    "custom" text   NOT NULL,
    "gross_Kg" int   NOT NULL,
    "net_Kg" int   NOT NULL,
    "usd_fob_total" real   NOT NULL,
    "usd_freight_total" real   NOT NULL,
    "usd_cfr_total" real   NOT NULL,
    "usd_cif_total" real   NOT NULL,
    "usd_fob_unit" real   NOT NULL,
    "usd_cif_unit" real   NOT NULL,
    "exporter" text   NOT NULL,
    "hts_code" int   NOT NULL,
    "importer" int   NOT NULL,
    CONSTRAINT "pk_transaction" PRIMARY KEY (
        "dua"
     )
);

CREATE TABLE "product" (
    "hts_code" int   NOT NULL,
    "hts_code_description" text   NOT NULL,
    "comercial_description" text   NOT NULL,
    "description" text   NOT NULL,
    "description1" text   NOT NULL,
    "description2" text   NOT NULL,
    "description3" text   NOT NULL,
    "description4" text   NOT NULL,
    "description5" text   NOT NULL,
    CONSTRAINT "pk_product" PRIMARY KEY (
        "hts_code"
     )
);

CREATE TABLE "importer" (
    "tax_id" int   NOT NULL,
    "name" text   NOT NULL,
    CONSTRAINT "pk_importer" PRIMARY KEY (
        "tax_id"
     )
);

CREATE TABLE "ports" (
    "port_name" text   NOT NULL,
    "latitude" int   NOT NULL,
    "longitude" int   NOT NULL,
    "country" text   NOT NULL,
    CONSTRAINT "pk_ports" PRIMARY KEY (
        "port_name"
     )
);

ALTER TABLE "transaction" ADD CONSTRAINT "fk_transaction_loading_port" FOREIGN KEY("loading_port")
REFERENCES "ports" ("port_name");

ALTER TABLE "transaction" ADD CONSTRAINT "fk_transaction_hts_code" FOREIGN KEY("hts_code")
REFERENCES "product" ("hts_code");

ALTER TABLE "transaction" ADD CONSTRAINT "fk_transaction_importer" FOREIGN KEY("importer")
REFERENCES "importer" ("tax_id");

