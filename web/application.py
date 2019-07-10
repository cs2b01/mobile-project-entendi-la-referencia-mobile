from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time
import datetime
import random
from operator import  itemgetter,attrgetter



db = connector.Manager()
engine = db.createEngine()
cache = {} # Users cache
application=app = Flask(__name__)
app.secret_key = ".."


##############################################
#                                            #
#                   RENDER                   #
#                                            #
##############################################
@app.route('/')
def index():
    session['logged']=None
    session['category']=None
    session['category_question']=None
    return render_template('dologin.html')

@app.route('/dologin')
def dologin():
    return render_template('dologin.html')

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')


@app.route('/juego')
def juego():
    return render_template('juego.html')


@app.route('/main_menu')
def main_menu():
    return render_template('main_menu.html')


@app.route('/rankings')
def rankings():
    return render_template('rankings.html')

@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/subir_contenido')
def subir_contenido():
    return render_template('subir_contenido.html')
@app.route('/subir_pregunta')
def subir_pregunta():
    return render_template('subir_pregunta.html')


##############################################
#                                            #
#                   LOGIN                    #
#                                            #
##############################################

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    message = json.loads(request.data)
    email = message['email']
    password = message['password']
    db_session = db.getSession(engine)
    try:
        user = db_session.query(entities.User
            ).filter(entities.User.email == email
            ).filter(entities.User.password == password
            ).one()
        message = {'message': 'Authorized'}
        session['logged'] = user.id
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')


##############################################
#                                            #
#                LOGIN MOBILE                #
#                                            #
##############################################

@app.route('/authenticate_mb', methods = ['POST'])
def mobile_login():
    message = json.loads(request.data)
    email =    message['email']
    password = message['password']
    sessiondb = db.getSession(engine)
    try:
        user = sessiondb.query(entities.User
            ).filter(entities.User.email == email
            ).filter(entities.User.password == password
            ).one()
        if user != None:
            return Response(json.dumps({'message': "Authorized", "user_id": user.id, "username":user.username,"lastname":user.lastname,"name":user.name}, cls=connector.AlchemyEncoder),status=200, mimetype='application/json')
        else:
            return Response(json.dumps({'response': False}, cls=connector.AlchemyEncoder), status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        message = json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(message, status=401, mimetype='application/json')



@app.route('/user_mobile/<xid>', methods=['GET'])
def user_mobile(xid):
    sessiondb = db.getSession(engine)
    user = sessiondb.query(entities.User).filter(entities.User.id == xid).one()
    js = json.dumps({'user_id':user.id,'username':user.username,'name':user.name,'lastname':user.lastname,'email':user.email,'password':user.password,'uploads':user.uploads,'record':user.record}, cls=connector.AlchemyEncoder)
    return Response(js, status=200, mimetype='application/json')



@app.route('/current', methods=['GET'])
def current():
    sessiondb = db.getSession(engine)
    user = sessiondb.query(entities.User).filter(entities.User.id == session['logged']).first()
    js = json.dumps(user, cls=connector.AlchemyEncoder)
    return Response(js, status=200, mimetype='application/json')


##############################################
#                                            #
#                  REGISTER                  #
#                                            #
##############################################

@app.route('/users', methods = ['POST'])
def create_user():
    sessiondb = db.getSession(engine)
    c =  json.loads(request.data)
    data = []
    users=sessiondb.query(entities.User).filter(entities.User.email== c['email'])
    for user in users:
        data.append(user)
    if(len(data)==0):
        user = entities.User(
        username=c['username'],
        email=c['email'],
        name=c['name'],
        lastname=c['lastname'],
        password=c['password'],
        record=0,
        uploads=0)
        sessiondb.add(user)
        sessiondb.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    else:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')


##############################################
#                                            #
#    EDIT AND DELETE ACCOUNT IN SETTINGS     #
#                                            #
##############################################

@app.route('/users', methods = ['PUT'])
def update_user():
    time.sleep(1)
    sessiondb = db.getSession(engine)
    c =  json.loads(request.data)
    try:
        user = sessiondb.query(entities.User).filter(entities.User.id == session['logged']).first()
        for key in c.keys():
            setattr(user, key, c[key])
        sessiondb.add(user)
        sessiondb.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

@app.route('/users', methods = ['DELETE'])
def delete_user():
    session_db = db.getSession(engine)
    try:
        users = session_db.query(entities.User).filter(entities.User.id == session['logged'])
        for user in users:
            session_db.delete(user)
        session_db.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

##############################################
#                                            #
#                 Categories                 #
#                                            #
##############################################

#Solo ejecutar /create_categories si la base de datos se borra para fines de prueba

@app.route('/create_categories', methods = ['GET'])
def create_categories():
    db_session = db.getSession(engine)
    Marvel = entities.Category(name="Marvel")
    Star_Wars = entities.Category(name="Star Wars")
    Anime = entities.Category(name="Anime")
    Deportes = entities.Category(name="Deportes")
    Memes = entities.Category(name="Memes")
    db_session.add(Marvel)
    db_session.add(Star_Wars)
    db_session.add(Anime)
    db_session.add(Deportes)
    db_session.add(Memes)
    db_session.commit()
    return "Categories created!"


@app.route('/current_category', methods=['GET'])
def current_category():
    sessiondb = db.getSession(engine)
    category = sessiondb.query(entities.Category).filter(entities.Category.id == session['category']).first()
    js = json.dumps(category, cls=connector.AlchemyEncoder)
    return Response(js, status=200, mimetype='application/json')

@app.route('/set_category', methods = ['POST'])
def set_category():
    message = json.loads(request.data)
    id = message['id']
    db_session = db.getSession(engine)
    try:
        category = db_session.query(entities.Category
            ).filter(entities.Category.id == id
            ).one()
        message = {'message': 'Authorized'}
        session['category'] = category.id
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

##############################################
#                                            #
#                 Questions                  #
#                                            #
##############################################

@app.route('/questions', methods = ['POST'])
def create_question():
    sessiondb = db.getSession(engine)
    c =  json.loads(request.data)
    try:
        user = entities.Question(
        statment=c['statment'],
        answer=c['answer'],
        wrong1=c['wrong1'],
        wrong2=c['wrong2'],
        wrong3=c['wrong3'],
        category_id=c['category_id'])
        sessiondb.add(user)
        sessiondb.commit()
        message = {'message': 'Authorized'}
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')

@app.route('/questions', methods = ['GET'])
def get_questions():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Question)
    data = []
    for user in dbResponse:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

##############################################
#                                            #
#                 Rankings                   #
#                                            #
##############################################

@app.route('/rankings_uploads', methods = ['GET'])
def rankings_uploads():
    session = db.getSession(engine)
    users = session.query(entities.User)
    data = []
    for user in users:
        data.append(user)
    data=sorted(data,key=attrgetter('uploads'),reverse=True)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/rankings_record', methods = ['GET'])
def rankings_record():
    session = db.getSession(engine)
    users = session.query(entities.User)
    data = []
    for user in users:
        data.append(user)
    data=sorted(data,key=attrgetter('record'),reverse=True)
    message={'data':data}
    return Response(json.dumps(message, cls=connector.AlchemyEncoder), mimetype='application/json')

##############################################
#                                            #
#             Get Users w/Cache              #
#                                            #
##############################################

@app.route('/users', methods = ['GET'])
def get_users():
    key = 'getUsers'
    if key not in cache.keys():
        session = db.getSession(engine)
        dbResponse = session.query(entities.User)
        cache[key] = dbResponse
    users = cache[key]
    response = []
    for user in users:
        response.append(user)
    return json.dumps(response, cls=connector.AlchemyEncoder)


##############################################
#                                            #
#                    Game                    #
#                                            #
##############################################


@app.route('/set_category_and_random_question', methods = ['POST'])
def set_category_question():
    message = json.loads(request.data)
    id = message['id']
    db_session = db.getSession(engine)
    try:
        category = db_session.query(entities.Category
            ).filter(entities.Category.id == id
            ).one()
        category_id = category.id
        data = []
        categoryX=db_session.query(entities.Question).filter(entities.Question.category_id==category_id)
        for category in categoryX:
            data.append(category)
        randomx=random.choice(data)
        return Response(json.dumps(randomx, cls=connector.AlchemyEncoder), mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        return Response(message, status=401, mimetype='application/json')


##############################################
#                                            #
#                 FAKE USERS                 #
#                                            #
##############################################


@app.route('/create_fake_users', methods = ['GET'])
def create_test_users():
    db_session = db.getSession(engine)
    user1 = entities.User(username="Taco",email="j-quezada@utec.edu.pe",name="Javier",lastname="Quezada",password="1234",record=9,uploads=3)

    user2 = entities.User(
        username="Arno",
        email="arnold@utec.edu.pe",
        name="Arnol",
        lastname="Martinez",
        password="1234",
        record=11,
        uploads=3)

    user3 = entities.User(
        username="Tin",
        email="rod@utec.edu.pe",
        name="Rodrigo",
        lastname="Arriaga",
        password="1234",
        record=7,
        uploads=6)

    user4 = entities.User(
        username="Negro",
        email="pelacho@utec.edu.pe",
        name="Cesar",
        lastname="Mimbela",
        password="1234",
        record=9,
        uploads=0)

    user5 = entities.User(
        username="Kuro",
        email="adrianalonso@utec.edu.pe",
        name="Adrian",
        lastname="Perez",
        password="1234",
        record=6,
        uploads=4)

    user6 = entities.User(
        username="Darklay",
        email="dark07@utec.edu.pe",
        name="Nicolas",
        lastname="Figueroa",
        password="1234",
        record=15,
        uploads=6)

    user7 = entities.User(
        username="Majo",
        email="marijoseutec.edu.pe",
        name="Maria",
        lastname="Vilchez",
        password="1234",
        record=16,
        uploads=10)

    user8 = entities.User(
        username="Tito",
        email="h-tito@utec.edu.pe",
        name="Hector",
        lastname="Pozada",
        password="1234",
        record=7,
        uploads=11)

    user9 = entities.User(
        username="Chispa",
        email="fer78@utec.edu.pe",
        name="Fernando",
        lastname="Castaneda",
        password="1234",
        record=15,
        uploads=5)

    user10 = entities.User(
        username="Papo",
        email="pap@utec.edu.pe",
        name="Pedro",
        lastname="Calderon",
        password="1234",
        record=13,
        uploads=3)

    user11 = entities.User(
        username="Chairi",
        email="die159@utec.edu.pe",
        name="Diego",
        lastname="Chiri",
        password="1234",
        record=10,
        uploads=2)

    user12 = entities.User(
        username="Drogo",
        email="richy@utec.edu.pe",
        name="Ricardo",
        lastname="Jara",
        password="1234",
        record=5,
        uploads=5)

    user13 = entities.User(
        username="Mafer",
        email="mllontopd@utec.edu.pe",
        name="Mafer",
        lastname="Llontop",
        password="1234",
        record=7,
        uploads=9)

    user14 = entities.User(
        username="kike",
        email="parades@utec.edu.pe",
        name="Enrique",
        lastname="Paredes",
        password="1234",
        record=11,
        uploads=6)

    user15 = entities.User(
        username="Pelado",
        email="paulmim@utec.edu.pe",
        name="Paul",
        lastname="Mimbela",
        password="1234",
        record=13,
        uploads=7)

    db_session.add(user1)
    db_session.add(user2)
    db_session.add(user3)
    db_session.add(user4)
    db_session.add(user5)
    db_session.add(user6)
    db_session.add(user7)
    db_session.add(user8)
    db_session.add(user9)
    db_session.add(user10)
    db_session.add(user11)
    db_session.add(user12)
    db_session.add(user13)
    db_session.add(user14)
    db_session.add(user15)
    db_session.commit()
    return "Usuarios creados!"

##############################################
#                                            #
#               FAKE QUESTIONS               #
#                                            #
##############################################


@app.route('/create_fake_questions', methods=['GET'])
def create_fake_questions():
       db_session = db.getSession(engine)
       m1 = entities.Question(
           statment="¿Cuantas veces se creyó que murió Loki?",
           answer="2",
           wrong1="3",
           wrong2="4",
           wrong3="5",
           category_id=1)
       db_session.add(m1)

       m2 = entities.Question(
           statment="¿Cuántos eran los finales que vio Dr Strange",
           answer="14000605",
           wrong1="14215125",
           wrong2="14212785",
           wrong3="15215211",
           category_id=1)
       db_session.add(m2)

       m3 = entities.Question(
           statment="¿En que película se introdujo a Black Widow?",
           answer="Iron Man",
           wrong1="Iron Man 2",
           wrong2="Avengers",
           wrong3="Capitan America",
           category_id=1)
       db_session.add(m3)

       m4 = entities.Question(
           statment="¿Cual de los siguientes no es parte de la primera fase del UCM",
           answer="Doctor Strange",
           wrong1="Hawkeye",
           wrong2="Maquina de guerra",
           wrong3="Black Widow",
           category_id=1)
       db_session.add(m4)

       m5 = entities.Question(
           statment="¿Primero en morir en infinity war?",
           answer="Heimdall",
           wrong1="Loki",
           wrong2="The Collector",
           wrong3="Gamora",
           category_id=1)
       db_session.add(m5)

       m6 = entities.Question(
           statment="¿En que película aparece por primera vez el Tesseract?",
           answer="Thor",
           wrong1="Iron Man",
           wrong2="Capitan America",
           wrong3="Avengers",
           category_id=1)
       db_session.add(m6)

       m7 = entities.Question(
           statment="¿Primera aparicion de Hawkeye?",
           answer="Thor",
           wrong1="Capitan America",
           wrong2="Iron man",
           wrong3="Avengers",
           category_id=1)
       db_session.add(m7)

       m8 = entities.Question(
           statment="¿Villano con mas tiempo en los comics",
           answer="Doctor Octopus",
           wrong1="Loki",
           wrong2="Dr Doom",
           wrong3="Magneto",
           category_id=1)
       db_session.add(m8)

       m9 = entities.Question(
           statment="¿Primer Xmen en volverse un vengador?",
           answer="Bestia",
           wrong1="Wolverine",
           wrong2="Tormenta",
           wrong3="Ciclope",
           category_id=1)
       db_session.add(m9)

       m10 = entities.Question(
           statment="¿Nombre de la raza de Venom?",
           answer="Klyntar",
           wrong1="Brood",
           wrong2="Badoon",
           wrong3="Shiar",
           category_id=1)
       db_session.add(m10)

       m11 = entities.Question(
           statment="¿Como se llama el pet de Falcon",
           answer="Redwing",
           wrong1="Blackwing",
           wrong2="Junior",
           wrong3="America",
           category_id=1)
       db_session.add(m11)

       m12 = entities.Question(
           statment="¿Quien mato a Steve Rogers luego de Civil War 1?",
           answer="Sharon Carter",
           wrong1="Iron man",
           wrong2="Winter Soldier",
           wrong3="Croosbones",
           category_id=1)
       db_session.add(m12)

       m13 = entities.Question(
           statment="¿Como se iba a llamar originalmente Luke Skywalker?",
           answer="Luke Starkiller",
           wrong1="Luke Skykiller",
           wrong2="Luke Sunkiller",
           wrong3="Luke Starwalker",
           category_id=2)
       db_session.add(m13)

       m14 = entities.Question(
           statment="¿Cómo consiguió Han Solo el halcón milenario que había pertenecido a Lando Calrissian?",
           answer="En un juego de Sabacc",
           wrong1="La robó",
           wrong2="En un juego de Dejarik",
           wrong3="En un duelo",
           category_id=2)
       db_session.add(m14)

       m15 = entities.Question(
           statment="¿Quién se esconde detrás de Darth Vader?",
           answer="Anakin Skywalker",
           wrong1="Obi-wan Kenobi",
           wrong2="Han Solo",
           wrong3="Luke Starwalker",
           category_id=2)
       db_session.add(m15)

       m16 = entities.Question(
           statment="¿de que color es el sable de luz de Mace Windu?",
           answer="Violeta",
           wrong1="Verde",
           wrong2="Azul",
           wrong3="Rojo",
           category_id=2)
       db_session.add(m16)

       m17 = entities.Question(
           statment="¿Cuantos actores han interpretado a Anakin Skywalker?",
           answer="6",
           wrong1="5",
           wrong2="4",
           wrong3="3",
           category_id=2)
       db_session.add(m17)

       m18 = entities.Question(
           statment="¿Como se llamaba el dueno de Anakin Skywalker cuando era esclavo?",
           answer="Watto",
           wrong1="Shaak Ti",
           wrong2="Blomer",
           wrong3="Flaur",
           category_id=2)
       db_session.add(m18)

       m19 = entities.Question(
           statment="¿Como se llamaba Anakin en las carreras de pods?",
           answer="Sebulba",
           wrong1="Barne",
           wrong2="Shimi",
           wrong3="Hango",
           category_id=2)
       db_session.add(m19)

       m20 = entities.Question(
           statment="¿Raza de Darth Maul?",
           answer="Zabrak",
           wrong1="Talu",
           wrong2="Ragnarok",
           wrong3="Wookie",
           category_id=2)
       db_session.add(m20)

       m21 = entities.Question(
           statment="¿Quién dijo la frase Es una trampa?",
           answer="Almirante Ackbar",
           wrong1="Han Solo",
           wrong2="Bant Eerin",
           wrong3="Greedo",
           category_id=2)
       db_session.add(m21)

       m22 = entities.Question(
           statment="¿En que planeta vive Jabba El Hutt?",
           answer="Tatooine",
           wrong1="Alderan",
           wrong2="Bespin",
           wrong3="Coruscant",
           category_id=2)
       db_session.add(m22)

       m23 = entities.Question(
           statment="¿En dónde conocieron Obi-Wan y Luke a Han Solo y Chewbacca?",
           answer="Cantina de Chalmun",
           wrong1="Cantina de Gundark",
           wrong2="Bar de Elgerkab",
           wrong3="Javyars Dinner",
           category_id=2)
       db_session.add(m23)

       m24 = entities.Question(
           statment="¿Batalla en la que se destruye la primera estrella de la muerte?",
           answer="Yavin",
           wrong1="Hoth",
           wrong2="Geonosis",
           wrong3="Utapau",
           category_id=2)
       db_session.add(m24)

       m25 = entities.Question(
           statment="¿Nombre de la protagonista femenida de Elfen Lied?",
           answer="Lucy",
           wrong1="Akane",
           wrong2="Elfen",
           wrong3="Niu",
           category_id=3)
       db_session.add(m25)

       m26 = entities.Question(
           statment="¿Nombre del protagonista de Fairy Tail?",
           answer="Natsu",
           wrong1="Gray",
           wrong2="Igneel",
           wrong3="Luffy",
           category_id=3)
       db_session.add(m26)

       m27 = entities.Question(
           statment="¿Personaje principal de School Days?",
           answer="Makoto",
           wrong1="Sekai",
           wrong2="Katsura",
           wrong3="Inutasha",
           category_id=3)
       db_session.add(m27)

       m28 = entities.Question(
           statment="¿Anime de Shiro y Sora?",
           answer="No game No life",
           wrong1="Elfen Lied",
           wrong2="Death Note",
           wrong3="Shigatsu Wa Kimi No Uso",
           category_id=3)
       db_session.add(m28)

       m29 = entities.Question(
           statment="¿Personaje que hace el Chidori?",
           answer="Sasuke",
           wrong1="Naruto",
           wrong2="Luffy",
           wrong3="Goku",
           category_id=3)
       db_session.add(m29)

       m30 = entities.Question(
           statment="¿Ataque que solo puede hacer Goku en DBZ",
           answer="Puno del dragon",
           wrong1="Genkidama",
           wrong2="Kamekameha",
           wrong3="Teletransportacion",
           category_id=3)
       db_session.add(m30)

       m31 = entities.Question(
           statment="¿Personajes de SAO",
           answer="Kirito y Asuna",
           wrong1="Inuyasha y Kagome",
           wrong2="Naruto y Hitana",
           wrong3="Sasuke y Sakura",
           category_id=3)
       db_session.add(m31)

       m32 = entities.Question(
           statment="¿Nombre del protagonista de Fairy Tail",
           answer="Natsu",
           wrong1="Gray",
           wrong2="Igneel",
           wrong3="Luffy",
           category_id=3)
       db_session.add(m32)

       m33 = entities.Question(
           statment="¿Que le sucedio a la espalda de hawkeye (FMA)",
           answer="Se la quemo Mustang",
           wrong1="Tuvo un accidente",
           wrong2="Herida de guerra",
           wrong3="Se lastimo asi misma",
           category_id=3)
       db_session.add(m33)

       m34 = entities.Question(
           statment="¿Primera victima en Death Note?",
           answer="Un agresor",
           wrong1="Politico corrupto",
           wrong2="Motociclista",
           wrong3="Abusivo",
           category_id=3)
       db_session.add(m34)

       m35 = entities.Question(
           statment="Mundiales jugados por Peru",
           answer="5",
           wrong1="1",
           wrong2="6",
           wrong3="3",
           category_id=4)
       db_session.add(m35)

       m36 = entities.Question(
           statment="¿Maximo goleador Euro 2016",
           answer="Griezman",
           wrong1="Cristiano",
           wrong2="Mbappe",
           wrong3="Lewandoski",
           category_id=4)
       db_session.add(m36)

       m37 = entities.Question(
           statment="¿Expulsado en la final del Mundial 2006",
           answer="Zidane",
           wrong1="Henry",
           wrong2="Vieira",
           wrong3="Makelele",
           category_id=4)
       db_session.add(m37)

       m38 = entities.Question(
           statment="¿Hat-trick semifinales Champions 2018/1019?",
           answer="Moura",
           wrong1="Messi",
           wrong2="Wijnaldum",
           wrong3="Ziyech",
           category_id=4)
       db_session.add(m38)

       m39 = entities.Question(
           statment="¿Arquero mas caro de la historia",
           answer="Arrizabalaga",
           wrong1="Buffon",
           wrong2="Neuer",
           wrong3="Becker",
           category_id=4)
       db_session.add(m39)

       m40 = entities.Question(
           statment="¿Defensa mas caro de la historia?",
           answer="Van Dijk",
           wrong1="Ramos",
           wrong2="Pavard",
           wrong3="Laporte",
           category_id=4)
       db_session.add(m40)

       m41 = entities.Question(
           statment="¿Puntos de Alianza en la libertadores 2019",
           answer="1",
           wrong1="0",
           wrong2="2",
           wrong3="4",
           category_id=4)
       db_session.add(m41)

       m42 = entities.Question(
           statment="¿Division del Juan Aurich",
           answer="Segunda",
           wrong1="Primera",
           wrong2="Tercera",
           wrong3="No existe",
           category_id=4)
       db_session.add(m42)

       m43 = entities.Question(
           statment="¿Poker en las semifinales 2012/2013 Champions League",
           answer="Lewandoski",
           wrong1="Ronaldo",
           wrong2="Messi",
           wrong3="Benzema",
           category_id=4)
       db_session.add(m43)

       m44 = entities.Question(
           statment="¿Mundial de clubes 2012 campeon?",
           answer="Corinthians",
           wrong1="Chealsea",
           wrong2="Barcelona",
           wrong3="Boca",
           category_id=4)
       db_session.add(m44)

       m45 = entities.Question(
           statment="Fue parte de la seleccion peruana del mundial de 1970",
           answer="Pedro Leon",
           wrong1="Cueto",
           wrong2="Ninguna",
           wrong3="Ambos",
           category_id=4)
       db_session.add(m45)

       m46 = entities.Question(
           statment="Estupida mi _____ , idiota",
           answer="Pelo",
           wrong1="Cabello",
           wrong2="Ropa",
           wrong3="Celular",
           category_id=5)
       db_session.add(m46)

       m47 = entities.Question(
           statment="No se quien eres, ...",
           answer="Pero te encontrare",
           wrong1="Pero lo hare",
           wrong2="Pero te matare",
           wrong3="Pero dimelo",
           category_id=5)
       db_session.add(m47)

       m48 = entities.Question(
           statment="Meme de la pelicula Proyecto X",
           answer="A eso se le llama estrategia",
           wrong1="Vamonos alv wey",
           wrong2="Eso duele no?",
           wrong3="El que no arriesga no gana",
           category_id=5)
       db_session.add(m48)

       m49 = entities.Question(
           statment="¿Nombre del protagonista de Fairy Tail",
           answer="Natsu",
           wrong1="Gray",
           wrong2="Igneel",
           wrong3="Luffy",
           category_id=5)
       db_session.add(m49)

       m50 = entities.Question(
           statment="Meme en el que sale peter parker",
           answer="Con que derecho lo dices tu",
           wrong1="No es tan facil",
           wrong2="Parker fotografia",
           wrong3="Inteligente no?",
           category_id=5)
       db_session.add(m50)

       m51 = entities.Question(
           statment="Meme que no viene de un dibujo animado",
           answer="Ja, novatos",
           wrong1="Un clasico",
           wrong2="Es una excelente pregunta",
           wrong3="El macho",
           category_id=5)
       db_session.add(m51)

       m52 = entities.Question(
           statment="Serie de donde proviene el meme Ese no es asunto mio",
           answer="Drake y Josh",
           wrong1="Zoe 101",
           wrong2="Los padrinos magicos",
           wrong3="Kendal y ken",
           category_id=5)
       db_session.add(m52)

       m53 = entities.Question(
           statment="Pelicula de adios vaquero",
           answer="Cowboys",
           wrong1="Toy story",
           wrong2="Ralph",
           wrong3="Mi villano favorito",
           category_id=5)
       db_session.add(m53)

       m54 = entities.Question(
           statment="¿Pelicula o serie que on tiene un meme?",
           answer="Spiderman Homecoming",
           wrong1="Avengers",
           wrong2="Tom y jerry",
           wrong3="Backyardigans",
           category_id=5)
       db_session.add(m54)

       m55 = entities.Question(
           statment="Saga de spiderman sin meme",
           answer="Primera trilogia",
           wrong1="Las de Andrew",
           wrong2="La del mcu",
           wrong3="Spiderverse",
           category_id=5)
       db_session.add(m55)
       db_session.commit()
       return "Preguntas creados!"


##############################################
#                                            #
#               POST QUESTION                #
#                                            #
##############################################


@app.route('/questions_mobile/<id>', methods = ['POST'])
def create_question_mobile(id):
    sessiondb = db.getSession(engine)
    c =  json.loads(request.data)
    try:
        question = entities.Question(
        statment=c['statment'],
        answer=c['answer'],
        wrong1=c['wrong1'],
        wrong2=c['wrong2'],
        wrong3=c['wrong3'],
        category_id=id)
        sessiondb.add(question)
        sessiondb.commit()
        message = {'message': 'Authorized'}
        message=json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        message=json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(message, status=401, mimetype='application/json')


@app.route('/subir_upload/<id>', methods = ['PUT'])
def subir_upload(id):
    sessiondb = db.getSession(engine)
    try:
        user = sessiondb.query(entities.User).filter(entities.User.id == id).first()
        setattr(user,'uploads',(user.uploads+1))
        sessiondb.add(user)
        sessiondb.commit()
        message = {'message': 'Authorized'}
        message=json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(message, status=200, mimetype='application/json')
    except Exception:
        message = {'message': 'Unauthorized'}
        message=json.dumps(message, cls=connector.AlchemyEncoder)
        return Response(message, status=401, mimetype='application/json')

@app.route('/categories', methods = ['GET'])
def get_categories():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Category)
    data = []
    for category in dbResponse:
        data.append(category)
    data=sorted(data,key=attrgetter('id'),reverse=False)
    message={'data':data}
    return Response(json.dumps(message, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/questions_by_category/<id>', methods = ['GET'])
def get_questions_by_category(id):
    session = db.getSession(engine)
    messages = session.query(entities.Question).filter(
            entities.Question.category_id== id)
    data = []
    for message in messages:
        data.append(message)
    message={'data':data}
    return Response(json.dumps(message, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/get_question_by_id/<id>', methods = ['GET'])
def get_question_by_category(id):
    session = db.getSession(engine)
    question = session.query(entities.Question).filter(entities.Question.id == id).one()
    js = json.dumps({'statment':question.statment,'answer':question.answer}, cls=connector.AlchemyEncoder)
    return Response(js, status=200, mimetype='application/json')



##############################################
#                                            #
#                   Run                      #
#                                            #
##############################################

if __name__ == '__main__':
    app.run()
