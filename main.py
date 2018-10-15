from geocode import Geocode

gc = Geocode()

queryAddress = 'Morskade 14, 2332GB, leiden'
lat, long    = gc.address(queryAddress)
address      = gc.latlong(lat, long)

print('%s -> %f, %f' % (queryAddress, lat, long))
print('%f, %f -> %s' % (lat, long, address))
