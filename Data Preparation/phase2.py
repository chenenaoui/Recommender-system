from pymongo import MongoClient
import numpy as np
import pandas as pd
import re
from collections import defaultdict, Counter
import sys

#*************************************skills list*************************************
sql_skills = ["sql","PL.?SQL","mysql","MS.?SQL","SQL.?Server","SQLite","PostgreSQL","Rubinius","T.?SQL","mariadb","vsql"]
nosql_skills=["CouchDB","cassandra","mongo","hbase","redis","Scylla","Neo4j","DynamoDB","Memcached","Bigtable","Hypertable","Oracle","NoSQL"]
js_back_fram_skills=["Hapi.?js","Koa.?js","Express.?js","Backbone","kraken.?js","TotalJS","Nest.?js","Sails.?Js","Meteor.?Js","LoopBack","Derby.?Js","Adonis.?Js","Mojito","Keystone.?Js","Feathers.?Js","Restify.?Js","ActionHero.?Js","Sequelize","Moleculer"]
js_front_framewrok=["ext.?js","vue.?js","ember","Prototype","jquery","angular","react"]
javascript_skills= ["javascript","babel","eslint", "typescript" ]
nodejs_skills = ["node.?js","npm"]
sys_skills=["linux","unix","ubuntu","redhat","SuSE","Debian","fedora","Bash","nginx","apache","systemctl","bash","shell","systemd","ssh","network"]
c_skills=["\sC\s","C\+\+","C#","wxWidgets","JUCE","CEGUI","CEF","GTK","Qt"]
xml_skills=["xml","html"]
css_skills=["css","bootstrap","sass","postcss"]
rest_skills=["soa","soap","REST","http","ajax"]
git_skills=["git","svn"]
java_skills=["Java","JEE","Spring","Struts","Hibernate","Wicket","JSF","Dropwizard","Grails","ATG","maven", "spring.?boot", "spring.?security"]
continus_build_skills=["Buddy","git","Jenkins","TeamCity","GoCD","Bamboo","CircleCI","Codeship","Buildbot","Nevercode","Integrity","Strider","Autorabit","Buildkite","Semaphore","CruiseControl","Urbancode"]
virt_skills=["Docker","Vagrant","Wox","Rancher","Kubernetes","Mesos","LXC","OpenVZ", "kvm"]
cloud_skills= ["Cloud", "Computing","AWS","google.?cloud","Bluemix","OVH","Joyent","Microsoft.?Azure","Cloudwatt","Ikoula","Rackspace","Nimbus","Niftyname","OpenStack","OpenNebula","Eucalyptus","vultr","DigitalOcean"]
php_skills=["php","symfony","CodeIgniter","Agavi","CakePHP","Dframe","Flight","FuelPHP","Hoa","Horde","Jelix","KumbiaPHP","Laravel","Laminas","Mkframework","MODx","PEAR","WebSite.?PHP","Zend","YAF"]
cms_skills=["drupal","wordpress","joomla","squarespace","magneto"]
scrum_skills= ["Zimbra","confluence","Slack","Scrum","Wrike","Agile","Trello","JIRA","Assembla","nTask","Targetprocess","Asana","Clarizen","QuickScrum","ScrumDo","VivifyScrum","scrumban","Kanban","Waterfall","GitScrum"]
testing_skills = ["Testrail","Zephyr","JMeter","TestLink","Selenium","QTP","SoapUI","Tricentis.?Tosca","Telerik","Katalon Studio","UFT","IBM.?RFT","Ranorex","Postman"]
front_skills=["webpack"]
teck_skills=["micro-services"]
# updated 10/4/2010 :
big_data_skills = ["Business Analytic","Mining","Warehous","décisionnelle","Splunk","Scala","Julia",
"Fluentd","Grafana","Memcached","KNIME","Statistica","Excel",
"dashboarding","big data","hadoop", "Spark", "Storm", "RapidMiner","SAMOA","HPCC", "Quoble", "Hive", "Cloudera", "Openrefine", "Teradata","kafka"]
networking_skills = ["cisco","pfsense","san", "\sdns\s", "dhcp", "\snat\s", "huawei","Troubleshooting","ccna","socket","\sip\s","tcp","udp","ssh","telnet","\slan\s", "vpn", "Packet Tracer"]
bi_skills = ["SAP","Sisense","bods","Talend", "warehouse","QlikSense","Power.?BI","Looker","Tableau","zoho","ssis","ssas","ssrs"]
embarque_skills = ["raspberry","Stm","assembleur","arduino"]
matlab_skills =["matlab"]
security_skills = ["ips","audit","Symantec","Metasploit","Hacking","Vulnera","Phishing","Malware"]
telecom_skills = ["voip","gsm"]
python_skills =["python","Tkinter","CherryPy","Django","Flask" ,"Pylons", "Pyramid", "Pylons", "Web2py","BeautifulSoup"]
deep_skills = ["deep",  "tensorflow", "Recurrent Neural","RNN", "Keras", "py.?torsh","caffe", "convolution neural network", "cnn"]
ml_skills = ["Learning","classification","regression", "clustering" ,"Computer vision","srilm", "theano","Lasagne", "scikit", "Anaconda", "scrap", "ADAS"]
robo_skills =["kuka","linx","winautomation","automai"] 
elastic_search_skills = ["Elasticsearch", "Logstash", "Kibana"]
r_skills = ["\sR\s"]
#***************************************preparing arch*********************************
tt = [
    
    {'js':np.unique(np.hstack([javascript_skills, js_back_fram_skills, js_front_framewrok,nodejs_skills, ])).tolist()},
    {'js_front': js_front_framewrok},
    {'js_back':np.unique(np.hstack([js_back_fram_skills,nodejs_skills, ])).tolist()},
    {"nodejs": nodejs_skills},
    {"jquery":["jquery"]},
    {"express.js":["Express.?js"]},
    {"koa.js":["Koa.?js"]},
    {"hapi.js":["Hapi.?js"]},
    {"angular.js":["angular"]},
    {"react.js":["react"]},
    {"sql": sql_skills},
    {"nosql": nosql_skills},
    {"bash":['bash','shell']},
    {"nginx":["nginx"]},
    {"C":c_skills},
    {"html":xml_skills},
    {"css":css_skills},
    {"sass":["sass"]},
    {"postCss":["postcss"]},
    {"rest":rest_skills},
    {"webpack":front_skills},
    {"git":["git"]},
    {"linux":sys_skills},
    {"java/jee":java_skills},
    {"microservices":teck_skills},
    {"Intégration continue":continus_build_skills},
    {"virt":virt_skills},
    {"Docker":["Docker"]},
    {"Kubernetes":["Kubernetes"]},
    {"cloud":cloud_skills},
    {"aws":["aws"]},
    {"ext.js":["ext.?js"]},
    {"mongoDB":["mongo"] },
    {"MySQL":["mysql"]},
    {"spring":["spring", "spring.?boot", "spring.?security"]},
    {"spring boot":["spring.?boot"]},
    {"spring security":["spring.?security"]},
    {"soa":["soa"]},
    {"soap":["soap"]},
    {"svn":["svn"]},
    {"scrum":scrum_skills},
    {"jira":["jira"]},
    {"confluence":["confluence"]},
    {"php":php_skills},
    {"Laravel":["Laravel"]},
    {"symfony":["symfony"]},
    {"cms":cms_skills},
    {"drupal":["drupal"]},
    {"testing":testing_skills},
    {"big_data":big_data_skills},
    {"elastic":elastic_search_skills},
    {"networking":networking_skills},
    {"bi": bi_skills},
    {"embarque":embarque_skills},
    {"matlab":matlab_skills},
    {"security":security_skills},
    {"telecom":telecom_skills},
    {"python":np.unique(np.hstack([python_skills, deep_skills, ml_skills ])).tolist()},
    {"django":["django"]},
    {"flask":["flask"]},
    {"deep":deep_skills},
    {"ml":ml_skills},
    {"r":r_skills},
    {"robotic":robo_skills}
]

