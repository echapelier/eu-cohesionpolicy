# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objects as go

graph_fontstyle = dict(family="Arial, sans-serif",
                        size=14)

app = dash.Dash(__name__)

server = app.server

dtype_colonnes = {
    'Région (pre-NOTRe)': str,
    'Catégorie de région': str,
    'Intitulé du projet': str,
    'Nom du bénéficiaire': str,
    'Instrument financier ?': bool,
    "Catégorie d'instrument financier": str,
    'Code postal du bénéficaire': str,
    "Code postal de l'opération": str,
    'Zone': str,
    "Département de l'opération": str,
    "Région de l'opération": str,
    'Fonds': str,
    'Montant UE programmé': float,
    'Total des dépenses éligibles': float,
    'Taux de cofinancement': float,
    'Durée, en mois': int,
    'Montant UE par mois': float,
    'Total éligible par mois': float,
    'catbeneficiaire': str,
    'themeprojet': str,
    'Palier': str
}

data = pd.read_csv('france-2014-2020-feder-fse.csv', dtype=dtype_colonnes, parse_dates=["Date de début de l'opération", "Date de fin de l'opération"])

data_pivot = pd.pivot_table(data, values='Montant UE programmé', index='themeprojet', columns='catbeneficiaire', aggfunc=np.sum).fillna(0)
ordre_themeprojet = ['Indéterminé', 'Insertion', 'Emploi', 'Formation', 'Subventions de fonctionnement des entreprises<br>(compensation de surcoûts)', 'Financement des entreprises', 'Investissements des entreprises', 'Recherche et innovation', 'Haut débit et très haut débit', 'Transport', 'Logement', 'Énergie', 'Environnement', 'Infrastructures sportives, culturelles et éducatives', 'Gestion administrative<br>(assistance technique)']
ordre_catbeneficiaires = ['Associations', 'Autres établissements publics', "Chambres consulaires et groupements d'entreprises", 'Communes', 'Départements', 'Entreprises', 'Formation continue et enseignement hors supérieur', 'État', 'Logement social', 'Missions locales emploi et insertion', "Organismes de soutien à l'entrepreneuriat", 'Régions', "Établissements de recherche et d'enseignement supérieur", 'Bénéficiaires de type indéterminé']
data_pivot = data_pivot.reindex(index=ordre_themeprojet, columns=ordre_catbeneficiaires, copy=False)

partie1_md = '''
    ## 1. Introduction

    L’ouverture de la nouvelle période de programmation des fonds européens 2021-2027 est un moment propice au bilan de la précédente période 2014-2020, et notamment de l’emploi des deux instruments de financement de la politique régionale de l’Union européenne que constituent le Fonds européen de développement régional (FEDER) et le Fonds social européen (FSE).

    Cette politique régionale vise à accroître la cohésion économique, sociale et territoriale entre régions européennes – c’est pourquoi elle est aussi appelée politique de cohésion – et à réduire leurs écarts de développement. Elle se décline en programmes opérationnels régionaux, interrégionaux et nationaux articulés autour de priorités d’investissement définies sur sept ans pour chaque territoire. Ces priorités se répartissent selon des axes thématiques et elles définissent les conditions d’éligibilité des opérations.

    La sélection des projets fait également intervenir des variables telles que la taille, la durée des projets, le montant d’aide ou le type de porteur de projet. La présente analyse des opérations cofinancées par le FEDER et le FSE en France au cours de la période 2014-2020 propose donc de répondre aux questions suivantes :
    - Quel est le profil des opérations soutenues et quel niveau d’aide reçoivent-elles ?
    - Qui sont les bénéficiaires des fonds et comment se répartissent-ils ?
    - Observe-t-on des différences entre régions dans la mise en œuvre des fonds ?
    - Comment s’articulent le cycle de programmation de sept ans et le calendrier de réalisation des opérations ?
    
    En procédant à l’analyse de données agrégées plutôt que par programme et par axe thématique, cette rétrospective offre aux gestionnaires, bénéficiaires et praticiens des fonds européens un éclairage renouvelé sur l’utilisation du FEDER et du FSE en France.
'''

