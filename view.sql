CREATE OR REPLACE VIEW fire_params_locations AS
    SELECT
        fire_info.fire_id,
        locations.latitude,
        locations.longitude,
        locations.location_id,
        params.brightness,
        params.params_id,
        confidence.confidence
    FROM
        fire_info
        INNER JOIN locations ON fire_info.location_id = locations.location_id
        INNER JOIN confidence ON fire_info.confidence = confidence.confidence
        inner join params on fire_info.params_id = params.params_id;
        
  