all_skills = [sql_skills, nosql_skills, js_back_fram_skills, js_front_framewrok, javascript_skills, nodejs_skills ,sys_skills, c_skills, xml_skills, css_skills,
rest_skills, git_skills, java_skills, continus_build_skills, virt_skills, cloud_skills, php_skills, cms_skills, scrum_skills, testing_skills,
networking_skills, big_data_skills, bi_skills, embarque_skills, matlab_skills, security_skills, telecom_skills, python_skills, deep_skills, ml_skills,
robo_skills,elastic_search_skills, r_skills ]

all_skills = set([j.lower().strip() for i in all_skills for j in i])

skills_swaped = {}
for i in all_skills:
    skills_swaped[i]=[i]
#print(skills_swaped)
"""
skills_swaped = defaultdict(list)
for element in tt:
    for i in element.values():
        for j in i:
            skills_swaped[j.lower().strip()].append(list(element.keys())[0])

skills_swaped = dict(skills_swaped)

print(skills_swaped)
"""
#*************************************functions**************************************
def find_cat(keyword):
    #print(keyword)
    for key in skills_swaped.keys():
        if re.match(key,keyword):
            #print("*******************")
            return skills_swaped[key] 

#*************************************mongo connection**************************************

client = MongoClient()
db = client.get_database('pi')
coll = db.get_collection('final')
data = list(coll.find())

