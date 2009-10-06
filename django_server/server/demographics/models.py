# coding=utf-8
from django.db import models

"""
== P1 TOTAL POPULATION
Total population

== P2 URBAN AND RURAL
# Urban population
## Inside urbanized areas
## Inside urban clusters
# Rural population

== P3 RACE[71]
# Population with one race:
## White
## Black
## Native American
## Asian
## Hawaiian/Pacific Islander
## Other
# Population, (mixed) two races:
## White + Black
## White + Native American
## White + Asian
## White + Hawaiian/Pacific Islander
## White + Other
## Black + Native American
## Black + Asian
## Black + Hawaiian/Pacific Islander
## Black + Other
## Native American + Asian
## Native American + Hawaiian/Pacific Islander
## Native American + Other
## Asian + Hawaiian/Pacific Islander
## Asian + Other
## Hawaiian/Pacific Islander + Other
## Popluation, 3 races
## Popluation, 4 races
## Popluation, 5 races
## Popluation, 6 races

== P12 SEX BY AGE
# Male population
## Under 5 years 
## 5 to 9 years 
## 10 to 14 years
## 15 to 17 years
## 18 and 19 years
## 20 years
## 21 years
## 22 to 24 years
## 25 to 29 years
## 30 to 34 years
## 35 to 39 years
## 40 to 44 years
## 45 to 49 years
## 50 to 54 years
## 55 to 59 years
## 60 and 61 years
## 62 to 64 years
## 65 and 66 years
## 67 to 69 years
## 70 to 74 years
## 75 to 79 years
## 80 to 84 years
## 85 years and over
# Female population
## Under 5 years 
## 5 to 9 years 
## 10 to 14 years
## 15 to 17 years
## 18 and 19 years
## 20 years
## 21 years
## 22 to 24 years
## 25 to 29 years
## 30 to 34 years
## 35 to 39 years
## 40 to 44 years
## 45 to 49 years
## 50 to 54 years
## 55 to 59 years
## 60 and 61 years
## 62 to 64 years
## 65 and 66 years
## 67 to 69 years
## 70 to 74 years
## 75 to 79 years
## 80 to 84 years
## 85 years and over

** Should derive "total population" by age from this.

""""