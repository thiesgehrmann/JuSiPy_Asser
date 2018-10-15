import GIS
import landcover

################################################################################
# Test the geocode API

gc = GIS.Geocode()

queryAddress = 'Morskade 14, 2332GB, leiden'
lat, long    = gc.address(queryAddress)
address      = gc.latlong(lat, long)

print('%s -> %f, %f' % (queryAddress, lat, long))
print('%f, %f -> %s' % (lat, long, address))

################################################################################
# Test the landcover datasets

lc = landcover.Glcf_avhrr(resolution='8km')
lc.lookup(lat, long)
