import json
import os
from groq import Groq

client = Groq(

    api_key=os.environ.get("GROQ_API_KEY", "PUNE_CHEIA_TA_AICI_din_motive_de_securitate_github_nu_am_putut_incarca"),
)


def incarca_ocupatii(cale_fisier):
    try:
        with open(cale_fisier, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def analizeaza_si_potriveste(descriere_candidat, lista_ocupatii):
    instructiune_sistem = (
        "Ești un expert în HR și arhitectura muncii (COR, ESCO, SFIA). "
        "Sarcina 1: Evaluează nivelul SFIA al candidatului (1-7) bazat pe text (ex: student/începător=1-2, autonom=3-4, senior=5+). "
        "Sarcina 2: Găsește cea mai bună potrivire din baza de date JSON oferită. "
        "Trebuie să returnezi STRICT un obiect JSON cu următoarele chei: "
        "'sfia_estimat_candidat' (int), 'id_ocupatie' (string), 'cor' (string), "
        "'procent_potrivire' (int), 'justificare_sfia_si_esco' (string)."
    )

    prompt = f"""
    Baza de date (COR, ESCO, SFIA):
    {json.dumps(lista_ocupatii, ensure_ascii=False, indent=2)}

    Profilul candidatului de analizat:
    "{descriere_candidat}"
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": instructiune_sistem},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
        response_format={"type": "json_object"},
        temperature=0.1,
    )

    return chat_completion.choices[0].message.content


if __name__ == "__main__":
    ocupatii = incarca_ocupatii('ocupatii.json')

    if ocupatii:
        profil_test = "Sunt în anul 2 la inginerie, scriu cod în Java și Python. Am făcut laboratoare de sisteme de operare, am ajutat la un simulator de drone, dar încă am nevoie de îndrumare pentru proiecte cap-coadă."

        print("Se analizează profilul conform COR, ESCO și SFIA...\n")
        rezultat_brut = analizeaza_si_potriveste(profil_test, ocupatii)

        rezultat_json = json.loads(rezultat_brut)
        print(json.dumps(rezultat_json, indent=2, ensure_ascii=False))