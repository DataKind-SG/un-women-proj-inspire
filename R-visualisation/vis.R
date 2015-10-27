library(leaflet)
library(jsonlite)
library(dplyr)

country <- read.csv("data/Country_List_ISO_3166_Codes_Latitude_Longitude.csv")
country_data <- fromJSON("data/impacted.json")

data_2015 <- left_join(country_data$year_2011, country, c("code" = "Alpha.2.code"))
head(data_2015)

m <- leaflet(data) %>%
  addProviderTiles("Stamen.Toner") %>%
  addCircleMarkers(
    lng=data_2015$Longitude..average., 
    lat=data_2015$Latitude..average., 
    radius=data_2015$z,
    popup=data_2015$Country)

plot(m)