#*************************************mongo connection**************************************
tmp_df = []
tmp_df2 = []
tmp_df3 = []
tmp_df4 = []

for row in data:
    tmp_dict = {}
    tmp_dict2 = {}
    tmp_dict3 = {}
    tmp_dict4 = {}

    tmp_skills = set()
    tmp_skills_job=defaultdict(list)

    tmp_dict['id']=row['id']
    tmp_dict['languages']= row["languages"]
    tmp_dict['organizations']= row["organizations"]
    tmp_dict['projects']= row["projects"]
    tmp_dict['certifs']= row["certifs"]
    tmp_dict['recommendations']= row["recommendations"]   
    for comp,val in row["experiences"]["companies"].items():
        tmp_dict[comp]=val 
    tmp_dict["date_range"]= row["experiences"]["date_range"]
    tmp_dict["date_mean"]= row["experiences"]["date_mean"]
    for comp,val in row["experiences"]["companies_type"].items():
        tmp_dict[comp]=val


    for skill in row['skills']:
        for cat in find_cat(skill):
            tmp_skills.add(cat)
    for skill in tmp_skills:
        tmp_dict2["sk_"+skill] = 1

    for skill in row["experiences"]["skills"].keys():
        for cat in find_cat(skill):
            tmp_skills_job[cat].append(row["experiences"]["skills"][skill])
    for k,v in tmp_skills_job.items():
        tmp_dict3[k]= max(v)
    
    for k,v in Counter(row["education"]).items():
        tmp_dict4[k]=v

    tmp_df.append(tmp_dict)
    tmp_df2.append(tmp_dict2)
    tmp_df3.append(tmp_dict3)
    tmp_df4.append(tmp_dict4)                
#****************************************test****************************************        
tmp_df = pd.DataFrame(tmp_df).fillna(0)
tmp_df2 = pd.DataFrame(tmp_df2, index=tmp_df.index).fillna(0)
tmp_df3 = pd.DataFrame(tmp_df3, index=tmp_df.index).fillna(0)
tmp_df4 = pd.DataFrame(tmp_df4, index=tmp_df.index).fillna(0)

df = pd.concat([tmp_df,tmp_df4,tmp_df2,tmp_df3], axis=1)
df.index=df.id
df.drop('id',axis=1, inplace=True)

df.to_csv('wevioo6.csv')
print(df)

"""
if __name__ == "__main__":
    print(find_cat(sys.argv[1]))
"""