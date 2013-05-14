SELECT s.latitude, s.lonitude, p.genus, p.species, c.abundance 
FROM MCDB_communities c 
JOIN MCDB_sites s, MCDB_species p 
ON c.species_id = p.species_id AND c.site_id = s.site_id
WHERE s.country = "USA" or s.country = "Canada"