#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import random
from datetime import datetime
random.seed(2)

FOLDER = "/home/ubuntu/mevboost.pics/scripts/enriched_data/"
PROJECT = "/home/ubuntu/mevboost.pics/scripts/"
STORAGE_FOLDER= "/home/ubuntu/mevboost.pics/scripts/eth-tornado-warning/"


# In[ ]:


DAYS = 1
with open(PROJECT+"tornado_latest_known_block.txt", "r") as file:
    slotnow = int(file.read())


df = pd.read_csv(PROJECT+"tornadothroughmev.csv")
tornados = []
while len(tornados) < 15:
    tornados = df.query(f"slot > {slotnow-(86400/12)*DAYS}")
    tornados = tornados[["block_number", "relay"]]
    tornados["block_number"] = tornados["block_number"].apply(lambda x: str(int(x)))
    DAYS += 1
DAYS -= 1


# In[ ]:


def get_timestamp_of_slot(slot):
    date = 1654824023 + (slot-int(4e6))*12
    date = datetime.strftime(datetime.utcfromtimestamp(date), "%Y-%m-%d, %I:%M %p") + " +UTC"
    return date

rand = lambda x, y: random.randint(x,y)

manifold_co = [(80, 150),(95, 150),(60, 130),(60, 140),(70, 160), (110, 120), (60, 250), (100, 300), 
               (100, 250), (120, 360), (70,180), (70,190),
               (100, 170), (130, 140), (80, 270), (120, 320), (120, 270), (140, 380), (140, 365),
               (90, 160), (120, 130), (70, 260), (110, 310), (110, 260), (130, 370), (135, 365)]

bloxroute_mp = [(350, 130), (350, 160), (370, 200), (370, 230), (370, 300), (370, 360), 
                (390, 380), (370, 120), (390, 220), (390, 250), (390, 320), (390, 380), 
                (410, 400), (360, 110), (380, 210), (380, 240), (380, 310), (380, 370), 
                (400, 390)]
bloxroute_et = [(290, 220), (320, 300), (310, 290), (340, 290), (310, 320), (310, 300), 
                (320, 295), (340, 320), (300, 230), (310, 285), (330, 310)]

blocknative_co = [(180, 50), (250, 50), (300, 50), (350, 50), (350, 90), (200, 70), 
                  (220, 70), (270, 70), (320, 70), (370, 70), (370, 110), (190, 60), 
                  (260, 60), (310, 60), (360, 60), (360, 100)]

def get_coordinates(relay):
    global manifold_co, bloxroute_mp,bloxroute_et,blocknative_co
    if relay == "manifold":
        if len(manifold_co) == 1:
            manifold_co = [(80, 150),(95, 150), (110, 120), (60, 250), (100, 300), (100, 250), (120, 360), 
               (100, 170), (130, 140), (80, 270), (120, 320), (120, 270), (140, 380), (140, 365),
               (90, 160), (120, 130), (70, 260), (110, 310), (110, 260), (130, 370), (135, 365)]
        x,y = manifold_co[rand(0,len(manifold_co)-1)]
        manifold_co.remove((x,y))
        x,y = x + rand(-10,10), y + rand(-10,10)
    elif relay == "bloxroute (max profit)":
        if len(bloxroute_mp) == 1:
            bloxroute_mp = [(350, 130), (350, 160), (370, 200), (370, 230), (370, 300), (370, 360), 
                (390, 380), (370, 120), (390, 220), (390, 250), (390, 320), (390, 380), 
                (410, 400), (360, 110), (380, 210), (380, 240), (380, 310), (380, 370), 
                (400, 390)]
        x,y = bloxroute_mp[rand(0,len(bloxroute_mp)-1)]
        bloxroute_mp.remove((x,y))
        if int(y-180) >20:
            x,y = x + rand(-10,10), y + rand(-10,10)
            
    elif relay == "bloxroute (ethical)":
        if len(bloxroute_et) == 1:
            bloxroute_et = [(290, 220), (320, 300), (310, 290), 
                (320, 295), (340, 320), (300, 230), (310, 285), (330, 310)]
        x,y = bloxroute_et[rand(0,len(bloxroute_et)-1)]
        bloxroute_et.remove((x,y))
        x,y = x + rand(-15,15), y + rand(0,15)
            
    elif relay == "blocknative":
        if len(blocknative_co) == 1:
            blocknative_co = [(180, 50), (250, 50), (300, 50), (350, 50), (350, 90), (200, 70), 
                      (220, 70), (270, 70), (320, 70), (370, 70), (370, 110), (190, 60), 
                      (260, 60), (310, 60), (360, 60), (360, 100)]
        x,y = blocknative_co[rand(0,len(blocknative_co)-1)]
        blocknative_co.remove((x,y))
        x,y = x + rand(-5,5), y + rand(-20,10)
            
    elif relay == "eden":
        x = rand(680,700)
        y = rand(100,350)
        if int(y-280) > 10:
            y += rand(80,150)
    else:
        x = 1
        y = 1
    if x <= 0:
        x+= 10
    return x,y


