SELECT (s.genus || " " || s.species) as spname, a.m_mass, a.unsexed_mass, a.m_bill, a.unsexed_bill
FROM BBS_species s 
JOIN AvianBodySize_species a 
ON spname = a.species_name 
ORDER BY spname;