from pymongo import MongoClient
import re
from datetime import datetime
import numpy as np
from collections import defaultdict

client = MongoClient()
db = client.get_database('pi')
coll = db.get_collection('dataBrut')
data = list(coll.find())

#*********************************************
#temps dict

time_dict = {
 'août': "aug",
 "avr.": "apr",
 "déc.": "Dec", 
 "févr.": "Feb", 
 "janv.": "Jan", 
 "juil.": "Jul", 
 "juin": "Jun",
 "mai": "may", 
 "mars":"mar", 
 "nov.": "Nov", 
 "oct.": "oct", 
 "sept.": "sep", 
 'Apr':'Apr',
 'Aug':'Aug',
 'Dec':'Dec',
 'Feb':'Feb',
 'Jan':'Jan',
 'Jul':'Jul',
 'Jun':'Jun',
 'Mar':'Mar',
 'May':'May',
 'Nov':'Nov',
 'Oct':'Oct',
 'Sep':'Sep'}

regex_time = "("+"|".join(list(time_dict.keys()))+")"

#skills dictionnary :

sql_skills = ["sql","PL.?SQL","mysql","MS.?SQL","SQL.?Server","SQLite","PostgreSQL","Rubinius","T.?SQL","mariadb","vsql"]
nosql_skills=["CouchDB","cassandra","mongo","hbase","redis","Scylla","Neo4j","DynamoDB","Memcached","Bigtable","Hypertable","Oracle","NoSQL"]
js_back_fram_skills=["javascript","Backbone","Express.?js","kraken.?js","Hapi.?js","Koa.?js","TotalJS","Nest.?js","Sails.?Js","Meteor.?Js","LoopBack","Derby.?Js","Adonis.?Js","Mojito","Keystone.?Js","Feathers.?Js","Restify.?Js","ActionHero.?Js","Sequelize","Moleculer"]
js_front_framewrok=["javascript","angular","vue.?js","react","ember","jquery","Prototype","ext.?js"]
javascript_skills= ["node.?js","javascript","babel","npm","eslint", "typescript" ]
sys_skills=["linux","unix","ubuntu","redhat","SuSE","Debian","fedora","Bash","nginx","apache","systemctl","bash","shell","systemd","ssh","network"]
c_skills=["\sC\s","C\+\+","C#","wxWidgets","JUCE","CEGUI","CEF","GTK","Qt"]
xml_skills=["xml","html"]
css_skills=["css","bootstrap","sass","postcss"]
rest_skills=["soa","soap","REST","http","ajax"]
git_skills=["git","svn"]
java_skills=["Java","JEE","Spring","Struts","Hibernate","Wicket","JSF","Dropwizard","Grails","ATG","maven","spring.?boot","spring.?security"]
continus_build_skills=["Buddy","git","Jenkins","TeamCity","GoCD","Bamboo","CircleCI","Codeship","Buildbot","Nevercode","Integrity","Strider","Autorabit","Buildkite","Semaphore","CruiseControl","Urbancode"]
virt_skills=["Docker","Vagrant","Wox","Rancher","Kubernetes","Mesos","LXC","OpenVZ", "kvm"]
cloud_skills= ["Cloud", "Computing","AWS","google.?cloud","Bluemix","OVH","Joyent","Microsoft.?Azure","Cloudwatt","Ikoula","Rackspace","Nimbus","Niftyname","OpenStack","OpenNebula","Eucalyptus","vultr","DigitalOcean"]
php_skills=["php","symfony","CodeIgniter","Agavi","CakePHP","Dframe","Flight","FuelPHP","Hoa","Horde","Jelix","KumbiaPHP","Laravel","Laminas","Mkframework","MODx","PEAR","WebSite.?PHP","Zend","YAF"]
cms_skills=["drupal","wordpress","joomla","squarespace","magneto"]
scrum_skills= ["Zimbra","confluence","Slack","Scrum","Wrike","Agile","Trello","JIRA","Assembla","nTask","Targetprocess","Asana","Clarizen","QuickScrum","ScrumDo","VivifyScrum","scrumban","Kanban","Waterfall","GitScrum"]
testing_skills = ["Testrail","Zephyr","JMeter","TestLink","Selenium","QTP","SoapUI","Tricentis.?Tosca","Telerik","Katalon Studio","UFT","IBM.?RFT","Ranorex","Postman"]

back_skills=[javascript_skills,sql_skills,nosql_skills,"node.js"]
front_skills=["webpack"]
teck_skills=["micro-services"]
po_skills=["Team Building"]

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

#analytic_skills =["Matplotlib", "nltk","Bokeh","gensim"]
# TODO: update list 

