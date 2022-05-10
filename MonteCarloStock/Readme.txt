How to use:

1 - Open GoogleSheets and write the following.

=GOOGLEFINANCE(STOCK TAG,"all", FIRST DATE, FINAL DATE,"DAILY")

	- Where STOCK TAG is the tag that you can get from infoMoney or whatever site do you want.
	- FIRST DATE you HAVE to write exactly like this: DATA(YEAR, MM, DD).
	- FINAL DATE is the same of FIRST DATE but... by the name you can guess.

EX: 
=GOOGLEFINANCE("MGLU3","all",DATA(2019,1,1),DATA(2022,4,20),"DAILY")

2 - Go to File -> Download -> Download as .csv

3 - Rename the file with the name STOCK

4 - Double click on the python file. 