partie2_md_a = '''
    La distribution des opérations en fonction des montants d’aides européennes reçues fait apparaître deux catégories de projets :

    - d’une part des projets **« courants »**, qui représentent 90% des opérations FEDER et FSE et représentent 30% des montants programmés ; 
    - d’autre part des projets **« d’ampleur »**, beaucoup moins nombreux (10% des opérations) mais qui absorbent la grande majorité des ressources (70% des fonds FEDER et FSE).
'''

partie2_md_b = '''
    Dans le cas du FSE, le seuil d’entrée dans la catégorie des projets « d’ampleur » (séparant les neuvième et dixième déciles) se situe à 326 000 euros tandis qu’il se situe à 700 000 euros pour le FEDER. En effet, les opérations FSE, qui sont liées à l’emploi, la formation et l’inclusion, tendent à être plus courtes (64% des projets durent moins d’un an) et affichent un coût total moyen de 447 000 euros ainsi qu’un niveau de cofinancement européen de 53%. En revanche, les opérations FEDER, généralement liées aux infrastructures et équipements, ont des durées plus longues (54% des projets durent deux à trois ans) et un coût plus élevé (960 000 euros en moyenne) tout en présentant un taux de cofinancement plus faible (40% en moyenne).
'''

partie3_md = '''
    ## 3. Vue d’ensemble des bénéficiaires
    
    Alors que les opérations FSE se concentrent sur trois thématiques (emploi, formation et inclusion) et associent des catégories variées de porteurs de projet, le FEDER cible des domaines plus nombreux mais bénéficie d’abord aux collectivités territoriales et aux établissements publics.

    Les opérations cofinancées par le FSE dans les domaines de l’emploi et de l’insertion font intervenir une gamme diversifiée d’acteurs : établissements publics, associations, départements, missions emploi et insertion, État et régions. Elles se distinguent du domaine de la formation où 90% des montants sont mobilisés par les régions, l’État ainsi que les établissements d'enseignement et organismes de formation.

    Concernant le FEDER, 74% des cofinancements viennent soutenir les actions des collectivités territoriales (régions, départements et secteur communal) ainsi que celles des établissements publics, y compris les établissements de recherche et d’enseignement supérieur.
'''

partie4_md = '''
    ## 4. Qui sont les porteurs de projets « courants » et de projets « d’ampleur » ?

    Les opérations bénéficiant d’une contribution du FSE inférieure à 326 000 euros (projets « courants ») sont le plus souvent portées par des associations, le secteur communal (dont les CCAS) et les missions emploi et insertion (missions locales, PLIE, maisons de l’emploi etc.). En revanche, les projets « d’ampleur » sont d’abord portés par les établissements d’enseignement et organismes de formation suivis par les régions et Pôle Emploi.

    Les organismes de formation sont également de nature différente suivant le profil des opérations : il s’agit principalement des GRETA, CFA et GIP de formation pour les projets « courants » et des OPCA de formation professionnelle pour les projets « d’ampleur ».

    Concernant le FEDER, la catégorie des projets « d’ampleur » (avec une contribution européenne supérieure à 700 000 euros) révèle une plus forte présence des collectivités territoriales et de leurs groupements : secteur communal (communes, intercommunalités, syndicats mixtes), départements et régions pour les actions d’aménagement du territoire.
'''

