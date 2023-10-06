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
    file_created text COLLATE pg_catalog."default",
    file_modified text COLLATE pg_catalog."default"
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;