# In[ ]:


tornados["point"] = tornados["relay"].apply(lambda x:get_coordinates(x))
tornados["x"] = tornados["point"].apply(lambda x: x[0])
tornados["y"] = tornados["point"].apply(lambda x: x[1])


# In[ ]:


img_width = 1600
img_height = 900
scale_factor = 0.5

tornado = tornados
# Create figure
fig1 = go.Figure()

fig1.update_xaxes(
    visible=False,
    range=[0, img_width * scale_factor]
)

fig1.update_yaxes(
    visible=False,
    range=[0, img_height * scale_factor],
    # the scaleanchor attribute ensures that the aspect ratio stays constant
    scaleanchor="x"
)

# Add trace
fig1.add_trace(
    go.Scatter()
)

# Add images
fig1.add_layout_image(
     source=Image.open(PROJECT+"map1.png"),
         x=0,
        sizex=img_width * scale_factor,
        y=img_height * scale_factor,
        sizey=img_height * scale_factor,
        xref="x",
        yref="y",
        opacity=1.0,
        layer="below",
        sizing="stretch",
)
fig1.update_layout(
    width=img_width * scale_factor,
    height=img_height * scale_factor,
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
)

fig2 = px.scatter(x=tornado["x"], 
                  y=tornado["y"], 
                  size=[150]*len(tornado), 
                  opacity=0.001)
#fig2 = px.scatter(x=[250,2,3], y=[250,1,3], size=[150,100,100], opacity=0.001)
#for i in [200,2,3]:
#    fig2.add_layout_image(
#            dict(
#               xref="x",
#                yref="y",
#                xanchor="center",
#                yanchor="middle",
#                x=i,
#                y=250,
#                sizex=200,
#                sizey=300,
#                sizing="contain",
#                opacity=1.0,
#                layer="above",
#                source=Image.open("./tornadologo.png"),
#            ))

fig = go.Figure(data=fig1.data+fig2.data, layout = fig1.layout)



for ix, i in tornados.iterrows():
    _x=i["x"]
    _y=i["y"]
    fig.add_layout_image(
            source=Image.open(PROJECT+"tornadologodark_light.png"),
            xref="x",
            yref="y",
            x=_x,
            y=_y,
            xanchor="center",
            yanchor="middle",
            sizex=20,
            sizey=20
        )
    fig.add_annotation(
        text=f"<a href='https://etherscan.io/block/{i['block_number']}' style='opacity:0;font-size:30px'>.</a>",
        font=dict(size=50),
        x=_x,
        y=_y,
        showarrow=False,
        xref="x",
            yref="y",                                         
        xanchor="center",
            yanchor="middle",
    )
    
    
