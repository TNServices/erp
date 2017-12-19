 ## Importation des modules
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
  
Fromadd = "matthieu.devalle@telecomnancy.net"
Toadd = "matthieu.devalle@telecomnancy.net"    ##  Spécification des destinataires
message = MIMEMultipart()    ## Création de l'objet "message"
message['From'] = Fromadd    ## Spécification de l'expéditeur
message['To'] = Toadd    ## Attache du destinataire à l'objet "message"
message['Subject'] = "SUJET DE VOTRE MAIL"    ## Spécification de l'objet de votre mail
msg = "VOTRE MESSAGE"    ## Message à envoyer
messageattach(MIMEText(msg.encode('utf-8'), 'plain', 'utf-8'))    ## Attache du message à l'objet "message", et encodage en UTF-8

nom_fichier = "db.sqlite3"    ## Spécification du nom de la pièce jointe
piece = open("", "rb")    ## Ouverture du fichier
part = MIMEBase('application', 'octet-stream')    ## Encodage de la pièce jointe en Base64
part.set_payload((piece).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "piece; filename= %s" % nom_fichier)
msg.attach(part)    ## Attache de la pièce jointe à l'objet "message" 

serveur = smtplib.SMTP('smtp.gmail.com', 587)    ## Connexion au serveur sortant (en précisant son nom et son port)
serveur.starttls()    ## Spécification de la sécurisation
serveur.login(Fromadd, "")    ## Authentification
texte= message.as_string().encode('utf-8')    ## Conversion de l'objet "message" en chaine de caractère et encodage en UTF-8
serveur.sendmail(Fromadd, Toadd, texte)    ## Envoi du mail
serveur.quit()    ## Déconnexion du serveur
