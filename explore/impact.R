library(RSQLite)
library(qdap)
library(dplyr)
library(tm)

clean_text <- function(txt){
  res <-
    txt %>%
    tolower() %>%
    scrubber() %>% 
    strip()
}

sqlite <- dbDriver("SQLite")
un_women_db <- dbConnect(sqlite, "Private Data/un_women_data.sqlite")

results <- dbSendQuery(un_women_db, 
                       "select 
                       application_id, 
                       project_location_1, project_location_2, 
                       summary, project_details
                       from un_women;")

raw_un_women <- fetch(results, -1)
dbDisconnect(un_women_db)

un_women <- 
  raw_un_women %>%
  mutate(clean_summary = clean_text(summary),
         clean_project_details = clean_text(project_details))

summary_corpus <-
  Corpus(VectorSource(un_women$clean_summary))

fil_summary_corpus <- tm_map(summary_corpus, removeWords, stopwords("english"))
summary_dtm <- t(as.matrix(DocumentTermMatrix(summary_corpus)))

countries <- read.csv("un-women-proj-inspire/data/ISO_mapping.csv")
head(countries)

words <- row.names(summary_dtm)
target_names <- intersect(words, tolower(countries$Name))

country_mat <- t(summary_dtm[target_names,])

impact_country_map <- as.data.frame(country_mat)
country_code <- 
  countries %>% 
  filter(tolower(Name) %in% target_names)

names(impact_country_map) <- country_code$Code
impact_country_map$application_id <- raw_un_women$application_id

write.csv(impact_country_map, 'impact_country_map.csv', row.names=FALSE)