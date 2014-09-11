#--------------------------------
# Name:         nfl_plot_r.R
# Purpose:      Plot the coords saved in the CSV file from Python
# Author:       Andrew Vitale  vitale232@gmail.com
# Created       2014/09/10
# R:            3.1.1
#--------------------------------
library(sp)
library(maps)
library(maptools)

setwd('~/Google Drive/twitter/')

#### Read in the tweets coordinates collected with Tweepy
#### as SpatialPoints
tweets = read.csv('./nfl_coords.csv')
coordinates(tweets) = ~long+lat
proj4string(tweets) = '+proj=longlat +datum=WGS84'

#### Upload the map of the USA from the maps package 
the_map = map("state", fill=TRUE, col="transparent", plot=FALSE)

#### Coerce the map to a SpatialPolgons object
IDs = sapply(strsplit(the_map$names, ":"), function(x) x[1])
the_map_sp = map2SpatialPolygons(the_map, IDs=IDs,
                                 proj4string=CRS("+proj=longlat +datum=WGS84"))

#### Set up a blank raster of the world
r = raster(nrow=720, ncol=1440)

#### create a blank list and loop through each row of tweets, making a raster
#### with value 1 where coordinates reside, and store each raster in the list
l = list()
for(i in 1:length(tweets)){
  p = tweets[i, ]  
  l[[i]] = rasterize(p, r)
}

#### stack the list and crop it to the USA
s = stack(l)
s = crop(s, the_map_sp)

#### Take the sum of the stack, which has value 1 for each
#### cell for a tweet location, thus will count the number
#### of tweets per cell
density = sum(s, na.rm=TRUE)
density[density==0] = NA

#### project the USA map and density raster to albers equal area
the_map_sp = spTransform(the_map_sp, 
                         CRS('+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs '))
density = projectRaster(density, 
                        crs='+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +ellps=GRS80 +datum=NAD83 +units=m +no_defs')

density[which(!is.na(values(density)))] = round(values(density)[-which(is.na(values(density)))], 0)

#### Make a basic map
cols = colorRampPalette(c('blue', 'green', 'yellow', 'orange', 'red'))
plot(the_map_sp, axes=FALSE, col='lightgray', border='black')
plot(density, add=TRUE, col=cols(14))#,
#      main="Tweets tagged '#nfl', 'goodell', 'nflcommish', '#RayRice'",
#      sub='Tweets recorded from 20:30 to 22:45, 2014-09-10')
plot(the_map_sp, add=TRUE, col=NA, border='black')
title("Tweets tagged '#nfl', 'goodell', 'nflcommish', '#RayRice'", cex=1.25)
mtext('Recorded from 20:30 to 22:45 PDT, 2014-09-10', cex=1.25)
