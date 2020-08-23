from bs4 import BeautifulSoup
import requests
import re
import json
import os


def get_transcript_ted(url):
    if "ted" not in str(url):
        raise Exception("URL Inválida")

    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    transcript = soup("div", {"class": "Grid Grid--with-gutter d:f@md p-b:4"})
    texts = []
    for div in transcript:
        text = div("p")[0].text
        text = text.strip()
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")
        text = re.sub(' +', ' ', text)
        texts.append(text)

    _ = soup.title.text
    author = _.split(":")[0].strip()
    title = _.split(":")[1].split("|")[0].strip()
    return {
        "title": title,
        "author": author,
        "body": " ".join(texts),
        "type": "video",
        "url": url
    }


def get_text_olhar_digital(url):
    if "olhardigital" not in str(url):
        raise Exception("URL Inválida")

    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    transcript = soup(
        "article", {"class": "mat-container"})[0]("div", {"class": "mat-txt"})
    texts = []
    for div in transcript:
        _ = div("p")
        for p in _:
            text = p.text
            text = text.strip()
            text = text.replace("\n", " ")
            text = text.replace("\t", " ")
            text = re.sub(' +', ' ', text)
            texts.append(text)

    try:
        author = soup("h1", {"class": "cln-nom"})[0].text
    except IndexError:
        author = soup("span", {"class": "meta-item meta-aut"})[0].text
        if "," in author:
            author = author.split(",")[0]
    except:
        raise Exception("Verifique o codigo")

    title = soup("h1", {"class": "mat-tit"})[0].text
    return {
        "title": title,
        "author": author,
        "body": " ".join(texts),
        "type": "article",
        "url": url
    }


def get_text_startse(url):
    if "startse" not in str(url):
        raise Exception("URL Inválida")

    response = requests.get(url)
    soup = BeautifulSoup(response.content)
    transcript = soup("span", {"style": "font-weight: 400;"})
    texts = []
    for p in transcript:
        text = p.text
        text = text.strip()
        text = text.replace("\n", " ")
        text = text.replace("\t", " ")
        text = re.sub(' +', ' ', text)
        texts.append(text)

    author = soup("div", {"class": "title-single__info"}
                  )[0]("h4")[0]("a")[0].text
    title = soup("div", {"class": "title-single__title"})[0]("h2")[0].text
    return {
        "title": title,
        "author": author,
        "body": " ".join(texts),
        "type": "article",
        "url": url
    }


def save_json(data):
    path = data["title"].replace(":", "") 
    path = path.replace(" ", "_") + ".json"
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    tedUrls = [
        "https://www.ted.com/talks/helen_czerski_the_fascinating_physics_of_everyday_life/transcript?language=pt-br#t-81674",
        "https://www.ted.com/talks/kevin_kelly_how_ai_can_bring_on_a_second_industrial_revolution/transcript?language=pt-br",
        "https://www.ted.com/talks/sarah_parcak_help_discover_ancient_ruins_before_it_s_too_late/transcript?language=pt-br",
        "https://www.ted.com/talks/sylvain_duranton_how_humans_and_ai_can_work_together_to_create_better_businesses/transcript?language=pt-br",
        "https://www.ted.com/talks/chieko_asakawa_how_new_technology_helps_blind_people_explore_the_world/transcript?language=pt-br",
        "https://www.ted.com/talks/pierre_barreau_how_ai_could_compose_a_personalized_soundtrack_to_your_life/transcript?language=pt-br",
        "https://www.ted.com/talks/tom_gruber_how_ai_can_enhance_our_memory_work_and_social_lives/transcript?language=pt-br",
    ]

    olhardigitalUrls = [
        "https://olhardigital.com.br/colunistas/wagner_sanchez/post/o_futuro_cada_vez_mais_perto/78972",
        "https://olhardigital.com.br/colunistas/wagner_sanchez/post/os_riscos_do_machine_learning/80584",
        "https://olhardigital.com.br/ciencia-e-espaco/noticia/nova-teoria-diz-que-passado-presente-e-futuro-coexistem/97786",
        "https://olhardigital.com.br/noticia/inteligencia-artificial-da-ibm-consegue-prever-cancer-de-mama/87030",
        "https://olhardigital.com.br/ciencia-e-espaco/noticia/inteligencia-artificial-ajuda-a-nasa-a-projetar-novos-trajes-espaciais/102772",
        "https://olhardigital.com.br/colunistas/jorge_vargas_neto/post/como_a_inteligencia_artificial_pode_mudar_o_cenario_de_oferta_de_credito/78999",
        "https://olhardigital.com.br/ciencia-e-espaco/noticia/cientistas-criam-programa-poderoso-que-aprimora-deteccao-de-galaxias/100683"
    ]

    startseUrls = [
        "https://www.startse.com/noticia/startups/mobtech/deep-learning-o-cerebro-dos-carros-autonomos"
    ]

    for item in tedUrls:
        data = get_transcript_ted(item)
        save_json(data)

    for item in olhardigitalUrls:
        data = get_text_olhar_digital(item)
        save_json(data)

    for item in startseUrls:
        data = get_text_startse(item)
        save_json(data)