#fig2 = px.scatter(x=[250,2,3], y=[250,1,3], size=[200,100,100], opacity=0.8)
fig = go.Figure(data=fig.data+fig2.data, layout = fig.layout)
fig.update_traces(hovertemplate='Click for info')
fig.update_layout(hovermode="closest",
                  hoverlabel=dict(
                    bgcolor="#0A0F14",
                    font_size=18
                 ),dragmode="pan"#, xaxis=dict(fixedrange =True),
                  #yaxis=dict(fixedrange =True)
                 )

# Set templates
#fig.update_layout(template="plotly_white",
#                  width=1000,
#                  height=500,
#                  xaxis = dict(
#                        tickmode = 'array',
#                        tickvals = [0,6],
#                        ticktext = ['0', '']
#                    ),
#                 yaxis = dict(
#                        tickmode = 'array',
#                        tickvals = [0,8],
#                        ticktext = ['0', '9']
#                    ))
#fig.update_yaxes(visible=False, showticklabels=False)
fig.update_layout(yaxis={'visible': False, 'showticklabels': False})
fig.update_layout(xaxis={'visible': False, 'showticklabels': False})

#Plotly.newPlot(id, data, layout, {scrollZoom: true})

#fig.show(config={'doubleClick': 'reset', 'scrollZoom': True})
print(True)


# In[ ]:


config = dict({'scrollZoom': True})
fig.write_html(PROJECT+"tornadohtml.html", include_plotlyjs="cdn", config=config)


# In[ ]:


#6b8bbc


# In[ ]:


#['blocknative', 'bloxroute (ethical)', 'bloxroute (max profit)', 'manifold', 'eden']


# In[ ]:


#relays = ['blocknative', 'bloxroute (ethical)', 'bloxroute (max profit)', 'manifold', 'eden']


# In[ ]:


relays = list(set(tornados["relay"]))
relays = [i[0].upper()+i[1:].split(" (")[0] for i in relays]
relays = list(set(relays))
relays = ", ".join(relays[0:-1])+ " and " + relays[-1]

print(relays)


# In[ ]:


header = """
<title>Tornado Warnings</title>
<link rel="shortcut icon" href="https://github.com/Nerolation/eth-tornado-warning/blob/main/tornadologodark_light.png">
<meta property="og:title" content="Ethereum Tornado Warnings">
<meta property="og:site_name" content="Ethereum Tornado Warnings">
<meta property="og:url" content="https://tornado-warning.info/">
<meta property="og:description" content="Tornado-warning.info provides information on the most recent tornados seen on the Ethereum blockchain.">
<meta property="og:type" content="website">
<meta property="og:image" content="https://github.com/Nerolation/eth-tornado-warning/blob/main/map1.png">

<meta name="twitter:card" content="summary_large_image">
<meta property="twitter:domain" content="https://tornado-warning.info">
<meta property="twitter:url" content="https://tornado-warning.info">
<meta name="twitter:title" content="Ethereum Tornado Warnings">
<meta name="twitter:description" content="Tornado-warning.info provides information on the most recent tornados seen on the Ethereum blockchain.">
<meta name="twitter:image" content="https://github.com/Nerolation/eth-tornado-warning/blob/main/map1.png">
<style>
tbody tr:nth-child(odd){
  background-color: #81a2d4;
}


@media only screen and (max-width: 767px)  { 
    .latest {
        font-size:8px;
    }
    .subt {
        font-size:14px;
    }
    .kids {
        font-size:12px;
    }
    .seighted {
        font-size:14px;
    }
    .footer {
        font-size:18px;
    }
    .zoomin {
        font-size:12px;
    }
}

@media only screen and (min-width: 768px) { 
    .latest {
        font-size:16px;
    }
    .subt {
        font-size:24px;
    }
    .kids {
        font-size:16px;
    }
    .seighted {
        font-size:18px;
    }
    .footer {
        font-size:16px;
    }
    .zoomin {
        font-size:18px;
    }
}

@media only screen and (orientation: portrait) {
    .latest {
        font-size:8px;
    }
    .subt {
        font-size:14px;
    }
    .kids {
        font-size:12px;
    }
    .seighted {
        font-size:14px;
    }
    .footer {
        font-size:18px;
    }
    .zoomin {
        font-size:12px;
    }
}
a:link {
  color: #0A0F14;
}

a:visited {
  color: #0A0F14;
}

a:hover {
  color: hotpink;
}

a:active {
  color: #0A0F14;
}

.nsewdrag {
    fill: #6b8bbc;
}
</style>
<script>
window.addEventListener('load', (event) => {
  var elem = document.getElementsByClassName("nsewdrag");
  elem[0].style.fill = "#6b8bbc";
});
</script>


"""

