# application analysis

library(dplyr)
library(jsonlite)
library(openxlsx)

# ===========================================================================
# Processing
# Expected Column Names :project_year, country_application, country_application_name, 
#                        country_impact, country_impact_name
# ===========================================================================

inspire2011 <- fromJSON("cleaned_applications_2011.json")
inspire2012 <- fromJSON("cleaned_applications_2012.json")
inspire2013 <- fromJSON("cleaned_applications_2013.json")
inspire2014 <- fromJSON("cleaned_applications_2014.json")
inspire2015 <- fromJSON("cleaned_applications_2015.json")

inspire <- rbind(inspire2011, inspire2012, inspire2013, inspire2014, inspire2015)

inspire_cleaned <- inspire %>% 
    select(project_year, country_application, country_application_name, country_impact, country_impact_name) %>%
    filter(country_application != "")

inspire_cleaned$project_year <- factor(inspire_cleaned$project_year)

# ===========================================================================
# Analysis
# ===========================================================================

# Name of all countries that applied per year, 2011 - 2015
inspire_country_names_applied <- inspire_cleaned %>% 
    group_by(project_year) %>% 
    select(country_application_name) %>%
    unique()
write.xlsx(inspire_country_names_applied, file = "01 application country names per year.xlsx")

# Name of all countries that were impacted per year, 2011 - 2015
inspire_country_names_impacted <- inspire_cleaned %>% 
    group_by(project_year) %>% 
    select(country_impact_name) %>%
    unique()
write.xlsx(inspire_country_names_impacted, file = "02 impact country names per year.xlsx")

# Number of countries that applied per year, 2011 - 2015
inspire_countries_applied <- inspire_cleaned %>% 
    group_by(project_year) %>% 
    summarise(count=length(country_application_name))
write.xlsx(inspire_countries_applied, file = "03 application country numbers per year.xlsx")

# Number of countries that were impacted per year, 2011 - 2015
inspire_countries_impact <- inspire_cleaned %>% 
    group_by(project_year) %>% 
    summarise(count=length(country_impact_name))
write.xlsx(inspire_countries_impact, file = "04 impact country numbers per year.xlsx")


#Application numbers per year for each country, 2011 - 2015
inspire_numbers_applied <- inspire_cleaned %>% 
    group_by(project_year, country_application_name) %>% 
    summarise(count=length(country_application_name))
write.xlsx(inspire_numbers_applied, file = "05 application country numbers per year per country.xlsx")

#Impact numbers per year for each country, 2011 - 2015
inspire_numbers_impact <- inspire_cleaned %>% 
    group_by(project_year, country_impact_name) %>% 
    summarise(count=length(country_impact_name))
write.xlsx(inspire_numbers_impact, file = "06 impact country numbers per year per country.xlsx")

# ===========================================================================
# Generate visualization data (JSON)
# Output Fields:
# code - Country Code
# name - Country Name
# z - count
# Output is grouped by year
# ===========================================================================

country_impact_lookup <- inspire_cleaned %>% select(country_impact,country_impact_name) %>% unique()

inspire_numbers_impact_merged <- left_join(inspire_numbers_impact, country_impact_lookup, by = "country_impact_name")

for (i in 2011:2015) {
    temp <- inspire_numbers_impact_merged %>%
        filter(project_year == i) %>% 
        select(country_impact, country_impact_name, count)
    temp$project_year <- NULL
    names(temp) <- c("code","name", "z")
    assign(paste0("impacted",i), temp)
}



output <- list(
    year_2011 = impacted2011,
    year_2012 = impacted2012,
    year_2013 = impacted2013,
    year_2014 = impacted2014,
    year_2015 = impacted2015
)

write(toJSON(output, pretty = TRUE), "impacted.json")