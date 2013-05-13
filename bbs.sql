SELECT r.lati, r.loni, s.genus, s.species, SUM(c.SpeciesTotal)
FROM BBS_counts c
JOIN BBS_routes r, BBS_species s
ON (c.countrynum = r.countrynum and c.statenum = r.statenum
    and c.Route = r.Route)
AND (s.Aou = c.Aou)
WHERE c.year >= 2006 and c.year <= 2010
GROUP BY r.lati, r.loni, s.genus, s.species
