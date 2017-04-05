library(readr)
library(dplyr)
library(ggplot2)

event.listeners <- read_csv("data-firstInteractive-EventListeners.csv") %>%
  mutate(measurement = "EventListeners")

proportional.and.lonely <- read_csv("data-firstInteractive-FMP-Proportional-w15-3000-lonely-ws-250-padding-1000psb-5000.csv") %>%
  mutate(measurement = "ProportionalAndLonely")

proportional <- read_csv("data-firstInteractive-FMP-Proportional-w15-3000.csv") %>%
  mutate(measurement = "Proportional")

forward.search <- read_csv("data-firstInteractive-FMP.csv") %>%
  mutate(measurement = "ForwardSearch")

lighthouse <- read_csv("data-firstInteractive-Lighthouse.csv") %>%
  mutate(measurement = "Lighthouse")

lonely <- read_csv("data-firstInteractiveNetRevLonelyWindow.csv") %>%
  mutate(measurement = "Lonely")

df <- rbind(event.listeners, proportional.and.lonely, proportional, forward.search, lighthouse, lonely) %>%
  mutate(measurement = as.factor(measurement),
         verdict = as.factor(verdict),
         sitename = as.factor(sitename))

ggplot(data = df, aes(x=sitename, y=metric_value)) +
  geom_errorbar(color="black", aes(ymin=reasonable_start, ymax=reasonable_end)) +
  geom_point(size=1, color="red") + 
  facet_wrap(~measurement)

ggplot(data = df, aes(x=sitename, y=metric_value, color=verdict)) +
  geom_errorbar(color="black", aes(ymin=reasonable_start, ymax=reasonable_end)) +
  geom_point(size=1) + 
  facet_wrap(~measurement)

ggplot(data = df, aes(x=sitename, y=metric_value, color=measurement)) +
  geom_errorbar(color="black", aes(ymin=reasonable_start, ymax=reasonable_end)) +
  geom_jitter(size=1, height=0)