partie5_md = '''
    ## 5. État et collectivités territoriales : des actions complémentaires ?

    **La nature des interventions des collectivités territoriales et de l’État, qui représentant 41% des montants programmés, suggère une complémentarité entre leurs actions. Cette complémentarité est d’ordre géographique pour les actions de formation mobilisant le FSE, entre mise en œuvre nationale, régionale ou infrarégionale, et thématique dans le cadre du FEDER.**

    Le financement de la formation apparaît comme une priorité centrale des régions et de l’État, principales autorités de gestion des programmes opérationnels. Les régions mettent ainsi très largement en œuvre les opérations FSE dans ce domaine, essentiellement au titre des mesures liées à l'apprentissage tout au long de la vie prévues par les programmes opérationnels régionaux.

    Parmi les opérations conduites par l’État, sont présentes les mesures liées à l’emploi et à la formation financées dans le cadre du programme opérationnel national « Initiative pour l’Emploi des Jeunes » ainsi que les mesures d’assistance technique liées à la gestion du programme opérationnel national FSE.

    Si les départements et les communes font usage du FSE à des niveaux équivalents pour leurs politiques d’accompagnement à l’emploi et d’inclusion active, c’est sur les investissements en infrastructures que leurs domaines d’intervention se distinguent. Les communes ont en effet largement recours aux cofinancements FEDER en matière de transport urbain, d’infrastructures multimodales et d’environnement tandis que les départements mobilisent davantage ce fonds pour la rénovation thermique des bâtiments et l’aménagement numérique.
'''

partie5_md_focus_assos = '''
    ### Focus : les associations

    Les structures associatives jouent un rôle de premier plan dans les actions dédiées à l’inclusion active cofinancées par le FSE, notamment en faveur de l’intégration des jeunes et des personnes éloignées de l’emploi. Elles sont également présentes, à un degré moindre, dans les actions de protection de l’environnement et de la biodiversité ainsi que dans la réalisation d’infrastructures vertes.
'''

partie5_md_focus_entreprises = '''
    ### Focus : le soutien à l’investissement des entreprises

    Tous axes programmatiques confondus, le soutien à l’investissement des entreprises, qui représente 11% des cofinancements FEDER hors instruments financiers, porte majoritairement sur les investissements génériques des PME (outil de production, bâtiments, et dans une moindre mesure adaptation des processus de production) et la production de biomasse-énergie (unités de méthanisation, chaufferies bois).
'''

partie6_md = '''
    ## 6. Quelles particularités outre-mer ?

    **Selon qu’elles soient conduites outre-mer ou en métropole, les actions de renforcement de la cohésion économique, sociale et territoriale soutenues par le FEDER et le FSE présentent des différences qui se traduisent notamment par le cofinancement d’acteurs différents.**

    Dans les cinq régions et départements d’outre-mer, régions dites « moins développées », l’État et les établissements publics portent une part significative des cofinancements européens (respectivement 8 et 10%, contre 0 et 3% en métropole). Dans le cas de l’État, il s’agit d’une part des mesures d’assistance technique à la gestion des fonds européens, et de l’autre des actions relatives au Service militaire adapté (SMA), un dispositif d’insertion destiné aux jeunes. De leur côté, les établissements publics mettent en œuvre des mesures relatives à l’emploi et à l’inclusion de plus grande ampleur qu’en métropole, ainsi que d’importantes opérations d’aménagement concernant notamment les infrastructures portuaires et le logement.
    
    Les entreprises en outre-mer bénéficient également de davantage de financements européens, en raison de l’existence de mesures de compensation des surcoûts de l’ultrapériphéricité. En revanche, les conseils régionaux et établissements d’enseignement supérieur et de recherche occupent une place moindre que dans les régions métropolitaines dites « en transition » et « plus développées ».
'''

partie7_md = '''
    ## 7. Des stratégies d’emploi des fonds différentes selon les régions

    Les stratégies de sélection des opérations par les Conseils régionaux, autorités de gestion de la plupart des programmes opérationnels, se sont traduites par un ciblage des investissements qui a pu bénéficier à certaines catégories de bénéficiaires.

    Ainsi, deux régions se distinguent par une concentration relativement élevée des fonds : l’Île-de-France, où le Conseil régional reçoit près de la moitié des cofinancements et notamment pour la mise en place d’instruments financiers, et la Bretagne, où les établissements de recherche et d’enseignement supérieur portent une large part (47%) des projets « courants » tandis que le FSE y a été mis en œuvre par des contrats de formation professionnelle de grande ampleur.

    Ce schéma se retrouve pour les régions présentant une concentration plutôt élevée des fonds, due soit aux opérations effectuées par le Conseil régional (Alsace, Haute-Normandie, Limousin, Picardie, Provence-Alpes-Côte d’Azur), soit à la présence plus forte d’une certaine catégorie de porteurs de projets « courants » (le secteur communal en Corse, les entreprises en Martinique).
'''

