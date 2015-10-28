library(leaflet)
library(jsonlite)
library(dplyr)
library(htmlwidgets)

country <- read.csv("data/Country_List_ISO_3166_Codes_Latitude_Longitude.csv")
country_data <- fromJSON("data/impacted.json")

data_2015 <- left_join(country_data$year_2011, country, c("code" = "Alpha.2.code"))

s = 4
n = 4
start.lng <- 103.8
start.lat <- 35
start.zoom <- 3

end.lng <- 159
end.lat <- -8

lng.delta <- (end.lng - start.lng)/n
lat.delta <- (end.lat - start.lat)/n

m <- leaflet(width = floor(s*512), height=floor(s*265)) %>%
  setView(lng=start.lng + l*lng.delta, lat=start.lat + l*lat.delta, zoom=start.zoom+l) %>%
  addProviderTiles("Stamen.Toner") %>%
  addCircleMarkers(
    lng=data_2015$Longitude..average., 
    lat=data_2015$Latitude..average., 
    radius=data_2015$z,
    popup=data_2015$Country)

for (l in 0:n){
  m <- m %>%
    setView(lng=start.lng + l*lng.delta, lat=start.lat + l*lat.delta, zoom=start.zoom+l)
  
  print(paste("shot", l, ".html", sep=""))
  Sys.sleep(1)
  print(m)
  saveWidget(m, paste("shot", l, ".html", sep=""))
}


#