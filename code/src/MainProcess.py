from GowallaData import GowallaData
from Synthesize import SynTraj
import Convertor
import time
import Evaluation

def DoProcess(infile,outfile):
    btime = time.time()
    Gowalla = GowallaData()
    Gowalla.read_checkin_file(infile)
    Gowalla.gen_feature()
    Gowalla.divide_user()
    originDB = Convertor.convertGowallaToTraj(Gowalla)
    synDB = {}
    for uid,db in originDB.items():
        synDB[uid] = SynTraj(originDB[uid],1)
    originAllDB = Convertor.convertDbToList(originDB)
    synAllDB = Convertor.convertDbToList(synDB)
    print("DiameterError",Evaluation.DiameterError(originAllDB,synAllDB,20))
    Convertor.convertTrajToFile(synDB,outfile)
    etime = time.time()
    print("DoProcess:",etime-btime)

if __name__ == "__main__":
    DoProcess("/home/Gowalla_sample.txt","output.csv")
    