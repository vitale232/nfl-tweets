#--------------------------------
# Name:         steelers-ravens_plots.R
# Purpose:      Plot the coords saved in the CSV file from Python
# Author:       Andrew Vitale  vitale232@gmail.com
# Created       2014/09/12
# R:            3.1.1
#--------------------------------

library(raster)
library(rgdal)
library(maps)
library(maptools)

setwd('~/Google Drive/twitter/Week-2/Steelers-Ravens/')

#### Load in the steelers and ravens tweets and make SpatialPoints
steelers = read.csv('steelers_coords.csv')
coordinates(steelers) = ~long+lat
proj4string(steelers) = '+proj=longlat +datum=WGS84'

ravens = read.csv('ravens_coords.csv')
coordinates(ravens) = ~long+lat
proj4string(ravens) = '+proj=longlat +datum=WGS84'

#### Upload the map of the USA from the maps package 
the_map = map("state", fill=TRUE, col="transparent", plot=FALSE)

#### Coerce the map to a SpatialPolgons object
IDs = sapply(strsplit(the_map$names, ":"), function(x) x[1])
the_map_sp = map2SpatialPolygons(the_map, IDs=IDs,
                                 proj4string=CRS("+proj=longlat +datum=WGS84"))

#### Initialize a global raster with specified number of cells
r = raster(nrow=1080, ncol=2160)

#### Rasterize the tweets using the global raster and function 'count'
#### which produces a raster with the cell value == number of tweets within the cell
steelers_count = rasterize(steelers, r, fun='count')
ravens_count = rasterize(ravens, r, fun='count')

#### Not a lot out of the USA, so let's crop it to focus in
steelers_count = crop(steelers_count, the_map_sp)
ravens_count = crop(ravens_count, the_map_sp)

#### Reproject to albers equal area to prettify the maps
#### use nearest neighbor since these are count data and not continuous
aea = '+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs'
the_map_sp = spTransform(the_map_sp, CRS(aea))
steelers_count = projectRaster(steelers_count, crs=aea, method='ngb')
ravens_count = projectRaster(ravens_count, crs=aea, method='ngb')

#### Set up the color ramps
steelers_cols = colorRampPalette(c('black', 'yellow'))
ravens_cols  = colorRampPalette(c('darkorchid4', 'white'))

#### plot the steelers map to disk as a PNG file
png('./steelers_map.png', width=10, height=7, units='in', res=300)
# x11(height=7, width=10)
par(mar=c(5, 0, 4, 2) + 0.1)
plot(the_map_sp, axes=FALSE, col='azure2', border='black')
plot(steelers_count, add=TRUE, col=steelers_cols(255))
plot(the_map_sp, add=TRUE, col=NA, border='black')
title("Tweets Returned for Search of 'Steelers'", cex=1.25)
mtext('Recorded from 15:12 2014-09-11 to 03:12 PDT 2014-09-12', cex=1.25)
dev.off()

#### Plot the ravens map to disk as a PNG file
png('./ravens_map.png', width=10, height=7, units='in', res=300)
# x11(height=7, width=10)
par(mar=c(5, 0, 4, 2) + 0.1)
plot(the_map_sp, axes=FALSE, col='azure2', border='black')
plot(ravens_count, add=TRUE, col=ravens_cols(255))
plot(the_map_sp, add=TRUE, col=NA, border='black')
title("Tweets Returned for Search of 'Ravens'", cex=1.25)
mtext('Recorded from 15:12 2014-09-11 to 03:12 PDT 2014-09-12', cex=1.25)
dev.off()


#### plot both to disk as PNG for reddit
png('./both_maps.png', width=9, height=11, units='in', res=350)
# x11(height=11, width=9)
par(mar=c(0, 0, 4, 1) + 0.1, mfrow=c(2,1))
plot(the_map_sp, axes=FALSE, col='azure2', border='black')
plot(steelers_count, add=TRUE, col=steelers_cols(255))
plot(the_map_sp, add=TRUE, col=NA, border='black')
title("Number of Tweets Returned for Search of 'Steelers'", cex=1.25)
mtext('Recorded from 15:12 2014-09-11 to 03:12 PDT 2014-09-12', cex=1.25)

plot(the_map_sp, axes=FALSE, col='azure2', border='black')
plot(ravens_count, add=TRUE, col=ravens_cols(255))
plot(the_map_sp, add=TRUE, col=NA, border='black')
title("Number of Tweets Returned for Search of 'Ravens'", cex=1.25)
mtext('Recorded from 15:12 2014-09-11 to 03:12 PDT 2014-09-12', cex=1.25)
dev.off()
