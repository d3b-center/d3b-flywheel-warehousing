CREATE TABLE IF NOT EXISTS fw_cloud.flywheel_report_export
(
    subject_label text COLLATE pg_catalog."default",
    subject_id text COLLATE pg_catalog."default",
    session_label text COLLATE pg_catalog."default",
    session_id text COLLATE pg_catalog."default",
    acquisition_label text COLLATE pg_catalog."default",
    acquisition_id text COLLATE pg_catalog."default",
    project_label text COLLATE pg_catalog."default",
    project_id text COLLATE pg_catalog."default",
    file_name text COLLATE pg_catalog."default",
    file_size bigint,
    file_modality text COLLATE pg_catalog."default",
    file_info_magnetic_field_strength double precision,
    file_classification_intent text COLLATE pg_catalog."default",
    file_classification_features text COLLATE pg_catalog."default",
    file_classification_measurement text COLLATE pg_catalog."default",
    file_info_dim1 double precision,
    file_info_dim2 double precision,
    file_info_spacing_between_slices double precision,
    file_info_manufacturer text COLLATE pg_catalog."default",
    file_info_manufacturers_model_name text COLLATE pg_catalog."default",
    file_info_software_versions varchar ,
    file_created text COLLATE pg_catalog."default",
    file_modified text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;



