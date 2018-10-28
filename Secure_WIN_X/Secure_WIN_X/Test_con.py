import webbrowser

HTML_name = open("Test_new.html","w")

def html_in(string_in_html, Check = 1, Param = True,file = HTML_name):
    if(Check == 0): #Заголовок
        file.writelines(fr'<font size = 6>{string_in_html} </font><br>')
    if(Check == 1): #Объект с галочкой
        if Param:
            file.writelines(fr'<font size = 4><font color="green">&#10004</font> {string_in_html}</font><br>')
        else:
            file.writelines(fr'<font size = 4><font color="red">&#10006</font> {string_in_html}</font><br>')
    if (Check == 2): #Объект с крестиком
        file.writelines(fr'<pre><p style="margin-left: 40px"><font size = 2> -{string_in_html} </font><br></p></pre>')
    if(Check == 3): # Plain_Text для дополнительных тегов нет тега <br>, поэтому не будет переноса на новую строку, может вызвать ошибку!!!
        file.writelines(fr'<font size = 4>{string_in_html}</font>')

def Init_html():
    html_in("<head><meta charset=""windows-1251""></head>",3)

def Out():
    useless_fun()
    webbrowser.open_new("Test_new.html")
    HTML_name.close()

def useless_fun():
    html_in("Тестовая часть-забчасть",0)
    html_in("first")
    html_in("second",Param = False)
    html_in("Test",2)
    html_in("first")  
    html_in("Слава тебе, \n\t безысходная боль!\n Умер вчера сероглазый король.<br> Вечер осенний был душен и ал,<br> Муж мой, вернувшись, спокойно сказал:<br> «Знаешь, с охоты его принесли,<br> Тело у старого дуба нашли.<br> Жаль королеву.\n\t Такой молодой!..<br> За ночь одну она стала седой».<br> Трубку свою на камине нашел<br> И на работу ночную ушел. <br> Дочку мою я сейчас разбужу,<br> В серые глазки ее погляжу.<br> А за окном шелестят тополя:<br> «Нет на земле твоего короля…»",2)