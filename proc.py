import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import pandas as pd
datapath = "./datapar2/"
resultpath = "./resultpar2/"
testlist = np.linspace(100,2000,20)
def plotone(data_test, index):
    # sns.set(style="whitegrid")
    # plt.figure(figsize=(10,6))
    
    # sns.histplot(data=data,x="time_before_send", label = "time_before_send", binwidth=2, color="blue")
    # sns.histplot(data=data,x="time_before_comp", label = "time_before_comp", binwidth=2, color = "red")
    # sns.histplot(data=data,x="time_after_comp", label = "time_after_comp", binwidth=2, color="green")
    # sns.histplot(data=data,x="period", label = "client_check_period", binwidth=2, color = "orange")
    # sns.histplot(data=data,x="time_client_check", label = "time_client_check", binwidth=4, color = "pink")
    # plt.xlim((min(min(data["time_after_comp"]),-100),max(max(max(data["time_after_comp"]),500),max(data["period"]))))
    # plt.ylim((0,datac.shape[0]))
    # plt.tight_layout()
    # plt.xlabel("time (us)")
    # plt.ylabel("sample count")
    # plt.legend()
    # plt.savefig("./result/time_test%d_s%dc%d.png"%(test,server,client),dpi=200)
    sns.set(style="whitegrid")
    plt.figure(figsize=(12,10))
    for i,data in enumerate(data_test):
        plt.subplot(4,2,2*i+1)

        sns.histplot(data=data,x="time_encode", label = "time_encode (T1-T0)", binwidth=1, color="blue")
        sns.histplot(data=data,x="time_send", label = "time_send (T2-T1)", binwidth=1, color = "red")
        sns.histplot(data=data,x="time_comp", label = "time_comp (T3-T2)", binwidth=1, color="green")
        plt.xlim(0,100)
        plt.ylim((0,data["time_comp"].shape[0]+1))
        plt.tight_layout()
        plt.xlabel("time (us)")
        plt.ylabel("sample count")
        plt.legend()
        plt.title("server=%d, client=%d"%(i//2, i%2))
        plt.subplot(4,2,2*i+2)
        sns.histplot(data=data,x="time_check", label = "time_check (T4-T2)", color = "pink")
        plt.ylim((0,data["time_comp"].shape[0]+1))
        plt.xlabel("time (us)")
        plt.ylabel("sample count")
        plt.legend()

    # plt.show()
    plt.savefig(resultpath+"seg_test_%d.png"%(index),dpi=200)
    
    return 


if __name__ == "__main__":
    data = []
    for test in range(1,21):
        data_test = []
        for server in range(2):
            for client in range(2):
                filenamec = datapath+"test%d_c_s%dc%d.txt"%(test,server,client)
                filenames = datapath+"test%d_s_s%dc%d.txt"%(test,server,client)
                with open(filenamec) as file:
                    datac = np.array([[int(string) for string in line] for line in list(csv.reader(file))])
                with open(filenames) as file:
                    datas = np.array([[int(string) for string in line] for line in list(csv.reader(file))])
                assert(datac.shape[0] == datas.shape[0])
                period = np.zeros((datac.shape[0], 1))
                period[:,0] = datac[:,3]
                period[period[:,0]==0] = np.average(period[period[:,0]!=0])
                data_test.append(pd.DataFrame({
                    "sequence": datas[1:,0],
                    "time_before_send": datas[1:,2],
                    "time_before_comp": datas[1:,3],
                    "time_after_comp": datas[1:,4],
                    "time_client_check": datac[1:,2],
                    "time_encode": datas[1:,2],
                    "time_send": datas[1:,3] - datas[1:,2],
                    "time_comp": datas[1:,4] - datas[1:,3],
                    "time_check": datac[1:,2] - datas[1:,3],
                    "period": period[1:,0]
                }))
        data.append(data_test)
    stat = pd.DataFrame({
        "b00": [np.average(data[test][0]["time_check"]) for test in range(len(testlist))],
        "b01": [np.average(data[test][1]["time_check"]) for test in range(len(testlist))],
        "b10": [np.average(data[test][2]["time_check"]) for test in range(len(testlist))],
        "b11": [np.average(data[test][3]["time_check"]) for test in range(len(testlist))],
        "send_avg00": [np.average(data[test][0]["time_send"]) for test in range(len(testlist))],
        "send_avg01": [np.average(data[test][1]["time_send"]) for test in range(len(testlist))],
        "send_avg10": [np.average(data[test][2]["time_send"]) for test in range(len(testlist))],
        "send_avg11": [np.average(data[test][3]["time_send"]) for test in range(len(testlist))],
        "comp_avg00": [np.average(data[test][0]["time_comp"]) for test in range(len(testlist))],
        "comp_avg01": [np.average(data[test][1]["time_comp"]) for test in range(len(testlist))],
        "comp_avg10": [np.average(data[test][2]["time_comp"]) for test in range(len(testlist))],
        "comp_avg11": [np.average(data[test][3]["time_comp"]) for test in range(len(testlist))],
        "Tc": testlist,
        "b00+b11": [np.average(data[test][0]["time_check"]) + np.average(data[test][3]["time_check"]) for test in range(len(testlist))],
        "b00-b11": [np.average(data[test][0]["time_check"]) - np.average(data[test][3]["time_check"]) for test in range(len(testlist))],
        "delta": [(np.average(data[test][1]["time_check"]) - np.average(data[test][2]["time_check"]))/2 for test in range(len(testlist))],
        "l01byb": [(np.average(data[test][1]["time_check"]) + np.average(data[test][2]["time_check"]) - np.average(data[test][0]["time_check"]) - np.average(data[test][3]["time_check"]))/2 for test in range(len(testlist))],
        "l01byf": [
            (-np.average(data[test][0]["time_send"])
            +np.average(data[test][1]["time_send"])
            +np.average(data[test][2]["time_send"])
            -np.average(data[test][3]["time_send"])
            -np.average(data[test][0]["time_comp"])
            +np.average(data[test][1]["time_comp"])
            +np.average(data[test][2]["time_comp"])
            -np.average(data[test][3]["time_comp"]))/4 for test in range(len(testlist))],
        # "check_std00": [np.std(data[test][0]["time_check"],ddof=1) for test in range(len(testlist))],
        # "check_std01": [np.std(data[test][1]["time_check"],ddof=1) for test in range(len(testlist))],
        # "check_std10": [np.std(data[test][2]["time_check"],ddof=1) for test in range(len(testlist))],
        # "check_std11": [np.std(data[test][3]["time_check"],ddof=1) for test in range(len(testlist))],
    })
    ## data[i][j]
    ## 00, 01, 10, 11

    sns.set(style="whitegrid")
    plt.figure(figsize=(8,8))
    sns.scatterplot(data=stat,x="Tc", y="b00+b11", label="experimental",color="red")
    plt.xlabel("Tc (us)")
    plt.ylabel("b00+b11 (us)")

    coeff = np.polyfit(stat["Tc"],stat["b00+b11"],deg=1)
    plt.plot(np.linspace(0,2500,2501),np.poly1d(coeff)(np.linspace(0,2500,2501)),color="blue",label="y=%.4fx%+.4f"%(coeff[0],coeff[1]))
    plt.legend()
    plt.axis("equal")
    plt.xlim((0,2500))
    plt.ylim((0,2500))
    print(coeff)
    print(np.corrcoef(stat["Tc"],stat["b00+b11"]))
    # plt.show()
    plt.savefig(resultpath+"stat_1.png",dpi=200)

    sns.set(style="whitegrid")
    plt.figure(figsize=(8,8))
    sns.scatterplot(data=stat,x="Tc", y="b00-b11", label="experimental",color="red")
    plt.xlabel("Tc (us)")
    plt.ylabel("b00-b11 (us)")
    coeff2 = np.polyfit(stat["Tc"],stat["b00-b11"],deg=1)
    plt.plot(np.linspace(0,2500,2501),np.poly1d(coeff2)(np.linspace(0,2500,2501)),color="blue",label="y=%.4fx%+.4f"%(coeff2[0],coeff2[1]))
    plt.legend()
    # plt.axis("equal")
    plt.xlim((0,2500))
    plt.ylim((-200,200))
    print(coeff)
    print(np.corrcoef(stat["Tc"],stat["b00-b11"]))
    # plt.show()
    plt.savefig(resultpath+"stat_2.png",dpi=200)

    sns.set(style="whitegrid")
    plt.figure(figsize=(8,8))
    sns.scatterplot(data=stat,x="Tc", y="delta", label="experimental",color="red")
    plt.xlabel("Tc (us)")
    plt.ylabel("1/2(b01-b10) (us)")

    # coeff2 = np.polyfit(stat["Tc"],stat["b00-b11"],deg=1)
    # plt.plot(np.linspace(0,2500,2501),np.poly1d(coeff2)(np.linspace(0,2500,2501)),color="blue",label="y=%.4fx%+.4f"%(coeff2[0],coeff2[1]))
    # plt.legend()
    # plt.axis("equal")
    plt.xlim((0,2500))
    # print(coeff)
    # print(np.corrcoef(stat["Tc"],stat["b00-b11"]))
    # plt.show()
    plt.savefig(resultpath+"stat_3.png",dpi=200)
    sns.set(style="whitegrid")
    plt.figure(figsize=(8,8))
    sns.scatterplot(data=stat, x="Tc", y="l01byb", label="calculated by b",color="red")
    sns.scatterplot(data=stat, x="Tc", y="l01byf", label="calculated by f",color="green")
    plt.xlabel("Tc (us)")
    plt.ylabel("l01-(l00+l11)/2 (us)")
    coeff4 = np.polyfit(stat["Tc"],stat["l01byb"],deg=1)
    plt.plot(np.linspace(0,2500,2501),np.poly1d(coeff4)(np.linspace(0,2500,2501)),color="purple",label="b: y=%.4fx%+.4f"%(coeff4[0],coeff4[1]))
    coeff5 = np.polyfit(stat["Tc"],stat["l01byf"],deg=1)
    plt.plot(np.linspace(0,2500,2501),np.poly1d(coeff5)(np.linspace(0,2500,2501)),color="blue",label="f: y=%.4fx%+.4f"%(coeff5[0],coeff5[1]))
    plt.legend()
    # plt.axis("equal")
    plt.xlim((0,2500))
    plt.ylim((-200,200))
    print(coeff4)
    print(np.corrcoef(stat["Tc"],stat["l01byb"]))
    
    # plt.show()
    plt.savefig(resultpath+"stat_4.png",dpi=200)
    for i,d in enumerate(data):
        plotone(d,testlist[i])
    print(0)
