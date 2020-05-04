  
DECLARE
    items_count int := 5;
BEGIN 
    for i in 1..items_count LOOP
    
        INSERT INTO locations ( location_id, latitude, longitude)
            values (i+2, '-10,2'+i, '130,123' + i);
      
    end loop;
END;
