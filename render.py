import requests
import shutil
import datetime
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

doc = SimpleDocTemplate("Report.pdf", pagesize=letter,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)
Story = []
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
image_list = []


SlackToken= "xoxb-573662986324-599506195031-oDP9ZSLQjFzrThZfQVEdgsml"
start_date = (datetime.datetime.now() - datetime.timedelta(minutes=15)).timestamp()
end_date = datetime.datetime.now().timestamp()

BASE_URL = "http://prom-grafana:80"
GET_DASHBOARD_URL = BASE_URL + "/api/search?folderIds=0&query=&starred=false"


headers = {
    'content-type': "application/json",
    'authorization': "Basic YWRtaW46cHJvbS1vcGVyYXRvcg==",
}

res = requests.get(url=GET_DASHBOARD_URL, headers=headers)
data = res.json()

for dashboard in data:
    print(dashboard["url"])
    URL = BASE_URL + "/render" + dashboard['url'] + "?width=1920&height=3000&from"+str(start_date)+"&to"+str(end_date)+"&kiosk"
    request = requests.get(url=URL, headers=headers, stream=True)
    if request.status_code == 200:
        if ' ' in dashboard["title"]:
            image_name = dashboard["title"].replace(" ", "").replace("/", "")
            print(image_name)
        else:
            image_name = dashboard["title"]
            print(image_name)
        image_list.append(image_name)
        with open(image_name + ".png", 'wb') as out_file:
            request.raw.decode_content = True
            shutil.copyfileobj(request.raw, out_file)
        del request

for image in image_list:
    ptext = '<font size=12>%s</font>' % image
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    im = Image(image + ".png", 4 * inch, 4 * inch)
    Story.append(im)

doc.build(Story)

my_file = {
    'file': ("Report.pdf", open("Report.pdf", 'rb'), 'pdf')
}

payload = {
    "filename": "Report.pdf",
    "token": SlackToken,
    "channels": ['#kubernetes-bot'],
}
req = requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)
print(req.json())