table_raw = """
<table style='font-family:Georgia;border: 1px solid #0A0F14;border-collapse: collapse;text-align: center;'>
<tbody>
<tr>
<th style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>Relay</th>
<th style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>...last 24h</th>
<th style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>...last 14 days</th>
<th style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>...last 30 days</th>
<th style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>...since merge</th>
<th style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>Total Blocks</th>
<th style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>Tornados per<br>Total Blocks</th>
</tr>
<tr>
<td style='border: 1px solid #0A0F14;font-weight: bold;padding: 1px 20px 2px 20px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px';>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px';>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px';>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px';>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px';>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px';>{}</td>
</tr>
<tr>
<td style='border: 1px solid #0A0F14;font-weight: bold;padding: 1px 20px 2px 20px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
</tr>
<tr>
<td style='border: 1px solid #0A0F14;font-weight: bold;padding: 1px 20px 2px 20px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
</tr>
<tr>
<td style='border: 1px solid #0A0F14;font-weight: bold;padding: 1px 20px 2px 20px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
</tr>
<tr>
<td style='border: 1px solid #0A0F14;font-weight: bold;padding: 1px 20px 2px 20px'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px'>{}</td>
</tr>
<tr>
<td style='border: 1px solid #0A0F14;font-weight: bold;padding: 1px 20px 2px 20px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
</tr>
<tr>
<td style='border: 1px solid #0A0F14;font-weight: bold;padding: 1px 20px 2px 20px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
<td style='border: 1px solid #0A0F14;padding: 1px 5px 2px 5px;'>{}</td>
</tr>
</tbody>
</table>"""


# In[ ]:


df = pd.read_csv(PROJECT+"tornado_stats.csv")
df = df[["relay", "slot_1_day", "slot_14_day", "slot_30_days", "slot", "slot_total"]]
df["percentage"] = df.apply(lambda x: str(round(x["slot"]/x["slot_total"]*100,2)) + "%", axis=1)
df["percentage_int"] = df.apply(lambda x: x["slot"]/x["slot_total"], axis=1)


df = df.sort_values("percentage_int")[::-1]
df = df.drop("percentage_int", axis = 1)
string = []
for ix, i in df.iterrows():
    for ixx, j in enumerate(i):
        if ixx == 0:
            string.append(j[0].upper()+j[1:])
            continue
        try:
            string.append("{:,}".format(int(j)))
        except:
            string.append(str(j))


# In[ ]:


headerscript = """<meta name="viewport" content="width=device-width, initial-scale=1">"""


add = '<h1 style="text-align:center;font-family:Georgia;font-variant:small-caps;font-size: 60px;color:#0F1419;">🚨 Tornado Warnings 🚨</h1>'
add2 = '<p class="subt" style="font-weight:bold;max-width:80%;font-family:Georgia">⚠️ Beware, dangerous tornados sighted at the relays of {}! ⚠️ <br>Some carry innocent money and come completely uncensored!</p>'.format(relays)
add3 = '<p class="zoomin" style="font-weight:bold;max-width:800px">Zoom in and click the Tornados to see their origin.</p>' \
        + '<p style="font-size:18px; font-weight:bold;max-width:800px"> </p>'

