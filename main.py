import jusipy

################################################################################
# Test the geocode API

gc = jusipy.GIS.Geocode()

queryAddress = 'Morskade 14, 2332GB, leiden'
lat, long    = gc.address(queryAddress)
address      = gc.latlong(lat, long)

print('%s -> %f, %f' % (queryAddress, lat, long))
print('%f, %f -> %s' % (lat, long, address))

################################################################################
# Test the landcover datasets

lc = jusipy.landcover.Glcf_avhrr(resolution='8km')
lc.lookup(lat, long)
