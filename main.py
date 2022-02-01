# !pip install ciw, matplotlib, pandas, seaborn
import ciw 
import seaborn as sns
import matplotlib.pyplot as plt
from random import randint
from platform import node
import pandas as pd

# Q=[]
# for sim in range(5):
#   ciw.seed(2)
#   Q.append(ciw.Simulation(N))
#   Q[sim].simulate_until_max_time(1440)

def estimation_ponctuelle(Y):
      return sum(Y)/len(Y)


PRECHAUFFAGE_TIME = 30
cols = ['id_number', 'customer_class', 'node', 'arrival_date', 'waiting_time', 'service_start_date', 'service_time', 'service_end_date', 'time_blocked', 'exit_date', 'destination', 'queue_size_at_arrival', 'queue_size_at_departure']
def rec_to_df(node, columns= cols):
      d = {col:[] for col in columns}
      
      for rec in node:
            for i in range(len(rec)):
              d[columns[i]].append(rec[i])
      
      return pd.DataFrame(d)

def moyenne(liste=[]) :
    return sum(liste)/len(liste)


tps_sejours = []
tps_attentes = []
nb_moy = {'node_1':[], 'node_2': [], 'node_3': [], 'node_4':[] }

#for a in range(10,40,3):

I=0.0001 
Y=0.0001 
R=10000 
S=1500 
A=30  #entre 10 et 40 
C=707 
B=16 
F=42.2 
N= ciw.create_network(
        arrival_distributions=[ ciw.dists.Exponential(rate=A),#SI 
                                ciw.dists.NoArrivals(),#SR   
                                ciw.dists.NoArrivals(),#SS 
                                ciw.dists.NoArrivals()],#SC 
        service_distributions=[ ciw.dists.Deterministic(value=I),#SI 
                                ciw.dists.Exponential(rate=1/(Y+B/R)),#SR 
                                ciw.dists.Deterministic(value=B/S),#SS 
                                ciw.dists.Deterministic(value=B/C)],#SC 
        routing=[[0, 1, 0, 0], 
                    [0, 0, 1, 0], 
                    [0, 0, 0, 1], 
                    [0, B/F, 0, 0]], 
        number_of_servers=[1, 1, 1, 1] 
    ) 
ciw.seed(randint(0,10000))
Q = ciw.Simulation(N)
Q.simulate_until_max_time(1440)
recs = Q.get_all_records()

#l = [rec for rec in recs if   rec.destination==-1]




prechauff = [rec.id_number for rec in recs if rec.node == 1 and rec.arrival_date <= PRECHAUFFAGE_TIME]
id_clients = [rec.id_number for rec in recs if rec.destination ==-1 and rec.id_number not in prechauff]

node_1 = rec_to_df([rec for rec in recs if rec.node==1 and rec.id_number not in prechauff])
node_2 = rec_to_df([rec for rec in recs if rec.node==2 and rec.id_number not in prechauff])
node_3 = rec_to_df([rec for rec in recs if rec.node==3 and rec.id_number not in prechauff])
node_4 = rec_to_df([rec for rec in recs if rec.node==4 and rec.id_number not in prechauff])


travel_time =[]



    # temps de sejours
for id_client in id_clients:
    travel_time.append(node_4[node_4.id_number==id_client].exit_date.iloc[0] - node_1[node_1.id_number==id_client].arrival_date.iloc[0])
print("travel_time : ",moyenne(travel_time))
tps_sejours.append(moyenne(travel_time))

# nb moyen de client en attente dans chaque noeud
nb_moy['node_1'].append(node_1.queue_size_at_arrival.mean())
nb_moy['node_2'].append(node_2.queue_size_at_arrival.mean())
nb_moy['node_3'].append(node_3.queue_size_at_arrival.mean())
nb_moy['node_4'].append(node_4.queue_size_at_arrival.mean())

# temps d'attente

tps_attentes.append(node_1.waiting_time.mean() + node_2.waiting_time.mean() + node_3.waiting_time.mean() + node_4.waiting_time.mean()) 

df_attentes = pd.DataFrame({'tps_attentes':tps_attentes})
df_nb_moy   = pd.DataFrame(nb_moy)
df_sejours  = pd.DataFrame({'tps_sejour': tps_sejours})

fig = plt.figure()
sns.scatterplot(x=30, y= df_attentes.tps_attentes)

fig.savefig('tps_attentes_P2.png')
fig, ax2 = plt.subplots(1,4, figsize=(25,5))
for i in range(1,5):
  sns.scatterplot(x=30, y= df_nb_moy['node_'+str(i)], ax=ax2[i-1]) 
fig.savefig('nb_moy_P2.png')

sns.scatterplot(x=30, y= df_sejours.tps_sejour) 
fig.savefig('tps_sejours_P2.png')

for a,b in ((1,2), (2,4)):
  print(a,b)
  
# print(node_1.arrival_date)
# node_1[node_1.id_number==40888]
# node_1.arrival_date.mean()
node1 =[rec for rec in recs if rec.node==1 and rec.arrival_date > PRECHAUFFAGE_TIME]
node4 =[rec for rec in recs if rec.node==4]
travelTime =[]
for rec1 in node1 :
  for rec4 in node4 :
    if rec1.id_number == rec4.id_number :
      travelTime.append(rec4.exit_date - rec1.arrival_date)
print("Travel time : ", moyenne(travelTime))