what = '<div style="padding-top: 3%;max-width:800px"><p style="font-size:28px; font-weight:bold;color:#0A0F14">What is this all about?</p>'
iss = '<p style="font-size:16px;margin-top:-15px;padding-bottom: 25px;">The map shows the existing MEV Boost relays and the MEV-boosted blocks of the last {} days that contained Tornado Cash transactions. While some relays take measures to prevent the terrible consequences of a tornado, others are exposed to them without any protection.</p>'.format(DAYS)

this = '<p style="font-size:26px; font-weight:bold;color:#0A0F14;">Why aren`t there tornados at every relay?</p>'
stuff = '<p style="font-size:16px;margin-top:-15px;padding-bottom: 25px;">Some relays operate under the guidance of the OFAC. This protects them from Tornados!</p>'

effec = '<p style="font-size:26px; font-weight:bold;color:#0A0F14">What are the effects of Tornados?</p>'
expla = '<p style="font-size:16px;margin-top:-15px;padding-bottom: 25px;">Tornados kick up a lot of dust, so observers often can`t identify the victims. Uprooted merkle trees fly through the air. A horrible scenario. Survivors often have zero knowledge what happened.</p>'


quali = '<p style="font-size:26px; font-weight:bold;color:#0A0F14">What qualifies as a Tornado?</p>'
ans = '<p style="font-size:16px;margin-top:-15px;padding-bottom: 25px;">Every block including a transaction that interacted with the ETH, DAI, USDC, USDT, cDai or wBTC contracts of Tornado Cash, no matter which denomination, plus TORN Transfers (mainnet only).</p>'


learn = '<p style="font-size:26px; font-weight:bold;color:#0A0F14">What`s the message?</p>'
yeah = '<p style="font-size:16px;margin-top:-15px;padding-bottom: 25px;">We should not interfere with nature.<br>🏴 Censorship-resistance must remain a core value. 🏴</p>'
end = '</div>'

warn = '<p class="kids" style="font-weight:bold;max-width:80%">There is an ongoing warning:<br>🚨&nbsp;Keep children from the mempool!&nbsp;🚨</p>'.format(relays)

love = '<div class="footer" style="padding-top: 5%;font-weight:bold;padding-bottom: 5%;max-width:800px;"><div class="footer" style ="float:left;">Built with 🖤 by '\
    + '<a href="https://github.com/Nerolation">Toni Wahrstätter</a></div>'\
    +'<div class="footer" style ="float:right;font-weight:bold;">View Source on <a href="https://github.com/Nerolation/eth-tornado-warning">Github</a></div></div>'

NOWTS = get_timestamp_of_slot(slotnow)

seighted = "<p class='seighted' style='text-align: center;margin-top:5%;font-weight:bold;'>🌪️ Tornado stats:</p>"
latest = "<div class='latest' style ='color:#0F1419;font-family:Georgia;'>Last updated at slot {:,.0f} ({})</div>".format(slotnow, NOWTS)

table = table_raw.format(*tuple(string))


# In[ ]:


with open(PROJECT+"tornadohtml.html", "r") as file:
    f = file.read()
    #f = f.replace("./tornadologodark_light.png","https://toniwahrstaetter.com/tornadologodark_light.png")
    #f = f.replace("./map1.png","https://toniwahrstaetter.com/map1.png")
    f = f.replace("<head>", "<head>"+header)    
    f = f.replace("<body>", "<body style='font-family: Courier New, monospace;max-width: 1280px;width: 100%;margin-left: auto;margin-right: auto;background-color:#6b8bbc'> <center>" + add+add2+add3)    
    f = f.replace("</body>", "{}</center></body> ".format(seighted+latest+table+warn+what+iss+this+stuff+effec+expla+quali+ans+learn+yeah+end+love))
    
with open(STORAGE_FOLDER+"index.html", "w") as filew:
    filew.write(f)


# In[ ]:


print(datetime.strftime(datetime.now(), "%Y-%m-%d, %I:%M %p") + " - tornadomap")


# In[ ]:




