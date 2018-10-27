import webbrowser
def html_in(string_in_html, Check = 0, Param = True,file = open("Test_new.html","w")):
    if(Check == 0):
        file.writelines(fr'<br><font size = 6>{string_in_html}</font><br>')
    if(Check == 1):
        if Param:
            file.writelines(fr'<font size = 4>&#10004 {string_in_html}</font><br>')
        else:
            file.writelines(fr'<font size = 4>&#10008 {string_in_html}</font><br>')
    if (Check == 2):
        file.write(fr'<p style="margin-left: 40px"><font size = 2> -{string_in_html}</font><br></p>')
    
html_in("Список удаленных приложений")
html_in("first",1)
html_in("second",1,False)
html_in("Test",2)
html_in("first",1)
html_in("Слава тебе, безысходная боль! Умер вчера сероглазый король. Вечер осенний был душен и ал, Муж мой, вернувшись, спокойно сказал: «Знаешь, с охоты его принесли, Тело у старого дуба нашли. Жаль королеву. Такой молодой!.. За ночь одну она стала седой». Трубку свою на камине нашел И на работу ночную ушел. Дочку мою я сейчас разбужу, В серые глазки ее погляжу. А за окном шелестят тополя: «Нет на земле твоего короля…»",2)
webbrowser.open_new("Test_new.html")