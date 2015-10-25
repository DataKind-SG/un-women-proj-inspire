# application analysis

library(dplyr)
library(jsonlite)
library(openxlsx)

inspire_random <- fromJSON("inspire_data_random.json")
inspire_random_cleaned <- inspire_random[complete.cases(inspire_random),]


# Number of countries that applied per year, 2011 - 2015
inspire_random_cleaned$project_year <- factor(inspire_random_cleaned$project_year)
inspire_random_countries_applied <- inspire_random_cleaned %>% 
    group_by(project_year) %>% 
    summarise(count=length(country_application))
write.xlsx(inspire_random_countries_applied, file = "countries applied per year.xlsx")


#Application numbers per year for each country, 2011 - 2015
inspire_random_numbers_applied <- inspire_random_cleaned %>% 
    group_by(project_year, country_application) %>% 
    summarise(count=length(country_application))
write.xlsx(inspire_random_numbers_applied, file = "application numbers per year per country.xlsx")

for (i in 2011:2015) {
    temp <- inspire_random_numbers_applied %>% 
        filter(project_year == i) %>% 
        select(country_application, count)
    temp$project_year <- NULL
    names(temp) <- c("code", "z")
    assign(paste0("applied",i), temp)
}



output <- list(
    year_2011 = applied2011,
    year_2012 = applied2012,
    year_2013 = applied2013,
    year_2014 = applied2014,
    year_2015 = applied2015
)

write(toJSON(output, pretty = TRUE), "applied.json")