partie8_md = '''
    ## 8. Les opérations de très grande envergure

    Hors instruments financiers, une centaine d’opérations présentent une contribution européenne supérieure à 10 millions d’euros. Elles représentent 0,3% des opérations mais 19,4% des contributions FEDER et FSE.

    Sont concernés en premier lieu les contrats de formation professionnelle portés par les Conseils régionaux et, dans une moindre mesure, certains organismes de formation et d’accompagnement des jeunes. Viennent ensuite les opérations relatives à l’emploi avec la mise en place de la Garantie Jeunes, les dispositifs d’accompagnement de Pôle Emploi et les aides à la mobilité.
    
    Les opérations en matière de transport (Nouvelle Route du Littoral à la Réunion, transports en commun en site propre) et d’aménagement numérique (création de réseaux très haut débit) ont également mobilisé d’importants financements FEDER par opération.
'''

partie9_md = '''
    ## 9. Les instruments financiers

    **Une partie des financements FEDER ont été alloués à la mise en place d’une soixantaine d’instruments financiers, c’est-à-dire des dispositifs d’aides remboursables représentant un total de plus de 354 millions d’euros.**

    Ces instruments sont principalement à destination des PME, et notamment des entreprises en création et/ou innovantes. Ils comprennent des instruments de participation (intervention en fonds propres et quasi-fonds propres), de prêt et de garantie, ainsi que des dotations à des fonds de fonds permettant d’abonder plusieurs instruments financiers. Ils sont essentiellement gérés par les Conseils régionaux (73%) et BPI France (18%).
'''

partie10_md = '''
    ## 10. Le rythme de mise en œuvre

    **La réalisation des opérations a connu une montée en puissance progressive avec un pic des contributions européennes à la mi-parcours, c’est-à-dire fin 2017.**

    Cependant, les opérations FEDER et FSE ont suivi deux tendances distinctes : après une brusque augmentation des contributions européennes en 2015, le FSE a conservé de 2016 à 2019 un rythme stable de réalisation des opérations ; la réalisation des opérations FEDER a quant à elle connu une croissance sensible et régulière jusqu’en 2017, avant de se stabiliser en 2018 et 2019. Plus de la moitié (55%) des opérations FEDER et FSE ont démarré avant la fin 2016 et 89% avant la fin 2018, avec un pic de mise en œuvre en 2017. Ce pic a été suivi d’un rapide recul de la mise en œuvre des opérations de courte durée, en majorité cofinancées par le FSE (dès 2016 pour les opérations de moins de 24 mois et à partir de 2017 pour les opérations de moins de 12 mois).
'''

partie11_md = '''
    ## 11. Note méthodologique

    L’analyse repose sur les données relatives à 38 532 opérations menées dans le cadre de 38 Programmes opérationnels FEDER, FSE et IEJ 2014-2020. Elles ont été extraites le 01/12/2020 et sont issues des listes d’opérations programmées publiées au 29/07/2020 par l’Agence nationale de la cohésion des territoires (16 411 opérations), au 01/12/2020 par la Région Nouvelle-Aquitaine (2 292 opérations), au 06/07/2020 par la Région Normandie (864 opérations), au 30/06/2020 par la Région Bretagne (529 opérations) et au 30/07/2020 par la Délégation générale à l’emploi et à la formation professionnelle (18 436 opérations). Ne sont donc pas incluses les opérations cofinancées au titre des programmes de coopération territoriale européenne (INTERREG). Les montants considérés représentent 83,2% des fonds FEDER et FSE-IEJ alloués à la France pour 2014-2020, la période de programmation n’étant pas clôturée à la date de l’analyse et les jeux de données publiés d’ayant donc pas un caractère définitif.
'''

