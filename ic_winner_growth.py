
import load 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties
fp = FontProperties(fname=r'/mnt/c/Windows/Fonts/YUMIN.TTF', size=10)


def extractData(df,df_dimName,valList):

	first = True

	for val in valList:

		if first:
			ans = df[df[df_dimName] == val]
			first = False
		else:
			tmp_df = df[df[df_dimName] == val]
			ans = pd.concat([ans,tmp_df])
	
	return ans

def calcGradeCnt(df):

	ans = []

	for i,t in df.iterrows():

		if t["date"].month > 4:
			t["grade"] = t["date"].year - t["admYear"] + 1
			t["cnt"] = (t["date"].year - t["admYear"]) * 2 + 1
		else:
			t["grade"] = t["date"].year - t["admYear"]
			t["cnt"] = (t["date"].year - t["admYear"]) * 2

		ans.append(t)

	return pd.DataFrame(ans)

def calcEstimatedRank(df):

	ans = []

	for i,t in df.iterrows():
		if t["rank"] == "NaN":
			t["estimatedRank"] = -1

		else:
			if t["className"] == "ME":
				t["estimatedRank"] = float(t["rank"])
			else:
				t["estimatedRank"] = float(t["rank"]) * 3 + 60

		ans.append(t)

	return pd.DataFrame(ans)

def makeData():
	# メインデータのロード
	df = load.load()
	df = df[["runnerName","date","rank","className"]]
	df.drop_duplicates(inplace=True)

	# IC入賞者の名簿をロード
	target = pd.read_csv("ic_winner.csv")

	# 両データのJOIN
	ic_winner_df = extractData(df,"runnerName",target["runnerName"])
	ic_winner_df = pd.merge(ic_winner_df,target,on=["runnerName"])
	ic_winner_df = calcGradeCnt(ic_winner_df)
	ic_winner_df = calcEstimatedRank(ic_winner_df)

	return ic_winner_df

def makeGraph(df,runnerName):

	tmp_df = df[df["runnerName"] == runnerName].sort_values("cnt")
	
	plt.title(runnerName,fontproperties=fp)
	plt.ylabel("推定順位",fontproperties=fp)
	plt.xlabel("インカレの回数",fontproperties=fp)
	plt.plot(tmp_df["cnt"],tmp_df["estimatedRank"])

	plt.savefig("images/"+runnerName+".png")
	plt.close()

def makeGraphAll(df):

	runnerNameList = df["runnerName"].drop_duplicates()

	for runnerName in runnerNameList:
		makeGraph(df,runnerName)
