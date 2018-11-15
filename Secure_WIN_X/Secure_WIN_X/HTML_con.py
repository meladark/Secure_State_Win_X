import webbrowser

def html_in(string_in_html, Check = 1, Param = True,file = ""):
    file = HTML_name
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
        file.writelines(fr'<font size = 3>{string_in_html}</font><br>')

def Init_html(PATH_to_Folder):
    global HTML_name
    if(isinstance(PATH_to_Folder,str)):
       HTML_name = open(PATH_to_Folder + r"/Conclusion.html","w")
    else:
        HTML_name = open("Conclusion.html","w")
    html_in("<head><meta charset=""windows-1251""></head>",3)

def Out(PATH_to_Folder):
    useless_fun()
    if(isinstance(PATH_to_Folder,str)):
        webbrowser.open_new(PATH_to_Folder + r"/Conclusion.html")
    else:
        webbrowser.open_new("Conclusion.html")  
    HTML_name.close()

def useless_fun():
    html_in("Тестовая часть-забчасть",0)
    html_in("Вторая вложеность",3)  
    html_in("first")  
    html_in("Слава тебе, \n\t безысходная боль!\n Умер вчера сероглазый король.<br> Вечер осенний был душен и ал,<br> Муж мой, вернувшись, спокойно сказал:<br> «Знаешь, с охоты его принесли,<br> Тело у старого дуба нашли.<br> Жаль королеву.\n\t Такой молодой!..<br> За ночь одну она стала седой».<br> Трубку свою на камине нашел<br> И на работу ночную ушел. <br> Дочку мою я сейчас разбужу,<br> В серые глазки ее погляжу.<br> А за окном шелестят тополя:<br> «Нет на земле твоего короля…»",2)
    html_in("second",Param = False)
    html_in("Test",2)