apropos_md = '''
    ## À propos

    Auteurs : [Elie HERBERICHS](eherberichs@novi-advisory.eu) et [Romain SU](https://romain.su) 
'''

lignes_feder = np.arange(1, data.loc[data['Fonds'] == 'FEDER', 'Montant UE programmé'].count())
lignes_fse = np.arange(1, data.loc[data['Fonds'] == 'FSE', 'Montant UE programmé'].count())
feder_normalises = (lignes_feder - lignes_feder.min()) / (lignes_feder.max() - lignes_feder.min()) 
fse_normalises = (lignes_fse - lignes_fse.min()) / (lignes_fse.max() - lignes_fse.min())

montants_feder = np.cumsum(data.loc[data['Fonds'] == 'FEDER', 'Montant UE programmé'].sort_values())
montants_fse = np.cumsum(data.loc[data['Fonds'] == 'FSE', 'Montant UE programmé'].sort_values())
montants_feder_normalises = (montants_feder - montants_feder.min()) / (montants_feder.max() - montants_feder.min()) 
montants_fse_normalises = (montants_fse - montants_fse.min()) / (montants_fse.max() - montants_fse.min()) 

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=feder_normalises, y=montants_feder_normalises, name='FEDER', hoverinfo='none'))
fig1.add_trace(go.Scatter(x=fse_normalises, y=montants_fse_normalises, name='FSE', hoverinfo='none'))
fig1.update_layout(xaxis = dict(
                                title_text = "Nombre d'opérations",
                                tickmode = 'array',
                                tickvals = np.arange(0.1, 1, 0.1),
                                tickformat = '%'
                                ),
                    yaxis = dict(
                                title_text = 'Montants UE programmés',
                                tickmode = 'array',
                                tickvals = np.arange(0.1, 1, 0.1),
                                tickformat = '%'
                                ),
                    margin = dict(l=0, r=0, t=0, b=70),
                    legend = dict(orientation="h", yanchor="top", y=1, xanchor="left", x=0.25),
                    dragmode=False
                    )

data_pivot_sansindetermine = data_pivot.drop(index=['Indéterminé'])

fig2 = go.Figure(layout = dict(
                               polar = dict(
                                   radialaxis = dict(
                                       visible = True,
                                       showticklabels = True,
                                       tickvals = [500000000, 1000000000, 1500000000],
                                       ticktext = ['500 mln €', '1 md €', '1,5 md €']
                                   ),
                                   angularaxis = dict(
                                       tickmode = "array",
                                       tickvals = [x*(360/len(data_pivot_sansindetermine.index)) for x in range(0, len(data_pivot_sansindetermine.index))],
                                       ticktext = data_pivot_sansindetermine.index
                                   )),
                               showlegend = True,
                               autosize = True
                               ))

for catbeneficiaire in data_pivot_sansindetermine.columns:
    fig2.add_trace(go.Barpolar(r=data_pivot_sansindetermine[catbeneficiaire],
                               name=catbeneficiaire,
                               hoverinfo="text",
                               hovertext=catbeneficiaire
                              )
                  )

fig2.update_layout(legend=dict(orientation="h", font=dict(size=12)), font=graph_fontstyle)

data_sansindetermine = data[data['catbeneficiaire'] != 'Bénéficiaires de type indéterminé']
data_feder_p1 = data_sansindetermine.loc[(data_sansindetermine['Fonds'] == 'FEDER') & (data_sansindetermine['Palier'] == 'P1'), 'catbeneficiaire'].value_counts(normalize=True, dropna=False).sort_index()
data_feder_p2 = data_sansindetermine.loc[(data_sansindetermine['Fonds'] == 'FEDER') & (data_sansindetermine['Palier'] == 'P2'), 'catbeneficiaire'].value_counts(normalize=True, dropna=False).sort_index()
data_fse_p1 = data_sansindetermine.loc[(data_sansindetermine['Fonds'] == 'FSE') & (data_sansindetermine['Palier'] == 'P1'), 'catbeneficiaire'].value_counts(normalize=True, dropna=False).sort_index()
data_fse_p2 = data_sansindetermine.loc[(data_sansindetermine['Fonds'] == 'FSE') & (data_sansindetermine['Palier'] == 'P2'), 'catbeneficiaire'].value_counts(normalize=True, dropna=False).sort_index()

