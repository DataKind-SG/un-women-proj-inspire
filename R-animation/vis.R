library(leaflet)
library(jsonlite)
library(dplyr)
library(htmlwidgets)

country <- read.csv("data/Country_List_ISO_3166_Codes_Latitude_Longitude.csv")
country_data <- fromJSON("data/impacted.json")

data_2015 <- left_join(country_data$year_2015, country, c("code" = "Alpha.2.code"))

s = 4
n = 10
start.lng <- 103.8
start.lat <- 35
start.zoom <- 3

end.lng <- 133 #159
end.lat <- -27 #-8
end.zoom <- 5

lng.delta <- (end.lng - start.lng)/n
lat.delta <- (end.lat - start.lat)/n
zoom.delta <- (end.zoom - start.zoom)/n

m <- leaflet(width = floor(s*512), height=floor(s*265)) %>%
  setView(lng=start.lng, lat=start.lat, zoom=start.zoom) %>%
  addProviderTiles("Stamen.Toner") %>%
  addCircleMarkers(
    lng=data_2015$Longitude..average., 
    lat=data_2015$Latitude..average., 
    radius=data_2015$z,
    popup=data_2015$Country)

print(m)
for (l in 0:n){
  m <- m %>%
    setView(lng=start.lng + l*lng.delta, lat=start.lat + l*lat.delta, zoom=floor(start.zoom+l*zoom.delta))
  
  Sys.sleep(1)
  print(m)
  saveWidget(m, sprintf("shot%03d.html", l))
}