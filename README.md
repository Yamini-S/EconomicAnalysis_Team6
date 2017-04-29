# EconomicAnalysis_Team6

# TimeSeries Forecasting of Indicators from FED Economic Dataset

Steps to run docker
```
docker pull yaminis/finalproject_team6:finalproject
```
```
docker run -it -e "accesskey=<your access key>" -e "secretkey=<your secret key>" -e "bucket=<your bucket name>" yaminis/finalproject_team6:finalproject
```

[Docker Hub link](https://hub.docker.com/r/yaminis/finalproject_team6/)

[Web Application Link For Porject](http://ec2-35-167-175-188.us-west-2.compute.amazonaws.com/)


Folders and the files inside in the repository:
1. Docker_And_LuigiScripts : This Folder contains docker file and luigi scripts
2. Final_WebApp: This forlder contain web application source code.
3. JupyterNotebooks: This folder contains python Jupyter scritps for all the models.
4. PPT: Presentation slides
5. Report: Project complete report
6. Tableau: Exploratory data analysis dashboards in Tableau

[Tableau Link](https://public.tableau.com/shared/4QFCMBDBT?:display_count=yes)


# References:
*	https://www.richmondfed.org/research/regional_economy/reports/regional_profiles#tab-2
*	https://cran.r-project.org/web/packages/dtwclust/vignettes/dtwclust.pdf
*	http://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/
*	https://stats.stackexchange.com/questions/191851/var-forecasting-methodology
*	http://statsmodels.sourceforge.net/devel/vector_ar.html#granger-causalit
* https://www.otexts.org/fpp/9/2