fig4a = go.Figure(data=[
    go.Bar(name='Nombre de projets « courants »', orientation='h', x=data_feder_p1, y=data_feder_p1.index, hoverinfo='none'),
    go.Bar(name='Nombre de projets « d’ampleur »', orientation='h', x=data_feder_p2, y=data_feder_p2.index, hoverinfo='none')
])
fig4a.update_layout(barmode='stack',
                    xaxis=dict(tickformat='%'),
                    margin = dict(l=0, r=0, t=10, b=40),
                    legend = dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="right", x=0.78),
                    dragmode=False)

fig4b = go.Figure(data=[
    go.Bar(name='Nombre de projets « courants »', orientation='h', x=data_fse_p1, y=data_fse_p1.index, hoverinfo='none'),
    go.Bar(name='Nombre de projets « d’ampleur »', orientation='h', x=data_fse_p2, y=data_fse_p2.index, hoverinfo='none')
])
fig4b.update_layout(barmode='stack',
                    xaxis=dict(tickformat='%'),
                    margin = dict(l=0, r=0, t=10, b=40),
                    legend = dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="right", x=0.78),
                    dragmode=False)

fig5 = go.Figure(layout = dict(
                               polar = dict(
                                   radialaxis = dict(
                                       visible = True,
                                       showticklabels=True,
                                       # range = [0, 1],
                                       tickvals = [0.25, 0.5, 0.75],
                                       ticktext = ['25%', '50%', '75%']
                                   ),
                                   angularaxis = dict(
                                       tickmode = "array",
                                       tickvals = [x*(360/len(data_pivot.index)) for x in range(0, len(data_pivot.index))],
                                       ticktext = data_pivot.index
                                   )),
                               showlegend = False,
                               autosize=True
                               ))

fig5.add_trace(go.Barpolar(base="stack", opacity=0.6, marker_color="#57575F", hoverinfo="none"))
fig5.add_trace(go.Barpolar(base="stack", opacity=0.6, marker_color="#CA3542", hoverinfo="none"))

buttons1 = [dict(method = "restyle",
                 args = [{'r': [data_pivot[catbeneficiaire] / data_pivot[catbeneficiaire].sum()]}, 0],
                 label = catbeneficiaire) for catbeneficiaire in data_pivot.columns]

buttons2 = [dict(method = "restyle",
                 args = [{'r': [data_pivot[catbeneficiaire] / data_pivot[catbeneficiaire].sum()]}, 1],
                 label = catbeneficiaire) for catbeneficiaire in data_pivot.columns]

fig5.update_layout(updatemenus=[dict(active=-1, buttons=buttons1, xanchor="left", x=-0.05, yanchor="top", y=1.39, bgcolor="#d4d4d7"),
                                dict(active=-1, buttons=buttons2, xanchor="right", x=1.05, yanchor="top", y=1.39, bgcolor="#f1cccf")],
                   margin=dict(l=50, r=50, t=150, b=50),
                   dragmode=False,
                   font=graph_fontstyle
                  )

categories_duree = ["moins d'un an", "entre un et deux ans", "entre deux et trois ans", "plus de trois ans"]
palette_bleus = ['blue', 'cornflowerblue', 'SkyBlue', 'LightSteelBlue']

fig10c = go.Figure(go.Treemap(
    labels = categories_duree,
    parents = ['FSE', 'FSE', 'FSE', 'FSE'],
    values = [14389, 4989, 2809, 171],
    text = ['64%', '22%', '13%', '< 1%'],
    textposition = "middle center",
    sort = False,
    hoverinfo = "none",
    marker_colors = palette_bleus
    ),
                 layout=dict(font=graph_fontstyle),
    
    )