all_skills = [sql_skills, nosql_skills, js_back_fram_skills, js_front_framewrok, javascript_skills, sys_skills, c_skills, xml_skills, css_skills,
rest_skills, git_skills, java_skills, continus_build_skills, virt_skills, cloud_skills, php_skills, cms_skills, scrum_skills, testing_skills,
networking_skills, big_data_skills, bi_skills, embarque_skills, matlab_skills, security_skills, telecom_skills, python_skills, deep_skills, ml_skills,
robo_skills,elastic_search_skills, r_skills ]

all_skills = set([j.lower().strip() for i in all_skills for j in i])
reg_all_skills = "("+"|".join(all_skills)+")"

data_tmp= []

def get_skills(text):
    return list(map(lambda x: re.sub("(\.|\-|_)" ,"",x), re.findall(reg_all_skills, text)))

def prepare_date(date):
    if date is None:
        return 0
    else:
        tmp_time = re.sub("(Present|Aujourd’hui)",datetime.strftime(datetime.now(),"%b %Y"),date)
        for i in re.findall(regex_time, tmp_time):
            tmp_time=tmp_time.replace(i, time_dict[i])   
        if re.search ("–",date) is None :
            tmp_time +=  "– "+datetime.strftime(datetime.now(),"%b %Y")    
        if len(re.findall("[A-Za-z]+",tmp_time))==1:
            tmp_time = re.sub("[A-Za-z]+","",tmp_time)            
        return (tmp_time.split("–")[0].strip(),tmp_time.split("–")[1].strip())  

def calc_date(dates):
    try :
        try :
            tmp1 = datetime.strptime(dates[1], "%b %Y") 
            tmp2 = datetime.strptime(dates[0], "%b %Y")
            return (tmp1.year*12 - tmp2.year*12) + (tmp1.month - tmp2.month)
        except :
            tmp1 = datetime.strptime(dates[1], "%Y")
            tmp2 = datetime.strptime(dates[0], "%Y")
            return (tmp1.year*12 - tmp2.year*12)
    except:
        return 0    


def get_degree (text):
    if text is not None:
        if re.search("(ing\w+|eng\w+)" ,text.lower()) is not None:
            return "eng"
        if re.search("licen\w+" ,text.lower()) is not None:
            return "lic"
        if re.search("(mait\w+|mâit\w+|mast\w+|maît\w+|mâît\w+)" ,text.lower()) is not None:
            return "mast"
        if re.search("(doct\w+|phd\w*)" ,text.lower()) is not None:
            return "phd"
    return None

for row in data:
    jobs = {"id":str(row['_id']) ,"url": row['url'], "search": row["search"], 'skills':[],
            "experiences":{'skills':{},"companies":[],"date_range":0,"date_mean":0}, 
            'education':list(filter ( lambda y: y is not None , map(lambda x: get_degree(x['degree']), row['experiences']['education']))),
            'languages': len(row['accomplishments']['languages']), 'organizations':len(row['accomplishments']['organizations'])+len(row['experiences']['volunteering']),
            'projects': len(row['accomplishments']['projects'])}
    skills_dict = defaultdict(int)
    title_set = set()
    date_set= []
    jobs['skills'] = list(set(get_skills(' '.join(list(map(lambda x: x['name'].strip().lower() ,row['skills']))))))
    for job in row['experiences']['jobs']:
        title_set.add(job['company'])
        tompon_text =job['title']
        try:
            date_set.append((int(re.sub("[A-Za-z]","",prepare_date(job['date_range'])[0])),int(re.sub("[A-Za-z]","",prepare_date(job['date_range'])[1]))))
        except:
            pass
        try :
            tompon_text += " "+job["description"]
        except:
            pass    
        tompon_text= tompon_text.lower()   
        skills_tmp = list(set(get_skills(tompon_text)))
        for s in skills_tmp:
            skills_dict[s]+=calc_date(prepare_date(job['date_range']))
    jobs["experiences"]['skills']=dict(skills_dict)
    jobs["experiences"]['companies']=list(title_set)
    if (date_set != []):
        jobs["experiences"]['date_mean'] = np.mean(list(map(lambda x: x[1]-x[0], date_set)))
        date_set = sorted(set([dd for d in date_set for dd in d]))
        jobs["experiences"]['date_range'] = date_set[-1]-date_set[0]
    else :
        pass

    #print(jobs)
    data_tmp.append(jobs)
print(data_tmp)

#print(len(list(filter(lambda x: len(x["experiences"]['skills'].keys())==0 , data_tmp))))
try:
    db.drop_collection('data')
except:
    pass

col_final = db.create_collection('data')

col_final.insert_many(data_tmp)
