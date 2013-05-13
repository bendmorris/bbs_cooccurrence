SELECT (s.genus || " " || s.species) as spname, 
IFNULL(a.m_mass, a.unsexed_mass), 
IFNULL(a.m_bill, a.unsexed_bill)
FROM BBS_species s 
JOIN AvianBodySize_species a 
ON spname = a.species_name 
ORDER BY spname;