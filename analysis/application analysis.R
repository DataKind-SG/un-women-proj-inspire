# application analysis

library(dplyr)
library(jsonlite)
library(openxlsx)
library(readr)

# ===========================================================================
# Processing
# Expected Column Names :project_year, country_application, country_application_name, 
#                        country_impact, country_impact_name
# ===========================================================================

inspire2011 <- read_csv("../data/cleaned_applications_2011.csv", na=character())
inspire2012 <- read_csv("../data/cleaned_applications_2012.csv", na=character())
inspire2013 <- read_csv("../data/cleaned_applications_2013.csv", na=character())
inspire2014 <- read_csv("../data/cleaned_applications_2014.csv", na=character())
inspire2015 <- read_csv("../data/cleaned_applications_2015.csv", na=character())

inspire <- rbind(inspire2011, inspire2012, inspire2013, inspire2014, inspire2015)

inspire <- inspire %>% 
    filter(is_deleted != 1) %>%
    select(project_year, country_application, country_application_name, country_impact, country_impact_name)

inspire$project_year <- factor(inspire$project_year)

# processes applied countries and impact countries separately
# filters out blank country codes or country names that are blank
inspire_applied_blanks <- inspire %>%
    filter(country_application_name == "" | country_application == "")
write.xlsx(inspire_applied_blanks,file = "../data/filtered_applied_countries.xlsx")

inspire_applied <- inspire %>%
    filter(country_application_name != "" & country_application != "")

inspire_impact_blanks <- inspire %>%
    filter(country_impact_name == "" | country_impact == "")
write.xlsx(inspire_impact_blanks,file = "../data/filtered_impact_countries.xlsx")

inspire_impact <- inspire %>%
    filter(country_impact_name != "" & country_impact != "")



# ===========================================================================
# Analysis
# ===========================================================================

# Name of all countries that applied per year, 2011 - 2015
inspire_country_names_applied <- inspire_applied %>% 
    group_by(project_year) %>% 
    select(country_application_name) %>%
    distinct(country_application_name) %>%
    arrange(country_application_name)
write.xlsx(inspire_country_names_applied, file = "../data/01 application country names per year.xlsx")

# Name of all countries that were impacted per year, 2011 - 2015
inspire_country_names_impacted <- inspire_impact %>% 
    group_by(project_year) %>% 
    select(country_impact_name) %>%
    distinct(country_impact_name) %>%
    arrange(country_impact_name)
write.xlsx(inspire_country_names_impacted, file = "../data/02 impact country names per year.xlsx")

# Number of countries that applied per year, 2011 - 2015
inspire_countries_applied <- inspire_applied %>% 
    group_by(project_year) %>% 
    summarise(count=length(country_application_name))
write.xlsx(inspire_countries_applied, file = "../data/03 application country numbers per year.xlsx")

# Number of countries that were impacted per year, 2011 - 2015
inspire_countries_impact <- inspire_impact %>% 
    group_by(project_year) %>% 
    summarise(count=length(country_impact_name))
write.xlsx(inspire_countries_impact, file = "../data/04 impact country numbers per year.xlsx")


#Application numbers per year for each country, 2011 - 2015
inspire_numbers_applied <- inspire_applied %>% 
    group_by(project_year, country_application_name) %>% 
    summarise(count=length(country_application_name))
write.xlsx(inspire_numbers_applied, file = "../data/05 application country numbers per year per country.xlsx")

#Impact numbers per year for each country, 2011 - 2015
inspire_numbers_impact <- inspire_impact %>% 
    group_by(project_year, country_impact_name) %>% 
    summarise(count=length(country_impact_name))
write.xlsx(inspire_numbers_impact, file = "../data/06 impact country numbers per year per country.xlsx")

# ===========================================================================
# Generate visualization data (JSON)
# Output Fields:
# code - Country Code
# name - Country Name
# z - count
# Output is grouped by year
# ===========================================================================

country_impact_lookup <- inspire_impact %>% 
    select(country_impact,country_impact_name) %>% 
    distinct(country_impact_name) %>%
    arrange(country_impact_name)

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

outfile <- file("../data/impacted.json",encoding="UTF-8")
write(toJSON(output, pretty = TRUE), file=outfile)
close(outfile)