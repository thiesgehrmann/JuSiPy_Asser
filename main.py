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
import jusipy

lat, long = (52.151816, 4.481109)

# Test GLCF
glcf = jusipy.landcover.Glcf_avhrr(resolution='1km')
print(glcf.lookup(lat, long, pixel_window=5))
glcf.draw(lat, long).show()

# Test USGS
usgs = jusipy.landcover.USGS('GFSAD1KCD')
usgs.draw(lat, long).figure.show()
