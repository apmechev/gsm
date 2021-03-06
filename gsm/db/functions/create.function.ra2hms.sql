--DROP FUNCTION IF EXISTS ra2hms;

/**
 * This function converts ra from degrees into HHMMSS format.
 * The input format must be DOUBLE:
 */
CREATE FUNCTION ra2hms(iraDEG DOUBLE) RETURNS VARCHAR(12)

BEGIN

  DECLARE raHHnum, raMMnum, raSSnum DOUBLE;
  DECLARE raHHstr, raMMstr VARCHAR(2); 
  DECLARE raSSstr VARCHAR(6);
  
  SET raHHnum = "truncate"(iraDEG / 15, 2);
  SET raMMnum = "truncate"((iraDEG / 15 - raHHnum) * 60, 2);
  SET raSSnum = ROUND((((iraDEG / 15 - raHHnum) * 60) - raMMnum) * 60, 3);
  
  IF raHHnum < 10 THEN
    SET raHHstr = CONCAT('0', raHHnum);
  ELSE 
    SET raHHstr = CAST(raHHnum AS VARCHAR(2));  
  END IF;

  IF raMMnum < 10 THEN
    SET raMMstr = CONCAT('0', raMMnum);
  ELSE 
    SET raMMstr = CAST(raMMnum AS VARCHAR(2));  
  END IF;

  IF raSSnum < 10 THEN
    SET raSSstr = CAST(CONCAT('0', "truncate"(raSSnum, 5)) AS VARCHAR(6));
  ELSE 
    SET raSSstr = CAST("truncate"(raSSnum,6) AS VARCHAR(6));  
  END IF;

  RETURN CONCAT(raHHstr, CONCAT(':', CONCAT(raMMstr, CONCAT(':', raSSstr))));

END;