fig10d = go.Figure(go.Treemap(
    labels = categories_duree,
    parents = ['FEDER', 'FEDER', 'FEDER', 'FEDER'],
    values = [2778, 3685, 4273, 3970],
    text = ['19%', '25%', '29%', '27%'],
    textposition = "middle center",
    sort = False,
    hoverinfo = "none",
    marker_colors = palette_bleus
    ),
                 layout=dict(font=graph_fontstyle),
    
    )

app.layout = html.Div(children=[
    html.H1(['Comment sont utilisés les fonds européens en France ?', html.Br(), 'Analyse des projets FEDER et FSE de la période 2014-2020']),

    html.Div([
        dcc.Markdown(children=partie1_md)
    ], className="paragraph"),

    html.Div([
        html.H2('2. Typologie des opérations'),
        html.Div([dcc.Markdown(children=partie2_md_a)], className="five columns"),
        html.Div([
            dcc.Graph(
            id='repartition_montants',
            figure=fig1,
            config={'displayModeBar': False}
        )], className="one-half column"),
        html.Div([dcc.Markdown(children=partie2_md_b)], className="twelve columns"),
    ], className="row"),

    html.Div([
        dcc.Markdown(children=partie3_md)
    ], className="paragraph"),

    html.Figure([
        html.Figcaption('Apport en fonds européens des catégories de bénéficiaires aux différentes thématiques'),
        dcc.Graph(
            id='apport_beneficiaires_thematiques',
            figure=fig2,
            config={'displayModeBar': False},
            style={'width':'100%', 'height':'100vh'}
        )
    ]),

    html.Div([
        dcc.Markdown(children=partie4_md)
    ], className="paragraph"),

    html.Figure([
        html.Figcaption('Répartition des opérations FEDER par catégorie de bénéficiaire et de projet'),
        dcc.Graph(
            id='paliers_operations_feder',
            figure=fig4a,
            config={'displayModeBar': False},
            style={'width':'90%'}
        )
    ]),

    html.Figure([
        html.Figcaption('Répartition des opérations FSE par catégorie de bénéficiaire et de projet'),
        dcc.Graph(
            id='paliers_operations_fse',
            figure=fig4b,
            config={'displayModeBar': False},
            style={'width':'90%'}
        )
    ]),

    html.Div([
        dcc.Markdown(children=partie5_md)
    ], className="paragraph"),

    html.Figure([
        html.Figcaption('Comparaison des usages des fonds européens entre catégories de bénéficiaires'),
        dcc.Graph(
            id='comparaison_usages_fonds',
            figure=fig5,
            config={'displayModeBar': False},
            style={'width':'95%', 'height':'75vh'}
        )
    ]),

    html.Div([
        html.Div([dcc.Markdown(children=partie5_md_focus_assos)], className="five columns"),
        html.Div([dcc.Markdown(children=partie5_md_focus_entreprises)], className="seven columns")
    ], className="row"),

    html.Div([
        dcc.Markdown(children=partie6_md)
    ], className="paragraph"),

    html.Div([
        dcc.Markdown(children=partie7_md)
    ], className="paragraph"),

    html.Div([
        dcc.Markdown(children=partie8_md)
    ], className="paragraph"),

    html.Div([
        dcc.Markdown(children=partie9_md)
    ], className="paragraph"),

    html.Div([
        dcc.Markdown(children=partie10_md)
    ], className="paragraph"),

    html.Figure([
        html.Figcaption('Distribution des projets en fonction de la durée des opérations'),
        dcc.Graph(
            id='distribution_durees_fse',
            figure=fig10c,
            config={'displayModeBar': False}),
        dcc.Graph(
            id='distribution_durees_feder',
            figure=fig10d,
            config={'displayModeBar': False}),
    ]),

    html.Div([
        dcc.Markdown(children=partie11_md)
    ], className="paragraph"),

    html.Div([
        dcc.Markdown(children=apropos_md)
    ], className="paragraph"),

],
    className="container"
)

if __name__ == '__main__':
    app.run_server(debug=True)
