BEGIN;
LOCK "{target_schema}"."{target_table}";
CREATE TEMP TABLE "{staging_table}" (LIKE "{target_schema}"."{target_table}");
COPY "{staging_table}" FROM '{s3_file_url}'
WITH CREDENTIALS
'aws_access_key_id={aws_access_key};aws_secret_access_key={aws_secret}'
TIMEFORMAT 'auto'
TRUNCATECOLUMNS
FORMAT AS JSON 'auto';

DELETE FROM "{target_schema}"."{target_table}"
  USING "{staging_table}"
  WHERE "{target_schema}"."{target_table}"."{p_key}" = "{staging_table}"."{p_key}";

INSERT INTO "{target_schema}"."{target_table}"
  SELECT * FROM "{staging_table}";
END;
